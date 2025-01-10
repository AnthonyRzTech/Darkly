# Tutoriel - Scraping de Fichiers Cachés

## 1. Description du Challenge
Ce challenge implique la recherche d'un flag parmi de nombreux fichiers README cachés dans différents répertoires imbriqués à l'adresse `http://{IP}/.hidden/`.

## 2. Comment ça marche

### Composants du Script :

1. **Imports nécessaires :**
```python
import requests        # Pour les requêtes HTTP
from bs4 import BeautifulSoup  # Pour parser le HTML
```

## 4. Comment Utiliser le Script

1. Installation des dépendances :
```bash
pip install requests beautifulsoup4
```

2. Exécution :
```bash
python scrapping.py
```

## 5. Comment Éviter Cette Vulnérabilité

### Solution en PHP
```php
class SecureFileManager {
    private $root_dir = '/var/www/files/';
    
    public function listFiles($directory = '') {
        // Validation du chemin
        $path = realpath($this->root_dir . $directory);
        
        if (!$path || strpos($path, $this->root_dir) !== 0) {
            throw new SecurityException('Accès non autorisé');
        }
        
        // Lister uniquement les fichiers autorisés
        return array_filter(scandir($path), function($file) {
            return !in_array($file, ['.', '..', '.hidden']);
        });
    }
}
```

### Protection avec .htaccess
```apache
# Interdire l'accès aux répertoires cachés
<FilesMatch "^\.">
    Order allow,deny
    Deny from all
</FilesMatch>

# Désactiver le listing des répertoires
Options -Indexes
```

## 6. Bonnes Pratiques

1. **Sécurité des Fichiers :**
   - Ne pas stocker de données sensibles dans des répertoires web
   - Utiliser des systèmes de stockage sécurisés
   - Implémenter une authentification forte

2. **Configuration Serveur :**
   - Désactiver le listing des répertoires
   - Restreindre l'accès aux fichiers sensibles
   - Utiliser des permissions appropriées

3. **Gestion des Données :**
   - Stocker les données sensibles en base de données
   - Chiffrer les informations critiques
   - Implémenter des logs d'accès

## 7. Ressources
- OWASP Directory Traversal
- Web Scraping Best Practices
- Apache Security Configuration Guide
