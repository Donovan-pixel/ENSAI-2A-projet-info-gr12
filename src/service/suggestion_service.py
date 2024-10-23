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
git add src