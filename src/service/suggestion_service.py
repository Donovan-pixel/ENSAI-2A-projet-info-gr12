from utils.log_decorator import log

from business_object.recette import Recette
from business_object.utilisateur import Utilisateur

from dao.recette_favorite_dao import RecettesFavoritesDao
from dao.recette_dao import RecetteDao
from dao.ingredient_non_desire_dao import IngredientNonDesireDao
from dao.ingredient_favori_dao import IngredientFavoriDao


class SuggestionService:
    """Classe contenant les méthodes pour faire une suggestion de recette à l'utilisateur"""

    @log
    def obtenirSuggestionRecette(self, utilisateur: Utilisateur) -> list[Recette]:
        """
        Suggerer à l'utilisateur des recettes n'étant pas dans ses recettes favorites,
        sans ingredient non désiré et avec au moins un ingredient favori

        Parameters
        ----------
        utilisateur : Utilisateur

        Returns
        -------
        recette : Recettes
            renvoie une recettes à l'utilisateur
        """
        # On récupère toutes les recettes de la bdd
        recettes = RecetteDao().obtenirToutesLesRecettes()

        # On récupère les recettes favorites de l'Utilisateur
        recettes_favorites = RecettesFavoritesDao().obtenirRecettesFavorites(utilisateur)

        # On récupère les ingredients favoris de l'Utilisateur
        ingredients_favoris = IngredientFavoriDao().obtenirIngredientsFavoris(utilisateur)

        # On récupère les ingrédients non désirés de l'Utilisateur
        ingredients_non_desires = IngredientNonDesireDao().obtenirIngredientsNonDesires(utilisateur)

        recettes_suggerees = [
            recette
            for recette in recettes
            if recette not in recettes_favorites
            and not (set(ingredients_non_desires) & set(recette.ingredientQuantite.keys()))
            and (set(ingredients_favoris) & set(recette.ingredientQuantite.keys()))
        ]
        return recettes_suggerees

        # On retire les recettes favorites de la liste des recettes
        recettes_filtrees = [recette for recette in recettes if recette not in recettes_favorites]

        # On retire les recettes contenant un ingredient non désiré
        recettes_filtrees_bis = []
        for ingredient_non_desire in ingredients_non_desires:
            nom_ingredient = ingredient_non_desire.nom
            for recette in recettes_filtrees:
                if (
                    nom_ingredient not in set(recette.ingredientQuantite.keys())
                    and recette not in recettes_filtrees_bis
                ):
                    recettes_filtrees_bis.append(recette)

        # On récupère les ingredients favoris de l'Utilisateur
        ingredients_favoris = IngredientFavoriDao().obtenirIngredientsFavoris(utilisateur)
        print(ingredients_favoris[0].nom)
        print(set(recettes_filtrees[0].ingredientQuantite.keys()))

        # On retire les recettes ne contenant aucun ingredient favori
        recettes_suggerees = []
        for ingredient_favori in ingredients_favoris:
            nom_ingredient = ingredient_favori.nom
            for recette in recettes_filtrees_bis:
                if (
                    nom_ingredient in set(recette.ingredientQuantite.keys())
                    and recette not in recettes_suggerees
                ):
                    recettes_suggerees.append(recette)

        print(recettes_suggerees)

        return recettes_suggerees
