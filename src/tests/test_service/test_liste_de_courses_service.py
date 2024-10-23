import pytest
from unittest.mock import patch
from service.liste_de_courses_service import ListeDeCoursesService
from business_object.liste_de_course import ListeDeCourses
from business_object.ingredient import Ingredient


@pytest.fixture
def service():
    """Fixture qui retourne une instance du service ListeDeCoursesService."""
    return ListeDeCoursesService()


@patch("dao.liste_de_course_dao.ListeDeCourseDAO.creerListeDeCourses", return_value=True)
def test_creer_liste_de_courses_ok(mock_creer, service):
    """Test pour la création d'une nouvelle liste de courses."""

    # GIVEN
    id_utilisateur = 1

    # WHEN
    resultat = service.creer(id_utilisateur)

    # THEN
    assert resultat is not None
    mock_creer.assert_called_once()


@patch("dao.liste_de_course_dao.ListeDeCourseDAO.listerTous", return_value=[])
def test_lister_tous_ok(mock_lister_tous, service):
    """Test pour lister toutes les listes de courses d'un utilisateur."""

    # GIVEN
    id_utilisateur = 1

    # WHEN
    listes = service.lister_tous(id_utilisateur)

    # THEN
    assert listes == []
    mock_lister_tous.assert_called_once_with(id_utilisateur)


@patch("dao.liste_de_course_dao.ListeDeCourseDAO.ajouterUnIngredient", return_value=True)
def test_ajouter_ingredient_ok(mock_ajouter_ingredient, service):
    """Test pour ajouter un ingrédient à une liste de courses."""

    # GIVEN
    id_utilisateur = 1
    ingredient_quantite = {"Tomate": 3, "Oignon": 2}

    # WHEN
    resultat = service.ajouter_ingredient(id_utilisateur, ingredient_quantite)

    # THEN
    assert resultat is True
    mock_ajouter_ingredient.assert_called_once_with(id_utilisateur, ingredient_quantite)


@patch("dao.liste_de_course_dao.ListeDeCourseDAO.retirerUnIngredient", return_value=True)
def test_retirer_ingredient_ok(mock_retirer_ingredient, service):
    """Test pour retirer un ingrédient d'une liste de courses."""

    # GIVEN
    id_utilisateur = 1
    ingredient = Ingredient(idIngredient=1, nom="Tomate")

    # WHEN
    resultat = service.retirer_ingredient(id_utilisateur, ingredient)

    # THEN
    assert resultat is True
    mock_retirer_ingredient.assert_called_once_with(id_utilisateur, ingredient)


@patch("dao.liste_de_course_dao.ListeDeCourseDAO.obtenirIdListeDeCourses", return_value=101)
def test_obtenir_id_liste_ok(mock_obtenir_id_liste, service):
    """Test pour obtenir l'ID de la liste de courses d'un utilisateur."""

    # GIVEN
    id_utilisateur = 1

    # WHEN
    id_liste = service.obtenir_id_liste(id_utilisateur)

    # THEN
    assert id_liste == 101
    mock_obtenir_id_liste.assert_called_once_with(id_utilisateur)


@patch("dao.liste_de_course_dao.ListeDeCourseDAO.listerTous")
def test_afficher_tous_ok(mock_lister_tous, service):
    """Test pour afficher toutes les listes de courses d'un utilisateur."""

    # GIVEN
    id_utilisateur = 1

    # Création d'une instance de ListeDeCourses
    liste_de_courses = ListeDeCourses(idUtilisateur=id_utilisateur)

    # Ajout d'ingrédients via la méthode ajouterIngredient
    liste_de_courses.ajouterIngredient(Ingredient(nom="Tomate"), 3)
    liste_de_courses.ajouterIngredient(Ingredient(nom="Oignon"), 2)

    # Simuler le retour de listerTous pour retourner cette liste
    mock_lister_tous.return_value = [liste_de_courses]

    # WHEN
    resultat = service.afficher_tous(id_utilisateur)

    # THEN
    assert "Tomate" in resultat
    assert "Oignon" in resultat
    mock_lister_tous.assert_called_once_with(id_utilisateur)


if __name__ == "__main__":
    pytest.main([__file__])
