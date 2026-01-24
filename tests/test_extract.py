#!/usr/bin/env python3
"""
Test rapide de l'extracteur PHP.
"""

import sys
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from extractors.php_extractor import extract_php
import json


def main():
    # Extraire le contrôleur de test
    sample_file = Path(__file__).parent / "sample_controller.php"
    
    print("=" * 60)
    print("🔍 Extraction du contrôleur PHP...")
    print("=" * 60)
    
    ir = extract_php(sample_file)
    
    # Afficher le résumé
    print("\n📊 RÉSUMÉ:")
    print("-" * 40)
    summary = ir.summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    # Afficher les actions trouvées
    print("\n🎯 ACTIONS TROUVÉES:")
    print("-" * 40)
    for ep in ir.entry_points:
        methods = ", ".join(ep.http_methods)
        print(f"  • {ep.name}Action  [{methods}]  →  {ep.route_pattern}")
    
    # Afficher les opérations DB
    print("\n💾 OPÉRATIONS BASE DE DONNÉES:")
    print("-" * 40)
    for op in ir.operations:
        if op.type.value.startswith("db_"):
            print(f"  [{op.type.value}] {op.details[:60]}...")
    
    # Afficher les inputs/outputs
    print("\n📥 DATA FLOW:")
    print("-" * 40)
    print(f"  Inputs: {', '.join(ir.data_flow.inputs)}")
    print(f"  Session reads: {', '.join(ir.data_flow.session_reads)}")
    print(f"  Outputs: {', '.join(ir.data_flow.outputs)}")
    
    # Afficher les dépendances
    print("\n📦 DÉPENDANCES:")
    print("-" * 40)
    for dep in ir.dependencies:
        suggested = f" → {dep.suggested_symfony}" if dep.suggested_symfony else ""
        print(f"  • {dep.name} ({dep.type}){suggested}")
    
    # Tokens estimés
    print("\n💰 ESTIMATION TOKENS:")
    print("-" * 40)
    print(f"  IR complet: ~{ir.token_estimate()} tokens")
    print(f"  (vs fichier PHP brut: ~{len(sample_file.read_text()) // 4} tokens)")
    
    # Sauvegarder l'IR en JSON
    output_file = Path(__file__).parent / "sample_ir.json"
    output_file.write_text(ir.to_json())
    print(f"\n✅ IR sauvegardé dans: {output_file}")
    
    print("\n" + "=" * 60)
    print("🎉 Extraction terminée!")
    print("=" * 60)


if __name__ == "__main__":
    main()
