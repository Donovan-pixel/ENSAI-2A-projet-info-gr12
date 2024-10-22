import pytest
from unittest.mock import MagicMock, patch
from dao.liste_de_course_dao import ListeDeCourseDAO
from business_object.liste_de_course import ListeDeCourses
from business_object.ingredient import Ingredient


@pytest.fixture
def mock_db_connection():
    """Fixture pour simuler une connexion à la base de données."""
    with patch("dao.db_connection.DBConnection") as MockDB:
        mock_connection = MagicMock()
        MockDB.return_value.connection = mock_connection
        yield mock_connection


def test_creer_liste_de_courses_ok(mock_db_connection):
    """Test pour la méthode creerListeDeCourses."""

    dao = ListeDeCourseDAO()
    liste_course = ListeDeCourses(idUtilisateur=1)

    # Simuler le comportement du curseur
    mock_cursor = MagicMock()
    mock_db_connection.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = {"id_liste_de_courses": 1}

    # Appeler la méthode
    result = dao.creerListeDeCourses(liste_course)

    # Vérifier les assertions
    assert result is True
    assert liste_course.idListeDecourses == 1


def test_lister_tous_ok(mock_db_connection):
    """Test pour la méthode listerTous."""

    dao = ListeDeCourseDAO()
    mock_cursor = MagicMock()
    mock_db_connection.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [{"nom": "Tomate", "quantite": "2"}]

    result = dao.listerTous(1)
    assert result == [{"nom": "Tomate", "quantite": "2"}]


def test_ajouter_un_ingredient_ok(mock_db_connection):
    """Test pour la méthode ajouterUnIngredient."""

    dao = ListeDeCourseDAO()
    mock_cursor = MagicMock()
    mock_db_connection.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [1]

    ingredient_quantite = {"Tomate": "2"}
    result = dao.ajouterUnIngredient(1, ingredient_quantite)

    assert result is True


def test_retirer_un_ingredient_ok(mock_db_connection):
    """Test pour la méthode retirerUnIngredient."""

    dao = ListeDeCourseDAO()
    mock_cursor = MagicMock()
    mock_db_connection.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.rowcount = 1

    ingredient = Ingredient(idIngredient=1)
    result = dao.retirerUnIngredient(1, ingredient)

    assert result is True
