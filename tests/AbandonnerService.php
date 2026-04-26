<?php
/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

namespace App\Service;

use App\Repository\AbandonBatchRepository;
use App\Repository\AdeliaRepository;
use App\Repository\AssistantRepository;
use App\Repository\AstroIhmSqlRepository;
use App\Repository\AstroLienRepository;
use App\Repository\AstroRepository;
use App\Repository\VerrouRepository;
use App\Tools\OceaneAssistant;
use App\Tools\Message;
use Hbm\Common\Tools\StringTools;
use Hbm\Globalapi\Service\Soap\OceaneUpd;
use Hbm\Globalapi\Service\Rest\Oceane;
use App\View\Helper\Adelia;
use Oft\Mvc\Application;
use App\Tools\DroitAstroTools;
use Hbm\Globalapi\Service\Rest\ApiOceane;

/**
 * Description of EdrService
 *
 * @author mbiyoud
 */
class AbandonnerService extends AstroBaseService
{

    /**
     * @var Application
     */
    protected $app;
    /**
     * @var AssistantRepository
     */
    protected $assistantRepository;

    /**
     * @var AdeliaRepository
     */
    protected $adeliaRepository;


    /**
     * @var VerrouRepository
     */
    protected $verrouRepository;

    /**
     * @var AstroRepository
     */
    protected $astroRepository;

    /**
     * @var AbandonBatchRepository
     */
    protected $abandonBatchRepository;

    /**
     * @var AstroLienRepository
     */
    protected $astroLienRepository;

    /**
     * @var AstroIhmSqlRepository
     */
    protected $astroIhmSqlRepository;

    /**
     * @var AdeliaService
     */
    protected $adeliaService;

    protected $globalApiService;
    /**
     * @var AireleService
     */
    protected $airelle;

    protected $getOceane;

    public function __construct($app)
    {
        $this->app = $app;
        $this->assistantRepository = $this->app->get('AssistantRepository');
        $this->adeliaRepository = $this->app->get('AdeliaRepository');
        $this->astroRepository = $this->app->get('AstroRepository');
        $this->verrouRepository = $this->app->get('VerrouRepository');
        $this->abandonBatchRepository = $this->app->get('AbandonBatchRepository');
        $this->astroLienRepository = $this->app->get('AstroLienRepository');
        $this->astroIhmSqlRepository = $this->app->get('AstroIhmSqlRepository');
        $this->adeliaService = $this->app->get('Adelia');
        $this->globalApiService = $app->get('GlobalApiUrlService');
        $this->maestroRepository = $app->get('MaestroRepository');
        $this->traceRepository = $this->app->get('TraceRepository');
        $this->sessId = (key_exists('api', $this->app->config) && $this->app->config['api']) ? $this->getUserId() : $this->app->get('Session')->getUtilisateurId();
        $this->loginId = (key_exists('api', $this->app->config) && $this->app->config['api']) ? $this->getLogin() : $this->app->get('Session')->getUtilisateurLogin();
        $this->analyseService = $this->app->get('AnalyseImpact');
        $this->airelle = $this->app->get('Airele');
        $this->getOceane = $this->app->get('OceaneGet');


    }

    /*
     * qualifierInformerClient
     * @param $astroId
     * @param $loginId
     * @return array
     */
    public function informerClient($astroId, $loginId)
    {
        $totalClts = '';
        $libelleImpactClient = '';

        $isLocked = $this->verrouRepository->isLocked($astroId, "confirmerIncident", true, $loginId);
        if ($isLocked === true) {
            $messageVerrou = $this->verrouRepository->getLabelVerrou($astroId, 'confirmerIncident');
        } else {
            $messageVerrou = '';
        }

        $dataAstroArray = $this->astroRepository->getTicket($astroId);
        $dataASTRO = $dataAstroArray[0];
        $dataAdelia = $this->adeliaRepository->getDataBlob($astroId);
        $adeliaPrestations = json_decode($dataAdelia["PRESTATIONS"]);

        $impact = $dataASTRO['ID_IMPACT_CLIENT_PRECONISE'];
        if ($impact != '') {
            $label = $this->astroRepository->getLabelPrio($dataASTRO['ID_IMPACT_CLIENT_PRECONISE']);
            $libelleImpactClient = $this->astroRepository->getLibelleImpactClient($dataASTRO['ID_IMPACT_CLIENT_PRECONISE']);

            $tdsl = (!is_null($adeliaPrestations) && property_exists($adeliaPrestations, 'TDSL')) ? intval($adeliaPrestations->TDSL) : 0;
            $totalClts = (is_array($dataAdelia) && key_exists('TOTAL_CLIENTS', $dataAdelia)) ? intval($dataAdelia['TOTAL_CLIENTS']) : 0;
            $priorite = (is_array($dataASTRO) && key_exists('ID_IMPACT_CLIENT_PRECONISE', $dataASTRO)) ? $dataASTRO['ID_IMPACT_CLIENT_PRECONISE'] : '';

            $priorite = $this->assistantRepository->getPriorite($priorite, $totalClts, $tdsl);
        } else {
            $label = "Pas d'impact préconisé";
            $priorite = '-';
        }

        return array(
            'is_locked' => $isLocked,
            'astroId' => $astroId,
            'message_verou' => $messageVerrou,
            'label' => $label,
            'priorite' => $priorite,
            'total_clients' => $totalClts,
            'libelle_impact_client' => $libelleImpactClient
        );
    }

    /**
     * @param $astroId
     * @param $label
     * @return array
     */
    public function displayReservation($astroId, $label)
    {
        $isMe = $this->verrouRepository->isLockedByMe($astroId, $label);
        $labelFinal = $this->verrouRepository->getLabelReservation($astroId, $label, $isMe);
        if ($labelFinal == '') {
            $imageName = 'doigt_vert';
        } else {
            if ($isMe) {
                $imageName = 'doigt_violet';
            } else {
                $imageName = 'doigt_rouge';
            }
        }

        return array(
            'image_name' => $imageName,
            'label_final' => $labelFinal
        );
    }


    public function abandonnerProcessAuto($idJeu, $ticketId, $astroId, $typeRessourceProd, $sessId, $loginId)
    {
        $messageFileName = $this->app->config['message_file'];
        $messageFile = DATA_DIR . '/' . $messageFileName;
        $abandonMessage = new Message($this->app, $astroId, $messageFile);

        $champValues = $this->abandonBatchRepository->getChampValues($idJeu);
        $detailProbleme = $this->astroIhmSqlRepository->getDetailFamilleProblemeValues($idJeu, $typeRessourceProd);

        $this->astroRepository->enrDateCauseAbandon($astroId, 'NON TRAITE - CLOTURE SYSTEME');
        $data = array(
            'originLabel' => 'NON TRAITE - CLOTURE SYSTEME',
            'startDate' => gmdate("c"),
            'localCommentLabel' => 'annulation événement - CAUSE ABANDON : NON TRAITE - CLOTURE SYSTEME',
            'localCommentPartyID' => $loginId,
            'partyRolePartyID' => $loginId,
            'troubleCauseLabel' => 'annulation événement - CAUSE ABANDON : NON TRAITE - CLOTURE SYSTEME',
            'troubleCauseCodeCategory' => isset($champValues['ABANDON_NATURE_FINALE']) ? $champValues['ABANDON_NATURE_FINALE'] : '',
            'troubleCauseDescription' => isset($detailProbleme[0]["IDENTIFIANT_DETAIL"]) ? $detailProbleme[0]["IDENTIFIANT_DETAIL"] : '',
            'troubleType' => isset($champValues['IMPACT_TECHNIQUE']) ? $champValues['IMPACT_TECHNIQUE'] : ''
        );

        $this->hbmLogin = $loginId;
        $this->getapeService = $this->app->get('Gatape');
        $oceaneApiData = $this->globalApiService->getUrlApi('API_OCEANE');
        $token = $this->getapeService->getToken($oceaneApiData, 'inside');

        $headerConfig = array(
            "X-Client-User-Id: $this->hbmLogin",
            "X-HTTP-Method-Override: PATCH"
        );

        $oceaneApi = new Oceane($token, $headerConfig);


        $this->app->get('TraceRepository')->setTrace($astroId, "OCEANE ENVOI", $data, $sessId, $ticketId);
        $result = json_decode($oceaneApi->getResponseAbandonProcessGenerique($oceaneApiData['url'], $ticketId, $data), true);
        $this->app->get('TraceRepository')->setTrace($astroId, "OCEANE RESPONSE", $result, $sessId, $ticketId);

        $dataCommentaire = array(
            "author" => $this->hbmLogin,
            "text" => $data['troubleCauseLabel'],
            "commentType" => array(
                "id" => "INT"
            ),
            "operationType" => array(
                "id" => 9
            )
        );
        $this->app->get('TraceRepository')->setTrace($astroId, "ENVOI OCEANE AJOUT COMMENTAIRE ABANDON EVENEMENT AUTO", $dataCommentaire, $this->sessId, $ticketId);
        $retourUpdate = json_decode($oceaneApi->ajouterCommentaire($oceaneApiData['url'], $ticketId, $dataCommentaire), true);
        $this->app->get('TraceRepository')->setTrace($astroId, "RETOUR OCEANE AJOUT COMMENTAIRE ABANDON EVENEMENT AUTO", $retourUpdate, $this->sessId, $ticketId);

        if (array_key_exists('message', $result) && array_key_exists('code', $result) && array_key_exists('description', $result)) {

            if ($result['message'] == 'Functional error: Ticket in closed status') {
                $this->abandonBatchRepository->updateTicketEtat($ticketId);
                return 2;
            } else {
                $message = 'code  :' . $result['code'] . 'message  :' . $result['message'] . '  description : ' . $result['description'];
                $abandonMessage->setMessage('E_ABANDON_EVENEMENT', $message);
                return 0;
            }
        } else {
            $this->abandonBatchRepository->updateTicketEtat($ticketId);
            $abandonMessage->setMessage('OK_ABANDON_EVENEMENT', 'Délai dépassé : abandon automatique du ticket');
            return 1;
        }
    }

    public function abandonnerProcess($data, $idJeu, $typeRessourceProd, $sessId, $loginId, $incidentEnCours = true)
    {
        $astroId = $data['astroid'];
        $ticketId = $data['ticketid'];
        $messageFileName = $this->app->config['message_file'];
        $messageFile = DATA_DIR . '/' . $messageFileName;

        $champValues = $this->abandonBatchRepository->getChampValues($idJeu);
        $detailProbleme = $this->astroIhmSqlRepository->getDetailFamilleProblemeValues($idJeu, $typeRessourceProd);

        if($incidentEnCours){
            $data['detail_cause_abandon'] = StringTools::convertEncoding($data['detail_cause_abandon'], 'ISO-8859-15', 'UTF-8');
        }
        $abandonMessage = new Message($this->app, $astroId, $messageFile, $sessId);
        $this->astroRepository->enrDateCauseAbandon($astroId, $data['cause_abandon'] . " " . $data['detail_cause_abandon']);

        $troubleCauseLabel = $data['cause_abandon'];
        $troubleCauseLabel .= ($data['detail_cause_abandon'] != '') ? ' - ' . $data['detail_cause_abandon'] : '';
        $troubleCauseLabel = $incidentEnCours ? StringTools::convertEncoding($troubleCauseLabel, 'ISO-8859-15', 'UTF-8') : $troubleCauseLabel;

        $causeAbandon = $incidentEnCours ? StringTools::convertEncoding($data['cause_abandon'], 'ISO-8859-15', 'UTF-8') : $data['cause_abandon'];
        $causeAbandonJournal = $causeAbandon;
        $causeAbandonJournal .= ($data['detail_cause_abandon'] != '') ? ' - ' . $data['detail_cause_abandon'] : '';
        $oceaneAssistant = new OceaneAssistant($this->app);
        $v = array(
            'originLabel' => (substr('CAUSE ABANDON : ' . $causeAbandon, 0, 30)),
            'startDate' => $oceaneAssistant->changeDateToUTCZuluoceane(date("d/m/Y H:i")),
            'localCommentLabel' => 'annulation événement - CAUSE ABANDON : ' . $troubleCauseLabel,
            'localCommentPartyID' => $loginId,
            'partyRolePartyID' => $loginId,
            'troubleCauseLabel' => 'annulation événement - CAUSE ABANDON : ' . $troubleCauseLabel,
            'troubleCauseCodeCategory' => isset($champValues['ABANDON_NATURE_FINALE']) ? $champValues['ABANDON_NATURE_FINALE'] : '',
            'troubleCauseDescription' => isset($detailProbleme[0]["IDENTIFIANT_DETAIL"]) ? $detailProbleme[0]["IDENTIFIANT_DETAIL"] : '',
            'troubleType' => isset($champValues['IMPACT_TECHNIQUE']) ? $champValues['IMPACT_TECHNIQUE'] : ''
        );
        $this->hbmLogin = $loginId;
        $this->getapeService = $this->app->get('Gatape');
        $oceaneApiData = $this->globalApiService->getUrlApi('API_OCEANE');
        $token = $this->getapeService->getToken($oceaneApiData, 'inside');

        $headerConfig = array(
            "X-Client-User-Id: $this->hbmLogin",
            "X-HTTP-Method-Override: PATCH"
        );

        $oceaneApi = new Oceane($token, $headerConfig);
        $this->app->get('TraceRepository')->setTrace($astroId, "OCEANE ENVOI", $v, $sessId, $ticketId);
        $result = json_decode($oceaneApi->getResponseAbandonProcessGenerique($oceaneApiData['url'], $ticketId, $v), true);
        $this->app->get('TraceRepository')->setTrace($astroId, "OCEANE REPONSE", $result, $sessId, $ticketId);
        $dataCommentaire = array(
            "author" => $this->hbmLogin,
            "text" => $v['troubleCauseLabel'],
            "commentType" => array(
                "id" => "INT"
            ),
            "operationType" => array(
                "id" => 9
            )
        );
        $this->app->get('TraceRepository')->setTrace($astroId, "ENVOI OCEANE AJOUT COMMENTAIRE ABANDON EVENEMENT", $dataCommentaire, $this->sessId, $ticketId);
        $retourUpdate = json_decode($oceaneApi->ajouterCommentaire($oceaneApiData['url'], $ticketId, $dataCommentaire), true);
        $this->app->get('TraceRepository')->setTrace($astroId, "RETOUR OCEANE AJOUT COMMENTAIRE ABANDON EVENEMENT", $retourUpdate, $this->sessId, $ticketId);

        if (array_key_exists('message', $result) && array_key_exists('code', $result) && array_key_exists('description', $result)) {
            $message = 'code  :' . $result['code'] . 'message  :' . $result['message'] . '  description : ' . $result['description'];
            $code = $incidentEnCours ? 'E_ABANDON_EVENEMENT' : 'API_E_ABANDON_CARTE_BRASIL_ETEINTE';
            return array(
                'message' => $abandonMessage->setMessage($code, $message),
                'statut' => 'ko'
            );
        } else {
            $this->abandonBatchRepository->updateTicketEtat($ticketId);
            $code = $incidentEnCours ? 'OK_ABANDON_EVENEMENT' : 'API_OK_ABANDON_CARTE_BRASIL_ETEINTE';
            $abandonMessage->setMessage($code, $causeAbandonJournal);
            return array(
                'message' => "Le ticket Océane n° $ticketId a été clos (abandon).",
                'statut' => 'ok'
            );
        }
    }

    /**
     * Récupérer la liste des priorité
     *
     * @retrun : array
     */
    public function getValuePriorite()
    {
        $listPriorites = array();
        foreach ($this->astroLienRepository->getPrioriteLibelle() as $prio) {
            $listPriorites[$prio['PRIORITY_ID']] = $prio['PRIORITY_LIBELLE'];
        }
        return $listPriorites;
    }

    public function getNatureImpactClientListe($selected = null)
    {
        $dataRaw = $this->astroIhmSqlRepository->getNatureImpactClient();
        $data = array();

        for ($i = 0; $i < count($dataRaw['IMPACTCLIENT_ID']); $i++) {
            $data[$dataRaw['IMPACTCLIENT_ID'][$i]] = ucfirst($dataRaw['AD_IMPACTNATURE'][$i]);
        }

        return $this->getOptionsHTML($data, $selected);
    }

    /**
     * A mettre ds helperView
     *
     * @param array $array
     * @param string $default
     * @return string
     */
    public function getOptionsHTML($array, $default = "")
    {
        $result = "";

        foreach ($array as $k => $v) {
            $selected = ($default == $k) ? 'selected' : '';
            $result .= "<option " . $selected . " value='" . $k . "'>" . $v . "</option>";
        }
        return $result;
    }

    public function getCommentaireImpactClient($dataAstro)
    {
        $adelia = new Adelia();
        $dataAdelia = $this->adeliaRepository->getDataBlob($dataAstro['ID_TICKET_ASTRO']);
        $dataPrestation = json_decode($dataAdelia['PRESTATIONS']);
        $dataFiltered = $adelia->filterPrestation($dataPrestation);

        $this->getOceane->getOceaneData($dataAstro['ID_TICKET_ASTRO'],  $this->loginId);
        $detectionDate = $this->getOceane->getDetectionDate();
        $oceaneAssistant = new OceaneAssistant($this->app);
        if ($dataAdelia) {
            $dataAdelia['SEUIL_GRAVE'] = intval($dataAdelia['SEUIL_GRAVE']);
            $dataAdelia['SEUIL_MAJEUR'] = intval($dataAdelia['SEUIL_MAJEUR']);
        }

        $rc = '&#13;&#10;';

        $date = $oceaneAssistant->changeUTCToDate($dataAstro['DT_DEBUT_ALARME_IADR']);

        $commentaire = '';
        $commentaire .= '# IC Impact clients #' . $rc;
        $commentaire .= 'Début d\'incident: ' . $date . $rc;
        foreach ($dataFiltered as $k => $v) {
            $commentaire .= $k . ':' . $v . $rc;

        }
        if ($dataAdelia['TOTAL_CLIENTS'] > 0) {
            if ($dataAstro['ADELIA_MANUEL'] == 'o') {
                $dataAdeliaManuel = $this->adeliaRepository->getDataBlobManuel($dataAstro['ID_TICKET_ASTRO']);
                if ($dataAdeliaManuel['BEGIN_DATE'] != '' && $dataAdeliaManuel['SEUIL_GRAVE'] != '' && $dataAdeliaManuel['SEUIL_MAJEUR'] != '') {
                    $commentaire .= 'grave à partir du ' . $this->adeliaService->getDateSeuil($dataAdeliaManuel['BEGIN_DATE'], $dataAdeliaManuel['SEUIL_GRAVE'], true) . $rc;
                    $commentaire .= 'majeur à partir du ' . $this->adeliaService->getDateSeuil($dataAdeliaManuel['BEGIN_DATE'], $dataAdeliaManuel['SEUIL_MAJEUR'], true) . $rc;
                } else {
                    $commentaire .= $rc;
                }

            } else {

                $seuilGrave =  ($detectionDate != null) ? $this->adeliaService->getDateSeuil($detectionDate, $dataAdelia['SEUIL_GRAVE']) : '-';
                $seuilMajeur = ($detectionDate != null) ? $this->adeliaService->getDateSeuil($detectionDate, $dataAdelia['SEUIL_MAJEUR']) : '-';
                $commentaire .= 'grave à partir du ' . $seuilGrave . $rc;
                $commentaire .= 'majeur à partir du ' . $seuilMajeur . $rc;
            }
        }
        return $commentaire;
    }
    public function getCommentaireImpactClientTvNum($dataAstro, $adeliaId, $compteMachine)
    {
        $adelia = new Adelia();
        $dataAdelia = $this->adeliaRepository->getDataBlob($dataAstro['ID_TICKET_ASTRO']);
        $dataPrestation = json_decode($dataAdelia['PRESTATIONS']);
        $dataFiltered = $adelia->filterPrestation($dataPrestation);
        $idRessource = '';
        $oceaneAssistant = new OceaneAssistant($this->app);
        if ($dataAdelia) {
            $dataAdelia['SEUIL_GRAVE'] =  intval($dataAdelia['SEUIL_GRAVE']);
            $dataAdelia['SEUIL_MAJEUR'] = intval($dataAdelia['SEUIL_MAJEUR']);
        }

        $rc = '&#13;&#10;';

        $date = $oceaneAssistant->changeUTCToDate($dataAstro['DT_DEBUT_ALARME_IADR']);

        $commentaire = '';
        $commentaire .= '# IC Impact clients #' . $rc;
        $commentaire .= 'Début d\'incident: ' . $date . $rc;
        $commentaire .= 'TVNUM'.':'.$dataFiltered['TVNUM'] . $rc;

        if ($dataAdelia['TOTAL_CLIENTS'] > 0) {
            if ($dataAstro['ADELIA_MANUEL'] == 'o') {
                $dataAdeliaManuel = $this->adeliaRepository->getDataBlobManuel($dataAstro['ID_TICKET_ASTRO']);
                if ($dataAdeliaManuel['BEGIN_DATE'] != '' && $dataAdeliaManuel['SEUIL_GRAVE'] != '' && $dataAdeliaManuel['SEUIL_MAJEUR'] != '') {
                    $commentaire .= 'grave à partir du ' . $this->adeliaService->getDateSeuil($dataAdeliaManuel['BEGIN_DATE'], $dataAdeliaManuel['SEUIL_GRAVE'], true) . $rc;
                    $commentaire .= 'majeur à partir du ' . $this->adeliaService->getDateSeuil($dataAdeliaManuel['BEGIN_DATE'], $dataAdeliaManuel['SEUIL_MAJEUR'], true) . $rc;
                } else {
                    $commentaire .= $rc;
                }

            } else {
                $ticket = $this->astroRepository->getTicket($dataAstro['ID_TICKET_ASTRO']);
                if (count($ticket)) {
                    $idRessource = $ticket[0]['ID_RESSOURCE'];
                }
                $result = $this->getSeuilsAdelia($idRessource, $adeliaId ,$dataAstro, $compteMachine);
                $seuilGrave = $result['seuil_grave'];
                $seuilMajeur = $result['seuil_majeur'];
                $commentaire .= 'grave à partir du ' . $seuilGrave . $rc;
                $commentaire .= 'majeur à partir du ' . $seuilMajeur . $rc;
            }
        }
        return $commentaire;
    }

    public function getCommentaireImpactClientTemplate($dataAstro)
    {
        $oceaneAssistant = new OceaneAssistant($this->app);
        $rc = '&#13;&#10;';
        $date = $oceaneAssistant->changeUTCToDate($dataAstro['DT_DEBUT_ALARME_IADR']);
        $commentaire = '';
        $commentaire .= '# IC Impact clients #' . $rc;
        $commentaire .= 'Début d\'incident: ' . $date . $rc;
        $commentaire .= 'XLAN TDSL:' . $rc;
        $commentaire .= 'Internet:' . $rc;
        $commentaire .= 'TOIP:' . $rc;
        $commentaire .= 'TVNUM:' . $rc;
        $commentaire .= 'NETVPN:' . $rc;
        $commentaire .= 'grave a partir: ' . $rc;
        $commentaire .= 'majeur a partir: ' . $rc;
        return $commentaire;
    }


    /**
     * @param $ticketId
     * @param $astroId
     * @param $valeurs
     * @return array
     * @throws \Exception
     */
    public function confirmerBase($ticketId, $astroId, $valeurs)
    {
        $messageFileName = $this->app->config['message_file'];
        $messageFile = DATA_DIR . '/' . $messageFileName;
        $messageManager = new Message($this->app, $astroId, $messageFile);
        $idUtilisateur = $this->app->get('Session')->getUtilisateurId();
        $this->getapeService = $this->app->get('Gatape');
        $oceaneApiData = $this->globalApiService->getUrlApi('API_OCEANE');
        $token = $this->getapeService->getToken($oceaneApiData, 'inside');
        $headerConfig = array(
            "X-Client-User-Id: $this->loginId",
            "X-HTTP-Method-Override: PATCH",
        );

        $oceaneApi = new Oceane($token, $headerConfig);

        $this->app->get('TraceRepository')->setTrace($astroId, "OCEANE ENVOI", $valeurs, $idUtilisateur, $ticketId);
        $dataConfirmation = array(
            'ticketType' => array(
                'id' => 1,
            ),

            'relatedParty' => array(
                0 => array(
                    'id' => $valeurs['partyRolePartyID'],
                    'role' => 'CustomerRepresentative',
                    '@referredType' => 'Organisation',
                ),
            )
        );
        $result = json_decode($oceaneApi->getConfirmerBase($oceaneApiData['url'], $ticketId, $dataConfirmation), true);

        $this->app->get('TraceRepository')->setTrace($astroId, "OCEANE REPONSE", $result, $idUtilisateur, $ticketId);

        if (key_exists('code', $result) && key_exists('message', $result)) {
            $message = $result['code'] . ' ' . $result['message'];
            $errorOceane = $messageManager->setMessage('E_CONFIRM', $message);
            return array(
                'return' => 'ko',
                'error_oceane' => $errorOceane
            );
        } else {
            $resultOceane = $messageManager->setMessage('CONFIRM_OK');
            return array(
                'return' => 'ok',
                'result_message' => $resultOceane
            );
        }
    }

    /**
     * Abandon automatique des tickets événements
     */
    public function abandonnerAuto()
    {
        $nbOk = $nbKo = 0;

        $tickets = $this->abandonBatchRepository->getTicketEvenement();
        echo "<u> Tickets événements traités : </u> <br /> \n";
        foreach ($tickets as $ticket) {

            $astroSession = $this->app->get('Session')->get('astroOft' . $ticket['TICKETOCEANEID']);
            $connectedGroup = key_exists('connectedgroup',$astroSession) ? $astroSession['connectedgroup'] : '';
            $loginId = $this->astroRepository->getCompteMachine($connectedGroup);

            $result = $this->abandonnerProcessAuto($ticket['ID_JEU_PARAM'], $ticket['TICKETOCEANEID'], $ticket['ID_TICKET_ASTRO'], $ticket['TYPE_RESSOURCE'], '', $loginId);
            if ($result == 1) {
                $this->abandonBatchRepository->updateTicketEtat($ticket['TICKETOCEANEID']);
                $nbOk++;
                echo $ticket['TICKETOCEANEID'] . " : abandon OK <br /> ";
            } elseif ($result == 2) {
                $this->abandonBatchRepository->updateTicketEtat($ticket['TICKETOCEANEID']);
                $nbKo++;
                echo $ticket['TICKETOCEANEID'] . " : échec abandon <br /> \n";
            } else {
                $nbKo++;
                echo $ticket['TICKETOCEANEID'] . " : échec abandon <br /> \n";
            }
        }
        echo "<u> Résultat du traitement : </u> <br /> \n";
        echo "Nombre de tickets abandonnés :   $nbOk <br /> \n
              Nombre de tickets non abandonnés (échec) :  $nbKo <br /> \n";

        if ($nbKo == 0) {
            echo "<b> Traitement OK</b> <br /> \n";
        } else {
            if ($nbOk > 0) {
                echo "<b> Traitement OK partiel </b> <br /> \n";
            } else {
                echo "<b> Traitement KO</b> <br /> \n";
            }
        }

    }

    public function getPrioritePreconiseByClasite($ticketId, $login, $fonctions, $astroSession)
    {
        $informerClient = $this->informerClient($astroSession['astroid'], $login);
        $priorite = (in_array('TICKET_ADELIA', $fonctions)) ? $informerClient['priorite'] : $this->astroLienRepository->getPrioriteLibById($astroSession['priority']);

        $resultFg = $this->app->get('OceaneService')->findAndGetOceane($ticketId);
        $clasite = array_key_exists('clasite_prio', $resultFg) ? $resultFg['clasite_prio'] : '';
        $prioClasite = ($astroSession['type'] == 'S-SUP') ? $this->astroRepository->getPrioByCalsite($clasite) : '-';

        return ($prioClasite == '-') ? $priorite : $prioClasite;
    }

    public function preconisationImpactPrioriteAdsl($idTicket, $login, $astrId = null, $isApi = null)
    {
        $ticketId = $idTicket;

        $droitTools = new DroitAstroTools($this->app);
        $isClientEntreprise = false;
        $isNetVpn = '';
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
            if ($isApi == 1) {
                $astroId = $astrId;
            }
            $informerClient = $this->informerClient($astroId, $login);
            $adelia = $this->adeliaService->getData($astroId);

            $totalClients = (is_array($adelia) && key_exists('TOTAL_CLIENTS', $adelia)) ? intval($adelia['TOTAL_CLIENTS']) : 0;
            $nombreClientEntreprise = (is_array($adelia) && key_exists('CLIENTS_ENTREPRISE', $adelia)) ? $adelia['CLIENTS_ENTREPRISE'] : '';
            if ($nombreClientEntreprise == 'oui' || intval($nombreClientEntreprise) > 0) {
                $isClientEntreprise = true;
            }
            $oceaneAssistant = new OceaneAssistant($this->app);
            $idJeuParam = $this->astroRepository->getJeuParamByBandeauFonction($idBandeau, 'CONFIRMER_GENERIQUE');
            $isNetVpn = $this->astroRepository->checkNetVpn($idJeuParam);
            if (!empty($adelia) && key_exists('PRESTATIONS', $adelia)) {
                $prestations = key_exists('PRESTATIONS', $adelia) ? json_decode($adelia['PRESTATIONS'], true) : '';
            }

            if (!empty($adelia) && !empty($prestations) && $prestations != '' && key_exists('NETVPN', $prestations) && $prestations['NETVPN'] > 0) {
                $isNetVpnAdelia = 1;
            }
            if ($isNetVpn == '1' && $isNetVpnAdelia == 1) {
                $isNetVpnFinal = '1';
            } else {
                $isNetVpnFinal = '';
            }

            $arrMatricePrio = $oceaneAssistant->getMatricePrioGenerique($idJeuParam, $totalClients, 'TYPE1', $isClientEntreprise, false, $isNetVpnFinal);


            $idValeurImpactPreconise = $this->astroIhmSqlRepository->getIdValeurConfirmerIncidentByChampAndLibelle($idJeuParam, 'NATURE_IMPACT_CLIENT', $informerClient['libelle_impact_client']);

            $presenceGtr = $this->app->get('Airele')->getImpactByAireleDSLAM($astroSession['id1']);
            $gtr = in_array('GTRS1', $presenceGtr) || in_array('GTRS2', $presenceGtr);


            if ($gtr && strtolower($informerClient['label']) == "coupure franche"){
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

            $this->getOceane->getOceaneData($ticketId,  $this->loginId);
            $clasite  =  $this->getOceane->getClasitePrio();
            $prioClasite = ($type == 'S-SUP') ? $this->astroRepository->getPrioByCalsite($clasite) : '-';
            $dataAdelia = $this->adeliaRepository->getDataBlob($astroId);
            $maestroValide = (strlen($dataAdelia['BLOBDATA']) > 0) ? 1 : 0;


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
            );
        }
    }

    /**
     * Refactored: Simplification et extraction des traitements répétitifs
     */
    private function parseTypePrio($data, $typeKey = 'TYPE_PRIO')
    {
        foreach ($data as $k => $value) {
            if (!is_null($value[$typeKey])) {
                $explodeData = explode(' ', $value[$typeKey]);
                $type = $explodeData[0];
                $explodeDataValue = preg_split('/(?=\d)/', $explodeData[1], 2);
                $operator = $explodeDataValue[0];
                $operatorValue = $explodeDataValue[1];
            } else {
                $type = null;
                $operator = null;
                $operatorValue = null;
            }
            $data[$k]['TYPE'] = $type;
            $data[$k]['OPERATOR'] = $operator;
            $data[$k]['OPERATOR_VALUE'] = $operatorValue;
        }
        return $data;
    }

    private function parseTypeSeuil($data)
    {
        return $this->parseTypePrio($data, 'TYPE_SEUIL');
    }

    /**
     * Récupère et prépare toutes les données liées au ticket
     */
    private function recupererDonneesTicket(string $ticketId, string $typeRessource, bool $api, $assemblee): array
    {
        if(is_null($assemblee)) {
            $assemblee = $this->analyseService->getNomAssemblee($typeRessource, $ticketId);
        }

        $analyseImpact = $this->app
            ->get('AnalyseImpact')
            ->getAnalyseImpactTransEquipement($typeRessource, $ticketId);
        $troncon = $analyseImpact['analyse_impact_session']['troncon_id'];

        $retourCountByService = $this->airelle
            ->getCountByService(
                $typeRessource,
                $ticketId,
                $this->sessId,
                $troncon,
                $assemblee,
                $api
            );

        return [
            'assemblee'            => $assemblee,
            'analyse_impact'       => $analyseImpact,
            'troncon'              => $troncon,
            'count_by_service_raw' => $retourCountByService,
        ];
    }

    public function preconisationPrioriteTrans($ticketId, $idBandeau, $typeRessource, $api = false, $assemblee = null)
    {
        $sansDone = $interrumpuDone = $degradeDone = $decDone = false;
        $decStat = true;
        $idJeuParam = $this->astroRepository->getJeuParamByBandeauFonction($idBandeau, 'CONFIRMER_TRANS');
        $listChamps = $this->app->get('AdminConfirmerRepository')->getListeChampsTrans($idJeuParam);
        $idChampJeuParam = null;
        foreach ($listChamps as $value) {
            if (key_exists('CODE', $value) && $value['CODE'] == 'PRIORITE') {
                $idChampJeuParam = $value['ID_CHAMP_JEU_PARAM'];
                break;
            }
        }
        $codeJeu = $this->app->get('ValeurChampJeuParamRepository')->getCodeJeu($idChampJeuParam);
        $arrayPrioriteTrans = [
            'service_interrompu' => '-',
            'service_degrade' => '-',
            'sans_perturbation_service' => '-'
        ];
        $interrumpuData = $this->parseTypePrio($this->app->get('ChampJeuParamRepository')->recupererPrioriteInterrumpu($codeJeu));
        $degradeData = $this->parseTypePrio($this->app->get('ChampJeuParamRepository')->recupererPrioriteDegrade($codeJeu));
        $sansData = $this->parseTypePrio($this->app->get('ChampJeuParamRepository')->recupererPrioriteSans($codeJeu));
        $decData = $this->parseTypeSeuil($this->app->get('ChampJeuParamRepository')->recupererSeuilData($codeJeu));

        $donneesTicket = $this->recupererDonneesTicket($ticketId, $typeRessource, $api, $assemblee);
        $troncon               = $donneesTicket['troncon'];
        $retourCountByService  = $donneesTicket['count_by_service_raw'];


        $countByService = $retourCountByService['count_by_service'] ?? [];
        $isAssemblee = $retourCountByService['is_assemblee'] ?? false;
        $isEquipementTrans = $retourCountByService['is_equipement_trans'] ?? false;
        if (!$isAssemblee && !$isEquipementTrans) {
            $countByService['troncon_id'] = $troncon;
        }
        $countByService['impact_result'] = $countByService['result'];
        $today = new \DateTime();
        $valToday = $today->format('d/m/Y H:i');
        $isHno = $this->app->get('AstroBase')->checkHno($valToday);
        $dataPrioImpact = $countByService;
        $dataPrioImpact['HNO'] = $isHno ? 'HNO' : 'HO';
        if (is_array($dataPrioImpact) && !empty($dataPrioImpact) && key_exists('impact_result', $dataPrioImpact)) {
            if (key_exists('VoIP', $dataPrioImpact['impact_result'])) {
                unset($dataPrioImpact['impact_result']['VoIP']);
            }
        }
        if (!is_null($countByService) && ((key_exists('gtrs1', $countByService) && $countByService['gtrs1']) || (key_exists('gtrs2', $countByService) && $countByService['gtrs2']))) {
            $dataPrioImpact['gtr_final'] = 'oui';
        } elseif (!is_null($dataPrioImpact) && key_exists('impact_result', $dataPrioImpact)) {
            $dataPrioImpact['gtr_final'] = 'non';
        }
        $dataPrioImpact['impact_result']['TOTAL'] = (is_array($dataPrioImpact) && !empty($dataPrioImpact) && key_exists('impact_result', $dataPrioImpact)) ? array_sum($dataPrioImpact['impact_result']) : 0;
        // Initialisation des services à 0 si non présents
        foreach ([
            'Internet', 'NETVPN', 'LL=2M', 'LL>2M', 'TDSL', 'T2'
        ] as $service) {
            if (!isset($dataPrioImpact['impact_result'][$service])) {
                $dataPrioImpact['impact_result'][$service] = 0;
            }
        }
        $arrayDeclencher = $dataPrioImpact['impact_result'] ?? [];
        // Nettoyage VoIP
        if (isset($arrayDeclencher['VoIP'])) {
            unset($arrayDeclencher['VoIP']);
        }
        // Calcul DEC
        if (!is_null($dataPrioImpact) && key_exists('impact_result', $dataPrioImpact)) {
            foreach ($arrayDeclencher as $k => $v) {
                foreach ($decData as $value2) {
                    if (($k == $value2['TYPE'] || $value2['TYPE'] == '_TOTAL') && !$decDone) {
                        $op = $value2['OPERATOR'];
                        $val = intval($value2['OPERATOR_VALUE']);
                        $gtr = $value2['GTR'] ?? null;
                        $gtrOk = is_null($gtr) || (key_exists('gtr_final', $dataPrioImpact) && $dataPrioImpact['gtr_final'] == $gtr);
                        if ($op == '>=') {
                            if ($v >= $val && $gtrOk && !$decDone) {
                                $decStat = true;
                                $decDone = true;
                            } else {
                                $decStat = false;
                            }
                        } elseif ($op == '<=') {
                            if ($v <= $val && $gtrOk && !$decDone) {
                                $decStat = true;
                                $decDone = true;
                            } else {
                                $decStat = false;
                            }
                        }
                    } elseif (is_null($value2['TYPE']) && !is_null($value2['GTR'])) {
                        if (key_exists('gtr_final', $dataPrioImpact) && $dataPrioImpact['gtr_final'] == $value2['GTR'] && !$decDone) {
                            $decStat = true;
                            $decDone = true;
                        } else {
                            $decStat = false;
                        }
                    } elseif (is_null($value2['TYPE']) && is_null($value2['GTR']) && !$decDone) {
                        $decStat = true;
                        $decDone = true;
                    }
                }
            }
        }
        // Traitement des priorités (extraction en méthode privée possible pour DRY)
        $arrayPrioriteTrans['sans_perturbation_service'] = $this->getPrioriteFromData($dataPrioImpact, $sansData, $sansDone);
        $arrayPrioriteTrans['service_degrade'] = $this->getPrioriteFromData($dataPrioImpact, $degradeData, $degradeDone);
        $arrayPrioriteTrans['service_interrompu'] = $this->getPrioriteFromData($dataPrioImpact, $interrumpuData, $interrumpuDone);
        return [
            'array_priorite_trans' => $arrayPrioriteTrans,
            'dec_state' => $decStat,
            'dec_done' => $decDone
        ];
    }

    /**
     * Factorisation du traitement des priorités
     */
    private function getPrioriteFromData($dataPrioImpact, $data, &$doneFlag)
    {
        if ($doneFlag || is_null($dataPrioImpact) || !key_exists('impact_result', $dataPrioImpact)) {
            return '-';
        }
        foreach ($dataPrioImpact['impact_result'] as $k => $v) {
            foreach ($data as $value2) {
                if ($doneFlag) break;
                if ($k == $value2['TYPE'] || $value2['TYPE'] == '_TOTAL') {
                    $op = $value2['OPERATOR'];
                    $val = intval($value2['OPERATOR_VALUE']);
                    $gtr = $value2['GTR'] ?? null;
                    $hno = $value2['HNO'] ?? null;
                    $prio = $value2['PRIORITE'] ?? null;
                    $hnoOk = is_null($hno) || (key_exists('HNO', $dataPrioImpact) && $dataPrioImpact['HNO'] == $hno);
                    $gtrOk = is_null($gtr) || (key_exists('gtr_final', $dataPrioImpact) && $dataPrioImpact['gtr_final'] == $gtr);
                    if ($op == '>=') {
                        if ($v >= $val && $gtrOk && $hnoOk) {
                            $doneFlag = true;
                            return 'P' . $prio;
                        }
                    } elseif ($op == '<=') {
                        if ($v <= $val && $gtrOk && $hnoOk) {
                            $doneFlag = true;
                            return 'P' . $prio;
                        }
                    }
                } elseif (is_null($value2['TYPE']) && !is_null($value2['GTR'])) {
                    $gtr = $value2['GTR'];
                    $hno = $value2['HNO'] ?? null;
                    $prio = $value2['PRIORITE'] ?? null;
                    $hnoOk = is_null($hno) || (key_exists('HNO', $dataPrioImpact) && $dataPrioImpact['HNO'] == $hno);
                    if (key_exists('gtr_final', $dataPrioImpact) && $dataPrioImpact['gtr_final'] == $gtr && $hnoOk) {
                        $doneFlag = true;
                        return 'P' . $prio;
                    }
                } elseif (is_null($value2['TYPE']) && is_null($value2['GTR'])) {
                    $hno = $value2['HNO'] ?? null;
                    $prio = $value2['PRIORITE'] ?? null;
                    $hnoOk = is_null($hno) || (key_exists('HNO', $dataPrioImpact) && $dataPrioImpact['HNO'] == $hno);
                    if ($hnoOk) {
                        $doneFlag = true;
                        return 'P' . $prio;
                    }
                }
            }
        }
        return '-';
    }
    public function getSeuilsAdelia($idRessource, $idAdelia ,$data,$compteMachine){

        $resultDslam = $this->maestroRepository->getRessource($idRessource);

        $adeliaData = $this->globalApiService->getUrlApi('ADELIA');
        $connexionData = $this->globalApiService->getUrlApi('CONNEXION');
        $adeliaData['cuid'] = $compteMachine;
        $adeliaData['nom'] = 'HBM';
        $adeliaData['prenom'] = 'HBM';
        $restAdelia = new \Hbm\Globalapi\Service\Rest\Adelia($connexionData, $adeliaData, true);
        $result = $restAdelia->getDerangementById($idAdelia);
        $resultPourSimulate = json_decode($result);
        $dataAdeliaSaved = array();
        $dataArr['dslamName'] = $resultDslam['DSLAM'];
        $dataArr['description'] = $resultPourSimulate->description;
        $dataArr['impactNature'] = $resultPourSimulate->impactNature;
        $dataArr['troubleTicketNumber'] = $resultPourSimulate->troubleTicketNumber;
        $dataArr['plannedEndDate'] = $resultPourSimulate->plannedEndDate;
        $dataArr['beginDate'] = $resultPourSimulate->beginDate;
        $dataArr['sourceEntity'] = $resultPourSimulate->sourceEntity;

        $resultSimulate = $restAdelia->simulateDslam($dataArr);
        $this->getOceane->getOceaneData($data['TICKETOCEANEID'],  $this->loginId);

        $dataAdeliaArraySimulate = json_decode($resultSimulate);
        $dataAdeliaSavedFirst = $this->adeliaService->saveAdeliaDataFirst( true,$dataAdeliaArraySimulate, $data['ID_TICKET_ASTRO']);

        if (!is_null($result)) {
            $dataAdeliaArray = json_decode($result);
            $dataAdeliaSaved = $this->adeliaService->saveAdeliaData($dataAdeliaArray, $data['ID_TICKET_ASTRO'],array(),true);

        }
        $detectionDate = $this->getOceane->getDetectionDate();
        $dateSeuilGrave = ($detectionDate != null) ? $this->adeliaService->getDateSeuil($detectionDate, $dataAdeliaSaved['SEUIL_GRAVE']) : '-';
        $dateSeuilMajeur = ($detectionDate != null) ? $this->adeliaService->getDateSeuil($detectionDate, $dataAdeliaSaved['SEUIL_MAJEUR']) : '-';

        $dateSeuilGrave = str_replace('à', '', $dateSeuilGrave);
        $dateSeuilMajeur = str_replace('à', '', $dateSeuilMajeur);

        return array(
            'seuil_grave' => $dateSeuilGrave,
            'seuil_majeur' => $dateSeuilMajeur
        );
    }

}

