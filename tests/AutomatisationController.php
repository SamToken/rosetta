<?php

namespace App\Controller;

use App\Repository\AdeliaRepository;
use App\Repository\AstroRepository;
use App\Service\AbandonnerService;
use App\Service\AutomatisationService;
use App\Service\ConfirmerService;
use Hbm\Common\Controller\BaseController;
use Hbm\Common\Filter\StringTrimHbm;

class AutomatisationController extends BaseController
{
    /**
     * @var AstroRepository
     */
    protected $astroRepo;

    /**
     * @var AbandonnerService
     */
    protected $abandonner;

    /**
     * @var AdeliaRepository
     */
    protected $adeliaRepo;

    /**
     * @var AutomatisationService
     */
    protected $automatisation;

    /**
     * @var ConfirmerService
     */
    protected $confirmer;

    protected $loginId;

    protected $sessId;

    protected $demandeIntervention;

    public function init()
    {
        parent::init();
        // Repositories
        $this->astroRepo = $this->app->get('AstroRepository');
        $this->adeliaRepo = $this->app->get('AdeliaRepository');

        // Services
        $this->abandonner = $this->app->get('Abandonner');
        $this->automatisation = $this->app->get('Automatisation');

        // Variables
        $this->loginId = $this->app->get('Session')->getUtilisateurLogin();
        $this->sessId = $this->app->get('Session')->getUtilisateurId();

    }


    public function alarmeVentiloAction()
    {
        set_time_limit(0);
        $this->disableRendering();

        $return = array(
            'statut' => 'ko',
            'message' => array()
        );

        $ticketId = $this->getParam('ticket_id');
        $bandeauId = $this->getParam('bandeau_id');
        $ticketSession = $this->app->get('Session')->get('astroOft' . $ticketId);
        $astroId = (!is_null($ticketSession) && key_exists('astroid', $ticketSession)) ? $ticketSession['astroid'] : 0;
        $typeRessourceProduit = key_exists('type', $ticketSession) ? $ticketSession['type'] : '';
        $dataAdelia = $this->adeliaRepo->getDataBlob($astroId);

        if ($dataAdelia && intval($dataAdelia['TOTAL_CLIENTS']) === 0) {
            $idJeuParam = $this->astroRepo->getJeuParamByBandeauFonction($bandeauId, 'ABONDONNER');
            $data = array(
                'astroid' => $astroId,
                'ticketid' => $ticketId,
                'detail_cause_abandon' => 'sans action - pas de clients',
                'cause_abandon' => 'AUTRE'
            );
            $message = $this->abandonner->abandonnerProcess($data, $idJeuParam, $typeRessourceProduit, $this->sessId, $this->loginId);
            array_push($return['message'], $message);
        } else {
            $return = $this->automatisation->confirmerIncident($ticketId, $return);
            if (key_exists('statut', $return) && $return['statut'] == 'ok') {
                $return = $this->automatisation->demandeIntervention($ticketId, $return);
            }
        }

        return $this->sendEncodedToJson($return);
    }

    public function lancerAutomateAction()
    {
        set_time_limit(0);
        $this->disableRendering();
        $ticketId = $this->getParam('ticket_id');
        $codeDetecteur = $this->getParam('code_detecteur');
        $collecte = $this->getParam('collecte');
        $bandeauId = $this->getParam('bandeau_id');
        $automatisationInfos = $this->app->get('AutomatisationRepository')->getAutomatisationValues($codeDetecteur, $collecte);
        $return = array(
            'statut' => 'ko',
            'message' => array()
        );

        if ($automatisationInfos) {
            if(key_exists('ABANDON', $automatisationInfos) && $automatisationInfos['ABANDON'] == '0') {
                $return = $this->confirmerDemandeIntervention($ticketId, $automatisationInfos, $return);
            } else {
                $ticketSession = $this->app->get('Session')->get('astroOft' . $ticketId);
                $astroId = (!is_null($ticketSession) && key_exists('astroid', $ticketSession)) ? $ticketSession['astroid'] : 0;
                $typeRessourceProduit = key_exists('type', $ticketSession) ? $ticketSession['type'] : '';
                $dataAdelia = $this->adeliaRepo->getDataBlob($astroId);


                if ($dataAdelia && intval($dataAdelia['TOTAL_CLIENTS']) === 0) {
                    $idJeuParam = $this->astroRepo->getJeuParamByBandeauFonction($bandeauId, 'ABONDONNER');
                    $data = array(
                        'astroid' => $astroId,
                        'ticketid' => $ticketId,
                        'detail_cause_abandon' => $automatisationInfos['DETAIL_ABANDON_CAUSE'],
                        'cause_abandon' => $automatisationInfos['ABANDON_CAUSE']
                    );
                    $message = $this->abandonner->abandonnerProcess($data, $idJeuParam, $typeRessourceProduit, $this->sessId, $this->loginId);
                    array_push($return['message'], $message);
                } else {
                    $return = $this->confirmerDemandeIntervention($ticketId, $automatisationInfos, $return);
                }
            }
        } else {
            $return = array(
                'statut' => 'ko',
                'message' => array('Aucune données d\'automatisation')
            );
        }

        return $this->sendEncodedToJson($return);
    }

    private function confirmerDemandeIntervention($ticketId, $automatisationInfos, $return)
    {
        $ticketSession = $this->app->get('Session')->get('astroOft' . $ticketId);
        $astroId = (!is_null($ticketSession) && key_exists('astroid', $ticketSession)) ? $ticketSession['astroid'] : '';
        $connectedGroup = key_exists('connectedgroup', $ticketSession) ? $ticketSession['connectedgroup'] : '';
        $typeRessource = key_exists('type_ressource', $ticketSession) ? $ticketSession['type_ressource'] : '';
        $dslam = key_exists('id1', $ticketSession) ? $ticketSession['id1'] : '';
        $this->sessId = $this->app->get('Session')->getUtilisateurId();

        $automatisationInfos['type_ressource'] = $typeRessource;
        $automatisationInfos['ASTRO_ID'] = $astroId;
        $automatisationInfos['CONNECTED_GROUP'] = $connectedGroup;
        $automatisationInfos['DSLAM'] = $dslam;
        $automatisationInfos['SESSION_ID'] = $this->sessId;

        $this->confirmer = $this->app->get('Confirmer');
        $this->demandeIntervention = $this->app->get('DemandeIntervention');
        $return = $this->confirmer->confirmerIncidentAutomatisation($ticketId, $automatisationInfos, $return);
        if (key_exists('statut', $return) && $return['statut'] == 'ok') {
            $return = $this->demandeIntervention->demandeIntervention($ticketId, 'automatisation', array(), $automatisationInfos, $return,$this->loginId);
        }
        return $return;
    }

    public function getInputFilterRules()
    {
        return array(
            'ticket_id' => array(
                'required' => true,
                'filters' => array(
                    array(
                        'name' => 'StripTags'
                    ),
                    new StringTrimHbm()
                ),
                'validators' => array(
                    array('name' => 'Alnum'), // Uniquement des caractères alphabétiques
                ),
            ),
            'code_detecteur' => array(
                'required' => true,
                'filters' => array(
                    array(
                        'name' => 'StripTags'
                    ),
                    new StringTrimHbm()
                ),
                'validators' => array(
                    array('name' => 'Digits'), // Uniquement des chiffres
                ),
            ),
            'collecte' => array(
                'required' => true,
                'filters' => array(
                    array(
                        'name' => 'StripTags'
                    ),
                    new StringTrimHbm()
                ),
                'validators' => array(
                    array('name' => 'Alnum'), // Uniquement des caractères alphabétiques
                ),
            ),
            'bandeau_id' => array(
                'required' => true,
                'filters' => array(
                    array(
                        'name' => 'StripTags'
                    ),
                    new StringTrimHbm()
                ),
                'validators' => array(
                    array('name' => 'Digits'), // Uniquement des chiffres
                ),
            )
        );
    }
}