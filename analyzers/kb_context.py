"""
KB Context Provider — Enrichissement des prompts LLM depuis la KB existante
============================================================================
Charge les fiches KB (Markdown + frontmatter YAML) et retourne un bloc
de contexte métier à injecter dans LLMEnricher et BugEnricher.

Objectifs :
- Éviter les doublons (règle déjà documentée → ne pas la re-générer)
- Enrichir le prompt avec les règles déjà connues du même domaine/fichier
- Améliorer la confiance LLM par triangulation avec le KB existant

Dépendances : python-frontmatter + pyyaml (déjà requis par kb_import.py)
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


try:
    import frontmatter as _fm
    _HAS_FRONTMATTER = True
except ImportError:
    _HAS_FRONTMATTER = False


@dataclass
class KBEntry:
    """Une entrée KB chargée depuis une fiche Markdown."""
    nom: str
    kb_type: str       # regle, code, colonne, vue, requete
    domaine: str
    confiance: str     # high, medium, inferred
    label: str
    semantique: str
    fichier: str       # kb_fichier — chemin relatif au repo source
    source_path: Path
    concepts: str = ""
    migration_note: str = ""


class KBContextProvider:
    """
    Charge une KB depuis un répertoire de fiches .md et expose un contexte
    pertinent pour un fichier PHP donné.

    Usage :
        kb = KBContextProvider(Path("/path/to/kb"))
        ctx = kb.context_for("MyService.php")
        # → bloc Markdown compact à injecter dans le prompt LLM
    """

    MAX_CONTEXT_CHARS = 3_000

    def __init__(self, kb_root: Path, verbose: bool = True):
        if not _HAS_FRONTMATTER:
            raise ImportError(
                "python-frontmatter requis : pip install python-frontmatter"
            )
        self.kb_root = Path(kb_root)
        self._verbose = verbose
        self._entries: list[KBEntry] = []
        self._load()

    def __len__(self) -> int:
        return len(self._entries)

    # ------------------------------------------------------------------
    # Chargement
    # ------------------------------------------------------------------

    def _load(self) -> None:
        count = 0
        for md_path in sorted(self.kb_root.rglob("*.md")):
            try:
                post = _fm.load(str(md_path))
            except Exception:
                continue
            if "kb_type" not in post.metadata:
                continue

            meta = post.metadata
            content = post.content

            # Domaine : frontmatter > nom du sous-répertoire parent
            domaine = str(
                meta.get("kb_domaine") or md_path.parent.name or ""
            )

            entry = KBEntry(
                nom=str(meta.get("kb_nom", md_path.stem)),
                kb_type=str(meta.get("kb_type", "regle")),
                domaine=domaine,
                confiance=str(meta.get("kb_confiance", "medium")),
                label=_extract_section(content, "Label"),
                semantique=(
                    _extract_section(content, "Sémantique")
                    or _extract_section(content, "Semantique")
                ),
                fichier=str(meta.get("kb_fichier", "")),
                source_path=md_path,
                concepts=(
                    _extract_section(content, "Concepts / Conditions / Constantes")
                    or _extract_section(content, "Concepts")
                    or _extract_section(content, "Conditions")
                ),
                migration_note=str(meta.get("kb_migration", "")),
            )
            self._entries.append(entry)
            count += 1

        if self._verbose:
            print(f"  [KB] {count} fiche(s) chargée(s) depuis {self.kb_root}")

    # ------------------------------------------------------------------
    # Requête
    # ------------------------------------------------------------------

    def context_for(
        self,
        filename: str,
        domain: Optional[str] = None,
        max_chars: int = MAX_CONTEXT_CHARS,
    ) -> str:
        """
        Retourne un bloc compact de règles KB pertinentes pour `filename`.

        Matching (par score décroissant) :
          +3  kb_fichier contient le stem du fichier analysé
          +2  nom de l'entrée contient le stem
          +2  domaine exact
          +1  domaine partiel (sous-chaîne)
        """
        stem = Path(filename).stem.lower()
        matches = self._score_and_sort(stem, domain)
        if not matches:
            return ""
        return _format_context(matches, max_chars)

    def domain_entries(self, domain: str) -> list[KBEntry]:
        """Toutes les entrées d'un domaine donné."""
        d = domain.lower()
        return [e for e in self._entries if e.domaine.lower() == d]

    def bug_entries_for(self, filename: str) -> list[KBEntry]:
        """Retourne les entrées kb_type=bug pertinentes pour `filename` (score > 0)."""
        stem = Path(filename).stem.lower()
        return [
            e for _, e in sorted(
                [
                    (s, e)
                    for e in self._entries
                    if e.kb_type == "bug"
                    for s in [
                        (3 if stem and stem in e.fichier.lower() else 0)
                        + (2 if stem and stem in e.nom.lower() else 0)
                    ]
                    if s > 0
                ],
                key=lambda x: -x[0],
            )
        ]

    def _score_and_sort(
        self, stem: str, domain: Optional[str]
    ) -> list[KBEntry]:
        scored: list[tuple[int, KBEntry]] = []
        for e in self._entries:
            score = 0
            if stem and stem in e.fichier.lower():
                score += 3
            if stem and stem in e.nom.lower():
                score += 2
            if domain:
                d = domain.lower()
                if e.domaine.lower() == d:
                    score += 2
                elif d in e.domaine.lower() or e.domaine.lower() in d:
                    score += 1
            if score > 0:
                scored.append((score, e))
        scored.sort(key=lambda x: -x[0])
        return [e for _, e in scored]


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def _extract_section(content: str, header: str) -> str:
    """Extrait le texte brut d'une section ## Header (jusqu'à la suivante)."""
    pattern = re.compile(
        rf"^##\s+{re.escape(header)}\s*\n(.*?)(?=^##\s|\Z)",
        re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    m = pattern.search(content)
    if not m:
        return ""
    # Supprimer les blocs de code — trop longs pour un contexte prompt
    text = re.sub(r"```.*?```", "", m.group(1), flags=re.DOTALL).strip()
    # Normaliser les lignes vides multiples
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def _format_context(entries: list[KBEntry], max_chars: int) -> str:
    """
    Formate les entrées en bloc texte compact pour injection dans un prompt LLM.
    Tronque proprement si `max_chars` est atteint.
    """
    header = (
        "════ RÈGLES MÉTIER CONNUES (KB Rosetta) ════\n"
        "Ces règles sont déjà documentées. Évite les doublons "
        "et enrichis avec ces concepts si pertinents :\n\n"
    )
    footer = "\n════ FIN RÈGLES KB ════"

    body_lines: list[str] = []
    chars_used = len(header) + len(footer)

    for e in entries:
        parts = [
            f"[{e.kb_type.upper()} — {e.nom}]"
            f" (domaine: {e.domaine}, confiance: {e.confiance})",
            f"  Label     : {e.label}",
            f"  Sémantique: {e.semantique[:300]}",
        ]
        if e.concepts:
            # Extraire seulement les 2 premières lignes non-vides des concepts
            concept_lines = [
                l.strip()
                for l in e.concepts.splitlines()
                if l.strip() and not l.strip().startswith("|")
            ][:2]
            if concept_lines:
                parts.append("  Concepts  : " + " | ".join(concept_lines))
        if e.migration_note and e.migration_note not in ("non", "partiel", "requis", ""):
            parts.append(f"  Migration : {e.migration_note[:150]}")
        parts.append("")

        block = "\n".join(parts) + "\n"
        if chars_used + len(block) > max_chars:
            remaining = max_chars - chars_used
            if remaining > 120:
                body_lines.append(block[:remaining].rstrip() + " […]")
            break
        body_lines.append(block)
        chars_used += len(block)

    return header + "".join(body_lines) + footer
