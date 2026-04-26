<?php

namespace App\Service;

use App\Tools\OceaneTools;
use Hbm\Globalapi\Service\Rest\ApiOceane;
use Hbm\Globalapi\Service\Soap\OceaneUpd;
use Hbm\Globalapi\Service\Soap\OceaneFg;
use Hbm\Globalapi\Service\Rest\Oceane;
use Hbm\Common\Tools\StringTools;
use \Oft\Mvc\Application;
use App\Tools\OceaneAssistant;

class OceaneService extends AstroBaseService
{

    /** @var $globalApiRepository \App\Repository\GlobalApiRepository */
    protected $globalApiRepository;

    /** @var $globalApiUrlService \App\Service\GlobalApiUrlService */
    protected $globalApiUrlService;

    protected $app;

    protected $astroIhmSqlRepository;

    protected $sessId;

    protected $getapeService;

    protected $loginId;

    /**
     * @var GlobalApiUrlService
     */
    protected $globalApiService;

    public function __construct(Application $app)
    {
        $this->app = $app;
        $this->globalApiService = $this->app->get('GlobalApiUrlService');
        $this->globalApiRepository = $app->get('GlobalApiRepository');
        $this->globalApiUrlService = $app->get('GlobalApiUrlService');
        $this->astroIhmSqlRepository = $app->get('AstroIhmSqlRepository');
        $this->globalApiRepository = $app->get('GlobalApiRepository');
        $this->getapeService = $this->app->get('Gatape');
    }

    /**
     * Retourner les informations pour F&G
     *
     * @param string $ticketId
     * @return array
     */
    public function findAndGetOceane($ticketId, $connectedEds = null)
    {
        $oceaneAssistant = new OceaneAssistant($this->app);

        $status = null;
        $natureFinale = null;
        $priority = null;
        $lbSuccint = null;
        $troubleCauseCodeCategory = null;
        $troubleType = null;
        $typeRessource = '';
        $libelleTechnique = '';
        $description = '';
        $causeDepassementDelai = '';
        $codeDetecteur = '';
        $libelleImputation = '';
        $detailProbleme = '';
        $ressource = '';
        $drDate = '';
        $type = '';
        $edsActif = $edsActifNiveau2 = '';
        $actif = 0;
        $clasitePrio = null;
        $edsActifNiveau2 = '';
        $posteAssocie = '';
        $connexionData = $this->globalApiUrlService->getUrlApi('CONNEXION');
        $findAndGet = $this->globalApiUrlService->getUrlApi('OCEANE_FG');
        $findAndGetResult = new OceaneFg($connexionData, $findAndGet);
        $data = '';
        $message = '';
        $actionEnCours = '';
        $dateActionEnCours = '';
        $edsActionEnCours = '';
        $hno = 0;
        $evtIncident = '';
        $champComplementaire4 = '';
        $aacquitte = 0;


        try {
            $result = $findAndGetResult->getResponseFindandGetTroubleTicket($ticketId);

            if (property_exists($result, 'faultstring') && $result->faultstring != '') {
                $message = $result->faultstring . ' ' . $result->faultcode;
            } elseif (property_exists($result, 'returnedRecordsNumber') && $result->returnedRecordsNumber == 0) {
                $message = 'Ticket ' . $ticketId . ' est inexistant dans océane !';
            } elseif (property_exists($result->TroubleTicketResponse, 'TroubleTicketResponse')) {
                $troubleTicketResponse = $result->TroubleTicketResponse->TroubleTicketResponse;

                if (property_exists($troubleTicketResponse->InstalledResource, 'Parameters') && property_exists($troubleTicketResponse->InstalledResource->Parameters, 'Parameter')) {
                    foreach ($troubleTicketResponse->InstalledResource->Parameters->Parameter as $val1) {
                        if (property_exists($val1, 'id') && 'CLASITE' == $val1->id) {
                            $clasitePrio = $val1->value;
                            break;
                        }
                    }
                }
                $startDate = $troubleTicketResponse->TroubleTicketStatus->StartDate;
                $fgDate = $troubleTicketResponse->creationDate;
                $troubleDetectionDate = $troubleTicketResponse->troubleDetectionDate;
                $installedResource = $troubleTicketResponse->InstalledResource;
                $installedService = $troubleTicketResponse->InstalledService;
                $rdPlus = $troubleTicketResponse->local_nbdrgclo;
                $category = $troubleTicketResponse->troubleTicketCategory;
                $driDate = property_exists($troubleTicketResponse, 'requestedRestorationDate') ? $troubleTicketResponse->requestedRestorationDate : '';
                $drcDate = property_exists($troubleTicketResponse, 'plannedRestorationDate') ? $troubleTicketResponse->plannedRestorationDate : '';
                $troubleSeverity = property_exists($troubleTicketResponse, 'troubleSeverity') ? $troubleTicketResponse->troubleSeverity : '';
                $ticketAdelia = '';
                $simulationMaestro = 'n';

                if (property_exists($troubleTicketResponse->TroubleTicketStatus, 'statusCode')) {
                    $status = StringTools::convertEncoding($troubleTicketResponse->TroubleTicketStatus->statusCode, 'ISO-8859-15', 'UTF-8');
                }
                if (property_exists($troubleTicketResponse, 'local_ComplementaryField')) {

                    if (is_array($troubleTicketResponse->local_ComplementaryField)) {
                        if (array_key_exists('3', $troubleTicketResponse->local_ComplementaryField) && isset($troubleTicketResponse->local_ComplementaryField[3]->value)) {

                            $champComplementaire4 = $troubleTicketResponse->local_ComplementaryField[3]->value;

                            if ($troubleTicketResponse->local_ComplementaryField[3]->value == "" && is_array($troubleTicketResponse->InstalledResource->ResourceSpecCharacteristic)) {
                                $ressource = $troubleTicketResponse->InstalledResource->ResourceSpecCharacteristic[0]->InstalledResourceCharValue->resourceCharacteristicValue;
                            } else {
                                $ressource = $troubleTicketResponse->local_ComplementaryField[3]->value;
                            }
                        }

                        if (array_key_exists('2', $troubleTicketResponse->local_ComplementaryField) && isset($troubleTicketResponse->local_ComplementaryField[2]->value)) {
                            $typeRessource = $troubleTicketResponse->local_ComplementaryField[2]->value;
                        }

                        if (array_key_exists('5', $troubleTicketResponse->local_ComplementaryField) && isset($troubleTicketResponse->local_ComplementaryField[5]->value)) {
                            $libelleTechnique = $troubleTicketResponse->local_ComplementaryField[5]->value;
                        }

                        if (array_key_exists('4', $troubleTicketResponse->local_ComplementaryField) && isset($troubleTicketResponse->local_ComplementaryField[4]->value)) {
                            $codeDetecteur = $troubleTicketResponse->local_ComplementaryField[4]->value;
                        }

                    }
                }

                if (property_exists($troubleTicketResponse, 'troubleTicketPriority')) {
                    $priority = StringTools::convertEncoding($troubleTicketResponse->troubleTicketPriority, 'ISO-8859-15', 'UTF-8');
                }

                if (property_exists($troubleTicketResponse, 'description')) {
                    $description = $troubleTicketResponse->description;
                }
                if (property_exists($troubleTicketResponse, 'local_ShortLabel')) {
                    $lbSuccint = $troubleTicketResponse->local_ShortLabel;
                }
                if (property_exists($troubleTicketResponse, 'TroubleCause')) {
                    if (property_exists($troubleTicketResponse->TroubleCause, 'local_internalcomplement')) {
                        $causeDepassementDelai = $troubleTicketResponse->TroubleCause->local_internalcomplement;
                    }
                    if (property_exists($troubleTicketResponse->TroubleCause, 'troubleCauseCodeCategory')) {
                        $natureFinale = StringTools::convertEncoding($troubleTicketResponse->TroubleCause->troubleCauseCodeCategory, 'ISO-8859-15', 'UTF-8');
                    }
                    if (property_exists($troubleTicketResponse->TroubleCause, 'troubleCauseLabel')) {
                        $libelleImputation = $troubleTicketResponse->TroubleCause->troubleCauseLabel;
                    }
                    if (property_exists($troubleTicketResponse->TroubleCause, 'troubleCauseDescription')) {
                        $detailProbleme = StringTools::convertEncoding($troubleTicketResponse->TroubleCause->troubleCauseDescription, 'ISO-8859-1', 'UTF-8');
                    }
                    if (property_exists($troubleTicketResponse->TroubleCause, 'troubleCauseCodeCategory')) {
                        $troubleCauseCodeCategory = StringTools::convertEncoding($troubleTicketResponse->TroubleCause->troubleCauseCodeCategory, 'ISO-8859-1', 'UTF-8');
                    }
                }

                if (property_exists($troubleTicketResponse, 'troubleType')) {
                    $troubleType = StringTools::convertEncoding($troubleTicketResponse->troubleType, 'ISO-8859-1', 'UTF-8');
                }

                $partyRole = $troubleTicketResponse->PartyRole;

                foreach ($partyRole as $value) {
                    if ($posteAssocie == '') {
                        $posteAssocie = (!empty($value->Party) && isset($value->Party->Local_occupationCode)) ? $value->Party->Local_occupationCode : '';
                    }

                    if (!is_null($connectedEds) && $value->partyRoleType == "TroubleResolutionContributor" && property_exists($value, 'Local_PartyIntervention') && is_array($value->Local_PartyIntervention->interventionStatus)) {
                        $interventionStatus = ($value->Local_PartyIntervention->interventionStatus[0]->status == "Requested" &&
                            $value->Local_PartyIntervention->interventionStatus[1]->status == "Accepted");
                        if (key_exists(2, $value->Local_PartyIntervention->interventionStatus)) {
                            $interventionStatus = $value->Local_PartyIntervention->interventionStatus[2]->status != 'Completed';
                        }

                        if ($value->Local_PartyIntervention->level == 1 && $interventionStatus && $value->PartyRoleSet->partyRoleSetID == $connectedEds) {
                            $actif = 1;
                            $edsActif = $value->PartyRoleSet->partyRoleSetID;
                            break;
                        } elseif ($value->Local_PartyIntervention->level == 2 && $interventionStatus && $value->PartyRoleSet->partyRoleSetID == $connectedEds) {
                            $actif = 1;
                            $edsActifNiveau2 = $value->PartyRoleSet->partyRoleSetID;
                            break;
                        }
                    }
                    foreach ($partyRole as $value) {

                        if (!is_null($connectedEds) && $value->partyRoleType == "TroubleResolutionContributor" && property_exists($value, 'Local_PartyIntervention') && is_object($value->Local_PartyIntervention->interventionStatus) && !property_exists($value->Local_PartyIntervention->interventionStatus, 'interventionStatus')) {
                            if ($value->Local_PartyIntervention->interventionStatus->status == 'Requested') {
                                $aacquitte = 1;
                                break;
                            }
                        }
                    }
                }

                $niveauUrgence = property_exists($troubleTicketResponse, 'troubleUrgency') ? $troubleTicketResponse->troubleUrgency : '';

                if ($driDate != '' && $drcDate != '') {
                    $type = "DRI / DRC";
                    $drDate = OceaneTools::changeUTCToDate('d/m/Y H:i', $drcDate);
                } elseif ($drcDate != '') {
                    $type = "DRC";
                    $drDate = OceaneTools::changeUTCToDate('d/m/Y H:i', $drcDate);
                } elseif ($driDate != '') {
                    $type = "DRI";
                    $drDate = OceaneTools::changeUTCToDate('d/m/Y H:i', $driDate);
                }
                $checkInc = false;
                $checkIncAct = false;
                $checkIncDate = false;

                if (property_exists($troubleTicketResponse, 'PartyRole')) {
                    $countArr = count($troubleTicketResponse->PartyRole);
                    $inc = range(0, $countArr);
                    foreach ($inc as $i) {
                        if (!$checkInc) {
                            if (key_exists($i, $troubleTicketResponse->PartyRole) && property_exists($troubleTicketResponse->PartyRole[$i], 'PartyRoleSet')
                                && property_exists($troubleTicketResponse->PartyRole[$i], 'partyRoleType') && $troubleTicketResponse->PartyRole[$i]->partyRoleType == 'TroubleResolutionLeader') {
                                if (property_exists($troubleTicketResponse->PartyRole[$i]->PartyRoleSet, 'local_groupactioninprogress')) {
                                    $checkIncAct = true;
                                    $actionEnCours = $troubleTicketResponse->PartyRole[$i]->PartyRoleSet->local_groupactioninprogress;
                                    $edsActionEnCours = $troubleTicketResponse->PartyRole[$i]->PartyRoleSet->partyRoleSetID;

                                }
                                if (property_exists($troubleTicketResponse->PartyRole[$i]->PartyRoleSet, 'local_groupactioninprogressdate')) {
                                    $checkIncDate = true;
                                    $dateActionEnCours = $troubleTicketResponse->PartyRole[$i]->PartyRoleSet->local_groupactioninprogressdate;
                                    $edsActionEnCours = $troubleTicketResponse->PartyRole[$i]->PartyRoleSet->partyRoleSetID;
                                }
                                if ($checkIncDate && $checkIncAct) {
                                    $checkInc = true;
                                }
                                break;
                            }
                        }
                    }
                }
                if (property_exists($troubleTicketResponse, 'local_onbhfollowup')) {
                    $hno = 1;
                }

                if (property_exists($troubleTicketResponse, 'troubleTicketCategory')) {
                    $evtIncident = $troubleTicketResponse->troubleTicketCategory;
                }

                $data = array(
                    'fg_date' => $fgDate,
                    'installed_resource' => $installedResource,
                    'rd_plus' => $rdPlus,
                    'status' => $status,
                    'start_date' => $startDate,
                    'nature_finale' => $natureFinale,
                    'trouble_detection_date' => $troubleDetectionDate,
                    'trouble_ticket_response' => $troubleTicketResponse,
                    'ressource' => $ressource,
                    'type_ressource' => $typeRessource,
                    'libelle_technique' => $libelleTechnique,
                    'description' => $description,
                    'code_detecteur' => $codeDetecteur,
                    'priority' => $priority,
                    'category' => $category,
                    'lb_succint' => $lbSuccint,
                    'detail_probleme' => $detailProbleme,
                    'trouble_type' => $troubleType,
                    'trouble_severity' => $troubleSeverity,
                    'dr_date' => $drDate,
                    'type' => $type,
                    'trouble_cause_code_category' => $troubleCauseCodeCategory,
                    'troubleDetectionDate' => $troubleDetectionDate,
                    'libelle_imputation' => $libelleImputation,
                    'actif' => $actif,
                    'cause_depassement_delai' => $causeDepassementDelai,
                    'eds_actif' => $edsActif,
                    'ticket_adelia' => $ticketAdelia,
                    'simulation_maestro' => $simulationMaestro,
                    'clasite_prio' => $clasitePrio,
                    'drc_date' => $drcDate,
                    'dri_date' => $driDate,
                    'eds_actif_niveau2' => $edsActifNiveau2,
                    'trouble_detection_date_formatted' => $oceaneAssistant->changeUTCToDate($troubleDetectionDate),
                    'niveau_urgence' => $niveauUrgence,
                    'poste_associe' => $posteAssocie,
                    'installed_service' => $installedService,
                    'action_en_cours' => $actionEnCours,
                    'date_action_en_cours' => $dateActionEnCours,
                    'eds_action_en_cours' => $edsActionEnCours,
                    'is_hno' => $hno,
                    'type_ticket' => $evtIncident,
                    'champ_complementaire3' => $typeRessource,
                    'champ_complementaire4' => $champComplementaire4,
                    'aacquitter' => $aacquitte
                );
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

    /**
     * check oceane
     *
     * @param string $ticketId
     * @return array
     */
    public function checkOceane($ticketId)
    {
        $oceaneApiData = $this->app->get('GlobalApiUrlService')->getUrlApi('API_OCEANE');
        $token = $this->app->get('Gatape')->getToken($oceaneApiData, 'inside');
        $this->loginId = (key_exists('api', $this->app->config) && $this->app->config['api']) ? $this->getLogin() : $this->app->get('Session')->getUtilisateurLogin();
        $headerConfig = array(
            "X-Client-User-Id: $this->loginId",
            "X-HTTP-Method-Override: PATCH"
        );
        $oceaneApi = new Oceane($token, $headerConfig);
        return json_decode($oceaneApi->getFlux($oceaneApiData['url'], $ticketId));

    }

    /**
     *
     * @param array $data
     * @param string $tag
     * @return string
     */
    public function updateOceane($data, $tag,$loginUser='')
    {

        $values = array();
        $maxImapct = 100; // Max Impact autorisé par request
        $this->hbmLogin = 'MMMM0425';
        $this->getapeService = $this->app->get('Gatape');
        $oceaneApiData = $this->globalApiService->getUrlApi('API_OCEANE');
        $token = $this->getapeService->getToken($oceaneApiData, 'inside');
        $login = $this->app->get('Session')->getUtilisateurLogin();

        $headerConfig = array(
            "X-Client-User-Id: $login",
            "X-HTTP-Method-Override: PATCH"
        );
        $oceaneApi = new Oceane($token, $headerConfig);

        if (array_key_exists('trouble_ticket_priority', $data) && isset($data['trouble_ticket_priority'])) {
            $values['TROUBLE_TICKET_PRIORITY'] = intval($data['trouble_ticket_priority']);
        } else {
            $values['TROUBLE_TICKET_PRIORITY'] = '0';
        }
        if (array_key_exists('ticket_id', $data) && isset($data['ticket_id'])) {
            $values['ticketId'] = $data['ticket_id'];
        }

        if (array_key_exists('astroid', $data) && isset($data['astroid'])) {
            $values['astroid'] = $data['astroid'];
        }

        if (array_key_exists('party_role_party_ID', $data) && isset($data['party_role_party_ID'])) {
            $values['PARTYROLE_PARTY_ID'] = $data['party_role_party_ID'];
        }

        if (array_key_exists('postes_associe', $data) && isset($data['postes_associe'])) {
            $values['POSTE_ASSOCIE_ID'] = $data['postes_associe'];
        }

        if (array_key_exists('niv_urgence', $data) && isset($data['niv_urgence'])) {
            $values['NIV_URGENCE_ID'] = $data['niv_urgence'];
        }

        if (array_key_exists('action_eds', $data) && isset($data['action_eds'])) {
            $values['ACTION_EDS_IN_PROGRESS'] = $data['action_eds'];
        }

        if (array_key_exists('commentaire_eds', $data) && isset($data['commentaire_eds'])) {
            $values['LOCAL_COMEMENTAIRE'] = $data['commentaire_eds'];
        }

        if (array_key_exists('eds_pilote', $data) && isset($data['eds_pilote'])) {
            $values['EDS_PILOTE'] = $data['eds_pilote'];
        }
        $values['party_id'] = $login;

        switch ($tag) {

            // Mise à jour de la priorité avec commentaire
            case 'MAJ_PRIORITE_COMMENTAIRE':

                if (array_key_exists('local_commentaire', $data) && isset($data['local_commentaire'])) {
                    $values['LOCAL_COMEMENTAIRE'] = $data['local_commentaire'];
                }
                if (array_key_exists('nb_plaintes', $data) && isset($data['nb_plaintes'])) {
                    $values['LOCAL_SIGNALISATION_NUMBER'] = intval($data['nb_plaintes']);
                }
                $result = json_decode($oceaneApi->updateMobileMajPrioriteCommentaire($oceaneApiData['url'], $values['ticketId']), true);
                json_decode($oceaneApi->ajoutCommentaireMobile($oceaneApiData['url'], $values), true);
                break;

            // Mise à jour des ressources
            case 'MAJ_PRIORITE_IMPACT_RESSOURCES':

                if (array_key_exists('description', $data) && isset($data['description'])) {
                    $values['DESCRIPTION'] = StringTools::convertEncoding($data['description'], 'ISO-8859-15', 'UTF-8');
                }
                if (array_key_exists('trouble_type', $data) && isset($data['trouble_type'])) {
                    $values['TROUBLE_TYPE'] = $data['trouble_type'];
                }
                if (array_key_exists('trouble_severity', $data) && isset($data['trouble_severity'])) {
                    $values['TROUBLE_SEVERITY'] = $data['trouble_severity'];
                }
                if (array_key_exists('party_set_ID', $data) && isset($data['party_set_ID'])) {
                    $values['PARTY_SET_ID'] = $data['party_set_ID'];
                }

                if (array_key_exists('requested_date', $data) && isset($data['requested_date'])) {
                    $values['REQUESTED_DATE'] = $data['requested_date'];
                    $requestedDate = strtotime($data['requested_date']);
                    $values['requestedRestorationDateZulu'] = gmdate('Y-m-d\TH:i:s\Z', $requestedDate);
                }
                $values['cellules'] = $data['cellules'];
                $nbCellules = count($values['cellules']);
                // Augmenter la taille du timeout pour eviter l'erreur verrou du ticket après déppassemnt du délai
                ini_set('default_socket_timeout', 60);

                if ($nbCellules <= $maxImapct) {
                    $this->app->get('TraceRepository')->setTrace($values['astroid'], "QUALIFIER OCEANE ENVOI ALL_CELLULES", $values, $this->app->get('Session')->getUtilisateurId(), $values['ticketId']);
                    $result = json_decode($oceaneApi->updateMobileImpactRessources($oceaneApiData['url'], $values['ticketId'], $values , true), true);
                    json_decode($oceaneApi->ajoutCommentaireMobile($oceaneApiData['url'], $values), true);
                    $this->app->get('TraceRepository')->setTrace($values['astroid'], "QUALIFIER OCEANE REPONSE ALL_CELLULES", $result, $this->app->get('Session')->getUtilisateurId(), $values['ticketId']);
                } else {
                    $cellulesArrays = array_chunk($values['cellules'], $maxImapct, true); // Diviser le nombre de cellules en tableau de $maxImapct éléments
                    foreach ($cellulesArrays as $key => $arrMaxCellues) {
                        sleep(5);
                        $values['cellules'] = $arrMaxCellues;
                        $this->app->get('TraceRepository')->setTrace($values['astroid'], "QUALIFIER OCEANE ENVOI FLUX_RESTANT" . ($key + 1), $values, $this->app->get('Session')->getUtilisateurId(), $values['ticketId']);
                        $result = json_decode($oceaneApi->updateMobileImpactRessourcesAddCells($oceaneApiData['url'], $values['ticketId'], $values , true), true);
                        json_decode($oceaneApi->ajoutCommentaireMobile($oceaneApiData['url'], $values), true);
                        $this->app->get('TraceRepository')->setTrace($values['astroid'], "QUALIFIER OCEANE REPONSE FLUX_RESTANT" . ($key + 1), $result, $this->app->get('Session')->getUtilisateurId(), $values['ticketId']);
                    }

                    $this->app->get('TraceRepository')->setTrace($values['astroid'], "QUALIFIER OCEANE ENVOI", $values, $this->app->get('Session')->getUtilisateurId(), $values['ticketId']);
                    $result = json_decode($oceaneApi->updateMobileImpactRessources($oceaneApiData['url'], $values['ticketId'], $values), true);
                    json_decode($oceaneApi->ajoutCommentaireMobile($oceaneApiData['url'], $values), true);
                    $this->app->get('TraceRepository')->setTrace($values['astroid'], "QUALIFIER OCEANE REPONSE", $result, $this->app->get('Session')->getUtilisateurId(), $values['ticketId']);
                }
                // remettre la valeur par defaut du timeout socket
                ini_set('default_socket_timeout', 30);
                break;

            // Mise à jour de la priorité et l'impact client
            case 'MAJ_PRIORITE_IMPACT':
                if (array_key_exists('description', $data) && isset($data['description'])) {
                    $values['DESCRIPTION'] = StringTools::convertEncoding($data['description'], 'ISO-8859-15', 'UTF-8');
                }
                if (array_key_exists('trouble_type', $data) && isset($data['trouble_type'])) {
                    $values['TROUBLE_TYPE'] = $data['trouble_type'];
                }
                if (array_key_exists('trouble_severity', $data) && isset($data['trouble_severity'])) {
                    $values['TROUBLE_SEVERITY'] = $data['trouble_severity'];
                }
                if (array_key_exists('party_set_ID', $data) && isset($data['party_set_ID'])) {
                    $values['PARTY_SET_ID'] = $data['party_set_ID'];
                }
                $result = json_decode($oceaneApi->updateMobileMajPrioriteImpact($oceaneApiData['url'], $values['ticketId'], $values), true);
                json_decode($oceaneApi->ajoutCommentaireMobile($oceaneApiData['url'], $values), true);
                break;
            default:
                $result = 'Tag non traité';
                break;
        }
        return $result;
    }

    /**
     * @param $data
     * @param $ticketId
     * @param $astroId
     * @param bool $generique
     * @return string
     * @throws \Exception
     */
    public function updateOceaneConfirmer($data, $ticketId, $astroId, $generique = false)
    {
        $oceaneAssistant = new OceaneAssistant($this->app);
        $actifDri = key_exists('actif_dri', $data) ? $data['actif_dri'] : '';
        if (!$generique) {
            $data['nature_impact_client'] = $this->astroIhmSqlRepository->getImpactClientOceane($data['nature_impact_client']);
        }
        $typeConfirmation = (key_exists('hidden_type_confirmation', $data) && !is_null($data['hidden_type_confirmation'])) ? $data['hidden_type_confirmation'] : 'TYPE1';
        $dateRetablissementUTC = $oceaneAssistant->changeDateToUTCZuluoceane($data['date_retablissement']);
        $loginUser = (key_exists('api', $data) && $data['api']) ? $data['compte_machine'] : strtoupper($this->app->get('Session')->getUtilisateurLogin());
        $comments = StringTools::convertEncoding($data['autre_commentaire'], 'ISO-8859-15', 'UTF-8');
        $v = array(
            'description' => $data['description_derangement'],
            'troubleType' => $data['impact_technique'],
            'troubleSeverity' => $data['nature_impact_client'],
            'localCommentLabel' => ($typeConfirmation === 'TYPE2') ? $comments : $this->createComment($data),
            'localCommentPartyID' => $loginUser,
            'partyRolePartyID' => $loginUser,
            'tagHNO' => (key_exists('hno', $data)) ? (bool)$data['hno'] : '0',
            'troubleTicketPriority' => $data['priorite'],
        );
        // Enchainement param OU IHM OU Enchainement LEGACY
        if ($actifDri) {
            $v['requestedRestorationDate'] = $dateRetablissementUTC;
        }

        $this->hbmLogin = $loginUser;
        $this->getapeService = $this->app->get('Gatape');
        $oceaneApiData = $this->globalApiService->getUrlApi('API_OCEANE');
        $token = $this->getapeService->getToken($oceaneApiData, 'inside');

        $headerConfig = array(
            "X-Client-User-Id: $this->hbmLogin",
            "X-HTTP-Method-Override: PATCH"
        );
        $oceaneApi = new Oceane($token, $headerConfig);

        $dataUpdate = array(
            "author" => $loginUser,
            "text" => $v['localCommentLabel'],
            "commentType" => array(
                "id" => "INT"
            ),
            "operationType" => array(
                "id" => 9
            )
        );

        $this->app->get('TraceRepository')->setTrace($astroId, "CONFIRMER OCEANE ENVOI", $v, $this->sessId, $ticketId);
        $result = $oceaneApi->getResponseUpdateGenerique($oceaneApiData['url'], $ticketId, $v);
        $this->app->get('TraceRepository')->setTrace($astroId, "CONFIRMER OCEANE REPONSE ", $result, $this->sessId, $ticketId);

        $this->app->get('TraceRepository')->setTrace($astroId, "ENVOI OCEANE AJOUT COMMENTAIRE CONFIRMER INCIDENT", $dataUpdate, $this->sessId, $ticketId);
        $retourUpdate = json_decode($oceaneApi->ajouterCommentaire($oceaneApiData['url'], $ticketId, $dataUpdate), true);
        $this->app->get('TraceRepository')->setTrace($astroId, "RETOUR OCEANE AJOUT COMMENTAIRE CONFIRMER INCIDENT ", $retourUpdate, $this->sessId, $ticketId);

        return $result;
    }

    /**
     * @param $data
     * @param $ticketId
     * @param $astroId
     * @return string
     * @throws \Exception
     */
    public function updateOceaneConfirmerTrans($data, $ticketId, $astroId)
    {
        $oceaneAssistant = new OceaneAssistant($this->app);
        $actifDri = key_exists('actif_dri', $data) ? $data['actif_dri'] : '';
        $dateRetablissementUTCZulu = $oceaneAssistant->changeDateToUTCZuluoceane($data['date_retablissement']);
        $dateDebutIncidentUTCZulu = $oceaneAssistant->changeDateToUTCZuluoceane($data['date_debut_incident']);
        $loginUser = (key_exists('api', $data) && $data['api']) ? $data['compte_machine'] : strtoupper($this->app->get('Session')->getUtilisateurLogin());
        $confirmTowStep = key_exists('confirm_two_step', $data) ? $data['confirm_two_step'] : 'non';

        $this->getapeService = $this->app->get('Gatape');
        $oceaneApiData = $this->globalApiUrlService->getUrlApi('API_OCEANE');
        $token = $this->getapeService->getToken($oceaneApiData, 'inside');

        $headerConfig = array(
            "X-Client-User-Id: $loginUser",
            "X-HTTP-Method-Override: PATCH"
        );
        $oceaneApi = new ApiOceane($token, $headerConfig);
        $dataUpdate = array(
            'ticketType' => array(
                'id' => 1,
            ),
            'description' => $data['description_derangement'],
            'priority' => array(
                'id' => $data['priorite'],
            ),
            'category' => array(
                'id' => $data['impact_technique'],
            ),
            'criticity' => array(
                'id' => $data['impact_client'],
            ),
            'relatedParty' => array(
                0 => array(
                    'id' => $loginUser,
                    'role' => 'CustomerRepresentative',
                    '@referredType' => 'Individual',
                ),
            ),
            'isONBHFollowupEnable' => (key_exists('hno', $data)) ? intval($data['hno']) : 0,
             "detectionDate" => $oceaneAssistant->changeDateToUTCZuluoceane($data["date_debut_incident"]),

        );
        if ($data['donnee_complementaire'] != '') {
            $dataUpdate['name'] = $data['donnee_complementaire'];
        }
        if (($actifDri == '1') || (key_exists('api', $this->app->config) && $this->app->config['api'])) {
            $dataUpdate['targetRestorationDate'] = $dateRetablissementUTCZulu;
            $dataUpdate['detectionDate'] = $dateDebutIncidentUTCZulu;
        }

        if ($confirmTowStep == 'oui') {
            $dataUpdateFirstStep = array(
                'detectionDate' => $dateDebutIncidentUTCZulu
            );
            $this->app->get('TraceRepository')->setTrace($astroId, "ENVOI OCEANE CONFIRMER TRANS 1 STEP", $dataUpdateFirstStep, $this->sessId, $ticketId);
            $retourUpdate = json_decode($oceaneApi->updateTicket($oceaneApiData['url'], $ticketId, $dataUpdateFirstStep), true);
            $this->app->get('TraceRepository')->setTrace($astroId, "RETOUR OCEANE CONFIRMER TRANS 1 STEP", $retourUpdate, $this->sessId, $ticketId);

            if (key_exists('code', $retourUpdate)) {
                return $retourUpdate;
            } else {
                $this->app->get('TraceRepository')->setTrace($astroId, "ENVOI OCEANE CONFIRMER TRANS 2 STEP", $dataUpdate, $this->sessId, $ticketId);
                $retourUpdate = json_decode($oceaneApi->updateTicket($oceaneApiData['url'], $ticketId, $dataUpdate), true);
                $this->app->get('TraceRepository')->setTrace($astroId, "RETOUR OCEANE CONFIRMER TRANS 2 STEP", $retourUpdate, $this->sessId, $ticketId);
            }
        } else {
            if(!key_exists('api', $data))
            {
                $dataUpdate['detectionDate'] = $dateDebutIncidentUTCZulu;
            }
            $this->app->get('TraceRepository')->setTrace($astroId, "ENVOI OCEANE CONFIRMER TRANS", $dataUpdate, $this->sessId, $ticketId);
            $retourUpdate = json_decode($oceaneApi->updateTicket($oceaneApiData['url'], $ticketId, $dataUpdate), true);
            $this->app->get('TraceRepository')->setTrace($astroId, "RETOUR OCEANE CONFIRMER TRANS", $retourUpdate, $this->sessId, $ticketId);
        }
        return $retourUpdate;
    }

    /**
     * @param $commentaire
     * @param $ticketId
     * @param $astroId
     * @return string
     * @throws \Exception
     */
    public function ajoutCommentaireConfirmerTrans($commentaire, $ticketId, $astroId, $eds = '')
    {
        $loginUser = (key_exists('api', $this->app->config) && $this->app->config['api']) ? $this->app->get('AstroRepository')->getCompteMachine($eds) : strtoupper($this->app->get('Session')->getUtilisateurLogin());

        $this->getapeService = $this->app->get('Gatape');
        $oceaneApiData = $this->globalApiUrlService->getUrlApi('API_OCEANE');
        $token = $this->getapeService->getToken($oceaneApiData, 'inside');

        $headerConfig = array(
            "X-Client-User-Id: $loginUser",
            "X-HTTP-Method-Override: PATCH"
        );
        $dataUpdate = array(
            "author" => $loginUser,
            "text" => $commentaire,
            "commentType" => array(
                "id" => "INT"
            ),
            "operationType" => array(
                "id" => 9
            )
        );

        $oceaneApi = new ApiOceane($token, $headerConfig);
        $this->app->get('TraceRepository')->setTrace($astroId, "ENVOI OCEANE AJOUT COMMENTAIRE CONFIRMER TRANS", $dataUpdate, $this->sessId, $ticketId);
        $retourUpdate = json_decode($oceaneApi->ajouterCommentaire($oceaneApiData['url'], $ticketId, $dataUpdate), true);
        $this->app->get('TraceRepository')->setTrace($astroId, "RETOUR OCEANE AJOUT COMMENTAIRE CONFIRMER TRANS", $retourUpdate, $this->sessId, $ticketId);

        return $retourUpdate;
    }

    public function ajoutNbrClientImpacte($nbrClientImpacte, $ticketId, $astroId, $eds = '')
    {
        $loginUser = (key_exists('api', $this->app->config) && $this->app->config['api']) ? $this->app->get('AstroRepository')->getCompteMachine($eds) : strtoupper($this->app->get('Session')->getUtilisateurLogin());
        $this->getapeService = $this->app->get('Gatape');
        $oceaneApiData = $this->globalApiUrlService->getUrlApi('API_OCEANE');
        $token = $this->getapeService->getToken($oceaneApiData, 'inside');

        $headerConfig = array(
            "X-Client-User-Id: $loginUser",
            "X-HTTP-Method-Override: PATCH"
        );

        $dataAssociation = array(
            'impactedcustomersquantity' => $nbrClientImpacte,
        );
        $oceaneApi = new ApiOceane($token, $headerConfig);

        $this->app->get('TraceRepository')->setTrace($astroId, "ENVOI OCEANE API AJOUT NOMBRE CLIENTS API", $dataAssociation, $this->sessId, $ticketId);
        $retourAssociation = json_decode($oceaneApi->updateTicket($oceaneApiData['url'], $ticketId, $dataAssociation), true);
        $this->app->get('TraceRepository')->setTrace($astroId, "RETOUR OCEANE AJOUT NOMBRE CLIENTS API", $retourAssociation, $this->sessId, $ticketId);

        return $retourAssociation;
    }

    /**
     * @param $data
     * @return string
     */
    public function createComment($data)
    {
        $rc = '&#13;&#10;';
        $data['commentaire_impact_client'] = isset($data['commentaire_impact_client']) ? $data['commentaire_impact_client'] : '';
        $data['priorite_commentaire'] = isset($data['priorite_commentaire']) ? $data['priorite_commentaire'] : '';
        if ($data['priorite_commentaire'] == '') {
            $priorityComment = '# priorité #' . $rc . 'priorité calculée : P' . $data['priorite'] . $rc;
        } else {
            $priorityComment = '# priorité #' . $rc . 'priorité modifiée : P' . $data['priorite'] . $rc;
            if ($data['priorite_commentaire'] == '4') {
                $priorityComment .= ($data['commentaire1']);
            } else {
                $priorityComment .= StringTools::convertEncoding($data['priorite_commentaire'], 'ISO-8859-15', 'UTF-8');
            }
        }
        $data['commentaire_impact_client'] = (key_exists('api', $data) && $data['api']) ? $data['commentaire_impact_client'] : StringTools::convertEncoding($data['commentaire_impact_client'], 'ISO-8859-15', 'UTF-8');
        $autreCommentaire = (key_exists('api', $data) && $data['api']) ? $data['autre_commentaire'] : StringTools::convertEncoding($data['autre_commentaire'], 'ISO-8859-15', 'UTF-8');
        return ($data['commentaire_impact_client']) . ($priorityComment != '' ? $rc . $priorityComment : '') . ($data['autre_commentaire'] != '' ? $rc . $autreCommentaire : '');
    }
    
    /**
     * MAJ le nombre de signalisation
     *
     * @param array $data
     * @return string
     */
    public function updateChampComplementaire($data)
    {
        $values = array(
            'local_signalisation_number' => $data['nb_plantes'],
            'partyRolePartyID' => $data['login']
        );
        $this->hbmLogin = $data['login'];
        $this->getapeService = $this->app->get('Gatape');
        $oceaneApiData = $this->globalApiService->getUrlApi('API_OCEANE');
        $token = $this->getapeService->getToken($oceaneApiData, 'inside');

        $headerConfig = array(
            "X-Client-User-Id: $this->hbmLogin",
            "X-HTTP-Method-Override: PATCH"
        );
        $oceaneApi = new Oceane($token, $headerConfig);

        return json_decode($oceaneApi->getResponseLocalComplementaire($oceaneApiData['url'],$data['ticket_id'], $values), true);
    }

    public function getUserId()
    {
        $cuidlower = $this->app->config['api_data']['cuid']; //ID HBM
        return $this->app->get('IhmUtilisateurRepository')->getByLogin($cuidlower)['ID_UTILISATEUR'];
    }

    public function getResponseTicketClosure($currentStatus, $startDateClosure, $ticketId, $astroId, $arrayData)
    {
        $astroSession = $this->app->get('Session')->get('astroOft' . $ticketId);
        $connectedGroup = key_exists('connectedgroup',$astroSession) ? $astroSession['connectedgroup'] : '';

        $loginUser = (key_exists('api', $this->app->config) && $this->app->config['api']) ? $this->app->get('AstroRepository')->getCompteMachine($connectedGroup) : strtoupper($this->app->get('Session')->getUtilisateurLogin());

        $this->hbmLogin = $loginUser;
        $this->getapeService = $this->app->get('Gatape');
        $oceaneApiData = $this->globalApiService->getUrlApi('API_OCEANE');
        $token = $this->getapeService->getToken($oceaneApiData, 'inside');

        $headerConfig = array(
            "X-Client-User-Id: $this->hbmLogin",
            "X-HTTP-Method-Override: PATCH"
        );
        //3484

        $oceaneApi = new ApiOceane($token, $headerConfig);

        $dataCommentaire = array(
            "author" => $this->hbmLogin,
            "text" => $arrayData['localCommentLabel'],
            "commentType" => array(
                "id" => "INT"
            ),
            "operationType" => array(
                "id" => 9
            )
        );

        $this->app->get('TraceRepository')->setTrace($astroId, "ENVOI OCEANE AJOUT COMMENTAIRE CLOSURE", $dataCommentaire, $this->sessId, $ticketId);
        $retourUpdate = json_decode($oceaneApi->ajouterCommentaire($oceaneApiData['url'], $ticketId, $dataCommentaire), true);
        $this->app->get('TraceRepository')->setTrace($astroId, "RETOUR OCEANE AJOUT COMMENTAIRE CLOSURE", $retourUpdate, $this->sessId, $ticketId);

        $dataAssociation = array(
            "status" => [
                "code" => "Closed",
                "isCurrentStatus" => "true",
                "startDate" => $startDateClosure,
                "reason"=> " "
            ],
            "troubleCause" => [
                [
                    "problemDetail" => [
                        "id" => $arrayData['troubleCauseDescription']
                    ],
                    "problemCategory" => [
                        "id" => $arrayData['troubleCauseCodeCategory']
                    ]
                ]
            ]
        );


        $this->app->get('TraceRepository')->setTrace($astroId, "ENVOI OCEANE API STATUS CLOSURE", $dataAssociation, $this->sessId, $ticketId);
        $retour = json_decode($oceaneApi->updateTicket($oceaneApiData['url'], $ticketId, $dataAssociation), true);
        $this->app->get('TraceRepository')->setTrace($astroId, "ENVOI OCEANE API STATUS CLOSURE", $retour, $this->sessId, $ticketId);

        return (object)$retour;
    }

}
