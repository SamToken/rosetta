<?php
/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

namespace App\Service;

use App\Repository\AstroRepository;
use App\Repository\TraceRepository;
use App\Tools\OceaneAssistant;
use Hbm\Common\Service\LinkService;
use Hbm\Common\Tools\StringTools;
use Hbm\Globalapi\Factory\OrchestraFactory;
use Hbm\Globalapi\Service\Rest\Orchestra;
use \Oft\Mvc\Application;

/**
 * Description of MaestroService
 *
 * @author mbiyoud
 */
class OrchestraService
{

    /**
     * @var Application
     */
    protected $app;
    /**
     * @var AstroRepository
     */
    protected $astroRepository;
    /**
     * @var GlobalApiUrlService
     */
    protected $globalApiService;

    /**
     * @var GatapeService
     */
    protected $getapeService;

    /**
     * @var TraceRepository
     */
    protected $traceRepository;

    /**
     * @var AireleService
     */
    protected $airele;

    /**
     * @var AstroBaseService
     */
    protected $astroBase;

    public function __construct(Application $app)
    {
        $this->app = $app;
        $this->astroRepository = $this->app->get('AstroRepository');
        $this->globalApiService = $this->app->get('GlobalApiUrlService');
    }

    /**
     * Test d'un produit par Orchestra
     *
     * @param $produit
     * @param array $traceInfos
     * @param $loginId
     * @param bool $cache
     * @param int $interval
     * @return array
     */
    public function testProduit($produit, array $traceInfos, $loginId, $cache = false, $interval = 0)
    {
        $astroId = $traceInfos['astroId'];
        $sessIs = $traceInfos['sessIs'];
        $ticketId = $traceInfos['ticketId'];

        $this->getapeService = $this->app->get('Gatape');
        $this->traceRepository = $this->app->get('TraceRepository');
        $orchestraApiData = $this->globalApiService->getUrlApi('API_ORCHESTRA');

        $token = $this->getapeService->getToken($orchestraApiData);
        $headerConfig = array(
            "X-ORC-Sync: true",
            "X-ORC-userProfile: HBM",
            "X-ORC-userName: $loginId"
        );
        $orchestra = new OrchestraFactory($token, $headerConfig);

        $this->traceRepository->setTrace($astroId, "ENVOI TEST ORCHESTRA - $produit", $produit, $sessIs, $ticketId);
        if (!$cache) {
            $retourOrchestra = $orchestra->getDiagnosisStatus($ticketId, $produit);
        } else {
            $retourOrchestra = $orchestra->getDiagnosisStatus($ticketId, $produit, $interval);
        }

        $retourOrchestra = StringTools::convertEncoding($retourOrchestra, 'ISO-8859-15', 'UTF-8');
        $this->traceRepository->setTrace($astroId, "RETOUR TEST ORCHESTRA - $produit", $retourOrchestra, $sessIs, $ticketId);

        $dataTestOrchestra = $this->formatOrchestraResponse($retourOrchestra, $produit);
        return $dataTestOrchestra;
    }
    public function testProduitEtx($produit, array $traceInfos, $loginId, $cache = false, $interval = 0)
    {
        $astroId = $traceInfos['astroId'];
        $sessIs = $traceInfos['sessIs'];
        $ticketId = $traceInfos['ticketId'];

        $this->getapeService = $this->app->get('Gatape');
        $this->traceRepository = $this->app->get('TraceRepository');
        $orchestraApiData = $this->globalApiService->getUrlApi('API_ORCHESTRA');

        $token = $this->getapeService->getToken($orchestraApiData);
        $headerConfig = array(
            "X-ORC-Sync: true",
            "X-ORC-userProfile: HBM",
            "X-ORC-userName: $loginId"
        );
        $orchestra = new OrchestraFactory($token, $headerConfig);

        $this->traceRepository->setTrace($astroId, "ENVOI TEST ORCHESTRA - $produit", $produit, $sessIs, $ticketId);
        
        // DEBUG: Log the input before calling Orchestra
        error_log("DEBUG ETX: Appell Orchestra pour produit: $produit, ticket: $ticketId");

        if (!$cache) {
            $retourEtx = $orchestra->getEtxStatus($ticketId, $produit);
        } else {
            $retourEtx = $orchestra->getEtxStatus($ticketId, $produit, $interval);
        }

        // DEBUG: Log the raw response from Orchestra
        error_log("DEBUG ETX: Retour Orchestra pour produit $produit: " . print_r($retourEtx, true));

        $retourEtx = StringTools::convertEncoding($retourEtx, 'ISO-8859-15', 'UTF-8');
        $this->traceRepository->setTrace($astroId, "RETOUR TEST ORCHESTRA- ETAT ETX - $produit", $retourEtx, $sessIs, $ticketId);

        $dataTestEtx = $this->formatOrchestraResponseEtx($retourEtx, $produit);
        return $dataTestEtx;
    }

    /**
     * Test tous les produits d'un troncon par Orchestra
     * @param $troncon
     * @param array $traceInfos
     * @param $loginId
     * @return array
     */
    public function testTroncon($troncon, array $traceInfos, $loginId, $cache = 1)
    {
        $synthseTest = [];
        $synthseTest['error'] = [];
        $synthseTest['ko'] = [];
        $synthseTest['ok'] = [];
        $synthseTest['error-talia'] = [];
        $this->airele = $this->app->get('Airele');

        $occupationUn = $this->airele->getOccupationNiveauUnFromCache($troncon, $traceInfos['ticketId']);
        $occupationUn = array_map("unserialize", array_unique(array_map("serialize", $occupationUn)));

        if (is_array($occupationUn) && !empty($occupationUn)) {
            $this->astroBase = $this->app->get('AstroBase');
            $fromCache = $cache == 1;
            $cacheOrchestra = intval($this->app->get('AssistantRepository')->getParamsMobile('CACHE_ORCHESTRA'));
            foreach ($occupationUn as $value) {
                if (key_exists('PRODUIT', $value) && $value['PRODUIT'] && $this->astroBase->isTestableProduct($value['PRODUIT'])) {
                    $testProduit = $this->testProduit($value['PRODUIT'], $traceInfos, $loginId, $fromCache, $cacheOrchestra);
                    if ($testProduit['status'] == 'error') {
                        $synthseTest['error'][] = $testProduit;
                    }if($testProduit["status"] == "error-talia") {
                        $synthseTest['error-talia'][] = $testProduit;
                    }elseif ($testProduit['status'] == 'ok' && $testProduit['criticality'] == '0') {
                        $synthseTest['ok'][] = $testProduit;
                    } elseif ($testProduit['status'] == 'ok' && $testProduit['criticality'] != '0') {
                        $synthseTest['ko'][] = $testProduit;
                    }
                }
            }
        }
        return $synthseTest;
    }
    private function formatOrchestraResponse($retourOrchestra , $produit){
        $dataTestOrchestra = [];
        if (is_array($retourOrchestra) && key_exists('endDate', $retourOrchestra) && $retourOrchestra['endDate'] != null && !is_bool($retourOrchestra['endDate'])) {
            $oceaneAssist = new OceaneAssistant($this->app);
            $dataTestOrchestra['tested_at'] = $oceaneAssist->changeFormat($retourOrchestra['endDate'], 'Y-m-d\TH:i:s.uP');
        } else {
            $dataTestOrchestra['tested_at'] = date('d/m/Y H:i');
        }

        if (!is_array($retourOrchestra) || empty($retourOrchestra) || key_exists('code', $retourOrchestra) &&   !key_exists( "error-talia",$retourOrchestra)) {
            $dataTestOrchestra['status'] = 'error';
            $dataTestOrchestra['id_produit'] = $produit;
        } else if( key_exists('code', $retourOrchestra) && key_exists( "error-talia",$retourOrchestra)){
            $dataTestOrchestra['status'] = 'error-talia';
            $dataTestOrchestra['id_produit'] = $produit;
            $parametres = [
                'diagId' =>  key_exists('diagnosis-id', $retourOrchestra) ? $retourOrchestra['diagnosis-id'] : '',
                'diagType' => 'FG'
            ];
            $this->instance = $this->app->config['ENV'];
            $this->linkCommonService = new LinkService($this->app);
            $dataTestOrchestra['url_consult_test'] = $this->linkCommonService->getGlobalLink('ORCHESTRA_CONSULTATION', $this->instance, $parametres);

        }
        else {
            if (is_array($retourOrchestra) && !empty($retourOrchestra) && key_exists('conclusions', $retourOrchestra) && key_exists('diagnosisId', $retourOrchestra)) {
                $diagnosisId = $retourOrchestra['diagnosisId'];
                if (!empty($retourOrchestra['conclusions']) && is_array($retourOrchestra['conclusions'][0]) && !empty($retourOrchestra['conclusions'][0]) && key_exists('criticality', $retourOrchestra['conclusions'][0]) && key_exists('rulename', $retourOrchestra['conclusions'][0])) {
                    $this->instance = $this->app->config['ENV'];
                    $this->linkCommonService = new LinkService($this->app);
                    $dataTestOrchestra['status'] = 'ok';
                    $parametres = [
                        'diagId' => $diagnosisId,
                        'diagType' => 'FG'
                    ];
                    $dataTestOrchestra['url_consult_test'] = $this->linkCommonService->getGlobalLink('ORCHESTRA_CONSULTATION', $this->instance, $parametres);
                    $dataTestOrchestra['id_produit'] = $produit;
                    $dataTestOrchestra['criticality'] = $retourOrchestra['conclusions'][0]['criticality'];
                    $dataTestOrchestra['rulename'] = $retourOrchestra['conclusions'][0]['rulename'];
                } else {
                    $dataTestOrchestra['status'] = 'error';
                    $dataTestOrchestra['id_produit'] = $produit;
                }
            } else {
                $dataTestOrchestra['status'] = 'error';
                $dataTestOrchestra['id_produit'] = $produit;
            }
        }
        return $dataTestOrchestra;
    }
    private function formatOrchestraResponseEtx($retourOrchestra , $produit){
        $dataTestOrchestra = [];
        $status = '';
        if (is_array($retourOrchestra) && key_exists('endDate', $retourOrchestra) && $retourOrchestra['endDate'] != null && !is_bool($retourOrchestra['endDate'])) {
            $oceaneAssist = new OceaneAssistant($this->app);
            $dataTestOrchestra['tested_at'] = $oceaneAssist->changeFormat($retourOrchestra['endDate'], 'Y-m-d\TH:i:s.uP');
        } else {
            $dataTestOrchestra['tested_at'] = date('d/m/Y H:i');
        }

        if (!is_array($retourOrchestra) || empty($retourOrchestra) || key_exists('code', $retourOrchestra) &&   !key_exists( "error-talia",$retourOrchestra)) {
            $dataTestOrchestra['status'] = 'error';
            $dataTestOrchestra['id_produit'] = $produit;
        } else if( key_exists('code', $retourOrchestra) && key_exists( "error-talia",$retourOrchestra)){
            $dataTestOrchestra['status'] = 'error-talia';
            $dataTestOrchestra['id_produit'] = $produit;
            $parametres = [
                'diagId' =>  key_exists('diagnosis-id', $retourOrchestra) ? $retourOrchestra['diagnosis-id'] : '',
                'diagType' => 'FG'
            ];
            $this->instance = $this->app->config['ENV'];
            $this->linkCommonService = new LinkService($this->app);
            $dataTestOrchestra['url_consult_test'] = $this->linkCommonService->getGlobalLink('ORCHESTRA_CONSULTATION', $this->instance, $parametres);

        }
        else {

            if (key_exists('tests', $retourOrchestra) &&
                !empty($retourOrchestra['tests']) &&
                key_exists('categorizedValues', $retourOrchestra['tests'][0]) &&
                !empty($retourOrchestra['tests'][0]['categorizedValues']) &&
                key_exists('datavalues', $retourOrchestra['tests'][0]['categorizedValues'][0]) &&
                !empty($retourOrchestra['tests'][0]['categorizedValues'][0]['datavalues']) &&
                key_exists('value', $retourOrchestra['tests'][0]['categorizedValues'][0]['datavalues'][0])) {
                $status = $retourOrchestra['tests'][0]['categorizedValues'][0]['datavalues'][0]['value'];
            }

            if (is_array($retourOrchestra) && !empty($retourOrchestra) && key_exists('conclusions', $retourOrchestra) && key_exists('diagnosisId', $retourOrchestra)) {
                $diagnosisId = $retourOrchestra['diagnosisId'];
                if (!empty($retourOrchestra['conclusions']) && is_array($retourOrchestra['conclusions'][0]) && !empty($retourOrchestra['conclusions'][0]) && key_exists('criticality', $retourOrchestra['conclusions'][0]) && key_exists('rulename', $retourOrchestra['conclusions'][0])) {
                    $this->instance = $this->app->config['ENV'];
                    $this->linkCommonService = new LinkService($this->app);
                    $dataTestOrchestra['status'] = 'ok';
                    $parametres = [
                        'diagId' => $diagnosisId,
                        'diagType' => 'FG'
                    ];
                    $dataTestOrchestra['url_consult_test'] = $this->linkCommonService->getGlobalLink('ORCHESTRA_CONSULTATION', $this->instance, $parametres);
                    $dataTestOrchestra['id_produit'] = $produit;
                    $dataTestOrchestra['criticality'] = $retourOrchestra['conclusions'][0]['criticality'];
                    $dataTestOrchestra['rulename'] = $retourOrchestra['conclusions'][0]['rulename'];
                    $dataTestOrchestra['status_etx'] = $status;
                } else {
                    $dataTestOrchestra['status'] = 'error';
                    $dataTestOrchestra['id_produit'] = $produit;
                }
            } else {
                $dataTestOrchestra['status'] = 'error';
                $dataTestOrchestra['id_produit'] = $produit;
            }
        }
        return $dataTestOrchestra;
    }
}
