<?php

/**
 * LHMIDI
 * Class assistant permet de créer le bandeau
 */

namespace App\Helper;

use App\Repository\AstroLienRepository;
use App\Repository\GlobalApiRepository;
use App\Repository\VariableRepository;
use App\Service\TransitoolService;
use App\Tools\OceaneAssistant;
use App\Tools\OceaneTools;
use App\Service\AdminFonctionService;
use Oft\Mvc\Application;
use App\Service\AssistantService;
use App\Service\VariableBaseService;

class Assistant extends VariableBaseService
{

    /**
     * @var Application
     */
    protected $app;

    protected $urlget;

    protected $astroId = 0;

    protected $ticketId = '';

    protected $typeRessource = '';

    protected $dslam = '';

    protected $linkOoutils = array();

    protected $nature = '';

    protected $access = '';

    protected $eds = '';

    protected $id1 = '';

    protected $id2 = '';

    protected $id3 = '';

    protected $pilotGroup;

    protected $status;

    protected $typetic;

    protected $type;

    protected $sessionId;

    protected $findAndGet;

    protected $troubleDetectionDate;

    protected $data;

    protected $bandeau;

    protected $idRessource;

    protected $typeTicket;

    /**
     *
     * @var AstroLienRepository
     */
    protected $astroLienRepository;

    /**
     *
     * @var GlobalApiRepository
     */
    protected $globalApiRepository;
    /**
     * @var VariableRepository
     */
    protected $variableRepository;

    protected $traceRepository;

    protected $session;

    /**
     *
     * @var AssistantService
     */
    protected $assistantService;

    protected $astroRepository;

    protected $oceaneAssistant;

    protected $informationsRessourceCommut;

    protected $listIncident;

    /**
     *
     * @var AdminFonctionService
     */
    protected $adminFonction;

    /**
     * @var TransitoolService
     */
    protected $transitoolService = null;

    protected $typeUn;

    public function __construct($data, $app)
    {
        $this->app = $app;
        $this->adminFonction = $this->app->get('AdminFonction');
        $this->listIncident = array(15, 1, 4);
        $this->astroLienRepository = $app->get('AstroLienRepository');
        $this->globalApiRepository = $app->get('GlobalApiRepository');
        $this->traceRepository = $app->get('TraceRepository');
        $this->assistantService = $app->get('AssistantService');
        $this->astroRepository = $app->get('AstroRepository');
        $this->variableRepository = $app->get('VariableRepository');
        $this->oceaneAssistant = new OceaneAssistant($app);
        $this->session = $this->app->get('Session');
        $this->initParams($data);
        $this->data = $data;
        $this->setAstroSession();

    }

    /**
     * Création du bandeau d'astro mobile
     *
     * @param
     *            string
     * @return array
     */
    public function getOutils($bandeau)
    {
        return $this->astroLienRepository->listeCategorieBandeau($bandeau);
    }

    /**
     * Récupération de la liste des liens par catégorie
     *
     * @param string $bandeau
     * @return array
     */
    public function getlisteByCat($bandeau, $type)
    {
        $tabListByCategorie = $this->astroLienRepository->getListeBtnByCat($bandeau, $this->typeRessource);
        $result = array();

        foreach ($tabListByCategorie as $k => $outils) {
            $result[$k] = array();
            foreach ($outils as $outil) {
                foreach ($outil['LIEN'] as $lien) {
                    $query = parse_url($lien['LIEN'], PHP_URL_QUERY);
                    if (parse_url($lien['LIEN'], PHP_URL_FRAGMENT)) {
                        $query .= '#' . parse_url($lien['LIEN'], PHP_URL_FRAGMENT);
                    }
                    $args = OceaneTools::getContents($query, '###', '###');
                    $lien['LIEN'] = $this->replaceTags($lien['LIEN'], $args, $type);
                    if ($lien['LIEN']) {
                        array_push($result[$k], array(
                            'nom' => $outil['NOM'],
                            'lien' => $lien['LIEN']
                        ));
                        break;
                    }
                }
            }
            if (empty($result[$k])) {
                unset($result[$k]);
            }
        }
        return $result;
    }

    /**
     * Récupération du numéro de ticket
     *
     * @return string|array
     */
    public function getTicketId()
    {
        return $this->ticketId;
    }

    public function getTroubleDetectionDate()
    {
        return $this->troubleDetectionDate;
    }

    /**
     * iniation des paramètres
     *
     * @param array $data
     */
    protected function initParams($data)
    {
        $this->typeUn = array('DSLAM', 'UNIRACC', 'CONNUM', 'COMMUT');
        $this->urlget = $data;
        $this->ticketId = $data['ticketid'];
        $this->dslam = strtoupper($data['id1']);
        $this->typeRessource = $data['type'];
        $this->nature = $data['nature'];
        $this->access = $data['access'];
        $this->eds = $data['connectedgroup'];
        $this->id1 = $data['id1'];
        $this->id2 = $data['id2'];
        $this->id3 = $data['id3'];
        $this->typetic = $data['typetic'];
        $this->typeTicket = $this->assistantService->getTypeTicket($data['type']);
        $this->sessionId = $this->session->getUtilisateurId();
        $this->status = $data['status'];
        $this->pilotGroup = $data['pilotgroup'];
        $this->bandeau = $data['bandeau'];
        $this->idRessource = null;
        $this->sessionId = null;
        if (is_null($this->findAndGet)) {
            $this->findAndGet = $this->app->get('OceaneService')->findAndGetOceane($this->ticketId);
        }
    }

    /**
     * replacer les Tags par les valeurs
     *
     * @param string $lien
     * @param array $args
     * @return string
     */
    public function replaceTags($lien, $args, $type)
    {
        $resourceSpecification = "";

        if (count($args) === 0) {
            $change = true;
        } else {
            $change = false;
        }

        foreach ($args as $arg) {

            switch ($arg) {
                case 'transitool_tronc_ext_1':
                case 'transitool_tronc_ext_2':
                case 'transitool_tronc_troncon':
                case 'transitool_tronc_cable':
                case 'transitool_tronc_longueur':
                case 'transitool_tronc_paire':
                    if (is_null($this->transitoolService)) {
                        $this->transitoolService = $this->app->get('Transitool');
                    }

                    $replaceValue = $this->transitoolService->getValueTronconTransitool($arg, $this->id3, $this->typeRessource, $this->astroId);

                    if (!OceaneTools::isValidVariable($replaceValue)) {
                        $lien = false;
                        break 2;
                    }

                    $lien = str_replace('###' . $arg . '###', $replaceValue, $lien);
                    $change = true;
                    break;
                case 'CUID':
                    $replaceValue = (!is_null($this->session->getUtilisateurLogin())) ? $this->session->getUtilisateurLogin() : '';
                    if (!OceaneTools::isValidVariable($replaceValue)) {
                        $lien = false;
                        break 2;
                    }

                    $lien = str_replace('###' . $arg . '###', $replaceValue, $lien);
                    $change = true;
                    break;
                case 'TICKETID':
                    $replaceValue = (!is_null($this->ticketId)) ? $this->ticketId : '';

                    if (!OceaneTools::isValidVariable($replaceValue)) {
                        $lien = false;
                        break 2;
                    }

                    $lien = str_replace('###' . $arg . '###', $replaceValue, $lien);
                    $change = true;
                    break;
                case 'NIDT':
                    $replaceValue = (!is_null($this->getCodeNidt())) ? $this->getCodeNidt() : '';

                    if (!OceaneTools::isValidVariable($replaceValue)) {
                        $lien = false;
                        break 2;
                    }
                    $lien = str_replace('###' . $arg . '###', $replaceValue, $lien);
                    $change = true;
                    break;
                case 'DSLAM_MAJ':
                    $replaceValue = (!is_null($this->getDslam('MAJ'))) ? $this->getDslam('MAJ') : '';

                    if (!OceaneTools::isValidVariable($replaceValue)) {
                        $lien = false;
                        break 2;
                    }
                    $lien = str_replace('###' . $arg . '###', $replaceValue, $lien);
                    $change = true;
                    break;
                case 'DSLAM_MIN':
                    $replaceValue = (!is_null($this->getDslam('MIN'))) ? $this->getDslam('MIN') : '';

                    if (!OceaneTools::isValidVariable($replaceValue)) {
                        $lien = false;
                        break 2;
                    }
                    $lien = str_replace('###' . $arg . '###', $replaceValue, $lien);
                    $change = true;
                    break;
                case 'PILOTE':
                    $replaceValue = (!is_null($this->eds)) ? $this->eds : '';

                    if (!OceaneTools::isValidVariable($replaceValue)) {
                        $lien = false;
                        break 2;
                    }

                    $lien = str_replace('###' . $arg . '###', $replaceValue, $lien);
                    $change = true;
                    break;
                case 'TYPE':
                    $replaceValue = (!is_null($this->typeRessource)) ? $this->typeRessource : '';

                    if (!OceaneTools::isValidVariable($replaceValue)) {
                        $lien = false;
                        break 2;
                    }

                    $lien = str_replace('###' . $arg . '###', $replaceValue, $lien);
                    $change = true;
                    break;
                case 'TOKEN':
                    $token = base64_encode(md5(date('yyyymmdd') . 'link_astro_charter'));
                    $lien = str_replace('###' . $arg . '###', $token, $lien);
                    $change = true;
                    break;

                case 'DATE':
                    if (is_null($this->findAndGet)) {
                        $this->findAndGet = $this->app->get('OceaneService')->findAndGetOceane($this->getTicketId());
                    }

                    $replaceValue = isset($this->findAndGet['fg_date']) ? $this->findAndGet['fg_date'] : '';

                    if (!OceaneTools::isValidVariable($replaceValue)) {
                        $lien = false;
                        break 2;
                    }

                    $lien = str_replace('###' . $arg . '###', $replaceValue, $lien);
                    $change = true;
                    break;
                case 'FG_NOMNAEQP':
                case 'FG_E1NOMNAEQP':
                case 'FG_E2NOMNAEQP':
                    if (is_null($this->findAndGet)) {
                        $this->findAndGet = $this->app->get('OceaneService')->findAndGetOceane($this->getTicketId());
                    }
                    if (!isset($this->findAndGet['message']) && !is_null($this->findAndGet['installed_resource']) && property_exists($this->findAndGet['installed_resource'],
                            'Parameters') && property_exists($this->findAndGet['installed_resource']->Parameters, 'Parameter')) {
                        $result = OceaneTools::searchValueInFindAndGet(substr($arg, 3), $this->findAndGet['installed_resource']->Parameters->Parameter);
                        $replaceValue = (!is_null($result)) ? $result : '';

                        if (!OceaneTools::isValidVariable($replaceValue)) {
                            $lien = false;
                            break 2;
                        }

                        $lien = str_replace('###' . $arg . '###', $replaceValue, $lien);
                        $change = true;
                    } else {
                        $lien = false;
                        break 2;
                    }
                    break;
                case 'RD3+':
                    if (is_null($this->findAndGet)) {
                        $this->findAndGet = $this->app->get('OceaneService')->findAndGetOceane($this->getTicketId());
                    }

                    if (!isset($this->findAndGet['message']) && !is_null($this->findAndGet['rd_plus'])) {
                        $replaceValue = (!is_null($this->findAndGet['rd_plus'])) ? $this->findAndGet['rd_plus'] : null;

                        if (!OceaneTools::isValidVariable($replaceValue)) {
                            $lien = false;
                            break 2;
                        }

                        $lien = str_replace('###' . $arg . '###', $replaceValue, $lien);
                        $change = true;
                    } else {
                        $lien = false;
                        break 2;
                    }
                    break;

                case 'DESCRIPTION':
                    if (is_null($this->findAndGet)) {
                        $this->findAndGet = $this->app->get('OceaneService')->findAndGetOceane($this->getTicketId());
                    }

                    if (!isset($this->findAndGet['message']) && !is_null($this->findAndGet['description'])) {
                        $replaceValue = (!is_null($this->findAndGet['description'])) ? $this->findAndGet['description'] : null;

                        if (!OceaneTools::isValidVariable($replaceValue)) {
                            $lien = false;
                            break 2;
                        }

                        $lien = str_replace('###' . $arg . '###', $replaceValue, $lien);
                        $change = true;
                    } else {
                        $lien = false;
                        break 2;
                    }
                    break;
                case 'Intervenant_EVT':
                    if (is_null($this->findAndGet)) {
                        $this->findAndGet = $this->app->get('OceaneService')->findAndGetOceane($this->getTicketId());
                    }

                    if (!isset($this->findAndGet['message']) && !is_null($this->findAndGet['code_detecteur'])) {
                        if (!is_null($this->findAndGet['code_detecteur'])) {
                            $replaceValue = ($this->findAndGet['code_detecteur'] != "ORANGE") ? $this->findAndGet['code_detecteur'] : "UI";
                        } else {
                            $replaceValue = null;
                        }

                        if (!OceaneTools::isValidVariable($replaceValue)) {
                            $lien = false;
                            break 2;
                        }

                        $lien = str_replace('###' . $arg . '###', $replaceValue, $lien);
                        $change = true;
                    } else {
                        $lien = false;
                        break 2;
                    }
                    break;

                default:

                    if ($this->globalApiRepository->isVariableAdminExist($arg, $type)) {

                        if (is_null($this->findAndGet)) {
                            $this->findAndGet = $this->app->get('OceaneService')->findAndGetOceane($this->getTicketId());
                        }
                        if (!isset($this->findAndGet['message'])) {

                            if (!is_null($this->findAndGet['installed_resource']) && property_exists($this->findAndGet['installed_resource'], 'ResourceSpecification') && property_exists($this->findAndGet['installed_resource']->ResourceSpecification,
                                    'resourceSpecificationCode')) {
                                $resourceSpecification = $this->findAndGet['installed_resource']->ResourceSpecification->resourceSpecificationCode;
                            } elseif (!is_null($this->findAndGet['installed_service']) && property_exists($this->findAndGet['installed_service'], 'ServiceSpecification') && property_exists($this->findAndGet['installed_service']->ServiceSpecification,
                                    'serviceSpecificationCode')) {
                                $resourceSpecification = $this->findAndGet['installed_service']->ServiceSpecification->serviceSpecificationCode;
                            }


                            if ($resourceSpecification != "") {

                                $data = array(
                                    'type' => $resourceSpecification,
                                    'nom' => $arg
                                );
                                $tabIdentifiants = $this->globalApiRepository->getIdentifiantsAdmin($data);
                                if (count($tabIdentifiants) > 0) {
                                    $replaceValue = $this->getVariableAdminValue($tabIdentifiants);
                                    if (!$replaceValue) {
                                        $lien = false;
                                        break 2;
                                    }

                                    $lien = str_replace('###' . $arg . '###', $replaceValue, $lien);
                                    $change = true;
                                    break;
                                }
                                $lien = false;
                                break 2;
                            } else {
                                $lien = false;
                                break 2;
                            }
                        } else {
                            $lien = false;
                            break 2;
                        }
                    } else {
                        $lien = false;
                        break 2;
                    }
            }
        }

        if ($change) {
            return $lien;
        }

        return false;
    }


    public function getAstroId()
    {
        return $this->astroId;
    }

    private function setAstroSession()
    {
        $dataTicket = $this->astroRepository->getTicketInit($this->ticketId);
        if (empty($dataTicket)) {
            $astroSession = $this->createTicket();
        } else {

            $this->idRessource = $dataTicket['ID_RESSOURCE'];
            $this->astroId = $dataTicket['ID_TICKET_ASTRO'];
            $astroSession = $this->updateTicket($dataTicket);
        }
        // Sauvegarde données en session
        $astroSession['ticketSession']['id_marine'] = $this->astroRepository->getMarineId($this->ticketId);

        $astroSession['ticketSession']['type_ticket'] = $this->typeTicket;
        $astroSession['astroIdSession']['type_ticket'] = $this->typeTicket;
        $astroTicketName = 'astroOft' . strtoupper($this->ticketId);
        $this->session->set($astroTicketName, $astroSession['ticketSession']);

        $astroIdName = 'astroOft' . $this->astroId;
        $this->session->set($astroIdName, $astroSession['astroIdSession']);
    }

    private function createTicket()
    {
        $astroIdSession = array();
        $idJeuParam = '';
        $isDslam = false;
        $idBandeau = $this->astroRepository->getBandeauId($this->bandeau);
        if (is_null($this->findAndGet)) {
            $this->findAndGet = $this->app->get('OceaneService')->findAndGetOceane($this->ticketId);
        }
        if (!empty($this->findAndGet) && !isset($this->findAndGet['message'])) {
            $libTechnique = $this->oceaneAssistant->antiquote($this->findAndGet['libelle_technique']);
            $typeRessourceIdr = $this->oceaneAssistant->antiquote($this->findAndGet['type_ressource']);
            $description = (in_array($this->typeRessource, $this->typeUn)) ? $libTechnique : $this->oceaneAssistant->antiquote($this->findAndGet['description']);

            $result = array(
                'session_id' => $this->sessionId,
                'trouble_detection_date' => key_exists('trouble_detection_date', $this->findAndGet) ? $this->findAndGet['trouble_detection_date'] : '',
                // 'troubleDetectionDateFormatted' => $this->oceaneAssistant->changeUTCToDate($this->findAndGet['trouble_detection_date']),
                'ressource' => key_exists('ressource', $this->findAndGet) ? $this->findAndGet['ressource'] : '',
                'type_ressource_iadr' => $typeRessourceIdr,
                'libelle_technique' => $libTechnique,
                'description' => $description,
                'code_detecteur' => key_exists('code_detecteur', $this->findAndGet) ? $this->findAndGet['code_detecteur'] : '',
                'priority' => key_exists('priority', $this->findAndGet) ? $this->findAndGet['priority'] : '',
                'category' => key_exists('category', $this->findAndGet) ? $this->findAndGet['category'] : '',
                'description_evt_incident' => ($this->typetic == '64') ? 1 : 0

            );
            //supprimer le controle type de ressource pour que les tickets evt, default... puissent avoir l'id ressource (suite a une demande au niveau d'historique génerique)
            if ($this->typeRessource == 'DSLAM') {
                $isDslam = true;
            }
        }

        $result['session_id'] = $this->sessionId;
        $result['status'] = $this->status;
        $result['type_ressource'] = $this->typeRessource;

        if ($isDslam) {
            $ressource = $this->oceaneAssistant->detailMateriel($result['ressource'], $result['type_ressource_iadr'], $result['code_detecteur'], $result['description'], $this->id1);

            $this->idRessource = $this->astroRepository->createRessource($ressource);
            $result['id_ressource'] = $this->idRessource;
            // Détail du matériel
            if ($this->typetic == '64') {
                $idJeuParam = $this->astroRepository->getJeuParamByBandeauFonction($idBandeau, 'ABONDONNER');
            }
            $result['id_jeu_param'] = $idJeuParam;
            $this->astroRepository->addTicket($this->ticketId, $this->status, $result);
            $this->astroId = $this->astroRepository->getAstroIdByTicket($this->ticketId);
            $result['astroid'] = $this->astroId;

            // Si autre chose qu'un DSLAM, on doit créer la ressource du DSLAM uniquement
            if ($ressource['ID_TYPE_RESSOURCE'] != '1' && $ressource['ID_TYPE_RESSOURCE'] != '9') {
                $inj['ID_TYPE_RESSOURCE'] = '1';
                $inj['DSLAM'] = $ressource['DSLAM'];
                $idRessourceDslam = $this->astroRepository->createRessource($inj);
                $this->astroRepository->updateTicketDslam($this->astroId, $idRessourceDslam);
            }
        } else {
            if ($this->access != 'CRE') {
                if ($this->typetic == '64') {
                    $idJeuParam = $this->astroRepository->getJeuParamByBandeauFonction($idBandeau, 'ABONDONNER');
                }
                $result['id_jeu_param'] = $idJeuParam;
                $result['id_ressource'] = $this->idRessource;
                $this->astroRepository->addTicket($this->ticketId, $this->status, $result);
                $this->astroId = $this->astroRepository->getAstroIdByTicket($this->ticketId);
                $result['astroid'] = $this->astroId;
            }
        }

        $this->traceRepository->setTrace($this->astroId, "INIT", $result, $this->sessionId, $this->ticketId);
        $this->traceRepository->setTrace($this->astroId, "URL", $this->data, $this->sessionId, $this->ticketId);

        // incident
        if (in_array($this->typetic, $this->listIncident)) {
            $this->assistantService->evtToIncident($this->astroId, 'incident');
            $result['EVT_INCIDENT'] = 'incident';
        } // evenement
        else {
            if ($this->typetic == '64') {
                $this->assistantService->evtToIncident($this->astroId, 'événement');
                $result['EVT_INCIDENT'] = 'événement';
            } else {
                $result['EVT_INCIDENT'] = '';
            }
        }

        // Session
        $dataTicketId = $result;
        $dataTicketId['id_ressource'] = $this->idRessource;
        $dataTicketId['id_ticket_oceane'] = $this->ticketId;
        $dataTicketId['bandeau'] = $this->bandeau;
        $dataTicketSession = $this->session->get('astro' . $this->ticketId);
        $ticketSession = array_merge($dataTicketSession, $dataTicketId);

        $astroIdSession = $result;
        $astroIdSession['id_ressource'] = $this->idRessource;
        $astroIdSession['id_ticket_oceane'] = $this->ticketId;
        return array(
            'ticketSession' => $ticketSession,
            'astroIdSession' => $astroIdSession
        );
    }

    private function updateTicket($data)
    {
        $dateDetection = '';
        $result['type_ressource'] = $this->typeRessource;
        $codeDetecteur = '';
        $libelleTechnique = '';
        $descriptionFg = '';

        if (!empty($this->findAndGet)) {
            $dateDetection = key_exists('trouble_detection_date', $this->findAndGet) ? $this->findAndGet['trouble_detection_date'] : '';
            $description = key_exists('description', $this->findAndGet) ? $this->findAndGet['description'] : '';
            $descriptionFg = $this->oceaneAssistant->antiquote($description);
            $libelleTechnique = key_exists('libelle_technique', $this->findAndGet) ? $this->findAndGet['libelle_technique'] : '';
            $codeDetecteur = key_exists('code_detecteur', $this->findAndGet) ? $this->findAndGet['code_detecteur'] : '';
        }
        $result['trouble_detection_date'] = ($dateDetection != '') ? $dateDetection : $data['DT_DEBUT_ALARME_IADR'];
        $result['ressource'] = $data['RESSOURCE_IADR'];
        $result['type_ressource_iadr'] = $data['TYPE_RESSOURCE_IADR'];
        $result['libelle_technique'] = $data['LB_TECHNIQUE_IADR'];
        $result['description'] = $data['DESCRIPTION_ALARME'];
        $result['code_detecteur'] = $data['CODE_DETECTEUR_IADR'];
        $result['priority'] = $data['PRIORITE_INITIAL'];
        $result['ticket_adelia'] = $data['TICKETADELIAID'];
        $result['simulation_maestro'] = $data['SIMULATION_MAESTRO'];
        $result['astroid'] = $data['ID_TICKET_ASTRO'];
        $result['impact_nature'] = $data['IMPACT_NATURE'];

        $this->traceRepository->setTrace($data['ID_TICKET_ASTRO'], "INIT", $result, $this->sessionId, $this->ticketId);
        $this->traceRepository->setTrace($data['ID_TICKET_ASTRO'], "URL", $this->data, $this->sessionId, $this->ticketId);

        if ($data['DESCRIPTION_EVT_INCIDENT'] == 1) {
            $result['description_evt_incident'] = (in_array($this->typetic, $this->listIncident)) ? 2 : 1;
        } else {
            $result['description_evt_incident'] = $data['DESCRIPTION_EVT_INCIDENT'];
        }
        // incident
        if (in_array($this->typetic, $this->listIncident)) {
            $result['EVT_INCIDENT'] = 'incident';
        } // evenement
        else {
            if ($this->typetic == '64') {
                $result['EVT_INCIDENT'] = 'événement';
            } else {
                $result['EVT_INCIDENT'] = '';
            }
        }

        $dataUp = array(
            'astroid' => $result['astroid'],
            'status' => $this->status,
            'dt_debut_alarme_iadr' => $result['trouble_detection_date'],
            'code_detecteur_iadr' => $codeDetecteur,
            'lb_technique_iadr' => $this->oceaneAssistant->antiquote($libelleTechnique),
            'evt_incident' => $result['EVT_INCIDENT'],
            'description_evt_incident' => $result['description_evt_incident'],
            'priorite_initial' => $result['priority'],
            'impact_nature' => $result['impact_nature'],
        );

        if ($result['description'] == null && !in_array($this->typeRessource, $this->typeUn)) {
            $dataUp['description'] = $descriptionFg;
        } else {
            $dataUp['description'] = $result['description'];
        }

        $this->astroRepository->updateTicket($dataUp);

        // Session
        $dataTicketId = $result;
        $dataTicketId['id_ressource'] = $this->idRessource;
        $dataTicketId['id_ticket_oceane'] = $this->ticketId;
        $dataTicketId['bandeau'] = $this->bandeau;
        $dataTicketSession = $this->session->get('astro' . $this->ticketId);
        $ticketSession = array_merge($dataTicketSession, $dataTicketId);

        $astroIdSession = $result;
        $astroIdSession['id_ressource'] = $this->idRessource;
        $astroIdSession['id_ticket_oceane'] = $this->ticketId;

        return array(
            'ticketSession' => $ticketSession,
            'astroIdSession' => $astroIdSession
        );
    }


    public function getVariables($idJeu, $type)
    {
        $variables = array();
        $result = $this->app->get('AffichageDonneesReferentiellesRepository')->getVariables($idJeu, $type);
        if (count($result) > 0) {
            foreach ($result as $identifiant) {
                $value = $this->adminFonction->replaceVariables($identifiant, $this->ticketId, $type);
                $variables[$identifiant['LIBELLE_BLOC_INFO']] = $value;
            }
        }
        return $variables;
    }

    public function getAlarmeLibelle($descriptionTooltip, $descriptionTronque)
    {
        return '<span ' . $descriptionTooltip . '>' . $descriptionTronque . "</span>";
    }

}

