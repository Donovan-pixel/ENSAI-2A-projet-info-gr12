# My Kitchen - 2nd Year Computer Science Project

**My Kitchen** is a culinary recipe management application developed as part of the 2nd-year computer science project at ENSAI. It integrates the following concepts:

- Layered programming (DAO, service, view, business_object)
- Connection to a PostgreSQL database
- User interface based on terminal via InquirerPy
- External Webservice calls: TheMealDB API
- Favorites and shopping list management

---

## :arrow_forward: Main Features

- **Recipe Search**: Display a list of recipes and associated details
- **Recipe Suggestions**: Personalized recipe suggestions based on favorite and unwanted ingredients
- **Favorites**: Add or remove recipes and ingredients from favorites
- **Shopping List**: Management of ingredients needed to prepare selected recipes
- **Administration**: Recipe management via a dedicated role (Administrator)
- **External API**: Integration with TheMealDB to enrich recipe data

---

## :hammer: Prerequisites

- [Python 3.10](https://www.python.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Git](https://git-scm.com/)
- [Visual Studio Code](https://code.visualstudio.com/)

---

## :computer: Installation

### Clone the Project

1. Open **Git Bash** or a terminal
2. Create a project folder:
   ```bash
   mkdir -p <folder_path> && cd $_
   ```
3. Clone this repository:
   ```bash
   https://github.com/Fathnelle/ENSAI-2A-projet-info-gr12.git
   ```

### Configure Environment

1. Navigate to the project directory:
   ```bash
   cd <folder_path>
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables:
   - Rename `.env.template` to `.env`
   - Fill in your personal information instead of **xxxx**. Example:
     ```env
     WEBSERVICE_HOST="https://www.themealdb.com/api/json/v1/1"

     POSTGRES_HOST=sgbd-eleves.domensai.ecole
     POSTGRES_PORT=5432
     POSTGRES_DATABASE=idxxxx
     POSTGRES_USER=idxxxx
     POSTGRES_PASSWORD=idxxxx
     POSTGRES_SCHEMA=projet
     ```

---

## :rocket: Launch

1. **Initialize the database**:
   - Run the initialization script:
     ```bash
     python src/utils/reset_database.py
     ```
   - This will create the necessary tables and import base data

2. **Launch the application in Git Bash**:
   ```bash
   winpty python src/__main__.py
   ```
   ![My Kitchen Interface](doc/Capture d’écran 2024-11-17 160058.png)

---

## :wrench: Unit Tests

1. Run tests:
   ```bash
   python -m pytest -v
   ```
2. Generate coverage report:
   ```bash
   coverage run -m pytest
   coverage html
   ```
   - Open report: `htmlcov/index.html`

---

## :notebook_with_decorative_cover: Architecture

### Project Structure

```plaintext
src/
├── business_object/                 # Business objects and data models
├── client/                          # API data retrieval
├── dao/                             # Data access and database interaction
├── test/                            # Application functionality tests
├── service/                         # Services exposing application features
├── utils/                           # Utility functions (log management, files, etc.)
├── view/                            # User interface and terminal display
```

### Main Tables

- **recettes**: Stores recipe information
- **ingredients**: List of ingredients associated with recipes
- **users**: User management
- **favoris**: User-favorites association
- **liste_de_courses**: Shopping list management per user

---

## :page_with_curl: Advanced Configuration

### Continuous Integration

- GitHub Actions workflows for:
  - Automatic unit test launches
  - Static code analysis with *pylint*

---
## 👨‍💻 Group Members

- Martin Ahouétognon
- Melvin Bazeille
- Maïlis Lanne
- Fathnelle Mehouelley
- Luna Riviere

## :bulb: Contributions

This project is designed to be extensible. You can:
- Add new features (e.g., advanced search)
- Improve performance (SQL query optimization)
- Enhance security (error handling, validations)

---

:wave: **Thank you for your interest in *My Kitchen*!** Feel free to share your feedback or suggestions.
