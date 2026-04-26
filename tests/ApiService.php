<?php
/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

namespace App\Service;

use App\ApiException\BadRequestException;
use App\ApiException\ScenarioDesactiveException;
use App\Tools\OceaneAssistant;
use Hbm\Common\Tools\StringTools;
use Hbm\Globalapi\Service\Soap\OceaneFg;
use App\ApiException\PreRequirementException;
use App\Tools\Message;
use Hbm\Globalapi\Service\Soap\OceaneUpd;
use App\ApiException\UpdateOceaneException;

/**
 * Description of ApiService
 *
 * @author mbiyoud
 */
class ApiService
{
    protected $apiRepository;
    protected $astroRepository;
    protected $globalApiUrlService;
    protected $assistantRepository;
    protected $oceaneAssistant;
    protected $ihmUserRepository;
    protected $traceRepository;
    protected $automatisationRepository;
    protected $apiRepoAuto;
    protected $messageFile;
    protected $sessId;
    protected $enchainementRepo;
    /**
     * @var OceaneGetService
     */
    protected $getOceane;

    public function __construct($app)
    {
        $this->app = $app;
        $this->apiRepository = $app->get('ApiRepository');
        $this->automatisationRepository = $app->get('AutomatisationRepository');
        $this->astroRepository = $app->get('AstroRepository');
        $this->globalApiUrlService = $app->get('GlobalApiUrlService');
        $this->assistantRepository = $app->get('AssistantRepository');
        $this->oceaneAssistant = new OceaneAssistant($app);
        $this->ihmUserRepository = $app->get('IhmUtilisateurRepository');
        $this->traceRepository = $app->get('TraceRepository');
        $messageFileName = $this->app->config['message_file'];
        $this->messageFile = DATA_DIR . '/' . $messageFileName;
        $this->sessId = (key_exists('api', $this->app->config) && $this->app->config['api']) ? $this->getUserId() : $this->app->get('Session')->getUtilisateurId();
        $this->validator = $this->app->get('Validation');
        $this->globalApiRepository = $app->get('GlobalApiRepository');
        $this->enchainementRepo = $this->app->get('EnchainementRepository');
    }

    public function initApi($ticketId, $eds)
    {
        //DATA INIT
        $edsActif = '';
        $lbSuccint = '';
        $cuid = 'public';
        $idUser = '';
        $this->getOceane = $this->app->get('OceaneGet');
        $cuidUpdate = $this->app->get('AstroRepository')->getCompteMachine($eds);

        $resultatO = $this->getOceane->getOceaneData($ticketId, $cuidUpdate);

        try {
            //Get FindAndGet Data
            //Check if fg is well received
            if (key_exists('code', $resultatO) && $resultatO['code'] != 60) {
                $message = $resultatO['message'] . ' ' . $resultatO['code'];
            } elseif (key_exists('code', $resultatO) && $resultatO['code'] == 60) {
                $message = 'Ticket ' . $ticketId . ' est inexistant dans océane !';
            } elseif (key_exists('id', $resultatO)) {
                //Hno
                $hno = $this->getOceane->getHno();
                //TIKETOCEANEID
                $ticketId = $this->getOceane->getId();
                //EDS_ACTIF et POSTE_ASSOCIE / ACTIF (1/0)
                $edsPilote = $this->getOceane->getPilotGroup();
                $actif = $this->getOceane->getActifGroup();
                $posteAssocie = $this->getOceane->getPosteAssocie();
                //ID_CREATEUR
                $cuid = $this->getOceane->getPartyId();
                //status closed or open .. STATUS
                $status = $this->getOceane->getStatus();
                //PRIORITE_INITIAL
                $priority = $this->getOceane->getPriority();
                //DT_DEBUT_ALARME_IADR
                $troubleDetectionDate = $this->getOceane->getDetectionDate('Y-m-d\TH:i:s');

                //TYPE_RESSOURCE_IADR
                $typeRessourceIadr = $this->getOceane->getTicketCharacteristics(3);
                //CODE_DETECTEUR_IADR
                $codeDetecteur = $this->getOceane->getTicketCharacteristics(5);
                //RESSOURCE_IADR controle a verifier
                $ressource = $this->getOceane->getTicketCharacteristics(4);
                $libelleTechnique = StringTools::convertEncoding($this->getOceane->getTicketCharacteristics(6), 'ISO-8859-15', 'UTF-8');

                //TYPE_RESSOURCE
                $typeRessource = $this->getOceane->getRessourceType();
                //DESCRIPTION
                $description = $this->getOceane->getDescription();
                //LIBELLE_SUCCINCT
                $lbSuccint = $this->getOceane->getLibelleSuccinct();
                //CAUSE_DEPASSEMENT_DELAI
                $causeDepassementDelai = $this->getOceane->getTicketCause();
                //EVT_INCIDENT 1/64
                $evtIncident = $this->getOceane->getTicketType();
                $typeTicket = $this->getOceane->getTicketType(true)['label'];
                //DESCRIPTION_EVT_INCIDENT
                $descriptionEvtIncident = ($evtIncident == '64') ? 1 : 0;
                //ID_CREATEUR
                $cuidLow = strtolower($cuid);
                $userData = $this->ihmUserRepository->getByLogin($cuidLow);

                if ($userData && is_array($userData) && !key_exists('message', $userData)) {
                    $idUser = $userData['ID_UTILISATEUR'];
                }
                //URL DATA

                //CLASSE

                $classe = $this->getOceane->getOrigin();
                // ID1, ID2, ID3
                $id1 = $this->getOceane->getRessourceIds(1);
                $id2 = $this->getOceane->getRessourceIds(2);
                $id3 = $this->getOceane->getRessourceIds(3);

                //IMPACT
                $impact = $this->getOceane->getInstalledRessourceId();

                $bandeau = $this->apiRepository->getBandeau($eds, $typeRessource);
                $bandeauId = $this->astroRepository->getBandeauId($bandeau);
                //FIN URL DATA
                //FIN DATA INIT

                $data = array(
                    'impact' => $impact,
                    'id3' => $id3,
                    'id2' => $id2,
                    'id1' => $id1,
                    'classe' => $classe,
                    'bandeau' => $bandeau,
                    'bandeau_id' => $bandeauId,
                    'description_evt_incident' => $descriptionEvtIncident,
                    'evt_incident' => $evtIncident,
                    'evt_incident_libelle' => $typeTicket,
                    'cause_depassement_delai' => $causeDepassementDelai,
                    'libelle_succinct' => $lbSuccint,
                    'description' => $description,
                    'type_ressource' => $typeRessource,
                    'libelle_technique' => $libelleTechnique,
                    'ressource' => $ressource, //*
                    'code_detecteur' => $codeDetecteur,//*
                    'type_ressource_iadr' => $typeRessourceIadr,
                    'trouble_detection_date' => $troubleDetectionDate, //*
                    'priority' => $priority,//*
                    'status' => $status,
                    'poste_associe' => $posteAssocie,
                    'eds_actif' => $edsActif,
                    'connected_eds' => $eds,
                    'actif' => $actif,
                    'session_id' => $idUser,
                    'ticketoceaneid' => $ticketId,
                    'eds_pilote' => $edsPilote,
                    'is_hno'=> $hno
                );
                $data['astro_id'] = $this->astroRepository->getAstroIdByTicket($data['ticketoceaneid']);

                $urlArray = array(
                    'ticketid' => $data['ticketoceaneid'],
                    'pilotgroup' => $data['eds_pilote'],
                    'connectedgroup' => $data['connected_eds'],
                    'class' => $data['classe'],
                    'id1' => $data['id1'],
                    'id2' => $data['id2'],
                    'id3' => $data['id3'],
                    'type' => $data['type_ressource'],
                    'impact' => $data['impact'],
                    'typetic' => $data['evt_incident'],
                    'bandeau' => $data['bandeau']
                );
                $this->traceRepository->setTrace($data['astro_id'], "URL", $urlArray, $data['session_id'], $data['ticketoceaneid']);
            } else {
                $message = 'Pas de reponse';
            }
            return (empty($data)) ? array('message' => $message) : $data;

        } catch (\Exception $e) {
            return array(
                'message' => $e->getMessage()
            );
        }
    }

    public function checkTicketType($category, $astroId)
    {
        $listIncident = array(15, 1, 4);
        //incident
        if (in_array($category, $listIncident)) {
            $this->assistantRepository->evtToIncident($astroId, 'incident');
            $value = 'incident';
        } // evenement
        else {
            if ($category == '64') {
                $this->assistantRepository->evtToIncident($astroId, 'événement');
                $value = 'événement';
            } else {
                $value = '';
            }
        }
        return $value;
    }

    public function createTicket($data)
    {
        $idJeuParam = '';
        if ($data['type_ressource'] == 'DSLAM') {
            $ressource = $this->oceaneAssistant->detailMateriel($data['ressource'], $data['type_ressource_iadr'], $data['code_detecteur'], $data['description'], $data['id1']);
            $idRessource = $this->astroRepository->createRessource($ressource);
            $data['id_ressource'] = $idRessource;
        }

        if ($data['evt_incident'] == '64') {
            $idJeuParam = $this->astroRepository->getJeuParamByBandeauFonction($data['bandeau_id'], 'ABONDONNER');
        }
        $data['id_jeu_param'] = $idJeuParam;
        $this->astroRepository->addTicket($data['ticketoceaneid'], $data['status'], $data);
        $astroId = $this->astroRepository->getAstroIdByTicket($data['ticketoceaneid']);

        if ($data['type_ressource'] == 'DSLAM') {
            // Si autre chose qu'un DSLAM, on doit créer la ressource du DSLAM uniquement
            if ($ressource['ID_TYPE_RESSOURCE'] != '1' && $ressource['ID_TYPE_RESSOURCE'] != '9') {
                $inj['ID_TYPE_RESSOURCE'] = '1';
                $inj['DSLAM'] = $ressource['DSLAM'];
                $idRessourceDslam = $this->astroRepository->createRessource($inj);
                $this->astroRepository->updateTicketDslam($astroId, $idRessourceDslam);
            }
        }

        $evtIncLibelle = $this->checkTicketType($data['evt_incident'], $astroId);
        $data['evt_incident_libelle'] = $evtIncLibelle;

        $this->traceRepository->setTrace($astroId, "INIT_API", $data, $data['session_id'], $data['ticketoceaneid']);
        return $astroId;
    }

    public function callEnchainementMethd($enchainement, $idTicket, $connectedGroup, $inputs, $codeDetecteur = null, $idAlarme = null, $typeFonctionnel = null, $typeEquipement = null)
    {
        $result = array();
        $checkIfTAADSL = false;
        $astroId = $this->astroRepository->getAstroIdByTicket($idTicket);
        $message = new Message($this->app, $astroId, $this->messageFile, $this->sessId);
        if ($enchainement == 'TRAITEMENT_ALARME_ADSL') {
            $checkIfTAADSL = true;
            $dataAuto = $this->app->get('AutomatisationRepository')->getCodeAndEnchainementAutomaisation($codeDetecteur);
            $enchainement = $dataAuto['ENCHAINEMENT'];
        }

        switch ($enchainement) {
            case 'TRAITEMENT_ALARME_CARTES_CLIENTS' :
                $this->updateDateActionEnCoursEds($idTicket, $connectedGroup);
                $preRequis = $this->checkPreRequirementEnchainement($idTicket, $enchainement, $connectedGroup);
                if (!$preRequis) {
                    $message->setMessageComplexe("E_AUTOMATE_ENCHAINEMENT", array('###DETAIL###' => "ECHEC AUTOMATE : l'état actuel du ticket ne permet pas le lancement de l'enchaînement"));
                    $preRequirementException = new PreRequirementException();
                    return $preRequirementException();
                }
                $this->automatisationRepository->setFlagEnchainement($idTicket, $enchainement);
                $result = $this->app->get('AutomatisationCarte')->traitementAutomatiseCarte($idTicket, $connectedGroup, $idAlarme, $checkIfTAADSL);
                break;
            case 'TRAITEMENT_ALARME_DSLAM_ISOLE' :
                $this->updateDateActionEnCoursEds($idTicket, $connectedGroup);
                $preRequis = $this->checkPreRequirementEnchainement($idTicket, $enchainement, $connectedGroup);
                if (!$preRequis) {
                    $message->setMessageComplexe("E_AUTOMATE_ENCHAINEMENT", array('###DETAIL###' => "ECHEC AUTOMATE : l'état actuel du ticket ne permet pas le lancement de l'enchaînement"));
                    $preRequirementException = new PreRequirementException();
                    return $preRequirementException();
                }
                $this->automatisationRepository->setFlagEnchainement($idTicket, $enchainement);
                $result = $this->app->get('AutomatisationDslamIsole')->traitementAutomatiseDslamIsole($idTicket, $connectedGroup, $idAlarme, $checkIfTAADSL);
                break;
            case 'TRAITEMENT_ALARME_VENTILATEUR' :
                $this->updateDateActionEnCoursEds($idTicket, $connectedGroup);
                $this->automatisationRepository->setFlagEnchainement($idTicket, $enchainement);
                $result = $this->app->get('AutomatisationVentilateur')->traitementAutomatiseVentilateur($idTicket, $connectedGroup, $idAlarme, $checkIfTAADSL);
                break;
            case 'MISE_A_JOUR_FIN_ALARME' :
                $this->automatisationRepository->setFlagEnchainement($idTicket, $enchainement);
                $result = $this->app->get('UpdateFinAlarme')->updateFinAlarme($idTicket, $connectedGroup, $inputs);
                break;
            case 'TRAITEMENT_ALARME_EVT' :
                $this->updateDateActionEnCoursEds($idTicket, $connectedGroup);
                $preRequis = $this->checkPreRequirementEnchainement($idTicket, $enchainement, $connectedGroup);
                if (!$preRequis) {
                    $message->setMessageComplexe("E_AUTOMATE_ENCHAINEMENT", array('###DETAIL###' => "ECHEC AUTOMATE : l'état actuel du ticket ne permet pas le lancement de l'enchaînement"));
                    $preRequirementException = new PreRequirementException();
                    return $preRequirementException();
                }
                $this->automatisationRepository->setFlagEnchainement($idTicket, $enchainement);
                $result = $this->app->get('AutomatisationEvt')->traitementAutomatiseEvt($idTicket, $connectedGroup, $idAlarme);
                break;
            case 'TRAITEMENT_RENDRE_MAIN_EVT' :
                $this->updateDateActionEnCoursEds($idTicket, $connectedGroup);
                $preRequis = $this->checkPreRequirementEnchainement($idTicket, $enchainement, $connectedGroup);
                if (!$preRequis) {
                    $message->setMessageComplexe("E_AUTOMATE_ENCHAINEMENT", array('###DETAIL###' => "ECHEC AUTOMATE : l'état actuel du ticket ne permet pas le lancement de l'enchaînement"));
                    $preRequirementException = new PreRequirementException();
                    return $preRequirementException();
                }
                $this->automatisationRepository->setFlagEnchainement($idTicket, $enchainement);
                $result = $this->app->get('AutomatisationRendreMainEvt')->traitementAutomatiseRendreMainEvt($idTicket, $connectedGroup, $idAlarme);
                break;
            case 'TRAITEMENT_ALARME_COMMUT' :
                $this->updateDateActionEnCoursEds($idTicket, $connectedGroup);
                $preRequis = $this->checkPreRequirementEnchainement($idTicket, $enchainement, $connectedGroup);
                if (!$preRequis) {
                    $message->setMessageComplexe("E_AUTOMATE_ENCHAINEMENT", array('###DETAIL###' => "ECHEC AUTOMATE : l'état actuel du ticket ne permet pas le lancement de l'enchaînement"));
                    $preRequirementException = new PreRequirementException();
                    return $preRequirementException();
                }
                $this->automatisationRepository->setFlagEnchainement($idTicket, $enchainement);
                $result = $this->app->get('AutomatisationCommut')->traitementAutomatiseCommut($idTicket, $connectedGroup, $idAlarme, $typeFonctionnel , $typeEquipement);
                break;
            default :
                $badRequestException = new BadRequestException('Correspondance enchainement-codeDetecteur non trouvé');
                return $badRequestException();
                break;
        }
        return $result;
    }

    public function callEnchainementCommutMethod($enchainement, $connectedGroup, $idFa, $idTicket)
    {
        $astroId = $this->astroRepository->getAstroIdByTicket($idTicket);
        $message = new Message($this->app, $astroId, $this->messageFile, $this->sessId);
        $this->automatisationRepository->insertFaAndSGTQS($idFa, $idTicket);
        switch ($enchainement) {
            case 'TRAITEMENT_PERMUT_DISQUE_COMMUT' :
                $this->updateDateActionEnCoursEds($idTicket, $connectedGroup);
                $preRequis = $this->checkPreRequirementEnchainement($idTicket, $enchainement, $connectedGroup);
                if (!$preRequis) {
                    $message->setMessageComplexe("E_AUTOMATE_ENCHAINEMENT", array('###DETAIL###' => "ECHEC AUTOMATE : l'état actuel du ticket ne permet pas le lancement de l'enchaînement"));
                    $preRequirementException = new PreRequirementException();
                    return $preRequirementException();
                }
                $this->automatisationRepository->setFlagEnchainement($idTicket, $enchainement);
                $result = $this->app->get('AutomatisationPermutDisqueCommut')->traitementAutomatisePermutDisqueCommut($idFa, $connectedGroup, $idTicket);
                break;
            default :
                $badRequestException = new BadRequestException();
                return $badRequestException();
                break;
        }
        return $result;
    }

    private function checkPreRequirementEnchainement($idTicket, $code, $connectedGroup)
    {
        $dataFg = $this->initApi($idTicket, $connectedGroup);
        if ($code == 'TRAITEMENT_ALARME_CARTES_CLIENTS' || $code == 'TRAITEMENT_ALARME_EVT' || $code == 'TRAITEMENT_RENDRE_MAIN_EVT') {
            return ($dataFg['eds_pilote'] == $connectedGroup && $dataFg['evt_incident'] == '64' && ($dataFg['status'] == 'Open' || $dataFg['status'] == 'InProgress' || $dataFg['status'] == 'OnHold'));
        } else {
            return true;
        }
    }

    public function getUserId()
    {
        $cuidlower = $this->app->config['api_data']['cuid']; //ID HBM
        return $this->app->get('IhmUtilisateurRepository')->getByLogin($cuidlower)['ID_UTILISATEUR'];
    }

    public function updateDateActionEnCoursEds($ticketId, $eds)
    {

        $connexionDataUrl = $this->globalApiUrlService->getUrlApi('CONNEXION');
        $oceaneUpdateUrl = $this->globalApiUrlService->getUrlApi('OCEANE_UPT');

        $troubleTicketUpdate = new OceaneUpd($connexionDataUrl, $oceaneUpdateUrl);
        $oceaneAssistant = new OceaneAssistant($this->app);
        $dateActionEnCoursEds = $oceaneAssistant->changeDateToUTCoceane(date("d/m/Y H:i", strtotime("+30 minutes")));

        $values = array(
            'edsPilote' => $eds,
            'groupActionInProgress' => 'traitement automate',
            'groupActionInProgressDate' => $dateActionEnCoursEds,
            'PartyID' => '',
            'localGroupCode' => ''
        );
        $result = $troubleTicketUpdate->getResponseUpdateDateActionEdsEnchainement($ticketId, $values);
        if (key_exists('faultstring', $result) && $result->faultstring != '' && key_exists('detail', $result)) {
            $updateOceaneException = new UpdateOceaneException();
            return $updateOceaneException();
        }
        return true;
    }

    public function getEDSActif($ticketID)
    {
        $conf = $this->app->config;
        $env = $conf['ENV'];

        $connexionData = $this->globalApiRepository->getDataGlobal('CONNEXION', $env);
        $findandGet = $this->globalApiRepository->getDataGlobal('OCEANE_FG', $env);
        $OceaneFg = new OceaneFg($connexionData, $findandGet);

        $EDSActif = array();
        $result = $OceaneFg->getResponseFindandGetTroubleTicket($ticketID);
        if (isset($result->TroubleTicketResponse->TroubleTicketResponse)) {
            $troubleTicketResponse = $result->TroubleTicketResponse->TroubleTicketResponse;

            $partyRole = $troubleTicketResponse->PartyRole;
            foreach ($partyRole as $key => $value) {
                if ($partyRole[$key]->partyRoleType == "TroubleResolutionContributor" && property_exists($partyRole[$key], 'Local_PartyIntervention')) {
                    if (is_object($partyRole[$key]->Local_PartyIntervention->interventionStatus) && $partyRole[$key]->Local_PartyIntervention->interventionStatus->status == "Accepted") {
                        return $partyRole[$key]->PartyRoleSet->partyRoleSetID;
                    } else if (is_object($partyRole[$key]->Local_PartyIntervention->interventionStatus) && $partyRole[$key]->Local_PartyIntervention->interventionStatus->status == "Requested" && $partyRole[$key]->Local_PartyIntervention->level == '1') {
                        return $partyRole[$key]->PartyRoleSet->partyRoleSetID;
                    } else if (is_array($partyRole[$key]->Local_PartyIntervention->interventionStatus)) {
                        foreach ($partyRole[$key]->Local_PartyIntervention->interventionStatus as $k => $v) {
                            if ($partyRole[$key]->Local_PartyIntervention->interventionStatus[$k]->status == "Requested" && $partyRole[$key]->Local_PartyIntervention->interventionStatus[$k + 1]->status == "Accepted") {
                                return $partyRole[$key]->PartyRoleSet->partyRoleSetID;
                            }
                        }
                    }
                }
            }
        }
        return $EDSActif;
    }

    public function getEDSPilote($ticketID)
    {
        $conf = $this->app->config;
        $env = $conf['ENV'];

        $connexionData = $this->globalApiRepository->getDataGlobal('CONNEXION', $env);
        $findandGet = $this->globalApiRepository->getDataGlobal('OCEANE_FG', $env);
        $OceaneFg = new OceaneFg($connexionData, $findandGet);

        $EDSPilote = array();
        $result = $OceaneFg->getResponseFindandGetTroubleTicket($ticketID);
        if (isset($result->TroubleTicketResponse->TroubleTicketResponse)) {
            $troubleTicketResponse = $result->TroubleTicketResponse->TroubleTicketResponse;

            $partyRole = $troubleTicketResponse->PartyRole;
            foreach ($partyRole as $key => $value) {
                if ($partyRole[$key]->partyRoleType == "TroubleResolutionLeader" && property_exists($partyRole[$key], 'Local_PartyIntervention')) {
                    if (is_object($partyRole[$key]->Local_PartyIntervention->interventionStatus) && $partyRole[$key]->Local_PartyIntervention->interventionStatus->status == "Accepted") {
                        return $partyRole[$key]->PartyRoleSet->partyRoleSetID;
                    } else if (is_array($partyRole[$key]->Local_PartyIntervention->interventionStatus)) {
                        foreach ($partyRole[$key]->Local_PartyIntervention->interventionStatus as $k => $v) {
                            if ($partyRole[$key]->Local_PartyIntervention->interventionStatus[$k]->status == "Requested" && $partyRole[$key]->Local_PartyIntervention->interventionStatus[$k + 1]->status == "Accepted") {
                                return $partyRole[$key]->PartyRoleSet->partyRoleSetID;
                            }
                        }
                    }
                }
            }
        }
        return $EDSPilote;
    }
    public function getTraceScenarioApi($enchainement){
        $traceScenario = array();

        switch ($enchainement) {
            case 'TRAITEMENT_ALARME_ADSL' :
            case 'TRAITEMENT_ALARME_CARTES_CLIENTS' :
                $traceScenario = $this->app->get('AutomatisationCarte')->getTraceScenario();
                break;
            case 'TRAITEMENT_ALARME_EVT' :
                $traceScenario = $this->app->get('AutomatisationEvt')->getTraceScenario();
                break;
            case 'TRAITEMENT_ALARME_DSLAM_ISOLE' :
                $traceScenario = $this->app->get('AutomatisationDslamIsole')->getTraceScenario();
                break;
            case 'TRAITEMENT_ALARME_VENTILATEUR' :
                $traceScenario = $this->app->get('AutomatisationVentilateur')->getTraceScenario();
                break;
            case 'TRAITEMENT_RENDRE_MAIN_EVT' :
                $traceScenario = $this->app->get('AutomatisationRendreMainEvt')->getTraceScenario();
                break;
            case 'TRAITEMENT_PERMUT_DISQUE_COMMUT' :
                $traceScenario = $this->app->get('AutomatisationPermutDisqueCommut')->getTraceScenario();
                break;
            default :

                break;
        }
        return $traceScenario;
    }

    public function verifierScenarioExist($idScenario)
    {
        $scenarioExist = $this->enchainementRepo->verifierScenarioExist($idScenario);
        if($scenarioExist == '0')
        {
            $badRequestException = new BadRequestException('scenarioId does not exist');
            return $badRequestException();
        }else {
            return false;
        }
    }
    public function verifierActivationScenario($idScenario)
    {
        $etatScenario = $this->enchainementRepo->verifierActivationScenario($idScenario);
        if($etatScenario == '0')
        {
            $scenarioDesactiveException = new ScenarioDesactiveException();
            return $scenarioDesactiveException();
        }else {
            return false;
        }
    }
    public function verifierTypeScenario($idScenario, $scenarioType)
    {
        $typeScenario = $this->enchainementRepo->verifierTypeScenario($idScenario);
        if($typeScenario == '0' && $scenarioType == 'parametrable')
        {
            $scenarioTypeException = new BadRequestException("Ce scenarioId n'est pas un scenario parametrable");
            return $scenarioTypeException();
        }elseif($typeScenario == '1' && $scenarioType == 'legacy')
        {
            $scenarioTypeException = new BadRequestException("Ce scenarioId n'est pas un scenario legacy");
            return $scenarioTypeException();
        }else  {
            return false;
        }
    }
}