# Bruteforce Login

## Vulnérabilité
Le formulaire de connexion n'implémente aucune protection contre les tentatives répétées de connexion, permettant une attaque par force brute.

## Détection
1. Page concernée: `/index.php?page=signin`
2. Formulaire de login simple avec username et password
3. Pas de CAPTCHA ou de limitation de tentatives

## Exploitation

### Résultat
- Username: admin
- Password: shadow

## Comment corriger
1. Implémentation du rate limiting:
```python
def check_rate_limit(ip):
    attempts = redis.get(f"login_attempts:{ip}")
    if attempts > MAX_ATTEMPTS:
        return False
    redis.incr(f"login_attempts:{ip}")
    redis.expire(f"login_attempts:{ip}", WINDOW_SECONDS)
    return True
```

2. Ajout de CAPTCHA après X tentatives échouées
3. Politique de mots de passe forts
4. Délai progressif entre les tentatives
5. Alertes sur les tentatives multiples

## Ressources
- [OWASP Authentication Cheatsheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [NIST Password Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)