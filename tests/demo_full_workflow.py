#!/usr/bin/env python3
"""
DÉMO COMPLÈTE : PHP Legacy → IR → Prompt Symfony
=================================================

Ce script montre le workflow complet d'Antigravity :
1. Extraction d'un contrôleur PHP legacy
2. Génération de l'IR
3. Création de prompts optimisés pour l'IA
"""

import sys
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from extractors.php_extractor import extract_php
from generators.symfony_generator import SymfonyPromptGenerator


def main():
    print("=" * 70)
    print("🚀 ANTIGRAVITY - Workflow complet de migration")
    print("=" * 70)
    
    # =========================================================================
    # Étape 1 : Extraction
    # =========================================================================
    print("\n📥 ÉTAPE 1 : Extraction du PHP legacy")
    print("-" * 50)
    
    sample_file = Path(__file__).parent / "sample_controller.php"
    ir = extract_php(sample_file)
    
    print(f"   ✅ Contrôleur: {ir.metadata.controller_name}Controller")
    print(f"   ✅ Actions trouvées: {len(ir.entry_points)}")
    for ep in ir.entry_points:
        print(f"      • {ep.name} [{', '.join(ep.http_methods)}]")
    
    # =========================================================================
    # Étape 2 : Génération des prompts
    # =========================================================================
    print("\n📝 ÉTAPE 2 : Génération des prompts Symfony")
    print("-" * 50)
    
    generator = SymfonyPromptGenerator(symfony_version="6.4")
    
    # Sauvegarder tous les prompts
    output_dir = Path(__file__).parent / "generated_prompts"
    created_files = generator.save_prompts(ir, output_dir)
    
    print(f"   ✅ {len(created_files)} prompts générés dans {output_dir}/")
    
    total_tokens = 0
    for filepath in created_files:
        prompt = filepath.read_text()
        tokens = generator.estimate_tokens(prompt)
        total_tokens += tokens
        print(f"      • {filepath.name} (~{tokens} tokens)")
    
    # =========================================================================
    # Étape 3 : Afficher un exemple de prompt
    # =========================================================================
    print("\n👁️  ÉTAPE 3 : Exemple de prompt (action 'edit')")
    print("-" * 50)
    
    edit_prompt = generator.generate_action_prompt(ir, "edit")
    
    # Afficher les premières lignes
    lines = edit_prompt.split('\n')
    preview_lines = lines[:40]
    print('\n'.join(preview_lines))
    print(f"\n   [...{len(lines) - 40} lignes de plus...]")
    
    # =========================================================================
    # Résumé des économies
    # =========================================================================
    print("\n" + "=" * 70)
    print("💰 RÉSUMÉ DES ÉCONOMIES")
    print("=" * 70)
    
    php_content = sample_file.read_text()
    php_tokens = len(php_content) // 4
    
    print(f"""
    ┌─────────────────────────────────────────────────────────────┐
    │  AVANT (envoyer tout le PHP)                                │
    │  • Tokens par requête : ~{php_tokens} (fichier entier)               │
    │  • Contexte : L'IA doit tout comprendre à chaque fois       │
    │  • Risque : Hallucinations, erreurs de compréhension        │
    ├─────────────────────────────────────────────────────────────┤
    │  APRÈS (prompts par action)                                 │
    │  • Tokens par action : ~{total_tokens // len(created_files)} (moyenne)                     │
    │  • Contexte : Structuré, ciblé, clair                       │
    │  • Risque : Minimal, l'IR guide l'IA                        │
    ├─────────────────────────────────────────────────────────────┤
    │  Pour 61 contrôleurs avec ~5 actions chacun :               │
    │  • Avant : 61 × {php_tokens} = ~{61 * php_tokens:,} tokens                     │
    │  • Après : 305 × {total_tokens // len(created_files)} = ~{305 * (total_tokens // len(created_files)):,} tokens                   │
    │  • Économie : ~{100 - (305 * (total_tokens // len(created_files))) * 100 // (61 * php_tokens)}% (si même taille que sample)                │
    └─────────────────────────────────────────────────────────────┘
    """)
    
    print("\n🎯 PROCHAINE ÉTAPE :")
    print("   1. Copie un prompt généré")
    print("   2. Colle-le dans Claude ou Gemini")
    print("   3. Récupère le code Symfony généré")
    print("   4. Vérifie et ajuste si besoin")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
