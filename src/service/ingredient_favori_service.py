from utils.log_decorator import log

from business_object.ingredient import Ingredient
from dao.ingredient_favori_dao import IngredientFavoriDao
from business_object.utilisateur import Utilisateur


class IngredientFavorisService:
    """Classe contenant les méthodes de service des Ingrédients favoris"""

    @log
    def ajouterIngredientFavori(self, nom_ingredient, utilisateur: Utilisateur) -> bool:
        """Ajout d'un ingrédient favori d'un utilisateur"""

        nouvel_ingredient_favori = Ingredient(
            nom=nom_ingredient,
        )

        return IngredientFavoriDao().ajouterIngredientFavori(nouvel_ingredient_favori, utilisateur)

    @log
    def obtenirIngredientsFavoris(self, utilisateur: Utilisateur) -> list[Ingredient]:
        """Lister tous les ingrédients favoris d'un utilisateur"""

        return IngredientFavoriDao().obtenirIngredientsFavoris(utilisateur)

    @log
    def supprimerIngredientFavori(self, nom_ingredient, utilisateur: Utilisateur) -> bool:
        """Supprimer un ingredient favori"""

        ingredient = Ingredient(
            nom=nom_ingredient,
        )
        return IngredientFavoriDao().supprimerIngredientFavori(ingredient, utilisateur)
