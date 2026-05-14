"""
Relation Extractor — Extraction statique des relations sémantiques
==================================================================
Détecte deux patterns dans le raw_code des entry_points :

Pattern A — Comparison-then-assignment (implies) :
    if ($code === 'TP2') { $criteres['C_TYP_FLX'] = 2; }
    Condition : le token comparé doit exister dans la KB.
    Confiance : medium (la relation n'est pas encore validée PO).

Pattern B — Tableau de mapping littéral (synonym_of) :
    $CODES_TYPE = ['TP1' => 1, 'TP2' => 2, 'TP3' => 3]
    Capture la définition au point de déclaration uniquement, pas les
    utilisations. Au moins un token du tableau doit exister en KB.
    Confiance : medium (la colonne réelle est inférée du nom du tableau
    PHP — à confirmer par PO).

Faux positifs : filtrés par l'existence en KB du token gauche.
Scope domaine : une relation extraite dans un fichier donné reste
    scoped à ce domaine — pas de promotion globale sans validation PO.
Transitivité : jamais générée automatiquement.
"""

import re
from typing import Callable

from ir.schema import CodeRef, EntityRef, Flag, IRSchema, Relation


# ---------------------------------------------------------------------------
# Scanner général — tous les littéraux entre guillemets (MAJ + camelCase)
# Filtré par kb_token_exists pour éviter l'explosion de faux positifs.
# ---------------------------------------------------------------------------

_PAT_LITERAL = re.compile(r"""['\"](?P<token>[a-zA-Z_]\w{1,39})['\"]""")

# ---------------------------------------------------------------------------
# Pattern A — if ($var === 'TOKEN') { $arr['KEY'] = val; }
# ---------------------------------------------------------------------------

_PAT_A_IF = re.compile(
    r"if\s*\(\s*\$\w+(?:\[['\"]\w+['\"]\])?\s*===?\s*['\"](?P<lhs>[\w_]+)['\"]\s*\)"
    r"\s*\{(?P<body>[^}]{0,600})\}",
    re.DOTALL,
)

# Assignation de tableau dans le corps du if : $arr['COL'] = val;
_PAT_A_ASSIGN = re.compile(
    r"\$\w*\[['\"](?P<col>[\w_]+)['\"]\]\s*=\s*(?P<val>[^;,\n\]]{1,60});?",
)

# Appel de service dans le corps du if : $var = $this->app->get('Svc')->method(...)
_PAT_A_SVC = re.compile(
    r"\$(?P<var>[\w_]+)\s*=\s*\$this->(?:app->get\(['\"](?P<svc>[\w_]+)['\"]\)|(?P<prop>[\w_]+))"
    r"->(?P<meth>[\w_]+)\s*\(",
)

# ---------------------------------------------------------------------------
# Pattern B — $VAR = ['K' => V, ...] ou const K = [...]
# ---------------------------------------------------------------------------

_PAT_B_DEF = re.compile(
    r"(?P<varname>(?:\$[\w_]+|const\s+[\w_]+))\s*=\s*"
    r"(?:\[\s*|array\s*\(\s*)"
    r"(?P<pairs>(?:['\"][\w_]+['\"]\s*=>\s*['\"]?[\w_]+['\"]?\s*,?\s*){2,})"
    r"\s*[\]\)]",
    re.DOTALL,
)

_PAT_B_PAIR = re.compile(
    r"['\"](?P<key>[\w_]+)['\"]\s*=>\s*(?P<val>['\"]?[\w_]+['\"]?)",
)


class RelationExtractor:
    """Extrait les relations sémantiques depuis un IRSchema.

    Args:
        kb_token_exists: Callable O(1) retournant True si un token est connu en KB.
                         Usage prod  : ``known_tokens.__contains__``
                         Usage tests : ``lambda t: t in {"TP1", "TP2"}``
    """

    def __init__(self, kb_token_exists: Callable[[str], bool] = lambda _: False):
        self._kb_exists = kb_token_exists
        self._counter = 0

    def _next_id(self) -> str:
        self._counter += 1
        return f"rel_{self._counter:04d}"

    def extract(self, ir: IRSchema) -> list[Relation]:
        """Extrait les relations et peuple Flag.see_also en post-processing."""
        self._counter = 0
        relations: list[Relation] = []

        for ep in ir.entry_points:
            if not ep.raw_code:
                continue
            method = ep.name or ep.original_name or "unknown"
            source_file = ir.metadata.source_file
            base_line = ep.start_line or 0

            relations.extend(self._extract_literals(ep.raw_code, method, source_file, base_line))
            relations.extend(self._extract_pattern_a(ep.raw_code, method, source_file, base_line))
            relations.extend(self._extract_pattern_b(ep.raw_code, method, source_file, base_line))

        self._link_see_also(relations, ir.flags)
        return relations

    # -------------------------------------------------------------------------
    # Scanner général : littéraux entre guillemets filtrés par KB
    # -------------------------------------------------------------------------

    def _extract_literals(
        self, code: str, method: str, source_file: str, base_line: int
    ) -> list[Relation]:
        rels: list[Relation] = []
        seen: set[str] = set()

        for m in _PAT_LITERAL.finditer(code):
            token = m.group("token")
            if token in seen or not self._kb_exists(token):
                continue
            seen.add(token)
            abs_line = base_line + code[: m.start()].count("\n")
            rels.append(Relation(
                id=self._next_id(),
                kind="mentions",
                from_entity=EntityRef(type="literal", value=token),
                to_entity=EntityRef(type="method", value=method),
                direction="one_way",
                confiance="inferred",
                trouvé_dans=[CodeRef(fichier=source_file, methode=method, ligne=abs_line)],
                semantique=f"Le token KB `{token}` apparaît littéralement dans `{method}`.",
                pattern="literal_scan",
            ))
        return rels

    # -------------------------------------------------------------------------
    # Pattern A
    # -------------------------------------------------------------------------

    def _extract_pattern_a(
        self, code: str, method: str, source_file: str, base_line: int
    ) -> list[Relation]:
        rels: list[Relation] = []
        seen: set[tuple] = set()

        for m in _PAT_A_IF.finditer(code):
            lhs = m.group("lhs")
            if not self._kb_exists(lhs):
                continue

            body = m.group("body")
            abs_line = base_line + code[: m.start()].count("\n")

            for assign in _PAT_A_ASSIGN.finditer(body):
                col = assign.group("col")
                val = assign.group("val").strip().strip("'\"")
                key = (lhs, col, val)
                if key in seen:
                    continue
                seen.add(key)

                rels.append(Relation(
                    id=self._next_id(),
                    kind="implies",
                    from_entity=EntityRef(type="code", value=lhs),
                    to_entity=EntityRef(type="column_value", value=f"{col} = {val}"),
                    direction="one_way",
                    confiance="medium",
                    trouvé_dans=[CodeRef(fichier=source_file, methode=method, ligne=abs_line)],
                    semantique=(
                        f"Le code `{lhs}` implique l'assignation `{col} = {val}` "
                        f"dans la méthode `{method}`."
                    ),
                    pattern="pattern_a",
                ))

            # Pattern A-bis : corps avec appel de service ($var = $this->svc->meth())
            if not _PAT_A_ASSIGN.search(body):
                for svc_m in _PAT_A_SVC.finditer(body):
                    svc = svc_m.group("svc") or svc_m.group("prop") or ""
                    meth = svc_m.group("meth")
                    target = f"{svc}::{meth}" if svc else meth
                    key = (lhs, target)
                    if key in seen:
                        continue
                    seen.add(key)
                    rels.append(Relation(
                        id=self._next_id(),
                        kind="implies",
                        from_entity=EntityRef(type="code", value=lhs),
                        to_entity=EntityRef(type="service_call", value=target),
                        direction="one_way",
                        confiance="medium",
                        trouvé_dans=[CodeRef(fichier=source_file, methode=method, ligne=abs_line)],
                        semantique=(
                            f"Le code `{lhs}` route vers `{target}` "
                            f"dans la méthode `{method}`."
                        ),
                        pattern="pattern_a",
                    ))
        return rels

    # -------------------------------------------------------------------------
    # Pattern B
    # -------------------------------------------------------------------------

    def _extract_pattern_b(
        self, code: str, method: str, source_file: str, base_line: int
    ) -> list[Relation]:
        rels: list[Relation] = []
        seen: set[tuple] = set()

        for m in _PAT_B_DEF.finditer(code):
            pairs_str = m.group("pairs")
            varname = m.group("varname").strip()
            abs_line = base_line + code[: m.start()].count("\n")

            pairs = [(p.group("key"), p.group("val")) for p in _PAT_B_PAIR.finditer(pairs_str)]
            if not pairs:
                continue

            # Filtrer : au moins un token du tableau doit exister en KB
            if not any(self._kb_exists(k) for k, _ in pairs):
                continue

            for key_str, val_raw in pairs:
                val_str = val_raw.strip().strip("'\"")
                dedup = (varname, key_str, val_str)
                if dedup in seen:
                    continue
                seen.add(dedup)

                rels.append(Relation(
                    id=self._next_id(),
                    kind="synonym_of",
                    from_entity=EntityRef(type="code", value=key_str),
                    to_entity=EntityRef(type="column_value", value=f"{varname} → {val_str}"),
                    direction="bidirectional",
                    confiance="medium",
                    conditions=[
                        f"Mapping déclaratif via tableau `{varname}` — "
                        f"résolution vers colonne SQL à confirmer par PO"
                    ],
                    trouvé_dans=[CodeRef(fichier=source_file, methode=method, ligne=abs_line)],
                    semantique=(
                        f"Le code `{key_str}` est mappé à `{val_str}` via `{varname}`. "
                        f"La colonne SQL réelle est à confirmer par PO."
                    ),
                    pattern="pattern_b",
                ))
        return rels

    # -------------------------------------------------------------------------
    # Post-processing : liaison flags ↔ relations via see_also
    # -------------------------------------------------------------------------

    def _link_see_also(self, relations: list[Relation], flags: list[Flag]) -> None:
        """Peuple Flag.see_also avec les IDs des relations voisines (même méthode, ±10 lignes)."""
        for rel in relations:
            if not rel.trouvé_dans:
                continue
            ref = rel.trouvé_dans[0]
            rel_line = ref.ligne or 0
            rel_method = ref.methode

            for flag in flags:
                # Filtrer par méthode si les deux sont renseignées
                if rel_method and flag.method_name and flag.method_name != rel_method:
                    continue

                flag_line = flag.source_line or 0
                if flag_line == 0 and rel_line == 0:
                    # Aucun numéro de ligne : matcher sur le token dans le fragment
                    if rel.from_entity.value in (flag.fragment or ""):
                        flag.see_also.append(rel.id)
                elif abs(flag_line - rel_line) <= 10:
                    flag.see_also.append(rel.id)
