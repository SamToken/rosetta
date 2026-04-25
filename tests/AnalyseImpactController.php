<?php

namespace App\Controller;

use App\Repository\EdrRepository;
use App\Repository\ImpactRepository;
use App\Repository\AstroRepository;
use App\Tools\OceaneAssistant;
use Hbm\Common\Controller\BaseController;
use App\Tools\OceaneTools;
use App\Service\AireleService;
use App\Service\AnalyseImpactService;
use Hbm\Common\Service\LinkService;
use Hbm\Globalapi\Service\Rest\Oceane;
use Hbm\Globalapi\Factory\ScanLiveFactory;
use Hbm\Common\Tools\StringTools;
use App\Form\ChoixListeTronconForm;


class AnalyseImpactController extends BaseController
{
    /**
     * @var EdrRepository
     */
    protected $edrRepository;
    /**
     * @var ImpactRepository
     */
    protected $analyseImpactRepo;
    /**
     * @var AstroRepository
     */
    protected $astroRepo;

    /**
     *
     * @var AireleService
     */
    protected $airelle;
    /**
     *
     * @var AnalyseImpactService
     */
    protected $analyseService;
    /**
     *
     * @var GlobalApiService
     */
    protected $globalApiService;
    /**
     *
     * @var LinkService
     */
    protected $linkService;

    protected $loginId;
    protected $instance;

    public function init()
    {
        parent::init();
        $this->airelle = $this->app->get('Airele');
        $this->analyseService = $this->app->get('AnalyseImpact');
        $this->analyseImpactRepo = $this->app->get('ImpactRepository');
        $this->astroRepo = $this->app->get('AstroRepository');
        $this->globalApiService = $this->app->get('GlobalApiUrlService');
        $this->loginId = $this->app->get('Session')->getUtilisateurLogin();
        $this->edrRepository = $this->app->get('EdrRepository');
        $this->view = $this->app->get('View');
        $this->traceRepository = $this->app->get('TraceRepository');
        $this->instance = $this->app->config['ENV'];
        $this->linkService = new LinkService($this->app);
    }

    /**
     * Met à jour la session cable_infos_ avec les clés assemblee et equipement
     */
    private function updateCableInfosSession($ticketId, $assemblee, $equipement) {
        $sessionKey = 'cable_infos_' . $ticketId;
        $cableInfos = $this->app->get('Session')->get($sessionKey);
        if (!is_array($cableInfos)) {
            $cableInfos = [];
        }
        if ($assemblee !== null && $assemblee !== '') {
            $cableInfos['assemblee'] = $assemblee;
        }
        if ($equipement !== null && $equipement !== '') {
            $cableInfos['equipement'] = $equipement;
        }
        $this->app->get('Session')->set($sessionKey, $cableInfos);
    }

    public function detailTransAction()
    {
        $this->setRenderLayout(false);

        $astroId = $this->request->getFromQuery('astroId', '');
        $ticketId = $this->request->getFromQuery('ticketId', '');
        $ticketOceaneArray = $this->app->get('Session')->get('cable_infos_' . $ticketId);


        $isAssemblee = false;
        $isEquipement = false;

        $ticketSession = $this->app->get('Session')->get('astroOft' . $ticketId);

        if ($ticketSession['type'] == "CABLE" || $ticketSession['type'] == "TRCCABLE" || $ticketSession['type'] == 'TRONCABLE') {
            $isAssemblee = false;
        } elseif ($ticketSession['type'] == "MIE") {
            $isEquipement = true;
        } else {
            $isAssemblee = true;
        }

        if (is_null($ticketOceaneArray)) {
            $tronconId = '';
            $cableId = '';
            $equipement = '';
        } else {
            $tronconId = (key_exists('troncon_id', $ticketOceaneArray)) ? $ticketOceaneArray['troncon_id'] : null;
            $cableId = (key_exists('cable_id', $ticketOceaneArray)) ? $ticketOceaneArray['cable_id'] : null;
            $equipement = (key_exists('equipement', $ticketOceaneArray)) ? $ticketOceaneArray['equipement'] : null;
        }

        // Alimentation de assemblee depuis le service (source de vérité)
        $assemblee = $this->analyseService->getNomAssemblee($ticketSession['type'], $ticketId);

        // Mise à jour de la session avec assemblee et equipement
        if ($isAssemblee) {
            $this->updateCableInfosSession($ticketId, $assemblee, null);
        } elseif ($isEquipement) {
            $this->updateCableInfosSession($ticketId, null, $equipement);
        }

        return array(
            'astro_id' => $astroId,
            'troncon_id' => $tronconId,
            'cable_id' => $cableId,
            'is_assemblee' => $isAssemblee,
            'assemblee' => $assemblee,
            'is_equipement' => $isEquipement,
            'equipement' => $equipement
        );
    }

    public function lancerTestOrchestraAction()
    {
        $this->disableRendering();
        $produit = $this->request->getFromPost('produit', '');
        $cache = $this->request->getFromPost('cache', '');
        $sessIs = $this->app->get('Session')->getUtilisateurId();
        $ticketId = $this->request->getFromPost('ticket_id', '');
        $astroId = $this->astroRepo->getAstroIdByTicket($ticketId);

        $traceInfo = [
            'astroId' => $astroId,
            'ticketId' => $ticketId,
            'sessIs' => $sessIs
        ];
        $cacheBool = ($cache == '1');
        $cacheOrchestra = intval($this->app->get('AssistantRepository')->getParamsMobile('CACHE_ORCHESTRA'));
        $dataTestOrchestra = $this->app->get('Orchestra')->testProduit($produit, $traceInfo, $this->loginId, $cacheBool, $cacheOrchestra);
        $retour = $this->view->impactHelper()->getRowTestOrchestra($dataTestOrchestra);
        return $this->sendEncodedToJson($retour, true, 'ISO-8859-15');
    }
    public function lancerTestEtxAction()
    {
        $this->disableRendering();
        $produit = $this->request->getFromPost('produit', '');
        $cache = $this->request->getFromPost('cache', '');
        $sessIs = $this->app->get('Session')->getUtilisateurId();
        $ticketId = $this->request->getFromPost('ticket_id', '');
        $astroId = $this->astroRepo->getAstroIdByTicket($ticketId);

        $traceInfo = [
            'astroId' => $astroId,
            'ticketId' => $ticketId,
            'sessIs' => $sessIs
        ];
        $cacheBool = ($cache == '1');
        $cacheOrchestra = intval($this->app->get('AssistantRepository')->getParamsMobile('CACHE_ORCHESTRA'));
        $dataTestOrchestra = $this->app->get('Orchestra')->testProduitEtx($produit, $traceInfo, $this->loginId, $cacheBool, $cacheOrchestra);
        $retour = $this->view->impactHelper()->getRowTestEtx($dataTestOrchestra);
        return $this->sendEncodedToJson($retour, true, 'ISO-8859-15');
    }

    public function lancerTestOrchestraTronconAction()
    {
        $this->disableRendering();
        $troncon = $this->request->getFromPost('troncon', '');
        $cache = $this->request->getFromPost('cache', 1);
        $sessIs = $this->app->get('Session')->getUtilisateurId();
        $ticketId = $this->request->getFromPost('ticket_id', '');
        $astroId = $this->astroRepo->getAstroIdByTicket($ticketId);

        $traceInfo = [
            'astroId' => $astroId,
            'ticketId' => $ticketId,
            'sessIs' => $sessIs
        ];
        $dataTestOrchestra = $this->app->get('Orchestra')->testTroncon($troncon, $traceInfo, $this->loginId, intval($cache));
        $retour = $this->view->impactHelper()->getRowTestOrchestraTroncon($dataTestOrchestra);

        $this->send($retour);
    }

    public function getDataTronconNewAction()
    {
        $this->disableRendering();
        $data = $this->request->getFromPost();
        $dslamList = array();

        $tronconId = $this->request->getFromPost('tronconId', '');

        if ($tronconId !== '') {
            $dataTroncon = $this->airelle->setDataTronconNew($tronconId, $data);

            if ($dataTroncon != "") {
                foreach ($dataTroncon->rows as $cle => $val) {
                    $lien = $dataTroncon->rows[$cle]['cell'][2];
                    if (substr($val['cell'][1], 0, 2) == "DS") {
                        array_push($dslamList, $val['cell'][1]);
                    }
                    $produit = $dataTroncon->rows[$cle]['cell'][1];
                    $dataTroncon->rows[$cle]['cell'][2] = "";
                    $dataTroncon->rows[$cle]['cell'][3] = "";
                    $dataTroncon->rows[$cle]['cell'][4] = $this->view->impactHelper()->getWaitCheckService($produit);
                    $dataTroncon->rows[$cle]['cell'][5] = $this->view->impactHelper()->getWaitTestOrchestra($produit, true).' '.$this->view->impactHelper()->getWaitTestEtx($produit, true);

                    // Ajouter le bouton SERIA Routing si un lien (assemblée) existe
                    $seriaButton = '';
                    if (!empty($lien)) {
                        $seriaBaseUrl = $this->linkService->getGlobalLink('SERIA', $this->instance);
                        $seriaUrl = $seriaBaseUrl . urlencode($lien).'&nameType=shortName';
                        $seriaButton = '<a href="' . $seriaUrl . '" target="_blank" rel="noopener noreferrer" title="SERIA Routing" class="btn_seria_routing"><i class="fa fa-code-fork" style="margin-right: 5px;"></i></a>';
                    }

                    $dataTroncon->rows[$cle]['cell'][6] = $seriaButton . $lien;
                }
                $pingBige = $this->pingScanLive($dslamList);
                foreach ($pingBige as $v) {
                    foreach ($dataTroncon->rows as $cle => $val) {
                        if (trim($val['cell'][1]) == $v['EQUIPEMENT']) {
                            $result = [];
                            switch ($v['PING']) {
                                case 'true':
                                    $etat = 'oui';
                                    break;
                                case 'false':
                                    $etat = 'non';
                                    break;
                                case 'not found':
                                    $etat = 'notfound';
                                    break;
                                default:
                                    $etat = '';
                                    break;
                            }
                            $result['ping_dslam'][$etat] = array('equipement'=> $v['EQUIPEMENT'],'ping_dt_requete'=> $v['PING_DT_REQUETE'] );
                            $dataTroncon->rows[$cle]['cell'][3] = $this->view->impactHelper()->getRowPingTronconOne($result['ping_dslam'], $v['EQUIPEMENT']);
                            $dataTroncon->rows[$cle]['cell'][2] = $v['BIGE'];
                            $dataTroncon->rows[$cle]['cell'][7] = $v['PING_DT_REQUETE'];
                            break;
                        }
                    }
                }
            }
            return $this->sendEncodedToJson($dataTroncon);
        }
        return $this->sendEncodedToJson(array());
    }


    //here detail niv 1 occupation
    public function getDataAssembleeAction()
    {
        $this->disableRendering();
        $data = $this->request->getFromPost();
        $astroId = $this->request->getFromPost('id_astro', $this->request->getFromPost('astroId', ''));
        $ticketId = $this->astroRepo->getTicketByAstroId($astroId);
        $dataSession = $this->app->get('Session')->get('cable_infos_'. $ticketId);
        $dslamList = array();
        if (is_array($dataSession) && !empty($dataSession) && key_exists('assemblee', $dataSession)) {
            $dataAssemblee = $this->airelle->setDataAssemblee($dataSession['assemblee'], $data);
            if ($dataAssemblee != "") {
                foreach ($dataAssemblee->rows as $cle => $val) {
                    $topology = $dataAssemblee->rows[$cle]['cell'][3];
                    if (substr($val['cell'][2], 0, 2) == "DS" && !in_array($val['cell'][2], $dslamList)) {
                        array_push($dslamList, $val['cell'][2]);
                    }
                    $dataAssemblee->rows[$cle]['cell'][3] = "";
                    $dataAssemblee->rows[$cle]['cell'][4] = "";
                    $dataAssemblee->rows[$cle]['cell'][5] = $this->view->impactHelper()->getWaitCheckService($val['cell'][2]);
                    $dataAssemblee->rows[$cle]['cell'][6] = $this->view->impactHelper()->getWaitTestOrchestra($val['cell'][2], true).' '.$this->view->impactHelper()->getWaitTestEtx($val['cell'][2], true);

                    // Ajouter le bouton SERIA Routing si une topologie (assemblée) existe
                    $seriaButton = '';
                    if (!empty($topology)) {
                        $seriaBaseUrl = $this->linkService->getGlobalLink('SERIA', $this->instance);
                        $seriaUrl = $seriaBaseUrl . urlencode($topology) .'&nameType=shortName';
                        $seriaButton = '<a href="' . $seriaUrl . '" target="_blank" rel="noopener noreferrer" title="SERIA Routing" class="btn_seria_routing"><i class="fa fa-code-fork" style="margin-right: 5px;"></i></a>';
                    }

                    $dataAssemblee->rows[$cle]['cell'][7] = $seriaButton . $topology;
                    $dataAssemblee->rows[$cle]['cell'][8] = "";
                }
                $pingBige = $this->pingScanLive($dslamList);
                foreach ($pingBige as $v) {
                    foreach ($dataAssemblee->rows as $cle => $val) {
                        if (trim($val['cell'][2]) == $v['EQUIPEMENT']) {
                            $dataAssemblee->rows[$cle]['cell'][3] = $v['PING'];
                            $dataAssemblee->rows[$cle]['cell'][4] = $v['BIGE'];
                            $dataAssemblee->rows[$cle]['cell'][8] = $v['PING_DT_REQUETE'];
                        }
                    }
                }
            }
            return $this->sendEncodedToJson($dataAssemblee);
        } elseif (is_array($dataSession) && !empty($dataSession) && key_exists('equipement', $dataSession)) {
            $dataEquipement = $this->airelle->setDataAssemblee($dataSession['equipement'], $data);
            if ($dataEquipement != "") {
                foreach ($dataEquipement->rows as $cle => $val) {
                    $lien = $dataEquipement->rows[$cle]['cell'][1];
                    // Ajouter le bouton SERIA Routing si un lien (assemblée) existe
                    $seriaButton = '';
                    if (!empty($lien)) {
                        $seriaBaseUrl = $this->linkService->getGlobalLink('SERIA', $this->instance);
                        $seriaUrl = $seriaBaseUrl . urlencode($lien).'&nameType=shortName';
                        $seriaButton = '<a href="' . $seriaUrl . '" target="_blank" rel="noopener noreferrer" title="SERIA Routing" class="btn_seria_routing"><i class="fa fa-code-fork" style="margin-right: 5px;"></i></a>';
                    }
                    $dataEquipement->rows[$cle]['cell'][1] = $seriaButton . $lien;
                    if (substr($val['cell'][2], 0, 2) == "DS") {
                        array_push($dslamList, $val['cell'][2]);
                    }
                    $dataEquipement->rows[$cle]['cell'][3] = "";
                    $dataEquipement->rows[$cle]['cell'][4] = "";
                    $dataEquipement->rows[$cle]['cell'][5] = $this->view->impactHelper()->getWaitCheckService($val['cell'][2]);
                    $dataEquipement->rows[$cle]['cell'][6] = $this->view->impactHelper()->getWaitTestOrchestra($val['cell'][2], true).' '.$this->view->impactHelper()->getWaitTestEtx($val['cell'][2], true);

                    $dataEquipement->rows[$cle]['cell'][7] = "";
                    $dataEquipement->rows[$cle]['cell'][8] = "";
                }
                $pingBige = $this->pingScanLive($dslamList);
                foreach ($pingBige as $v) {
                    foreach ($dataEquipement->rows as $cle => $val) {
                        if (trim($val['cell'][2]) == $v['EQUIPEMENT']) {
                            $dataEquipement->rows[$cle]['cell'][3] = $v['PING'];
                            $dataEquipement->rows[$cle]['cell'][4] = $v['BIGE'];
                            $dataEquipement->rows[$cle]['cell'][8] = $v['PING_DT_REQUETE'];
                        }
                    }
                }
            }
            return $this->sendEncodedToJson($dataEquipement);
        }
        return $this->sendEncodedToJson(array());
    }

    public function lancerCheckServiceAllAction()
    {
        $this->setRenderer('JsonRenderer');
        $ticketId = $this->request->getFromPost('ticket_id', '');
        $gridRows = $this->request->getFromPost('grid_rows', []);
        $dslams = $this->request->getFromPost('dslams', []);
        $isWdm = $this->request->getFromPost('is_wdm', []);

        if (empty($dslams)) {
            $id = $isWdm == '1' ? 2 : 1;
            $dslamList = [];
            foreach ($gridRows as $val) {
                if (substr($val['cell'][$id], 0, 2) == "DS") {
                    array_push($dslamList, $val['cell'][$id]);
                }
            }
        } else {
            $dslamList = $dslams;
        }

        $reponse = [];
        if (!empty($dslamList)) {
            $astroId = $this->astroRepo->getAstroIdByTicket($ticketId);
            $traceData = array(
                'astro_id' => $astroId,
                'sess_id' => $this->app->get('Session')->getUtilisateurId(),
                'ticket_id' => $ticketId
            );
            $result = $this->app->get('CheckService')->getCheckService($dslamList, $traceData);

            if (is_array($result) && key_exists('dslams', $result) && is_array($result['dslams'])) {
                $dateConsultation = is_array($result) && key_exists('time', $result) ? $result['time'] : '';
                $formattedDate = OceaneAssistant::changeFormat($dateConsultation, 'Y-m-d H:i:s');
                foreach ($result['dslams'] as $v) {
                    $reponse[$v['name']] = $this->view->impactHelper()->getRowCheckService($v, $formattedDate);
                }
            } elseif (is_array($result) && key_exists('state', $result) && $result['state'] == 'KO' && count($dslamList) == 1) {
                $currentDate = date('d/m/Y H:i', time());
                $result['name'] = $dslamList[0];
                $reponse[$dslamList[0]] = $this->view->impactHelper()->getRowCheckService($result, $currentDate);
            }
        }

        if (empty($reponse)) {
            foreach ($dslamList as $dslam) {
                $v['name'] = $dslam;
                $reponse[$dslam] = $this->view->impactHelper()->getRowCheckService($v, '');
            }
        }

        return $this->sendEncodedToJson($reponse);
    }

    public function afficherListeTronconAction()
    {
        $id3 = $this->request->getFromQuery('id3', '');
        $ticketid = $this->request->getFromQuery('ticketId', '');
        $cableId = trim($this->request->getFromQuery('cable', ''));

        $isTronconsExlusParCorrelation = false;
        $arrayTroconsPrefiltre = $this->analyseService->prefiltrageTroncons($ticketid);

        $choixListeTronconForm = new ChoixListeTronconForm(null, array(
            'trocons_prefiltre' => $arrayTroconsPrefiltre
        ));
        $premierFiltrage = $this->analyseImpactRepo->isFirstFilter($ticketid);
        if ($premierFiltrage !== '0' && is_array($arrayTroconsPrefiltre) && !empty($arrayTroconsPrefiltre)) {
            $isTronconsExlusParCorrelation = true;
        }
        $tronconsExlus = $this->analyseImpactRepo->getNbTronconsExclus($ticketid);
        if ($tronconsExlus == 0) {
            $tronconsTotal = $this->analyseImpactRepo->getNbTronconsExclus($ticketid, 1);
            if ($tronconsTotal == 0) {
                $tronconListeArr = $this->airelle->getFormattedDataCable($cableId);
                if (is_array($arrayTroconsPrefiltre) && !empty($arrayTroconsPrefiltre) && (count($tronconListeArr) > count($arrayTroconsPrefiltre))) {
                    $isTronconsExlusParCorrelation = true;
                    $tronconsExlus = count($tronconListeArr) - count($arrayTroconsPrefiltre);
                }
            }
        }

        return array(
            'id3' => $id3,
            'choix_liste_troncon_form' => $choixListeTronconForm,
            'id_ticket' => $ticketid,
            'isTroncon_exclus_par_correlation' => $isTronconsExlusParCorrelation,
            'ticketsExclus' => $tronconsExlus
        );
    }

    /**
     */
    public function listeTronconsAction()
    {
        $this->setRenderer('JsonRenderer');
        $data = $this->request->getFromPost();
        $cableId = trim($this->request->getFromPost('cable', ''));
        $ticketId = trim($this->request->getFromPost('ticket_id', ''));

        $tronconListeArr = $this->airelle->getFormattedDataCable($cableId);
        $this->analyseImpactRepo->deleteAllTronconCable($cableId);
        $this->analyseImpactRepo->addDataTronconCable($ticketId, $cableId, $tronconListeArr);

        $arrayTroconsPrefiltre = $this->analyseService->prefiltrageTroncons($ticketId);
        $premierFiltrage = $this->analyseImpactRepo->isFirstFilter($ticketId);
        if (!$premierFiltrage && $premierFiltrage !== '0' && is_array($arrayTroconsPrefiltre) && !empty($arrayTroconsPrefiltre)) {
            $troncons = array_map(function ($value) {
                return "'$value'";
            }, $arrayTroconsPrefiltre);
            $this->analyseImpactRepo->updateTronconsState($troncons, $ticketId, 'afficher_troncons_suspecte');
        }

        $dataExtract = $this->analyseImpactRepo->getListeTroncon($data, $cableId, $ticketId);
        if (is_object($dataExtract) && property_exists($dataExtract, 'rows') && count($dataExtract->rows) > 0) {
            // Array Final
            foreach ($dataExtract->rows as $key => $value) {
                $dataExtract->rows[$key]['cell']['ORCHESTRA'] = $this->view->impactHelper()->getWaitTestOrchestraTroncon($dataExtract->rows[$key]['cell']['TRONCON']);
                $dataExtract->rows[$key]['cell']['PINGDSLAM'] = $this->view->impactHelper()->getWaitPing($dataExtract->rows[$key]['cell']['TRONCON']);
                $dataExtract->rows[$key]['cell']['NBDSLAM'] = $this->view->impactHelper()->getWaitPingCell($dataExtract->rows[$key]['cell']['TRONCON'], 'nb_dslam');
                $dataExtract->rows[$key]['cell']['PRESENCEBIGE'] = $this->view->impactHelper()->getWaitPingCell($dataExtract->rows[$key]['cell']['TRONCON'], 'bige');
            }
        }

        return $this->sendEncodedToJson($dataExtract);
    }

    public function checkSameOccupAction()
    {
        //the function check the occup niv1 of the selected troncon and not the excluded ones
        $this->setRenderer('JsonRenderer');
        $ticketId = trim($this->request->getFromPost('ticket_id', ''));
        $cable = trim($this->request->getFromPost('cable', ''));

        $alert = 1;

        $selectedTroncons = $this->analyseImpactRepo->getListeTroncon([], $cable, $ticketId, false);

        if (is_array($selectedTroncons) && count($selectedTroncons) > 1) {
            $selectedTroncons = array_column($selectedTroncons, 'TRONCON');
            $columns = ['FIBRE', 'PRODUIT', 'LIEN'];
            $occupationRef = [];
            foreach ($selectedTroncons as $key => $v) {
                if ($key === 0) {
                    $occupationRef = $this->app->get('AstroBase')->filterArrayByKeys($this->airelle->getOccupationNiveauUnFromCache($v, $ticketId), $columns);
                } else {
                    $occupation = $this->app->get('AstroBase')->filterArrayByKeys($this->airelle->getOccupationNiveauUnFromCache($v, $ticketId), $columns);
                    $bool = (is_array($occupationRef) && is_array($occupation) && count($occupationRef) == count($occupation));

                    if (!$bool && ($occupationRef != $occupation)) {
                        $alert = 0;
                        break;
                    }
                }
            }
        } else {
            return [
                'same' => $alert
            ];
        }
        return [
            'same' => $alert
        ];
    }

    //here synthese

    /**
     */
    public function analyseImpactTransAction()
    {
        $this->setRenderLayout(false);
        $troncon = trim($this->request->getFromPost('troncon', ''));
        $ticketId = $this->request->getFromPost('ticket_id', '');
        $idUtilisateur = $this->app->get('Session')->getUtilisateurId();
        $seuils = array();
        $isAssemblee = false;
        $isEquipementTrans = false;
        $oceaneAssistant = new OceaneAssistant($this->app);
        $infoBulleDeclencheurIM = '';
        $decDone = false;

        $tools = new OceaneTools();

        $ticketSession = $this->app->get('Session')->get('astroOft' . $ticketId);
        $idBandeau = $this->astroRepo->getBandeauId($ticketSession['bandeau']);
        $assemblee = $this->analyseService->getNomAssemblee($ticketSession['type'], $ticketId);
        $retourCountByService = $this->airelle->getCountByService($ticketSession['type'], $ticketId, $idUtilisateur, $troncon, $assemblee);
        $countByService = key_exists('count_by_service', $retourCountByService) ? $retourCountByService['count_by_service'] : [];
        $isAssemblee = key_exists('is_assemblee', $retourCountByService) ? $retourCountByService['is_assemblee'] : false;
        $isEquipementTrans = key_exists('is_equipement_trans', $retourCountByService) ? $retourCountByService['is_equipement_trans'] : false;

        if ($isAssemblee) {
            $getSeuilId = $assemblee;
        } else {
            $getSeuilId = $troncon;
        }

        if (key_exists('trouble_detection_date', $ticketSession)) {
            $dateDebut = $ticketSession['trouble_detection_date'];
            $result = $this->analyseImpactRepo->getSeuils($ticketId, $idUtilisateur,
                $tools->changeUTCToDate('d-m-Y H:i', $dateDebut), $getSeuilId);
            $seuils['grave'] = (is_array($result) && key_exists('MIN_GRAVE', $result)) ? $result['MIN_GRAVE'] : '-';
            $seuils['majeur'] = (is_array($result) && key_exists('MIN_MAJEUR', $result)) ? $result['MIN_MAJEUR'] : '-';
            $today = new \DateTime();

            $seuilGraveDate = \DateTime::createFromFormat('d/m/Y H:i', $seuils['grave']);
            $seuilMajeurDate = \DateTime::createFromFormat('d/m/Y H:i', $seuils['majeur']);

            if ($seuilGraveDate && ($today > $seuilGraveDate)) {
                $seuils['grave_is_sup'] = true;
            } else {
                $seuils['grave_is_sup'] = false;
            }
            if ($seuilMajeurDate && ($today > $seuilMajeurDate)) {
                $seuils['majeur_is_sup'] = true;
            } else {
                $seuils['majeur_is_sup'] = false;
            }
        } else {
            $seuils['grave'] = '-';
            $seuils['majeur'] = '-';
            $seuils['grave_is_sup'] = false;
            $seuils['majeur_is_sup'] = false;
        }

        if (!$isAssemblee && !$isEquipementTrans) {
            $astroSession = $this->app->get('Session')->get('cable_infos_'. $ticketId);
            $astroSession['troncon_id'] = $troncon;
            $astroSession['cable_id'] = $countByService['cable_id'];
            $this->app->get('Session')->set('cable_infos_'. $ticketId, $astroSession);
            $this->astroRepo->setLastTroncon($ticketId, $troncon);
        } elseif ($isAssemblee) {
            $this->updateCableInfosSession($ticketId, $assemblee, null);
        } elseif ($isEquipementTrans) {
            $this->updateCableInfosSession($ticketId, null, $troncon);
        }

        $gtrMsgInfoBulle = $oceaneAssistant->ol_tooltip($this->analyseService->getGtrMsg($countByService['gtrs1'], $countByService['gtrs2']), 150);

        $impactCheck = $this->analyseService->getImpactClient($ticketId);

        $astroSession['impact_result'] = $countByService['result'];
        $astroSession['gtrs1'] = $countByService['gtrs1'];
        $astroSession['gtrs2'] = $countByService['gtrs2'];
        $this->app->get('Session')->set('prio_infos' . $ticketId, $astroSession);

        //
        $familles = $this->analyseImpactRepo->getDataFamilleService();
        $idCable = key_exists('cable_id', $countByService) ? $countByService['cable_id'] : 'inconnu';
        $idTroncon = $troncon;
        $params = array();

        $data = $this->airelle->getDataProduits($idTroncon, $idUtilisateur, $familles, array(
            'id_section' => $idTroncon,
            'id_cable' => $idCable
        ), $params);

        $nbFamilleTdmoip = $this->analyseService->calculeTotaleFamilleTdmoip($data);
        if($nbFamilleTdmoip != ''){
            $countByService['result']['TDMOIP'] = $nbFamilleTdmoip;
        }
        if($impactCheck){
            $returnPreconisationTrans = $this->app->get('Abandonner')->preconisationPrioriteTrans($ticketId, $idBandeau, $ticketSession['type_ressource']);
            $decDone = $returnPreconisationTrans['dec_done'];
            $infoBulleDeclencheurIM = $oceaneAssistant->ol_tooltip('Seuil IM dépassé', 150);

        }
        
        return array(
            'cable_id' => $isAssemblee || $isEquipementTrans ? '' : $countByService['cable_id'],
            'troncon_id' => $isAssemblee || $isEquipementTrans ? '' : $troncon,
            'impact_result' => $countByService['result'],
            'seuils' => $seuils,
            'is_assemblee' => $isAssemblee,
            'assemblee' => $isAssemblee ? $assemblee : '',
            'is_equipement' => $isEquipementTrans,
            'equipement' => $troncon,
            'impact_check' => $impactCheck,
            'gtrs1' => $countByService['gtrs1'],
            'gtrs2' => $countByService['gtrs2'],
            'gtr_infobulle' => $gtrMsgInfoBulle,
            'type' => $ticketSession['type'],
            'dec_done' => $decDone,
            'info_bulle_declencheur_im' => $infoBulleDeclencheurIM

        );
    }

    public function updateListeTronconsAction()
    {
        $this->disableRendering();
        $troncons = $this->request->getFromPost('troncons', '');
        $ticketId = $this->request->getFromPost('ticket_id', '');
        $operation = $this->request->getFromPost('operation', '');
        $tronconsExlusParCorrelation = false;

        if ($operation == 'afficher_troncons_suspecte') {
            $arrayTroconsPrefiltre = $this->analyseService->prefiltrageTroncons($ticketId);
            $troncons = array_map(function ($value) {
                return "'$value'";
            }, $arrayTroconsPrefiltre);
            $tronconsExlusParCorrelation = true;
            $this->analyseImpactRepo->updateStateFirstFilterTroncon($ticketId, 1);

        } else {
            $this->analyseImpactRepo->updateStateFirstFilterTroncon($ticketId, 0);

        }

        $this->analyseImpactRepo->updateTronconsState($troncons, $ticketId, $operation);
        $nb_tronconsExclus = $this->analyseImpactRepo->getNbTronconsExclus($ticketId);

        return $this->sendEncodedToJson(array(
            'nb_tronconsExclus' => $nb_tronconsExclus,
            'troncons_exlus_par_correlation' => $tronconsExlusParCorrelation
        ));
    }

    public function analysePlusGrosImpactTransAction()
    {
        $this->disableRendering();
        set_time_limit(0);
        $tools = new OceaneTools();

        $troncons = $this->request->getFromPost('troncons', array());
        $ticketId = $this->request->getFromPost('ticket_id', '');
        $idUtilisateur = $this->app->get('Session')->getUtilisateurId();
        $ticketSession = $this->app->get('Session')->get('astroOft' . $ticketId);
        $dateDebut = !is_null($ticketSession['trouble_detection_date']) ? $tools->changeUTCToDate('d-m-Y H:i', $ticketSession['trouble_detection_date']) : '';

        $res = $this->airelle->getPlusGrosImpact($troncons, $ticketId, $idUtilisateur, $dateDebut);

        return $this->sendEncodedToJson(array(
            'troncon_id' => $res['troncon']
        ));
    }

    public function produitsAction()
    {
        $this->setRenderLayout(false);

        $refresh = $this->request->getFromPost('refresh', 0);

        if ($refresh == '1') {
            $idUtilisateur = $this->app->get('Session')->getUtilisateurId();
            $idTroncon = $this->request->getFromPost('id_troncon', '');

            $data = array(
                'identifiant' => $idTroncon,
                'id_createur' => $idUtilisateur,
                'id_tableau' => 'BilanImpactGTRservice'
            );

            $this->analyseImpactRepo->purgetData($data);
        }
    }

    public function updateCommentaireAssembleAction()
    {
        $this->disableRendering();

        $textFinalAll = htmlspecialchars_decode($this->request->getFromPost('text_final_all', ''));
        $allCheck = $this->request->getFromPost('all', '');

        $textFinalArray[0] = $this->request->getFromPost('text_final_one', '');
        //variables below will be used after PO validation
        $textFinalArray[1] = $this->request->getFromPost('text_final_two', '');
        $textFinalArray[2] = $this->request->getFromPost('text_final_three', '');
        $textFinalArray[3] = $this->request->getFromPost('text_final_four', '');
        $textFinalArray[4] = $this->request->getFromPost('text_final_five', '');
        $textFinalArray[5] = $this->request->getFromPost('text_final_six', '');
        $textFinalArray[6] = $this->request->getFromPost('text_final_seven', '');
        $textFinalArray[7] = $this->request->getFromPost('text_final_eight', '');
        $textFinalArray[8] = $this->request->getFromPost('text_final_nine', '');
        $textFinalArray[9] = $this->request->getFromPost('text_final_ten', '');
        $textFinalArray[10] = $this->request->getFromPost('text_final_eleven', '');

        $ticketId = $this->request->getFromPost('ticket_id', '');

        $this->getapeService = $this->app->get('Gatape');
        $oceaneApiData = $this->globalApiService->getUrlApi('API_OCEANE');
        $token = $this->getapeService->getToken($oceaneApiData, 'inside');
        $headerConfig = array(
            "X-Client-User-Id: $this->loginId",
            "X-HTTP-Method-Override: PATCH",
        );
        $loginUser = $this->loginId;
        $oceaneApi = new Oceane($token, $headerConfig);

        if ($allCheck == '1') {
            $commentaire = $textFinalAll;

            $dataUpdate = array(
                "author" => $loginUser,
                "text" => StringTools::convertEncoding($commentaire, 'ISO-8859-1', 'UTF-8'),
                "commentType" => array(
                    "id" => "INT"
                ),
                "operationType" => array(
                    "id" => 9
                )
            );

            $oceaneApi->getResponseCommentaireAjout($oceaneApiData['url'], $ticketId, $dataUpdate);

        } else {
            foreach ($textFinalArray as $k => $value) {
                $commentaire = $textFinalArray[$k];

                $dataUpdate = array(
                    "author" => $loginUser,
                    "text" => StringTools::convertEncoding($commentaire, 'ISO-8859-1', 'UTF-8'),
                    "commentType" => array(
                        "id" => "INT"
                    ),
                    "operationType" => array(
                        "id" => 9
                    )
                );

                $oceaneApi->getResponseCommentaireAjout($oceaneApiData['url'], $ticketId, $dataUpdate);
            }
        }
        $this->send('OK');
    }


    public function produitsAssembleeAction()
    {
        $this->setRenderLayout(false);

        $refresh = $this->request->getFromPost('refresh', 0);

        if ($refresh == '1') {
            $idUtilisateur = $this->app->get('Session')->getUtilisateurId();
            $assemblee = $this->request->getFromPost('assemblee', '');

            $data = array(
                'identifiant' => $assemblee,
                'id_createur' => $idUtilisateur,
                'id_tableau' => 'BilanImpactGTRserviceAssemblee'
            );

            $this->analyseImpactRepo->purgetData($data);
        }
    }

    public function listeProduitsAction()
    {
        $this->disableRendering();

        $astroId = $this->request->getFromPost('id_astro', '');
        $ticketId = $this->astroRepo->getTicketByAstroId($astroId);
        $idTroncon = $this->request->getFromPost('id_troncon', '');
        $params = $this->request->getFromPost();
        $cableSession = $this->app->get('Session')->get('cable_infos_'. $ticketId);
        $idUtilisateur = $this->app->get('Session')->getUtilisateurId();
        $idCable = (is_array($cableSession) && !empty($cableSession) && key_exists('cable_id', $cableSession)) ? $cableSession['cable_id'] : 'inconnu';
        $familles = $this->analyseImpactRepo->getDataFamilleService();

        $data = $this->airelle->getDataProduits($idTroncon, $idUtilisateur, $familles, array(
            'id_section' => $idTroncon,
            'id_cable' => $idCable
        ), $params);

        return $this->sendEncodedToJson($data);
    }

    public function listeProduitsAssembleeAction()
    {
        $this->disableRendering();

        $assemblee = $this->request->getFromPost('assemblee', '');
        $equipement = $this->request->getFromPost('equipement', '');

        $params = $this->request->getFromPost();
        $idUtilisateur = $this->app->get('Session')->getUtilisateurId();

        if ($assemblee != '') {
            $data = $this->airelle->getDataProduitsAssemblee($assemblee, $idUtilisateur, $params);
        } else {
            $data = $this->airelle->getDataProduitsAssemblee($equipement, $idUtilisateur, $params);
        }

        return $this->sendEncodedToJson($data);
    }

    public function enteteProduitsAction()
    {
        $this->setRenderLayout(false);
        $astroId = $this->request->getFromPost('id_astro', '');
        $ticketId = $this->astroRepo->getTicketByAstroId($astroId);
        $idTroncon = $this->request->getFromPost('id_troncon', '');
        $cableSession = $this->app->get('Session')->get('cable_infos_'. $ticketId);
        $idUtilisateur = $this->app->get('Session')->getUtilisateurId();
        $idCable = (is_array($cableSession) && !empty($cableSession) && key_exists('cable_id', $cableSession)) ? $cableSession['cable_id'] : 'inconnu';
        $familles = $this->analyseImpactRepo->getDataFamilleService();
        $dslamsResponse = $this->airelle->getDslamImpactesAirele($idTroncon);
        $dslam = (is_object($dslamsResponse) && property_exists($dslamsResponse, 'code') && $dslamsResponse->message == 'no_data_found') ? array() : $dslamsResponse[0]->dslams;
        $bilanImpact = $this->airelle->bilanImpactGtrServiceTotalService($idTroncon, $idUtilisateur, $familles);

        return array_merge(
            $bilanImpact, array(
                'id_troncon' => $idTroncon,
                'id_cable' => $idCable,
                'dslam' => $dslam
            )
        );
    }

    public function enteteProduitsAssembleeAction()
    {
        $this->setRenderLayout(false);

        $dslam = $dslamsResponse = array();
        $idUtilisateur = $this->app->get('Session')->getUtilisateurId();
        $assemblee = $this->request->getFromPost('assemblee', '');
        $equipement = $this->request->getFromPost('equipement', '');
        $bilanImpact = array();
        $ticketId = $this->request->getFromPost('id_ticket', '');
        $astroSession = $this->app->get('Session')->get('astroOft' . $ticketId);
        $type = $astroSession['type'];
        if (($type == "SLN" || $type == "WDM_SID" || $type == "SDH" || $type == "OCH") && $assemblee != '') {
            $dslamsResponse = $this->airelle->getDataDslamViaAssemblyId($assemblee);
            $dslam = (is_object($dslamsResponse) && property_exists($dslamsResponse, 'code') && $dslamsResponse->message == 'no_data_found') ? array() : $dslamsResponse[0]->dslams;
        }
        if ($type == "WDM_SID" && $assemblee != '') {
            $familles = $this->analyseImpactRepo->getDataFamilleService();
            $bilanImpact = $this->airelle->bilanImpactGtrServiceTotalServiceWdm($assemblee, $idUtilisateur, $familles);
        }
        return array_merge(
            $bilanImpact, array(
                'assemblee' => $assemblee,
                'equipement' => $equipement,
                'dslam' => $dslam
            )
        );
    }


    public function jqgridProduitsAssembleeAction()
    {

        $this->disableRendering();

        $params = array();
        $params['_search'] = $this->getParam('_search');
        $params['filters'] = $this->getParam('filters');
        $params['page'] = $this->getParam('page');
        $params['rows'] = $this->getParam('rows');
        $params['supprimer'] = $this->getParam('supprimer');
        $params['sidx'] = $this->getParam('sidx');
        $params['sord'] = $this->getParam('sord');


        $params['id_section'] = strtoupper($this->getParam('id_section'));
        $param = StringTools::convertEncoding($params, 'ISO-8859-1', 'UTF-8');

        $liste = $this->app->get('Liste');

        $filters = "";
        if ($param['_search'] == "true") {
            $filters = json_decode(stripslashes($param['filters']));
        }

        // suppression de cache dans BD et pour fichier Excel
        if ($param['supprimer'] == "OK") {
            $this->fluxApiSqlRepository->cleanData('BilanImpactGTRserviceAssemblee');

            $default = $this->session->getContainer('Default');
            $default->html2xls = array(('BilanImpactGTRserviceAssemblee') => "");
            $sessionObject = $this->session->getSessionObject();
            $sessionObject->save();
        } else {
            $this->fluxApiSqlRepository->purgeData();
        }

        $dataRaw = $this->fluxApiSqlRepository->getData($param['id_section'], 'BilanImpactGTRserviceAssemblee');
        $download = false;

        if (empty($dataRaw)) {

            $data = $this->globalApiRepository->getDataTroncon($param, $this->connexionAirelle, $this->urlData['urlBilanImpactGTRserviceAssemblee'], $this->instanceAirelle);

            if (isset($data->message) && $data->message == 'no_data_found') {

                $this->send($liste->error());
            }

            $download = true;
        } else {

            $data = json_decode($dataRaw);
        }
        //********//gestion de l'historique
        if (count($data) > 0) {
            $v = array('nom' => $this->nomSess, 'prenom' => $this->prenomSess, 'id_createur' => $this->login, 'id_tableau' => 'BilanImpactGTRserviceAssemblee', 'domaine' => 'ASSEMBLEES', 'typedeproduit' => 'Assemblee', 'produit' => $param['id_section']);
            $this->historique->insertHistorique($v);
        }

        $dataArray = $this->dataXmlGrid->getDataGridProduitsAssemblee($data, $param, $this->dataFamilleService, $this->app);

        //getsion de flux
        if ((count($dataArray) > 0) && $download) {

            $this->fluxApiSqlRepository->insertData(array('id_createur' => $this->login, 'id_tableau' => 'BilanImpactGTRserviceAssemblee', 'identifiant' => $param['id_section'], 'blob' => json_encode($data)));
        }

        $page = 1;
        $array = $liste::getContentXml($dataArray, $param, $filters, 'BilanImpactGTRserviceAssemblee');

        $default = $this->session->getContainer('Default');
        $default->html2xls = array(('BilanImpactGTRserviceAssemblee') => $array['xls']);
        $sessionObject = $this->session->getSessionObject();
        $sessionObject->save();

        $this->send($this->dataXmlGrid->getXml($page, $array, ""));
    }

    public function insertCommentaireImpactProduitAction()
    {
        $this->disableRendering();

        $tronconId = $this->request->getFromPost('troncon_id', '');
        $cableId = $this->request->getFromPost('cable_id', '');
        $ticketId = $this->request->getFromPost('ticket_id', '');
        $this->analyseService->insertCommentaireImpactProduit($tronconId, $cableId, $ticketId);

        $this->send('OK');

    }

    public function getLabel($dataArray)
    {

        $msg = 'Il y a ';
        foreach ($dataArray as $k => $v) {
            if ($v > 0 && $k != '') {
                $msg .= ' ' . $v . ' ' . $k . ', ';
            }
        }
        $msg = substr($msg, 0, -2) . '.';

        return substr_replace($msg, ' et', strrpos($msg, ','), 1);
    }

    public function pingDslamAction()
    {
        $this->setRenderLayout(false);
        $data = $this->request->getFromPost('list_dslam', '');

        return array(
            'data' => $data
        );

    }

    public function pingTronconAction()
    {
        $this->setRenderLayout(false);
        $dataTroncon = $this->request->getFromPost('troncon', '');

        $this->app->get('Session')->set('troncon_infos', $dataTroncon);

        return array(
            'troncon' => $dataTroncon
        );

    }

    public function pingScanLiveAction()
    {
        $data = $this->request->getFromPost('list_dslam', '');
        $dataArray = explode(',', $data);
        $dataArray = array_map('trim', $dataArray);

        return $this->sendEncodedToJson($this->pingScanLive($dataArray));
    }

    public function pingScanLive($dataArray)
    {
        $scanLive = new ScanLiveFactory();
        $scanLive->getEquipmentsStatus($dataArray, 10, true);
        $resultPingDslam = $this->analyseImpactRepo->pingDslam($dataArray);
        foreach ($dataArray as $v) {
            $dslamBlobData = $this->edrRepository->getDslBrasseur(($v));
            if (count($dslamBlobData) > 1) {
                foreach ($resultPingDslam as $cle => $val) {
                    $val = array_map('trim', $val);
                    if (array_search(($v), $val)) {
                        $resultPingDslam[$cle]['BIGE'] = 'Oui';
                    }
                }
            }
        }
        return $resultPingDslam;
    }

    private function setDataTronconPingDslam($troncon)
    {
        $data = $this->airelle->getDataTronconNiveauUn($troncon);

        if (is_array($data) && !empty($data)) {

            $dslamList = array();
            if (is_array($data) && !empty($data)) {
                foreach ($data as $val) {
                    if (substr($val['produit'], 0, 2) == "DS") {
                        array_push($dslamList, $val['produit']);
                    }
                }
                $pingBige = $this->pingScanLive($dslamList);

                $result['nb_dslam'] = count($pingBige);
                $result['bige'] = '';
                foreach ($pingBige as $k => $v) {
                    if ($v['PING'] == 'true') {
                        $result['ping_dslam']['oui'][$k] = array('equipement' => $v['EQUIPEMENT'], 'ping_dt_requete' => $v['PING_DT_REQUETE']);
                    } elseif ($v['PING'] == 'false') {
                        $result['ping_dslam']['non'] [$k] = array('equipement' => $v['EQUIPEMENT'], 'ping_dt_requete' => $v['PING_DT_REQUETE']);
                    } elseif ($v['PING'] == 'not found') {
                        $result['ping_dslam']['notfound'][$k] = array('equipement' => $v['EQUIPEMENT'], 'ping_dt_requete' => $v['PING_DT_REQUETE']);
                    }
                    $result['bige'] = 'Non';
                    if ($v['BIGE'] == 'Oui') {
                        $result['bige'] = 'Oui';
                    }
                }
            }
            return $result;
        }
    }

    public function getPingDslamTronconAction()
    {
        $this->setRenderer('JsonRenderer');

        $result = [
            'nb_dslam' => 0,
            'bige' => '',
            'ping_dslam' => ''
        ];

        $troncon = $this->request->getFromPost('troncon', '');
        $resultPing = $this->setDataTronconPingDslam($troncon);
        if (is_array($resultPing)) {
            if (key_exists('nb_dslam', $resultPing) && $resultPing['nb_dslam'] > 0) {
                $result['nb_dslam'] = $resultPing['nb_dslam'];
            }
            if (key_exists('bige', $resultPing) && $resultPing['bige'] != '') {
                $result['bige'] = $resultPing['bige'];
            }
            if (key_exists('ping_dslam', $resultPing) && is_array($resultPing['ping_dslam']) && !empty($resultPing['ping_dslam'])) {
                $result['ping_dslam'] = $this->view->impactHelper()->getRowPingTroncon($resultPing['ping_dslam']);
            }
        }

        return $this->sendEncodedToJson($result);
    }

    public function lancerPingDslamAllAction()
    {
        $this->setRenderer('JsonRenderer');

        $dslams = $this->request->getFromPost('dslams', []);
        $dslams = array_unique($dslams);
        $resultReturn = [];

        $pingBige = $this->pingScanLive($dslams);
        foreach ($pingBige as $v) {
            $result = [];
            if($v['PING'] == 'true') {
                $result['ping_dslam']['oui'] = array('equipement'=> $v['EQUIPEMENT'],'ping_dt_requete'=> $v['PING_DT_REQUETE'] );
            } elseif($v['PING'] == 'false') {
                $result['ping_dslam']['non']= array('equipement'=> $v['EQUIPEMENT'],'ping_dt_requete'=> $v['PING_DT_REQUETE'] );
            } elseif($v['PING'] == 'not found'){
                $result['ping_dslam']['notfound'] = array('equipement'=> $v['EQUIPEMENT'],'ping_dt_requete'=> $v['PING_DT_REQUETE'] );
            }

            $resultReturn[$v['EQUIPEMENT']] = $this->view->impactHelper()->getRowPingTronconOne($result['ping_dslam'], $v['EQUIPEMENT']);
        }

        return $this->sendEncodedToJson($resultReturn, true, 'ISO-8859-15');
    }

}
