# Système de Gestion de Tickets

## Description

Ce projet est une application web développée avec Flask permettant la gestion de tickets de support. Les utilisateurs peuvent créer, modifier et suivre leurs tickets, tandis que les administrateurs disposent de fonctionnalités avancées de gestion et de suivi.

---

## Fonctionnalités

- **Authentification** : Inscription, connexion, déconnexion
- **Gestion des tickets** : Création, modification, suppression, changement de statut
- **Priorisation automatique** : Détection automatique de la priorité selon la description du ticket
- **Historique** : Archivage des tickets résolus
- **Calendrier** : Vue calendrier des tickets pour les administrateurs
- **Notifications par email** : Envoi d’un email lors de la résolution d’un ticket
- **Gestion des rôles** : Utilisateur standard et administrateur

---

## Installation

### Prérequis

- Python 3.x
- MySQL
- Un serveur SMTP (Gmail recommandé)
- Les modules Python listés dans `requirements.txt`

### Étapes

1. **Cloner le dépôt**
2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt

3. Créer la base de données MySQL Crée une base nommée ticket et configure l’accès dans app.py ou via une variable d’environnement.
4. Configurer les variables d’environnement Crée un fichier .env à la racine du projet :
   
   
   MAIL_USERNAME=ton_email@gmail.com
   
   MAIL_PASSWORD=ton_mot_de_passe_app
   
   MAIL_DEFAULT_SENDER=ton_email@gmail.com
   
5. Lancer l’application Accède à http://localhost:5000
## Structure du projet
- app.py : Application principale Flask
- connection.py : Configuration de la connexion mail
- templates/ : Fichiers HTML (interfaces)
- static/ : Fichiers statiques (CSS, JS)
- .env : Variables d’environnement (non versionné)
- .gitignore : Fichiers/dossiers à ignorer par Git
## Sécurité
- Les mots de passe sont hashés avec Werkzeug.
- Les informations sensibles (mots de passe, clés) doivent être stockées dans .env et jamais versionnées.
- Les routes sont protégées selon le rôle de l’utilisateur.
## Premier lancement
Lors du premier lancement, l’application redirige automatiquement vers /setup pour créer le compte administrateur.

## Contribution
1. Fork le projet
2. Crée une branche pour ta fonctionnalité
3. Propose une Pull Request
## Avertissement
Ne jamais versionner de fichiers sensibles ( .env , clés privées, etc.) Si une clé privée ou un mot de passe a été exposé, change-le immédiatement.