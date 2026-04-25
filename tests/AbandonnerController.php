<?php

namespace App\Controller;

use Hbm\Globalapi\Service\Rest\ApiOceane;
use App\Form\ConfirmerIncidentTransForm;
use App\Repository\AdeliaRepository;
use App\Repository\AgpGeneriqueRepository;
use App\Repository\AstroIhmSqlRepository;
use App\Repository\AstroLienRepository;
use App\Repository\AstroRepository;
use App\Repository\EdrRepository;

use App\Repository\TraceRepository;
use App\Service\AbandonnerService;
use App\Service\AdeliaService;
use App\Service\AireleService;
use App\Service\AutomatisationService;
use App\Service\ConfirmerService;
use App\Service\OceaneGetService;
use Hbm\Common\Controller\BaseController;
use App\Tools\OceaneAssistant;
use App\Tools\DroitAstroTools;
use App\Form\ConfirmerIncidentGeneriqueForm;
use App\Form\ConfirmerIncidentForm;
use App\Tools\Message;
use Hbm\Common\Tools\StringTools;
use Hbm\Common\Service\LinkService;
use Hbm\Globalapi\Service\Rest\Oceane;
use Hbm\Globalapi\Service\Soap\OceaneFg;
use App\Tools\OceaneTools;

class AbandonnerController extends BaseController
{

    /**
     * @var AstroRepository
     */
    protected $astroRepository;

    /**
     * @var AstroIhmSqlRepository
     */
    protected $astroIhmSqlRepository;

    /**
     * @var AdeliaRepository
     */
    protected $adeliaRepository;

    /**
     * @var AstroLienRepository
     */
    protected $astroLienRepository;

    /**
     * @var TraceRepository
     */
    protected $traceRepository;

    /**
     * @var AdeliaService
     */
    protected $adeliaService;

    /**
     * @var ConfirmerService
     */
    protected $confirmerService;

    /**
     * @var EdrRepository
     */
    protected $edrRepository;

    /**
     * @var AutomatisationService
     */
    protected $automatisationRepo;

    /**
     * @var AbandonnerService
     */
    protected $abandonnerService;

    protected $astroId;

    protected $loginId;

    protected $sessId;

    protected $lienAdeliaExt;

    protected $analyseService;

    protected $portailInfoService;
    /**
     * @var OceaneGetService
     */
    protected $getOceane;

    /**
     *
     * @var AireleService
     */
    protected $airelle;
    /**
     * @var AgpGeneriqueRepository
     */
    protected $agpGeneriqueRepository;

    /**
     * @var GlobalApiService
     */
    protected $globalApiService;

    protected $messageFile;

    public function init()
    {
        parent::init();

        $this->astroRepository = $this->app->get('AstroRepository');
        $this->astroIhmSqlRepository = $this->app->get('AstroIhmSqlRepository');
        $this->verrouRepository = $this->app->get('VerrouRepository');
        $this->adeliaRepository = $this->app->get('AdeliaRepository');
        $this->astroLienRepository = $this->app->get('AstroLienRepository');
        $this->traceRepository = $this->app->get('TraceRepository');
        $this->automatisationRepo = $this->app->get('AutomatisationRepository');
        $this->edrRepository = $this->app->get('EdrRepository');

        $this->adeliaService = $this->app->get('Adelia');
        $this->confirmerService = $this->app->get('Confirmer');
        $this->abandonnerService = $this->app->get('Abandonner');
        $this->linkCommonService = new LinkService($this->app);
        $this->analyseService = $this->app->get('AnalyseImpact');
        $this->portailInfoService = $this->app->get('PortailInfo');
        $this->canariService = $this->app->get('Canari');

        $this->instance = $this->app->config['ENV'];
        $this->lienAdeliaExt = $this->linkCommonService->getGlobalLink('ADELIA', $this->instance);
        $this->loginId = $this->app->get('Session')->getUtilisateurLogin();
        $this->sessId = $this->app->get('Session')->getUtilisateurId();

        $this->getOceane = $this->app->get('OceaneGet');
        $this->airelle = $this->app->get('Airele');
        $this->agpGeneriqueRepository = $this->app->get('AgpGeneriqueRepository');
        $this->messageFile = $this->app->config['message_file'];
        $this->globalApiService = $this->app->get('GlobalApiUrlService');

    }

    public function abandonnerIncidentAction()
    {
        $this->setRenderLayout(false);
        $data = $this->request->getFromQuery();
        $astroId = $this->request->getFromPost("astroid");
        $idJeuParam = $this->astroRepository->getJeuParamByBandeauFonction($data['id_bandeau'], 'ABONDONNER');
        $causeAbandon = $this->astroIhmSqlRepository->getListeCauseAbandon($idJeuParam);
        $defaultCause = array();
        $defaultCause[0] = array(
            'LIBELLE' => '* Choisir *',
            'ORDRE' => ''
        );
        $causeAbandon = array_merge($defaultCause, $causeAbandon);
        array_push($causeAbandon, array(
            'LIBELLE' => 'AUTRE',
            'ORDRE' => ''
        ));

        return array(
            'cause_abandon' => $causeAbandon,
            'astroId' => $astroId
        );
    }

    public function checkIncidentAction()
    {
        $this->disableRendering();
        $data = $this->request->getFromPost();
        $astroid = $data['astroId'];
        $ticket = $this->astroRepository->getTicket($astroid);
        $ticket = $ticket[0];
        $this->send($ticket['EVT_INCIDENT']);
    }

    public function qualifierInformerClientsAction()
    {
        $this->setRenderLayout(false);

        $arrayPrioriteTrans = false;
        $error = false;
        $isShown = false;
        $afficherDec = true;
        $decStat = false;
        $decDone = false;

        $ticketId = $this->request->getFromQuery('ticketid');
        $dataPost = $this->request->getFromPost();

        if (key_exists('error', $dataPost)) {
            $error = true;
        }

        $droitTools = new DroitAstroTools($this->app);
        $gtr = false;

        if (!$droitTools->isIncident($ticketId)) {

            $astroSession = $this->app->get('Session')->get('astroOft' . $ticketId);
            $astroId = $astroSession['astroid'];
            $type = $astroSession['type'];

            $idBandeau = $this->astroRepository->getBandeauId($astroSession['bandeau']);
            $fonctions = $droitTools->getDroitFonction($idBandeau);
            $droitEds = $droitTools->droitEds($ticketId, $astroSession['connectedgroup'], $astroSession['pilotgroup']);
            $codeDetecteur = key_exists('code_detecteur', $astroSession) ? $astroSession['code_detecteur'] : '';

            if ($type == "IPCONV" || $type == "CABLE" || $type == "TRCCABLE" || $type == 'TRONCABLE' || $type == 'SDH' || $type == 'SLN' || $type == 'WDM_SID' || $type == 'MIE' || $type == 'OCH' || $type == 'ETH' || $type == 'PDH') {

                if ($error) {
                    $arrayPrioriteTrans = array(
                        'service_interrompu' => '-',
                        'service_degrade' => '-',
                        'sans_perturbation_service' => '-'
                    );
                } else {
                    $isShown = true;
                    $returnPreconisationTrans = $this->abandonnerService->preconisationPrioriteTrans($ticketId, $idBandeau, $type);
                    $arrayPrioriteTrans = $returnPreconisationTrans['array_priorite_trans'];
                    $decStat = $returnPreconisationTrans['dec_state'];
                    $decDone = $returnPreconisationTrans['dec_done'];
                }
                $informerClient = $this->abandonnerService->informerClient($astroId, $this->loginId);

                $prioClasite = '-';
                $maestroValide = 0;
                $detecteurArray = array();
                $priorite = '-';
                $impactPreconise = '-';
            } else {
                if ($type == 'DSLAM') {
                    $presenceGtr = $this->app->get('Airele')->getImpactByAireleDSLAM($astroSession['id1']);
                    $gtr = in_array('GTRS1', $presenceGtr) || in_array('GTRS2', $presenceGtr);
                }
                $informerClient = $this->abandonnerService->informerClient($astroId, $this->loginId);

                if ($informerClient['label'] == 'Sans perturbation') {
                    $priorite = 'P3';
                    $impactPreconise = $informerClient['label'];
                } elseif ($gtr && strtolower($informerClient['label']) == "coupure franche") {
                    $priorite = 'P1';
                    $impactPreconise = 'Service interrompu';
                } else {
                    $priorite = (in_array('TICKET_ADELIA', $fonctions)) ? $informerClient['priorite'] : $this->astroRepository->getLibPriorite($astroSession['priority']);
                    $impactPreconise = $informerClient['label'];
                }

                $this->getOceane->getOceaneData($ticketId, $this->loginId);
                $clasite = $this->getOceane->getTicketParamsAttribute('Parameter', 'CLASITE');
                $prioClasite = ($type == 'S-SUP') ? $this->astroRepository->getPrioByCalsite($clasite) : '-';
                $dataAdelia = $this->adeliaRepository->getDataBlob($astroId);
                $maestroValide = (strlen($dataAdelia['BLOBDATA']) > 0) ? 1 : 0;
                $detecteurArray = $this->automatisationRepo->getDetecteurList();
            }

            return array(
                'ticketid' => $ticketId,
                'astroId' => $astroId,
                'is_locked' => $informerClient['is_locked'],
                'message_verrou' => $informerClient['message_verou'],
                'priorite_preconise' => ($prioClasite == '-') ? $priorite : $prioClasite,
                'impact_preconise' => $impactPreconise,
                'astroId' => $astroId,
                'maestroValide' => $maestroValide,
                'actif_adelia' => (in_array('TICKET_ADELIA', $fonctions)) ? 1 : 0,
                'actif_abandonner' => (in_array('ABONDONNER', $fonctions)) ? 1 : 0,
                'actif_eds' => $droitEds['droit_actif'],
                'guest_eds' => $droitEds['guest'],
                'fonctions' => $fonctions,
                'code_detecteur' => $codeDetecteur,
                'detecteur_array' => $detecteurArray,
                'impact_prio_array' => $arrayPrioriteTrans,
                'is_shown' => $isShown,
                'afficher_dec' => $afficherDec,
                'dec_done' => $decDone,
                'dec_state' => $decStat
            );
        } else {
            $this->disableRendering();
            $this->send('');
        }
    }


    public function preconisationImpactPrioriteAdslAction($idTicket = null)
    {
        $this->setRenderLayout(false);

        $ticketId = $this->request->getFromQuery('ticketid');

        if ($ticketId == null) {
            $ticketId = $idTicket;
        }
        $droitTools = new DroitAstroTools($this->app);
        $isClientEntreprise = false;
        $isNetVpnAdelia = 0;
        $prestations = '';
        $isNetVpnFinal = '';

        if (!$droitTools->isIncident($ticketId)) {

            $astroSession = $this->app->get('Session')->get('astroOft' . $ticketId);
            $astroId = $astroSession['astroid'];
            $type = $astroSession['type'];
            $idBandeau = $this->astroRepository->getBandeauId($astroSession['bandeau']);

            $fonctions = $droitTools->getDroitFonction($idBandeau);
            $droitEds = $droitTools->droitEds($ticketId, $astroSession['connectedgroup'], $astroSession['pilotgroup']);
            $codeDetecteur = key_exists('code_detecteur', $astroSession) ? $astroSession['code_detecteur'] : '';

            $informerClient = $this->abandonnerService->informerClient($astroId, $this->loginId);

            $adelia = $this->adeliaService->getData($astroId);
            $nombreClientEntreprise = (is_array($adelia) && key_exists('CLIENTS_ENTREPRISE', $adelia)) ? $adelia['CLIENTS_ENTREPRISE'] : '';
            $totalClients = (is_array($adelia) && key_exists('TOTAL_CLIENTS', $adelia)) ? intval($adelia['TOTAL_CLIENTS']) : 0;
            if ($nombreClientEntreprise == 'oui' || intval($nombreClientEntreprise) > 0) {
                $isClientEntreprise = true;
            }
            $oceaneAssistant = new OceaneAssistant($this->app);
            $idJeuParam = $this->astroRepository->getJeuParamByBandeauFonction($idBandeau, 'CONFIRMER_GENERIQUE');

            $isNetVpn = $this->astroRepository->checkNetVpn($idJeuParam);

            if (is_array($adelia) && key_exists('PRESTATIONS', $adelia)) {
                $prestations = key_exists('PRESTATIONS', $adelia) ? json_decode($adelia['PRESTATIONS'], true) : '';
            }

            if (!empty($adelia) && !empty($prestations) && $prestations != '' && key_exists('NETVPN', $prestations) && $prestations['NETVPN'] > 0) {
                $isNetVpnAdelia = 1;
            }
            if ($isNetVpn == '1' && $isNetVpnAdelia == 1) {
                $isNetVpnFinal = '1';
            }

            $arrMatricePrio = $oceaneAssistant->getMatricePrioGenerique($idJeuParam, $totalClients, 'TYPE1', $isClientEntreprise, false, $isNetVpnFinal);

            $idValeurImpactPreconise = $this->astroIhmSqlRepository->getIdValeurConfirmerIncidentByChampAndLibelle($idJeuParam, 'NATURE_IMPACT_CLIENT', $informerClient['libelle_impact_client']);

            $presenceGtr = $this->app->get('Airele')->getImpactByAireleDSLAM($astroSession['id1']);
            $gtr = in_array('GTRS1', $presenceGtr) || in_array('GTRS2', $presenceGtr);

            if ($informerClient['label'] == 'Sans perturbation') {
                $priorite = 'P3';
                $impactPreconise = $informerClient['label'];
            } elseif ($gtr && strtolower($informerClient['label']) == "coupure franche") {
                $priorite = 'P1';
                $impactPreconise = 'Service interrompu';
            } else {
                if ($informerClient['priorite'] == '-') {
                    $priorite = (in_array('PRECONISATION_PRIORITE_ADSL', $fonctions)) ? $informerClient['priorite'] : $this->astroRepository->getLibPriorite($astroSession['priority']);
                } else {
                    $priorite = (in_array('PRECONISATION_PRIORITE_ADSL', $fonctions)) ? 'P' . $arrMatricePrio[$idValeurImpactPreconise] : $this->astroRepository->getLibPriorite($astroSession['priority']);
                }
                $impactPreconise = $informerClient['label'];
            }

            $this->getOceane->getOceaneData($ticketId, $this->loginId);
            $clasite = $this->getOceane->getTicketParamsAttribute('Parameter', 'CLASITE');

            $prioClasite = ($type == 'S-SUP') ? $this->astroRepository->getPrioByCalsite($clasite) : '-';
            $dataAdelia = $this->adeliaRepository->getDataBlob($astroId);
            $maestroValide = (strlen($dataAdelia['BLOBDATA']) > 0) ? 1 : 0;
            $detecteurArray = $this->automatisationRepo->getDetecteurList();

            return array(
                'ticketid' => $ticketId,
                'astroId' => $astroId,
                'is_locked' => $informerClient['is_locked'],
                'message_verrou' => $informerClient['message_verou'],
                'priorite_preconise' => ($prioClasite == '-') ? $priorite : $prioClasite,
                'impact_preconise' => $impactPreconise,
                'astroId' => $astroId,
                'maestroValide' => $maestroValide,
                'actif_adelia' => (in_array('TICKET_ADELIA', $fonctions)) ? 1 : 0,
                'preconisation_prio_adsl' => (in_array('PRECONISATION_PRIORITE_ADSL', $fonctions)) ? 1 : 0,
                'actif_abandonner' => (in_array('ABONDONNER', $fonctions)) ? 1 : 0,
                'actif_eds' => $droitEds['droit_actif'],
                'guest_eds' => $droitEds['guest'],
                'fonctions' => $fonctions,
                'code_detecteur' => $codeDetecteur,
                'detecteur_array' => $detecteurArray,
            );
        } else {
            $this->disableRendering();
            $this->send('');
        }
    }

    public function abandonOceaneAction()
    {
        $this->disableRendering();

        $data = $this->request->getFromPost();
        $idBandeau = $data['id_bandeau'];
        $idJeuParam = $this->astroRepository->getJeuParamByBandeauFonction($idBandeau, 'ABONDONNER');
        $typeRessourceProduit = $data['type'];

        $result = $this->abandonnerService->abandonnerProcess($data, $idJeuParam, $typeRessourceProduit, $this->sessId, $this->loginId);

        $this->send($result['message']);
    }

    public function reserverTicketAction()
    {
        $this->setRenderLayout(false);

        $data = $this->request->getFromPost();
        $astroID = $data['astroid'];
        $label = $data['label'];
        $action = $data['action'];
        if ($action == 'delete') {
            $this->verrouRepository->freeVerrou($astroID, $label, $this->sessId);
            $reservationDisplay = $this->abandonnerService->displayReservation($astroID, $label);
        }

        if ($action == 'reserver') {
            if ($this->verrouRepository->isLockedTrue($astroID, $label) == 0) {
                $this->verrouRepository->setVerrou($astroID, $label, $this->app->get('Session')
                    ->getUtilisateurLogin());
            }
            $reservationDisplay = $this->abandonnerService->displayReservation($astroID, $label);
        }

        if ($action == 'prendre') {
            $this->verrouRepository->freeVerrou($astroID, $label, $this->sessId);
            $this->verrouRepository->setVerrou($astroID, $label, $this->app->get('Session')
                ->getUtilisateurLogin());
            $reservationDisplay = $this->abandonnerService->displayReservation($astroID, $label);
        }

        if ($action == 'check') {
            $reservationDisplay = $this->abandonnerService->displayReservation($astroID, $label);
        }

        return array(
            'image_name' => $reservationDisplay['image_name'],
            'label_final' => $reservationDisplay['label_final']
        );
    }

    public function confirmerIncidentAction()
    {
        $this->disableRendering();
        $data = $this->request->getFromPost();

        // Trouver l'identifiant de la consigne en fonction du code détecteur
        if ($data['action'] == 'source_derangement') {
            $connectedGroup = $data['connectedGroup'];
            $sourceDerangement = $this->astroRepository->getSourceDerangement($connectedGroup);
            return $this->sendEncodedToJson($sourceDerangement);
        }
        // 'option' => $option; A verifier
    }

    public function createAdeliaIhmAction()
    {
        $this->setRenderLayout(false);
        $oceaneAssistant = new OceaneAssistant($this->app);
        $data = $this->request->getFromPost();
        $astroId = $data['astroid'];
        $ticketId = $data['ticketid'];
        $astroSession = $this->app->get('Session')->get('astroOft' . $ticketId);
        $impactNature = key_exists('nature_impact_client', $data) ? $data['nature_impact_client'] : '';
        $data['description_derangement'] = StringTools::convertEncoding($data['description_derangement'], 'ISO-8859-15', 'UTF-8');
        $data['type_ressource'] = key_exists('type_ressource', $astroSession) ? $astroSession['type_ressource'] : '';
        $data['date_retablissementUTC'] = $oceaneAssistant->changeDateToUTCoceane($data['date_retablissement']);
        $numeroAdelia = key_exists('numero_adelia', $data) ? $data['numero_adelia'] : '';
        $ticketAdeliaManuel = trim($numeroAdelia);


        if ($data['optionDisplayIncidentC'] == 'sans') { // pas de ticket adelia
            $this->astroRepository->updateTicketConfirmIncident($astroId);
            $meesage = $this->oceaneUpdateAjax($data);
            $result = array(
                'message' => $meesage,
                'type' => 'sans_adelia'
            );
        } else {
            $astroSession['astroConfirmerIncident' . $astroId] = $data;
            $this->app->get('Session')->set('astroOft' . $ticketId, $astroSession);
            $this->astroRepository->updateTicketConfirmIncident($astroId, $ticketAdeliaManuel, $impactNature, 'o');

            if ($ticketAdeliaManuel == '') {
                $data['dslam'] = $astroSession['id1'];
                $data['sessId'] = $this->sessId;
                $result = $this->app->get('Confirmer')->confirmerIncident($data);
                $result['type'] = 'adelia_auto';
            } else {
                $meesage = $this->oceaneUpdateAjax($data);
                $result = array(
                    'message' => $meesage,
                    'type' => 'adelia_manuelle',
                    'ticket_adelia' => $ticketAdeliaManuel
                );
            }
        }

        return $result;
    }

    public function oceaneUpdateAjax($dataConfirmer, $generique = false)
    {
        $astroId = $dataConfirmer['astroid'];
        $dataAstro = $this->astroRepository->getTicket($astroId);
        $dataAstro = $dataAstro[0];
        $ticketId = $dataAstro['TICKETOCEANEID'];

        $astroSession = $this->app->get('Session')->get('astroOft' . $ticketId);

        $astroSession['astroConfirmerIncident' . $astroId] = array();
        $this->app->get('Session')->set('astroOft' . $astroId, $astroSession);
        $dataConfirmer['description_derangement'] = StringTools::convertEncoding($dataConfirmer['description_derangement'], 'ISO-8859-15', 'UTF-8');
        $result = $this->app->get('OceaneService')->updateOceaneConfirmer($dataConfirmer, $ticketId, $astroId, $generique);

        $ticket = $this->astroRepository->getTicket($astroId);
        $ticket = $ticket[0];

        $message = '';
        // gestion des messages d'erreur
        $messageFileName = $this->app->config['message_file'];
        $messageFile = DATA_DIR . '/' . $messageFileName;
        $errorMessage = new Message($this->app, $astroId, $messageFile);

        // if (property_exists($result, 'faultstring') && $result->faultstring != '') {
        $result = json_decode($result);
        if (property_exists($result, 'code') && $result->message != '') {
            $error = $result->message . '  ' . $result->description . '   ' . $result->infoURL;
            if ($ticket['ADELIA_MANUEL'] == 'o') {
                $errorOceane = $errorMessage->setMessage("E_CONFIRM_ADELIA_MANUEL_OCEANE", $error);
            } else {
                $errorOceane = $errorMessage->setMessage("E_CONFIRM_SANS_ADELIA_OCEANE", $error);
            }
            $message .= $errorOceane;
        } else {
            if ($ticket['ADELIA_MANUEL'] == 'o') {
                $messageOceane = $errorMessage->setMessage("CONFIRM_ADELIA_MANUEL_OK", '');
            } else {
                if (isset($dataConfirmer['hidden_type_confirmation']) && $dataConfirmer['hidden_type_confirmation'] == 'TYPE2') {
                    $messageOceane = $errorMessage->setMessage("CONFIRM_OK", '');
                } else {
                    $messageOceane = $errorMessage->setMessage("CONFIRM_SANS_ADELIA_OK", '');
                }
            }

            $message .= $messageOceane;
        }
        $this->traceRepository->setTrace($astroId, "OCEANE", $result, $this->sessId, $ticketId);
        return $message;
    }


    public function oceaneUpdateAjaxTrans($dataConfirmer)
    {
        $arrayMessage = array();
        $astroId = $dataConfirmer['astroid'];
        $dataAstro = $this->astroRepository->getTicket($astroId);
        $dataAstro = $dataAstro[0];
        $ticketId = $dataAstro['TICKETOCEANEID'];

        $astroSession = $this->app->get('Session')->get('astroOft' . $ticketId);

        $astroSession['astroConfirmerIncident' . $astroId] = array();
        $this->app->get('Session')->set('astroOft' . $astroId, $astroSession);
        $result = $this->app->get('OceaneService')->updateOceaneConfirmerTrans($dataConfirmer, $ticketId, $astroId);

        $message = '';
        // gestion des messages d'erreur
        $messageFileName = $this->app->config['message_file'];
        $messageFile = DATA_DIR . '/' . $messageFileName;
        $errorMessage = new Message($this->app, $astroId, $messageFile);

        if (key_exists('code', $result)) {
            $messageOceane = $errorMessage->setMessageComplexe("E_CONFIRM_TRANS_OCEANE", array("###DETAIL###" => $result['message']));
            $message .= $messageOceane;
            $arrayMessage['etat'] = 'ko';
            $arrayMessage['message'] = nl2br($message);
            $seuils['grave'] = '-';
            $seuils['majeur'] = '-';
            $seuils['grave_is_sup'] = false;
            $seuils['majeur_is_sup'] = false;
            $arrayMessage['seuils'] = $seuils;
            $arrayMessage['commentaire'] = '';
        } else {
            $messageOceane = $errorMessage->setMessage("CONFIRM_TRANS_OK", '');
            $message .= $messageOceane;
            $commentaireConfirmTrans = $this->analyseService->createCommentaireConfirmerTrans($ticketId, $dataConfirmer);

            $resultCom = $this->app->get('OceaneService')->ajoutCommentaireConfirmerTrans($commentaireConfirmTrans['commentaire'], $ticketId, $astroId);
            if (key_exists('code', $resultCom)) {
                $messageOceaneCom = $errorMessage->setMessageComplexe("E_AJOUT_COMMENTAIRE_OCEANE", array("###DETAIL###" => $resultCom['message']));
                $message .= "\n \n" . $messageOceaneCom;
            }
            $arrayMessage['etat'] = 'ok';
            $arrayMessage['message'] = nl2br($message);
            $arrayMessage['seuils'] = $commentaireConfirmTrans['seuils'];
            $arrayMessage['commentaire'] = $commentaireConfirmTrans['commentaire_portail'];

            $astroSession = $this->app->get('Session')->get('astroOft' . $ticketId);
            $connectedGroup = key_exists('connectedgroup',$astroSession) ? $astroSession['connectedgroup'] : '';

            $loginUser = (key_exists('api', $this->app->config) && $this->app->config['api']) ? $this->app->get('AstroRepository')->getCompteMachine($connectedGroup) : strtoupper($this->app->get('Session')->getUtilisateurLogin());

            $result['login_user'] = $loginUser;
            // creation ticket impacté
            $paramsTicketImpacte = $this->astroRepository->getValuesParamConfirmTrans($dataConfirmer['id_jeu_param'], $dataConfirmer['hidden_type_ressource'], 'CREATE_TICKETS_IMPACTES');
            if (is_array($paramsTicketImpacte) && key_exists('IS_CHECKED', $paramsTicketImpacte) && $paramsTicketImpacte['IS_CHECKED'] == '1') {
                $result['api'] = 0;
                $result['type'] = $astroSession['type'];
                $this->confirmerService->createTicketImpacte($result);
            }

        }
        return $arrayMessage;
    }

    public function adeliaFailIhmAction()
    {
        $this->setRenderLayout(false);
        $data = $this->request->getFromPost();
        $astroId = $data['astroid'];
        // gestion des messages d'erreur
        $messageFileName = $this->app->config['message_file'];
        $messageFile = DATA_DIR . '/' . $messageFileName;
        $errorMessage = new Message($this->app, $astroId, $messageFile);
        return array(
            'message_erreur' => $errorMessage->getMessageJournal("E_CONFIRM_ADELIA_AUTO_ADELIA"),
            'message' => '',
            'description' => ''
        );
    }

    public function confirmerBaseAction()
    {
        $this->disableRendering();

        $ticketId = $this->request->getFromPost('ticketId', '');
        $astroId = $this->request->getFromPost('astroId', '');
        $loginUser = $this->app->get('Session')->getUtilisateurLogin();
        $valeurs = array(
            'partyRolePartyID' => $loginUser
        );

        $abandonService = $this->app->get('Abandonner');
        $data = $abandonService->confirmerBase($ticketId, $astroId, $valeurs);
        return $this->sendEncodedToJson($data);
    }

    public function confirmerIncidentIhmAction()
    {
        $oceaneAssistant = new OceaneAssistant($this->app);
        $data = $this->request->getFromQuery();
        $astroid = $data['astroId'];
        $nbClientsTdsl = '';
        $dataAdelia = $this->adeliaRepository->getDataBlob($astroid);

        $adeliaPrestations = json_decode($dataAdelia['PRESTATIONS']);
        $this->verrouRepository->freeVerrou($astroid, 'test');

        $dataAstro = $this->astroRepository->getTicket($astroid);
        $dataAstro = $dataAstro[0];
        $ticketId = $dataAstro['TICKETOCEANEID'];
        $astroSession = $this->app->get('Session')->get('astroOft' . $ticketId);
        $idRessource = $astroSession['id_ressource'];
        $ressourceAdelia = ucfirst($oceaneAssistant->afficheDetailMaterielAccueil($idRessource)); // Carte DSLAM DSVEN306 / C10 /

        $option = key_exists('option', $data) ? $data['option'] : '';

        $confirmerIncidentForm = new ConfirmerIncidentForm(null, array(
            'app' => $this->app,
            'astroid' => $astroid,
            'option' => $option
        ));

        $troubleDetectionDate = $oceaneAssistant->changeUTCToDate($dataAstro['DT_DEBUT_ALARME_IADR']);

        $commentaireImpactClientTemplate = $this->abandonnerService->getCommentaireImpactClientTemplate($dataAstro);

        $arrMatricePrio = $oceaneAssistant->getMatricePrio();
        $arrValeurSeuil = $oceaneAssistant->getValeurSeuil();
        if (!empty($adeliaPrestations) && property_exists($adeliaPrestations, 'TDSL')) {
            $nbClientsTdsl = (!is_null($adeliaPrestations)) ? (intval($adeliaPrestations->TDSL)) : '';
        }
        $nbClientsTotal = $dataAdelia ? intval($dataAdelia['TOTAL_CLIENTS']) : '';

        $arrDureeRetablissement = $oceaneAssistant->getDureeRetab();

        $tabHoraireAdeliaManuel = $oceaneAssistant->changeUTCToDateDetail($dataAstro['DT_DEBUT_ALARME_IADR']);
        $adeliaManuelDate = $tabHoraireAdeliaManuel['date'];
        $adeliaManuelHeure = $tabHoraireAdeliaManuel['heure'];
        $adeliaManuelMinute = $tabHoraireAdeliaManuel['minute'];

        $ressource = $this->astroIhmSqlRepository->getRessourceComplete($astroid);

        $typeEquipement = $ressource['LB_URL_ADELIA'];
        $nomEquipement = $ressource['DSLAM'];
        $numeroBaie = $ressource['CHASSIS'];

        $numeroChassis = $ressource['CHASSIS'];
        $numeroCarte = $ressource['CARTE'];
        $numeroPort = $ressource['PORT'];
        $nomDslam = $ressource['DSLAM'];

        $edr = $this->edrRepository->getDataDslam($astroid);

        $nomRouteurA = $edr['ROUTER_A'];
        $nomRouteurN = $edr['ROUTER_N'];
        $numeroVp = $edr['VP'];
        $codeVlan = $edr['VLAN'];

        return array(
            'ticket_id' => $ticketId,
            'astro_id' => $astroid,
            'ressource_adelia' => $ressourceAdelia,
            'trouble_detection_date' => $troubleDetectionDate,
            'commentaire_impact_client_template' => $commentaireImpactClientTemplate,
            'arr_matrice_prio' => $arrMatricePrio,
            'arr_valeur_seuil' => $arrValeurSeuil,
            'nb_clients_tdsl' => $nbClientsTdsl,
            'nb_clients_total' => $nbClientsTotal,
            'arr_duree_retablissement' => $arrDureeRetablissement,
            'option' => $option,
            'adelia_manuel_date' => $adeliaManuelDate,
            'adelia_manuel_heure' => $adeliaManuelHeure,
            'adelia_manuel_minute' => $adeliaManuelMinute,
            'type_equipement' => $typeEquipement,
            'nom_equipement' => $nomEquipement,
            'numero_baie' => $numeroBaie,
            'numero_chassis' => $numeroChassis,
            'numero_carte' => $numeroCarte,
            'numero_port' => $numeroPort,
            'nom_dslam' => $nomDslam,
            'nom_routeur_a' => $nomRouteurA,
            'nom_routeur_n' => $nomRouteurN,
            'numero_vp' => $numeroVp,
            'code_vlan' => $codeVlan,
            'connected_group' => $astroSession['connectedgroup'],
            'lien_adelia_ext' => $this->lienAdeliaExt,
            'form' => $confirmerIncidentForm
        );
    }

    public function confirmerIncidentGeneriqueIhmAction()
    {
        $oceaneAssistant = new OceaneAssistant($this->app);
        $data = $this->request->getFromQuery();
        $astroid = $data['astroId'];
        $preconisationActive = '';
        $ressourceAdelia = '';
        $nbClientsTdsl = '';
        $prioritePreconise = '';
        $isClientEntreprise = false;
        $this->verrouRepository->freeVerrou($astroid, 'test');
        $ressourceValuesType1 = array('DSLAM', 'UNIRACC', 'CONNUM', 'COMMUT');
        $champComp6 = null;
        $chmpcmp6AdminValue = '';
        $forcedSans = false;
        $isNetVpnAdelia = 0;
        $isNetVpnFinal = '';

        $dataAstro = $this->astroRepository->getTicket($astroid);
        $dataAstro = $dataAstro[0];
        $ticketId = $dataAstro['TICKETOCEANEID'];
        $dataAdelia = $this->adeliaRepository->getDataBlob($astroid);
        $adeliaPrestations = json_decode($dataAdelia['PRESTATIONS']);
        $astroSession = $this->app->get('Session')->get('astroOft' . $ticketId);
        $idRessource = $astroSession['id_ressource'];
        $typeRessource = $astroSession['type'];
        $idBandeau = $this->astroRepository->getBandeauId($astroSession['bandeau']);
        $droitTools = new DroitAstroTools($this->app);
        $fonctions = $droitTools->getDroitFonction($idBandeau);
        $idFonction = $this->astroRepository->getFonctionId('CONFIRMER_GENERIQUE');
        $regles = $this->astroRepository->getChampsRegle($idBandeau . '_' . $idFonction);
        $regles = $this->formatRegle($regles);
        $idJeuParam = $this->astroRepository->getJeuParamByBandeauFonction($idBandeau, 'CONFIRMER_GENERIQUE');
        $priorite = $this->astroLienRepository->getPrioriteLibelle();

        //HO HNO

        //start
        $today = new \DateTime();
        $valToday = $today->format("d/m/Y H:i");

        $periodeHno = false;
        $holidayDates = $this->astroRepository->recupererJoursFerie();
        $weekdaysNamesArray = array('Saturday', 'Sunday');

        $date = \DateTime::createFromFormat('d/m/Y H:i', $valToday);
        $timezone = 'Europe/Paris';
        $temp = strtotime($date->format('m/d/Y H:i') . ' ' . $timezone);
        $dayName = date("l", $temp);
        $day = date('d/m/y', $temp);
        $heureCourante = date("H:i", $temp);

        if (in_array($day, $holidayDates) || in_array($dayName, $weekdaysNamesArray)) {
            $periodeHnoToday = true;
        } elseif (!in_array($dayName, $weekdaysNamesArray)) {
            $periodeHnoToday = $this->confirmerService->checkBetweenTwoTimes($heureCourante, '17:30', '24:00');
            $periodeHnoTomorrow = $this->confirmerService->checkBetweenTwoTimes($heureCourante, '00:00', '08:00');
        }

        if ($periodeHnoToday || $periodeHnoTomorrow) {
            $periodeHno = true;
        }
        //end

        $isNetVpn = $this->astroRepository->checkNetVpn($idJeuParam, $periodeHno);

        if (!empty($adeliaPrestations) && property_exists($adeliaPrestations, 'NETVPN') && intval($adeliaPrestations->NETVPN) > 0) {
            $isNetVpnAdelia = 1;
        }

        if ($isNetVpn == '1' && $isNetVpnAdelia == 1) {
            $isNetVpnFinal = '1';
        }

        if (in_array('TICKET_ADELIA', $fonctions) || in_array('PRECONISATION_PRIORITE', $fonctions)) {
            $preconisationImpact = $this->app->get('Abandonner')->preconisationImpactPrioriteAdsl($ticketId, $this->loginId);
            $prioritePreconise = $preconisationImpact['priorite_preconise'];
        }

        if (in_array('TICKET_ADELIA', $fonctions) || in_array('PRECONISATION_PRIORITE_ADSL', $fonctions)) {
            $preconisationActive = true;
        }

        $option = key_exists('option', $data) ? $data['option'] : '';
        $descriptionValue = $this->astroRepository->getDescriptionTicket($ticketId, 'DESCRIPTION_ALARME');

        $confirmationType = in_array($typeRessource, $ressourceValuesType1) ? 'TYPE1' : 'TYPE2';

        $troubleDetectionDate = $oceaneAssistant->changeUTCToDate($dataAstro['DT_DEBUT_ALARME_IADR']);

        $prioriteCommentaire = $this->astroIhmSqlRepository->getPrioriteCommentaire();
        $commentaireImpactClientTemplate = $this->abandonnerService->getCommentaireImpactClientTemplate($dataAstro);

        if (!empty($adeliaPrestations) && property_exists($adeliaPrestations, 'TDSL')) {
            $nbClientsTdsl = (!is_null($adeliaPrestations)) ? (intval($adeliaPrestations->TDSL)) : '';
        }
        $nombreClientEntreprise = (is_array($dataAdelia) && key_exists('CLIENTS_ENTREPRISE', $dataAdelia)) ? $dataAdelia['CLIENTS_ENTREPRISE'] : '';
        if ($nombreClientEntreprise == 'oui' || intval($nombreClientEntreprise) > 0) {
            $isClientEntreprise = true;
        }
        $nbClientsTotal = $dataAdelia ? intval($dataAdelia['TOTAL_CLIENTS']) : '';

        $arrMatricePrio = $oceaneAssistant->getMatricePrioGenerique($idJeuParam, $nbClientsTotal, $confirmationType, $isClientEntreprise, false, $isNetVpnFinal, $periodeHno);

        $arrValeurSeuil = $oceaneAssistant->getValeurSeuil();

        $this->getOceane->getOceaneData($ticketId, $this->loginId);
        $champComp6 = StringTools::convertEncoding($this->getOceane->getTicketCharacteristics(6), 'ISO-8859-15', 'UTF-8');

        $arrDureeRetabInitial = $this->astroIhmSqlRepository->getConfirmerIncidentListeByChamp($idJeuParam, 'DELAI_RETAB_INITIAL');
        $arrDuree = array();
        foreach ($arrDureeRetabInitial['options'] as $key => $dri) {
            if (!is_null($dri['CONDITION']) && $dri['CONDITION'] !== '' && strpos($champComp6, $dri['CONDITION']) !== false) {
                $arrDureeRetabInitial['options'][$key]['IDENTIFIANT'] = $dri['DELAI'];
                $arrDuree[$arrDureeRetabInitial['options'][$key]['LIBELLE']] = $dri['DELAI'];
            }
            if (!key_exists($arrDureeRetabInitial['options'][$key]['LIBELLE'], $arrDuree)) {
                $arrDuree[$arrDureeRetabInitial['options'][$key]['LIBELLE']] = $dri['IDENTIFIANT'];

            }
        }
        $arrDureeRetablissement = $oceaneAssistant->getDureeRetabInitialGenerique($arrDuree);


        $defaultRadioAdeliaArray = $this->astroIhmSqlRepository->getConfirmerIncidentListeByChamp($idJeuParam, 'CHOIX_ADELIA');
        $valueDefaultRadioAdelia = $defaultRadioAdeliaArray['options'][0]['IDENTIFIANT'];

        $chmpcmp6AdminValue = $defaultRadioAdeliaArray['options'][0]['COMMENTAIRE'];

        if ($typeRessource == 'DSLAM' && $champComp6 != '' && strpos($champComp6, $chmpcmp6AdminValue) !== false) {
            $valueDefaultRadioAdelia = 'sans';
            $forcedSans = true;
        }

        $confirmerIncidentForm = new ConfirmerIncidentGeneriqueForm(null, array(
            'app' => $this->app,
            'astroid' => $astroid,
            'id_jeu' => $idJeuParam,
            'option' => $option,
            'priorite_preconise' => $prioritePreconise,
            'preconisation_active' => $preconisationActive,
            'description_value' => $descriptionValue,
            'connected_group' => $astroSession['connectedgroup'],
            'type_confirmation' => $confirmationType,
            'type_ressource' => $typeRessource,
            'forced_sans_adelia' => $forcedSans
        ));

        $arrTagHno = $oceaneAssistant->getMatriceHnoArray($idJeuParam);

        $tabHoraireAdeliaManuel = $oceaneAssistant->changeUTCToDateDetail($dataAstro['DT_DEBUT_ALARME_IADR']);
        $adeliaManuelDate = $tabHoraireAdeliaManuel['date'];
        $adeliaManuelHeure = $tabHoraireAdeliaManuel['heure'];
        $adeliaManuelMinute = $tabHoraireAdeliaManuel['minute'];

        $ressource = $this->astroIhmSqlRepository->getRessourceComplete($astroid);

        $typeEquipement = $ressource['LB_URL_ADELIA'];
        $nomEquipement = $ressource['DSLAM'];
        $numeroBaie = $ressource['CHASSIS'];

        $numeroChassis = $ressource['CHASSIS'];
        $numeroCarte = $ressource['CARTE'];
        $numeroPort = $ressource['PORT'];
        $nomDslam = $ressource['DSLAM'];

        $edr = $this->edrRepository->getDataDslam($astroid);

        $nomRouteurA = $edr['ROUTER_A'];
        $nomRouteurN = $edr['ROUTER_N'];
        $numeroVp = $edr['VP'];
        $codeVlan = $edr['VLAN'];

        if ($typeRessource == 'DSLAM') {
            $ressourceAdelia = ucfirst($oceaneAssistant->afficheDetailMaterielAccueil($idRessource)); // Carte DSLAM DSVEN306 / C10 /
        } elseif ($typeRessource == 'UNIRACC' || $typeRessource == 'CONNUM' || $typeRessource == 'COMMUT') {
            $ressourceAdelia = $this->adeliaRepository->getRessourceAdelia($astroid);
        }

        //commut ... new data
        $infosEquipements = $this->adeliaService->getEquipementCommut($astroSession['type_ressource'], $ticketId, $astroSession);
        $codeSgtArray = explode(' ', $infosEquipements['code_SGTQSCAA']);
        return array(
            'ticket_id' => $ticketId,
            'astro_id' => $astroid,
            'priorite' => $priorite,
            'priorite_preconise' => $prioritePreconise,
            'priorite_commentaire' => $prioriteCommentaire,
            'arr_duree_retablissement' => $arrDureeRetablissement,
            'option' => $option,
            'connected_group' => $astroSession['connectedgroup'],
            'form' => $confirmerIncidentForm,
            'regles' => $regles,
            'confirmation_type' => $confirmationType,
            'ressource_adelia' => $ressourceAdelia,
            'trouble_detection_date' => $troubleDetectionDate,
            'commentaire_impact_client_template' => $commentaireImpactClientTemplate,
            'arr_matrice_prio' => $arrMatricePrio,
            'arr_matrice_hno' => $arrTagHno,
            'arr_valeur_seuil' => $arrValeurSeuil,
            'nb_clients_tdsl' => $nbClientsTdsl,
            'nb_clients_total' => $nbClientsTotal,
            'adelia_manuel_date' => $adeliaManuelDate,
            'adelia_manuel_heure' => $adeliaManuelHeure,
            'adelia_manuel_minute' => $adeliaManuelMinute,
            'type_equipement' => $typeEquipement,
            'nom_equipement' => $nomEquipement,
            'numero_baie' => $numeroBaie,
            'numero_chassis' => $numeroChassis,
            'numero_carte' => $numeroCarte,
            'numero_port' => $numeroPort,
            'nom_dslam' => $nomDslam,
            'nom_routeur_a' => $nomRouteurA,
            'nom_routeur_n' => $nomRouteurN,
            'numero_vp' => $numeroVp,
            'code_vlan' => $codeVlan,
            'lien_adelia_ext' => $this->lienAdeliaExt,
            'code_SGTQSCAA' => $codeSgtArray[0],
            'ur_number' => str_pad($infosEquipements['ur_number'], 3, 0, STR_PAD_LEFT),
            'ur_chassis_number' => str_pad($infosEquipements['ur_chassis_number'], 3, 0, STR_PAD_LEFT),
            'type_equipement_comm' => $infosEquipements['type_equipement'],
            'value_default_radio_adelia' => $valueDefaultRadioAdelia,
            'is_netvpn' => $isNetVpnFinal
        );
    }

    public function confirmerIncidentTransIhmAction()
    {
        $oceaneAssistant = new OceaneAssistant($this->app);
        $data = $this->request->getFromQuery();
        $astroid = $data['astroId'];
        $this->verrouRepository->freeVerrou($astroid, 'test');
        $champComp6 = null;
        $creationPortailInfo = 'non';

        $dataAstro = $this->astroRepository->getTicket($astroid);
        $dataAstro = $dataAstro[0];

        $ticketId = $dataAstro['TICKETOCEANEID'];
        $astroSession = $this->app->get('Session')->get('astroOft' . $ticketId);
        $typeRessource = $astroSession['type'];
        $idBandeau = $this->astroRepository->getBandeauId($astroSession['bandeau']);
        $idFonction = $this->astroRepository->getFonctionId('CONFIRMER_TRANS');
        $regles = $this->astroRepository->getChampsRegle($idBandeau . '_' . $idFonction);
        $regles = $this->formatRegle($regles);
        $idJeuParam = $this->astroRepository->getJeuParamByBandeauFonction($idBandeau, 'CONFIRMER_TRANS');
        $priorite = $this->astroLienRepository->getPrioriteLibelle();
        $prioritePreconise = $this->app->get('Abandonner')->preconisationPrioriteTrans($ticketId, $idBandeau, $typeRessource);

        $option = key_exists('option', $data) ? $data['option'] : '';
        $descriptionValue = $this->astroRepository->getDescriptionTicket($ticketId, 'DESCRIPTION_ALARME');

        $troubleDetectionDate = $oceaneAssistant->changeUTCToDate($dataAstro['DT_DEBUT_ALARME_IADR']);
        $this->getOceane->getOceaneData($ticketId, $this->loginId);
        $champComp6 = StringTools::convertEncoding($this->getOceane->getTicketCharacteristics(6), 'ISO-8859-15', 'UTF-8');
        $arrDureeRetabInitial = $this->astroIhmSqlRepository->getConfirmerIncidentListeByChamp($idJeuParam, 'DELAI_RETAB_INITIAL');
        $arrDuree = array();
        foreach ($arrDureeRetabInitial['options'] as $key => $dri) {
            if (!is_null($dri['CONDITION']) && $dri['CONDITION'] !== '' && strpos($champComp6, $dri['CONDITION']) !== false) {
                $arrDureeRetabInitial['options'][$key]['IDENTIFIANT'] = $dri['DELAI'];
                $arrDuree[$arrDureeRetabInitial['options'][$key]['LIBELLE']] = $dri['DELAI'];
            }
            if (!key_exists($arrDureeRetabInitial['options'][$key]['LIBELLE'], $arrDuree)) {
                $arrDuree[$arrDureeRetabInitial['options'][$key]['LIBELLE']] = $dri['IDENTIFIANT'];

            }
        }
        $arrDureeRetablissement = $oceaneAssistant->getDureeRetabInitialGenerique($arrDuree);

        $this->getOceane->getOceaneData($ticketId, $this->loginId);
        $fgDate = $this->getOceane->getCreationDate();
        $creationDate = $oceaneAssistant->changeUTCToDate($fgDate);

        $confirmerIncidentForm = new ConfirmerIncidentTransForm(null, array(
            'app' => $this->app,
            'astroid' => $astroid,
            'id_jeu' => $idJeuParam,
            'option' => $option,
            'description_value' => $descriptionValue,
            'connected_group' => $astroSession['connectedgroup'],
            'type_ressource' => $typeRessource,
        ));

        $arrTagHno = $oceaneAssistant->getMatriceHnoArray($idJeuParam);
        $paramsPortailInfo = $this->astroRepository->getValuesParamConfirmTrans($idJeuParam, $typeRessource, 'CREATE_PORTAIL_INFO');
        if (is_array($paramsPortailInfo) && key_exists('IS_CHECKED', $paramsPortailInfo) && $paramsPortailInfo['IS_CHECKED'] == '1') {
            $creationPortailInfo = 'oui';
        }
        $departement = '';
        $commune = '';
        $codeInsee = array();
        if ($typeRessource == "TRONCABLE" || $typeRessource == "CABLE" || $typeRessource == "MIE") {
            $departement = $this->portailInfoService->getDepartementFromIds($astroSession['id1'], $astroSession['id2']);
            $commune = $this->portailInfoService->getCommuneFromIds($astroSession['id1'], $astroSession['id2']);
            $codeInsee = $this->portailInfoService->getCodeInseeFromIds($astroSession['id1'], $astroSession['id2']);
        } elseif ($typeRessource == "SLN" || $typeRessource == "WDM_SID" || $typeRessource == "SDH" || $typeRessource == "PDH") {
            $departement = $this->portailInfoService->getDepartementFromIds($astroSession['id2'], $astroSession['id3']);
            $commune = $this->portailInfoService->getCommuneFromIds($astroSession['id2'], $astroSession['id3']);
            $codeInsee = $this->portailInfoService->getCodeInseeFromIds($astroSession['id2'], $astroSession['id3']);
        }
        return array(
            'ticket_id' => $ticketId,
            'astro_id' => $astroid,
            'priorite' => $priorite,
            'priorite_preconise' => $prioritePreconise['array_priorite_trans'],
            'dec_state' => ($prioritePreconise['dec_state']) ? '1' : '0',
            'arr_duree_retablissement' => $arrDureeRetablissement,
            'option' => $option,
            'connected_group' => $astroSession['connectedgroup'],
            'form' => $confirmerIncidentForm,
            'regles' => $regles,
            'trouble_detection_date' => $troubleDetectionDate,
            'creation_date' => $creationDate,
            'arr_matrice_hno' => $arrTagHno,
            'creation_portail_info_admin' => $creationPortailInfo,
            'departement_from_ids' => $departement,
            'commune_from_ids' => $commune,
            'code_insee' => $codeInsee
        );
    }

    public function simulateManuelAction()
    {
        $this->disableRendering();
        $data = $this->request->getFromPost();
        $astroId = $data['astroid'];
        $adeliaId = $data['adelia_id'];
        $simulateManuel = $this->adeliaService->simulateManuel($adeliaId, $astroId);
        return $this->sendEncodedToJson($simulateManuel);
    }

    public function confirmerIncidentGeneriqueAction()
    {
        $this->setRenderLayout(false);
        $oceaneAssistant = new OceaneAssistant($this->app);
        $data = $this->request->getFromPost();
        $astroId = $data['astroid'];
        $ticketId = $data['ticketid'];
        $adeliaRadio = key_exists('radioAdelia', $data) ? $data['radioAdelia'] : 0;
        if ($adeliaRadio == 1) {
            $data['optionDisplayIncidentC'] = 'sans';
        }

        $astroSession = $this->app->get('Session')->get('astroOft' . $ticketId);
        if ($data['hidden_type_confirmation'] == 'TYPE1') {
            $impactNature = key_exists('nature_impact_client_oceane', $data) ? $data['nature_impact_client_oceane'] : '';
            $impactNatureLibele = key_exists('nature_impact_client_oceane_libelle', $data) ? $data['nature_impact_client_oceane_libelle'] : '';
        } else {
            $impactNature = key_exists('impact_client_oceane', $data) ? $data['impact_client_oceane'] : '';
            $impactNatureLibele = key_exists('impact_client_oceane', $data) ? $data['impact_client_oceane'] : '';
        }

        $data['nature_impact_client'] = $impactNature;
        $data['date_retablissementUTC'] = $oceaneAssistant->changeDateToUTCoceane($data['date_retablissement']);
        $numeroAdelia = key_exists('numero_adelia', $data) ? $data['numero_adelia'] : '';
        $ticketAdeliaManuel = trim($numeroAdelia);

        if ($data['hidden_type_confirmation'] == 'TYPE2') {
            $this->astroRepository->updateTicketConfirmIncident($astroId);
            $meesage = $this->oceaneUpdateAjax($data, true);
            $result = array(
                'message' => $meesage,
                'type' => 'Type_2'
            );
        } else {
            if ($data['optionDisplayIncidentC'] == 'sans') { // pas de ticket adelia
                $this->astroRepository->updateTicketConfirmIncident($astroId);
                $meesage = $this->oceaneUpdateAjax($data, true);
                $result = array(
                    'message' => $meesage,
                    'type' => 'sans_adelia'
                );
            } else {
                $astroSession['astroConfirmerIncident' . $astroId] = $data;
                $this->app->get('Session')->set('astroOft' . $ticketId, $astroSession);
                $this->astroRepository->updateTicketConfirmIncident($astroId, $ticketAdeliaManuel, $impactNatureLibele, 'o');

                if ($ticketAdeliaManuel == '') {

                    $data['dslam'] = $astroSession['id1'];
                    $data['type_ressource'] = $astroSession['type'];
                    $data['connected_group'] = $astroSession['connectedgroup'];
                    $data['sessId'] = $this->sessId;
                    $data['impact_client_libelle'] = StringTools::convertEncoding($impactNatureLibele, 'ISO-8859-15', 'UTF-8');
                    $data['generique'] = true;
                    $result = $this->app->get('Confirmer')->confirmerIncident($data);
                    $result['type'] = 'adelia_auto';
                } else {
                    $meesage = $this->oceaneUpdateAjax($data, true);
                    $result = array(
                        'message' => $meesage,
                        'type' => 'adelia_manuelle',
                        'ticket_adelia' => $ticketAdeliaManuel
                    );
                }
            }
        }

        return $result;
    }

    public function choixDepartementPortailAction()
    {
        $this->disableRendering(false);
        return array('data' => $this->portailInfoService->displayChoixDepartement());
    }

    public function confirmerIncidentTransAction()
    {

        $this->setRenderLayout(false);
        $creationPortailInfo = 'non';
        $creationCanari = 'non';
        $this->setRenderLayout(false);
        $oceaneAssistant = new OceaneAssistant($this->app);
        $data = StringTools::convertEncoding($this->request->getFromPost(), 'ISO-8859-15', 'UTF-8');
        $astroId = $data['astroid'];
        $typeRessource = $data['hidden_type_ressource'];
        $ticketId = $data['ticketid'];
        $data['date_retablissementUTC'] = $oceaneAssistant->changeDateToUTCoceane($data['date_retablissement']);
        $this->astroRepository->updateTicketConfirmIncident($astroId);

        $paramsPortailInfo = $this->astroRepository->getValuesParamConfirmTrans($data['id_jeu_param'], $data['hidden_type_ressource'], 'CREATE_PORTAIL_INFO');
        $paramsCanari = $this->astroRepository->getValuesParamConfirmTrans($data['id_jeu_param'], $data['hidden_type_ressource'], 'CREATE_FICHE_CANARI');
        $message = $this->oceaneUpdateAjaxTrans($data);
        $message['etat'] = 'ok';

        if (($data['impact_client'] == '2' || $data['impact_client'] == '7') && $message['etat'] == 'ok') {
            if (is_array($paramsPortailInfo) && key_exists('IS_CHECKED', $paramsPortailInfo) && $paramsPortailInfo['IS_CHECKED'] == '1' && $this->portailInfoService->getCasPortailInfoCanari($typeRessource, $ticketId)) {
                $creationPortailInfo = 'oui';
            }
            if (is_array($paramsCanari) && key_exists('IS_CHECKED', $paramsCanari) && $paramsCanari['IS_CHECKED'] == '1' && $this->portailInfoService->getCasPortailInfoCanari($typeRessource, $ticketId)) {
                $creationCanari = 'oui';
            }
        }
        $data['indice_type_ress_portail'] = (is_array($paramsPortailInfo) && key_exists('TYPE', $paramsPortailInfo)) ? $paramsPortailInfo['TYPE'] : '';
        $data['indice_type_ress_canari'] = (is_array($paramsCanari) && key_exists('TYPE', $paramsCanari)) ? $paramsCanari['TYPE'] : '';
        $return = array(
            'data' => $data,
            'crea_portail_info' => $creationPortailInfo,
            'crea_fiche_canari' => $creationCanari,
            'seuils' => $message['seuils'],
            'commentaire' => $message['commentaire'],
            'message' => $message['message']
        );
        return $this->sendEncodedToJson($return, true, 'ISO-8859-15');
    }

    public function creationPortailInfoAjaxAction()
    {
        $this->disableRendering();
        $data = StringTools::convertEncoding($this->request->getFromPost(), 'ISO-8859-15', 'UTF-8');

        $seuilGraveIsSup = key_exists('seuil_grave_is_sup', $data) ? $data['seuil_grave_is_sup'] : 'false';
        $seuilMajeurIsSup = key_exists('seuil_majeur_is_sup', $data) ? $data['seuil_majeur_is_sup'] : 'false';
        $data['seuil_grave_is_sup'] = ($seuilGraveIsSup == 'true');
        $data['seuil_majeur_is_sup'] = ($seuilMajeurIsSup == 'true');

        $creationPortailInfo = $this->portailInfoService->creerPortailInfo($data);

        return $this->sendEncodedToJson($creationPortailInfo);
    }

    public function creationFicheCanariAjaxAction()
    {
        $this->disableRendering();
        $data = StringTools::convertEncoding($this->request->getFromPost(), 'ISO-8859-15', 'UTF-8');

        $creationFicheCanari = $this->canariService->creerFicheCanari($data);

        return $this->sendEncodedToJson($creationFicheCanari);
    }

    public function majFicheCanariAction()
    {
        $this->disableRendering();
        $data = $this->request->getFromPost();
        $majFicheCanari = $this->canariService->majFicheCanari($data);

        return $this->sendEncodedToJson($majFicheCanari);
    }


    private function formatRegle(array $regles)
    {
        $result = array();
        if (!empty($regles)) {
            foreach ($regles as $value) {
                $result[$value['CODE']] = array(
                    'OBLIGATOIRE' => $value['OBLIGATOIRE'],
                    'INFOBULLE' => $value['INFOBULLE']
                );
            }
        }
        return $result;
    }

    public function calculDateRetablissementAction()
    {
        $this->disableRendering();
        $data = $this->request->getFromPost();

        $maDate = key_exists('maDate', $data) ? $data['maDate'] : '';
        $duree = key_exists('duree', $data) ? $data['duree'] : '';
        $maPriorite = key_exists('maPriorite', $data) ? $data['maPriorite'] : '';
        $ticketId = key_exists('ticketId', $data) ? $data['ticketId'] : '';
        $domaine = key_exists('domaine', $data) ? $data['domaine'] : '';

        $this->getOceane->getOceaneData($ticketId, $this->loginId);
        $champComp6 = StringTools::convertEncoding($this->getOceane->getTicketCharacteristics(6), 'ISO-8859-15', 'UTF-8');
        $astroSession = $this->app->get('Session')->get('astroOft' . $ticketId);
        $idBandeau = $this->astroRepository->getBandeauId($astroSession['bandeau']);
        if ($domaine == 'TRANS') {
            $idJeuParam = $this->astroRepository->getJeuParamByBandeauFonction($idBandeau, 'CONFIRMER_TRANS');
        } else {
            $idJeuParam = $this->astroRepository->getJeuParamByBandeauFonction($idBandeau, 'CONFIRMER_GENERIQUE');
        }

        $arrDureeRetabInitial = $this->astroIhmSqlRepository->getConfirmerIncidentListeByChamp($idJeuParam, 'DELAI_RETAB_INITIAL');
        $arrayOptionsDRI = $arrDureeRetabInitial['options'];

        foreach ($arrayOptionsDRI as $key => $dri) {
            if (strpos($champComp6, $dri['CONDITION']) !== false) {
                $arrayOptionsDRI[$key]['IDENTIFIANT'] = $dri['DELAI'];
            }
        }
        $dateRetablisement = $this->confirmerService->calculDateRetablissement($maDate, $duree, $maPriorite, $arrayOptionsDRI);

        return $this->sendEncodedToJson($dateRetablisement);
    }


}
