from unittest.mock import MagicMock

from service.ingredient_favori_service import IngredientFavoriService

from dao.ingredient_favori_dao import IngredientFavoriDao

from business_object.ingredient import Ingredient


liste_ingredients_favoris = [
    Ingredient(nom="Tomate", idIngredient=12),
    Ingredient(nom="Carotte", idIngredient=13),
    Ingredient(nom="Avocat", idIngredient=34),
]


def test_ajouterIngredientFavori_succes():

    # GIVEN

    nom = "Pomme"
    IngredientFavoriDao().ajouterIngredientFavori = MagicMock(return_value=True)

    # WHEN

    res = IngredientFavoriService().ajouterIngredientFavori(nom)

    # THEN

    assert res is True


def test_ajouterIngredientFavori_echec():

    # GIVEN

    nom = "Pomme"
    IngredientFavoriDao().ajouterIngredientFavori = MagicMock(return_value=None)

    # WHEN

    res = IngredientFavoriService().ajouterIngredientFavori(nom)

    # THEN

    assert res is None


def test_obtenirIngredientsFavoris_succes():

    # GIVEN

    IngredientFavoriDao().obtenirIngredientsFavoris = MagicMock(
        return_value=liste_ingredients_favoris
    )

    # WHEN

    res = IngredientFavoriService().obtenirIngredientsFavoris()

    # THEN

    assert len(res) == 3
    assert res[0].nom == "Tomate"
    assert res[1].nom == "Carotte"
    assert res[2].nom == "Avocat"


def test_supprimerIngredientFavori_succes():

    # GIVEN

    ingredient = "Tomate"
    IngredientFavoriDao().supprimerIngredientFavori = MagicMock(return_value=True)

    # WHEN

    res = IngredientFavoriService().supprimerIngredientFavori(ingredient)

    # THEN

    assert res is True


def test_supprimer_echec():

    # GIVEN

    ingredient = "Tomate"
    IngredientFavoriDao().supprimerIngredientFavori = MagicMock(return_value=False)

    # WHEN

    res = IngredientFavoriService().supprimerIngredientFavori(ingredient)

    # THEN

    assert res is False


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
