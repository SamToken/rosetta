<?php


namespace App\Service;


use App\Tools\OceaneTools;
use Oft\Mvc\Application;

class VariableBaseService extends AstroBaseService
{
    /**
     * @var Application
     */
    protected $app;

    protected $findAndGet;

    /**
     * @var AdminFonctionService
     */
    protected $adminFonction;

    public function __construct($app)
    {
        $this->app = $app;
        if (is_null($this->findAndGet)) {
            $this->findAndGet = $this->app->get('OceaneService')->findAndGetOceane($this->ticketId);
        }
    }

    public function getVariableAdminValue($tabIdentifiants)
    {
        $this->adminFonction = $this->app->get('AdminFonction');
        foreach ($tabIdentifiants as $identifiant) {

            switch ($identifiant['SOURCE_GLOBALE']) {
                case 'PARAMETRE':
                    if (property_exists($this->findAndGet['installed_resource']->Parameters, 'Parameter')) {
                        $res = OceaneTools::searchValueInFindAndGet($identifiant['SOURCE'], $this->findAndGet['installed_resource']->Parameters->Parameter);
                        $res = ($identifiant['MIN_MAJ'] == "MIN") ? strtolower($res) : strtoupper($res);
                        if (!is_null($res)) {
                            return $res;
                        }
                    }
                    break;
                case 'ATTRIBUT':
                    if (property_exists($this->findAndGet['installed_resource']->Attributes, 'Attribute')) {
                        $res = OceaneTools::searchValueInFindAndGet($identifiant['SOURCE'], $this->findAndGet['installed_resource']->Attributes->Attribute);
                        $res = ($identifiant['MIN_MAJ'] == "MIN") ? strtolower($res) : strtoupper($res);
                        if (!is_null($res)) {
                            return $res;
                        }
                    }
                    break;
                case 'IDENTIFIANT':
                    $res = $this->adminFonction->getDataFromId($identifiant, $this->ticketId);
                    $res = ($identifiant['MIN_MAJ'] == "MIN") ? strtolower($res) : strtoupper($res);
                    if (!is_null($res)) {
                        return $res;
                    }
                    break;
                default:
                    break;
            }
        }
        return false;
    }

    /**
     * Récupération Dslam
     *
     * @param string $type
     * @return boolean|string
     */
    protected function getDslam($type)
    {
        $monDslam = false;
        if ($this->id1) {
            $dslam = substr($this->id1, 0, 8);
            switch ($type) {
                case 'MAJ':
                    $monDslam = strtoupper($dslam);
                    break;
                case 'MIN':
                    $monDslam = strtolower($dslam);
                    break;
                default:
                    break;
            }
        }
        return $monDslam;
    }

    /**
     * Récupération du code nidt
     *
     * @return string
     */
    public function getCodeNidt()
    {
        return substr($this->id2, 0, 10);
    }
}