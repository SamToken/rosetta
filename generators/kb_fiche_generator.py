"""
KB Fiche Generator — Génère des fiches KB Rosetta depuis les insights LLM
==========================================================================
Prend un IRSchema enrichi et écrit des fiches .md (format KB avec frontmatter)
directement dans le répertoire cible.

Règles :
- 1 fiche par (méthode, type_flag) — pas 1 par flag (évite l'explosion)
- confiance: medium toujours — seul un humain (PO) monte en high
- Skip si fiche existante avec confiance: high
- sha256 du fichier source calculé localement
- Nommage : {kb_type}_{METHOD}_{FLAG_SHORT}.md
"""

import hashlib
import re
import subprocess
from datetime import date
from pathlib import Path
from typing import Optional

from ir.schema import IRSchema, Flag, LLMInsight, BugFinding, Relation


# ---------------------------------------------------------------------------
# Tables de mapping
# ---------------------------------------------------------------------------

_FLAG_SHORT: dict[str, str] = {
    "missing_branch":            "BRANCH",
    "magic_value":               "MAGIC",
    "security_risk":             "SECURITY",
    "unmapped_dep":              "DEP",
    "business_logic_unclear":    "LOGIC",
    "side_effect":               "SIDE_EFFECT",
    "dynamic_session_key":       "SESSION",
    "chained_api_call":          "CHAINED_API",
    "situation_coverage":        "SITUATION",
    "external_state_dependency": "EXTERNAL_STATE",
    "module_execution_gap":      "MODULE_GAP",
    "hardcoded_situation_code":  "HARDCODED",
    "empty_catch":               "EMPTY_CATCH",
    "strong_coupling":           "COUPLING",
    "chained_method_call":       "CHAINED",
}

_FLAG_KB_TYPE: dict[str, str] = {
    "security_risk":            "bug",
    "empty_catch":              "bug",
    "magic_value":              "code",
    "hardcoded_situation_code": "code",
}

_FLAG_LABEL: dict[str, str] = {
    "missing_branch":            "Branche manquante — décision métier sans cas par défaut",
    "magic_value":               "Valeur magique — constante sans libellé documenté",
    "security_risk":             "Risque de sécurité",
    "unmapped_dep":              "Dépendance non documentée",
    "business_logic_unclear":    "Logique métier ambiguë",
    "side_effect":               "Effet de bord — email ou écriture après opération principale",
    "dynamic_session_key":       "Clé de session dynamique — risque stale data",
    "chained_api_call":          "Appels API séquentiels sans validation intermédiaire",
    "situation_coverage":        "Couverture de situation incomplète",
    "external_state_dependency": "Dépendance service externe sans fallback",
    "module_execution_gap":      "Séquence de modules — échec silencieux possible",
    "hardcoded_situation_code":  "Code de situation hardcodé",
    "empty_catch":               "Catch vide — exception avalée silencieusement",
    "strong_coupling":           "Couplage fort — services injectés manuellement",
    "chained_method_call":       "Appels de méthodes chaînés sans garde",
}

_BUG_LABEL: dict[str, str] = {
    "uninit_variable":        "Variable non initialisée réutilisée entre cases",
    "php82_compat":           "Incompatibilité PHP 8.2",
    "operator_precedence":    "Précédence opérateurs ambiguë",
    "strpos_type_unsafe":     "strpos sans comparaison === false",
    "date_format_invalid":    "Format date() invalide",
    "switch_fallthrough":     "Switch fallthrough non intentionnel",
    "foreach_null_guard":     "foreach sur variable potentiellement null",
    "sleep_blocking":         "sleep() bloquant dans worker PHP",
    "instance_state_mutation":"Mutation d'état d'instance dans méthode réentrante",
    "null_dereference":       "Déréférencement de null",
    "array_access_unchecked": "Accès tableau sans isset()",
    "finally_scope_logic":    "Code métier après finally non atteint si exception",
    "parameter_order":        "Arguments inversés par rapport à la signature",
}


# ---------------------------------------------------------------------------
# Classe principale
# ---------------------------------------------------------------------------

class KBFicheGenerator:
    """
    Génère des fiches KB .md depuis un IRSchema enrichi.

    Usage :
        gen = KBFicheGenerator(Path("~/projects/rosetta/kb"), domain="mon-domaine")
        created, updated, skipped = gen.generate(ir, php_path)
    """

    def __init__(self, kb_output_dir: Path, domain: Optional[str] = None):
        self.kb_output_dir = Path(kb_output_dir).expanduser()
        self.domain = domain

    def generate(
        self,
        ir: IRSchema,
        php_source_path: Optional[Path] = None,
    ) -> tuple[int, int, int]:
        """
        Génère les fiches KB.
        Retourne (nb_créées, nb_mises_à_jour, nb_ignorées).
        """
        domain = self.domain or _infer_domain(ir.metadata.controller_name)
        out_dir = self.kb_output_dir / domain
        out_dir.mkdir(parents=True, exist_ok=True)

        file_hash = _file_hash(php_source_path) if php_source_path else "sha256:inconnu"
        git_commit, git_date = _git_info(php_source_path)
        source_file = ir.metadata.source_file

        insight_by_flag: dict[str, LLMInsight] = {
            ins.flag_id: ins for ins in ir.llm_insights
        }

        # Grouper par (méthode, type_flag)
        groups: dict[tuple[str, str], list[Flag]] = {}
        for flag in ir.flags:
            method = flag.method_name or flag.location or "unknown"
            key = (method, str(flag.type))
            groups.setdefault(key, []).append(flag)

        created = updated = skipped = 0

        for (method, flag_type), flags in sorted(groups.items()):
            insights = [insight_by_flag[f.id] for f in flags if f.id in insight_by_flag]
            if not insights:
                continue

            kb_type = _FLAG_KB_TYPE.get(flag_type, "regle")
            kb_nom = _make_nom(method, flag_type)
            fiche_path = out_dir / f"{kb_type}_{kb_nom}.md"

            if fiche_path.exists() and _is_high_confidence(fiche_path):
                skipped += 1
                continue

            content = _render_fiche(
                kb_type=kb_type, kb_nom=kb_nom,
                method=method, flag_type=flag_type,
                flags=flags, insights=insights,
                source_file=source_file, domain=domain,
                file_hash=file_hash,
                git_commit=git_commit, git_date=git_date,
            )
            existed = fiche_path.exists()
            fiche_path.write_text(content, encoding="utf-8")
            updated += existed
            created += not existed

        # Fiches bug (--bug-check)
        if ir.bug_findings:
            bug_groups: dict[tuple[str, str], list[BugFinding]] = {}
            for bug in ir.bug_findings:
                key = (bug.method_name or "unknown", bug.category.value)
                bug_groups.setdefault(key, []).append(bug)

            for (method, category), bugs in sorted(bug_groups.items()):
                kb_nom = _make_nom(method, category)
                fiche_path = out_dir / f"bug_{kb_nom}.md"

                if fiche_path.exists() and _is_high_confidence(fiche_path):
                    skipped += 1
                    continue

                content = _render_bug_fiche(
                    kb_nom=kb_nom, method=method, bugs=bugs,
                    source_file=source_file, domain=domain,
                    file_hash=file_hash,
                    git_commit=git_commit, git_date=git_date,
                )
                existed = fiche_path.exists()
                fiche_path.write_text(content, encoding="utf-8")
                updated += existed
                created += not existed

        return created, updated, skipped

    def generate_relations(
        self,
        ir: IRSchema,
        php_source_path: Optional[Path] = None,
    ) -> tuple[int, int, int]:
        """Génère les fiches KB pour les relations extraites. Retourne (créées, mises_à_jour, ignorées)."""
        if not ir.relations:
            return 0, 0, 0

        domain = self.domain or _infer_domain(ir.metadata.controller_name)
        out_dir = self.kb_output_dir / domain
        out_dir.mkdir(parents=True, exist_ok=True)

        file_hash = _file_hash(php_source_path) if php_source_path else "sha256:inconnu"
        git_commit, git_date = _git_info(php_source_path)

        created = updated = skipped = 0
        seen: set[tuple] = set()

        for rel in ir.relations:
            dedup_key = (rel.kind, rel.from_entity.value, rel.to_entity.value)
            if dedup_key in seen:
                continue
            seen.add(dedup_key)

            nom = _make_relation_nom(rel)
            fiche_path = out_dir / f"relation_{nom}.md"

            if fiche_path.exists() and _is_high_confidence(fiche_path):
                skipped += 1
                continue

            content = _render_relation_fiche(
                rel=rel, domain=domain,
                file_hash=file_hash, git_commit=git_commit, git_date=git_date,
            )
            existed = fiche_path.exists()
            fiche_path.write_text(content, encoding="utf-8")
            updated += existed
            created += not existed

        return created, updated, skipped


# ---------------------------------------------------------------------------
# Rendu Markdown
# ---------------------------------------------------------------------------

def _render_fiche(
    kb_type: str, kb_nom: str,
    method: str, flag_type: str,
    flags: list[Flag], insights: list[LLMInsight],
    source_file: str, domain: str,
    file_hash: str, git_commit: str, git_date: str,
) -> str:
    label = _FLAG_LABEL.get(flag_type, flag_type)
    anchor_method = method
    anchor_logic = _first_line(flags[0].fragment) if flags else ""
    lignes = _line_range(flags)

    # Sémantique : joindre les règles uniques
    semantique_parts = list(dict.fromkeys(
        ins.business_rule for ins in insights if ins.business_rule
    ))
    semantique = "\n\n".join(semantique_parts[:3])

    # Questions PO
    questions = list(dict.fromkeys(
        ins.missing_context for ins in insights
        if ins.missing_context
    ))

    # Fragments
    fragments = list(dict.fromkeys(f.fragment for f in flags))[:5]

    # Trouvé dans
    trouvé = _trouvé_dans(flags, source_file)

    # Confiance moyenne
    avg_conf = sum(i.confidence for i in insights) / len(insights)
    confiance = "high" if avg_conf >= 0.80 else "medium"
    confiance = "medium"  # jamais high en automatique

    fm = _frontmatter(
        kb_type=kb_type, kb_nom=kb_nom,
        kb_fichier=source_file, kb_lignes=lignes,
        kb_domaine=domain, kb_confiance=confiance,
        anchor_method=anchor_method, anchor_logic=anchor_logic,
        file_hash=file_hash, git_commit=git_commit, git_date=git_date,
    )

    sections = [fm]
    sections.append(f"## Label\n{label} — `{method}`")
    sections.append(f"## Sémantique\n{semantique}")

    if fragments:
        frag_lines = "\n".join(f"```\n{f}\n```" for f in fragments[:3])
        sections.append(f"## Concepts\n{frag_lines}")

    if questions:
        q_lines = "\n".join(f"- {q}" for q in questions)
        sections.append(f"## Conditions\n{q_lines}")

    sections.append(f"## Trouvé dans\n{trouvé}")
    sections.append("## Impact Migration Symfony\n_(à compléter après validation PO)_")
    sections.append("## Notes\n_(généré automatiquement — confiance: medium — à valider PO)_")

    return "\n\n".join(sections) + "\n"


def _render_bug_fiche(
    kb_nom: str, method: str, bugs: list[BugFinding],
    source_file: str, domain: str,
    file_hash: str, git_commit: str, git_date: str,
) -> str:
    label = _BUG_LABEL.get(bugs[0].category.value, bugs[0].category.value)
    anchor_logic = _first_line(bugs[0].fragment) if bugs else ""

    fm = _frontmatter(
        kb_type="bug", kb_nom=kb_nom,
        kb_fichier=source_file, kb_lignes="",
        kb_domaine=domain, kb_confiance="medium",
        anchor_method=method, anchor_logic=anchor_logic,
        file_hash=file_hash, git_commit=git_commit, git_date=git_date,
    )

    descriptions = "\n".join(
        f"- **[{b.severity.value.upper()}]** {b.description}" for b in bugs
    )
    fixes = "\n".join(f"- {b.fix}" for b in bugs if b.fix)
    fragments = "\n".join(f"```php\n{b.fragment}\n```" for b in bugs[:3])

    sections = [fm]
    sections.append(f"## Label\nBug — {label} — `{method}`")
    sections.append(f"## Sémantique\n{descriptions}")
    sections.append(f"## Concepts\n{fragments}")
    if fixes:
        sections.append(f"## Conditions\n**Corrections suggérées :**\n{fixes}")
    sections.append(f"## Trouvé dans\n- `{source_file}` — `{method}()`")
    sections.append("## Impact Migration Symfony\n_(corriger avant migration — ne pas reproduire le bug)_")
    sections.append("## Notes\n_(généré automatiquement — confiance: medium — à valider)_")

    return "\n\n".join(sections) + "\n"


def _frontmatter(
    kb_type: str, kb_nom: str,
    kb_fichier: str, kb_lignes: str,
    kb_domaine: str, kb_confiance: str,
    anchor_method: str, anchor_logic: str,
    file_hash: str, git_commit: str, git_date: str,
) -> str:
    today = str(date.today())
    anchor_logic_safe = anchor_logic.replace('"', "'")[:80]
    return (
        "---\n"
        f"kb_type: {kb_type}\n"
        f"kb_nom: {kb_nom}\n"
        f"kb_fichier: {kb_fichier}\n"
        f"kb_lignes: \"{kb_lignes}\"\n"
        f"kb_source: \"Rosetta KB-Fiche-Generator — généré {today}\"\n"
        f"kb_domaine: {kb_domaine}\n"
        f"kb_confiance: {kb_confiance}\n"
        f"kb_anchor_method: {anchor_method}\n"
        f"kb_anchor_logic: \"{anchor_logic_safe}\"\n"
        f"kb_source_file_hash: {file_hash}\n"
        f"kb_source_commit: \"{git_commit}\"\n"
        f"kb_source_commit_date: \"{git_date}\"\n"
        f"kb_migration: \"\"\n"
        "---"
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_nom(method: str, flag_type: str) -> str:
    """Ex: pariV2 + missing_branch → PARIV2_BRANCH"""
    method_part = re.sub(r'[^a-zA-Z0-9]', '_', method).upper().strip('_')
    type_part = _FLAG_SHORT.get(flag_type, flag_type.upper())
    return f"{method_part}_{type_part}"


def _make_relation_nom(rel: Relation) -> str:
    """Ex: TP2 implies C_TYP_FLX → TP2_IMPLIES_C_TYP_FLX"""
    from_part = re.sub(r'[^A-Za-z0-9]', '_', rel.from_entity.value)[:20].strip('_').upper()
    to_raw = rel.to_entity.value.split('=')[0].split('→')[0].strip()
    to_part = re.sub(r'[^A-Za-z0-9]', '_', to_raw)[:20].strip('_').upper()
    return f"{from_part}_{rel.kind.upper()}_{to_part}"


def _infer_domain(controller_name: str) -> str:
    """MonServiceController → mon-service"""
    name = re.sub(r'(Controller|Service|Repository|Helper)$', '', controller_name, flags=re.IGNORECASE)
    name = re.sub(r'(?<=[a-z])(?=[A-Z])', '-', name).lower()
    return name or "default"


def _first_line(text: str) -> str:
    return (text or "").strip().splitlines()[0][:80] if text else ""


def _line_range(flags: list[Flag]) -> str:
    lines = [f.source_line for f in flags if f.source_line]
    if not lines:
        return ""
    return f"L{min(lines)}-L{max(lines)}"


def _trouvé_dans(flags: list[Flag], source_file: str) -> str:
    lines = []
    seen: set[str] = set()
    for f in flags:
        method = f.method_name or f.location or "?"
        line = f"L{f.source_line}" if f.source_line else ""
        entry = f"- `{source_file}:{line}` — `{method}()`"
        if entry not in seen:
            lines.append(entry)
            seen.add(entry)
    return "\n".join(lines[:6]) or f"- `{source_file}`"


def _render_relation_fiche(
    rel: Relation,
    domain: str,
    file_hash: str,
    git_commit: str,
    git_date: str,
) -> str:
    today = str(date.today())
    from_val_safe = rel.from_entity.value.replace('"', "'")
    to_val_safe = rel.to_entity.value.replace('"', "'")

    fm_lines = [
        "---",
        "kb_type: relation",
        f"kind: {rel.kind}",
        f"kb_nom: {rel.id}",
        f"kb_domaine: {domain}",
        f"kb_confiance: {rel.confiance}",
        f"kb_source: \"Rosetta RelationExtractor — généré {today}\"",
        "from:",
        f"  type: {rel.from_entity.type}",
        f"  value: \"{from_val_safe}\"",
        "to:",
        f"  type: {rel.to_entity.type}",
        f"  value: \"{to_val_safe}\"",
        f"direction: {rel.direction}",
        f"kb_source_file_hash: {file_hash}",
        f"kb_source_commit: \"{git_commit}\"",
        f"kb_source_commit_date: \"{git_date}\"",
        f"kb_pattern: {rel.pattern}",
        "---",
    ]
    fm = "\n".join(fm_lines)

    sections = [fm]
    sections.append(
        f"## Label\nRelation `{rel.kind}` : `{rel.from_entity.value}` → `{rel.to_entity.value}`"
    )
    sections.append(f"## Sémantique\n{rel.semantique}")

    if rel.conditions:
        cond_lines = "\n".join(f"- {c}" for c in rel.conditions)
        sections.append(f"## Conditions\n{cond_lines}")

    if rel.trouvé_dans:
        ref_lines = []
        for r in rel.trouvé_dans:
            line_str = f" ligne {r.ligne}" if r.ligne else ""
            ref_lines.append(f"- `{r.fichier}` — `{r.methode}()`{line_str}")
        sections.append(f"## Trouvé dans\n" + "\n".join(ref_lines))

    sections.append(
        "## Notes\n_(généré automatiquement — confiance: medium — à valider PO)_"
    )

    return "\n\n".join(sections) + "\n"


def _file_hash(path: Optional[Path]) -> str:
    if not path or not path.exists():
        return "sha256:inconnu"
    try:
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        return f"sha256:{sha}"
    except Exception:
        return "sha256:inconnu"


def _git_info(path: Optional[Path]) -> tuple[str, str]:
    if not path or not path.exists():
        return "inconnu", str(date.today())
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%H|%ci", "--", str(path)],
            cwd=path.parent, capture_output=True, text=True, timeout=5,
        )
        if result.returncode == 0 and "|" in result.stdout:
            commit, dt = result.stdout.strip().split("|", 1)
            return commit[:12], dt.strip()
    except Exception:
        pass
    return "inconnu", str(date.today())


def _is_high_confidence(fiche_path: Path) -> bool:
    """Retourne True si la fiche existante est en confiance: high."""
    try:
        content = fiche_path.read_text(encoding="utf-8")
        return bool(re.search(r"^kb_confiance:\s*high\s*$", content, re.MULTILINE))
    except Exception:
        return False
