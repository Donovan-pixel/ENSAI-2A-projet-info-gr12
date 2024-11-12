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
        sans ingredient non désiré et avec au moins un ingredient favori.

        Parameters
        ----------
        utilisateur : Utilisateur

        Returns
        -------
        recettes_suggerees : list[Recette]
            La liste des recettes suggérées pour l'utilisateur.
        """
        recettes = RecetteDao().obtenirToutesLesRecettes()

        recettes_favorites = RecettesFavoritesDao().obtenirRecettesFavorites(utilisateur)

        ingredients_favoris = IngredientFavoriDao().obtenirIngredientsFavoris(utilisateur)
        ingredients_non_desires = IngredientNonDesireDao().obtenirIngredientsNonDesires(utilisateur)

        if not (ingredients_favoris and ingredients_non_desires):
            print("Aucun ingrédient favori et non désirés trouvés pour suggérer des recettes.")
            return []

        recettes_filtrees = [recette for recette in recettes if recette not in recettes_favorites]

        recettes_filtrees_bis = []
        for recette in recettes_filtrees:
            if not any(
                ingredient_non_desire.nom in recette.ingredientQuantite
                for ingredient_non_desire in ingredients_non_desires
            ):
                recettes_filtrees_bis.append(recette)

        recettes_suggerees = []
        for recette in recettes_filtrees_bis:
            if any(
                ingredient_favori.nom in recette.ingredientQuantite
                for ingredient_favori in ingredients_favoris
            ):
                recettes_suggerees.append(recette)

        return recettes_suggerees
