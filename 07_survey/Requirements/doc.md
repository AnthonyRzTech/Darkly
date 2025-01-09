# Vulnérabilité de Validation des Données de Formulaire

## 1. Description de la Faille
Cette vulnérabilité permet de manipuler le système de vote en modifiant les valeurs possibles dans le formulaire HTML, permettant d'attribuer un score arbitraire au lieu des valeurs limitées entre 1 et 10.

## 2. Localisation
- Page : Survey
- Composant : Formulaire de vote
- Type de vulnérabilité : Manipulation de données côté client

## 3. Exploitation

### Étape 1 : Code Original
```html
<form action="#" method="post">
    <input type="hidden" name="sujet" value="2">
    <select name="valeur" onchange="javascript:this.form.submit();">
        <option value="1">1</option>
        <!-- ... autres options ... -->
        <option value="10">10</option>
    </select>
</form>
```

### Étape 2 : Modification pour Exploitation
1. Ouvrir les outils développeur (F12)
2. Localiser l'élément select
3. Ajouter ou modifier une option :
```html
<option value="651665195">10</option>
```

## 4. Impact de la Faille
1. Manipulation des scores :
   - Scores irréalistes
   - Fausser les résultats
   - Compromettre l'intégrité du vote

2. Conséquences :
   - Résultats non fiables
   - Perte de confiance
   - Système de vote compromis

## 5. Comment Corriger

### Solution en PHP
```php
class VoteManager {
    private const MIN_SCORE = 1;
    private const MAX_SCORE = 10;
    
    public function processVote($userId, $candidateId, $score) {
        // Validation du score
        if (!$this->isValidScore($score)) {
            throw new InvalidVoteException('Score invalide');
        }
        
        // Validation du candidat
        if (!$this->isValidCandidate($candidateId)) {
            throw new InvalidVoteException('Candidat invalide');
        }
        
        // Enregistrement du vote
        return $this->saveVote($userId, $candidateId, $score);
    }
    
    private function isValidScore($score) {
        return is_numeric($score) && 
               $score >= self::MIN_SCORE && 
               $score <= self::MAX_SCORE;
    }
    
    private function saveVote($userId, $candidateId, $score) {
        $score = (int)$score; // Cast explicite
        // Code de sauvegarde en base de données
    }
}
```

### Version Simple
```php
// Validation basique
function validateVote($score) {
    $score = filter_var($score, FILTER_VALIDATE_INT);
    if ($score === false || $score < 1 || $score > 10) {
        die('Vote invalide');
    }
    return $score;
}

// Utilisation
$score = validateVote($_POST['valeur']);
```

## 6. Bonnes Pratiques

### Validation des Données
1. Toujours valider côté serveur
2. Utiliser des types stricts
3. Définir des limites claires
4. Nettoyer les entrées

### Sécurisation du Formulaire
```php
// Template sécurisé
<select name="valeur" onchange="this.form.submit();">
    <?php
    for ($i = 1; $i <= 10; $i++) {
        echo "<option value=\"" . htmlspecialchars($i) . "\">" . htmlspecialchars($i) . "</option>";
    }
    ?>
</select>
```

## 7. Protection Additionnelle

### Validation JavaScript (couche supplémentaire)
```javascript
document.querySelector('form').addEventListener('submit', function(e) {
    const value = parseInt(this.valeur.value);
    if (isNaN(value) || value < 1 || value > 10) {
        e.preventDefault();
        alert('Score invalide');
    }
});
```

### Protection Base de Données
```sql
CREATE TABLE votes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    candidate_id INT NOT NULL,
    score INT CHECK (score >= 1 AND score <= 10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 8. Ressources
- OWASP Input Validation Cheat Sheet
- CWE-20: Improper Input Validation
- Form Validation Best Practices