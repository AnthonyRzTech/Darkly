# Sécurisation contre les attaques Directory Traversal

## Description de la vulnérabilité

Une vulnérabilité de type Directory Traversal (ou Path Traversal) a été identifiée sur le site. Cette faille de sécurité permet à un attaquant d'accéder à des fichiers système sensibles en manipulant les paramètres de l'URL.

## Analyse technique

Dans ce cas précis, la vulnérabilité permet d'accéder au fichier `/etc/passwd` en exploitant le paramètre `page` de l'URL. Le chemin d'exploitation est le suivant :

```
http://[IP]/?page=../../../../../../../etc/passwd
```

L'utilisation répétée de `../` permet de remonter dans l'arborescence du système de fichiers jusqu'à atteindre la racine, puis d'accéder au fichier `/etc/passwd`. Ce fichier est particulièrement sensible car il contient les informations sur les comptes utilisateurs du système.

## Impact sur la sécurité

Cette vulnérabilité présente plusieurs risques majeurs :
- Accès non autorisé aux fichiers système sensibles
- Divulgation d'informations sur les utilisateurs du système
- Possibilité d'exploitation pour une élévation de privilèges
- Compromission potentielle de la confidentialité du système

## Mesures de remédiation

Pour sécuriser l'application contre les attaques Directory Traversal, il est recommandé de :

1. Implémenter une validation stricte des entrées utilisateur en :
   - Filtrant les caractères spéciaux comme "../"
   - Validant le format des chemins de fichiers
   - Utilisant des expressions régulières pour valider les entrées

2. Configurer correctement le serveur web :
   - Restreindre l'accès aux répertoires sensibles
   - Appliquer le principe du moindre privilège
   - Utiliser des listes blanches pour les fichiers accessibles

3. Mettre en place des contrôles d'accès :
   - Implémenter une authentification robuste
   - Définir des permissions précises sur les fichiers
   - Limiter les droits du serveur web

En appliquant ces mesures, vous réduirez significativement le risque d'exploitation de cette vulnérabilité.