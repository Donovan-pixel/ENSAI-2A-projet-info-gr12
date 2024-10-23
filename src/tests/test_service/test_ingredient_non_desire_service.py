from unittest.mock import MagicMock

from service.ingredient_non_desire_service import IngredientNonDesireService

from dao.ingredient_non_desire_dao import IngredientNonDesireDao

from business_object.ingredient import Ingredient
from business_object.utilisateur import Utilisateur

liste_ingredients_non_desires = [
    Ingredient(nom="Tomate", idIngredient=12),
    Ingredient(nom="Carotte", idIngredient=13),
    Ingredient(nom="Avocat", idIngredient=34),
]


def test_ajouterIngredientNonDesire_succes():

    # GIVEN

    nom = "Pomme"
    utilisateur = Utilisateur(pseudo="jp", motDePasse="1234", role="Utilisateur", idUtilisateur=1)

    IngredientNonDesireDao().ajouterIngredientNonDesire = MagicMock(return_value=True)

    # WHEN

    res = IngredientNonDesireService().ajouterIngredientNonDesire(nom, utilisateur)

    # THEN

    assert res is True


def test_ajouterIngredientNonDesire_echec():

    # GIVEN

    nom = "Pomme"
    utilisateur = Utilisateur(pseudo="jp", motDePasse="1234", role="Utilisateur", idUtilisateur=1)

    IngredientNonDesireDao().ajouterIngredientNonDesire = MagicMock(return_value=None)

    # WHEN

    res = IngredientNonDesireService().ajouterIngredientNonDesire(nom, utilisateur)

    # THEN

    assert res is None


def test_obtenirIngredientsNonDesires_succes():

    # GIVEN

    utilisateur = Utilisateur(pseudo="jp", motDePasse="1234", role="Utilisateur", idUtilisateur=1)

    IngredientNonDesireDao().obtenirIngredientsNonDesires = MagicMock(
        return_value=liste_ingredients_non_desires
    )

    # WHEN

    res = IngredientNonDesireService().obtenirIngredientsNonDesires(utilisateur)

    # THEN

    assert len(res) == 3
    assert res[0].nom == "Tomate"
    assert res[1].nom == "Carotte"
    assert res[2].nom == "Avocat"


def test_supprimerIngredientNonDesire_succes():

    # GIVEN

    nom = "Tomate"
    utilisateur = Utilisateur(pseudo="jp", motDePasse="1234", role="Utilisateur", idUtilisateur=1)

    IngredientNonDesireDao().supprimerIngredientNonDesire = MagicMock(return_value=True)

    # WHEN

    res = IngredientNonDesireService().supprimerIngredientNonDesire(nom, utilisateur)

    # THEN

    assert res is True


def test_supprimerIngredientNonDesire_echec():

    # GIVEN

    nom = "Tomate"
    utilisateur = Utilisateur(pseudo="jp", motDePasse="1234", role="Utilisateur", idUtilisateur=1)

    IngredientNonDesireDao().supprimerIngredientNonDesire = MagicMock(return_value=False)

    # WHEN

    res = IngredientNonDesireService().supprimerIngredientNonDesire(nom, utilisateur)

    # THEN

    assert res is False


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
