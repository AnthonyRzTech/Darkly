# Vulnérabilité de Cookie d'Administration

## 1. Description de la Faille
Cette vulnérabilité permet d'obtenir des droits d'administration en modifiant simplement un cookie dont la valeur est un hash MD5 facilement déchiffrable.

## 2. Localisation
- Cookie visible dans la console du navigateur
- Nom du cookie : `I_am_admin`
- Valeur initiale (MD5) : `68934a3e9455fa72420237eb05902327` (= "false")

## 3. Exploitation

### Étape 1 : Observer le Cookie Initial
1. Ouvrir la console du navigateur (F12)
2. Exécuter :
```javascript
document.cookie
```
Output attendu : `"I_am_admin=68934a3e9455fa72420237eb05902327"`

### Étape 2 : Analyser le Hash
- Hash MD5 original : `68934a3e9455fa72420237eb05902327`
- Valeur décodée : `"false"`
- Hash MD5 de "true" : `b326b5062b2f0e69046810717534cb09`

### Étape 3 : Modifier le Cookie
Exécuter dans la console :
```javascript
document.cookie = "I_am_admin=b326b5062b2f0e69046810717534cb09"
```

## 4. Impact de la Faille
1. Accès non autorisé :
   - Élévation de privilèges
   - Accès à des fonctionnalités admin
   - Contournement de sécurité

2. Risques :
   - Modification de données
   - Vol d'informations
   - Compromission du système

## 5. Comment Corriger

### Solution en PHP avec Sessions
```php
<?php
class AdminAuth {
    public function __construct() {
        session_start();
    }
    
    public function login($username, $password) {
        // Vérification en base de données
        $user = $this->verifyCredentials($username, $password);
        
        if ($user && $user['is_admin']) {
            $_SESSION['admin_id'] = $user['id'];
            $_SESSION['admin_token'] = $this->generateSecureToken();
            return true;
        }
        return false;
    }
    
    public function isAdmin() {
        return isset($_SESSION['admin_id']) && 
               $this->validateAdminToken($_SESSION['admin_token']);
    }
    
    private function generateSecureToken() {
        return bin2hex(random_bytes(32));
    }
}
```

### Solution avec JWT
```php
<?php
class SecureAdminAuth {
    private $secret_key = 'votre_clé_secrète_très_longue';
    
    public function createAdminToken($user_id) {
        $payload = [
            'user_id' => $user_id,
            'is_admin' => true,
            'exp' => time() + 3600,
            'jti' => bin2hex(random_bytes(16))
        ];
        
        return JWT::encode($payload, $this->secret_key, 'HS256');
    }
    
    public function verifyAdmin($token) {
        try {
            $decoded = JWT::decode($token, $this->secret_key, ['HS256']);
            return $decoded->is_admin === true;
        } catch (Exception $e) {
            return false;
        }
    }
}
```

## 6. Bonnes Pratiques

### Authentification
1. Utiliser des sessions côté serveur
2. Implémenter des tokens JWT
3. Ne jamais stocker de données sensibles dans les cookies
4. Utiliser des tokens d'authentification sécurisés

### Sécurité des Cookies
1. Flags de sécurité :
```php
session_set_cookie_params([
    'secure' => true,
    'httponly' => true,
    'samesite' => 'Strict'
]);
```

2. Configuration Apache :
```apache
Header always set Set-Cookie HttpOnly;Secure
```

## 7. Pour le CTF
Valeurs MD5 importantes :
```
"false" = 68934a3e9455fa72420237eb05902327
"true"  = b326b5062b2f0e69046810717534cb09
```

Commande pour obtenir le flag :
```javascript
document.cookie = "I_am_admin=b326b5062b2f0e69046810717534cb09"
```
refresh

## 8. Ressources Additionnelles
- OWASP Session Management Cheat Sheet
- OWASP Authentication Cheat Sheet
- JWT Best Practices
- Secure Cookie Handling Guidelines

## 9. Points Clés à Retenir
1. Ne jamais utiliser de cookies pour l'authentification admin
2. Toujours gérer les permissions côté serveur
3. Utiliser des mécanismes d'authentification robustes
4. Mettre en place des sessions sécurisées