from unittest.mock import MagicMock
from service.liste_de_courses_service import ListeDeCoursesService
from dao.liste_de_course_dao import ListeDeCourseDAO
from business_object.liste_de_course import ListeDeCourses
from business_object.ingredient import Ingredient


def test_creer_liste_de_courses_succes():
    """Test pour la création d'une nouvelle liste de courses qui réussit."""

    # GIVEN
    id_utilisateur = 1
    ListeDeCourseDAO().creerListeDeCourses = MagicMock(return_value=True)

    # WHEN
    resultat = ListeDeCoursesService().creer(id_utilisateur)

    # THEN
    assert resultat is not None


def test_creer_liste_de_courses_echec():
    """Test pour la création d'une nouvelle liste de courses qui échoue."""

    # GIVEN
    id_utilisateur = 1
    ListeDeCourseDAO().creerListeDeCourses = MagicMock(return_value=False)

    # WHEN
    resultat = ListeDeCoursesService().creer(id_utilisateur)

    # THEN
    assert resultat is None


def test_ajouter_ingredient_succes():
    """Test pour ajouter un ingrédient à une liste de courses qui réussit."""

    # GIVEN
    id_utilisateur = 1
    ingredient_quantite = {"Tomate": 3}
    ListeDeCourseDAO().ajouterUnIngredient = MagicMock(return_value=True)

    # WHEN
    resultat = ListeDeCoursesService().ajouter_ingredient(id_utilisateur, ingredient_quantite)

    # THEN
    assert resultat is True


def test_ajouter_ingredient_echec():
    """Test pour ajouter un ingrédient à une liste de courses qui échoue."""

    # GIVEN
    id_utilisateur = 1
    ingredient_quantite = {"Tomate": 3}
    ListeDeCourseDAO().ajouterUnIngredient = MagicMock(return_value=False)

    # WHEN
    resultat = ListeDeCoursesService().ajouter_ingredient(id_utilisateur, ingredient_quantite)

    # THEN
    assert resultat is False


def test_retirer_ingredient_succes():
    """Test pour retirer un ingrédient d'une liste de courses qui réussit."""

    # GIVEN
    id_utilisateur = 1
    ingredient = Ingredient(idIngredient=1, nom="Tomate")
    ListeDeCourseDAO().retirerUnIngredient = MagicMock(return_value=True)

    # WHEN
    resultat = ListeDeCoursesService().retirer_ingredient(id_utilisateur, ingredient)

    # THEN
    assert resultat is True


def test_retirer_ingredient_echec():
    """Test pour retirer un ingrédient d'une liste de courses qui échoue."""

    # GIVEN
    id_utilisateur = 1
    ingredient = Ingredient(idIngredient=1, nom="Tomate")
    ListeDeCourseDAO().retirerUnIngredient = MagicMock(return_value=False)

    # WHEN
    resultat = ListeDeCoursesService().retirer_ingredient(id_utilisateur, ingredient)

    # THEN
    assert resultat is False


def test_afficher_tous_vide():
    """Test pour afficher aucune liste de courses d'un utilisateur."""

    # GIVEN
    id_utilisateur = 1
    ListeDeCourseDAO().listerTous = MagicMock(return_value=[])

    # WHEN
    resultat = ListeDeCoursesService().afficher_tous(id_utilisateur)

    # THEN
    assert resultat == "Aucune liste de courses disponible pour cet utilisateur."


def test_afficher_tous_succes():
    """Test pour afficher les listes de courses d'un utilisateur qui réussit."""

    # GIVEN
    id_utilisateur = 1
    ingredient_quantite = {Ingredient(nom="Tomate"): 3, Ingredient(nom="Oignon"): 2}
    liste_de_courses = ListeDeCourses(idUtilisateur=id_utilisateur)
    liste_de_courses.ingredientQuantite = ingredient_quantite
    ListeDeCourseDAO().listerTous = MagicMock(return_value=[liste_de_courses])

    # WHEN
    resultat = ListeDeCoursesService().afficher_tous(id_utilisateur)

    # THEN
    assert "Tomate" in resultat
    assert "Oignon" in resultat


def test_obtenir_id_liste_succes():
    """Test pour obtenir l'ID de la liste de courses d'un utilisateur qui réussit."""

    # GIVEN
    id_utilisateur = 1
    ListeDeCourseDAO().obtenirIdListeDeCourses = MagicMock(return_value=101)

    # WHEN
    id_liste = ListeDeCoursesService().obtenir_id_liste(id_utilisateur)

    # THEN
    assert id_liste == 101


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
