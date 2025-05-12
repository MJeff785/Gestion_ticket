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