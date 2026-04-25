<?php

/**
 * Helper
 *
 * @author alaaroua
 */
namespace App\Helper;

use App\Repository\LienRepository;

class Lien
{

    /**
     *
     * @var LienRepository
     */
    protected $lienRepository;

    public function __construct($app)
    {
        $this->lienRepository = $app->get('LienRepository');
    }

    /**
     * Retourner la liste des categories
     *
     * @return array
     */
    public function getCategoriesList($bandeau)
    {
        $result = array();
        $categories = $this->lienRepository->getAllCategories($bandeau);
        $result['1'] = $this->searchForCategory('1', $categories);
        $result['2'] = $this->searchForCategory('2', $categories);
        $result['3'] = $this->searchForCategory('3', $categories);
        $result['4'] = $this->searchForCategory('4', $categories);
        return $result;
    }

    /**
     * Chercher une categorie par numero de colonne
     *
     * @param string $categorie
     * @param array $categories
     * @return array|NULL
     */
    private function searchForCategory($categorie, $categories)
    {
        foreach ($categories as $key => $val) {
            if ($val['COLONNE'] === $categorie) {
                return $val;
            }
        }
        return null;
    }

    /**
     * Modifier les categories
     *
     * @param array $data
     */
    public function updateCategories($data)
    {
        $result = $this->lienRepository->updateCategories($data);
        return $result;
    }

    /**
     * Retourner la liste des bouton par bandeau
     *
     * @param string $bandeau
     * @return array
     */
    public function getButtonsListByBandeau($bandeau)
    {
        $buttons = $this->lienRepository->getButtonsByBandeau($bandeau);
        return $buttons;
    }

    /**
     * Génèrer les options des catégories
     *
     * @return string[]
     */
    public function getCategoryOptions()
    {
        $result = array(
            0 => '* ' . __('category_text') . ' *'
        );
        for ($i = 1; $i <= 4; $i ++) {
            $result[$i] = __('category_text') . ' ' . $i;
        }
        return $result;
    }

    /**
     * Génèrer les options des ordres
     *
     * @return string[]
     */
    public function getOrderOptions()
    {
        $result = array(
            0 => '* ' . __('emplacement_text') . ' *'
        );
        for ($i = 1; $i <= 10; $i ++) {
            $result[$i] = __('emplacement_text') . ' ' . $i;
        }
        return $result;
    }

    /**
     * Génèrer les options des priorités
     *
     * @return string[]
     */
    public function getPriorityOptions()
    {
        $result = array(
            0 => '* ' . __('priority_text') . ' *'
        );
        for ($i = 1; $i <= 10; $i ++) {
            $result[$i] = __('priority_text') . ' ' . $i;
        }
        return $result;
    }

    /**
     * Retourner les informations d'un bouton
     *
     * @param int $id
     * @return array
     */
    public function getInfosButton($id)
    {
        $infosBtn = array();
        $infosBtn['button'] = $this->lienRepository->getButtonsById($id);
        $infosBtn['links'] = $this->lienRepository->getLinksByButtonId($id);
       // $infosBtn['ressources'] = $this->lienRepository->getRessourcesByButtonId($id);
        return $infosBtn;
    }

    /**
     * Créer un bouton
     *
     * @param array $data
     * @return boolean
     */
    public function createButton($data)
    {
        $result = $this->lienRepository->insertButton($data);
        return $result;
    }

    /**
     * Modifier un bouton
     *
     * @param array $data
     * @return boolean
     */
    public function updateButton($data)
    {
        $result = $this->lienRepository->updateButton($data);
        return $result;
    }

    /**
     * Supprimer un bouton
     *
     * @param int $buttonId
     * @return boolean
     */
    public function deleteButton($buttonId)
    {
        $result = $this->lienRepository->deleteButton($buttonId);
        return $result;
    }

    /**
     * Retourner les options des variables
     *
     * @return array
     */
    public function getVariablesOptions()
    {
        $result = array();
        $variablelist = $this->lienRepository->getListeVariables();
        array_push($result, __('_var_'));
        
        $uniqueTypes = array_unique(array_map(function ($i) {
            return $i['TYPE'];
        }, $variablelist));
        foreach ($uniqueTypes as $type) {
            $result[$type]['label'] = $type;
            $result[$type]['options'] = array();
            foreach ($variablelist as $variable) {
                if ($type === $variable['TYPE']) {
                    $nom = $variable['NOM'];
                    $result[$type]['options'][$nom] = $nom;
                }
            }
        }
        return $result;
    }

    /**
     * Retourner les informations d'un lien
     *
     * @param int $id
     * @return boolean
     */
    public function getInfosLink($id)
    {
        $infosLink = $this->lienRepository->getLinkById($id);
        return $infosLink;
    }

    /**
     * Créer un lien
     *
     * @param array $data
     * @return boolean
     */
    public function createLink($data)
    {
        $result = $this->lienRepository->insertLink($data);
        return $result;
    }

    /**
     * Modifier un lien
     *
     * @param array $data
     * @return boolean
     */
    public function updateLink($data)
    {
        $result = $this->lienRepository->updateLink($data);
        return $result;
    }

    /**
     * Supprimer un lien
     *
     * @param int $linkId
     * @return boolean
     */
    public function deleteLink($linkId)
    {
        $result = $this->lienRepository->deleteLink($linkId);
        return $result;
    }
}

