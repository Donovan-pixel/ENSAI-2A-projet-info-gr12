from unittest.mock import MagicMock

from service.ingredient_service import IngredientService

from dao.ingredient_dao import IngredientDao

from business_object.ingredient import Ingredient


liste_ingredients = [
    Ingredient(nom="Tomate", idIngredient=12),
    Ingredient(nom="Carotte", idIngredient=13),
    Ingredient(nom="Avocat", idIngredient=34),
]


def test_ajouterNouvelIngredient_succes():

    # GIVEN

    nom = "Pomme"
    IngredientDao().ajouterIngredient = MagicMock(return_value=True)

    # WHEN

    res = IngredientService().ajouterNouvelIngredient(nom)

    # THEN

    assert res is True


def test_ajouterNouvelIngredient_echec():

    # GIVEN

    nom = "Pomme"
    IngredientDao().ajouterIngredient = MagicMock(return_value=None)

    # WHEN

    res = IngredientService().ajouterNouvelIngredient(nom)

    # THEN

    assert res is None


def test_obtenirTousLesIngredients_succes():

    # GIVEN

    IngredientDao().obtenirTousLesIngredients = MagicMock(return_value=liste_ingredients)

    # WHEN

    res = IngredientService().obtenirTousLesIngredients()

    # THEN

    assert len(res) == 3
    assert res[0].nom == "Tomate"
    assert res[1].nom == "Carotte"
    assert res[2].nom == "Avocat"


def test_supprimer_succes():

    # GIVEN

    ingredient = "Tomate"
    IngredientDao().supprimerIngredient = MagicMock(return_value=True)

    # WHEN

    res = IngredientService().supprimer(ingredient)

    # THEN

    assert res is True


def test_supprimer_echec():

    # GIVEN

    ingredient = "Tomate"
    IngredientDao().supprimerIngredient = MagicMock(return_value=False)

    # WHEN

    res = IngredientService().supprimer(ingredient)

    # THEN

    assert res is False


def test_obtenirIdParNom():

    # GIVEN

    ingredient = "Tomate"
    IngredientDao().obtenirIdParNom = MagicMock(return_value=12)

    # WHEN

    res = IngredientService().obtenirIdPArNom(ingredient)

    # THEN

    assert res == 12


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
