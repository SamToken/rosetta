<?php
/**
 * Contrôleur de gestion des utilisateurs
 * Code legacy typique Zend Framework 1
 */

class ContractController extends Zend_Controller_Action
{
    protected $_userModel;
    protected $_authService;
    
    public function init()
    {
        $this->_userModel = new Application_Model_User();
        $this->_authService = $this->getInvokeArg('bootstrap')->getResource('auth');
    }
    
    /**
     * Liste des utilisateurs
     */
    public function indexAction()
    {
        $page = $this->_getParam('page', 1);
        $limit = $this->_getParam('limit', 20);
        
        $db = Zend_Db_Table::getDefaultAdapter();
        $users = $db->fetchAll("SELECT * FROM users WHERE status = 'active' ORDER BY created_at DESC");
        
        $this->view->users = $users;
        $this->view->currentPage = $page;
    }
    
    /**
     * Édition d'un utilisateur
     */
    public function editAction()
    {
        $id = $this->_getParam('id');
        
        if (!$id) {
            $this->_redirect('/user/index');
            return;
        }
        
        // Vérifier les permissions
        if ($_SESSION['user']['role'] != 'admin') {
            $this->_redirect('/error/forbidden');
            return;
        }
        
        $db = Zend_Db_Table::getDefaultAdapter();
        $user = $db->fetchRow("SELECT * FROM users WHERE id = ?", array($id));
        
        if ($this->getRequest()->isPost()) {
            $email = $_POST['email'];
            $name = $_POST['name'];
            $role = $_POST['role'];
            
            // Validation basique
            if (empty($email) || empty($name)) {
                $this->view->error = "Tous les champs sont obligatoires";
            } else {
                $db->update('users', array(
                    'email' => $email,
                    'name' => $name,
                    'role' => $role,
                    'updated_at' => date('Y-m-d H:i:s')
                ), "id = " . (int)$id);
                
                $this->_helper->flashMessenger('Utilisateur mis à jour');
                $this->_redirect('/user/index');
                return;
            }
        }
        
        $this->view->user = $user;
        $this->render('edit');
    }
    
    /**
     * Suppression d'un utilisateur
     */
    public function deleteAction()
    {
        $id = $this->_getParam('id');
        
        if ($_SESSION['user']['role'] != 'admin') {
            $this->_redirect('/error/forbidden');
            return;
        }
        
        if ($id) {
            $db = Zend_Db_Table::getDefaultAdapter();
            $db->delete('users', 'id = ' . (int)$id);
        }
        
        $this->_redirect('/user/index');
    }
    
    /**
     * Création d'un utilisateur
     */
    public function createAction()
    {
        if ($this->getRequest()->isPost()) {
            $email = $_POST['email'];
            $name = $_POST['name'];
            $password = $_POST['password'];
            
            // Vérifier si l'email existe déjà
            $db = Zend_Db_Table::getDefaultAdapter();
            $existing = $db->fetchRow("SELECT id FROM users WHERE email = ?", array($email));
            
            if ($existing) {
                $this->view->error = "Cet email est déjà utilisé";
            } else {
                $db->insert('users', array(
                    'email' => $email,
                    'name' => $name,
                    'password' => md5($password),
                    'role' => 'user',
                    'status' => 'active',
                    'created_at' => date('Y-m-d H:i:s')
                ));
                
                // Envoyer email de bienvenue
                $mail = new Zend_Mail();
                $mail->setBodyText("Bienvenue $name !");
                $mail->setFrom('noreply@example.com');
                $mail->addTo($email);
                $mail->setSubject('Bienvenue');
                $mail->send();
                
                $this->_redirect('/user/index');
                return;
            }
        }
        
        $this->render('create');
    }
}
