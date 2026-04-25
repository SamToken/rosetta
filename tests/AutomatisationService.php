<?php


namespace App\Service;

use App\Repository\AgpRepository;
use App\Repository\TraceRepository;
use App\Tools\AgpCC;
use App\Tools\Message;
use App\Tools\OceaneAssistant;
use App\View\Helper\DemandeIntervention;
use Hbm\Common\Tools\StringTools;
use Hbm\Globalapi\Service\Rest\Oceane;
use Hbm\Globalapi\Service\Soap\OceaneUpd;
use Zend\Json\Json;
use Hbm\Common\Service\LinkService;

class AutomatisationService
{

    protected $app;

    protected $messageFile;

    /**
     * @var AgpRepository
     */
    protected $agpRepo;

    /**
     * @var TraceRepository
     */
    protected $traceRepo;

    /**
     * @var AbandonnerService
     */
    protected $abandonner;

    protected $loginId;

    protected $sessId;

    public function __construct($app)
    {
        $this->app = $app;
        // gestion des messages d'erreur
        $messageFileName = $this->app->config['message_file'];
        $this->messageFile = DATA_DIR . '/' . $messageFileName;

        $this->agpRepo = $this->app->get('AgpRepository');
        $this->traceRepo = $this->app->get('TraceRepository');

        $this->abandonner = $this->app->get('Abandonner');

        $this->loginId = $this->app->get('Session')->getUtilisateurLogin();
        $this->sessId = $this->app->get('Session')->getUtilisateurId();
        $this->linkCommonService = new LinkService($this->app);
        $this->instance = $this->app->config['ENV'];
        $this->urlCadi = $this->linkCommonService->getGlobalLink('CADI', $this->instance, array('TIC' => ''));

    }

    public function demandeIntervention($ticketId, $return = array())
    {
        $ticketSession = $this->app->get('Session')->get('astroOft' . $ticketId);
        $astroId = (!is_null($ticketSession) && key_exists('astroid', $ticketSession)) ? $ticketSession['astroid'] : '';
        $message = new Message($this->app, $astroId, $this->messageFile);
        $oceaneAssistant = new OceaneAssistant($this->app);
        $res = $this->initAgp($ticketId);
        $infoAutomatisation = $this->agpRepo->getInfoActionAutomatisation(41);
        $dateActionEnCours = $oceaneAssistant->changeDateToUTCoceane($this->agpRepo->calcDateOuvree(3, $infoAutomatisation['ID_ENTITE']));
        $actionEnCours = $infoAutomatisation['ACTION_EN_COURS'];
        $loginUser = strtoupper($this->loginId);
        $modeActivation = $infoAutomatisation['MODE_ACTIVATION'];
        $urgence = $infoAutomatisation['URGENCE'];
        $pilotGroup = key_exists('pilotgroup', $ticketSession) ? $ticketSession['pilotgroup'] : '';

        $agpIdRscDslam = key_exists('agp_id_rsc_dslam', $res) ? $res['agp_id_rsc_dslam'] : null;
        $agpChassis = (key_exists('chassis', $res) && key_exists(0, $res['chassis'])) ? $res['chassis'][0] : null;
        $agpCarte = key_exists('agp_carte', $res) ? $res['agp_carte'] : null;
        $agpPeriph = array('0' => "FAN");
        $agpLien = key_exists('agp_lien', $res) ? $res['agp_lien'] : null;

        $commentaire = new AgpCC($this->app, array(
            'Id_astro' => $astroId,
            'Id_rsc' => $agpIdRscDslam,
            'Id_action' => 41,
            'Chassis' => $agpChassis,
            'Cartes' => $agpCarte,
            'Periphs' => $agpPeriph,
            'Liens' => $agpLien,
            'EDSPilote' => key_exists('pilotgroup', $ticketSession) ? $ticketSession['pilotgroup'] : ''
        ));

        $agpCommentaire = $commentaire->getCommentaire();

        $values = array(
            'troubleUrgency' => $urgence,
            'modeActivation' => $modeActivation,
            'edsActif' => '',
            'groupActionInProgressDate' => $dateActionEnCours,
            'groupActionInProgress' => $actionEnCours,
            'edsPilote' => $pilotGroup,
            'localCommentLabel' => $agpCommentaire,
            'PartyID' => $loginUser,
            'localCommentPartyID' => $loginUser,
            'plannedRestorationDate' => '',
            'tagHNO' => '0'
        );

        $this->traceRepo->setTrace($astroId, "ENVOI ACT OCEANE", serialize($values), $this->sessId, $ticketId);
        $serviceGlobalApi = $this->app->get('GlobalApiUrlService');
        $connexionDataUrl = $serviceGlobalApi->getUrlApi('CONNEXION');
        $oceaneUpdateUrl = $serviceGlobalApi->getUrlApi('OCEANE_UPT');

        $this->hbmLogin = $loginUser;
        $this->getapeService = $this->app->get('Gatape');
        $oceaneApiData = $this->globalApiService->getUrlApi('API_OCEANE');
        $token = $this->getapeService->getToken($oceaneApiData, 'inside');

        $headerConfig = array(
            "X-Client-User-Id: $this->hbmLogin",
            "X-HTTP-Method-Override: PATCH"
        );
        $oceaneApi = new Oceane($token, $headerConfig);
        $result = $oceaneApi->getResponseAgirPiloter($oceaneApiData['url'], $ticketId, $values);

        $valueCommentaire = array(
            "author" => $loginUser,
            "text" =>  $agpCommentaire,
            "commentType" => array(
                "id" => "INT"
            ),
            "operationType" => array(
                "id" => 9
            )
        );

        $oceaneApi->ajouterCommentaire($oceaneApiData['url'], $ticketId, $valueCommentaire);

        $this->traceRepo->setTrace($astroId, "RETOUR ACT OCEANE", $result, $this->sessId, $ticketId);

        $value = array(
            '###HNO###' => 'HO',
            '###ENTITE###' => $infoAutomatisation['ENTITE'],
            '###ACTION###' => $infoAutomatisation['ACTION'],
            '###RESSOURCE###' => $res['agp_dslam'],
            '###EDS###' => ''
        );

        // Erreur
        if (is_array($result) && key_exists('code', $result)  && key_exists('message', $result)) {
            $error = $result['code'] . ' ' . $result['message'];
            $message->setMessageComplexe("E_AGIR_PILOTER_OCEANE", array_merge($value, array(
                '###DETAIL###' => $error
            )));
            array_push($return['message'], $message->replaceData($message->getMessageJournal('E_AGIR_PILOTER_OCEANE'), $value));
            $return['statut'] = 'ko';
        } else {
            $message->setMessageComplexe("AGIR_PILOTER_OK", $value);

            // Enregistrement de l'action Choisie pour Rétablir Clôturer
            $this->agpRepo->enrAction($astroId, 41, 'ADSL');
            // Initialisation EDS pilote
            $this->app->get('AssistantRepository')->addEDS($ticketId, '', 'ACTIF');

            array_push($return['message'], $message->replaceData($message->getMessageJournal('AGIR_PILOTER_OK'), $value));
            $return['statut'] = 'ok';
            $return['url_cadi'] = $this->urlCadi . $ticketId;
        }

        return $return;
    }

    public function initAgp($ticketId)
    {
        $interventionHelper = new DemandeIntervention($this->app);
        // Obligatoire car dans certains cas, ID_RESSOURCE_DSLAM n'est pas dans la variable $_SESSION
        $ticketSession = $this->app->get('Session')->get('astroOft' . $ticketId);
        $astroId = (!is_null($ticketSession) && key_exists('astroid', $ticketSession)) ? $ticketSession['astroid'] : '';
        $idRessource = (!is_null($ticketSession) && key_exists('id_ressource', $ticketSession)) ? $ticketSession['id_ressource'] : '';
        $rsc = $this->app->get('AstroRepository')->getRessource($idRessource);
        $idRscDslam = $rsc['ID_RESSOURCE_DSLAM'];

        if ($this->app->get('EdrRepository')->testDataInfo($astroId) == 0) {
            $msg = $interventionHelper->getIndispoMessage();
            return array(
                'msg' => $msg
            );
        } else {
            $dslamData = $this->app->get('EdrRepository')->getBlobDslam($idRscDslam)['BLOBDATA'];
            $result = Json::decode(StringTools::convertEncoding($dslamData, 'UTF-8', 'ISO-8859-15'), true)[0];
            $deports = key_exists('offsets', $result) ? $result['offsets'] : array();
            $chassisArr = array();
            if (key_exists('racks', $result)) {
                foreach ($result['racks'] as $chassis) {
                    array_push($chassisArr, $chassis['rackName']);
                }
            }

            return array(
                'agp_id_rsc' => $idRessource,
                'agp_id_rsc_dslam' => $rsc['ID_RESSOURCE_DSLAM'],
                'agp_id_rsc_ec' => $idRessource,
                'ticketid' => $ticketId,
                'agp_deports' => $deports,
                'agp_master' => $result['masterName'],
                'agp_dslam' => $result['equipmentName'],
                'dslam_name' => $result['equipmentName'],
                'chassis' => $chassisArr
            );

        }
    }

    public function confirmerIncident($ticketId, $return = array())
    {
        $astroRepo = $this->app->get('AstroRepository');
        $ticketSession = $this->app->get('Session')->get('astroOft' . $ticketId);
        $astroId = (!is_null($ticketSession) && key_exists('astroid', $ticketSession)) ? $ticketSession['astroid'] : '';
        // gestion des messages d'erreur
        $message = new Message($this->app, $astroId, $this->messageFile);
        //creation Adelia
        $result = $this->createAdelia($astroRepo, $ticketSession);

        $adelia = key_exists('adelia', $result) ? $result['adelia'] : null;
        $data = key_exists('data', $result) ? $result['data'] : array();

        if (key_exists('priorite', $data) && in_array($data['priorite'], array(3, 5))) {
            $data['commentaire_impact_client'] = null;
        }

        $this->traceRepo->setTrace($astroId, "ADELIA REPONSE", $adelia, $this->sessId, $ticketId);

        if (property_exists($adelia, 'code') && ($adelia->code != '' || $adelia->id == '')) {
            // Si la création automatique ADELIA a planté
            $messageAdelia = $adelia->message . ' ' . $adelia->description;
            $message->setMessage("E_CONFIRM_ADELIA_AUTO_ADELIA", StringTools::convertEncoding($messageAdelia, 'ISO-8859-15', 'UTF-8'));
            array_push($return['message'], $message->getMessageJournal('E_CONFIRM_ADELIA_AUTO_ADELIA'));
            $return['statut'] = 'ko';
        } else {
            $return = $this->updateTicketConfirmIncident($astroRepo, $message, $astroId, $ticketId, $adelia->id, $data, $return);
        }

        return $return;
    }

    public function updateTicketConfirmIncident($astroRepo, $message, $astroId, $ticketId, $adeliaId, $data, $return)
    {
        $astroRepo->updateTicketConfirmIncident($astroId, $adeliaId, $data['impact_nature']);
        $result = $this->app->get('OceaneService')->updateOceaneConfirmer($data, $ticketId, $astroId);
        $this->traceRepo->setTrace($astroId, "CONFIRMER OCEANE REPONSE", $result, $this->sessId, $ticketId);
        $result=json_decode($result);

           if (property_exists($result, 'code') && $result->message != '') {

                $values = array(
                    '###ADELIA_ID###' => $adeliaId,
                    '###DETAIL###' =>$result->message.'  '.$result->description.'   '.$result->infoURL
                );
                $messageKo = $message->setMessageComplexe("E_CONFIRM_ADELIA_AUTO_OCEANE", $values);
                array_push($return['message'], $messageKo);
                $return['code'] = 'ko';
                $return['message_error_api'] = $result->message;
                $return['description'] = $result->description;
                $return['infoURL'] = $result->infoURL;
                $return['statut'] = 'ko';

        } else {
            $values = array(
                '###ADELIA_ID###' => $adeliaId
            );
            $message->setMessageComplexe("CONFIRM_ADELIA_AUTO_OK", $values);
            array_push($return['message'], $message->getMessageJournal('CONFIRM_ADELIA_AUTO_OK'));
            $return['statut'] = 'ok';
        }

        return $return;
    }

    public function createAdelia($astroRepo, $ticketSession)
    {
        $astroId = key_exists('astroid', $ticketSession) ? $ticketSession['astroid'] : '';
        $ticketId = key_exists('ticketid', $ticketSession) ? $ticketSession['ticketid'] : '';
        $oceaneAssistant = new OceaneAssistant($this->app);
        $dataAstro = $astroRepo->getTicket($astroId);
        $dataAstro = (count($dataAstro)) ? $dataAstro[0] : array();
        $arrDureeRetablissement = array();

        foreach ($this->app->get('AstroIhmSqlRepository')->getDureeRetablissement() as $durre) {
            $arrDureeRetablissement[$durre['PRIORITY_ID']] = $durre['DUREE_RETABLISSEMENT_MAX'];
        }

        $dslam = key_exists('id1', $ticketSession) ? $ticketSession['id1'] : '';
        $connectedGroup = key_exists('connectedgroup', $ticketSession) ? $ticketSession['connectedgroup'] : '';
        $sourceDerangement = $astroRepo->getSourceDerangement($connectedGroup);
        $dataDebutAlarmeIadr = key_exists('DT_DEBUT_ALARME_IADR', $dataAstro) ? $dataAstro['DT_DEBUT_ALARME_IADR'] : '';
        $typeRessourceIadr = key_exists('TYPE_RESSOURCE_IADR', $dataAstro) ? $dataAstro['TYPE_RESSOURCE_IADR'] : '';
        $descriptionDerangement = (key_exists('LB_TECHNIQUE_IADR', $dataAstro)  && !is_null($dataAstro['LB_TECHNIQUE_IADR']))? $dataAstro['LB_TECHNIQUE_IADR'] : ' ';
        $commentaireImpactClient = $this->abandonner->getCommentaireImpactClient($dataAstro);

        $time = new \DateTime();
        $time = $time->createFromFormat('j/m/Y H:i', $oceaneAssistant->changeUTCToDate($dataDebutAlarmeIadr));
        $time->add(new \DateInterval('PT' . intval($arrDureeRetablissement[3]) . 'M'));
        $dateRetablisement = $time->format('j/m/Y H:i');

        $data = array(
            'source_derangement' => $sourceDerangement ? $sourceDerangement : 'false',
            'description_derangement' => $descriptionDerangement,
            'impact_nature' => $astroRepo->getNatureImpactClient(3),
            'nature_impact_client' => 3,
            'impact_technique' => 'A',
            'dt_debut_alarme_iadr' => $dataDebutAlarmeIadr,
            'date_retablissement' => $dateRetablisement,
            'type_ressource_iadr' => $typeRessourceIadr,
            'commentaire_impact_client' => $commentaireImpactClient,
            'autre_commentaire' => '',
            'priorite' => 3,
            'hno' => 0,
            'priorite_commentaire' => '',
        );

        $adelia = $this->app->get('Adelia')->create($dslam, $ticketId, $astroId, $data);

        return array(
            'adelia' => $adelia,
            'data' => $data
        );
    }
}