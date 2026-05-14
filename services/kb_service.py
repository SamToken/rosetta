"""Rosetta — Service de gestion de la Knowledge Base.

Contient toute la logique métier et la persistance YAML extraites de rosetta_kb.py.
Aucun print, aucun argparse, aucune interaction console.
Toutes les méthodes retournent des dataclasses ou des str (pour les exports texte).
"""
import json
import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Optional

import yaml

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

CONFIDENCE_ORDER: dict[str, int] = {"high": 2, "medium": 1, "inferred": 0}
CONFIDENCE_LABELS: dict[str, str] = {
    "high": "[HIGH]", "medium": "[MED] ", "inferred": "[INF] "
}

_PENDING_DECISION_FLAG_TYPES: frozenset[str] = frozenset({
    "missing_branch", "external_state_dependency", "dynamic_session_key",
})
_PENDING_DECISION_CODE_RE = re.compile(
    r"^(BRANCHES_MANQUANTES_|DI-missing_branch--|DI-external_state--|FALLBACK_)",
    re.IGNORECASE,
)
_IMPORT_TYPE_ROUTES: dict[str, tuple[str, ...]] = {
    "code":     ("codes",),
    "regle":    ("regles",),
    "bug":      ("regles",),
    "colonne":  ("sql_artifacts", "colonnes"),
    "vue":      ("sql_artifacts", "vues"),
    "requete":  ("sql_artifacts", "requetes"),
    "relation": ("relations",),
}

# ---------------------------------------------------------------------------
# Dataclasses de résultats (contrat entre le service et les consommateurs)
# ---------------------------------------------------------------------------

@dataclass
class LookupResult:
    found: bool
    code: str
    section: Optional[str] = None
    entry: Optional[dict] = None

    def to_enricher_dict(self) -> dict[str, Any]:
        """Format attendu par llm_enricher.py / audit_service.py."""
        if not self.found or not self.entry:
            return {
                "found": False, "confiance": None, "label": None,
                "valeurs": None, "semantique": None, "section": None,
            }
        e = self.entry
        return {
            "found": True,
            "confiance": e.get("confiance", "inferred"),
            "label": e.get("label"),
            "valeurs": e.get("valeurs"),
            "semantique": e.get("semantique"),
            "section": self.section,
            **{k: v for k, v in e.items()
               if k not in ("confiance", "label", "valeurs", "semantique")},
        }

    def to_json_dict(self) -> dict[str, Any]:
        """Format pour --json dans le CLI lookup."""
        if not self.found:
            return {"found": False, "code": self.code}
        return {"found": True, "code": self.code, "section": self.section, **(self.entry or {})}


@dataclass
class CaptureResult:
    success: bool
    code: str
    confiance: str
    domain: str
    action: str               # "created" | "updated" | "skipped_high"
    file_path: Optional[str] = None


@dataclass
class PendingItem:
    id: str
    code: str
    question: str
    priorite: str
    domaine: Optional[str] = None
    fichiers: list[str] = field(default_factory=list)
    kb_type: Optional[str] = None
    pending_type: Optional[int] = None
    destination: Optional[str] = None
    validated: bool = False


@dataclass
class AddPendingResult:
    pending_id: str
    code: str
    priorite: str
    destination: str


@dataclass
class ValidateResult:
    success: bool
    pending_id: str
    code: str
    action: str               # "created" | "updated"
    domain: str
    error: Optional[str] = None


@dataclass
class FileEntry:
    name: str
    count: int
    is_global: bool = False


@dataclass
class KBStats:
    projet: str
    version: str
    last_updated: str
    maintainer: str
    # Sections
    codes: int = 0
    regles: int = 0
    schema: int = 0
    colonnes: int = 0
    vues: int = 0
    requetes: int = 0
    total: int = 0
    # Confiance
    high: int = 0
    medium: int = 0
    inferred: int = 0
    # Pending
    pending_total: int = 0
    pending_high: int = 0
    # Mode répertoire
    is_dir: bool = False
    files: list[FileEntry] = field(default_factory=list)


@dataclass
class SearchResult:
    section: str
    nom: str
    entry: dict


@dataclass
class ImportResult:
    added: int = 0
    updated: int = 0
    ignored: int = 0
    errors: int = 0
    messages: list[str] = field(default_factory=list)


@dataclass
class SplitResult:
    domains: list[tuple[str, int]] = field(default_factory=list)  # (name, count)
    total_entries: int = 0
    pending_count: int = 0
    output_dir: Optional[Path] = None


# ---------------------------------------------------------------------------
# Utilitaires bas niveau (module-level, sans état)
# ---------------------------------------------------------------------------

def normalize_domain(name: str) -> str:
    """'OrchestraService.php' → 'OrchestraService' · 'orchestra-service' → identique."""
    p = Path(name)
    if p.suffix.lower() == ".php":
        return p.stem
    return name


def _global_file(kb_dir: Path) -> Path:
    return kb_dir / "_global.yaml"


def _domain_file(kb_dir: Path, domain: str) -> Path:
    safe = re.sub(r"[^A-Za-z0-9_-]", "_", domain)
    return kb_dir / f"{safe}.yaml"


def _empty_kb() -> dict:
    return {
        "meta": {
            "projet": "monprojet", "version": "2.1.0",
            "last_updated": str(date.today()), "maintainer": "Samah",
        },
        "codes": {}, "regles": {}, "schema": {},
        "sql_artifacts": {"colonnes": {}, "vues": {}, "requetes": {}},
        "relations": {},
        "pending_validation": {},
    }


def _empty_domain() -> dict:
    return {
        "codes": {}, "regles": {}, "schema": {},
        "sql_artifacts": {"colonnes": {}, "vues": {}, "requetes": {}},
        "relations": {},
    }


# ---------------------------------------------------------------------------
# Renderers de texte (utilisés par les méthodes export_* du service)
# ---------------------------------------------------------------------------

def _conf_badge(conf: str) -> str:
    return {"high": "✅ validé PO", "medium": "⚠️ inféré",
            "inferred": "🔍 non validé"}.get(conf, conf)


def _migration_badge(note: str) -> str:
    if not note:
        return ""
    n = note.lower()
    if n.startswith("non"):
        return "🟢 aucune"
    if n.startswith("partiel"):
        return "🟡 partielle"
    return "🔴 requise"


def _truncate(text: str, max_len: int = 120) -> str:
    text = (text or "").replace("\n", " ").strip()
    if len(text) <= max_len:
        return text
    cut = text.rfind(" ", 0, max_len)
    return (text[:cut] if cut > 0 else text[:max_len]) + "…"


def _first_sentence(text: str, max_len: int = 300) -> str:
    """Première phrase complète. Ne coupe pas sur '1. ' (listes numérotées)."""
    text = (text or "").replace("\n", " ").strip()
    for m in re.finditer(r'(?<!\d)[.!?](?=\s+[A-ZÀ-Ÿ«"(]|\s*$)', text[: max_len + 60]):
        end = m.end()
        if end <= max_len:
            return text[:end].strip()
    if len(text) <= max_len:
        return text
    cut = text.rfind(" ", 0, max_len)
    return (text[:cut] if cut > 0 else text[:max_len]) + "…"


def _first_para(text: str, max_len: int = 420) -> str:
    """Introduction avant la première liste ou table Markdown."""
    text = (text or "").strip()
    m = re.search(r"\n\s*(?:-|\d+\.|\|)\s", text)
    m2 = re.search(r":\s+(?:-\s|\d+\.\s)", text)
    candidates = [mc.start() for mc in [m, m2] if mc]
    intro = text[: min(candidates)].rstrip(": ").strip() if candidates else text
    if not intro:
        intro = text
    return _first_sentence(intro, max_len)


def _bug_severity(label: str, notes: str) -> str:
    combined = (label + " " + (notes or "")).lower()
    if "🔴" in combined or "critique" in combined:
        return "🔴 Critique"
    if "🟠" in combined or "important" in combined:
        return "🟠 Important"
    return "🟡 Moyen"


_MIGRATION_BADGE_WORDS = {"non", "partiel", "requis"}

_TYPE_META = {
    "dynamic_session_key":       ("🔴", "Session dynamique"),
    "external_state_dependency": ("🔴", "Dépendance externe"),
    "hardcoded_situation_code":  ("🟡", "Code hardcodé"),
    "missing_branch":            ("🟡", "Branche manquante"),
    "magic_value":               ("🟡", "Valeur magique"),
}


# ---------------------------------------------------------------------------
# Import Markdown helpers (utilisés par import_docs)
# ---------------------------------------------------------------------------

def _import_extract_sections(content: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current: Optional[str] = None
    for line in content.splitlines():
        m = re.match(r"^##\s+(.+)", line)
        if m:
            current = m.group(1).strip()
            sections[current] = []
        elif current is not None:
            sections[current].append(line)
    return sections


def _import_text(lines: list[str]) -> str:
    return " ".join(l.strip() for l in lines if l.strip())


def _import_parse_table(lines: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in lines:
        line = line.strip()
        if not line.startswith("|") or re.match(r"^\|[-| ]+\|$", line):
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) >= 2 and parts[0].lower() not in ("valeur", "colonne", "value", "clé", "code"):
            result[parts[0]] = parts[1]
    return result


def _import_parse_list(lines: list[str]) -> list[str]:
    result = []
    for line in lines:
        line = line.strip()
        if line.startswith(("- ", "* ", "+ ")):
            result.append(line[2:].strip())
        elif re.match(r"^\d+\.\s", line):
            result.append(re.sub(r"^\d+\.\s+", "", line).strip())
    return result


def _import_build_entry(kb_type: str, meta: dict, sections: dict) -> dict:
    t = _import_text
    entry: dict[str, Any] = {}

    if "Label" in sections:
        entry["label"] = t(sections["Label"])
    sem_lines = sections.get("Semantique") or sections.get("Sémantique") or []
    if sem_lines:
        entry["semantique"] = t(sem_lines)

    if kb_type == "code":
        if meta.get("kb_domaine"):
            entry["domaine"] = meta["kb_domaine"]
        refs = _import_parse_list(sections.get("Trouvé dans", []))
        if refs:
            entry["contextes"] = [{"champ": r} for r in refs]

    elif kb_type in ("regle", "bug"):
        conds = _import_parse_list(sections.get("Conditions", []))
        if conds:
            entry["conditions"] = conds
        if meta.get("kb_domaine"):
            entry["domaine"] = meta["kb_domaine"]
        if kb_type == "bug":
            if "label" in entry and not entry["label"].startswith("[BUG]"):
                entry["label"] = "[BUG] " + entry["label"]
            sev_lines = sections.get("Sévérité", [])
            if sev_lines:
                sev = _import_text(sev_lines)
                entry["notes"] = f"Sévérité: {sev}. " + entry.get("notes", "")
            refs = _import_parse_list(sections.get("Trouvé dans", []))
            if refs:
                entry["contextes"] = [{"champ": r} for r in refs]

    elif kb_type == "colonne":
        if meta.get("kb_table"):
            entry["table"] = meta["kb_table"]
        if meta.get("kb_type_oracle"):
            entry["type_oracle"] = meta["kb_type_oracle"]
        vals = _import_parse_table(sections.get("Valeurs", []))
        if vals:
            entry["valeurs"] = vals
        dists = _import_parse_table(sections.get("Distinctions", []))
        if dists:
            entry["distinctions"] = dists
        refs = _import_parse_list(sections.get("Trouvé dans", []))
        if refs:
            entry["trouvé_dans"] = refs

    elif kb_type == "vue":
        if meta.get("kb_tables"):
            entry["tables_source"] = [s.strip() for s in str(meta["kb_tables"]).split(",")]
        piege = sections.get("Piège", [])
        if piege:
            entry["piège_connu"] = t(piege)

    elif kb_type == "requete":
        if meta.get("kb_fichier"):
            entry["fichier_source"] = meta["kb_fichier"]
        if meta.get("kb_lignes"):
            entry["lignes"] = meta["kb_lignes"]
        consts = _import_parse_table(sections.get("Constantes", []))
        if consts:
            entry["constantes_magiques"] = consts
        concepts = _import_parse_list(sections.get("Concepts", []))
        if concepts:
            entry["concepts_métier"] = concepts

    elif kb_type == "relation":
        entry["kind"] = meta.get("kind", "implies")
        if meta.get("from"):
            entry["from_entity"] = dict(meta["from"])
        if meta.get("to"):
            entry["to_entity"] = dict(meta["to"])
        entry["direction"] = meta.get("direction", "one_way")
        if meta.get("kb_domaine"):
            entry["domaine"] = meta["kb_domaine"]
        conds = _import_parse_list(sections.get("Conditions", []))
        if conds:
            entry["conditions"] = conds
        refs = _import_parse_list(sections.get("Trouvé dans", []))
        if refs:
            entry["trouvé_dans"] = [{"fichier": r} for r in refs]

    if meta.get("kb_migration"):
        entry["migration_note"] = meta["kb_migration"]
    note_lines = sections.get("Notes", [])
    if note_lines:
        note = t(note_lines)
        if note and note.lower() not in ("aucune.", "aucune", "none", "~"):
            entry["notes"] = note

    entry["source"] = meta.get("kb_source", "kb_import — généré")
    entry["confiance"] = "medium"
    return entry


# ---------------------------------------------------------------------------
# KBService — service principal
# ---------------------------------------------------------------------------

class KBService:
    """Gestion complète de la Knowledge Base Rosetta.

    Compatible fichier unique (knowledge_base.yaml) et répertoire multi-domaine (kb/).
    Aucune interaction console. Toutes les méthodes retournent des dataclasses ou str.
    """

    def __init__(self, kb_path: Path) -> None:
        self.kb_path = kb_path

    # ── Persistance privée ────────────────────────────────────────────────────

    def _read_file(self, path: Path) -> dict:
        if not path.exists():
            return {}
        with path.open(encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def _write_file(self, path: Path, data: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    def _load_kb_dir(self) -> dict:
        merged = _empty_kb()
        for yaml_file in sorted(self.kb_path.glob("*.yaml")):
            d = self._read_file(yaml_file)
            if yaml_file.name == "_global.yaml":
                merged["meta"].update(d.get("meta", {}))
                merged["pending_validation"].update(d.get("pending_validation", {}))
            else:
                for section in ("codes", "regles", "schema"):
                    merged[section].update(d.get(section, {}))
                sa = d.get("sql_artifacts", {})
                for sub in ("colonnes", "vues", "requetes"):
                    merged["sql_artifacts"][sub].update(sa.get(sub, {}))
                merged["relations"].update(d.get("relations", {}))
        return merged

    def _load_for_write(self, domain: str) -> dict:
        """Charge uniquement le fichier du domaine cible (pour les écritures)."""
        if self.kb_path.is_dir():
            d = self._read_file(_domain_file(self.kb_path, domain))
            base = _empty_domain()
            for section in ("codes", "regles", "schema"):
                base[section].update(d.get(section, {}))
            sa = d.get("sql_artifacts", {})
            for sub in ("colonnes", "vues", "requetes"):
                base["sql_artifacts"][sub].update(sa.get(sub, {}))
            base["relations"].update(d.get("relations", {}))
            return base
        return self.load()

    def _save_for_write(self, data: dict, domain: str) -> None:
        if self.kb_path.is_dir():
            self.kb_path.mkdir(parents=True, exist_ok=True)
            domain_path = _domain_file(self.kb_path, domain)
            domain_data = {k: v for k, v in data.items()
                           if k not in ("meta", "pending_validation")}
            self._write_file(domain_path, domain_data)
            g = self._read_file(_global_file(self.kb_path))
            g.setdefault("meta", {})["last_updated"] = str(date.today())
            self._write_file(_global_file(self.kb_path), g)
        else:
            data["meta"]["last_updated"] = str(date.today())
            self.kb_path.parent.mkdir(parents=True, exist_ok=True)
            with self.kb_path.open("w", encoding="utf-8") as f:
                yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    def _lookup_all(self, data: dict, code: str) -> Optional[dict[str, Any]]:
        checks = [
            ("codes",                  data.get("codes", {})),
            ("regles",                 data.get("regles", {})),
            ("schema",                 data.get("schema", {})),
            ("sql_artifacts.colonnes", data.get("sql_artifacts", {}).get("colonnes", {})),
            ("sql_artifacts.vues",     data.get("sql_artifacts", {}).get("vues", {})),
            ("sql_artifacts.requetes", data.get("sql_artifacts", {}).get("requetes", {})),
        ]
        for section, bucket in checks:
            if bucket and code in bucket:
                return {"section": section, "entry": bucket[code]}
        return None

    def _next_pending_id(self, pending: dict) -> str:
        n = len(pending) + 1
        while f"PV-{n:03d}" in pending:
            n += 1
        return f"PV-{n:03d}"

    # ── API publique : Chargement ─────────────────────────────────────────────

    def load(self) -> dict:
        """Charge le KB complet (vue fusionnée, lecture seule)."""
        if self.kb_path.is_dir():
            return self._load_kb_dir()
        base = _empty_kb()
        if self.kb_path.exists():
            with self.kb_path.open(encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            base.update(data)
        base.setdefault("sql_artifacts", {})
        base["sql_artifacts"].setdefault("colonnes", {})
        base["sql_artifacts"].setdefault("vues", {})
        base["sql_artifacts"].setdefault("requetes", {})
        return base

    def load_pending(self) -> dict:
        """Charge uniquement le pending_validation."""
        if self.kb_path.is_dir():
            return self._read_file(_global_file(self.kb_path)).get("pending_validation", {})
        return self.load().get("pending_validation", {})

    def save_pending(self, pending: dict) -> None:
        """Sauvegarde le pending_validation."""
        if self.kb_path.is_dir():
            self.kb_path.mkdir(parents=True, exist_ok=True)
            g = self._read_file(_global_file(self.kb_path))
            g["pending_validation"] = pending
            g.setdefault("meta", {})["last_updated"] = str(date.today())
            self._write_file(_global_file(self.kb_path), g)
        else:
            data = self.load()
            data["pending_validation"] = pending
            data["meta"]["last_updated"] = str(date.today())
            self._write_file(self.kb_path, data)

    def detect_pending_type(
        self, code: str, flag_type: Optional[str] = None
    ) -> tuple[int, str]:
        """Détermine (pending_type, destination) d'un pending.

        1 → token en KB (medium/inferred)  → kb_upgrade
        2 → token absent du KB             → kb_new_entry
        3 → décision comportement          → migration_notes
        """
        if flag_type in _PENDING_DECISION_FLAG_TYPES:
            return 3, "migration_notes"
        if _PENDING_DECISION_CODE_RE.match(code):
            return 3, "migration_notes"
        data = self.load()
        if self._lookup_all(data, code):
            return 1, "kb_upgrade"
        return 2, "kb_new_entry"

    # ── API publique : Lookup ─────────────────────────────────────────────────

    def lookup(self, code: str) -> LookupResult:
        """Cherche un token dans toutes les sections du KB."""
        data = self.load()
        hit = self._lookup_all(data, code)
        if not hit:
            return LookupResult(found=False, code=code)
        return LookupResult(found=True, code=code,
                            section=hit["section"], entry=hit["entry"])

    def lookup_for_enricher(self, token: str) -> dict[str, Any]:
        """API pour llm_enricher.py — format dict compatible."""
        return self.lookup(token).to_enricher_dict()

    def list_known_tokens(self) -> frozenset[str]:
        """Retourne tous les tokens connus (codes, colonnes, vues, requêtes, règles).

        Construire une fois au démarrage du pipeline et passer ``__contains__``
        à RelationExtractor pour un filtre faux-positifs O(1) sans I/O en boucle.
        """
        data = self.load()
        tokens: set[str] = set()
        tokens.update(data.get("codes", {}).keys())
        tokens.update(data.get("regles", {}).keys())
        sa = data.get("sql_artifacts", {})
        tokens.update(sa.get("colonnes", {}).keys())
        tokens.update(sa.get("vues", {}).keys())
        tokens.update(sa.get("requetes", {}).keys())
        return frozenset(tokens)

    # ── API publique : Capture ────────────────────────────────────────────────

    def capture(
        self, *, code: str, label: str, source: str,
        confiance: str = "high", domain: str = "commun",
        champ: Optional[str] = None, table: Optional[str] = None,
        lie_a: Optional[str] = None, notes: Optional[str] = None,
        force: bool = False,
    ) -> CaptureResult:
        data = self._load_for_write(domain)
        codes = data["codes"]

        existing_conf = CONFIDENCE_ORDER.get(
            codes.get(code, {}).get("confiance", "inferred"), 0
        )
        if code in codes and existing_conf >= CONFIDENCE_ORDER["high"] and not force:
            return CaptureResult(
                success=False, code=code, confiance=confiance,
                domain=domain, action="skipped_high",
            )

        entry: dict[str, Any] = {
            "label": label, "source": source, "confiance": confiance,
        }
        if champ or table:
            ctx: dict[str, str] = {}
            if champ:
                ctx["champ"] = champ
            if table:
                ctx["table"] = table
            entry["contextes"] = [ctx]
        if domain and domain != "commun":
            entry["domaine"] = domain
        if lie_a:
            entry["lié_à"] = [x.strip() for x in lie_a.split(",")]
        if notes:
            entry["notes"] = notes

        action = "updated" if code in codes else "created"
        codes[code] = entry
        self._save_for_write(data, domain)

        file_path = (
            _domain_file(self.kb_path, domain).name if self.kb_path.is_dir() else None
        )
        return CaptureResult(
            success=True, code=code, confiance=confiance,
            domain=domain, action=action, file_path=file_path,
        )

    def capture_colonne(
        self, *, nom: str, label: str, domain: str = "commun",
        table: Optional[str] = None, type_oracle: Optional[str] = None,
        semantique: Optional[str] = None, valeurs: Optional[str] = None,
        distinctions: Optional[str] = None, trouve_dans: Optional[str] = None,
        migration: Optional[str] = None, source: Optional[str] = None,
        confiance: str = "high", force: bool = False,
    ) -> CaptureResult:
        data = self._load_for_write(domain)
        colonnes = data["sql_artifacts"]["colonnes"]

        existing_conf = CONFIDENCE_ORDER.get(
            colonnes.get(nom, {}).get("confiance", "inferred"), 0
        )
        if nom in colonnes and existing_conf >= CONFIDENCE_ORDER["high"] and not force:
            return CaptureResult(
                success=False, code=nom, confiance=confiance,
                domain=domain, action="skipped_high",
            )

        entry: dict[str, Any] = {
            "label": label,
            "source": source or f"capture — {date.today()}",
            "confiance": confiance,
        }
        if table:
            entry["table"] = table
        if type_oracle:
            entry["type_oracle"] = type_oracle
        if semantique:
            entry["semantique"] = semantique
        if valeurs:
            entry["valeurs"] = dict(
                kv.strip().split("=", 1) for kv in valeurs.split(",") if "=" in kv
            )
        if distinctions:
            entry["distinctions"] = dict(
                kv.strip().split("=", 1) for kv in distinctions.split(",") if "=" in kv
            )
        if trouve_dans:
            entry["trouvé_dans"] = [f.strip() for f in trouve_dans.split(",")]
        if migration:
            entry["migration_note"] = migration

        action = "updated" if nom in colonnes else "created"
        colonnes[nom] = entry
        self._save_for_write(data, domain)

        file_path = (
            _domain_file(self.kb_path, domain).name if self.kb_path.is_dir() else None
        )
        return CaptureResult(
            success=True, code=nom, confiance=confiance,
            domain=domain, action=action, file_path=file_path,
        )

    def capture_vue(
        self, *, nom: str, label: str, domain: str = "commun",
        semantique: Optional[str] = None, tables: Optional[str] = None,
        piege: Optional[str] = None, migration: Optional[str] = None,
        source: Optional[str] = None, confiance: str = "high",
        force: bool = False,
    ) -> CaptureResult:
        data = self._load_for_write(domain)
        vues = data["sql_artifacts"]["vues"]

        existing_conf = CONFIDENCE_ORDER.get(
            vues.get(nom, {}).get("confiance", "inferred"), 0
        )
        if nom in vues and existing_conf >= CONFIDENCE_ORDER["high"] and not force:
            return CaptureResult(
                success=False, code=nom, confiance=confiance,
                domain=domain, action="skipped_high",
            )

        entry: dict[str, Any] = {
            "label": label,
            "source": source or f"capture — {date.today()}",
            "confiance": confiance,
        }
        if semantique:
            entry["semantique"] = semantique
        if tables:
            entry["tables_source"] = [t.strip() for t in tables.split(",")]
        if piege:
            entry["piège_connu"] = piege
        if migration:
            entry["migration_note"] = migration

        action = "updated" if nom in vues else "created"
        vues[nom] = entry
        self._save_for_write(data, domain)

        file_path = (
            _domain_file(self.kb_path, domain).name if self.kb_path.is_dir() else None
        )
        return CaptureResult(
            success=True, code=nom, confiance=confiance,
            domain=domain, action=action, file_path=file_path,
        )

    def capture_requete(
        self, *, nom: str, label: Optional[str] = None, domain: str = "commun",
        fichier: Optional[str] = None, lignes: Optional[str] = None,
        semantique: Optional[str] = None, constantes: Optional[str] = None,
        concepts: Optional[str] = None, index: Optional[str] = None,
        risque: Optional[str] = None, migration: Optional[str] = None,
        notes: Optional[str] = None, source: Optional[str] = None,
        confiance: str = "high", force: bool = False,
    ) -> CaptureResult:
        data = self._load_for_write(domain)
        requetes = data["sql_artifacts"]["requetes"]

        existing = requetes.get(nom, {})
        existing_conf = CONFIDENCE_ORDER.get(existing.get("confiance", "inferred"), 0)
        if existing and existing_conf >= CONFIDENCE_ORDER["high"] and not force:
            return CaptureResult(
                success=False, code=nom, confiance=confiance,
                domain=domain, action="skipped_high",
            )

        if not label and not existing:
            raise ValueError(f"--label obligatoire pour une nouvelle requête '{nom}'")

        entry: dict[str, Any] = dict(existing) if existing else {}
        if label:
            entry["label"] = label
        entry["source"] = source or f"capture — {date.today()}"
        entry["confiance"] = confiance
        if fichier:
            entry["fichier_source"] = fichier
        if lignes:
            entry["lignes"] = lignes
        if semantique:
            entry["semantique"] = semantique
        if constantes:
            entry["constantes_magiques"] = dict(
                kv.strip().split("=", 1) for kv in constantes.split(",") if "=" in kv
            )
        if concepts:
            entry["concepts_métier"] = [c.strip() for c in concepts.split(",")]
        if index:
            entry["performance"] = {"index_critiques": [index]}
        if risque:
            entry.setdefault("performance", {})["risque_migration"] = risque
        if migration:
            entry["migration_note"] = migration
        if notes:
            entry["notes"] = notes

        action = "updated" if nom in requetes else "created"
        requetes[nom] = entry
        self._save_for_write(data, domain)

        file_path = (
            _domain_file(self.kb_path, domain).name if self.kb_path.is_dir() else None
        )
        return CaptureResult(
            success=True, code=nom, confiance=confiance,
            domain=domain, action=action, file_path=file_path,
        )

    # ── API publique : Pending ────────────────────────────────────────────────

    def list_pending(self, priorite: Optional[str] = None) -> list[PendingItem]:
        pending = self.load_pending()
        priority_order = {"high": 0, "medium": 1, "low": 2}
        items = []
        for pid, p in pending.items():
            if priorite and p.get("priorite") != priorite:
                continue
            fichiers = p.get("fichiers", [])
            if isinstance(fichiers, str):
                fichiers = [f.strip() for f in fichiers.split(",") if f.strip()]
            items.append(PendingItem(
                id=pid,
                code=p.get("code", ""),
                question=p.get("question", ""),
                priorite=p.get("priorite", "low"),
                domaine=p.get("domaine"),
                fichiers=fichiers,
                kb_type=p.get("kb_type"),
                pending_type=p.get("pending_type"),
                destination=p.get("destination"),
                validated=bool(p.get("validated")),
            ))
        items.sort(key=lambda x: priority_order.get(x.priorite, 3))
        return items

    def add_pending(
        self, *, code: str, question: str, priorite: str = "medium",
        fichiers: Optional[str] = None, kb_type: Optional[str] = None,
        domaine: Optional[str] = None,
    ) -> AddPendingResult:
        pending = self.load_pending()
        pid = self._next_pending_id(pending)

        item: dict[str, Any] = {
            "code": code, "question": question, "priorite": priorite,
        }
        if fichiers:
            item["fichiers"] = [f.strip() for f in fichiers.split(",")]
        if kb_type:
            item["kb_type"] = kb_type
        if domaine:
            item["domaine"] = domaine

        ptype, dest = self.detect_pending_type(code, flag_type=kb_type)
        item["pending_type"] = ptype
        item["destination"] = dest

        pending[pid] = item
        self.save_pending(pending)
        return AddPendingResult(
            pending_id=pid, code=code, priorite=priorite, destination=dest
        )

    def validate_pending(
        self, *, pending_id: str, label: Optional[str] = None,
        source: Optional[str] = None, notes: Optional[str] = None,
        domaine: Optional[str] = None,
    ) -> ValidateResult:
        pending = self.load_pending()

        if pending_id not in pending:
            return ValidateResult(
                success=False, pending_id=pending_id, code="",
                action="", domain="",
                error=f"ID '{pending_id}' introuvable dans pending_validation.",
            )

        item = pending[pending_id]
        code = item.get("code", "")
        kb_type = item.get("kb_type", "code")
        domain = domaine or item.get("domaine") or "commun"
        effective_source = source or f"PO validé — {date.today()}"

        update: dict[str, Any] = {"confiance": "high", "source": effective_source}
        if label:
            update["label"] = label
        if notes:
            update["notes"] = notes

        data = self._load_for_write(domain)
        if kb_type == "colonne":
            section = data["sql_artifacts"]["colonnes"]
        elif kb_type == "vue":
            section = data["sql_artifacts"]["vues"]
        elif kb_type == "requete":
            section = data["sql_artifacts"]["requetes"]
        elif kb_type == "regle":
            section = data["regles"]
        else:
            section = data["codes"]

        action = "updated" if code in section else "created"
        section.setdefault(code, {}).update(update)
        self._save_for_write(data, domain)

        del pending[pending_id]
        self.save_pending(pending)

        return ValidateResult(
            success=True, pending_id=pending_id, code=code,
            action=action, domain=domain,
        )

    # ── API publique : Suppression ────────────────────────────────────────────

    def delete(self, code: str, section: str) -> bool:
        """Supprime une entrée KB. Retourne True si trouvée et supprimée."""
        _SECTION_KEYS: dict[str, tuple[str, ...]] = {
            "codes":                   ("codes",),
            "regles":                  ("regles",),
            "sql_artifacts.colonnes":  ("sql_artifacts", "colonnes"),
            "sql_artifacts.vues":      ("sql_artifacts", "vues"),
            "sql_artifacts.requetes":  ("sql_artifacts", "requetes"),
        }
        keys = _SECTION_KEYS.get(section)
        if not keys:
            return False

        if self.kb_path.is_dir():
            for yaml_file in sorted(self.kb_path.glob("*.yaml")):
                data = self._read_file(yaml_file)
                bucket = data
                for k in keys[:-1]:
                    bucket = bucket.get(k, {})
                target = bucket.get(keys[-1], {})
                if code in target:
                    del target[code]
                    from datetime import date as _date
                    data.setdefault("meta", {})["last_updated"] = str(_date.today())
                    self._write_file(yaml_file, data)
                    return True
            return False
        else:
            data = self.load()
            bucket = data
            for k in keys[:-1]:
                bucket = bucket.get(k, {})
            target = bucket.get(keys[-1], {})
            if code not in target:
                return False
            del target[code]
            self._write_file(self.kb_path, data)
            return True

    # ── API publique : Stats et recherche ─────────────────────────────────────

    def stats(self) -> KBStats:
        data = self.load()
        meta = data.get("meta", {})

        codes    = data.get("codes", {}) or {}
        regles   = data.get("regles", {}) or {}
        schema   = data.get("schema", {}) or {}
        colonnes = data.get("sql_artifacts", {}).get("colonnes", {}) or {}
        vues     = data.get("sql_artifacts", {}).get("vues", {}) or {}
        requetes = data.get("sql_artifacts", {}).get("requetes", {}) or {}
        pending  = data.get("pending_validation", {}) or {}

        all_entries = (
            list(codes.values()) + list(regles.values()) + list(schema.values())
            + list(colonnes.values()) + list(vues.values()) + list(requetes.values())
        )
        conf_counts: dict[str, int] = {"high": 0, "medium": 0, "inferred": 0}
        for e in all_entries:
            if isinstance(e, dict):
                c = e.get("confiance", "inferred")
                conf_counts[c] = conf_counts.get(c, 0) + 1

        pending_high = sum(1 for p in pending.values() if p.get("priorite") == "high")

        files: list[FileEntry] = []
        if self.kb_path.is_dir():
            for f in sorted(self.kb_path.glob("*.yaml")):
                d = self._read_file(f)
                if f.name == "_global.yaml":
                    n = len(d.get("pending_validation", {}))
                    files.append(FileEntry(name="_global.yaml", count=n, is_global=True))
                else:
                    n = sum(len(d.get(s, {})) for s in ("codes", "regles", "schema"))
                    n += sum(len(d.get("sql_artifacts", {}).get(s, {}))
                             for s in ("colonnes", "vues", "requetes"))
                    files.append(FileEntry(name=f.name, count=n))

        return KBStats(
            projet=meta.get("projet", "KB"),
            version=meta.get("version", "?"),
            last_updated=meta.get("last_updated", "?"),
            maintainer=meta.get("maintainer", "?"),
            codes=len(codes), regles=len(regles), schema=len(schema),
            colonnes=len(colonnes), vues=len(vues), requetes=len(requetes),
            total=len(all_entries),
            high=conf_counts.get("high", 0),
            medium=conf_counts.get("medium", 0),
            inferred=conf_counts.get("inferred", 0),
            pending_total=len(pending),
            pending_high=pending_high,
            is_dir=self.kb_path.is_dir(),
            files=files,
        )

    def search(self, texte: str) -> list[SearchResult]:
        data = self.load()
        texte_lower = texte.lower()
        results: list[SearchResult] = []

        sections = [
            ("codes",                  data.get("codes", {})),
            ("regles",                 data.get("regles", {})),
            ("schema",                 data.get("schema", {})),
            ("sql_artifacts.colonnes", data.get("sql_artifacts", {}).get("colonnes", {})),
            ("sql_artifacts.vues",     data.get("sql_artifacts", {}).get("vues", {})),
            ("sql_artifacts.requetes", data.get("sql_artifacts", {}).get("requetes", {})),
        ]
        for section_name, bucket in sections:
            if not bucket:
                continue
            for nom, entry in bucket.items():
                if not isinstance(entry, dict):
                    continue
                haystack = nom.lower() + " " + json.dumps(entry, ensure_ascii=False).lower()
                if texte_lower in haystack:
                    results.append(SearchResult(section=section_name, nom=nom, entry=entry))
        return results

    # ── API publique : Exports (retournent str) ───────────────────────────────

    def export_markdown(self) -> str:
        data = self.load()
        meta = data.get("meta", {})
        lines: list[str] = [
            f"# KB Rosetta — {meta.get('projet', 'KB')}",
            f"*Version {meta.get('version', '?')} — {meta.get('last_updated', '?')}*\n",
        ]

        def _section_md(title: str, bucket: Optional[dict]) -> None:
            if not bucket:
                return
            lines.append(f"## {title}\n")
            for nom, entry in bucket.items():
                if not isinstance(entry, dict):
                    continue
                conf = entry.get("confiance", "?")
                label = entry.get("label", "—")
                lines.append(f"### `{nom}` [{conf.upper()}]")
                lines.append(f"**{label}**\n")
                if "semantique" in entry:
                    lines.append(f"{entry['semantique']}\n")
                if "table" in entry:
                    lines.append(f"- Table : `{entry['table']}`")
                if "type_oracle" in entry:
                    lines.append(f"- Type Oracle : `{entry['type_oracle']}`")
                if "valeurs" in entry:
                    lines.append("\n| Valeur | Signification |")
                    lines.append("|--------|---------------|")
                    for k, v in entry["valeurs"].items():
                        lines.append(f"| `{k}` | {v} |")
                if "migration_note" in entry:
                    lines.append(f"\n> Migration : {entry['migration_note']}")
                if "piège_connu" in entry:
                    lines.append(f"\n> Piège : {entry['piège_connu']}")
                if "source" in entry:
                    lines.append(f"\n*Source : {entry['source']}*")
                lines.append("")

        _section_md("Codes métier",       data.get("codes"))
        _section_md("Règles",             data.get("regles"))
        _section_md("Schéma",             data.get("schema"))
        _section_md("Colonnes Oracle",    data.get("sql_artifacts", {}).get("colonnes"))
        _section_md("Vues Oracle",        data.get("sql_artifacts", {}).get("vues"))
        _section_md("Requêtes complexes", data.get("sql_artifacts", {}).get("requetes"))

        return "\n".join(lines)

    def export_prompt(
        self,
        domaine: Optional[str] = None,
        confiance_min: str = "medium",
        max_chars: int = 4_000,
    ) -> str:
        """Sérialise le KB en bloc texte compact injectable dans un prompt LLM."""
        data = self.load()
        min_level = CONFIDENCE_ORDER.get(confiance_min, 1)

        def _keep(entry: dict) -> bool:
            if not isinstance(entry, dict):
                return False
            if CONFIDENCE_ORDER.get(entry.get("confiance", "inferred"), 0) < min_level:
                return False
            if domaine and entry.get("domaine") and entry.get("domaine") != domaine:
                return False
            return True

        def _vals_inline(vals: Optional[dict]) -> str:
            return ", ".join(f"{k}={v}" for k, v in list((vals or {}).items())[:5])

        def _conds_inline(conds: Optional[list]) -> str:
            return " | ".join(str(c) for c in (conds or [])[:3])

        lines: list[str] = []
        skipped = 0

        def _add(line: str) -> bool:
            nonlocal skipped
            if sum(len(l) + 1 for l in lines) + len(line) + 1 > max_chars:
                skipped += 1
                return False
            lines.append(line)
            return True

        codes = {k: v for k, v in (data.get("codes") or {}).items() if _keep(v)}
        if codes:
            _add("## Codes métier")
            for nom, e in codes.items():
                sem = _first_sentence(e.get("semantique") or e.get("notes") or "")
                parts = [f"{nom} [{e.get('confiance','?')}] — {e.get('label','')}"]
                if sem and sem != e.get("label", ""):
                    parts.append(sem)
                _add("  " + ". ".join(parts).rstrip(".") + ".")

        regles = {k: v for k, v in (data.get("regles") or {}).items() if _keep(v)}
        if regles:
            _add("## Règles métier")
            for nom, e in regles.items():
                sem = _first_sentence(e.get("semantique") or "")
                conds = _conds_inline(e.get("conditions"))
                parts = [f"{nom} [{e.get('confiance','?')}] — {e.get('label','')}"]
                if sem:
                    parts.append(sem)
                if conds:
                    parts.append(f"Conditions: {conds}")
                _add("  " + ". ".join(parts).rstrip(".") + ".")

        cols = {k: v for k, v in (data.get("sql_artifacts", {}).get("colonnes") or {}).items() if _keep(v)}
        if cols:
            _add("## Colonnes Oracle")
            for nom, e in cols.items():
                table = e.get("table", "")
                otype = e.get("type_oracle", "")
                meta = ", ".join(x for x in [table, otype] if x)
                head = f"{nom} [{meta}, {e.get('confiance','?')}]" if meta else f"{nom} [{e.get('confiance','?')}]"
                parts = [f"{head} — {e.get('label','')}"]
                sem = _first_sentence(e.get("semantique") or "")
                if sem:
                    parts.append(sem)
                vals = _vals_inline(e.get("valeurs"))
                if vals:
                    parts.append(f"Valeurs: {vals}")
                _add("  " + ". ".join(parts).rstrip(".") + ".")

        vues = {k: v for k, v in (data.get("sql_artifacts", {}).get("vues") or {}).items() if _keep(v)}
        if vues:
            _add("## Vues Oracle")
            for nom, e in vues.items():
                parts = [f"{nom} [{e.get('confiance','?')}] — {e.get('label','')}"]
                sem = _first_sentence(e.get("semantique") or "")
                if sem:
                    parts.append(sem)
                piege = e.get("piège_connu", "")
                if piege:
                    parts.append(f"Piège: {_first_sentence(piege, 120)}")
                _add("  " + ". ".join(parts).rstrip(".") + ".")

        reqs = {k: v for k, v in (data.get("sql_artifacts", {}).get("requetes") or {}).items() if _keep(v)}
        if reqs:
            _add("## Requêtes nommées")
            for nom, e in reqs.items():
                parts = [f"{nom} [{e.get('confiance','?')}] — {e.get('label','')}"]
                sem = _first_sentence(e.get("semantique") or "")
                if sem:
                    parts.append(sem)
                _add("  " + ". ".join(parts).rstrip(".") + ".")

        if not lines:
            return ""

        total = sum(len(d) for d in [codes, regles, cols, vues, reqs])
        dom_label = f"domaine: {domaine} | " if domaine else ""
        header = f"════ CONTEXTE KB ({dom_label}confiance ≥ {confiance_min} | {total} entrée(s)) ════"
        footer = "════ FIN CONTEXTE KB ════"
        if skipped:
            footer = f"[… {skipped} entrée(s) supplémentaire(s) non incluses]\n{footer}"

        return "\n".join([header, ""] + lines + ["", footer])

    def export_brief(
        self,
        domaine: Optional[str] = None,
        priorite: Optional[str] = None,
    ) -> str:
        """Brief PO à partir du pending_validation."""
        pending = self.load_pending()
        entries = list(pending.values())
        if domaine:
            entries = [e for e in entries if e.get("domaine") == domaine]
        if priorite:
            entries = [e for e in entries if e.get("priorite") == priorite]
        entries = [e for e in entries if not e.get("validated")]

        if not entries:
            return ""

        lines: list[str] = []
        domaine_label = domaine or "tous domaines"
        lines.append(f"# Brief PO — {domaine_label}")
        lines.append(f"{date.today().isoformat()} · {len(entries)} concept(s) à valider")
        lines.append("")

        type_counts = Counter(e.get("flag_type", "?") for e in entries)
        lines.append("| Type | Concepts | Priorité |")
        lines.append("|------|----------|---------|")
        for ftype, count in sorted(
            type_counts.items(),
            key=lambda kv: _TYPE_META.get(kv[0], ("🟢", kv[0]))[0],
        ):
            icon, label = _TYPE_META.get(ftype, ("⚪", ftype))
            lines.append(f"| {icon} {label} | {count} | — |")
        lines += ["", "---", ""]

        SECTION_ORDER = [
            ("dynamic_session_key",       "🔴 SESSION DYNAMIQUE"),
            ("external_state_dependency", "🔴 DÉPENDANCES EXTERNES"),
            ("hardcoded_situation_code",  "🟡 CODES HARDCODÉS"),
            ("magic_value",               "🟡 VALEURS MAGIQUES"),
            ("missing_branch",            "🟡 BRANCHES MANQUANTES"),
        ]
        CLUSTER_A = {"magic_value", "hardcoded_situation_code"}

        for ftype, section_title in SECTION_ORDER:
            section_entries = sorted(
                [e for e in entries if e.get("flag_type") == ftype],
                key=lambda e: -e.get("occurrences", 1),
            )
            if not section_entries:
                continue
            lines.append(f"## {section_title}")
            lines.append("")
            if ftype in CLUSTER_A:
                lines += ["| Valeur | Méthode(s) | ×N | Question | Réponse |",
                          "|--------|-----------|-----|---------|---------|"]
                for e in section_entries:
                    concept = e.get("concept", "")
                    value = concept.split("::", 1)[-1] if "::" in concept else concept
                    fichiers = e.get("fichiers", [])
                    methods = ", ".join(f.split(":")[0] for f in fichiers[:2])
                    q = e.get("question", "").replace("|", "·")
                    lines.append(f"| `{value}` | {methods} | ×{e.get('occurrences',1)} | {q} |  |")
            else:
                lines += ["| Méthode | ×N | Question | Réponse |",
                          "|---------|-----|---------|---------|"]
                for e in section_entries:
                    concept = e.get("concept", "")
                    method = concept.split("::", 1)[-1] if "::" in concept else concept
                    q = e.get("question", "").replace("|", "·")
                    lines.append(f"| `{method}()` | ×{e.get('occurrences',1)} | {q} |  |")
            lines += ["", "---", ""]

        lines.append("*Brief généré par **Rosetta***")
        return "\n".join(lines)

    def export_human(
        self,
        domaines: Optional[list[str]] = None,
        sources: Optional[list[str]] = None,
    ) -> str:
        """Dossier de fusion lisible humain : règles + bugs + questions."""
        kb_data = self.load()
        pending  = self.load_pending()
        domaines = domaines or []

        def _in_scope(entry: dict) -> bool:
            if not domaines:
                return True
            return entry.get("domaine", "") in domaines

        regles, bugs, codes = [], [], []
        for code, entry in (kb_data.get("regles") or {}).items():
            if not _in_scope(entry):
                continue
            if entry.get("label", code).startswith("[BUG]"):
                bugs.append((code, entry))
            else:
                regles.append((code, entry))

        for code, entry in (kb_data.get("codes") or {}).items():
            if _in_scope(entry):
                codes.append((code, entry))

        pending_items = sorted(
            [p for p in pending.values() if not p.get("validated") and _in_scope(p)],
            key=lambda p: {"high": 0, "medium": 1, "low": 2}.get(p.get("priorite", "low"), 9),
        )
        pending_decisions = [p for p in pending_items if p.get("pending_type") == 3]
        pending_new       = [p for p in pending_items if p.get("pending_type") == 2]
        pending_upgrade   = [p for p in pending_items if p.get("pending_type") == 1]

        titre_domaine = ", ".join(domaines) if domaines else "tous domaines"
        date_str = date.today().isoformat()

        lines = [
            f"# {titre_domaine} — Dossier de fusion",
            f"> Généré par **Rosetta** · {date_str} · "
            f"{len(regles)} règles · {len(codes)} codes · "
            f"{len(bugs)} bugs · {len(pending_items)} questions ouvertes",
            "",
        ]
        if sources:
            lines += ["**Fichiers PHP analysés :**", ""]
            lines += [f"- `{s}`" for s in sources]
            lines.append("")
        lines += ["---", ""]

        if regles:
            lines += [
                "## 1. Règles métier documentées", "",
                "| Règle | Comportement | Confiance | Migration |",
                "|-------|-------------|-----------|-----------|",
            ]
            for code, e in sorted(regles, key=lambda x: x[1].get("confiance", "z")):
                sem = _first_para(e.get("semantique", e.get("label", "")))
                lines.append(
                    f"| `{code}` | {sem} "
                    f"| {_conf_badge(e.get('confiance',''))} "
                    f"| {_migration_badge(e.get('migration_note', ''))} |"
                )
            lines.append("")

        if codes:
            lines += [
                "## 2. Codes et constantes connus", "",
                "| Token | Label | Contexte | Confiance | Migration |",
                "|-------|-------|---------|-----------|-----------|",
            ]
            for code, e in sorted(codes, key=lambda x: x[1].get("confiance", "z")):
                label = e.get("label", "")
                ctx_list = e.get("contextes", [])
                ctx = ctx_list[0].get("semantique", ctx_list[0].get("champ", "")) if ctx_list else ""
                lines.append(
                    f"| `{code}` | {_truncate(label, 95)} | {_truncate(ctx, 120)} "
                    f"| {_conf_badge(e.get('confiance',''))} "
                    f"| {_migration_badge(e.get('migration_note', ''))} |"
                )
            lines.append("")

        if bugs:
            lines += [
                "## 3. Bugs identifiés avant migration", "",
                "| Bug | Description | Sévérité |",
                "|-----|------------|---------|",
            ]
            for code, e in bugs:
                label = e.get("label", code).replace("[BUG] ", "")
                sev = _bug_severity(label, e.get("notes", ""))
                lines.append(f"| `{code}` | {_first_sentence(label, 260)} | {sev} |")
            lines.append("")

        if pending_items:
            lines += ["## 4. Questions ouvertes — Arbitrage requis", ""]
            prio_icon = lambda p: {"high": "🔴", "medium": "🟡", "low": "⚪"}.get(p, "")

            if pending_decisions:
                lines += [
                    "### 4a. Décisions d'architecture / comportement", "",
                    "| Priorité | Méthode | Question |",
                    "|----------|---------|---------|",
                ]
                for p in pending_decisions:
                    icon = prio_icon(p.get("priorite", ""))
                    method = (
                        (p.get("fichiers") or [""])[0].split(":")[0]
                        if p.get("fichiers") else p.get("concept", "")
                    )
                    q = (p.get("question", "") or "").replace("\n", " ").strip()
                    lines.append(f"| {icon} {p.get('priorite','').upper()} | `{method}` | {q} |")
                lines.append("")

            if pending_new:
                lines += [
                    "### 4b. Tokens non documentés — à capturer en KB", "",
                    "| Priorité | Token / Concept | Question |",
                    "|----------|----------------|---------|",
                ]
                for p in pending_new:
                    icon = prio_icon(p.get("priorite", ""))
                    concept = p.get("concept", p.get("code", ""))
                    q = (p.get("question", "") or "").replace("\n", " ").strip()
                    lines.append(f"| {icon} {p.get('priorite','').upper()} | `{concept}` | {q} |")
                lines.append("")

            if pending_upgrade:
                lines += [
                    "### 4c. Tokens en KB — à valider PO", "",
                    "| Priorité | Token | Question |",
                    "|----------|-------|---------|",
                ]
                for p in pending_upgrade:
                    icon = prio_icon(p.get("priorite", ""))
                    q = (p.get("question", "") or "").replace("\n", " ").strip()
                    lines.append(f"| {icon} {p.get('priorite','').upper()} | `{p.get('code','')}` | {q} |")
                lines.append("")

        migration_notes = [
            (code, e.get("migration_note", ""))
            for section in (regles, codes)
            for code, e in section
            if e.get("migration_note")
            and e["migration_note"].strip().lower() not in _MIGRATION_BADGE_WORDS
            and not e["migration_note"].lower().startswith("non")
        ]
        if migration_notes:
            lines += [
                "## 5. Notes de migration Symfony", "",
                "| Token | Migration | Note |",
                "|-------|-----------|------|",
            ]
            for code, note in migration_notes:
                lines.append(
                    f"| `{code}` | {_migration_badge(note)} | {_first_sentence(note, 180)} |"
                )
            lines.append("")

        lines += ["---", "", "*Document généré par **Rosetta** — outil d'audit statique PHP*"]
        return "\n".join(lines)

    # ── API publique : Migration ──────────────────────────────────────────────

    def split(self, source_path: Path) -> SplitResult:
        """Migre un YAML unique vers des fichiers par domaine dans kb_path (dossier)."""
        if not source_path.exists():
            raise FileNotFoundError(f"Source introuvable : {source_path}")
        if not self.kb_path.is_dir() and self.kb_path.exists():
            raise ValueError("kb_path doit être un répertoire, pas un fichier.")

        self.kb_path.mkdir(parents=True, exist_ok=True)

        with source_path.open(encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        global_data = {
            "meta": data.get("meta", {}),
            "pending_validation": data.get("pending_validation", {}),
        }
        self._write_file(_global_file(self.kb_path), global_data)
        pending_count = len(global_data["pending_validation"])

        domain_buckets: dict[str, dict] = {}

        def _bucket(domain: str) -> dict:
            return domain_buckets.setdefault(domain, _empty_domain())

        for section in ("codes", "regles", "schema"):
            for key, entry in (data.get(section) or {}).items():
                domain = entry.get("domaine", "commun") if isinstance(entry, dict) else "commun"
                _bucket(domain)[section][key] = entry

        sa = data.get("sql_artifacts", {})
        for sub in ("colonnes", "vues", "requetes"):
            for key, entry in (sa.get(sub) or {}).items():
                domain = entry.get("domaine", "commun") if isinstance(entry, dict) else "commun"
                _bucket(domain)["sql_artifacts"][sub][key] = entry

        domains_result: list[tuple[str, int]] = []
        total_entries = 0
        for domain, domain_data in sorted(domain_buckets.items()):
            n = sum(len(domain_data.get(s, {})) for s in ("codes", "regles", "schema"))
            n += sum(len(domain_data.get("sql_artifacts", {}).get(s, {}))
                     for s in ("colonnes", "vues", "requetes"))
            self._write_file(_domain_file(self.kb_path, domain), domain_data)
            domains_result.append((domain, n))
            total_entries += n

        return SplitResult(
            domains=domains_result,
            total_entries=total_entries,
            pending_count=pending_count,
            output_dir=self.kb_path,
        )

    def import_docs(self, docs_dir: Path, dry_run: bool = False) -> ImportResult:
        """Importe des fiches .md (frontmatter kb_type) dans le KB YAML."""
        try:
            import frontmatter as _fm
        except ImportError:
            raise ImportError("python-frontmatter requis — pip install python-frontmatter")

        if not docs_dir.exists():
            raise FileNotFoundError(f"Dossier introuvable : {docs_dir}")

        result = ImportResult()
        by_domain: dict[str, list[tuple[tuple[str, ...], str, dict, str]]] = {}

        for md_path in sorted(docs_dir.rglob("*.md")):
            try:
                post = _fm.loads(md_path.read_text(encoding="utf-8-sig"))
            except Exception as e:
                result.errors += 1
                result.messages.append(f"[E] {md_path.name} — frontmatter : {e}")
                continue

            meta = dict(post.metadata)
            kb_type = meta.get("kb_type", "").strip().lower()
            kb_nom = meta.get("kb_nom", "").strip()

            if not kb_type:
                continue
            if kb_type not in _IMPORT_TYPE_ROUTES:
                result.errors += 1
                result.messages.append(f"[E] {md_path.name} — kb_type inconnu : '{kb_type}'")
                continue
            if not kb_nom:
                result.errors += 1
                result.messages.append(f"[E] {md_path.name} — kb_nom manquant")
                continue

            domain = str(meta.get("kb_domaine") or "commun")
            sections = _import_extract_sections(post.content)
            try:
                entry = _import_build_entry(kb_type, meta, sections)
            except Exception as e:
                result.errors += 1
                result.messages.append(f"[E] {md_path.name} — construction entrée : {e}")
                continue

            route = _IMPORT_TYPE_ROUTES[kb_type]
            by_domain.setdefault(domain, []).append((route, kb_nom, entry, md_path.name))

        if not by_domain and not result.errors:
            return result

        for domain, entries in sorted(by_domain.items()):
            data = self._load_for_write(domain)
            domain_changed = False
            for route, nom, entry, fname in entries:
                node = data
                for key in route:
                    node = node.setdefault(key, {})
                existing = node.get(nom)
                if existing is None:
                    node[nom] = entry
                    result.added += 1
                    domain_changed = True
                    result.messages.append(f"[+] {nom} ({fname})")
                elif CONFIDENCE_ORDER.get(existing.get("confiance", "inferred"), 0) >= 2:
                    result.ignored += 1
                    result.messages.append(f"[!] {nom} ignoré — confiance high existante ({fname})")
                else:
                    node[nom] = entry
                    result.updated += 1
                    domain_changed = True
                    result.messages.append(f"[~] {nom} mis à jour ({fname})")
            if not dry_run and domain_changed:
                self._save_for_write(data, domain)

        return result


# ---------------------------------------------------------------------------
# Fonction standalone pour compatibilité llm_enricher / audit_service
# ---------------------------------------------------------------------------

def format_kb_for_prompt(
    data: dict,
    domaine: Optional[str] = None,
    confiance_min: str = "medium",
    max_chars: int = 4_000,
) -> str:
    """Wrapper standalone pour export_prompt (appelé depuis kb_context.py si nécessaire)."""
    from pathlib import Path as _Path
    import tempfile, yaml as _yaml
    # Crée un service éphémère pointant sur un YAML temporaire
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode="w", encoding="utf-8") as f:
        _yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
        tmp_path = _Path(f.name)
    try:
        return KBService(tmp_path).export_prompt(
            domaine=domaine, confiance_min=confiance_min, max_chars=max_chars
        )
    finally:
        tmp_path.unlink(missing_ok=True)
