import os
import pytest
from unittest.mock import patch
from dao.liste_de_course_dao import ListeDeCourseDAO
from business_object.liste_de_course import ListeDeCourses
from business_object.ingredient import Ingredient
from utils.reset_database import ResetDatabase


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialisation de la base de données pour les tests"""
    with patch.dict(os.environ, {"SCHEMA": "projet_test_dao"}):
        ResetDatabase().lancer(test_dao=True)
        yield


def test_creer_liste_de_courses():
    """Test pour la création d'une nouvelle liste de courses"""

    # GIVEN
    id_utilisateur = 1
    liste_course = ListeDeCourses(idUtilisateur=id_utilisateur)

    # WHEN
    creation_ok = ListeDeCourseDAO().creerListeDeCourses(liste_course)

    # THEN
    assert creation_ok == 1
    assert liste_course.idListeDecourses is not None


def test_ajouter_un_ingredient():
    """Test pour ajouter un ingrédient à une liste de courses"""

    # GIVEN
    id_utilisateur = 1
    ingredient_quantite = {"Tomate": 3, "Oignon": 2}

    # WHEN
    ajout_ok = ListeDeCourseDAO().ajouterUnIngredient(id_utilisateur, ingredient_quantite)

    # THEN
    assert ajout_ok


def test_retirer_un_ingredient():
    """Test pour retirer un ingrédient d'une liste de courses"""

    # GIVEN
    id_utilisateur = 1
    ingredient = Ingredient(idIngredient=1, nom="Tomate")

    # WHEN
    retrait_ok = ListeDeCourseDAO().retirerUnIngredient(id_utilisateur, ingredient)

    # THEN
    assert retrait_ok


if __name__ == "__main__":
    pytest.main([__file__])
