<?php

namespace App\Tools;

use App\Repository\AstroIhmSqlRepository;
use Oft\Mvc\Application;

/**
 * Class OceaneAssistant
 * Classe Assistant Itération
 *
 * @version 1.0
 * @package
 *
 */
class OceaneAssistant
{

    /**
     * @var Application
     */
    public $app;

    protected $astroRepository;

    /**
     * @var AstroIhmSqlRepository
     */
    protected $repositoryAstroSqlIhm;

    // const
    const DSLAM = 'DSLAM';
    const DSLAM_MIN = 'dslam';
    const CHASSIS = 'CHASSIS';
    const CHASSIS_MIN = 'chassis';
    const DSLAMSUBRACK = 'DSLAMSUBRACK';
    const DSLAMRACK = 'DSLAMRACK';
    const DSLAMSLOT = 'DSLAMSLOT';
    const CARTE = 'CARTE';
    const PORT = 'PORT';
    const VP = 'VP';
    const DSLAMPORT = 'DSLAMPORT';
    const SOPCNX = 'SOPCNX';
    const SOPLINK = 'SOPLINK';
    const VLAN = 'VLAN';
    const ID_TYPE_RESSOURCE = 'ID_TYPE_RESSOURCE';
    const PRIORITY_ID = 'PRIORITY_ID';
    const LIBELLE = 'LIBELLE';
    const IDENTIFIANT = 'IDENTIFIANT';
    const COUPURE_FRANCHE = 'Coupure franche';
    const OPTIONS = 'options';
    const DATE_FORMAT = 'd/m/Y H:i';

    public function __construct($app)
    {
        $this->app = $app;
        $this->repositoryAstroSqlIhm = $this->app->get('AstroIhmSqlRepository');
        $this->astroRepository = $this->app->get('AstroRepository');
    }

    /**
     * Récupère la durée de rétablissement
     *
     * @return string
     */
    public function lbAlarmeSurRessource($rsc)
    {
        $r = $rsc['LB_COURT'] . " ";
        $r .= $rsc[self::DSLAM];
        $r .= (strlen($rsc[self::CHASSIS]) > 0) ? "/" . $rsc[self::CHASSIS] : "";
        $r .= (strlen($rsc[self::CARTE]) > 0) ? "/" . $rsc[self::CARTE] : "";
        $r .= (strlen($rsc[self::PORT]) > 0) ? "/" . $rsc[self::PORT] : "";
        $r .= (strlen($rsc[self::VP]) > 0) ? "/" . $rsc[self::VP] : "";
        $r .= (strlen($rsc[self::VP]) > 0) ? "/" . $rsc[self::VP] : "";
        return $r;
    }

    /**
     * Récupère la durée de rétablissement
     *
     * @return string
     */
    public function getDureeRetab()
    {
        $tabDuree = $this->repositoryAstroSqlIhm->getDureeRetablissement();
        $ret = '';
        if (count($tabDuree) > 0) {
            foreach ($tabDuree as $v) {
                $ret .= "\tarrDuree['" . $v[self::PRIORITY_ID] . "'] = " . $v['DUREE_RETABLISSEMENT_MAX'] . ";\r\n";
            }
        }
        return $ret;
    }

    public function getDureeRetabInitialGenerique($array)
    {
        $ret = '';
        if (count($array) > 0) {
            foreach ($array as $k => $v) {
                $ret .= "\tarrDuree['" . substr($k, 1) . "'] = " . $v . ";\r\n";
            }
        }

        return $ret;
    }

    // Changer le format d'une date 20/04/2017 14:15 vers 2017-04-20T14:15:00.000
    public function changeDateToUTCoceane($date)
    {
        if ($date != null && $date != '') {
            $date = \DateTime::createFromFormat(self::DATE_FORMAT, $date);
            if ($date != null) {
                $date = gmdate('c', $date->getTimestamp());
            }
        }else{
            $date = new \DateTime($date);
            $date->format('d/m/Y H:i');
            if ($date != null) {
                $date = gmdate('c', $date->getTimestamp());
            }
        }

        return $date;
    }
    // Changer le format d'une date 20/04/2017 14:15 vers 2017-04-20T14:15Z
    public function changeDateToUTCZuluoceane($date)
    {
        if ($date != null && $date != '') {
            $date = \DateTime::createFromFormat(self::DATE_FORMAT, $date);
            if ($date != null) {
                $date = gmdate('Y-m-d\TH:i:s\Z', $date->getTimestamp());
            }
        }else{
            $date = new \DateTime($date);
            $date->format('d/m/Y H:i');
            if ($date != null) {
                $date = gmdate('Y-m-d\TH:i:s\Z', $date->getTimestamp());
            }
        }

        return $date;
    }

    public function changeZuluToFormat($date, $format = self::DATE_FORMAT)
    {
        $date = \DateTime::createFromFormat('Y-m-d\TH:i:s.u\Z', $date);
        if (gettype($date) !== 'boolean') {
            return $date->format($format);
        }
        return '';
    }

    public static function changeFormat($date, $fromFormat, $format = self::DATE_FORMAT)
    {
        $date = \DateTime::createFromFormat($fromFormat, $date);

        if (gettype($date) !== 'boolean') {
            return $date->format($format);
        }
        return '';
    }

    // Changer le format d'une date 20/04/2017 14:15 vers 2017-04-20T14:15:00.000 + add a minute
    public function changeDateToUTCoceanePlusAminute($date)
    {
        $minutes_to_add = 1;

        if ($date != null && $date != '') {
            $date = \DateTime::createFromFormat(self::DATE_FORMAT, $date);
            if ($date != null) {
                $date = gmdate('c', $date->getTimestamp());
            }
        }else{
            $date = new \DateTime($date);

            $date->add(new \DateInterval('PT' . $minutes_to_add . 'M'));
            $date->format('d/m/Y H:i');

            if ($date != null) {
                $date = gmdate('c', $date->getTimestamp());
            }
        }

        return $date;
    }

    // Changer le format d'une date 20/04/2017 14:15 vers 2017-04-20T14:15:00.000
    public function changeDateToUTCAdelia($date, $format = 'US')
    {
        if ($format == 'US') {
            $date = \DateTime::createFromFormat('d/m/Y H:i', $date);
        } elseif ($format == 'FR') {
            $date = \DateTime::createFromFormat('d-m-Y H:i', $date);
        }
        return $date->format('Y-m-d\TH:iO');
    }

    /**
     * Change une date UTC en une date au format d/m/Y H:i
     *
     * @param
     *            $dateUTC
     * @return \DateTime|string
     */
    public function changeUTCToDate($dateUTC)
    {
        $utc_ts = strtotime($dateUTC . " UTC");
        return date(self::DATE_FORMAT, $utc_ts);
    }

    /**
     * Change une date UTC en une date au format d-m-Y H:i
     *
     * @param
     *            $dateUTC
     * @return false|string
     */
    public function changeUTCToDateStd($dateUTC)
    {
        $utc_ts = strtotime($dateUTC . " UTC");
        return date('d-m-Y H:i', $utc_ts);
    }

    /**
     * Change une date UTC au format Y-m-d H:i:s
     *
     * @param
     *            $dateUTC
     * @return string
     */
    public function changeUTCToDateJS($dateUTC)
    {
        $date = new \DateTime($dateUTC);
        return $date->format('Y-m-d H:i:s');
    }

    /**
     * Change une date non UTC au format Y-m-d H:i:s
     *
     * @param
     *            $date
     * @return false|string
     */
    public function changeNoUTCToDateJS($date)
    {
        $utc_ts = strtotime($date . " UTC");
        return date('Y-m-d H:i:s', $utc_ts);
    }

    /**
     * Change une date UTC au format Y-m-d H:i
     *
     * @param
     *            $date
     * @return bool|string
     */
    public function changeUTCToDateYmd($dateUTC)
    {
        $utc_ts = strtotime($dateUTC . " UTC");
        return date('Y-m-d H:i', $utc_ts);
    }

    /**
     * Retourne un tableau détaillé de la date UTC, avec date d/m/Y, heures et minutes
     *
     * @param
     *            $dateUTC
     * @return mixed
     */
    public function changeUTCToDateDetail($dateUTC)
    {
        $utc_ts = strtotime($dateUTC . " UTC");
        $tab['date'] = date('d/m/Y', $utc_ts);
        $tab['heure'] = date('H', $utc_ts);
        $tab['minute'] = date('i', $utc_ts);
        return $tab;
    }

    /**
     *
     * @return string
     */
    public function refresh()
    {
        return '<script>javascript:refresh();</script>';
    }

    public function getWaitHtml($id = '')
    {
        return '<div id="' . $id . '"><div id="wait" style="width:80px;margin-left:auto;margin-right:auto;"><span class="wait" ></span></div></div>';
    }

    /**
     * Convertit array to xml
     *
     * @param
     *            $array
     * @param
     *            $xml_user_info
     * @return mixed
     */
    public function arrayToXml($array, &$xml_user_info)
    {
        foreach ($array as $key => $value) {
            if (is_array($value)) {
                if (!is_numeric($key)) {
                    $subnode = $xml_user_info->addChild("$key");
                    $this->array_to_xml($value, $subnode);
                } else {
                    $subnode = $xml_user_info->addChild("item$key");
                    $this->arrayToXml($value, $subnode);
                }
            } else {
                $xml_user_info->addChild("$key", htmlspecialchars("$value"));
            }
        }
        return $xml_user_info;
    }

    /**
     * Tronquer proprement une chaine de caractères trop longue
     *
     * @param $chaine
     * @param $lg_max
     * @param string $ending
     * @return bool|string
     */
    public function tronque($chaine, $lg_max = 300, $ending = "&nbsp;[...]")
    {
        if (strlen($chaine) > $lg_max) {
            $chaine = substr($chaine, 0, $lg_max);
            $last_space = strrpos($chaine, " ");
            $chaine = substr($chaine, 0, $last_space) . $ending;
        }
        return $chaine;
    }

    /**
     * Supprime les quotes '
     *
     * @param
     *            $str
     * @return mixed
     */
    public function antiquote($str)
    {
        return str_replace("'", " ", $str);
    }

    /**
     *
     * @return array $classe = dslam, dslamSubRack, etc.
     *         $objet = /T2 /DSCR8102-C11/INTERNET/2311 ou /T1 DS1ZZ999-C11
     */
    public function detailMateriel($objet, $classe, $code, $label, $default)
    {
        $tab = array();
        $tabValide = array(
            self::DSLAM,
            self::DSLAMSUBRACK,
            self::DSLAMSLOT,
            self::DSLAMPORT,
            self::SOPCNX,
            'DSLAMPORTSYSTEM',
            self::SOPLINK,
            self::DSLAMRACK
        );
        if (!in_array(strtoupper(trim($classe)), $tabValide)) { // TODO : prévoir les cas de figure un peu foireux...
            $objet = $default;
            $classe = "";
        }

        $result = array();
        $result['BL_OLT'] = "0"; // C'est un DSLAM. // TODO : prévoir pour les OLT

        $classe = strtoupper(trim($classe));
        // Cas spécifique : /T1 DS1ZZ999-C11 - Pas de / entre T1 et DSLAM-Chassis
        if (strlen($classe) > 0 && substr($objet, 4, 1) != '/') {
            $objet = substr_replace($objet, '/', 3, 1);

        } // TODO : cette règle est très douteuse. À vérifier.

        $tabObjet = explode("/", $objet);
        if (count($tabObjet) == 1 && $classe != '') {
            $tabObjet = explode("\\", $objet);
        }


        foreach ($tabObjet as $value) {
            if ($value != "" && $value != " ") {
                $tab[] = trim($value);
            }
        }

        if ($classe == self::SOPCNX) {
            if (in_array($code, array(4510, 4511, 4514, 4515, 4516))) { // /X0 /DSSTP160-C10/INTERNET/835 --> extraire DSLAM : DSSTP160 et Vlan : 835
                $cd = $this->chassisDslam($tab['1']);
                $result[self::DSLAM] = $cd[self::DSLAM_MIN];  // Affiche
                if (isset($cd[self::CHASSIS_MIN]) && count($cd[self::CHASSIS_MIN]) > 0) {
                    $result[self::CHASSIS] = $cd[self::CHASSIS_MIN];
                }  // NON Affiché
                if (count($tab) > 3) {
                    $result[self::VLAN] = $tab[3];
                }
                $result[self::ID_TYPE_RESSOURCE] = 5;
                /* TODO :
                    Collecter le routeur de raccordement du DSLAM dans les données enrichies EDR
                    Effectuer un calcul d'impact et un Adelia de niveau VLAN en précisant le nom DSLAM, le nom Routeur et le n° Vlan
                 */
            } else {
                if (in_array($code, array(4500, 0)) || (strpos($label, 'DERCO ADSL VP') > -1)) { // /R0 /DSLOGA01-C00/NET/DSLOGA01VP11-BSROU258-CSERV UBR // /S0 /DSSEM401-Cxx/NET/DSSEM401VP11 (sopCnx) VP DERCO
                    $cd = $this->chassisDslam($tab['1']);
                    $result[self::DSLAM] = $cd[self::DSLAM_MIN];  // Affiche
                    if (key_exists(self::CHASSIS_MIN, $cd) && is_array($cd[self::CHASSIS_MIN]) && count($cd[self::CHASSIS_MIN]) > 0) {
                        $result[self::CHASSIS] = $cd[self::CHASSIS_MIN];
                    }  // NON Affiché
                    $nimp = explode("-", $tab[3]);
                    $nimp = explode("VP", $nimp[0]);
                    $result[self::VP] = key_exists(1, $nimp) ? $nimp[1] : '';
                    $result[self::ID_TYPE_RESSOURCE] = 6;
                    /* TODO : Collecter le brasseur
                     Collecter le brasseur de raccordement du DSLAM dans les données enrichies EDR
                     Effectuer un calcul d'impact et un Adelia de niveau Connexion de Vp en précisant le nom DSLAM, le nom NPA (Brasseur) et le n° VP
                     */
                }
            }
        } else {
            if ($classe == self::SOPLINK) {
                $cd = $this->chassisDslam($tab['1']);
                $result[self::DSLAM] = $cd[self::DSLAM_MIN];  // Affiche
                if (isset($cd[self::CHASSIS_MIN]) && count($cd[self::CHASSIS_MIN]) > 0) {
                    $result[self::CHASSIS] = $cd[self::CHASSIS_MIN];
                }  // NON Affiché
                $result[self::ID_TYPE_RESSOURCE] = 9;
            } else {
                if ($classe == '') { // Quand on n'a pas de F&G...
                    $cd = $this->chassisDslam($objet);
                    $result[self::DSLAM] = $cd[self::DSLAM_MIN];  // Affiche

                    if (isset($cd[self::CHASSIS_MIN]) && count((is_countable($cd[self::CHASSIS_MIN]) ? $cd[self::CHASSIS_MIN] : [])) > 0) {
                        $result[self::CHASSIS] = $cd[self::CHASSIS_MIN];
                        $result[self::ID_TYPE_RESSOURCE] = 2;
                    } else {
                        $result[self::ID_TYPE_RESSOURCE] = 1;
                    }
                } else {
                    $cd = $this->chassisDslam($tab['1']);
                    if ($tab['1'] == '') {
                        $cd = $this->chassisDslam($tab['0']);
                    }
                    $result[self::DSLAM] = $cd[self::DSLAM_MIN];  // Affiche
                    if (is_array($cd) && key_exists(self::CHASSIS_MIN, $cd)) {
                        $result[self::CHASSIS] = $cd[self::CHASSIS_MIN];
                    }

                    if (count($tab) > 2) {
                        $result[self::DSLAMRACK] = $tab[2];
                    }
                    if (count($tab) > 3) {
                        $result[self::DSLAMSUBRACK] = $tab[3];
                    }  // Affiche
                    if ($classe == self::DSLAM && key_exists(self::CHASSIS_MIN, $cd) && $cd[self::CHASSIS_MIN] != '') {
                        $result[self::ID_TYPE_RESSOURCE] = 2;
                    } elseif ($classe == self::DSLAM) {
                        $result[self::ID_TYPE_RESSOURCE] = 1;
                    }
                    if ($classe == self::DSLAMRACK) {
                        $result[self::ID_TYPE_RESSOURCE] = 7;
                    }
                    if ($classe == self::DSLAMSUBRACK) {
                        $result[self::ID_TYPE_RESSOURCE] = 2;
                    }
                    if ($classe == self::DSLAMSLOT) {
                        // ?	Si on est dans le premier cas, c?est-à-dire qu'on trouve après /XX/DSxxxxxx-Cij/  3 entiers séparés par des « / »  (n, m et k)  alors ASTRO porte sur un type de ressource carte : DSxxxxxx , Châssis Cij, carte k (on ne tient pas compte de n et m pourvu que ce soient des nombres)
                        //Si on n?est pas dans le premier cas, c?est-à-dire qu?on n?a pas 3 entiers séparés par des « / », alors ASTRO se reporte sur un type de ressource châssis : DSxxxxxx, châssis Cij
                        if (is_numeric($tab[2]) && is_numeric($tab[3]) && key_exists(4, $tab) && is_numeric($tab[4])) {
                            $result[self::DSLAMSLOT] = $tab[4];  // Affiche
                            $result[self::ID_TYPE_RESSOURCE] = 3;
                        } else {
                            $result[self::ID_TYPE_RESSOURCE] = 2;
                        }
                    }
                    if ($classe == self::DSLAMPORT) {
                        $result[self::DSLAMSLOT] = key_exists(4, $tab) ? $tab[4] : '';
                        $result[self::DSLAMPORT] = key_exists(5, $tab) ? $tab[5] : ''; // Affiche
                        $result[self::ID_TYPE_RESSOURCE] = 4;
                    }
                }
            }
        }
        return $result;
    }

    /**
     * Retrouver l'identifiant chassis et/ou DSLAM en fonction des infos envoyées.
     * DSHLZ102 --> DSLAM
     * DSESP302-C41 --> DSLAM DSESP302 + chassis C41
     *
     * @param
     *            $id
     * @return mixed
     */
    private function chassisDslam($id)
    {
        $tab = explode("-", $id);
        $result['origine'] = $id;
        $result['type'] = self::DSLAM;
        $result[self::DSLAM_MIN] = $tab[0];
        if (count($tab) > 1 && $tab[1] != "") {
            $result[self::CHASSIS_MIN] = $tab[1];
            $result['type'] = self::CHASSIS_MIN;
        }
        return $result;
    }

    /**
     * Afficher la ressource sur la page d'accueil
     * @param $tabRessource
     * @param $classe
     * @return string
     */
    public function afficheDetailMateriel($tabRessource, $classe)
    {
        $t = [];
        if (count($tabRessource) < 2) {
            echo "Erreur : aucune ressource à traiter. ";
            return null;
        }
        $classe = strtoupper($classe);
        if ($classe == self::SOPCNX) {
            if ($tabRessource[self::VLAN] != "") {
                $t[] = "VLAN " . $tabRessource[self::VLAN];
            } else {
                if ($tabRessource[self::VP] != "") {
                    $t[] = "VP " . $tabRessource[self::VP];
                }
            }
        } else {
            if ($classe == self::SOPLINK) {
                $t[] = $tabRessource[self::DSLAM];
            } else {
                if ($classe == self::DSLAM) {
                    $t[] = $tabRessource[self::DSLAM];
                } // Si c'est un DSLAM, on n'affiche pas le chassis logique
                else {
                    $t[] = $tabRessource[self::DSLAM] . ((isset($tabRessource[self::CHASSIS]) == "") ? '' : "-" . $tabRessource[self::CHASSIS]);
                }
                if (strlen(isset($tabRessource[self::DSLAMSLOT])) > 0) {
                    $t[] = $tabRessource[self::DSLAMSLOT];
                }
                if (strlen(isset($tabRessource[self::DSLAMPORT])) > 0) {
                    $t[] = $tabRessource[self::DSLAMPORT];
                }
            }
        }

        return implode($t, '/');
    }

    /**
     * Affichage de la ressource sur DSLAM.php (accueil), bloc simu impact client
     * @param $astroid
     * @return null|string
     */
    public function afficheDetailMateriel3($astroid)
    {
        $tabRessource = $this->repositoryAstroSqlIhm->getRessourceComplete($astroid);

        if (count($tabRessource) < 2) {
            echo "Erreur : aucune ressource à traiter. ";
            return null;
        }

        // SOPCNX
        if ($tabRessource[self::ID_TYPE_RESSOURCE] == 5 || $tabRessource[self::ID_TYPE_RESSOURCE] == 6) {
            if ($tabRessource[self::VLAN] != "") {
                $t[] = 'VLAN ' . $tabRessource[self::VLAN];
            } else {
                if ($tabRessource[self::VP] != "") {
                    $t[] = "VP " . $tabRessource[self::VP];
                }
            }
        } // SOPLINK
        else {
            if ($tabRessource[self::ID_TYPE_RESSOURCE] == 9) {
                $t[] = $tabRessource[self::DSLAM];
            } else { // Classique, DSLAM, chassis, carte, port...
                if ($tabRessource[self::ID_TYPE_RESSOURCE] == "1") {
                    $t[] = $tabRessource[self::DSLAM];
                } // Si c'est un DSLAM, on n'affiche pas le chassis logique
                else {
                    $t[] = $tabRessource[self::DSLAM] . (($tabRessource[self::CHASSIS] == "") ? '' : "-" . $tabRessource[self::CHASSIS]);
                }
                if (strlen($tabRessource[self::CARTE]) > 0) {
                    $t[] = $tabRessource[self::CARTE];
                }
                if (strlen($tabRessource[self::PORT]) > 0) {
                    $t[] = $tabRessource[self::PORT];
                }
            }
        }
        return implode($t, '/');
    }

    /**
     * Affiche le matériel sous la forum Carte DSLAM DSVEN306 / C10 / 6
     * @param $id_ressource
     * @return string
     */
    public function afficheDetailMaterielAccueil($id_ressource)
    {
        $data = $this->astroRepository->getRessource($id_ressource);

        $result = $data['LB_COURT'] . " " . $data[self::DSLAM];
        if ($data[self::ID_TYPE_RESSOURCE] != "1" && $data[self::CHASSIS] != "") {
            $result .= " / " . $data[self::CHASSIS];
        } // Si c'est un DSLAM, on n'affiche pas le chassis logique
        if ($data[self::ID_TYPE_RESSOURCE] == 5 || $data[self::ID_TYPE_RESSOURCE] == 6) {
            // SOPCNX
            if ($data[self::VP] != "") {
                $result .= " / " . $data[self::VP];
            }
            if ($data[self::VLAN] != "") {
                $result .= " / " . $data[self::VLAN];
            }
        } else {
            if ($data[self::ID_TYPE_RESSOURCE] == 9) {
                // SOPLINK

            } else {
                // DSLAM et autres OLT
                if ($data[self::CARTE] != "") {
                    $result .= " / " . $data[self::CARTE];
                }
                if ($data[self::PORT] != "") {
                    $result .= " / " . $data[self::PORT];
                }
            }
        }
        return $result;
    }

    /**
     *
     * @return array
     */
    public function getMatricePrioGenerique($idJeuParam, $nbTotalClient, $confirmationType, $clientEntreprise = false, $serviceUrgence = false, $isNetVpn = false, $periodeHno = false)
    {
        $arrayPrioriteValues = array();
        $paramsPrioData = $this->repositoryAstroSqlIhm->getConfirmerIncidentListeByChamp($idJeuParam, 'PRIORITE');
        $optionsPrio = key_exists(self::OPTIONS, $paramsPrioData) ? $paramsPrioData[self::OPTIONS] : array();
        $seuil1 = $seuil2 = 0;
        $paramsNatureImpactData = $this->repositoryAstroSqlIhm->getConfirmerIncidentListeByChamp($idJeuParam, 'NATURE_IMPACT_CLIENT');
        $optionsNature = key_exists(self::OPTIONS, $paramsNatureImpactData) ? $paramsNatureImpactData[self::OPTIONS] : array();

        if ($confirmationType == 'TYPE2') {
            foreach ($optionsPrio as $valeur) {
                if ($valeur[self::LIBELLE] == 'priorite') {
                    $prioriteParDefaut = ltrim($valeur[self::IDENTIFIANT], 'P');
                }
            }
            $arrayPrioriteValues['defaut'] = $prioriteParDefaut;
        } else {
            foreach ($optionsNature as $valeurNature) {
                $natureImpactValues[$valeurNature[self::LIBELLE]] = $valeurNature['ID_VALEUR'];
            }
            foreach ($optionsPrio as $valeur) {
                if($periodeHno){
                    if ($valeur[self::LIBELLE] == 'seuil_1') {
                        $seuil1 = $valeur[self::IDENTIFIANT];
                    }
                    if ($valeur[self::LIBELLE] == 'seuil_2') {
                        $seuil2 = $valeur[self::IDENTIFIANT];
                    }
                }else{
                    if ($valeur[self::LIBELLE] == 'seuil_1_ho') {
                        $seuil1 = $valeur[self::IDENTIFIANT];
                    }
                    if ($valeur[self::LIBELLE] == 'seuil_2_ho') {
                        $seuil2 = $valeur[self::IDENTIFIANT];
                    }
                }
                if ($valeur[self::LIBELLE] == 'priorite') {
                    $prioriteParDefaut = ltrim($valeur[self::IDENTIFIANT], 'P');
                }
                if (key_exists($valeur[self::LIBELLE], $natureImpactValues)) {
                    $arrayPrioriteValues[$natureImpactValues[$valeur[self::LIBELLE]]] = ltrim($valeur[self::IDENTIFIANT], 'P');
                }
            }
            if ($clientEntreprise || $serviceUrgence || ($isNetVpn == '1') || ($nbTotalClient >= $seuil1)) {
                $arrayPrioriteValues[$natureImpactValues[self::COUPURE_FRANCHE]] = '1';
            } elseif ($nbTotalClient < $seuil1 && $nbTotalClient >= $seuil2) {
                $arrayPrioriteValues[$natureImpactValues[self::COUPURE_FRANCHE]] = '2';
            } elseif ($nbTotalClient < $seuil2) {
                $arrayPrioriteValues[$natureImpactValues[self::COUPURE_FRANCHE]] = '3';
            }
            $arrayPrioriteValues['defaut'] = $prioriteParDefaut;
        }


        return $arrayPrioriteValues;
    }

    /**
     *
     * @return string
     */
    public function getMatricePrio()
    {
        $tabMatricePriorite = $this->repositoryAstroSqlIhm->getmatricePrioriteImpact();
        $r = '';
        if (count($tabMatricePriorite) > 0) {
            foreach ($tabMatricePriorite as $v) {
                $p = ($v[self::PRIORITY_ID] != '') ? $v[self::PRIORITY_ID] : "";
                $r .= "\tarrMatricePrio['" . $v['ID_MATRICE_PRIO_IMPACT'] . "'] = '$p';\r\n";
            }
        }
        return $r;
    }

    /**
     *
     * @return string
     */
    public function getValeurSeuil()
    {
        $tabValeurSeuil = $this->repositoryAstroSqlIhm->getPrioriteSeuil();
        $r = '';
        if (count($tabValeurSeuil) > 0) {
            foreach ($tabValeurSeuil as $v) {
                $r .= "\tarrValeurSeuil['" . $v['CODE_MATRICE_PRIO_SEUIL'] . "'] = '" . $v['MATRICE_PRIO_SEUIL_VALEUR'] . "';\r\n";
            }
        }
        return $r;
    }

    /**
     * @param $idJeuParam
     * @return array
     */
    public function getMatriceHnoArray($idJeuParam)
    {
        $tagHnoData = $this->repositoryAstroSqlIhm->getConfirmerIncidentListeByChamp($idJeuParam, 'CONFIRMER_SUIVI_HNO');
        $optionsTagHno = key_exists(self::OPTIONS, $tagHnoData) ? $tagHnoData[self::OPTIONS] : array();

        $result = array();
        if (count($optionsTagHno) > 0) {
            foreach ($optionsTagHno as $valeur) {
                $result[$valeur[self::LIBELLE]] = !is_null($valeur[self::IDENTIFIANT]) ? $valeur[self::IDENTIFIANT] : 0;
            }
        }
        return $result;
    }

    /**
     *
     * @return array
     */
    public function getMatricePrioArray()
    {
        $tabMatricePriorite = $this->repositoryAstroSqlIhm->getmatricePrioriteImpact();
        $result = array();
        if (count($tabMatricePriorite) > 0) {
            foreach ($tabMatricePriorite as $v) {
                $result[$v['ID_MATRICE_PRIO_IMPACT']] = is_null($v[self::PRIORITY_ID]) ? '' : $v[self::PRIORITY_ID];
            }
        }
        return $result;
    }

    /**
     *
     * @return array
     */
    public function getValeurSeuilArray()
    {
        $tabValeurSeuil = $this->repositoryAstroSqlIhm->getPrioriteSeuil();
        $result = array();
        if (count($tabValeurSeuil) > 0) {
            foreach ($tabValeurSeuil as $v) {
                $result[$v['CODE_MATRICE_PRIO_SEUIL']] = $v['MATRICE_PRIO_SEUIL_VALEUR'];
            }
        }
        return $result;
    }

    /**
     * Retourne l'attribut onmouseover avec l'appel à la fonction js overlib
     *
     * @param string $msg
     * @param string $opt
     * @return string
     */
    public function ol_tooltip($msg, $opt = null)
    {
        if (trim($msg)) {
            $msg = preg_replace(array("/'/", "/[\r\n]/"), array("\'", '\r'), str_replace("\\", "\\\\", $this->nl2br2($msg)));
            $bopt = 'WRAP,TEXTSIZE,\'11px\',FGCOLOR,\'#F6F6F6\',BGCOLOR,\'#FF6600\',BORDER,1,VAUTO,SHADOW,SHADOWY,3,SHADOWX,3,SHADOWOPACITY,60' . ($opt ? ',' . $opt : '');
            return ' onmouseover="return overlib(\'' . $msg . '\',' . $bopt . ');" onmouseout="return nd();" ';
        }
        return '';
    }

    /**
     * Applique un nl2br2 après remplacement des \r \n et \r\rn par des <br/>
     *
     * @param string $string
     *
     * @return string
     */
    public function nl2br2($string)
    {
        $string = str_replace(array('\r\n', '\r', '\n'), "<br/>", htmlentities($string, ENT_COMPAT | ENT_HTML401, 'ISO-8859-15'));
        return nl2br($string);
    }
}
