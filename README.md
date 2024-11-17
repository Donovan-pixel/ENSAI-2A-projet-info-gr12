# My Kitchen - Projet informatique 2A

**My Kitchen** est une application de gestion de recettes culinaires développée dans le cadre du projet informatique de 2e année à l'ENSAI. Elle intègre les concepts suivants :  

- Programmation en couches (DAO, service, vue, business_object).  
- Connexion à une base de données PostgreSQL.  
- Interface utilisateur basée sur le terminal via InquirerPy.  
- Appels à un Webservice externe : TheMealDB API.  
- Gestion des favoris et liste de courses.  

---

## :arrow_forward: Fonctionnalités principales

- **Recherche de recettes** : Affichage d'une liste de recettes et détails associés.  
- **Favoris** : Ajout ou suppression de recettes et ingrédients dans les favoris.  
- **Liste de courses** : Gestion des ingrédients nécessaires pour préparer les recettes sélectionnées.  
- **Administration** : Gestion des recettes via un rôle dédié (Administrateur).  
- **API externe** : Intégration avec TheMealDB pour enrichir les données des recettes.  

---

## :hammer: Pré-requis

- [Python 3.10](https://www.python.org/)  
- [PostgreSQL](https://www.postgresql.org/)  
- [Git](https://git-scm.com/)  
- [Visual Studio Code](https://code.visualstudio.com/)  

---

## :computer: Installation

### Cloner le projet

1. Ouvrez **Git Bash** ou un terminal.  
2. Créez un dossier pour le projet :  
   ```bash
   mkdir -p <chemin_du_dossier> && cd $_
   ```  
3. Clonez ce dépôt :  
   ```bash
   https://github.com/Fathnelle/ENSAI-2A-projet-info-gr12.git
   ```  

### Configurer l'environnement

1. Accédez au répertoire du projet :  
   ```bash
   cd my-kitchen
   ```  
2. Installez les dépendances Python :  
   ```bash
   pip install -r requirements.txt
   ```  
3. Configurez les variables d'environnement :  
   - Renommez le fichier `.env.template` en `.env`.  
   - Renseignez les paramètres PostgreSQL et TheMealDB dans ce fichier. Exemple :  
     ```env
     POSTGRES_HOST=localhost
     POSTGRES_PORT=5432
     POSTGRES_DATABASE=mykitchen
     POSTGRES_USER=admin
     POSTGRES_PASSWORD=password

     THEMEALDB_API=https://www.themealdb.com/api/json/v1/1
     ```

---

## :rocket: Démarrage

1. **Initialisez la base de données** :  
   - Lancez le script d'initialisation :  
     ```bash
     python src/utils/reset_database.py
     ```  
   - Cela créera les tables nécessaires et importera les données de base.  

2. **Lancez l'application** :  
   ```bash
   python src/__main__.py
   ```  

---

## :wrench: Tests unitaires

1. Exécutez les tests :  
   ```bash
   pytest -v
   ```  
2. Générez un rapport de couverture :  
   ```bash
   coverage run -m pytest
   coverage html
   ```  
   - Ouvrez le rapport : `htmlcov/index.html`.

---

## :notebook_with_decorative_cover: Architecture

### Structure du projet

```plaintext
src/
├── dao/                # Data Access Objects
├── services/           # Business logic
├── views/              # Interface utilisateur
├── utils/              # Outils divers (logs, BDD, etc.)
└── business_objects/   # Objets métier
```

### Tables principales

- **recettes** : Stocke les informations des recettes.  
- **ingredients** : Liste des ingrédients associés aux recettes.  
- **users** : Gestion des utilisateurs.  
- **favoris** : Association utilisateur-favoris.  
- **liste_de_courses** : Gestion des listes de courses par utilisateur.  

---

## :page_with_curl: Configuration avancée

### Journaux d'exécution

- Fichier de configuration : `logging_config.yml`.  
- Logs accessibles dans le dossier `logs/`.  

### Intégration continue

- Workflows GitHub Actions pour :  
  - Lancement automatique des tests unitaires.  
  - Analyse statique du code avec *pylint*.  

---

## :bulb: Contributions

Ce projet est conçu pour être extensible. Vous pouvez :  
- Ajouter de nouvelles fonctionnalités (par exemple, une recherche avancée).  
- Améliorer les performances (optimisation des requêtes SQL).  
- Renforcer la sécurité (gestion des erreurs, validations).  

---  

:wave: **Merci de votre intérêt pour *My Kitchen* !** N'hésitez pas à nous faire part de vos retours ou suggestions.
