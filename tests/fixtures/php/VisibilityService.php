<?php

namespace App\Service;

/**
 * Fixture : mélange de visibilités pour valider le périmètre d'extraction
 * des entry points sur une classe *Service (non-contrôleur).
 */
class VisibilityService
{
    public function __construct($app)
    {
        $this->app = $app;
    }

    public function getPublicOne($id)
    {
        return $this->helperCompute($id);
    }

    public function getPublicTwo()
    {
        return 42;
    }

    private function helperCompute($id)
    {
        if ($id > 0) {
            return $id * 2;
        }
        return 0;
    }

    protected function guardAccess($role)
    {
        return $role === 'admin';
    }

    public static function buildLabel($code)
    {
        return 'LABEL_' . $code;
    }
}
