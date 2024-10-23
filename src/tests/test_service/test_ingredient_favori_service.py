from unittest.mock import MagicMock

from service.ingredient_favori_service import IngredientFavoriService

from dao.ingredient_favori_dao import IngredientFavoriDao

from business_object.ingredient import Ingredient
from business_object.utilisateur import Utilisateur

liste_ingredients_favoris = [
    Ingredient(nom="Tomate", idIngredient=12),
    Ingredient(nom="Carotte", idIngredient=13),
    Ingredient(nom="Avocat", idIngredient=34),
]


def test_ajouterIngredientFavori_succes():

    # GIVEN

    nom = "Pomme"
    utilisateur = Utilisateur(pseudo="jp", motDePasse="1234", role="Utilisateur", idUtilisateur=1)
    IngredientFavoriDao().ajouterIngredientFavori = MagicMock(return_value=True)

    # WHEN

    res = IngredientFavoriService().ajouterIngredientFavori(nom, utilisateur)

    # THEN

    assert res is True


def test_ajouterIngredientFavori_echec():

    # GIVEN

    nom = "Pomme"
    utilisateur = Utilisateur(pseudo="jp", motDePasse="1234", role="Utilisateur", idUtilisateur=1)

    IngredientFavoriDao().ajouterIngredientFavori = MagicMock(return_value=None)

    # WHEN

    res = IngredientFavoriService().ajouterIngredientFavori(nom, utilisateur)

    # THEN

    assert res is None


def test_obtenirIngredientsFavoris_succes():

    # GIVEN

    utilisateur = Utilisateur(pseudo="jp", motDePasse="1234", role="Utilisateur", idUtilisateur=1)

    IngredientFavoriDao().obtenirIngredientsFavoris = MagicMock(
        return_value=liste_ingredients_favoris
    )

    # WHEN

    res = IngredientFavoriService().obtenirIngredientsFavoris(utilisateur)

    # THEN

    assert len(res) == 3
    assert res[0].nom == "Tomate"
    assert res[1].nom == "Carotte"
    assert res[2].nom == "Avocat"


def test_supprimerIngredientFavori_succes():

    # GIVEN

    nom = "Tomate"
    utilisateur = Utilisateur(pseudo="jp", motDePasse="1234", role="Utilisateur", idUtilisateur=1)

    IngredientFavoriDao().supprimerIngredientFavori = MagicMock(return_value=True)

    # WHEN

    res = IngredientFavoriService().supprimerIngredientFavori(nom, utilisateur)

    # THEN

    assert res is True


def test_supprimerIngredientFavori_echec():

    # GIVEN

    nom = "Tomate"
    utilisateur = Utilisateur(pseudo="jp", motDePasse="1234", role="Utilisateur", idUtilisateur=1)

    IngredientFavoriDao().supprimerIngredientFavori = MagicMock(return_value=False)

    # WHEN

    res = IngredientFavoriService().supprimerIngredientFavori(nom, utilisateur)

    # THEN

    assert res is False


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
