# Rosetta KB — Aliases shell
# Usage : source ~/projects/rosetta/aliases.sh
# Ajouter dans ~/.bashrc ou ~/.zshrc : source ~/projects/rosetta/aliases.sh

# Nettoyage des éventuelles versions précédentes
unalias kb-check kb-sync kb-import kb-stats 2>/dev/null

export PATH="/home/nixos/projects/rosetta/bin:$PATH"

# SOURCE_REPO : chemin vers le repo source PHP (à définir dans ~/.bashrc)
# export SOURCE_REPO=~/projects/monapp
alias kb-check="/home/nixos/projects/rosetta/.venv/bin/python3 \${SOURCE_REPO}/.github/rosetta/kb_drift_check.py \${SOURCE_REPO}"
alias kb-sync="/home/nixos/projects/rosetta/.venv/bin/python3 \${SOURCE_REPO}/.github/rosetta/kb_update_anchors.py \${SOURCE_REPO}"
