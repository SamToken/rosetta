<?php

namespace App\Service;

/**
 * Fixture ciblant les regex magic_value (P1 - DÉFAUT B).
 * Tokens 100 % fictifs — aucune donnée métier réelle (règle CLAUDE.md #1).
 */
class MagicValueService
{
    public function evalStatus($statusFoo, $count, $ref, $flags, $module)
    {
        // Comparaison chaîne PascalCase / mixte — avant : ratée ([a-z_]+ only)
        if ($statusFoo == 'Wibbled') {
            return 1;
        }
        // Comparaison chaîne MAJUSCULES
        if ($ref != 'ACMEREF') {
            return 2;
        }
        // Entier quoté à un chiffre — avant : raté (\d{2,})
        if ($count == '3') {
            return 3;
        }
        // Entier non quoté à un chiffre — avant : raté
        if ($count == 7) {
            return 4;
        }
        // Bruit à filtrer : 0/1, true, chaîne vide
        if ($count == 1) {
            return 5;
        }
        if ($ref == '') {
            return 6;
        }
        // in_array literal — avant : non couvert
        if (in_array('FLAG_ALPHA', $flags)) {
            return 7;
        }
        // switch/case mixte
        switch ($module) {
            case 'Frobnik':
                return 8;
            case 'STEP_TWO':
                return 9;
        }
        return 0;
    }
}
