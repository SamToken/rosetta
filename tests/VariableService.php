<?php


namespace App\Service;


use App\Repository\AstroRepository;
use App\Repository\RefsitesRepository;
use App\Repository\VariableRepository;
use App\Repository\GlobalApiRepository;
use App\Tools\OceaneTools;
use Hbm\Common\Tools\StringTools;
use Hbm\Globalapi\Factory\Pariv2Factory;
use Hbm\Globalapi\Service\Rest\ApiOceane;
use Oft\Mvc\Application;
use Zend\Json\Json;

class VariableService extends VariableBaseService
{

    /**
     * @var Application
     */
    protected $app;

    protected $sessId;

    protected $loginId;

    protected $ticketId;

    protected $astroId;

    protected $findAndGet;

    protected $dataPariv2;

    protected $typeRessource;

    protected $id1;

    protected $id2;

    protected $id3;

    protected $eds;

    /**
     * @var AstroRepository
     */
    protected $astroRepository;

    /**
     * @var RefsitesRepository
     */
    protected $refSiteRepository;

    /**
     * @var VariableRepository
     */
    protected $variableRepository;

    /**
     * @var TransitoolService
     */
    protected $transitoolService;

    /**
     * @var GlobalApiRepository
     */
    protected $globalApiRepository;

    /**
     * @var GatapeService
     */
    protected $getapeService;

    /**
     * @var GlobalApiUrlService
     */
    protected $globalApiService;
    protected $arrayRessourcesTransAvecExt;

    public function __construct($app)
    {
        parent::__construct($app);
        $this->app = $app;
        $this->sessId = (key_exists('api', $this->app->config) && $this->app->config['api']) ? $this->getUserId() : $this->app->get('Session')->getUtilisateurId();
        $this->loginId = (key_exists('api', $this->app->config) && $this->app->config['api']) ? $this->getLogin() : $this->app->get('Session')->getUtilisateurLogin();
        $this->findAndGet = null;
        $this->dataPariv2 = null;
        $this->arrayRessourcesTransAvecExt = array(
            'WDM_SID',
            'SLN',
            'SDH',
            'MIE'
        );
    }

    /**
     * replacer les Tags par les valeurs
     *
     * @param string $chaine
     * @param array $args
     * @return string
     */
    public function replaceTagsChaine($chaine, $args, $type, $ticketId, $variable = '', $extrimite = '')
    {
        $this->ticketId = $ticketId;
        $this->typeRessource = $type;
        $this->astroRepository = $this->app->get('AstroRepository');
        $this->astroId = $this->astroRepository->getAstroIdByTicket($this->ticketId);

        $this->getOceane = $this->app->get('OceaneGet');
        $this->getOceane->getOceaneData($ticketId, $this->loginId);
        $this->id1 = $this->getOceane->getRessourceIds(1);
        $this->id2 = $this->getOceane->getRessourceIds(2);
        $this->id3 = $this->getOceane->getRessourceIds(3);
        $resourceSpecification = "";
        $libSite = "";
        $donnesTempsReel = array();
        foreach ($args as $arg) {
            if ($arg == 'Temperature' || $arg == 'Etat_batterie' || $arg == 'Tension_batterie' || $arg == 'Element_HS') {
                $traceData = array(
                    'astro_id' => $this->astroId,
                    'ticket_id' => $this->ticketId,
                    'session_id' => $this->sessId,
                );
                $this->findAndGet = $this->app->get('OceaneService')->findAndGetOceane($this->ticketId);
                $parameters = (key_exists('installed_resource', $this->findAndGet) && property_exists($this->findAndGet['installed_resource'], 'Parameters')) ? $this->findAndGet['installed_resource']->Parameters : array();
                if (property_exists($parameters, 'Parameter')) {
                    foreach ($parameters->Parameter as $val1) {
                        if (property_exists($val1, 'id') && $val1->id == 'LIBSITE') {
                            $libSite = $val1->value;
                        }
                    }
                    if ($libSite != "") {
                        $donnesTempsReel = $this->app->get('Cia')->getDataSite($libSite, $traceData);
                    }
                }
            }
            if ($arg == 'DSLAM_PRODUIT_DSLAM' || $arg == 'DSLAM_PRODUIT_CHASSIS' || $arg == 'DSLAM_PRODUIT_CARTE' || $arg == 'DSLAM_PRODUIT_PORT' || $arg == 'DSLAM_PRODUIT_PM') {
                if (is_null($this->variableRepository)) {
                    $this->variableRepository = $this->app->get('VariableRepository');
                }
                $replaceValue = $this->variableRepository->getVarsNonAdministree($this->ticketId, $arg);
                if (!$replaceValue) {
                    $replaceValue = $this->app->get('AssistantService')->getInfoTicketAdeliaByPrestation($this->ticketId, $arg);
                    if ($replaceValue != '' && !is_null($replaceValue) && !is_array($replaceValue)) {
                        $this->variableRepository->insertVarsNonAdministree($this->ticketId, $arg, $replaceValue);
                    }
                }
                if (OceaneTools::isValidVariable($replaceValue) && !is_array($replaceValue)) {
                    $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                }

            }
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

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }
                    break;

                case 'CUID':
                    $replaceValue = (!is_null($this->loginId)) ? $this->loginId : '';
                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }
                    break;
                case 'TICKETID':
                    $replaceValue = (!is_null($this->ticketId)) ? $this->ticketId : '';

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }
                    break;

                case 'SUPPORT 30N':
                    $replaceValue = $this->app->get('CommutationRessource')->infoRessourcesCommutation($this->ticketId, true);
                    $chaine = str_replace('###' . $arg . '###', $replaceValue['synthese']['30N'], $chaine);
                    break;
                case 'Etat_batterie':
                    if (key_exists('etat', $donnesTempsReel) && $donnesTempsReel['etat'] == 'ok') {

                        $replaceValue = $donnesTempsReel;
                        $chaine = str_replace('###' . $arg . '###', $replaceValue['mode_fonctionnement_batterie'], $chaine);
                    }

                    break;
                case 'Element_HS':
                    if (key_exists('etat', $donnesTempsReel) && $donnesTempsReel['etat'] == 'ok') {
                        $replaceValue = $donnesTempsReel;
                        $chaine = str_replace('###' . $arg . '###', $replaceValue['element_equipement_panne_tronc'], $chaine);
                    }

                    break;
                case 'Tension_batterie':
                    if (key_exists('etat', $donnesTempsReel) && $donnesTempsReel['etat'] == 'ok') {
                        $replaceValue = $donnesTempsReel;
                        $chaine = str_replace('###' . $arg . '###', $replaceValue['tension'], $chaine);
                    }

                    break;
                case 'Temperature':
                    if (key_exists('etat', $donnesTempsReel) && $donnesTempsReel['etat'] == 'ok') {
                        $replaceValue = $donnesTempsReel;
                        $chaine = str_replace('###' . $arg . '###', $replaceValue['temperature'], $chaine);
                    }

                    break;
                case 'NIDT':
                    $replaceValue = (!is_null($this->getCodeNidt())) ? $this->getCodeNidt() : '';

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }
                    break;

                case 'DSLAM_MAJ':
                    $replaceValue = (!is_null($this->getDslam('MAJ'))) ? $this->getDslam('MAJ') : '';

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }
                    break;

                case 'DSLAM_MIN':
                    $replaceValue = (!is_null($this->getDslam('MIN'))) ? $this->getDslam('MIN') : '';

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }

                    break;
                case 'PILOTE':
                    $this->eds = $this->astroRepository->getPiloteGroup($this->ticketId);
                    $replaceValue = (!is_null($this->eds)) ? $this->eds : '';

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }

                    break;
                case 'TYPE':
                    $replaceValue = (!is_null($this->typeRessource)) ? $this->typeRessource : '';

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }

                    break;
                case 'TOKEN':
                    $token = base64_encode(md5(date('yyyymmdd') . 'link_astro_charter'));
                    $chaine = str_replace('###' . $arg . '###', $token, $chaine);
                    break;

                case 'DATE':
                    if (is_null($this->findAndGet)) {
                        $this->findAndGet = $this->app->get('OceaneService')->findAndGetOceane($this->ticketId);
                    }

                    $replaceValue = isset($this->findAndGet['fg_date']) ? $this->findAndGet['fg_date'] : '';

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }

                    break;
                case 'FG_NOMNAEQP':
                case 'FG_E1NOMNAEQP':
                case 'FG_E2NOMNAEQP':
                    if (is_null($this->findAndGet)) {
                        $this->findAndGet = $this->app->get('OceaneService')->findAndGetOceane($this->ticketId);
                    }
                    if (!isset($this->findAndGet['message']) && !is_null($this->findAndGet['installed_resource']) && property_exists($this->findAndGet['installed_resource'],
                            'Parameters') && property_exists($this->findAndGet['installed_resource']->Parameters, 'Parameter')) {
                        $result = OceaneTools::searchValueInFindAndGet(substr($arg, 3), $this->findAndGet['installed_resource']->Parameters->Parameter);
                        $replaceValue = (!is_null($result)) ? $result : '';
                        if (OceaneTools::isValidVariable($replaceValue)) {
                            $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                        }
                    }
                    break;
                case 'RD3+':
                    if (is_null($this->findAndGet)) {
                        $this->findAndGet = $this->app->get('OceaneService')->findAndGetOceane($this->ticketId);
                    }

                    if (!isset($this->findAndGet['message']) && !is_null($this->findAndGet['rd_plus'])) {
                        $replaceValue = (!is_null($this->findAndGet['rd_plus'])) ? $this->findAndGet['rd_plus'] : null;

                        if (OceaneTools::isValidVariable($replaceValue)) {
                            $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                        }
                    }
                    break;
                case 'DESCRIPTION':
                    if (is_null($this->findAndGet)) {
                        $this->findAndGet = $this->app->get('OceaneService')->findAndGetOceane($this->ticketId);
                    }

                    if (!isset($this->findAndGet['message']) && !is_null($this->findAndGet['description'])) {
                        $replaceValue = (!is_null($this->findAndGet['description'])) ? $this->findAndGet['description'] : null;

                        if (OceaneTools::isValidVariable($replaceValue)) {
                            $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                        }
                    }
                    break;
                case 'Intervenant_EVT':
                    if (is_null($this->findAndGet)) {
                        $this->findAndGet = $this->app->get('OceaneService')->findAndGetOceane($this->ticketId);
                    }
                    if (!isset($this->findAndGet['message']) && !is_null($this->findAndGet['code_detecteur'])) {
                        if (!is_null($this->findAndGet['code_detecteur'])) {
                            $replaceValue = ($this->findAndGet['code_detecteur'] != "ORANGE") ? $this->findAndGet['code_detecteur'] : "UI";
                        } else {
                            $replaceValue = null;
                        }

                        if (OceaneTools::isValidVariable($replaceValue)) {
                            $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                        }

                    }
                    break;

                case 'CODE_EAN':
                case 'Nom_Carte':
                case 'Type_Equipement':
                    // des variables non admnistrés récupéré par l'action replaceVarsBlocsComment
                    break;

                case 'INTERVENANT_REFSITES':
                    if (in_array($type, $this->arrayRessourcesTransAvecExt)) {
                        $replaceValue = $this->getIntervenant($type, $variable, $extrimite);
                    } else {
                        $replaceValue = $this->getIntervenant($type);
                    }

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);

                    }
                    break;
                case 'PRIMO_REFSITE_DEPARTEMENT':
                case 'PRIMO_REFSITE_CODE_TIPI':
                case 'PRIMO_REFSITE_CODE_NIDT':
                case 'PRIMO_REFSITE_APPELLATION_SUPERVISION':
                case 'PRIMO_REFSITE_CODE_FIXEDR':

                    $arrayRefSite = [
                        'PRIMO_REFSITE_DEPARTEMENT' => 'DEPARTEMENT',
                        'PRIMO_REFSITE_CODE_TIPI' => 'TIPICODE',
                        'PRIMO_REFSITE_APPELLATION_SUPERVISION' => 'ORIG_GEO',
                        'PRIMO_REFSITE_CODE_NIDT' => 'NIDTCODE',
                        'PRIMO_REFSITE_CODE_FIXEDR' => 'DRCODEFIXE'

                    ];
                    $this->refSiteRepository = $this->app->get('RefsitesRepository');
                    $replaceValue = $this->refSiteRepository->getRefsiteColumn($arrayRefSite[$arg], $ticketId);

                    if (OceaneTools::isValidVariable($replaceValue) && gettype($replaceValue) != 'boolean') {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }
                    break;
                case 'PARIV2_DISTRIBUTOR_LOCATION_NAME':
                case 'PARIV2_DISTRIBUTOR_LOCATION_LOCATIONTYPE_NAME':
                case 'PARIV2_MODEL_CATEGORYDTO_NAME':
                case 'PARIV2_SENSITIVITY_NAME':
                case 'PARIV2_NAME':
                case 'PARIV2_DISTRIBUTOR_LOCATION_LEAF':
                case 'PARIV2_DISTRIBUTOR_LOCATION_LEAF1':
                case 'PARIV2_DISTRIBUTOR_LOCATION_LEAF2':
                case 'PARIV2_DISTRIBUTOR_LOCATION_ADDRESS':
                case 'PARIV2_LOCATION_POSTALCODE':
                case 'PARIV2_DISTRIBUTOR_LOCATION_CITY':
                case 'PARIV2_MODEL_NAME':
                case 'PARIV2_DISTRIBUTOR_LOCATION_LOCATIONPHONE':
                case 'PARIV2_DEVICETYPE_PERIMETER_NAME':
                case 'PARIV2_IPADMIN':
                case 'PARIV2_DISTRIBUTOR_NAME':
                case 'PARIV2_LOOPBACK':
                case 'PARIV2_DISTRIBUTOR_LOCATION_TIPI':
                case 'PARIV2_DISTRIBUTOR_LOCATION_REFSITECODE':

                $chaine = $this->replaceTagsChainePariV2($chaine, $type, $ticketId, $arg);
                    break;
                case 'PRIMO_AIGUILLAGE_TRONCON':
                    if ($this->typeRessource == 'TRONCABLE') {

                        $replaceValue = $this->replaceTagsChainePrimoAiguillageTroncon($ticketId);
                        if (OceaneTools::isValidVariable($replaceValue)) {
                            $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                        }
                        break;
                    }
                case 'PRIMO_REFSITE_100RS':
                    $this->refSiteRepository = $this->app->get('RefsitesRepository');
                    $resultColumn = $this->refSiteRepository->getRefsiteColumn('RS', $ticketId);

                    $replaceValue = '';
                    if (!is_null($resultColumn) && $resultColumn != '') {
                        $replaceValue = ($resultColumn == 'ORANGE') ? 'Non' : 'Oui';
                    }
                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }
                    break;
                default:
                    $this->globalApiRepository = $this->app->get('GlobalApiRepository');
                    if ($this->globalApiRepository->isVariableAdminExist($arg, $type)) {

                        if (is_null($this->findAndGet)) {
                            $this->findAndGet = $this->app->get('OceaneService')->findAndGetOceane($this->ticketId);
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
                                    if (isset($replaceValue)) {
                                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                                    }
                                }
                            }
                        }
                    }
            }
        }

        return $chaine;
    }

    public function transcodage($var)
    {

        $refsiteFirst = substr($var, 0, -strlen(strrchr($var, '/')));
        $refsiteFirst = preg_replace('/\s\s+/', ' ', trim($refsiteFirst));
        $refsiteFirst = str_replace("!", "/", $refsiteFirst);
        return $refsiteFirst;
    }

    public function replaceTagsChainePrimoAiguillageTroncon($ticketId)
    {
        $this->getOceane = $this->app->get('OceaneGet');
        $this->getOceane->getOceaneData($ticketId, $this->loginId);

        $ext1 = $this->getOceane->getRessourceIds(1);//sans $this->transcodage()
        $ext2 = $this->getOceane->getRessourceIds(2);

        $isSitePassifext1 = $this->refSiteRepository->isSitePassif($this->transcodage($ext1));
        $isSitePassifext2 = $this->refSiteRepository->isSitePassif($this->transcodage($ext2));

        return $this->selectExtension($ext1, $isSitePassifext1, $ext2, $isSitePassifext2);
    }

    public function selectExtension($ext1, $ext1_status, $ext2, $ext2_status)
    {
        // Si EXT1 est actif, on retourne sa valeur
        // actif=>0, passif=>1

        if ($ext1_status == 0) {
            return $ext1;
        }
        // Si EXT1 est passif et EXT2 est actif
        if ($ext1_status == 1 && $ext2_status == 0) {
            return $ext2;
        }
        // si EXT1 n'existe pas sur refsites
        if($ext1_status == -1){
            return $ext2;
        }
        // si EXT2 n'existe pas sur refsites
        if($ext2_status == -1) {
            return $ext1;
        }
        // Dans tous les autres cas, on retourne EXT1
        return $ext1;
    }

    public function getIntervenant($typeRessource, $variable = '', $ext = '')
    {
        $intervenant = '';
        $this->refSiteRepository = $this->app->get('RefsitesRepository');
        $resultQuery = false;
        if ($typeRessource == 'TRONCABLE') { // Si le type de ressource est TRONCABLE, on récupère la valeur de la variable PRIMO_AIGUILLAGE_TRONCON
            $variableAdministree = 'PRIMO_AIGUILLAGE_TRONCON';
        } else {
            $variableAdministree = 'INTERVENANT_MATRICE_REFSITES';
        }

        if ($variable != '') {
            $intervenantMatriceRefsite = $variable;
        } else {
            $argsVariableGlobal = array();
            $argsVariableGlobal[] = $variableAdministree;
            $intervenantMatriceRefsite = $this->replaceTagsChaine("###$variableAdministree###", $argsVariableGlobal, $typeRessource, $this->ticketId);
        }

        if ($intervenantMatriceRefsite != "###$variableAdministree###") {
            switch ($typeRessource) {
                case 'CA-CASW':
                case 'S-SUP':
                case 'PI-PROTSW':
                case 'E-ENERSW':
                    $resultQuery = $this->refSiteRepository->getEvtFixeByOrigGeo($intervenantMatriceRefsite);
                    break;
                case 'SUP-SUPION':
                    $resultQuery = $this->refSiteRepository->getRsByOrigGeo($intervenantMatriceRefsite);
                    break;
                case 'DSLAM':
                    $refsiteFirst = substr($intervenantMatriceRefsite, 0, -strlen(strrchr($intervenantMatriceRefsite, '/')));
                    $chaineQuery = preg_replace("~ (?!.* )~", " / ", $refsiteFirst);
                    $resultQuery = $this->refSiteRepository->getRsByAggloSite($chaineQuery);
                    break;
                case 'ROUTEURGE':
                case 'SWTIP':
                case 'ROUTIP':
                case 'MGATEWAY':
                    $refsiteFirst = $this->replaceCaractRefSite($intervenantMatriceRefsite);
                    $refsiteFirst = str_replace("!", "/", $refsiteFirst);
                    $resultQuery = $this->refSiteRepository->getRsByAppelationIr($refsiteFirst);
                    break;
                case 'UNIRACC':
                case 'CONNUM':
                case 'COMMUT':
                    $resultQuery = $this->getRefSiteBySGTQS($intervenantMatriceRefsite, null);
                    break;
                case 'WDM_SID':
                case 'SLN':
                case 'SDH':
                case 'MIE':
                    $refsiteFirst = substr($intervenantMatriceRefsite, 0, -strlen(strrchr($intervenantMatriceRefsite, '/')));
                    $refsiteFirst = preg_replace('/\s\s+/', ' ', trim($refsiteFirst));
                    $refsiteFirst = str_replace("!", "/", $refsiteFirst);
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
                    $techno = $this->replaceTagsChaine("###$extremiteTechno###", $argsVariableGlobal1, $typeRessource, $this->ticketId);

                    if ($techno == 'FH') {
                        $resultQuery = $this->refSiteRepository->getFhByAppelationIr($refsiteFirst);
                    } else {
                        $resultQuery = $this->refSiteRepository->getRsByAppelationIr($refsiteFirst);
                    }
                    break;
                case 'TRONCABLE':
                    $resultQuery = $this->refSiteRepository->getRsByAppelationIr($this->transcodage($intervenantMatriceRefsite));
                    break;
                default:
                    $resultQuery = false;
                    break;
            }
        }

        if (gettype($resultQuery) != 'boolean' && $resultQuery != '' && is_array($resultQuery)) {
            $intervenant = key_exists('INTERVENANT', $resultQuery) ? $resultQuery['INTERVENANT'] : '';
            if (key_exists('ID', $resultQuery)) {
                $this->refSiteRepository->UpdateTicketAstroWithIdRefsite($this->ticketId, $resultQuery['ID']);
            }
        } else {
            $this->refSiteRepository->UpdateTicketAstroWithIdRefsite($this->ticketId, null);
        }
        return $intervenant;
    }

    public function replaceCaractRefSite($intervenantMatriceRefsite)
    {
        if (strpos($intervenantMatriceRefsite, "/")) {
            $refsiteFirst = substr($intervenantMatriceRefsite, 0, -strlen(strrchr($intervenantMatriceRefsite, '/')));
            $refsiteFirst = preg_replace('/\s\s+/', ' ', trim($refsiteFirst));
        } else {
            $refsiteFirst = $intervenantMatriceRefsite;
        }
        return $refsiteFirst;
    }

    public function replaceCaractRefSiteAgglo($value)
    {
        if (strpos($value, "/")) {
            $refsiteFirst = substr($value, 0, -strlen(strrchr($value, '/')));
            $refsiteFirst = str_replace(":", " ", $refsiteFirst);
            $refsiteFirst = str_replace("!", "/", $refsiteFirst);
            $refsiteFirst = preg_replace("~ (?!.* )~", " / ", $refsiteFirst);
        } else {
            $refsiteFirst = $value;
        }
        return $refsiteFirst;
    }

    public function getRefSiteByData($selectData, $value, $interv)
    {
        $this->refSiteRepository = $this->app->get('RefsitesRepository');
        $interv = str_replace("!", "/", $interv);
        return $this->refSiteRepository->getDataByAppelationIr($selectData, $value, $interv);
    }

    public function getRefSiteBySGTQS($designation, $donnee = null)
    {
        $this->refSiteRepository = $this->app->get('RefsitesRepository');
        $idNoeud = $this->refSiteRepository->getIdFromRefsitesNoeuds($designation);
        return $this->refSiteRepository->getRsByIdNoeud($idNoeud, $donnee);
    }

    /**
     * Remplacer les variables par les valeurs de l'API PARIV2
     *
     * @param $chaine
     * @param $typeRessource
     * @param $ticketId
     * @param $variable
     * @return array|string|string[]|null
     */
    public function replaceTagsChainePariV2($chaine, $typeRessource, $ticketId, $variable)
    {
        $astroId = $this->app->get('AstroRepository')->getAstroIdByTicket($ticketId);
        $variableAdministree = 'INFRA_CONTEXTE_PARIV2';
        $argsVariableGlobal[] = $variableAdministree;
        $infraContextePari = $this->replaceTagsChaine("###$variableAdministree###", $argsVariableGlobal, $typeRessource, $ticketId);

        if (!in_array($infraContextePari, ["###$variableAdministree###", ''])) {
            if (is_null($this->dataPariv2)) {
                $dataJson = $this->getDataPariv2($ticketId, $typeRessource, $infraContextePari);

                if ($this->app->get('AstroBase')->isJson($dataJson)) {
                    $this->dataPariv2 = Json::decode($dataJson, JSON::TYPE_ARRAY);
                    $this->app->get('TraceRepository')->setTrace($astroId, "PARI V2 REPONSE", $this->dataPariv2, $this->sessId, $ticketId);
                } else {
                    $this->app->get('TraceRepository')->setTrace($astroId, "PARI V2 REPONSE", $dataJson, $this->sessId, $ticketId);
                }
            }

            $replaceValue = $this->getReplaceValue($this->dataPariv2, $variable);
            if (OceaneTools::isValidVariable($replaceValue) && gettype($replaceValue) != 'boolean') {
                $chaine = str_replace('###' . $variable . '###', $replaceValue, $chaine);
            } else {
                $chaine = str_replace('###' . $variable . '###', '', $chaine);
            }
        } else {
            $chaine = str_replace('###' . $variable . '###', '', $chaine);
        }

        return $chaine;
    }

    public function getDataPariv2($ticketId, $typeRessource, $infraContextePari)
    {
        $dataTicket = [];
        $this->getOceane = $this->app->get('OceaneGet');
        $this->getOceane->getOceaneData($ticketId, $this->loginId);
        $isProduit = !$this->getOceane->isRessource();
        $complementaryField6 = $this->getOceane->getTicketCharacteristics(6);

        $this->globalApiService = $this->app->get('GlobalApiUrlService');
        $oceaneApiData = $this->globalApiService->getUrlApi('API_OCEANE');

        $this->getapeService = $this->app->get('Gatape');
        $token = $this->getapeService->getToken($oceaneApiData, 'inside');
        $headerConfig = array(
            "X-Client-User-Id: $this->loginId",
            "X-HTTP-Method-Override: PATCH"
        );
        $oceaneApi = new ApiOceane($token, $headerConfig);

        $pariv2ApiData = $this->globalApiService->getUrlApi('API_PARIV2');
        $token = $this->getapeService->getToken($pariv2ApiData);

        $pariUser = $pariv2ApiData["pari-user"];
        $headerConfig = array(
            "pari-user: $pariUser"
        );

        $astroId = $this->app->get('AstroRepository')->getAstroIdByTicket($ticketId);
        $this->app->get('TraceRepository')->setTrace($astroId, "PARI V2 ENVOI", $infraContextePari, $this->sessId, $ticketId);
        $pariv2 = new Pariv2Factory($token, $headerConfig, $this->app->config['ENV']);
        $dataTicket['type_ressource'] = $typeRessource;
        $dataTicket['champ_compl_6'] = $complementaryField6;
        $dataTicket['is_produit'] = $isProduit;
        $dataTicket['ticket_id'] = $ticketId;

        $oceaneApiArray['oceane_api_object'] = $oceaneApi;
        $oceaneApiArray['oceane_api_data_url'] = $oceaneApiData['url'];

        $dataJson = $pariv2->getVariableStatus($pariv2ApiData, 'API_PARIV2', 'INFRA_CONTEXTE_PARIV2', $infraContextePari, $dataTicket, $oceaneApiArray);

        return $dataJson;
    }

    /**
     * Récupérer la valeur de remplacement pour une variable
     *
     * @param $data
     * @param $variable
     * @return mixed|null
     */
    private function getReplaceValue($data, $variable)
    {
        $mapping = [
            'PARIV2_DISTRIBUTOR_LOCATION_NAME' => ['distributor', 'location', 'name'],
            'PARIV2_DISTRIBUTOR_LOCATION_LOCATIONTYPE_NAME' => ['distributor', 'location', 'locationType', 'name'],
            'PARIV2_MODEL_CATEGORYDTO_NAME' => ['model', 'categoryDto', 'name'],
            'PARIV2_SENSITIVITY_NAME' => ['sensitivity', 'name'],
            'PARIV2_NAME' => ['name'],
            'PARIV2_DISTRIBUTOR_LOCATION_LEAF' => ['distributor', 'location', 'leaf'],
            'PARIV2_DISTRIBUTOR_LOCATION_LEAF1' => ['distributor', 'location', 'leaf1'],
            'PARIV2_DISTRIBUTOR_LOCATION_LEAF2' => ['distributor', 'location', 'leaf2'],
            'PARIV2_DISTRIBUTOR_LOCATION_ADDRESS' => ['distributor', 'location', 'address'],
            'PARIV2_LOCATION_POSTALCODE' => ['distributor', 'location', 'postalCode'],
            'PARIV2_DISTRIBUTOR_LOCATION_CITY' => ['distributor', 'location', 'city'],
            'PARIV2_MODEL_NAME' => ['model', 'name'],
            'PARIV2_DISTRIBUTOR_LOCATION_LOCATIONPHONE' => ['distributor', 'location', 'locationPhone'],
            'PARIV2_DEVICETYPE_PERIMETER_NAME' => ['model', 'perimeter', 'name'],
            'PARIV2_IPADMIN' => ['ipAdmin'],
            'PARIV2_DISTRIBUTOR_NAME' => ['distributor', 'name'],
            'PARIV2_LOOPBACK' => ['loopback'],
            'PARIV2_DISTRIBUTOR_LOCATION_TIPI' => ['distributor', 'location', 'tipi'],
            'PARIV2_DISTRIBUTOR_LOCATION_REFSITECODE' => ['distributor', 'location', 'refsiteCode'],
        ];

        if (isset($mapping[$variable])) {
            $keys = $mapping[$variable];
            $value = $data;
            foreach ($keys as $key) {
                if (is_array($value) && key_exists($key, $value)) {
                    $value = $value[$key];
                } else {
                    return null;
                }
            }
            return StringTools::convertEncoding($value, 'ISO-8859-15', 'UTF-8');
        }

        return null;
    }

    /**
     * Récupérer la valeur d'un attribut dans un tableau
     *
     * @param $data
     * @param $attribute
     * @return string
     */
    protected function getAttribute($data, $attribute)
    {
        return (key_exists($attribute, $data)) ? $data[$attribute] : '';
    }
}
