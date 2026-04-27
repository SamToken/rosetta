.PHONY: kb-check kb-sync kb-import kb-full

ASTRO_ROOT   := $(HOME)/projects/astro
ROSETTA_ROOT := $(HOME)/projects/rosetta
PYTHON       := $(ROSETTA_ROOT)/.venv/bin/python3

kb-check:
	$(PYTHON) $(ASTRO_ROOT)/.github/rosetta/kb_drift_check.py $(ASTRO_ROOT)

kb-sync:
	$(PYTHON) $(ASTRO_ROOT)/.github/rosetta/kb_update_anchors.py $(ASTRO_ROOT)

kb-import:
	$(PYTHON) $(ROSETTA_ROOT)/kb_import.py $(ASTRO_ROOT)/.github/kb/

kb-full: kb-sync kb-import
	$(PYTHON) $(ROSETTA_ROOT)/rosetta_kb.py stats
