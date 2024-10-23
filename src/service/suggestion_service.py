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

        # On retire les recettes favorites de la liste des recettes
        for recette in recettes_favorites:
            if recette in recettes:
                recettes.remove(recette)

        # On récupère les ingrédeitns non désirés de l'Utilisateur
        ingredients_non_desires = IngredientNonDesireDao().obtenirIngredientsNonDesires(utilisateur)

        # On retire les recettes contenant un ingredient non désiré
        for recette in recettes:
            for ingredient in ingredients_non_desires:
                if ingredient in [
                    list(ingredient.keys())[0] for ingredient in recette.ingredientQuantite
                ]:
                    recettes.remove(recette)

        # On récupère les ingredients favoris de l'Utilisateur
        ingredients_favoris = IngredientFavoriDao().obtenirIngredientsFavoris(utilisateur)

        # On retire les recettes ne contenant aucun ingredient favori
        i = 0
        while i != len(recettes) + 1:
            booleen = False
            keys_recette = [
                list(ingredient.keys())[0] for ingredient in recettes[i].ingredientQuantite
            ]
            for ingredient in keys_recette:
                if ingredient in ingredients_favoris:
                    booleen = True
                    i += 1
            if booleen is False:
                recettes.pop(i)

        return recettes


"""for i in range(len(recettes)):
            booleen = None
            keys_recette = [
                list(ingredient.keys())[0]
                for ingredient in recettes[i].ingredientQuantite
            ]
            for ingredient in keys_recette:
                if ingredient in ingredients_favoris:
                    booleen = True
            if booleen is False:
                recettes.remove(recette)"""

"""
        j = 0
        while j != len(recettes) + 1:
            keys_recette = [
                list(ingredient.keys())[0] for ingredient in recettes[j].ingredientQuantite
            ]
            for ingredient in keys_recette:
                if ingredient in ingredients_favoris:
                    booleen = True
                    j += 1
            if booleen is False:
                recettes.pop(j)"""
