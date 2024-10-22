from utils.log_decorator import log

from business_object.recette import Recette
from business_object.utilisateur import Utilisateur

from dao.recette_favorite_dao import RecettesFavoritesDao
from dao.recette_dao import RecetteDao
from dao.ingredient_non_desire_dao import IngredientNonDesireDAO
from dao.ingredient_favori_dao import IngredientFavoriDao


class SuggestionService:
    """Classe contenant les méthodes pour faire une suggestion de recette à l'utilisateur"""

    @log
    def obtenirSuggestionRecette(self, utilisateur: Utilisateur) -> Recette:
        """
        Suggerer à l'utilisateur une recette n'étant pas dans ses recettes favorites,
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
        recettes.remove(recettes_favorites)

        # On récupère les ingrédeitns non désirés de l'Utilisateur
        ingredients_non_desires = IngredientNonDesireDAO().obtenirIngredientsNonDesires(utilisateur)

        # On retire les recettes contenant un ingredient non désiré
        for recette in recettes:
            for ingredient in ingredients_non_desires:
                if ingredient in recette.ingredientQuantite.keys():
                    recettes.remove(recette)

        # On récupère les ingredients favoris de l'Utilisateur
        ingredients_favoris = IngredientFavoriDao().obtenirIngredientsFavoris(utilisateur)

        # On retire les recettes ne contenant aucun ingredient favori
        for recette in recettes:
            booleen = None
            for ingredient in recette.ingredientQuantite.keys():
                if ingredient in ingredients_favoris:
                    booleen = True
            if booleen is False:
                recettes.remove(recette)
        return recettes
