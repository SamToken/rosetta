<?php
/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

namespace App\Service;

use App\Repository\AgpGeneriqueRepository;
use App\Repository\AgpRepository;
use App\Repository\AstroIhmSqlRepository;
use App\Repository\AstroLienRepository;
use App\Repository\AstroRepository;
use App\Repository\EdrRepository;
use App\Repository\GlobalApiRepository;
use App\Tools\Message;
use \App\View\Helper\Edr;
use App\Tools\OceaneAssistant;
use App\Tools\AgpCC;
use App\Form\DemandeInterventionForm;
use App\Form\DemandeInterventionGeneriqueForm;
use App\Form\DemandeInterventionSecondForm;
use App\Form\CreaTicketTransForm;
use App\Form\CreaTicketAdslForm;
use Hbm\Globalapi\Service\Rest\ApiOceane;
use Hbm\Common\Service\LinkService;
use App\View\Helper\DemandeIntervention;
use App\Tools\DroitAstroTools;
use App\Tools\OceaneTools;
use Hbm\Common\Tools\StringTools;
use Oft\Mvc\Application;
use Zend\Json\Json;

/**
 * Description of AgpService
 *
 * @author mbiyoud
 */
class AgpService
{
    /**
     * @var AstroRepository
     */
    protected $astroRepository;

    /**
     * @var EdrRepository
     */
    protected $edrRepository;

    /**
     * @var EdrService
     */
    protected $edrService;

    /**
     * @var AgpRepository
     */
    protected $agpRepository;

    /**
     * @var AgpGeneriqueRepository
     */
    protected $agpGeneriqueRepository;

    protected $interventionHelper;

    /**
     * @var CommutationRessourceService
     */
    protected $commutationRessource;

    /**
     * @var GlobalApiUrlService
     */
    protected $globalApiService;

    /**
     * @var DiagsdhService
     */
    protected $diagSdh;

    /**
     * @var AstroLienRepository
     */
    protected $astroLienRepository;

    /**
     * @var AstroIhmSqlRepository
     */
    protected $astroIhmSqlRepository;

    /**
     * @var AireleService
     */
    protected $airele;

    /**
     * @var CiaService
     */
    protected $ciaService;

    /**
     * @var VariableService
     */
    protected $variableService;

    /**
     * @var DemandeInterventionService
     */
    protected $demandeIntervention;

    /**
     * @var OceaneService
     */
    protected $oceaneService;

    /**
     * @var GlobalApiRepository
     */
    protected $globalApiRepository;

    /**
     * @var AdminFonctionService
     */
    protected $adminFonction;

    /**
     * @var Application
     */
    protected $app;

    const ISO_8859_15 = 'ISO-8859-15';
    protected $messageFile;
    private $cuidUpdate;
    private $ticketId;
    private $eds;
    private $typeRessource;
    protected $getoceane;
    protected $loginId;


    public function __construct($app)
    {
        $this->app = $app;
        $this->edrRepository = $app->get('EdrRepository');
        $this->edrService = $app->get('Edr');
        $this->agpRepository = $app->get('AgpRepository');
        $this->astroRepository = $app->get('AstroRepository');
        $this->agpGeneriqueRepository = $app->get('AgpGeneriqueRepository');
        $this->interventionHelper = new DemandeIntervention($this->app);
        $this->diagSdh = $app->get('DiagSdh');
        $this->astroLienRepository = $app->get('AstroLienRepository');
        $this->messageFile = $this->app->config['message_file'];
        $this->getOceane = $this->app->get('OceaneGet');
        $this->loginId = (key_exists('api', $this->app->config) && $this->app->config['api']) ? $this->getLogin() : $this->app->get('Session')->getUtilisateurLogin();

    }

    /**
     * Première initialisation Agir-Piloter
     *
     * @param integer $id_ticket_astro
     *            Id du ticket Astro
     * @return array
     */
    public function initAgp($astroId, $ticketId, $droitAgir, $cmd, $guestEds)
    {
        // Obligatoire car dans certains cas, ID_RESSOURCE_DSLAM n'est pas dans la variable $_SESSION
        $astroSession = $this->app->get('Session')->get('astroOft' . $ticketId);
        $idRessource = $astroSession['id_ressource'];
        $rsc = $this->astroRepository->getRessource($idRessource);
        $idRscDslam = $rsc['ID_RESSOURCE_DSLAM'];

        if ($this->edrRepository->testDataInfo($astroId) == 0) {
            $msg = $this->interventionHelper->getIndispoMessage();
            return array(
                'msg' => $msg
            );
        } else {
            $dslamData = $this->edrRepository->getBlobDslam($idRscDslam)['BLOBDATA'];
            $result = json_decode(utf8_encode($dslamData), true)[0];

            return $this->displayAgp1($result, $astroId, $rsc, $idRessource, $ticketId, $droitAgir, $cmd, $guestEds);
        }
    }

    /**
     * Affichage Ecran 1 - Classique DI
     *
     * @param array $deports
     *            Déports du DSLAM
     * @param string $master
     *            Maître du DSLAM
     * @param string $dslamName
     *            Nom du DSLAM
     * @param integer $astroId
     *            Id du ticket Astro
     * @param array $rsc
     *            Informations sur la ressource
     * @param integer $idRessource
     *            ID de la ressource
     * @param string $ticketId
     *            Numero du ticket
     * @param string $droitAgir
     *            les droit d'agir
     * @param string $cmd
     *            la commande demandée
     * @return array
     */
    public function displayAgp1($result, $astroId, $rsc, $idRessource, $ticketId, $droitAgir, $cmd, $guestEds)
    {
        $helper = new Edr();
        $hDeports = '';
        $tDeports = array();
        $idRscMaster = '';

        $deports = (isset($result['offsets']) ? $result['offsets'] : array());
        $master = (isset($result['masterName']) ? $result['masterName'] : '');
        $dslamName = (isset($result['equipmentName']) ? $result['equipmentName'] : '');

        $typeCollecte = (isset($result['techno']) ? $result['techno'] : '');
        $constructeur = (isset($result['constructor']) ? $result['constructor'] : '');
        $technologie = (isset($result['category']) ? $result['category'] : '');

        $astroSession = $this->app->get('Session')->get('astroOft' . $ticketId);

        $typeRessource = $astroSession['type_ressource'];

        $droitAstro = new DroitAstroTools($this->app);
        $droitEds = $droitAstro->droitEds($ticketId, $astroSession['connectedgroup'], $astroSession['pilotgroup']);

        if (count($deports) > 0) {
            foreach ($deports as $v) {
                $maitreDeport = $this->edrService->getDataMaitreDeport($v, false);
                if ($maitreDeport['status'] == 'ok') {
                    $tDeports[$maitreDeport['id_rsc']] = $v;
                }
            }
            $hDeports .= $this->interventionHelper->getDeports($tDeports, 'agp_deport', '90', '', 'choisir', $droitEds['guest']);
        }

        $hMaster = '';
        if ($master != '' && $master != $dslamName) {
            $maitreDeport = $this->edrService->getDataMaitreDeport($master, false);
            $idRscMaster = $maitreDeport['id_rsc'];
            if ($maitreDeport['status'] == 'nok') {
                $hMaster = $this->interventionHelper->getHMaster($master, true, $droitEds['guest']);
            } else {
                $hMaster = $this->interventionHelper->getHMaster($master, false, $droitEds['guest']);
            }
        }

        // Récupération de l'Alarme et construction bloc du Centre
        $alarme = $helper->getIntituleAla($rsc, false);
        $dslam = '';
        if ($alarme != $dslamName) {
            $dslam = $this->interventionHelper->getDslamNameInput($dslamName, $droitEds['guest']);
        }
        $dslam .= $this->interventionHelper->getDslamAlarmeInput($alarme, $droitEds['guest']);
        $agpEds = $this->agpRepository->getEntite();

        $teleactionListe = $this->agpRepository->getAllTeleaction($constructeur, $technologie, $typeCollecte);
        foreach ($teleactionListe as $key => $v) {
            $teleactionListe[$key]['LIBELLE_IHM'] = str_replace('etat', 'état', $teleactionListe[$key]['LIBELLE_IHM']);
        }

        $chassisCarte = $this->astroRepository->getCarteTicket($ticketId);
        $listCartes = $this->getCartesLignes($chassisCarte['CHASSIS'], $result);
        $isCarteLigne = (isset($chassisCarte['CARTE']) && in_array($chassisCarte['CARTE'], $listCartes)) ? 'true' : 'false';

        if ($typeRessource == 'DSLAM') {
            $demandeInterventionForm = new DemandeInterventionForm(null, array(
                'app' => $this->app,
                'agp_entite' => $agpEds,
                'agp_id_astro' => $astroId,
                'agp_id_rsc' => $idRessource,
                'agp_id_rsc_dslam' => $rsc['ID_RESSOURCE_DSLAM'],
                'agp_id_rsc_master' => $idRscMaster,
                'agp_id_rsc_ec' => $idRessource,
                'astroid' => $astroId,
                'ticketid' => $ticketId,
                'droit_agir' => $droitAgir,
                'agp_deports' => $deports,
                'agp_master' => $master,
                'agp_dslam' => $dslam,
                'dslam_name' => $dslamName,
                'alarme' => $alarme,
                'guest_eds' => $guestEds,
                'agp_teleaction' => $teleactionListe,
                'is_carte_ligne' => $isCarteLigne,
                'is_dslam' => true
            ));
        } else {
            $demandeInterventionForm = new DemandeInterventionForm(null, array(
                'app' => $this->app,
                'agp_entite' => $agpEds,
                'agp_id_astro' => $astroId,
                'agp_id_rsc' => $idRessource,
                'agp_id_rsc_dslam' => $rsc['ID_RESSOURCE_DSLAM'],
                'agp_id_rsc_master' => $idRscMaster,
                'agp_id_rsc_ec' => $idRessource,
                'astroid' => $astroId,
                'ticketid' => $ticketId,
                'droit_agir' => $droitAgir,
                'agp_deports' => $deports,
                'agp_master' => $master,
                'agp_dslam' => $dslam,
                'dslam_name' => $dslamName,
                'alarme' => $alarme,
                'guest_eds' => $guestEds,
                'agp_teleaction' => $teleactionListe,
                'is_carte_ligne' => $isCarteLigne,
                'is_dslam' => false));

        }
        if ($typeRessource == 'DSLAM') {
            return array(
                'form' => $demandeInterventionForm,
                'cmd' => $cmd,
                'agp_deports' => $hDeports,
                'agp_master' => $hMaster,
                'agp_dslam' => $dslam,
                'agp_entite' => $agpEds,
                'non_agir' => '',
                'actif_eds' => $droitEds['droit_actif'],
                'guest_eds' => $droitEds['guest'],
                'type_ressource' => $typeRessource,
            );
        } else {
            return array(
                'form' => $demandeInterventionForm,
                'cmd' => $cmd,
                'agp_deports' => $hDeports,
                'agp_master' => $hMaster,
                'agp_dslam' => $dslam,
                'agp_entite' => $agpEds,
                'non_agir' => '',
                'actif_eds' => $droitEds['droit_actif'],
                'guest_eds' => $droitEds['guest'],
                'ticketid' => $ticketId,
                'astroid' => $astroId,
                'droit_agir' => $droitAgir,
                'type_ressource' => $typeRessource,

            );
        }
    }

    /**
     * Affichage Ecran 2
     *
     * @param integer $idTicketAstro
     *            Id du ticket Astro
     * @param integer $idAction
     *            Id de l'action selectionnée
     * @param integer $idRsc
     *            Id de la ressource choisie
     * @param integer $ticketId
     *            Id du ticket
     * @return array
     */
    public function displayAGP2($idTicketAstro, $idAction, $idRsc, $ticketId, $equipmentName, $isReset)
    {
        $agpChoix = '';
        // Récupération des données en base pour la requête (ressource Dslam)
        $dslamData = $this->edrRepository->getBlobDslam($idRsc);
        $result = json_decode(utf8_encode($dslamData['BLOBDATA']), true)[0];

        $chx = $this->agpRepository->getActionChoix($idAction);
        $chassis = $this->agpRepository->getDataAlarme($idTicketAstro)['CHASSIS'];

        $agpChoix = $this->interventionHelper->getAgpChoix($chassis, $chx, $result);

        $demandeInterventionSecondForm = new DemandeInterventionSecondForm(null, array(
            'app' => $this->app,
            'agp_id_astro' => $idTicketAstro,
            'agp_id_rsc' => $idRsc,
            'agp_id_action' => $idAction,
            'ticketid' => $ticketId,
            'equipement_name' => $equipmentName,
            'is_reset' => $isReset
        ));

        return array(
            'form' => $demandeInterventionSecondForm,
            'agp_choix' => $agpChoix,
            'ticket_id' => $ticketId,
            'agp_id_astro' => $idTicketAstro,
            'agp_title' => 'ASTRO - Agir Piloter n°' . $ticketId,
            'equipement_name' => $equipmentName,
            'is_reset' => $isReset
        );
    }

    /**
     * Affichage Ecran 3
     *
     * @param array $Data
     *            Contenu du POST
     * @param string $oPriority
     *            Priorité Océane
     * @param string $oPRDate
     *            Date de rétablissement planifiée Océane
     * @param integer $ticketId
     *            Id du ticket
     * @return string
     */
    public function displayAGP3($data, $oPriority, $oPRDate, $ticketId)
    {
        $Params = $this->agpRepository->getParams();
        $astroSession = $this->app->get('Session')->get('astroOft' . $ticketId);

        $agpEntiteActivee = $data['entite'];
        $agpModeActivation = (strpos($data['activation'], 'EDS ') !== false ? 'EDS' : $data['activation']);
        $agpActivation = $data['activation'];
        $agpEds = str_replace(array(
            'CADI',
            'CADI HNO',
            'EDS '
        ), array(
            '',
            '',
            ''
        ), $data['activation']);
        $agpSuivreHno = ($oPriority == 1 || $data['hno'] == 1 ? '1' : '0');

        // Niveau d'urgence suivant l'entité et la Priorité Océane
        $ParamsEnt = $this->agpRepository->getParamsEntite($data['id_entite'], $data['hno']);

        $k = $ParamsEnt['ID_URGENCE_P' . $oPriority];
        $agpUrgence = $this->interventionHelper->setSelect('1', $Params['OCEANE_NIVEAU_URGENCE']['VALEUR'], '170', 'agp_urgence', $k);
        $agpActionEds = $this->interventionHelper->select($Params['ACTION_EN_COURS_EDS']['VALEUR'], 'agp_actionencours', '220', '', '', $data['id_action_encours']);
        $agpDtretabDRI = $oPRDate['agp_dt_retab_dri'];
        $agpDtretabDRC = $oPRDate['agp_dt_retab_drc'];

        $date = $this->agpRepository->calcDateOuvree($oPriority, $data['id_entite'], $data['hno']);

        $agpDtEnCours = $date;
        $agpIdAstro = key_exists('agp_id_astro', $data) ? $data['agp_id_astro'] : null;
        $agpIdRsc = key_exists('agp_id_rsc', $data) ? $data['agp_id_rsc'] : null;
        $agpIdAction = key_exists('agp_id_action', $data) ? $data['agp_id_action'] : null;
        $agpChassis = key_exists('agp_chassis', $data) ? $data['agp_chassis'] : null;
        $agpCarte = key_exists('agp_carte', $data) ? $data['agp_carte'] : null;
        $agpPeriph = key_exists('agp_periph', $data) ? $data['agp_periph'] : null;
        $agpLien = key_exists('agp_lien', $data) ? $data['agp_lien'] : null;

        $commentaire = new AgpCC($this->app, array(
            'Id_astro' => $agpIdAstro,
            'Id_rsc' => $agpIdRsc,
            'Id_action' => $agpIdAction,
            'Chassis' => $agpChassis,
            'Cartes' => $agpCarte,
            'Periphs' => $agpPeriph,
            'Liens' => $agpLien,
            'EDSPilote' => $astroSession['pilotgroup']
            // 'Alarme'=>$_SESSION['astro'.$data['agp_id_astro']]['ressource'] )
        ));
        $agpCommentaire = $commentaire->getCommentaire();
        return array(
            'agp_entite_activee' => $agpEntiteActivee,
            'agp_mode_activation' => $agpModeActivation,
            'agp_activation' => $agpActivation,
            'agp_eds' => $agpEds,
            'agp_suivre_hno' => $agpSuivreHno,
            'agp_urgence' => $agpUrgence,
            'agp_action_eds' => $agpActionEds,
            'agp_dt_retab_dri' => $agpDtretabDRI,
            'agp_dt_retab_drc' => $agpDtretabDRC,
            'agp_dt_en_cours' => $agpDtEnCours,
            'agp_commentaire' => $agpCommentaire
        );
    }

    /**
     * Options du select des Actions
     *
     * @param integer $idEntite
     *            Entité choisie
     * @param boolean $hno
     *            Choix HO/Astreinte
     * @param integer $idTicketAstro
     *            Id du Ticket Astro
     * @param integer $idRsc
     *            Id de la ressource choisie
     * @param integer $idRscDslam
     *            Id de la ressource du dslam (dslam,déport ou maître)
     * @return string
     */
    public function getOptionsActions($idEntite, $hno, $idRsc, $idRscDslam)
    {
        // Récupération des données en base pour la requête (ressource Dslam)
        $dslamData = $this->edrRepository->getBlobDslam($idRscDslam);
        $result = json_decode(utf8_encode($dslamData['BLOBDATA']), true)[0];

        $dataEdr = array(
            'techno' => $result['techno'],
            'constructor' => $result['constructor'],
            'rank' => $result['rank'],
            'category' => $result['category']
        );
        $act = $this->agpRepository->getAction($idEntite, $hno, $idRsc, $dataEdr);

        return $this->interventionHelper->getOptionsActionsHelp($act);

    }

    /**
     * Affichage Ecran 1 Generique DI
     *
     * @param array $idJeuParam
     *            ID du jeu de paramètre
     * @param integer $astroId
     *            Id du ticket Astro
     * @param integer $ticketId
     *            Id du ticket
     * @param string $droitAgir
     *            les droit d'agir
     * @param string $cmd
     *            la commande demandée
     * @param string $guestEds
     *            EDS guest
     * @return array
     */
    public function displayAgp1Generique($idJeuParam, $astroId, $ticketId, $droitAgir, $cmd, $guestEds)
    {
        $astroSession = $this->app->get('Session')->get('astroOft' . $ticketId);
        $typeRessource = $astroSession['type_ressource'];

        if ($typeRessource == 'DSLAM') {
            $idRscMaster = '';
            $dslam = '';
            $helper = new Edr();
            $hDeports = '';
            $tDeports = array();
            $listCartes = array();
            $isCarteLigne = false;
        }

        if ($typeRessource == 'DSLAM') {
            $idRessource = $astroSession['id_ressource'];
            $rsc = $this->astroRepository->getRessource($idRessource);
            $idRscDslam = $rsc['ID_RESSOURCE_DSLAM'];
        }
        $droitAstro = new DroitAstroTools($this->app);
        $droitEds = $droitAstro->droitEds($ticketId, $astroSession['connectedgroup'], $astroSession['pilotgroup']);
        $agpFamille = $this->agpGeneriqueRepository->getFamille($idJeuParam, $astroSession['type_ressource']);
        $agpEntite = $this->agpGeneriqueRepository->getEntiteByJeuFamille($idJeuParam, $astroSession['type']);

        if ($typeRessource == 'DSLAM') {

            $alarme = $helper->getIntituleAla($rsc, false);

            $dslamData = $this->edrRepository->getBlobDslam($idRscDslam)['BLOBDATA'];
            $result = json_decode(utf8_encode($dslamData), true)[0];

            $typeCollecte = (isset($result['techno']) ? $result['techno'] : '');
            $constructeur = (isset($result['constructor']) ? $result['constructor'] : '');
            $technologie = (isset($result['category']) ? $result['category'] : '');

            $teleactionListe = $this->agpRepository->getAllTeleaction($constructeur, $technologie, $typeCollecte);
            foreach ($teleactionListe as $key => $v) {
                $teleactionListe[$key]['LIBELLE_IHM'] = str_replace('etat', 'état', $teleactionListe[$key]['LIBELLE_IHM']);
            }
            $deports = (isset($result['offsets']) ? $result['offsets'] : array());
            $master = (isset($result['masterName']) ? $result['masterName'] : '');
            $dslamName = (isset($result['equipmentName']) ? $result['equipmentName'] : '');

            if ($alarme != $dslamName) {
                $dslam = $this->interventionHelper->getDslamNameInput($dslamName, $droitEds['guest']);
            }
            $dslam .= $this->interventionHelper->getDslamAlarmeInput($alarme, $droitEds['guest']);

            if (count($deports) > 0) {
                foreach ($deports as $v) {
                    $maitreDeport = $this->edrService->getDataMaitreDeport($v, false);
                    if ($maitreDeport['status'] == 'ok') {
                        $tDeports[$maitreDeport['id_rsc']] = $v;
                    }
                }
                $hDeports .= $this->interventionHelper->getDeports($tDeports, 'agp_deport', '90', '', 'choisir', $droitEds['guest']);
            }

            $hMaster = '';
            if ($master != '' && $master != $dslamName) {
                $maitreDeport = $this->edrService->getDataMaitreDeport($master, false);
                $idRscMaster = $maitreDeport['id_rsc'];
                if ($maitreDeport['status'] == 'nok') {
                    $hMaster = $this->interventionHelper->getHMaster($master, true, $droitEds['guest']);
                } else {
                    $hMaster = $this->interventionHelper->getHMaster($master, false, $droitEds['guest']);
                }
            }

            $chassisCarte = $this->astroRepository->getCarteTicket($ticketId);

            if (!is_null($chassisCarte) && $chassisCarte && key_exists('CHASSIS', $chassisCarte)) {
                $listCartes = $this->getCartesLignes($chassisCarte['CHASSIS'], $result);
                $isCarteLigne = (isset($chassisCarte['CARTE']) && in_array($chassisCarte['CARTE'], $listCartes)) ? 'true' : 'false';
            }


        }

        if ($typeRessource == 'MIE') {
            $args[] = 'FG_NOMNAEQP';

        }

        if ($typeRessource == 'SLN' || $typeRessource == 'WDM_SID') {
            $args[] = 'FG_E1NOMNAEQP';

            $args[] = 'FG_E2NOMNAEQP';
        }

        if ($typeRessource == 'DSLAM') {
            $demandeInterventionGeneriqueForm = new DemandeInterventionGeneriqueForm(null, array(
                'app' => $this->app,
                'agp_famille' => $agpFamille,
                'agp_entite' => $agpEntite,
                'agp_id_astro' => $astroId,
                'astroid' => $astroId,
                'ticketid' => $ticketId,
                'droit_agir' => $droitAgir,
                'guest_eds' => $guestEds,
                'agp_id_rsc' => $idRessource,
                'agp_id_rsc_dslam' => $rsc['ID_RESSOURCE_DSLAM'],
                'agp_id_rsc_master' => $idRscMaster,
                'agp_id_rsc_ec' => $idRessource,
                'is_carte_ligne' => $isCarteLigne,
                'agp_deports' => $deports,
                'agp_master' => $master,
                'agp_dslam' => $dslam,
                'dslam_name' => $dslamName,
                'alarme' => $alarme,
                'agp_teleaction' => $teleactionListe,
                'is_dslam' => true
            ));
        } else {
            $demandeInterventionGeneriqueForm = new DemandeInterventionGeneriqueForm(null, array(
                'app' => $this->app,
                'agp_famille' => $agpFamille,
                'agp_entite' => $agpEntite,
                'agp_id_astro' => $astroId,
                'astroid' => $astroId,
                'ticketid' => $ticketId,
                'droit_agir' => $droitAgir,
                'guest_eds' => $guestEds,
                'is_dslam' => false
            ));
        }
        if ($typeRessource == 'DSLAM') {
            return array(
                'form' => $demandeInterventionGeneriqueForm,
                'cmd' => $cmd,
                'agp_entite' => $agpEntite,
                'non_agir' => '',
                'actif_eds' => $droitEds['droit_actif'],
                'guest_eds' => $droitEds['guest'],
                'agp_famille' => $agpFamille,
                'id_jeu' => $idJeuParam,
                'ticketid' => $ticketId,
                'astroid' => $astroId,
                'droit_agir' => $droitAgir,
                'agp_deports' => $hDeports,
                'agp_master' => $hMaster,
                'agp_dslam' => $dslam,
                'type_ressource' => $typeRessource
            );
        } else {
            return array(
                'form' => $demandeInterventionGeneriqueForm,
                'cmd' => $cmd,
                'agp_entite' => $agpEntite,
                'non_agir' => '',
                'actif_eds' => $droitEds['droit_actif'],
                'guest_eds' => $droitEds['guest'],
                'agp_famille' => $agpFamille,
                'id_jeu' => $idJeuParam,
                'ticketid' => $ticketId,
                'astroid' => $astroId,
                'droit_agir' => $droitAgir,
                'type_ressource' => $typeRessource
            );
        }
    }

    public function getCommentaireByType($idCommentaire, $type, $ticketId)
    {
        $commentairePiolter = $this->app->get('AdminCommentaireRepository')->getCommentairePerType($idCommentaire, $type);
        $variables = OceaneTools::getContents($commentairePiolter, '###', '###');

        return $this->app->get('Variable')->replaceTagsChaine($commentairePiolter, $variables, $type, $ticketId);
    }

    public function getOptionsCommentaireGenerique($idAction, $type)
    {
        $actions = $this->app->get('AdminCommentaireRepository')->getListeCommentairePilotagePerAction($idAction, $type);
        return $this->interventionHelper->getOptionsActionCommentaireGenerique($actions);
    }

    public function getOptionsActionsGenerique($idEntite, $hno, $idJeuParam, $typeRessource, $identifiants, $data)
    {
        $filtre = $idRsc = $edrDslEquipe = '';
        $dataDslam = array();

        if ($typeRessource == 'COMMUT' || $typeRessource == 'UNIRACC' || $typeRessource == 'CONNUM' || $typeRessource == 'MICBPNCSN' || $typeRessource == 'MICBPNCAA' || $typeRessource == 'MICBPNCOM') {
            $this->commutationRessource = $this->app->get('CommutationRessource');
            $filtre = $this->commutationRessource->varSystemeCommut($identifiants, $typeRessource);
        }
        if (($typeRessource == 'DSLAM' || $typeRessource == 'DSLAMDERCO') && $data['id_rsc'] != '' && $data['id_rsc_dslam'] != '') {
            $idRsc = $data['id_rsc'];
            $dataEdr = $this->edrRepository->getBlobDslam($data['id_rsc_dslam'])['BLOBDATA'];
            $ressource = $this->astroRepository->getRessource($data['id_rsc_dslam'] != $data['id_rsc'] ? $data['id_rsc'] : $data['id_rsc_dslam']);
            $ressource = is_array($ressource) && key_exists('DSLAM', $ressource) ? $ressource['DSLAM'] : '';
            if (!empty($ressource)) {
                $edrDslEquipe = $this->edrRepository->getDslEquipement($ressource);
            }
            $typeNro = is_array($edrDslEquipe) && key_exists('TYPE_NRO', $edrDslEquipe) && isset($edrDslEquipe['TYPE_NRO']) ? $edrDslEquipe['TYPE_NRO'] : '';
            $dataDslam = Json::decode(StringTools::convertEncoding($dataEdr, 'UTF-8', self::ISO_8859_15), true)[0];
            $dataDslam['type_nro'] = $typeNro;
        }
        $idActivationUi = $this->app->config['action_activation_ui'];
        $action = $this->agpGeneriqueRepository->getAction($idEntite, $hno, $idJeuParam, $typeRessource, $filtre, $idActivationUi, $dataDslam, $idRsc);
        return $this->interventionHelper->getOptionsActionGenerique($action);
    }

    public function displayPiloterGenerique($data, $oceaneData, $ticketId, $idJeuParam, $api = false)
    {
        if (!$api) {
            $astroSession = $this->app->get('Session')->get('astroOft' . $ticketId);
        }
        $oceaneAssistant = new OceaneAssistant($this->app);
        $agpEntiteActivee = StringTools::convertEncoding($data['entite'], self::ISO_8859_15, 'UTF-8');
        $modeActivation = explode(" ", $data['activation']);
        $agpModeActivation = (strpos($data['activation'], 'EDS ') !== false) ? 'EDS' : $modeActivation[0];
        $agpActivation = $data['activation'];
        $agpEds = $data['agp_eds'];
        $agpSuivreHno = 0;

        if ($oceaneData['herite_oceane_hno'] == 1) {
            $agpSuivreHno = $oceaneData['herite_oceane_hno'] == 1 ? $oceaneData['herite_oceane_hno'] : 0;
        } else {
            $priorityHoHno = $this->agpGeneriqueRepository->getActivationHoHnoByJeu($idJeuParam, $oceaneData['oceane_priority']);

            if (key_exists($oceaneData['oceane_priority'], $priorityHoHno)) {
                if ($data['agp_ho_hno_generique'] == 'HO' && $priorityHoHno[$oceaneData['oceane_priority']]['activation_ho'] == '1') {
                    $agpSuivreHno = 0;
                } elseif ($data['agp_ho_hno_generique'] == 'HNO' && $priorityHoHno[$oceaneData['oceane_priority']]['activation_hno'] == '1') {
                    $agpSuivreHno = 1;
                }
            }
        }

        // Niveau d'urgence suivant l'entité et la Priorité Océane
        $agpUrgence = $this->agpGeneriqueRepository->getValeurParametres($idJeuParam, 'NIVEAU_URGENCE');
        $idActionEnCoursEds = $oceaneData['herite_oceane_action_en_cours'];

        $agpDtretab = $oceaneData['opr_date'];

        $idUrgenceOceane = $this->agpGeneriqueRepository->getIdentifiantUrgenceByValeurParametres($idJeuParam, 'NIVEAU_URGENCE', $oceaneData['herite_oceane_niveau_urgence']);
        if (key_exists('herite_oceane_date_action_en_cours', $oceaneData)) {
            $agpDtEnCoursOceane = $oceaneData['herite_oceane_date_action_en_cours'];
        } else {
            $agpDtEnCoursOceane = '';
        }
        $agpIdAction = key_exists('agp_action_generique', $data) ? $data['agp_action_generique'] : null;
        $agpCommentaire = $this->agpGeneriqueRepository->getCommentaireByAction($idJeuParam, $agpIdAction);

        $variables = OceaneTools::getContents($agpCommentaire['COMMENTAIRE'], '###', '###');
        $commentaire = $this->app->get('Variable')->replaceTagsChaine($agpCommentaire['COMMENTAIRE'], $variables, $astroSession['type'], $ticketId);

        $blocs = OceaneTools::getContents($agpCommentaire['COMMENTAIRE'], '##bloc_', '##');
        if (!empty($blocs) && key_exists(0, $blocs)) {
            foreach ($blocs as $blocName) {
                if ($blocName != 'choix_de_carte_trans' && $blocName != 'Types_Carte' && $blocName != 'Types' && $blocName != 'Carte_EAN' && $blocName != 'Complet') {
                    $blocVariable = $this->agpGeneriqueRepository->getBlocVariable($blocName);
                    $commentaire = str_replace('##bloc_' . $blocName . '##', $blocVariable, $commentaire);
                }
            }
        }
        if (is_string($data['id_commentaire']) && $data['id_commentaire'] == 'DiagSDH') {
            $accessNumber = $this->diagSdh->getAccessNumber($astroSession);
            $diagSdhData = $this->diagSdh->getDiagSdhInfos($accessNumber);
            $commentaire = is_array($diagSdhData) && !key_exists('message', $diagSdhData) ? $this->diagSdh->getCommentaireCharteActivationUiTicket($diagSdhData) : '';

        }
        $agpCommentaire['COMMENTAIRE'] = $commentaire;

        return array(
            'agp_entite_activee' => $agpEntiteActivee,
            'agp_mode_activation' => $agpModeActivation,
            'agp_activation' => $agpActivation,
            'agp_eds' => $agpEds,
            'agp_suivre_hno' => $agpSuivreHno,
            'agp_urgence' => $agpUrgence,
            'agp_action_eds' => $idActionEnCoursEds,
            'agp_dt_retab' => ($agpDtretab != '') ? $oceaneAssistant->changeUTCToDate($agpDtretab) : $agpDtretab,
            'agp_dt_retab_requested' => $oceaneData['orreq_date'],
            'agp_dt_en_cours' => $agpDtEnCoursOceane,
            'agp_dt_en_cours_oceane' => ($agpDtEnCoursOceane != '') ? $oceaneAssistant->changeUTCToDate($agpDtEnCoursOceane) : $agpDtEnCoursOceane,
            'agp_commentaire' => $agpCommentaire,
            'id_urgence' => $idUrgenceOceane,
            'id_action_en_cours' => $idActionEnCoursEds
        );
    }

    public function getCommentaireAgp2Generique($data)
    {
        $astroSession = $this->app->get('Session')->get('astroOft' . $data['ticketId']);
        $agpIdAstro = key_exists('agp_id_astro', $data) ? $data['agp_id_astro'] : null;
        $agpIdRsc = key_exists('agp_id_rsc', $data) ? $data['agp_id_rsc'] : null;
        $agpIdAction = key_exists('agp_id_action', $data) ? $data['agp_id_action'] : null;
        $agpChassis = key_exists('agp_chassis', $data) ? $data['agp_chassis'] : null;
        $agpCarte = key_exists('agp_carte', $data) ? $data['agp_carte'] : null;
        $agpPeriph = key_exists('agp_periph', $data) ? $data['agp_periph'] : null;
        $agpLien = key_exists('agp_lien', $data) ? $data['agp_lien'] : null;
        $comm = new AgpCC($this->app, array(
            'Id_astro' => $agpIdAstro,
            'Id_rsc' => $agpIdRsc,
            'Id_action' => $agpIdAction,
            'Chassis' => $agpChassis,
            'Cartes' => $agpCarte,
            'Periphs' => $agpPeriph,
            'Liens' => $agpLien,
            'EDSPilote' => $astroSession['pilotgroup'],
            'intervenant' => $data['intervenant'] ? $data['intervenant'] : ''
        ), $data['idJeu']);

        $variables = OceaneTools::getContents($comm->getCommentaire(), '###', '###');
        $commentaire = $this->app->get('Variable')->replaceTagsChaine($comm->getCommentaire(), $variables, $astroSession['type'], $data['ticketId']);
        $comm->setCommentaire($commentaire);
        return $comm;

    }

    public function displayAgp2Generique($data, $oceaneData, $ticketId, $idJeuParam, $api = false)
    {
        if (!$api) {
            $astroSession = $this->app->get('Session')->get('astroOft' . $ticketId);
            $data['connected_group'] = $astroSession['connectedgroup'];
        }
        $oceaneAssistant = new OceaneAssistant($this->app);
        $agpEntiteActivee = StringTools::convertEncoding($data['entite'], self::ISO_8859_15, 'UTF-8');
        $modeActivation = explode(" ", $data['activation']);
        $agpModeActivation = (strpos($data['activation'], 'EDS ') !== false) ? 'EDS' : $modeActivation[0];
        $agpActivation = $data['activation'];
        $agpEds = $data['agp_eds'];
        $agpSuivreHno = 0;
        $agpTransferer = 0;

        if ($oceaneData['herite_oceane_hno'] == 1) {
            $agpSuivreHno = $oceaneData['herite_oceane_hno'] == 1 ? $oceaneData['herite_oceane_hno'] : 0;
        } else {
            $priorityHoHno = $this->agpGeneriqueRepository->getActivationHoHnoByJeu($idJeuParam, $oceaneData['oceane_priority']);

            if (key_exists($oceaneData['oceane_priority'], $priorityHoHno)) {
                if ($data['agp_ho_hno_generique'] == 'HO' && $priorityHoHno[$oceaneData['oceane_priority']]['activation_ho'] == '1') {
                    $agpSuivreHno = 0;
                } elseif ($data['agp_ho_hno_generique'] == 'HNO' && $priorityHoHno[$oceaneData['oceane_priority']]['activation_hno'] == '1') {
                    $agpSuivreHno = 1;
                }
            }
        }

        /* Récuperer le paramétrage des champs heritee oceane */
        $isValeurNiveauUrgenceHeriteeOceane = $this->agpGeneriqueRepository->getValeurHeriteeOceaneByJeuParam($idJeuParam, 'NIVEAU_URGENCE');

        // Niveau d'urgence suivant l'entité et la Priorité Océane
        $paramsUrgence = $this->agpGeneriqueRepository->getParamsUrgence($data['id_entite'], $data['hno'], $idJeuParam);
        $agpUrgence = $this->agpGeneriqueRepository->getValeurParametres($idJeuParam, 'NIVEAU_URGENCE');
        $agpActionEds = $this->agpGeneriqueRepository->getValeurParametres($idJeuParam, 'ACTION_EN_COURS_EDS');
        $idActionEnCoursEds = ($oceaneData['is_action_eds_heritee_oceane'] == 1) ? $oceaneData['herite_oceane_action_en_cours'] : $paramsUrgence[$oceaneData['oceane_priority']]['id_action_en_cours_eds'];

        $agpDtretab = $oceaneData['opr_date'];

        $idUrgence = $paramsUrgence[$oceaneData['oceane_priority']]['id_urgence'];
        $idUrgenceOceane = $this->agpGeneriqueRepository->getIdentifiantUrgenceByValeurParametres($idJeuParam, 'NIVEAU_URGENCE', $oceaneData['herite_oceane_niveau_urgence']);
        $agpDtEnCours = $this->agpGeneriqueRepository->calcDateOuvreeGenerique($oceaneData['oceane_priority'], $data['id_entite'], $data['hno']);
        if (key_exists('herite_oceane_date_action_en_cours', $oceaneData)) {
            $agpDtEnCoursOceane = $oceaneData['herite_oceane_date_action_en_cours'];
        } else {
            $agpDtEnCoursOceane = '';
        }
        $agpIdAction = key_exists('agp_action_generique', $data) ? $data['agp_action_generique'] : null;

        $agpCommentaire = $this->agpGeneriqueRepository->getCommentaireByAction($idJeuParam, $agpIdAction);
        $data['id_valeur'] = $agpCommentaire['ID_COMMENTAIRE'];
        if (key_exists('intervenant', $data) && $data['intervenant'] != '') {
            $segComment = $this->app->get('AdminCommentaireRepository')->getCommentaireSecondaireByIntervenant($data);
            if (is_array($segComment) && isset($segComment['SECOND_COMMENT']) && trim($segComment['SECOND_COMMENT']) !== '') {
                $agpCommentaire['COMMENTAIRE'] = $segComment['SECOND_COMMENT'];
            }

        }

        $refCom = $this->agpRepository->getRefCommentaire();
        $commentaire = $agpCommentaire['COMMENTAIRE'];


        $isDslamTest = false;
        if ($api) {
            if ($data['type_ressource'] == 'DSLAM' || $data['type_ressource'] == 'DSLAMDERCO') {
                $isDslamTest = true;
            }
            $astroSession['type'] = $data['type_ressource'];
            $astroSession['ticketid'] = $ticketId;
        } else {
            if ($astroSession['type'] == 'DSLAM' || $astroSession['type'] == 'DSLAMDERCO') {
                $isDslamTest = true;
            }
        }

        $blocs = OceaneTools::getContents($agpCommentaire['COMMENTAIRE'], '##bloc_', '##');

        if (!empty($blocs) && key_exists(0, $blocs)) {
            foreach ($blocs as $blocName) {
                if ($isDslamTest) {
                    $blocVariable = $this->agpGeneriqueRepository->getBlocVariable($blocName);
                    $blocVariableContent = $refCom['' . $blocVariable . ''];
                    $commentaire = str_replace('##bloc_' . $blocName . '##', $blocVariableContent, $commentaire);
                } elseif ($blocName != 'choix_de_carte_trans' && $blocName != 'Types_Carte' && $blocName != 'Types' && $blocName != 'Carte_EAN' && $blocName != 'Complet') {
                    $blocVariable = $this->agpGeneriqueRepository->getBlocVariable($blocName);
                    $commentaire = str_replace('##bloc_' . $blocName . '##', $blocVariable, $commentaire);
                }
            }
        }
        if (is_string($data['id_commentaire']) && $data['id_commentaire'] == 'DiagSDH') {
            $astroSession['class'] = $oceaneData['class'];
            $astroSession['id1'] = $oceaneData['id1'];
            $astroSession['id2'] = $oceaneData['id2'];
            $astroSession['id3'] = $oceaneData['id3'];
            $accessNumber = $this->diagSdh->getAccessNumber($astroSession);
            $diagSdhData = $this->diagSdh->getDiagSdhInfos($accessNumber);
            $commentaire = is_array($diagSdhData) && !key_exists('message', $diagSdhData) ? $this->diagSdh->getCommentaireCharteActivationUiTicket($diagSdhData) : '';

        }


        if ($isDslamTest) {
            $agpIdAstro = key_exists('agp_id_astro', $data) ? $data['agp_id_astro'] : null;
            $agpIdRsc = key_exists('agp_id_rsc', $data) ? $data['agp_id_rsc'] : null;
            $agpIdAction = key_exists('agp_id_action', $data) ? $data['agp_id_action'] : null;
            $agpChassis = key_exists('agp_chassis', $data) ? $data['agp_chassis'] : null;
            $agpCarte = key_exists('agp_carte', $data) ? $data['agp_carte'] : null;
            $agpPeriph = key_exists('agp_periph', $data) ? $data['agp_periph'] : null;
            $agpLien = key_exists('agp_lien', $data) ? $data['agp_lien'] : null;

            $rsc = $this->astroRepository->getRessource($agpIdRsc);
            $idRscDslam = $rsc['ID_RESSOURCE_DSLAM'];
            $comm = new AgpCC($this->app, array(
                'Id_astro' => $agpIdAstro,
                'Id_rsc' => $idRscDslam,
                'Id_action' => $agpIdAction,
                'Chassis' => $agpChassis,
                'Cartes' => $agpCarte,
                'Periphs' => $agpPeriph,
                'Liens' => $agpLien,
                'EDSPilote' => $api ? $data['pilot_group'] : $astroSession['pilotgroup'],
                'intervenant' => key_exists('intervenant', $data) ? $data['intervenant'] : ''

                        // 'Alarme'=>$_SESSION['astro'.$data['agp_id_astro']]['ressource'] )
                    ), $idJeuParam);
                    $agpCCResult = $comm->getCommentaire();
                    // Ne remplacer le commentaire que si $idRscDslam est non vide
                    if ($idRscDslam !== null && $idRscDslam !== '') {
                        $commentaire = $agpCCResult;
                    }


        }
        $variables = OceaneTools::getContents($commentaire, '###', '###');
        if ($api) {
            $this->ticketId = $ticketId;
            $this->typeRessource = key_exists('type_ressource', $data) ? $data['type_ressource'] : '';
            $data['id3'] = key_exists('id3', $oceaneData) ? $oceaneData['id3'] : '';
            $commentaire = $this->replaceTagsChaineEnchainement($commentaire, $variables, $data['type_ressource'], $data);
        } else {
            $commentaire = $this->app->get('Variable')->replaceTagsChaine($commentaire, $variables, $astroSession['type'], $ticketId);
        }

        if ($data['agp_ecran'] == 0) {

            $commentaire = preg_replace('/###[\s\S]+?###/ ', '', $commentaire);
        }

        $agpCommentaire['COMMENTAIRE'] = $commentaire;

        if (!$idUrgenceOceane) {
            $idUrgenceOceane = $idUrgence;
        }

        return array(
            'agp_entite_activee' => $agpEntiteActivee,
            'agp_mode_activation' => $agpModeActivation,
            'agp_activation' => $agpActivation,
            'agp_eds' => $agpEds,
            'agp_suivre_hno' => $agpSuivreHno,
            'agp_transferer' => $agpTransferer,
            'agp_urgence' => $agpUrgence,
            'agp_action_eds' => $agpActionEds,
            'agp_dt_retab' => ($agpDtretab != '') ? $oceaneAssistant->changeUTCToDate($agpDtretab) : $agpDtretab,
            'agp_dt_retab_requested' => $oceaneData['orreq_date'],
            'agp_dt_en_cours' => $agpDtEnCours,
            'agp_dt_en_cours_oceane' => ($agpDtEnCoursOceane != '') ? $oceaneAssistant->changeUTCToDate($agpDtEnCoursOceane) : $agpDtEnCoursOceane,
            'agp_commentaire' => $agpCommentaire,
            'id_urgence' => ($isValeurNiveauUrgenceHeriteeOceane == 1) ? $idUrgenceOceane : $idUrgence,
            'id_action_en_cours' => $idActionEnCoursEds
        );
    }

    public function checkActionInput($input, $hasChassis)
    {
        $carteArray = array("dslam", "master", "deport");

        if (in_array($input, $carteArray) || (($input == 'alarme') && ($hasChassis == 'false'))) {
            return 517;
        } else {
            return 518;
        }
    }

    public function getCartesLignes($chassis, $dslamArray)
    {
        $cartes = array();

        foreach ($dslamArray['racks'] as $k => $v) {
            if ($dslamArray['racks'][$k]['rackName'] == $chassis) {
                foreach ($dslamArray['racks'][$k]['cards'] as $vv) {
                    $test = true;
                    // Carte dans la bonne catégorie ?
                    if (isset($vv['category']) && $vv['category'] != 'carte ligne') {
                        $test = false;
                    }

                    if ($test) {
                        $cartes[$vv['cardNumber']] = $vv['cardNumber'];
                    }
                }
            }
        }
        return $cartes;
    }

    /**
     * Affiche le formulaire de création d'un ticket TOC TRANS impacté
     * Récupère les données du ticket Océane et prépare le formulaire de création
     *  d'un ticket impacté de type TRANS avec les assemblées de niveau 1 selon le type de ressource.
     *
     * @param $ticketId
     * @return array|false
     */
    public function displayCreationTocTrans($ticketId)
    {
        // Récupération des données de session et ASTRO
        $astroSession = $this->app->get('Session')->get('astroOft' . $ticketId);
        $sessionId = $this->app->get('Session')->getUtilisateurId();
        $astroId = $astroSession['astroid'];
        // Chargement des données Océane du ticket

        $this->getOceane->getOceaneData($ticketId, $this->loginId);
        $oceaneAssistant = new OceaneAssistant($this->app);
        $data = array();
        $data['libel_type'] = $this->astroRepository->getLibelleTypeRess($astroSession['type']);

        $assembleeNiveauUn = '';

        $msgTocCrea = $oceaneAssistant->ol_tooltip("Le ticket sera crée sur l'assemblée sélectionnée", 150);

        $startDate = rtrim($this->getOceane->getDetectionDate(), 'Z');

        $this->airele = $this->app->get('Airele');
        if (!is_null($this->getOceane)) {
            // Récupération des données du ticket Océane (impacts, priorité, dates)
            $data['impact_technique'] = $this->astroLienRepository->getImpactTechniqueById($this->getOceane->getCategory());
            $data['impact_client'] = $this->astroLienRepository->getImpactClientLibById($this->getOceane->getCriticity());
            $data['priority'] = $this->astroLienRepository->getPrioriteLibById($this->getOceane->getPriority());
            $data['start_date'] = $oceaneAssistant->changeUTCToDate($startDate);
            $data['type'] = $astroSession['type'];
            $data['ticket_id'] = $ticketId;
            $data['type_ticket'] = $this->getOceane->getTicketType();
            $data['origin'] = $this->getOceane->getOrigin();
            $assemblee = $this->app->get('AnalyseImpact')->getNomAssemblee($astroSession['type'], $ticketId);
            // Récupération des assemblées niveau 1 selon le type de ressource

            if ($data['type'] == 'TRCCABLE' || $data['type'] == 'TRONCABLE' || $data['type'] == 'CABLE') {
                $assembleeNiveauUn = $this->airele->getDataTronconNiveauUn($astroSession ['id3']);
                usort($assembleeNiveauUn, function ($a, $b) {
                    return (int)$a['fibre'] > (int)$b['fibre'];
                });
            }
            if ($data['type'] == 'SDH' || $data['type'] == 'SLN' || $data['type'] == 'PDH' || $data['type'] == 'ETH' || $data['type'] == 'OCH' || $data['type'] == 'WDM_SID') {
                $assembleeNiveauUn = $this->airele->getDataAssembleeNiveauUn($assemblee, $sessionId, $ticketId);
            }
            if ($data['type'] == 'MIE') {
                $nomEqpt1 = $this->getOceane->getTicketParamsAttribute('Parameter', 'NOMEQPT1');
                $assembleeNiveauUn = $this->airele->getDataAssembleeNiveauUn($nomEqpt1, $sessionId, $ticketId);
            }
            // Création du formulaire avec les données récupérées

            $creaTicketTransForm = new CreaTicketTransForm(null, array(
                'app' => $this->app,
                'crea_ticket_select' => $assembleeNiveauUn,
                'data' => $data,
                'impact_technique' => $this->getOceane->getCategory(),
                'type' => $astroSession['type']
            ));
            // Calcul de la date d'action en cours (max entre DRI et DRC)

            $driDt = $this->getOceane->getTargetRestorationDate();
            $drcDt = $this->getOceane->getPlannedRestorationDate();
            $dtActionEnCoursEds = (strtotime($driDt) > strtotime($drcDt)) ? $driDt : $drcDt;

        } else {
            return false;
        }
        return array(
            'data' => $data,
            'form' => $creaTicketTransForm,
            'ticket_id' => $ticketId,
            'astro_id' => $astroId,
            'dt_action_en_cours_eds' => $dtActionEnCoursEds,
            'msg_toc' => $msgTocCrea
        );
    }

    public function displayCreationTocAdsl($ticketId)
    {
        $astroSession = $this->app->get('Session')->get('astroOft' . $ticketId);
        $astroId = $astroSession['astroid'];

        $creaTicketAdslForm = new CreaTicketAdslForm(null, array(
            'app' => $this->app,
            'ticket_id' => $ticketId
        ));

        return array(
            'form_crea_toc_adsl' => $creaTicketAdslForm,
            'ticket_id' => $ticketId,
            'astro_id' => $astroId,
        );
    }

    public function creerTicketRessourceAdsl($ticketId, $choixCreation, $choixValeur)
    {
        $this->loginId = $this->app->get('Session')->getUtilisateurLogin();
        $this->getapeService = $this->app->get('Gatape');
        $this->globalApiService = $this->app->get('GlobalApiUrlService');
        $oceaneApiData = $this->globalApiService->getUrlApi('API_OCEANE');
        $token = $this->getapeService->getToken($oceaneApiData, 'inside');

        $headerConfig = array(
            "X-Client-User-Id: $this->loginId",
            "X-HTTP-Method-Override: PATCH"
        );

        if ($choixCreation == "DSLAM") {
            $champComp3 = "dslam";
        } elseif ($choixCreation == "Chassis") {
            $champComp3 = "dslamSubRack";
        } elseif ($choixCreation == "Carte") {
            $champComp3 = "dslamSlot";
        }
        $choixValeur = explode(")", explode("(", "$choixValeur")[1])[0];
        $champComp4 = "XX /$choixValeur";
        $dslam = explode("-", $choixValeur)[0];
        $dataCreation = [
            "ticketType" => [
                "id" => "64"
            ],
            "priority" => [
                "id" => "4"
            ],
            "origin" => [
                "id" => "2"
            ],
            "criticity" => [
                "id" => "11"
            ],
            "relatedResource" => [
                "resourceSpecification" => [
                    "id" => "DSLAM"
                ],
                "resourceSpecCharacteristic" => [
                    [
                        "index" => "1",
                        "value" => "$dslam"
                    ]
                ]
            ],
            "troubleTicketCharacteristic" => [
                [
                    "value" => "$champComp3",
                    "index" => "3"
                ],
                [
                    "value" => $champComp4,
                    "index" => "4"
                ],
                [
                    "value" => "Ticket ressource crée depuis le ticket produit $ticketId",
                    "index" => "6"
                ]
            ]
        ];

        $oceaneApi = new ApiOceane($token, $headerConfig);
        $astroId = $this->app->get('AstroRepository')->getAstroIdByTicket($ticketId);

        $this->app->get('TraceRepository')->setTrace($astroId, "CREATION TOC RESSOURCE ENVOI", $dataCreation, $this->app->get('Session')->getUtilisateurId(), $ticketId);
        $retourCreation = json_decode($oceaneApi->creerTicketRessource($oceaneApiData['url'], $dataCreation), true);
        $this->app->get('TraceRepository')->setTrace($astroId, "CREATION TOC RESSOURCE REPONSE", $retourCreation, $this->app->get('Session')->getUtilisateurId(), $ticketId);

        if (is_array($retourCreation) && key_exists('id', $retourCreation)) {
            $paramUrlOceane = array(
                'RUNURLGENOK' => '1',
                'APPLI' => 'HBM',
                'SERV' => 'VISU',
                'TIC' => ''
            );
            $this->linkCommonService = new LinkService($this->app);
            $this->instance = $this->app->config['ENV'];
            $oceaneUrl = $this->linkCommonService->getGlobalLink('OCEANE', $this->instance, $paramUrlOceane);


            $messageFileName = DATA_DIR . '/' . $this->messageFile;
            $message = new Message($this->app, $astroId, $messageFileName);
            $message->setMessageComplexe("CREA_TOC_RESSOURCE", array('###NUM_TOC###' => $retourCreation['id']));

            return array(
                'toc_created' => $retourCreation['id'],
                'oceane_url' => $oceaneUrl,
                'etat' => 'ok',
                'erreur' => '',
            );
        } else {
            return array(
                'toc_created' => '',
                'etat' => 'ko',
                'erreur' => $retourCreation['description'],
            );
        }
    }

    public function displayEcranChx($idTicketAstro, $idAction, $idRsc, $ticketId, $equipmentName, $isReset)
    {
        // Récupération des données en base pour la requête (ressource Dslam)
        $dslamData = $this->edrRepository->getBlobDslam($idRsc);
        $result = json_decode(utf8_encode($dslamData['BLOBDATA']), true)[0];
        $chx = $this->agpRepository->getActionChoixGenerique($idAction);
        $chassis = $this->agpRepository->getDataAlarme($idTicketAstro)['CHASSIS'];

        $agpChoix = $this->interventionHelper->getAgpChoix($chassis, $chx, $result);

        $demandeInterventionSecondForm = new DemandeInterventionSecondForm(null, array(
            'app' => $this->app,
            'agp_id_astro' => $idTicketAstro,
            'agp_id_rsc' => $idRsc,
            'agp_id_action' => $idAction,
            'ticketid' => $ticketId,
            'equipement_name' => $equipmentName,
            'is_reset' => $isReset
        ));

        return array(
            'form' => $demandeInterventionSecondForm,
            'agp_choix' => $agpChoix,
            'ticket_id' => $ticketId,
            'agp_id_astro' => $idTicketAstro,
            'agp_title' => 'ASTRO - Agir Piloter n°' . $ticketId,
            'equipement_name' => $equipmentName,
            'is_reset' => $isReset
        );
    }

    /**
     * replacer les Tags par les valeurs
     *
     * @param string $chaine
     * @param array $args
     * @return string
     */
    public function replaceTagsChaineEnchainement($chaine, $args, $type, $data = array())
    {
        $this->oceaneService = $this->app->get('OceaneService');
        $this->ticketId = $data['ticketid'] ?? '';
        $this->eds = $data['connected_group'] ?? '';
        $this->cuidUpdate = $this->eds ? $this->astroRepository->getCompteMachine($this->eds) : '';

        $astroId = $data['astroid'] ?? '';
        if ($astroId == '') {
            $astroId = $this->astroRepository->getAstroIdByTicket($this->ticketId);
        }
        $id3 = $data['id3'] ?? '';
        $this->typeRessource = $type;

        if (!$this->getOceane) {
            $this->getOceane = $this->app->get('OceaneGet');
        }
        if ($this->ticketId && $this->getOceane) {
            $this->getOceane->getOceaneData($this->ticketId, $this->loginId);
        }


        $donnesTempsReel = array();
        $libSite = "";
        foreach ($args as $arg) {
            if ($arg == 'Temperature' || $arg == 'Etat_batterie' || $arg == 'Tension_batterie' || $arg == 'Element_HS') {
                $this->sessId = (key_exists('api', $this->app->config) && $this->app->config['api']) ? $this->getUserId() : $this->app->get('Session')->getUtilisateurId();
                $traceData = array(
                    'astro_id' => $this->astroRepository->getAstroIdByTicket($this->ticketId),
                    'ticket_id' => $this->ticketId,
                    'session_id' => $this->sessId,
                );
                $libSite = $this->getOceane->getTicketParamsAttribute('Parameter', 'LIBSITE');
                if ($libSite != "") {
                    $donnesTempsReel = $this->app->get('Cia')->getDataSite($libSite, $traceData);
                }

            }

            switch ($arg) {
                case 'transitool_tronc_ext_1':
                case 'transitool_tronc_ext_2':
                case 'transitool_tronc_troncon':
                case 'transitool_tronc_cable':
                case 'transitool_tronc_longueur':
                case 'transitool_tronc_paire':

                    $replaceValue = $this->app->get('Transitool')->getValueTronconTransitool($arg, $id3, $this->typeRessource, $astroId);

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }
                    break;
                case 'CUID':
                    $replaceValue = $this->cuidUpdate;
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

                case 'PILOTE':
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
                    $replaceValue = rtrim($this->getOceane->getCreationDate(), 'Z');
                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }
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
                case 'FG_NOMNAEQP':
                case 'FG_E1NOMNAEQP':
                case 'FG_E2NOMNAEQP':
                    $fgParameterMapping = [
                        'FG_NOMNAEQP' => 'NOMNAEQP',
                        'FG_E1NOMNAEQP' => 'E1NOMNAEQP',
                        'FG_E2NOMNAEQP' => 'E2NOMNAEQP'
                    ];
                    $replaceValue = $this->getOceane->getTicketParamsAttribute('Parameter', $fgParameterMapping[$arg]);
                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }
                    break;
                case 'RD3+':
                    $replaceValue = $this->getOceane->getClosedTicketQuantity();

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }

                    break;

                case 'DESCRIPTION':
                    $description = $this->getOceane->getDescription();
                    $replaceValue = ($description != '') ? $description : null;

                    if (OceaneTools::isValidVariable($replaceValue)) {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }

                    break;
                case 'Intervenant_EVT':
                    $codeDetecteur = StringTools::convertEncoding($this->getOceane->getTicketCharacteristics(5), 'ISO-8859-15', 'UTF-8');
                    if (!is_null($codeDetecteur)) {
                        $replaceValue = ($codeDetecteur != "ORANGE") ? $codeDetecteur : "UI";
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
                    $replaceValue = $this->refSiteRepository->getRefsiteColumn($arrayRefSite[$arg], $this->ticketId);

                    if (OceaneTools::isValidVariable($replaceValue) && gettype($replaceValue) != 'boolean') {
                        $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                    }
                    break;
                case 'PRIMO_AIGUILLAGE_TRONCON':
                    if ($this->typeRessource == 'TRONCABLE') {
                        $this->variableService = $this->app->get('Variable');

                        $replaceValue = $this->variableService->replaceTagsChainePrimoAiguillageTroncon($this->ticketId);
                        $replaceValue = preg_replace('/\s+/', ' ', $replaceValue);

                        if (OceaneTools::isValidVariable($replaceValue)) {
                            $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                        }
                        break;
                    }
                default:
                    $this->globalApiRepository = $this->app->get('GlobalApiRepository');
                    if ($this->globalApiRepository->isVariableAdminExist($arg, $type)) {
                        $resourceSpecification = ($this->getOceane->getRessourceType() !== null)
                            ? $this->getOceane->getRessourceType()
                            : $this->getOceane->getProductType();
                        if ($resourceSpecification) {
                            $dataIdentifiantsAdmin = ['type' => $resourceSpecification, 'nom' => $arg];
                            $tabIdentifiants = $this->globalApiRepository->getIdentifiantsAdmin($dataIdentifiantsAdmin);
                            if (count($tabIdentifiants) > 0 && $this->ticketId !== null) {
                                $replaceValue = $this->app->get('Variable')->getVariableAdminValue($tabIdentifiants, $this->ticketId);
                                if (isset($replaceValue)) {
                                    $chaine = str_replace('###' . $arg . '###', $replaceValue, $chaine);
                                }
                            }
                        }

                    }
            }
        }

        return $chaine;
    }

    public function getUserId()
    {
        $cuidlower = $this->app->config['api_data']['cuid']; //ID HBM
        return $this->app->get('IhmUtilisateurRepository')->getByLogin($cuidlower)['ID_UTILISATEUR'];
    }

    public function aiguillageManuel($dataAiguillageManuel, $intervenantInfos, $allEcransValues = null)
    {
        $intervenantArray = [];
        $donnee = $dataAiguillageManuel['donnee'];
        $competence = $dataAiguillageManuel['competence'];
        $designation = $dataAiguillageManuel['designation'];
        $intervenant = $dataAiguillageManuel['intervenant'] != '' ? $dataAiguillageManuel['intervenant'] != 'undefined' ? $dataAiguillageManuel['intervenant'] : 'Aiguillage impossible' : 'Aiguillage impossible';
        $technoComp = $dataAiguillageManuel['techno_comp'];
        $ticketId = $dataAiguillageManuel['ticketId'];
        $type = key_exists('type', $dataAiguillageManuel) ? $dataAiguillageManuel['type'] : '';

        //3349
        if (empty($intervenantInfos) || ($intervenantInfos['TECHNO'] == null || $intervenantInfos['TECHNO'] == '') || (($intervenantInfos['TECHNO'] != null && $intervenantInfos['TECHNO'] != '') && $intervenantInfos['TECHNO'] == $technoComp)) {
            if ($intervenant != 'ORANGE') {
                $this->variableService = $this->app->get('Variable');

                switch ($competence) {
                    case 'aglo_site-point_ir':
                        $designation = $this->variableService->replaceCaractRefSite($designation);
                        $intervenantArray = $this->variableService->getRefSiteByData($donnee, 'APPELLATION_IR', $designation);
                        break;
                    case 'supervision':
                        $intervenantArray = $this->variableService->getRefSiteByData($donnee, 'orig_geo', $designation);
                        break;
                    case 'SGTQS':
                        $intervenantArray = $this->variableService->getRefSiteBySGTQS($designation, null);
                        break;
                    case 'TIPI':
                        $intervenantArray = $this->variableService->getRefSiteByData($donnee, 'TIPICODE', $designation);
                        break;
                    default:
                        break;
                }
                $this->refsiteRepository = $this->app->get('RefsitesRepository');
                if (is_array($intervenantArray) && key_exists('INTERVENANT', $intervenantArray)) {
                    $intervenant = $intervenantArray['INTERVENANT'];
                    $this->refsiteRepository->UpdateTicketAstroWithIdRefsite($ticketId, $intervenantArray['ID']);
                } else {
                    $this->refsiteRepository->UpdateTicketAstroWithIdRefsite($ticketId, null);
                }
            }
        } else {
            $this->getIntervenant($type, $ticketId, $dataAiguillageManuel['idJeuParam']);
        }

        if (is_array($intervenantInfos)) {
            $dataAiguillageManuel['agp_eds'] = key_exists('EDS', $intervenantInfos) ? $intervenantInfos['EDS'] : '';
            $dataAiguillageManuel['selected_eds'] = key_exists('EDS', $intervenantInfos) ? $intervenantInfos['EDS'] : '';
            $dataAiguillageManuel['agp_activation'] = 'EDS ' . $dataAiguillageManuel['agp_eds'];
            $dataAiguillageManuel['agp_entite_second'] = key_exists('LIBELLE_ENTITE', $intervenantInfos) ? $intervenantInfos['LIBELLE_ENTITE'] : '';
            $dataAiguillageManuel['variable_check'] = key_exists('VARIABLE_CHECK', $intervenantInfos) ? $intervenantInfos['VARIABLE_CHECK'] : '';
            $dataAiguillageManuel['techno'] = key_exists('TECHNO', $intervenantInfos) ? $intervenantInfos['TECHNO'] : '';
        }
        $astroData['type'] = $type;
        $dataAiguillageManuel['intervenant'] = $intervenant;
        $dataAiguillageManuel['commentaire'] = $this->aiguillageCommentaireAction($dataAiguillageManuel, $astroData);

        if (!is_null($allEcransValues) && is_array($allEcransValues)) {
            $dataAiguillageManuel['commentaire'] = $this->aiguillageCommentaireRemplaceBloc($dataAiguillageManuel, $allEcransValues);
        }

        return $dataAiguillageManuel;
    }

    private function getIntervenant($type, $ticketId, $idJeuParam, $nomExtrimite = '', $extrimite = '')
    {
        $this->demandeIntervention = $this->app->get('DemandeIntervention');
        return $this->demandeIntervention->getIntervenant($type, $ticketId, $idJeuParam, $nomExtrimite, $extrimite);
    }

    public function aiguillageCommentaireRemplaceBloc($data, $allEcranValuesArray)
    {
        $commentaire = $data['commentaire'];
        $blocs = OceaneTools::getContents($commentaire, '##bloc_', '##');
        foreach ($blocs as $blocName) {
            if ('Carte_EAN' == $blocName && key_exists('donnee_cartes', $allEcranValuesArray)) {
                $blocDonneeCarte = '<br />';
                foreach ($allEcranValuesArray['donnee_cartes'] as $dataCarte) {
                    $blocVariable = $this->agpGeneriqueRepository->getBlocVariable('Carte_EAN');
                    foreach ($dataCarte as $keyTag => $dataTag) {
                        $blocVariable = str_replace('###' . $keyTag . '###', $dataTag, $blocVariable);
                    }
                    $blocDonneeCarte .= str_replace("\n", '<br />', $blocVariable . '<br/>');
                }
                $commentaire = str_replace('##bloc_' . $blocName . '##', $blocDonneeCarte, $commentaire);
            }
        }
        foreach ($allEcranValuesArray as $keyVariable => $valueVariable) {
            if ($keyVariable != 'donnee_cartes' && $keyVariable != 'CODE_EAN' && $keyVariable != 'Nom_Carte' && $keyVariable != 'Type_Equipement') {
                $commentaire = str_replace('###' . $keyVariable . '###', $valueVariable, $commentaire);
            }
            if ($keyVariable == 'CODE_EAN') {
                $blocDonneeVariable = '';
                foreach ($allEcranValuesArray['donnee_cartes'] as $dataCarte) {
                    foreach ($dataCarte as $keyTag => $dataTag) {
                        if ($keyTag == 'CODE_EAN') {
                            $dataVariable = $dataTag;
                        }
                    }
                    $blocDonneeVariable .= str_replace("\n", '<br />', '<br />' . $dataVariable . '<br />');
                }
                $commentaire = str_replace("###$keyVariable###", $blocDonneeVariable, $commentaire);
            }
            if ($keyVariable == 'Type_Equipement') {
                $blocDonneeVariable = '';
                foreach ($allEcranValuesArray['donnee_cartes'] as $dataCarte) {
                    foreach ($dataCarte as $keyTag => $dataTag) {
                        if ($keyTag == 'TYPE_EQUIPEMENT') {
                            $dataVariable = $dataTag;
                        }
                    }
                    $blocDonneeVariable .= str_replace("\n", '<br />', '<br />' . $dataVariable . '<br />');
                }
                $commentaire = str_replace("###$keyVariable###", $blocDonneeVariable, $commentaire);
            }
            if ($keyVariable == 'Nom_Carte') {
                $blocDonneeVariable = '';
                foreach ($allEcranValuesArray['donnee_cartes'] as $dataCarte) {
                    foreach ($dataCarte as $keyTag => $dataTag) {
                        if ($keyTag == 'NOM_CARTE') {
                            $dataVariable = $dataTag;
                        }
                    }
                    $blocDonneeVariable .= str_replace("\n", '<br />', '<br />' . $dataVariable . '<br />');
                }
                $commentaire = str_replace("###$keyVariable###", $blocDonneeVariable, $commentaire);
            }

            foreach ($blocs as $blocName) {

                if ($keyVariable == 'donnee_cartes' && !empty($blocs) && $blocName == 'choix_de_carte_trans') {
                    // Remplacer bloc_choix_de_carte_trans par les donnes des cartes selection?es
                    $blocDonneeCarte = '';
                    foreach ($valueVariable as $dataCarte) {
                        $blocVariable = $this->agpGeneriqueRepository->getBlocVariable('choix_de_carte_trans');

                        foreach ($dataCarte as $keyTag => $dataTag) {
                            if ($keyTag == 'ean') {
                                if ($dataTag == 'True') {
                                    $blocVariable = str_replace('###crochet_ouvrant###', '[', $blocVariable);
                                    $blocVariable = str_replace('###crochet_fermant###', ']', $blocVariable);
                                } else {
                                    $blocVariable = str_replace('###crochet_ouvrant###', '', $blocVariable);
                                    $blocVariable = str_replace('###crochet_fermant###', '', $blocVariable);
                                }
                                $blocVariable = str_replace('###' . $keyTag . '###', $dataTag, $blocVariable);
                            } else {
                                $blocVariable = str_replace('###' . $keyTag . '###', $dataTag, $blocVariable);
                            }
                        }
                        $blocDonneeCarte .= str_replace("\n", '<br />', $blocVariable . '<br/>');
                    }
                    $commentaire = str_replace('##bloc_choix_de_carte_trans##', $blocDonneeCarte, $commentaire);
                } elseif ($keyVariable != 'donnee_cartes' && !empty($blocs) && ($blocName == 'defaut_constate_trans' || $blocName == 'action_a_realiser_trans' || $blocName == 'Types_Carte' || $blocName == 'Types' || $blocName == 'Carte_EAN' || $blocName == 'Complet')) {
                    // Remplacer bloc par les donnes des cartes selection?es
                    $blocDonneeCarte = '';

                    $blocVariable = $this->agpGeneriqueRepository->getBlocVariable($blocName);

                    $blocDonneeCarte .= str_replace("\n", '<br />', $blocVariable . '<br/>');

                    $commentaire = str_replace("##bloc_$blocName##", $blocDonneeCarte, $commentaire);
                    foreach ($allEcranValuesArray as $keyVariable2 => $valueVariable2) {
                        if ($keyVariable2 != 'donnee_cartes') {
                            $commentaire = str_replace("###$keyVariable2###", $valueVariable2, $commentaire);
                        }

                    }

                }
            }
        }
        return $commentaire;

    }

    public function aiguillageCommentaireAction($data, $astroData)
    {
        $isDslamTest = false;

        if ($astroData['type'] == 'DSLAM' || $astroData['type'] == 'DSLAMDERCO') {
            $isDslamTest = true;
        }
        if ($isDslamTest) {
            $data['idJeu'] = $data['idJeuParam'];

            $agpResult = $this->getCommentaireAgp2Generique($data);

            return $agpResult->getCommentaire();
        } else {
            $agpCommentaire = $this->agpGeneriqueRepository->getCommentaireByAction($data['idJeuParam'], $data['agp_id_action']);
            $data['id_valeur'] = $agpCommentaire['ID_COMMENTAIRE'];
            if (key_exists('intervenant', $data) && $data['intervenant'] != '') {
                $segComment = $this->app->get('AdminCommentaireRepository')->getCommentaireSecondaireByIntervenant($data);
                if (is_array($segComment) && isset($segComment['SECOND_COMMENT']) && trim($segComment['SECOND_COMMENT']) !== '') {
                    $agpCommentaire['COMMENTAIRE'] = $segComment['SECOND_COMMENT'];
                }
            }
            $variables = OceaneTools::getContents($agpCommentaire['COMMENTAIRE'], '###', '###');
            return $this->app->get('Variable')->replaceTagsChaine($agpCommentaire['COMMENTAIRE'], $variables, $astroData['type'], $data['ticketId']);
        }
    }

    public function getLogin()
    {
        $cuidlower = $this->app->config['api_data']['cuid']; //ID HBM
        return $this->app->get('IhmUtilisateurRepository')->getByLogin($cuidlower)['LOGIN'];
    }

}
