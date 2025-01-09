# Faille de Sécurité sur la Récupération de Mot de Passe

## 1. Description de la Faille
Cette vulnérabilité permet de rediriger le mail de récupération de mot de passe vers une adresse arbitraire en modifiant une valeur dans le formulaire HTML.

## 2. Localisation
- Chemin : `/?page=recover`
- Page : "Forgot Password"
- Composant : Formulaire de récupération de mot de passe

## 3. Exploitation

### Étape 1 : Accès à la page
1. Aller sur la page d'accueil
2. Cliquer sur "Sign in"
3. Cliquer sur "I forgot my password"

### Étape 2 : Analyse du Code Source
```html
<form action="#" method="POST">
    <input type="hidden" name="mail" value="webmaster@borntosec.com" maxlength="15">
    <input type="submit" name="Submit" value="Submit">
</form>
```

### Étape 3 : Exploitation
1. Inspecter l'élément (F12)
2. Localiser l'input hidden
3. Modifier la valeur de l'attribut `value` ex : webmaster@borntosec.com par hacker@evil.com
4. Cliquer sur "Submit"

## 4. Impact de la Faille
1. Détournement des emails de récupération
2. Possibilité de réinitialiser les mots de passe d'autres utilisateurs
3. Compromission des comptes utilisateurs
4. Vol d'informations sensibles

## 5. Comment Corriger

### Solution Backend (PHP)
```php
<?php
class PasswordRecovery {
    private $allowedEmails = [
        'webmaster@borntosec.com'
    ];
    
    public function handleRecovery() {
        // Token de sécurité unique par session
        if (!isset($_SESSION['csrf_token']) || $_POST['csrf_token'] !== $_SESSION['csrf_token']) {
            throw new SecurityException('Invalid token');
        }
        
        // Vérification de l'email en base de données
        $userEmail = $this->getUserEmailFromDatabase($_SESSION['user_id']);
        
        if (!$userEmail || !in_array($userEmail, $this->allowedEmails)) {
            throw new SecurityException('Unauthorized email');
        }
        
        // Génération d'un token unique à durée limitée
        $recoveryToken = $this->generateSecureToken();
        
        // Envoi du mail avec le token
        $this->sendRecoveryEmail($userEmail, $recoveryToken);
    }
}
```

### Template Sécurisé (HTML)
```html
<form action="/recover.php" method="POST">
    <!-- Email géré côté serveur -->
    <input type="hidden" name="csrf_token" value="<?php echo $_SESSION['csrf_token']; ?>">
    <input type="submit" name="Submit" value="Submit">
</form>
```

## 6. Bonnes Pratiques

### Côté Serveur
1. Ne jamais faire confiance aux données client
2. Stocker les emails en base de données
3. Implémenter un système de tokens CSRF
4. Limiter les tentatives de récupération
5. Utiliser des tokens à usage unique
6. Mettre en place des délais d'expiration

### Sécurité Générale
1. Logging des tentatives de récupération
2. Notifications de sécurité
3. Vérification en deux étapes
4. Validation des adresses email
5. Rate limiting

## 7. Documentation Technique

### Architecture Sécurisée
```plaintext
1. Utilisateur demande récupération → 
2. Serveur vérifie session → 
3. Génère token unique → 
4. Envoie email sécurisé → 
5. Vérifie token lors de la réinitialisation
```

### Points de Contrôle
- Validation de session
- Vérification d'identité
- Protection contre le brute force
- Logs de sécurité
- Monitoring des tentatives suspectes

## 8. Ressources Additionnelles
- OWASP Password Reset Guidelines
- CWE-640: Weak Password Recovery
- NIST Digital Identity Guidelines