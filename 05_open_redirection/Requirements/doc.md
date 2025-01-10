# Vulnérabilité de Redirection Ouverte (Open Redirect)

## 1. Description de la Faille
Cette vulnérabilité permet de rediriger les utilisateurs vers des sites arbitraires en modifiant le paramètre `site` dans l'URL. C'est une faille classique de type Open Redirect qui peut être utilisée pour des attaques de phishing.

## 2. Localisation
- En bas de chaque page du site
- Dans les liens de réseaux sociaux
- URL vulnérable : `index.php?page=redirect&site=facebook`

## 3. Exploitation

### Étape 1 : Identifier les URLs originales
```
http://{IP}/index.php?page=redirect&site=facebook
http://{IP}/index.php?page=redirect&site=twitter
http://{IP}/index.php?page=redirect&site=instagram
```

### Étape 2 : Modifier le paramètre site
Changer :
```
index.php?page=redirect&site=facebook
```
En :
```
index.php?page=redirect&site=https://profile.intra.42.fr/
```

## 4. Impact de la Faille
1. Phishing :
   - Redirection vers des sites malveillants
   - Vol d'identifiants
   - Infection par malware

2. Atteintes à la réputation :
   - Utilisation de la confiance des utilisateurs
   - Association du domaine légitime avec des attaques

## 5. Comment Corriger

### Solution en PHP
```php
class RedirectManager {
    private $allowedSites = [
        'facebook' => 'https://facebook.com',
        'twitter' => 'https://twitter.com',
        'instagram' => 'https://instagram.com'
    ];
    
    public function safeRedirect($site) {
        // Vérification si le site est dans la liste autorisée
        if (!array_key_exists($site, $this->allowedSites)) {
            throw new SecurityException('Site non autorisé');
        }
        
        // Redirection vers l'URL sécurisée
        header('Location: ' . $this->allowedSites[$site]);
        exit();
    }
}

// Utilisation
$redirect = new RedirectManager();
$redirect->safeRedirect($_GET['site']);
```

### Version avec Whitelist Simple
```php
function secureRedirect($site) {
    $allowed = ['facebook', 'twitter', 'instagram'];
    
    if (!in_array($site, $allowed)) {
        header('Location: /');
        exit();
    }
    
    $urls = [
        'facebook' => 'https://facebook.com',
        'twitter' => 'https://twitter.com',
        'instagram' => 'https://instagram.com'
    ];
    
    header('Location: ' . $urls[$site]);
    exit();
}
```

## 6. Bonnes Pratiques

1. Validation Stricte :
   - Utiliser une whitelist
   - Valider les URLs
   - Pas de redirections dynamiques

2. Implémentation :
   - Gérer les URLs en backend
   - Utiliser des identifiants courts
   - Éviter les URLs en paramètres

3. Sécurité Additionnelle :
   - Page de confirmation
   - Logging des redirections
   - Notifications des redirections suspectes

## 7. Documentation

### Pattern de Redirection Sécurisée
```plaintext
1. Requête de redirection →
2. Vérification whitelist →
3. Mapping vers URL réelle →
4. Redirection sécurisée
```

### Exemples de Configuration Serveur
```apache
# Apache - Protection supplémentaire
RewriteEngine On
RewriteCond %{QUERY_STRING} site=(?!facebook|twitter|instagram).+ [NC]
RewriteRule ^ - [F]
```

## 8. Ressources
- OWASP Unvalidated Redirects
- CWE-601: URL Redirection to Untrusted Site
- Prevention Cheat Sheet

Tu peux exploiter cette faille en modifiant simplement le paramètre "site" dans l'URL pour rediriger vers n'importe quel site. Pour le projet, essaie de rediriger vers `https://profile.intra.42.fr/` pour obtenir le flag.