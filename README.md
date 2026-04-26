?? Rosetta ? Branch tree-rosettaOutil d'audit fonctionnel et d'extraction de connaissance pour la migration de systèmes PHP legacy (Zend/Astro) vers Symfony.Rosetta ne se contente plus de lire du texte ; elle comprend la structure du code grâce à un arbre syntaxique abstrait (AST). Elle produit des livrables stratégiques pour le Product Owner : règles métier extraites, comportements non définis (Gaps), et cartographie des risques, le tout sans jargon technique.?? Principe : "Structural Truth"Rosetta fonctionne en deux passes complémentaires :Extraction Structurelle (AST via Tree-sitter) : Le code PHP est analysé localement. L'AST garantit une fiabilité de 100% sur la détection des méthodes, des blocs if/else imbriqués et des injections de services. Le Flag Engine identifie les "points noirs" (Gaps de logique, dépendances critiques, couplage fort).Enrichissement Sémantique (LLM) : Seuls les fragments de code flaggués et leurs commentaires adjacents sont transmis à Claude. Le LLM traduit la structure technique en règle métier en français, prête pour un arbitrage PO.Philosophie : Deterministic AST for structure, Probabilistic LLM for meaning.?? InstallationPour les utilisateurs NixOS (recommandé) ou environnements Python standards :Bash# Installation des dépendances système (NixOS)
# Ajoutez pkgs.graphviz et pkgs.tree-sitter à votre shell.nix

pip install tree-sitter tree-sitter-php anthropic pydantic python-dotenv
Configuration du .env :BashANTHROPIC_API_KEY=sk-ant-...
?? UsageAnalyse d'un composant uniqueBashpython rosetta_analyze.py AssistantController.php --output-dir ./output
Fichier produitDestinataireContenu<Nom>_business_doc.mdProduct OwnerSynthèse des règles, Gaps à arbitrer, Score de risque.<Nom>_flags.mdTech LeadDétail technique des alertes (Lignes, Types de n½uds).<Nom>_business_logic.jsonPipeline / RAGIR complet (JSON) pour ingestion IA.Mode Batch (Répertoire complet)Bashpython rosetta_analyze.py ./src/Controller/ --output-dir ./audit_report
Génère un global_audit.md avec la matrice de décision transverse et le score de santé global.?? Risk Scoring & Santé FonctionnelleRosetta calcule un score de risque automatisé pour chaque méthode afin de prioriser la migration :$$Score_{Risque} = (Complexity_{Cyclomatic} \times 2) + (Coupling_{Services} \times 5) + (Magic_{Values} \times 3)$$?? Critique (Score > 70) : Méthodes "God Object", couplage extrême, logique opaque.?? Modéré (Score 30-70) : Logique à isoler dans des services dédiés.?? Sain (Score < 30) : Code prêt pour une migration directe.?? Architecture de la branche treePlaintextrosetta/
??? extractors/
?   ??? php_extractor.py    <-- Parseur AST (Tree-sitter PHP)
?       ??? _extract_params_ast()      # Extraction typée des signatures
?       ??? _extract_control_flow_ast() # Détection chirurgicale des if/else
?       ??? _link_comments()           # Corrélation Commentaires <-> Code
?
??? analyzers/
?   ??? flag_engine.py      <-- Moteur de règles (Missing Else, Empty Catch, etc.)
?   ??? risk_analyzer.py    <-- Calculateur de complexité et de couplage
?
??? aggregators/
?   ??? business_aggregator.py  <-- Consolidation (57 Gaps vs 106 Flags)
?
??? generators/
    ??? business_doc_generator.py  <-- Rendu Markdown "PO-Friendly"
?? Confidentialité & PerformanceZéro "Full-File" Upload : Le fichier PHP complet n'est jamais envoyé au LLM. Seuls les fragments identifiés par l'AST (ex: un bloc if spécifique) sont transmis.Précision AST : Réduction de 44% des faux positifs par rapport à l'ancienne version Regex.Prompt Caching : Optimisation des coûts Anthropic sur les analyses de masse.?? Roadmap tree-rosetta[x] Migration complète vers Tree-sitter (Structure & Flow)[x] Implémentation du Risk Scoring (Complexité & Couplage)[x] Corrélation automatique Code/Commentaires (Business Context)[ ] Génération de graphes de dépendances Graphviz (DOT)[ ] Export des matrices de décision vers Jira/Confluence