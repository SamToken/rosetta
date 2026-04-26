<?php

namespace App\Service;

use Hbm\Common\Tools\StringTools;
use Hbm\Globalapi\Service\Rest\ApiOceane;
use Oft\Mvc\Application;
use Zend\Json\Json;
use App\Tools\OceaneTools;


class OceaneGetService
{
    protected $oceaneData = [];

    /**
     * @var GatapeService
     */
    protected $getapeService;

    /**
     * @var Application
     */
    protected $app;

    public function __construct($app)
    {
        $this->app = $app;
        $this->sessId = (key_exists('api', $this->app->config) && $this->app->config['api']) ? $this->getUserId() : $this->app->get('Session')->getUtilisateurId();
        $this->loginId = (key_exists('api', $this->app->config) && $this->app->config['api']) ? $this->getLogin() : $this->app->get('Session')->getUtilisateurLogin();
        $this->getapeService = $this->app->get('Gatape');
    }

    /**
     * Initiatier et récupérer les données d'un ticket Oceane
     * @param $ticketId
     * @param $cuiId
     * @return mixed
     */
    public function getOceaneData($ticketId, $cuiId)
    {
        $oceaneApiData = $this->app->get('GlobalApiUrlService')->getUrlApi('API_OCEANE');
        $token = $this->getapeService->getToken($oceaneApiData, 'inside');
        $astroId = $this->app->get('AstroRepository')->getAstroIdByTicket($ticketId);

        $headerConfig = array(
            "X-Client-User-Id: $cuiId"
        );
        $oceaneApi = new ApiOceane($token, $headerConfig);
        $this->app->get('TraceRepository')->setTrace($astroId, "ENVOI GET OCEANE DATA", $ticketId, $this->sessId, $ticketId);
        $detailTicketJson = $oceaneApi->geDetail($oceaneApiData['url'], $ticketId);
        $this->app->get('TraceRepository')->setTrace($astroId, "RETOUR GET OCEANE DATA", $detailTicketJson, $this->sessId, $ticketId);

        if ($this->app->get('AstroBase')->isJson($detailTicketJson)) {
            $this->oceaneData = Json::decode($detailTicketJson, Json::TYPE_ARRAY);
        }
        return $this->oceaneData;
    }

    /**
     * Récupérer l'identifiant ou les identifiants de la ressource associée à un ticket
     * @param $id
     * @return array|mixed|null
     */
    public function getRessourceIds($id = null)
    {
        $ids = [];
        if (key_exists('relatedResource', $this->oceaneData) && is_array($this->oceaneData['relatedResource']) && key_exists('resourceSpecCharacteristic', $this->oceaneData['relatedResource']) && is_array($this->oceaneData['relatedResource']['resourceSpecCharacteristic'])) {
            foreach ($this->oceaneData['relatedResource']['resourceSpecCharacteristic'] as $value) {
                if (is_array($value) && key_exists('index', $value) && !is_null($id) && (intval($value['index']) == $id) && key_exists('value', $value)) {
                    return $value['value'];
                } elseif (is_array($value) && key_exists('index', $value) && key_exists('value', $value)) {
                    $ids[$value['index']] = $value['value'];
                }
            }
        }
        return is_null($id) ? $ids : null;
    }

    /**
     * Récupérer l'identifiant ou les identifiants du produit associé à un ticket
     * @param $id
     * @return array|mixed|null
     */
    public function getProductIds($id = null)
    {
        $ids = [];
        if (key_exists('relatedService', $this->oceaneData) && is_array($this->oceaneData['relatedService']) && key_exists('serviceSpecCharacteristic', $this->oceaneData['relatedService']) && is_array($this->oceaneData['relatedService']['serviceSpecCharacteristic'])) {
            foreach ($this->oceaneData['relatedService']['serviceSpecCharacteristic'] as $value) {
                if (is_array($value) && key_exists('index', $value) && !is_null($id) && (intval($value['index']) == $id) && key_exists('value', $value)) {
                    return $value['value'];
                } elseif (is_array($value) && key_exists('index', $value) && key_exists('value', $value)) {
                    $ids[$value['index']] = $value['value'];
                }
            }
        }
        return is_null($id) ? $ids : null;
    }

    /**
     * Récupérer le type de ressource associée à un ticket
     * @param $idAndName
     * @return array|mixed|null
     */
    public function getRessourceType($idAndName = false)
    {
        if (key_exists('relatedResource', $this->oceaneData) && is_array($this->oceaneData['relatedResource']) && key_exists('resourceSpecification', $this->oceaneData['relatedResource'])) {
            $id = key_exists('id', $this->oceaneData['relatedResource']['resourceSpecification']) ? $this->oceaneData['relatedResource']['resourceSpecification']['id'] : null;
            if ($idAndName) {
                $name = key_exists('name', $this->oceaneData['relatedResource']['resourceSpecification']) ? $this->oceaneData['relatedResource']['resourceSpecification']['name'] : null;
                return [
                    'id' => $id,
                    'name' => StringTools::convertEncoding($name, 'ISO-8859-15', 'UTF-8')
                ];
            } else {
                return $id;
            }
        }
        return null;
    }

    /**
     * Récupérer le type de produit associé à un ticket
     * @param $idAndName
     * @return array|mixed|null
     */
    public function getProductType($idAndName = false)
    {
        if (key_exists('relatedService', $this->oceaneData) && is_array($this->oceaneData['relatedService']) && key_exists('serviceSpecification', $this->oceaneData['relatedService'])) {
            $id = key_exists('id', $this->oceaneData['relatedService']['serviceSpecification']) ? $this->oceaneData['relatedService']['serviceSpecification']['id'] : null;
            if ($idAndName) {
                $name = key_exists('name', $this->oceaneData['relatedService']['serviceSpecification']) ? $this->oceaneData['relatedService']['serviceSpecification']['name'] : null;
                return [
                    'id' => $id,
                    'name' => StringTools::convertEncoding($name, 'ISO-8859-15', 'UTF-8')
                ];
            } else {
                return $id;
            }
        }
        return null;
    }

    /**
     * Récupérer un ou plusieurs champs complémentaires d'un ticket
     * @param $champ
     * @return array|mixed|null
     */
    public function getTicketCharacteristics($champ = null)
    {
        $characteristic = [];
        if (key_exists('troubleTicketCharacteristic', $this->oceaneData) && is_array($this->oceaneData['troubleTicketCharacteristic']) && count($this->oceaneData['troubleTicketCharacteristic']) > 0) {
            foreach ($this->oceaneData['troubleTicketCharacteristic'] as $value) {
                if (is_array($value) && key_exists('index', $value) && !is_null($champ) && (intval($value['index']) == $champ) && key_exists('value', $value)) {
                    return $value['value'];
                } elseif (is_array($value) && key_exists('index', $value) && key_exists('value', $value)) {
                    $characteristic[$value['index']] = $value['value'];
                }
            }
        }
        return is_null($champ) ? $characteristic : null;
    }

    /**
     * Récupérer la priorité d'un ticket
     * @param $idAndLabel
     * @return array|mixed|null
     */
    public function getPriority($idAndLabel = false)
    {
        if (key_exists('priority', $this->oceaneData) && is_array($this->oceaneData['priority'])) {
            $id = key_exists('id', $this->oceaneData['priority']) ? $this->oceaneData['priority']['id'] : null;
            if ($idAndLabel) {
                $label = key_exists('label', $this->oceaneData['priority']) ? $this->oceaneData['priority']['label'] : null;
                return [
                    'id' => $id,
                    'label' => StringTools::convertEncoding($label, 'ISO-8859-15', 'UTF-8')
                ];
            } else {
                return $id;
            }
        }
        return null;
    }

    /**
     * Récupérer le niveau d'urgence d'un ticket
     * @param $idAndLabel
     * @return array|mixed|null
     */
    public function getUrgency($idAndLabel = false)
    {
        if (key_exists('urgency', $this->oceaneData) && is_array($this->oceaneData['urgency'])) {
            $id = key_exists('id', $this->oceaneData['urgency']) ? $this->oceaneData['urgency']['id'] : null;
            if ($idAndLabel) {
                $label = key_exists('label', $this->oceaneData['urgency']) ? $this->oceaneData['urgency']['label'] : null;
                return [
                    'id' => $id,
                    'label' => StringTools::convertEncoding($label, 'ISO-8859-15', 'UTF-8')
                ];
            } else {
                return $id;
            }
        }
        return null;
    }

    /**
     * Récupérer la date de création d'un ticket
     * @param $format
     * @return mixed|null
     */
    public function getCreationDate($format = null)
    {
        if (key_exists('creationDate', $this->oceaneData)) {
            if (!is_null($format)) {
                return $this->app->get('AstroBase')->formatDate($this->oceaneData['creationDate'], 'Y-m-d\TH:i:s\Z', $format);
            } else {
                return $this->oceaneData['creationDate'];
            }
        }
        return null;
    }

    /**
     * Récupérer l'eds pilote d'un ticket
     * @return mixed|null
     */
    public function getDetectionDate($format = null)
    {
        if (key_exists('detectionDate', $this->oceaneData)) {
            if (!is_null($format)) {
                return $this->app->get('AstroBase')->formatDate($this->oceaneData['detectionDate'], 'Y-m-d\TH:i:s\Z', $format);
            } else {
                return $this->oceaneData['detectionDate'];
            }
        }
        return null;
    }

    public function getDetailProblem()
    {
        if (key_exists('troubleCause', $this->oceaneData) && is_array($this->oceaneData['troubleCause']) && count($this->oceaneData['troubleCause']) > 0) {
            foreach ($this->oceaneData['troubleCause'] as $value) {
                if (is_array($value) && key_exists('problemDetail', $value) && key_exists('id', $value['problemDetail'])){
                    return $value['problemDetail']['id'];
                }
            }
        }
        return null;
    }

    /**
     * Récupérer l'eds pilote d'un ticket
     * @return mixed|null
     */
    public function getPilotGroup()
    {
        if (key_exists('relatedParty', $this->oceaneData) && is_array($this->oceaneData['relatedParty']) && count($this->oceaneData['relatedParty']) > 0) {
            foreach ($this->oceaneData['relatedParty'] as $value) {
                if (is_array($value) && key_exists('role', $value) && $value['role'] == 'TroubleResolutionLeader' && key_exists('id', $value)) {
                    return $value['id'];
                }
            }
        }
        return null;
    }
    public function getOriginatorGroup()
    {
        if (key_exists('relatedParty', $this->oceaneData) && is_array($this->oceaneData['relatedParty']) && count($this->oceaneData['relatedParty']) > 0) {
            foreach ($this->oceaneData['relatedParty'] as $value) {
                if (is_array($value) && key_exists('role', $value) && $value['role'] == 'troubleTicketOriginator' && key_exists('id', $value)) {
                    return $value['id'];
                }
            }
        }
        return null;
    }

    public function getActionEds()
    {
        if (key_exists('partyIntervention', $this->oceaneData) && is_array($this->oceaneData['partyIntervention']) && count($this->oceaneData['partyIntervention']) > 0) {
            foreach ($this->oceaneData['partyIntervention'] as $value) {
                if (is_array($value['relatedParty'])) {
                    foreach ($value['relatedParty'] as $valueRelatedParty) {
                        if (is_array($valueRelatedParty) && key_exists('actionInProgress', $valueRelatedParty) && $valueRelatedParty['role'] == 'TroubleResolutionLeader') {
                            if (is_array($valueRelatedParty['actionInProgress']) && key_exists('description', $valueRelatedParty['actionInProgress']))
                                return $valueRelatedParty['actionInProgress']['description'];
                        }
                    }
                }
            }
        }
        return null;
    }
    public function getActifGroup()
    {
        if (key_exists('relatedParty', $this->oceaneData) && is_array($this->oceaneData['relatedParty']) && count($this->oceaneData['relatedParty']) > 0) {
            foreach ($this->oceaneData['relatedParty'] as $value) {
                if (is_array($value) && key_exists('role', $value) && $value['role'] == 'TroubleResolutionContributor' && key_exists('id', $value)) {
                    return $value['id'];
                }
            }
        }
        return null;
    }

    public function getInterventionStatus()
    {
        if (key_exists('partyIntervention', $this->oceaneData) && is_array($this->oceaneData['partyIntervention'])) {
            foreach ($this->oceaneData['partyIntervention'] as $value) {
                    if (key_exists('interventionStatus', $value) && is_array($value['interventionStatus'])) {
                        foreach ($value['interventionStatus'] as $status) {
                            if((is_array($status) && key_exists('status', $status))){
                                return $status['status'];
                            }
                        }

                    }
            }
        }
        return null;
    }
    public function getStatus()
    {
        if (key_exists('status', $this->oceaneData) && is_array($this->oceaneData['status'])) {
            foreach ($this->oceaneData['status'] as $value) {
                if (key_exists('isCurrentStatus', $value) && $value['isCurrentStatus'] == 1) {
                    return $value['code'];
                }
            }
        }
        return null;
    }

    public function getTicketType($idAndLabel = false)
    {
        if (key_exists('ticketType', $this->oceaneData) && is_array($this->oceaneData['ticketType'])) {
            $id = key_exists('id', $this->oceaneData['ticketType']) ? $this->oceaneData['ticketType']['id'] : null;
            if ($idAndLabel) {
                $label = key_exists('label', $this->oceaneData['ticketType']) ? $this->oceaneData['ticketType']['label'] : null;
                return [
                    'id' => $id,
                    'label' => StringTools::convertEncoding($label, 'ISO-8859-15', 'UTF-8')
                ];
            } else {
                return $id;
            }
        }
        return null;
    }

    public function getOrigin($idAndLabel = false)
    {
        if (key_exists('origin', $this->oceaneData) && is_array($this->oceaneData['origin'])) {
            $id = key_exists('id', $this->oceaneData['origin']) ? $this->oceaneData['origin']['id'] : null;
            if ($idAndLabel) {
                $label = key_exists('label', $this->oceaneData['origin']) ? $this->oceaneData['origin']['label'] : null;
                return [
                    'id' => $id,
                    'label' => StringTools::convertEncoding($label, 'ISO-8859-15', 'UTF-8')
                ];
            } else {
                return $id;
            }
        }
        return null;
    }

    //relatedResource => impact
    public function getInstalledRessourceId()
    {
        if (key_exists('relatedResource', $this->oceaneData) && is_array($this->oceaneData['relatedResource']) && key_exists('id', $this->oceaneData['relatedResource'])) {
            return $this->oceaneData['relatedResource']['id'];
        }
        return null;
    }

    //relatedResource => impact
    public function getTicketParamsAttribute($param,$name)
    {
        if (key_exists('relatedResource', $this->oceaneData) && is_array($this->oceaneData['relatedResource']) && key_exists('resourceCharacteristic', $this->oceaneData['relatedResource']) && is_array($this->oceaneData['relatedResource']['resourceCharacteristic'])) {
            foreach ($this->oceaneData['relatedResource']['resourceCharacteristic'] as $value) {
                if (is_array($value) && key_exists('@type', $value) && $value['@type'] == $param && key_exists('id', $value) && $value['id'] == $name) {
                    return $value['value'];
                }
            }
        }
        return null;
    }

    public function getDescription()
    {
        return key_exists('description', $this->oceaneData) ? StringTools::convertEncoding($this->oceaneData['description'], 'ISO-8859-15', 'UTF-8') : '';
    }

    public function getId()
    {
        return key_exists('id', $this->oceaneData) ? $this->oceaneData['id'] : '';
    }
    public function getHno()
    {
        return key_exists('isONBHFollowupEnable', $this->oceaneData) ? $this->oceaneData['isONBHFollowupEnable'] : '';
    }
    public function getPartyId()
    {
        if (key_exists('relatedParty', $this->oceaneData) && is_array($this->oceaneData['relatedParty']) && count($this->oceaneData['relatedParty']) > 0) {
            foreach ($this->oceaneData['relatedParty'] as $value) {
                if (is_array($value) && key_exists('familyName', $value) && key_exists('id', $value)) {
                    return $value['id'];
                }
            }
        }
        return null;
    }

    public function getTicketCause()
    {
        if (key_exists('troubleCause', $this->oceaneData) && is_array($this->oceaneData['troubleCause'])) {
            return key_exists('internalComplement', $this->oceaneData['troubleCause']) ? $this->oceaneData['troubleCause']['internalComplement'] : '';
        }
        return null;
    }

    public function getPosteAssocie()
    {
        if (key_exists('partyIntervention', $this->oceaneData) && is_array($this->oceaneData['partyIntervention'])) {
            if (key_exists('relatedParty', $this->oceaneData) && is_array($this->oceaneData['relatedParty']) && count($this->oceaneData['relatedParty']) > 0) {
                foreach ($this->oceaneData['relatedParty'] as $value) {
                    if (is_array($value) && key_exists('role', $value) && $value['role'] == 'WorkingGroup' && key_exists('id', $value)) {
                        return $value['id'];
                    }
                }
            }
        }
        return null;
    }

    public function getLibelleSuccinct()
    {
        if (key_exists('status', $this->oceaneData) && is_array($this->oceaneData['status'])) {
            foreach ($this->oceaneData['status'] as $value) {
                if (key_exists('reason', $value)) {
                    return $value['reason'];
                }
            }
        }
        return null;
    }

    /**
     * Vérifier si un ticket est créé sur une ressource
     * @return bool
     */
    public function isRessource()
    {
        if (key_exists('relatedResource', $this->oceaneData) && is_array($this->oceaneData['relatedResource']) && key_exists('resourceSpecification', $this->oceaneData['relatedResource'])) {
            return true;
        }
        return false;
    }

    /**
     * Vérifier si un ticket est fils d'un autre ticket
     * @param $ticketId
     * @param $cuiId
     * @return bool
     */
    public function isChild($ticketId, $cuiId)
    {
        $oceaneApiData = $this->app->get('GlobalApiUrlService')->getUrlApi('API_OCEANE');
        $token = $this->getapeService->getToken($oceaneApiData, 'inside');

        $headerConfig = array(
            "X-Client-User-Id: $cuiId"
        );
        $oceaneApi = new ApiOceane($token, $headerConfig);
        $resultChild = $oceaneApi->getParent($oceaneApiData['url'], $ticketId);
        if ($this->app->get('AstroBase')->isJson($resultChild)) {
            $resultChild = Json::decode($resultChild, Json::TYPE_ARRAY);
            if (is_array($resultChild) && !empty($resultChild) && !key_exists('code', $resultChild) && key_exists('type', $resultChild[0]) && $resultChild[0]['type'] == 'isParent') {
                return true;
            }
        }
        return false;
    }

    /**
     * Vérifier s'il y a une demande d'activation sur un ticket
     * @param $eds
     * @return bool
     */
    public function isActivationRequested($eds)
    {
        $activationRequested = false;
        $isContributor = false;
        if (key_exists('partyIntervention', $this->oceaneData) && is_array($this->oceaneData['partyIntervention'])) {
            foreach ($this->oceaneData['partyIntervention'] as $value) {
                if (is_array($value) && key_exists('relatedParty', $value) && is_array($value['relatedParty'])) {
                    foreach ($value['relatedParty'] as $party) {
                        if (is_array($party) && key_exists('@referredType', $party) && $party['@referredType'] == 'Organisation' && key_exists('role', $party) && $party['role'] == 'TroubleResolutionContributor' && key_exists('id', $party) && $party['id'] == $eds) {
                            $isContributor = true;
                            break;
                        }
                    }
                    if ($isContributor && key_exists('interventionStatus', $value) && is_array($value['interventionStatus'])) {
                        foreach ($value['interventionStatus'] as $status) {
                            $activationRequested = (is_array($status) && key_exists('status', $status) && $status['status'] == 'Requested');
                        }

                    }
                }
                if ($activationRequested) {
                    return true;
                }
            }
        }
        return false;
    }
    public function getRestorationDate($format = null)
    {
        if (key_exists('status', $this->oceaneData) && is_array($this->oceaneData['status'])) {
            foreach ($this->oceaneData['status'] as $value) {
                if (key_exists('code', $value) && $value['code'] == "Restored") {
                    if (key_exists('startDate', $value)) {
                        if (!is_null($format)) {
                            return $this->app->get('AstroBase')->formatDate($value['startDate'], 'Y-m-d\TH:i:s\Z', $format);
                        } else {
                            return $value['startDate'];
                        }
                    }
                }
            }
        }
        return '';
    }
    public function getResolutionDate($format = null)
    {
        if (key_exists('status', $this->oceaneData) && is_array($this->oceaneData['status'])) {
            foreach ($this->oceaneData['status'] as $value) {
                if (key_exists('code', $value) && $value['code'] == "Resolved") {
                    if (key_exists('startDate', $value)) {
                        if (!is_null($format)) {
                            return $this->app->get('AstroBase')->formatDate($value['startDate'], 'Y-m-d\TH:i:s\Z', $format);
                        } else {
                            return $value['startDate'];
                        }
                    }
                }
            }
        }
        return '';
    }
    /**
     * Récupérer le niveau d'urgence d'un ticket
     * @param $idAndLabel
     * @return array|mixed|null
     */
    public function getCategory($idAndLabel = false)
    {
        if (key_exists('category', $this->oceaneData) && is_array($this->oceaneData['category'])) {
            $id = key_exists('id', $this->oceaneData['category']) ? $this->oceaneData['category']['id'] : null;
            if ($idAndLabel) {
                $label = key_exists('label', $this->oceaneData['category']) ? $this->oceaneData['category']['label'] : null;
                return [
                    'id' => $id,
                    'label' => StringTools::convertEncoding($label, 'ISO-8859-15', 'UTF-8')
                ];
            } else {
                return $id;
            }
        }
        return null;
    }
     public function getLibelleImputation(){

             if (key_exists('troubleCause', $this->oceaneData) && is_array($this->oceaneData['troubleCause'])) {
                 return key_exists('label', $this->oceaneData['troubleCause']) ? $this->oceaneData['troubleCause']['label'] : '';
             }
             return null;

     }

    public function isActivationAccpeted()
    {
        $activationAccepted = false;
        $isContributor = false;
        if (key_exists('partyIntervention', $this->oceaneData) && is_array($this->oceaneData['partyIntervention'])) {
            foreach ($this->oceaneData['partyIntervention'] as $value) {
                if (is_array($value) && key_exists('relatedParty', $value) && is_array($value['relatedParty'])) {
                    foreach ($value['relatedParty'] as $party) {
                        if (is_array($party) && key_exists('@referredType', $party) && $party['@referredType'] == 'Organisation' && key_exists('role', $party) && $party['role'] == 'TroubleResolutionContributor' && key_exists('id', $party)) {
                            $isContributor = true;
                            break;
                        }
                    }
                    if ($isContributor && key_exists('interventionStatus', $value) && is_array($value['interventionStatus'])) {
                        foreach ($value['interventionStatus'] as $status) {
                            $activationAccepted = (is_array($status) && key_exists('status', $status) && $status['status'] == 'Accepted' || $status['status'] == 'Completed');
                        }

                    }
                }
                if ($activationAccepted) {
                    return 1;
                }
            }
        }
        return 0;
    }

    public function activationIdsAndRoles()
    {
        $activationAccepted = false;
        $isContributor = false;
        $eds_nom = [];
        $eds_code = [];
        if (key_exists('partyIntervention', $this->oceaneData) && is_array($this->oceaneData['partyIntervention'])) {
            foreach ($this->oceaneData['partyIntervention'] as $value) {
                if (is_array($value) && key_exists('relatedParty', $value) && is_array($value['relatedParty'])) {
                    foreach ($value['relatedParty'] as $party) {
                        if (is_array($party) && key_exists('@referredType', $party) && $party['@referredType'] == 'Organisation' && key_exists('role', $party) && $party['role'] == 'TroubleResolutionContributor' && key_exists('id', $party)) {
                            $isContributor = true;
                            break;
                        }
                    }
                    if ($isContributor && key_exists('interventionStatus', $value) && is_array($value['interventionStatus'])) {
                        foreach ($value['interventionStatus'] as $status) {
                            $activationAccepted = (is_array($status) && key_exists('status', $status) && $status['status'] == 'Accepted' || $status['status'] == 'Completed');
                        }
                        if ($activationAccepted) {
                            array_push($eds_code, $party['id']);
                            array_push($eds_nom, $party['label']);
                        }

                    }
                }
            }
            return array('id' => $eds_code, 'label' => $eds_nom);

    }
        return null;
    }

    public function getCriticity($idAndLabel = false)
    {
        if (key_exists('criticity', $this->oceaneData) && is_array($this->oceaneData['criticity'])) {
            $id = key_exists('id', $this->oceaneData['criticity']) ? $this->oceaneData['criticity']['id'] : null;
            if ($idAndLabel) {
                $label = key_exists('label', $this->oceaneData['criticity']) ? $this->oceaneData['criticity']['label'] : null;
                return [
                    'id' => $id,
                    'label' => StringTools::convertEncoding($label, 'ISO-8859-15', 'UTF-8')
                ];
            } else {
                return $id;
            }
        }
        return null;
    }
    /**
     * Récupérer la date de création d'un ticket
     * @param $format
     * @return mixed|null
     */
    public function getTargetRestorationDate($format = null)
    {
        if (key_exists('targetRestorationDate', $this->oceaneData)) {
            if (!is_null($format)) {
                return $this->app->get('AstroBase')->formatDate($this->oceaneData['targetRestorationDate'], 'Y-m-d\TH:i:s\Z', $format);
            } else {
                return rtrim($this->oceaneData['targetRestorationDate'],"Z");
            }
        }
        return null;
    }
    /**
     * Récupérer  plannedRestorationDate
     * @param $format
     * @return mixed|null
     */
    public function getPlannedRestorationDate($format = null)
    {
        if (key_exists('plannedRestorationDate', $this->oceaneData)) {
            if (!is_null($format)) {
                return $this->app->get('AstroBase')->formatDate($this->oceaneData['plannedRestorationDate'], 'Y-m-d\TH:i:s\Z', $format);
            } else {
                return rtrim($this->oceaneData['plannedRestorationDate'],"Z");
            }
        }
        return null;
    }
    public function getDateActionInProgress($format = null)
    {
        if (key_exists('partyIntervention', $this->oceaneData) && is_array($this->oceaneData['partyIntervention'])) {
            if (key_exists('relatedParty', $this->oceaneData['partyIntervention'][0]) && is_array($this->oceaneData['partyIntervention'][0]['relatedParty'])) {
                foreach ($this->oceaneData['partyIntervention'][0]['relatedParty'] as $value) {
                    if (is_array($value) && key_exists('actionInProgress', $value) &&  key_exists('startDate', $value['actionInProgress'])) {

                        if (!is_null($format)) {
                            return $this->app->get('AstroBase')->formatDate($value['actionInProgress']['startDate'], 'Y-m-d\TH:i:s\Z', $format);
                        } else {
                            return rtrim($value['actionInProgress']['startDate'],"Z");
                        }
                    }
                }
            }
        }
        return null;
    }
    public function getActionInProgress()
    {
        if (key_exists('partyIntervention', $this->oceaneData) && is_array($this->oceaneData['partyIntervention'])) {
            if (key_exists('relatedParty', $this->oceaneData['partyIntervention'][0]) && is_array($this->oceaneData['partyIntervention'][0]['relatedParty'])) {
                foreach ($this->oceaneData['partyIntervention'][0]['relatedParty'] as $value) {
                    if (is_array($value) && key_exists('actionInProgress', $value) &&  key_exists('description', $value['actionInProgress'])) {
                     return $value['actionInProgress']['description'];

                    }
                }
            }
        }
        return null;
    }

    public function getEdsActionInProgress()
    {
        if (key_exists('partyIntervention', $this->oceaneData) && is_array($this->oceaneData['partyIntervention'])) {
            if (key_exists('relatedParty', $this->oceaneData['partyIntervention'][0]) && is_array($this->oceaneData['partyIntervention'][0]['relatedParty'])) {
                foreach ($this->oceaneData['partyIntervention'][0]['relatedParty'] as $value) {
                    if (is_array($value) && key_exists('id', $value)) {
                        return $value['id'];
                    }
                }
            }
        }
        return null;
    }
    public function getDrDate(){
        $drDate = '';
        $driDate = $this->getTargetRestorationDate();
        $drcDate = $this->getPlannedRestorationDate();
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
        return $drDate;
    }
    public function getClasitePrio(){
        if (key_exists('relatedResource', $this->oceaneData) && is_array($this->oceaneData['relatedResource'])) {
            if (key_exists('resourceCharacteristic', $this->oceaneData['relatedResource'])){
                foreach ($this->oceaneData['relatedResource']['resourceCharacteristic'] as $value) {
                    if (is_array($value) && key_exists('id', $value) && $value['id'] == 'CLASITE') {
                        if (key_exists('value', $value)) {
                            return $value['value'];
                        }
                    }
            }
        }
        return '';
    }
    }
    public function getRelatedRessource()
    {
        if (key_exists('relatedResource', $this->oceaneData) && is_array($this->oceaneData['relatedResource']) && key_exists('resourceSpecCharacteristic', $this->oceaneData['relatedResource'])) {
            return $this->oceaneData['relatedResource']['resourceSpecCharacteristic'][0]['value'];
        }
        return null;
    }
    public function getUserId()
    {
        $cuidlower = $this->app->config['api_data']['cuid']; //ID HBM
        return $this->app->get('IhmUtilisateurRepository')->getByLogin($cuidlower)['ID_UTILISATEUR'];
    }
    public function getLogin()
    {
        $cuidlower = $this->app->config['api_data']['cuid']; //ID HBM
        return $this->app->get('IhmUtilisateurRepository')->getByLogin($cuidlower)['LOGIN'];
    }

}
