<?php

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

namespace App\Service;

use App\Repository\AstroRepository;


/**
 * Description of AdeliaService
 *
 * @author
 */
class AiguillageIntervenantService
{

    protected $app;

    /**
     * @var AstroRepository
     */
    protected $astroRepository;

    protected $demandeInterventionRepository;

    protected $agpGenRepo;


    public function __construct($app)
    {
        $this->app = $app;
        $this->astroRepository = $app->get('AstroRepository');
        $this->demandeInterventionRepository = $this->app->get('DemandeInterventionRepository');
        $this->agpGenRepo = $this->app->get('AgpGeneriqueRepository');

    }

    public function getIntervenantInfos($idJeuParam, $intervenant, $typeRessource, $ticketId, $ext = '')
    {
        $intervenantInfosList = $this->agpGenRepo->getIntervenantInfos($idJeuParam, $intervenant);
        $ok = true;

        if (empty($intervenantInfosList)) {
            return $intervenantInfosList;
        }
        foreach ($intervenantInfosList as $intervenantInfos) {
            if ($intervenantInfos['VARIABLE_ADMIN'] != '* Variables *' && !is_null($intervenantInfos['CONDITION']) && !is_null($intervenantInfos['VALEUR_CONDITION'])) {
                $ok = false;
                $variable = $intervenantInfos['VARIABLE_ADMIN'];
                $argsVariableGlobal = array();
                $argsVariableGlobal[] = $variable;
                $checkVar = $this->app->get('Variable')->replaceTagsChaine("###$variable###", $argsVariableGlobal, $typeRessource, $ticketId);
                $valeurs = explode(",", $intervenantInfos['VALEUR_CONDITION']);
                foreach ($valeurs as $val) {
                    switch ($intervenantInfos['CONDITION']) {
                        case 'begin_with':
                            if (strpos($checkVar, $val) === 0) $ok = true;
                            break;
                        case 'equal':
                            if (strcmp($checkVar, $val) === 0) $ok = true;///valeurs admin case Sensitive
                            break;
                        case 'contains':
                            if (strpos($checkVar, $val) !== false) $ok = true;
                            break;
                        case '':
                            $ok = true;
                            break;

                    }
                    if ($ok) break;

                }
            } elseif ($intervenantInfos['VARIABLE_ADMIN'] != '* Variables *' && (is_null($intervenantInfos['CONDITION']) || is_null($intervenantInfos['VALEUR_CONDITION']))) {
                $ok = false;
            } elseif ($intervenantInfos['VARIABLE_ADMIN'] == '* Variables *' && (!is_null($intervenantInfos['CONDITION']) || !is_null($intervenantInfos['VALEUR_CONDITION']))) {
                $ok = false;
            } elseif($intervenantInfos['VARIABLE_ADMIN'] == '* Variables *' && (is_null($intervenantInfos['CONDITION']) || is_null($intervenantInfos['VALEUR_CONDITION']))) {
                $ok = true;
            }
            if (!is_null($intervenantInfos['TECHNO']) && $intervenantInfos['TECHNO'] != '' && $ok) {
                switch ($typeRessource) {
                    case 'CA-CASW':
                    case 'S-SUP':
                    case 'PI-PROTSW':
                    case 'E-ENERSW':
                        // EVTFIXE
                        $ok = ($intervenantInfos['TECHNO'] == 'EVTFIXE');
                        break;
                    case 'DSLAM':
                    case 'ROUTEURGE':
                    case 'SWTIP':
                    case 'ROUTIP':
                    case 'MGATEWAY':
                    case 'UNIRACC':
                    case 'CONNUM':
                    case 'COMMUT':
                        // RS
                        $ok = ($intervenantInfos['TECHNO'] == 'RS');
                        break;
                    case 'WDM_SID':
                    case 'SLN':
                    case 'SDH':
                    case 'MIE':
                        if ($typeRessource == 'MIE') {
                            $extremiteTechno = 'TECHNO';
                        } else {
                            if ($ext == 'tabs_action_ext1') {
                                $extremiteTechno = 'EXT1_TECHNO';
                            } elseif ($ext == 'tabs_action_ext2') {
                                $extremiteTechno = 'EXT2_TECHNO';
                            }
                        }
                        $argsVariableGlobal1 = array();
                        $argsVariableGlobal1[] = $extremiteTechno;
                        $techno = $this->app->get('Variable')->replaceTagsChaine("###$extremiteTechno###", $argsVariableGlobal1, $typeRessource, $ticketId);

                        if ($techno == 'FH') {
                            // FH
                            $ok = ($intervenantInfos['TECHNO'] == 'FH');
                        } else {
                            // RS
                            $ok = ($intervenantInfos['TECHNO'] == 'RS');
                        }
                        break;
                    default:
                        break;
                }
            }
            if($ok) {
                return array(
                    'ID_AIGUILLAGE' => $intervenantInfos['ID'],
                    'EDS' => $intervenantInfos['EDS'],
                    'LIBELLE_ENTITE' => $intervenantInfos['LIBELLE_ENTITE'],
                    'VARIABLE_CHECK' => $ok,
                    'TECHNO' => $intervenantInfos['TECHNO']
                );
            }
        }
        return array(
            'VARIABLE_CHECK' => $ok
        );
    }

}
