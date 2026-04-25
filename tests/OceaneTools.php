<?php

namespace App\Tools;

/**
 * Class OceaneAssistant
 * Classe Assistant Itération
 *
 * @version 1.0
 * @package
 *
 */
class OceaneTools
{

    /**
     * Cherche une valeur dans un tableau d'objets par id
     *
     * @param string $id
     * @param array $objets
     * @return string
     */

    public static function searchValueInFindAndGet($id, $objets)
    {
        $valeur = null;
        if (is_array($objets) && count($objets) > 0) {
            foreach ($objets as $objet) {
                if (key_exists('id', $objet) && $objet->id == $id && key_exists('value', $objet)) {
                    $valeur = $objet->value;
                }
            }
        } else {
            if (key_exists('id', $objets) && $objets->id == $id && key_exists('value', $objets)) {
                $valeur = $objets->value;
            }
        }

        return $valeur;
    }

    /**
     * Valider une variable (non vide)
     *
     * @param string $variable
     * @return boolean
     */
    public static function isValidVariable($variable)
    {
        return ($variable !== '' && !is_null($variable));
    }

    /**
     * Supprimer les espaces
     *
     * @param string $str
     * @return string
     */
    public static function supprEspacesSurnumeraires($str)
    {
        $str = preg_replace('# +#', ' ', $str);
        $rep = array(
            " /",
            "/ "
        );
        $str = str_replace($rep, "/", $str);
        return $str;
    }

    /**
     * Retourne la liste des Variables entre ### ###
     *
     * @param string $str
     * @param string $startDelimiter
     * @param string $endDelimiter
     * @return array
     */
    public static function getContents($str, $startDelimiter, $endDelimiter)
    {
        $contents = array();
        $startDelimiterLength = strlen($startDelimiter);
        $endDelimiterLength = strlen($endDelimiter);
        $startFrom = $contentStart = $contentEnd = 0;
        while (false !== ($contentStart = strpos($str, $startDelimiter, $startFrom))) {
            $contentStart += $startDelimiterLength;
            $contentEnd = strpos($str, $endDelimiter, $contentStart);
            if (false === $contentEnd) {
                break;
            }
            $contents[] = substr($str, $contentStart, $contentEnd - $contentStart);
            $startFrom = $contentEnd + $endDelimiterLength;
        }

        return $contents;
    }

    /**
     *
     * @param string $format
     * @param \DateTime|string $dateUTC
     * @return \DateTime
     */
    public static function changeUTCToDate($format, $dateUTC)
    {
        $utc_ts = strtotime($dateUTC . " UTC");
        return date($format, $utc_ts);
    }

    public static function cleanTextDescription($txt)
    {
        $txt = str_replace('<br />', chr(13), $txt);
        return $txt;
    }

    /**
     * remplacer les retours à la ligne
     *
     * @param string $text
     * @return string
     */
    public static function cleanText($text)
    {
        $text = str_replace(chr(13), '&lt;br /&gt;', $text);
        return $text;
    }

    /**
     * Demande commets
     * @param string $description
     * @param string $commentaire
     * @return mixed
     */

    public static function cleanCommets($description, $commentaire)
    {
        $commentaire = '# DEBUT_COMMENTAIRE #' . chr(13) . chr(13) . $commentaire . chr(13) . '# FIN_COMMENTAIRE #';
        preg_match('/# DEBUT_COMMENTAIRE #(.*?)# FIN_COMMENTAIRE #/s', $description, $matches);
        if (count($matches)) {
            $description = str_replace($matches[0], $commentaire, $description);
        } else {
            preg_match('/# DEBUT_COMMENTAIRE #.*/', $description, $debutMatches);
            if (count($debutMatches)) {
                $description = str_replace($debutMatches[0], $commentaire, $description);
            } else {
                $description = $description . chr(13) . $commentaire . chr(13);
            }
        }
        return str_replace(chr(13), '<br />', $description);
    }

    /**
     * Convertir objet à un array
     * @param object $oObj
     * @return array[]
     */
    public static function objectToArray($oObj)
    {
        $aTab = array();
        if ((is_object($oObj) || is_array($oObj)) && !empty($oObj)) {
            foreach ($oObj as $xKey => $xVal) {
                if (is_object($xVal) || is_array($xVal)) {
                    $aTab[strtoupper($xKey)] = self::objectToArray($xVal);
                } else {
                    $aTab[strtoupper($xKey)] = $xVal;
                }
            }
        }
        return $aTab;
    }
}