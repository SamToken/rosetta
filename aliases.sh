# Rosetta KB — Aliases shell
# Usage : source ~/projects/rosetta/aliases.sh
# Ajouter dans ~/.bashrc ou ~/.zshrc : source ~/projects/rosetta/aliases.sh

# Nettoyage des éventuelles versions précédentes
unalias kb-check kb-sync kb-import kb-stats 2>/dev/null

export PATH="/home/nixos/projects/rosetta/bin:$PATH"

alias kb-check="/home/nixos/projects/rosetta/.venv/bin/python3 /home/nixos/projects/astro/.github/rosetta/kb_drift_check.py /home/nixos/projects/astro"
alias kb-sync="/home/nixos/projects/rosetta/.venv/bin/python3 /home/nixos/projects/astro/.github/rosetta/kb_update_anchors.py /home/nixos/projects/astro"
