# ⚡ FreelanceHT

> La première plateforme freelance dédiée aux talents haïtiens — connectez clients et freelancers, gérez projets, contrats et paiements en **HTG (Gourde Haïtienne)**.

---

## Table des matières

1. [Présentation](#présentation)
2. [Fonctionnalités](#fonctionnalités)
3. [Stack technique](#stack-technique)
4. [Architecture du projet](#architecture-du-projet)
5. [Installation et démarrage](#installation-et-démarrage)
6. [Configuration](#configuration)
7. [Structure des URLs](#structure-des-urls)
8. [Modèles de données](#modèles-de-données)
9. [Templates & Design System](#templates--design-system)
10. [Déploiement en production](#déploiement-en-production)
11. [Contribuer](#contribuer)

---

## Présentation

FreelanceHT est une plateforme web Django qui met en relation des **clients** haïtiens cherchant des prestataires avec des **freelancers** locaux qualifiés. Elle gère l'intégralité du cycle de vie d'une mission : publication de projet → propositions → contrat → jalons → paiement (MonCash, virement, espèces) → évaluation.

Le projet cible le marché haïtien avec une interface entièrement en **français**, des montants en **HTG**, une timezone réglée sur **America/Port-au-Prince** et un support natif de **MonCash** comme méthode de paiement.

---

## Fonctionnalités

### Comptes & Profils
- Inscription avec choix de rôle : **Client**, **Freelancer**, ou **Les deux**
- Authentification personnalisée (email ou nom d'utilisateur)
- Profil utilisateur avec avatar, bio, localisation, téléphone
- Profil freelancer étendu : titre, taux horaire, disponibilité, années d'expérience, portfolio, langues parlées
- Système de vérification de compte (`is_verified`)
- Notifications intégrées (propositions, messages, paiements, contrats)

### Projets
- Publication de projets par les clients (budget fixe ou horaire, en HTG)
- Filtres avancés : catégorie, compétence, type de budget, fourchette de prix, durée, recherche textuelle
- Visibilité configurable : public, privé, sur invitation
- Compteur de vues par projet
- Statuts : Brouillon → Ouvert → En cours → Terminé / Annulé

### Propositions
- Soumission de proposition par les freelancers (lettre de motivation, montant, durée estimée)
- Unicité de la proposition par freelancer et par projet
- Acceptation d'une proposition par le client → création automatique du contrat
- Rejet automatique des autres propositions à l'acceptation

### Contrats & Jalons
- Création automatique du contrat à l'acceptation d'une proposition
- Jalons avec montants, dates d'échéance et statuts (En attente → En cours → Soumis → Approuvé → Payé)
- Historique complet des paiements (escrow, libération, remboursement)
- Méthodes de paiement : **MonCash**, virement bancaire, espèces
- Clôture du contrat par le client avec mise à jour des statistiques freelancer

### Messagerie
- Conversations bilatérales entre utilisateurs
- Marquage automatique des messages comme lus
- Démarrage de conversation depuis le profil d'un freelancer ou d'un projet
- Interface de chat avec auto-scroll

### Évaluations
- Avis post-contrat avec note globale (1–5 étoiles)
- Scores détaillés : communication, qualité du travail, respect des délais
- Mise à jour automatique de la note moyenne du freelancer
- Avis publics visibles sur les profils

### Catégories & Compétences
- Catégories de compétences avec slug et icône (compatible Lucide Icons)
- Compétences tagguées sur les projets et les profils freelancers
- Niveau de maîtrise par compétence : Débutant, Intermédiaire, Expert

---

## Stack technique

| Couche | Technologie |
|---|---|
| Framework | Django 5.x |
| Base de données | SQLite (dev) / PostgreSQL recommandé (prod) |
| Authentification | Django Auth + vues personnalisées |
| CSS | Tailwind CSS v3 (via CDN) |
| Icônes | Lucide Icons (via CDN) |
| Typographie | Syne (display) + DM Sans (body) — Google Fonts |
| Upload fichiers | Pillow + Django media files |
| Variables d'environnement | python-dotenv |
| Langue | Français (`fr-ht`) |
| Timezone | `America/Port-au-Prince` |

---

## Architecture du projet

```
backends/
├── manage.py
├── requirements.txt
├── db.sqlite3                    # Généré après migrations
├── static/                       # Fichiers statiques du projet
├── media/                        # Uploads utilisateurs (avatars, portfolio)
├── templates/                    # Tous les templates Django
│   ├── base.html                 # Layout global (navbar, footer, flash messages)
│   ├── core/
│   │   └── home.html             # Page d'accueil
│   ├── accounts/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── profile.html
│   │   ├── dashboard_freelancer.html
│   │   ├── dashboard_client.html
│   │   └── complete_freelancer_profile.html
│   ├── freelancers/
│   │   ├── freelancer_list.html  # Annuaire avec filtres
│   │   └── freelancer_detail.html
│   ├── projects/
│   │   ├── project_list.html     # Liste avec filtres
│   │   ├── project_detail.html   # Détail + formulaire de proposition
│   │   └── project_form.html     # Création / édition
│   ├── contracts/
│   │   ├── contract_list.html
│   │   ├── contract_detail.html
│   │   └── review_form.html
│   └── messaging/
│       ├── conversation_list.html
│       └── conversation_detail.html
├── freelanceht/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── apps/
    ├── accounts/                 # Utilisateurs, profils, notifications
    ├── freelancers/              # Profils freelancers, compétences, portfolio
    ├── projects/                 # Projets, propositions
    ├── contracts/                # Contrats, jalons, paiements, avis
    ├── messaging/                # Conversations et messages
    └── core/                     # Page d'accueil, vues génériques
```

---

## Installation et démarrage

### Prérequis

- Python 3.10+
- pip
- (Optionnel) virtualenv ou venv

### 1. Cloner le dépôt

```bash
git clone https://github.com/votre-org/freelanceht.git
cd freelanceht/backends
```

### 2. Créer et activer un environnement virtuel

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Appliquer les migrations

```bash
python manage.py migrate
```

### 5. Créer un superutilisateur

```bash
python manage.py createsuperuser
```

### 6. Charger des données de démonstration (optionnel)

Si vous avez des fixtures :

```bash
python manage.py loaddata fixtures/categories.json
python manage.py loaddata fixtures/skills.json
```

Sinon, ajoutez manuellement des catégories et compétences depuis l'interface admin (`/admin/`).

### 7. Lancer le serveur de développement

```bash
python manage.py runserver
```

L'application est accessible sur [http://127.0.0.1:8000](http://127.0.0.1:8000).

L'interface d'administration est sur [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin).

---

## Configuration

### Variables d'environnement

Créez un fichier `.env` à la racine du dossier `backends/` :

```env
SECRET_KEY=votre-cle-secrete-tres-longue-et-aleatoire
DEBUG=False
ALLOWED_HOSTS=votredomaine.ht,www.votredomaine.ht

# Base de données (PostgreSQL en production)
DATABASE_URL=postgresql://user:password@localhost:5432/freelanceht

# Email (optionnel)
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=no-reply@votredomaine.ht
EMAIL_HOST_PASSWORD=motdepasse
```

Mettez à jour `settings.py` pour lire ces variables :

```python
import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
```

### Paramètres importants dans `settings.py`

| Paramètre | Valeur actuelle | Description |
|---|---|---|
| `LANGUAGE_CODE` | `fr-ht` | Interface en français haïtien |
| `TIME_ZONE` | `America/Port-au-Prince` | Fuseau horaire local |
| `LOGIN_URL` | `accounts:login` | Redirection si non authentifié |
| `LOGIN_REDIRECT_URL` | `accounts:dashboard` | Après connexion réussie |
| `LOGOUT_REDIRECT_URL` | `core:home` | Après déconnexion |

---

## Structure des URLs

| URL | Namespace | Vue | Description |
|---|---|---|---|
| `/` | `core:home` | `home` | Page d'accueil |
| `/compte/inscription/` | `accounts:register` | `register` | Inscription |
| `/compte/connexion/` | `accounts:login` | `CustomLoginView` | Connexion |
| `/compte/deconnexion/` | `accounts:logout` | `CustomLogoutView` | Déconnexion |
| `/compte/dashboard/` | `accounts:dashboard` | `dashboard` | Redirection selon rôle |
| `/compte/dashboard/freelancer/` | `accounts:freelancer_dashboard` | `freelancer_dashboard` | Dashboard freelancer |
| `/compte/dashboard/client/` | `accounts:client_dashboard` | `client_dashboard` | Dashboard client |
| `/compte/profil/` | `accounts:profile` | `profile` | Modifier son profil |
| `/compte/profil/freelancer/completer/` | `accounts:complete_freelancer_profile` | `complete_freelancer_profile` | Compléter profil freelancer |
| `/freelancers/` | `freelancers:list` | `freelancer_list` | Annuaire freelancers |
| `/freelancers/<pk>/` | `freelancers:detail` | `freelancer_detail` | Profil d'un freelancer |
| `/projets/` | `projects:list` | `project_list` | Liste des projets |
| `/projets/nouveau/` | `projects:create` | `project_create` | Créer un projet |
| `/projets/<pk>/` | `projects:detail` | `project_detail` | Détail d'un projet |
| `/projets/<pk>/modifier/` | `projects:edit` | `project_edit` | Modifier un projet |
| `/projets/<pk>/proposer/` | `projects:submit_proposal` | `submit_proposal` | Soumettre une proposition |
| `/projets/<pk>/proposition/<pk>/accepter/` | `projects:accept_proposal` | `accept_proposal` | Accepter une proposition |
| `/contrats/` | `contracts:list` | `contract_list` | Mes contrats |
| `/contrats/<pk>/` | `contracts:detail` | `contract_detail` | Détail d'un contrat |
| `/contrats/<pk>/terminer/` | `contracts:complete` | `complete_contract` | Clôturer un contrat |
| `/contrats/<pk>/avis/` | `contracts:review` | `review_contract` | Laisser un avis |
| `/messages/` | `messaging:list` | `conversation_list` | Mes messages |
| `/messages/<pk>/` | `messaging:detail` | `conversation_detail` | Ouvrir une conversation |
| `/messages/nouveau/<user_pk>/` | `messaging:start` | `start_conversation` | Démarrer une conversation |

---

## Modèles de données

### `UserProfile` (accounts)
Extension du `User` Django. Rôles : `client`, `freelancer`, `both`. Champs : avatar, bio, localisation, téléphone, timezone, `is_verified`.

### `FreelancerProfile` (freelancers)
Lié à `UserProfile`. Champs clés : titre, taux horaire (HTG), disponibilité, années d'expérience, portfolio URL. Statistiques calculées : `rating_avg`, `completed_jobs`, `total_earned`.

### `SkillCategory` & `Skill` (freelancers)
Catégories avec slug et icône (nom compatible Lucide). Compétences associées aux catégories et aux profils via `FreelancerSkill` (table intermédiaire avec niveau de maîtrise).

### `Project` (projects)
Publié par un client. Budget fixe ou horaire. Statuts : Draft → Open → In Progress → Completed / Cancelled. Visibilité : public, privé, sur invitation.

### `Proposal` (projects)
Soumise par un freelancer pour un projet ouvert. Unique par couple `(project, freelancer)`. Inclut lettre de motivation, montant proposé, durée estimée.

### `Contract` (contracts)
Créé automatiquement à l'acceptation d'une proposition. Lie client, freelancer et projet. Supporte les jalons (`Milestone`), les paiements (`Payment`) et les avis (`Review`).

### `Payment` (contracts)
Méthodes supportées : **MonCash** (avec `moncash_transaction_id`), virement bancaire, espèces. Statuts : En attente → En dépôt → Libéré / Remboursé. Calcul des frais de plateforme et du montant net.

### `Conversation` & `Message` (messaging)
Conversation entre deux `UserProfile`. Messages avec horodatage et marquage de lecture (`read_at`).

---

## Templates & Design System

### Philosophie

Tous les templates héritent de `base.html` via `{% extends 'base.html' %}`. Le design est **épuré et moderne**, pensé pour la lisibilité et la confiance, deux valeurs clés pour une plateforme de freelancing.

### Palette de couleurs

| Rôle | Couleur | Classe Tailwind |
|---|---|---|
| Couleur principale | Teal 600 | `bg-brand-600` / `text-brand-600` |
| Accent | Cyan | `text-cyan-500` |
| Succès | Green | `bg-green-100 text-green-700` |
| Avertissement | Amber | `bg-amber-100 text-amber-700` |
| Erreur | Red | `bg-red-100 text-red-700` |
| Étoiles | Gold | `text-amber-400` |

### Typographie

- **Titres** : `Syne` (Google Fonts) — moderne et distinctif
- **Corps** : `DM Sans` (Google Fonts) — lisible et neutre

### Composants réutilisables

- **`.btn-primary`** — bouton dégradé teal avec hover lift
- **`.card-hover`** — carte avec transition translateY au survol
- **`.skill-badge`** — badge de compétence uppercase condensé
- **`.glass`** — fond glassmorphism pour la navbar sticky
- **`.gradient-text`** — texte en dégradé teal → cyan
- **`.pattern-bg`** — fond pointillé subtil (section hero)

### Icônes

Toutes les icônes utilisent **Lucide Icons** via CDN. L'initialisation se fait en fin de page avec `lucide.createIcons()`. Syntaxe dans les templates :

```html
<i data-lucide="nom-de-l-icone" class="w-5 h-5"></i>
```

---

## Déploiement en production

### Checklist

```bash
# 1. Désactiver le mode debug
DEBUG=False

# 2. Générer une vraie SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# 3. Configurer ALLOWED_HOSTS
ALLOWED_HOSTS=votredomaine.ht

# 4. Collecter les fichiers statiques
python manage.py collectstatic --noinput

# 5. Appliquer les migrations
python manage.py migrate

# 6. Configurer un serveur WSGI (Gunicorn recommandé)
pip install gunicorn
gunicorn freelanceht.wsgi:application --bind 0.0.0.0:8000
```

### PostgreSQL (recommandé en production)

```bash
pip install psycopg2-binary
```

Dans `settings.py` :

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'freelanceht',
        'USER': 'freelanceht_user',
        'PASSWORD': 'motdepasse',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Nginx (exemple de configuration)

```nginx
server {
    listen 80;
    server_name votredomaine.ht;

    location /static/ {
        alias /chemin/vers/backends/staticfiles/;
    }

    location /media/ {
        alias /chemin/vers/backends/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Tailwind CSS en production

Actuellement, Tailwind est chargé via CDN (pratique pour le développement). Pour la production, il est recommandé de compiler Tailwind pour obtenir un CSS optimisé et purgé :

```bash
npm install -D tailwindcss
npx tailwindcss init
npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --minify
```

---

## Contribuer

Les contributions sont les bienvenues ! Voici comment participer :

1. Forkez le dépôt
2. Créez une branche pour votre feature : `git checkout -b feature/ma-fonctionnalite`
3. Committez vos changements : `git commit -m "feat: description claire"`
4. Poussez la branche : `git push origin feature/ma-fonctionnalite`
5. Ouvrez une Pull Request

### Idées d'améliorations futures

- Intégration API MonCash officielle
- Système de notifications en temps réel (WebSockets / Django Channels)
- Tableau de bord analytique pour les admins
- Compilation Tailwind CSS pour la production
- Tests unitaires et d'intégration
- API REST (Django REST Framework) pour une future app mobile
- Système de litiges entre clients et freelancers
- Profils d'agences (plusieurs freelancers sous une même entité)

---

*FreelanceHT — Fait avec ❤️ pour la communauté haïtienne*
