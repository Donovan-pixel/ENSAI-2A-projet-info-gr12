from unittest.mock import MagicMock

from service.suggestion_service import SuggestionService
from business_object.utilisateur import Utilisateur
from business_object.ingredient import Ingredient
from business_object.recette import Recette
from dao.recette_dao import RecetteDao
from dao.recette_favorite_dao import RecettesFavoritesDao
from dao.ingredient_non_desire_dao import IngredientNonDesireDao
from dao.ingredient_favori_dao import IngredientFavoriDao

liste_utilisateur = [
    Utilisateur(idUtilisateur=1, pseudo="jp", role="Utilisateur", motDePasse="1234"),
    Utilisateur(idUtilisateur=2, pseudo="lea", role="Utilisateur", motDePasse="0000"),
    Utilisateur(idUtilisateur=3, pseudo="gg", role="Utilisateur", motDePasse="abcd"),
]

liste_ingredients = [
    Ingredient(nom="Tomate", idIngredient=12),
    Ingredient(nom="Carotte", idIngredient=13),
    Ingredient(nom="Avocat", idIngredient=34),
    Ingredient(nom="pomme", idIngredient=6),
    Ingredient(nom="banane", idIngredient=34),
]

liste_ingredients_favoris = [Ingredient(nom="Tomate", idIngredient=12)]

liste_ingredients_non_desires = [Ingredient(nom="Carotte", idIngredient=13)]

recette_favorites = [
    Recette(
        idRecette=3,
        titre="Recette Test",
        ingredientQuantite=[{"pommes": 2}, {"Avocat": 1}],
        consignes="Couper et cuire",
        categorie="Dessert",
        origine="France",
    ),
]

recette = [
    Recette(
        idRecette=1,
        titre="Recette Test 1",
        ingredientQuantite=[{"pomme": 2}, {"Tomate": 2}],
        consignes="Couper et cuire",
        categorie="Dessert",
        origine="France",
    ),
    Recette(
        idRecette=2,
        titre="Recette Test 2",
        ingredientQuantite={"bananes": 3},
        consignes="Mixer",
        categorie="Boisson",
        origine="Brésil",
    ),
    Recette(
        idRecette=3,
        titre="Recette Test",
        ingredientQuantite=[{"pommes": 2}, {"Avocat": 1}],
        consignes="Couper et cuire",
        categorie="Dessert",
        origine="France",
    ),
    Recette(
        idRecette=4,
        titre="Recette Test 3",
        ingredientQuantite=[{"bananes": 3}, {"Carotte": 3}],
        consignes="Mixer",
        categorie="Boisson",
        origine="Brésil",
    ),
    Recette(
        idRecette=5,
        titre="Recette Test 4",
        ingredientQuantite=[{"Carotte": 2}, {"Tomate": 2}],
        consignes="Couper et cuire",
        categorie="Dessert",
        origine="France",
    ),
]

Recettes_proposées = [
    Recette(
        idRecette=1,
        titre="Recette Test 1",
        ingredientQuantite=[{"pomme": 2}, {"Tomate": 2}],
        consignes="Couper et cuire",
        categorie="Dessert",
        origine="France",
    ),
]


def test_obtenirSuggestionRecette():
    """Vérifie que la fonction renvoie bien une liste de recettes
    vérifiant les critères de l'utilisateur"""

    # GIVEN
    utilisateur = liste_utilisateur[0]
    RecetteDao().obtenirToutesLesRecettes = MagicMock(return_value=recette)
    RecettesFavoritesDao().obtenirRecettesFavorites = MagicMock(return_value=recette_favorites)
    IngredientFavoriDao().obtenirIngredientsFavoris = MagicMock(
        return_value=liste_ingredients_favoris
    )
    IngredientNonDesireDao().obtenirIngredientsNonDesires = MagicMock(
        return_value=liste_ingredients_non_desires
    )

    # WHEN
    res = SuggestionService().obtenirSuggestionRecette(utilisateur)

    # THEN
    assert res == Recettes_proposées


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
