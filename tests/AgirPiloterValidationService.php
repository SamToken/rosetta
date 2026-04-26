<?php

namespace App\Service;

class AgirPiloterValidationService extends ValidationService
{

    /**
     * validation formulaire retablir reparer cloturer
     *
     * @param array $data
     * @param array $regles
     * @return boolean|string[]
     */
    public function validateAgirPiloterForm(array $data, array $regles)
    {
        $result = true;
        $message = array();

        // Validation Date rétablissement
        $dateRetab = key_exists('agp_dtretab', $data) ? $data['agp_dtretab'] : '';

        if (key_exists('DATE_RETABLISSEMENT_DEMANDE_INTERVENTION',
                $regles) && $regles['DATE_RETABLISSEMENT_DEMANDE_INTERVENTION']["OBLIGATOIRE"] === '1') {
            if (!$this->notEmpty($dateRetab)) {
                $result = false;
                $message[] = 'Champ date rétablissement requis';
            }
        }
        if ($dateRetab !== '') {
            if (!$this->isDate($dateRetab, "d/m/Y H:i")) {
                $result = false;
                $message[] = 'Format date rétablissement invalide';
            }
        }

        // Date action en cours EDS
        $actionCoursEds = key_exists('agp_dtencours', $data) ? $data['agp_dtencours'] : '';

        if (key_exists('DATE_COURS_EDS_DEMANDE_INTERVENTION',
                $regles) && $regles['DATE_COURS_EDS_DEMANDE_INTERVENTION']["OBLIGATOIRE"] === '1') {
            if (!$this->notEmpty($actionCoursEds)) {
                $result = false;
                $message[] = 'Champ date action en cours requis';
            }
        }
        if ($actionCoursEds !== '') {
            if (!$this->isDate($actionCoursEds, "d/m/Y H:i")) {
                $result = false;
                $message[] = 'Format date action en cours invalide';
            }
        }

        // Validation Commentaire charté
        $commentaire = key_exists('agp_commentaire', $data) ? $data['agp_commentaire'] : '';
        if (key_exists('COMMENTAIRE_DEMANDE_INTERVENTION',
                $regles) && $regles['COMMENTAIRE_DEMANDE_INTERVENTION']["OBLIGATOIRE"] === '1') {
            if (!$this->notEmpty($commentaire)) {
                $result = false;
                $message[] = 'Champ commentaire requis';
            }
        }

        // Validation Action en cours EDS
        $actionCoursEds = key_exists('agp_action_eds', $data) ? $data['agp_action_eds'] : '';
        if (key_exists('ACTION_EN_COURS_EDS',
                $regles) && $regles['ACTION_EN_COURS_EDS']["OBLIGATOIRE"] === '1') {
            if (!$this->notEmpty($actionCoursEds)) {
                $result = false;
                $message[] = 'Champ action en cours EDS requis';
            }
        }
        // Validation du Niveau d'urgence
        $actionCoursEds = key_exists('niveau_urgence', $data) ? $data['niveau_urgence'] : '';
        if (key_exists('NIVEAU_URGENCE',
                $regles) && $regles['NIVEAU_URGENCE']["OBLIGATOIRE"] === '1') {
            if (!$this->notEmpty($actionCoursEds)) {
                $result = false;
                $message[] = 'Champ niveau d\'urgence requis';
            }
        }

        if (!$result) {
            return $message;
        }
        return true;
    }
}
