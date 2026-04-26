<?php
namespace App\Service;

use Zend\Validator\NotEmpty;
use Zend\Validator\Digits;
use Zend\Validator\Date;
use Zend\Validator\Regex;
use Zend\I18n\Validator\IsInt;

class ValidationService
{
    /**
     * 
     * @param string $value
     * @return boolean
     */
    public function notEmpty($value)
    {
        $validator = new NotEmpty();
        return $validator->isValid($value);
    }
    
    /**
     * 
     * @param int $value
     * @return boolean
     */
    public function isDigit($value)
    {
        $validator = new Digits();
        return $validator->isValid($value);
    }
    
    /**
     * 
     * @param string $date
     * @param string $format
     * @return boolean
     */
    public function isDate($date, $format = 'd/m/Y H:i:s')
    {
        $validator = new Date(array('format' => $format));
        return $validator->isValid($date);
    }
    
    /**
     * 
     * @param string $value
     * @param string $pattern
     * @return boolean
     */
    public function matchRegex($value, $pattern)
    {
        $validator = new Regex(array('pattern' => $pattern));
        return $validator->isValid($value);
    }
    
    public function isInt($value)
    {
        $validator = new IsInt();
        return $validator->isValid($value);
    }

    /**
     *
     * @param array $regles
     * @return array
     */
    public function formatRegles(array $regles)
    {
        $result = array();
        foreach ($regles as $value) {
            $result[$value['CODE']] = $value['OBLIGATOIRE'];
        }
        return $result;
    }
}

