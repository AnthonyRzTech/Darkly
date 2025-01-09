# Analyse de la vulnérabilité de falsification des en-têtes HTTP

## Contexte
Cette vulnérabilité se trouve sur la page accessible via le lien "Born2Sec" qui mène vers une URL contenant un hash SHA-256. La page contient des commentaires HTML révélant des conditions d'accès spécifiques.

## Conditions requises
Pour accéder au contenu protégé, deux paramètres HTTP doivent être modifiés :
1. Le Referer doit provenir de "https://www.nsa.gov/"
2. Le User-Agent doit être "ft_bornToSec"

## Solution technique
La commande curl suivante permet d'exploiter cette vulnérabilité :

```bash
curl -e https://www.nsa.gov/ -A "ft_bornToSec" "http://192.168.56.102/?page=b7e44c7a40c5f80139f0a50f3650fb2bd8d00b0d24667c4c2ca32c88e13b758f"
```

Où :
- `-e` définit l'en-tête Referer
- `-A` définit l'en-tête User-Agent

## Explication de la vulnérabilité
Cette faille repose sur une validation insuffisante des en-têtes HTTP. Le système fait confiance aux informations envoyées par le client, qui peuvent être facilement falsifiées. Ce type de protection est inefficace car :
- Les en-têtes HTTP peuvent être modifiés par n'importe quel client
- Il n'y a pas de vérification cryptographique de l'authenticité de la requête
- Aucune session utilisateur n'est requise

## Recommandations de sécurité
Pour sécuriser ce type d'accès, il faudrait :
1. Implémenter une authentification robuste
2. Utiliser des jetons JWT ou des sessions sécurisées
3. Ne pas se fier uniquement aux en-têtes HTTP pour la sécurité
4. Mettre en place un système de contrôle d'accès basé sur les rôles (RBAC)

Cette vulnérabilité souligne l'importance de ne jamais faire confiance aux données envoyées par le client sans validation appropriée.