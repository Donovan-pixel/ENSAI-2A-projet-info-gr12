from utils.log_decorator import log

from business_object.ingredient import Ingredient
from dao.ingredient_non_desire_dao import IngredientNonDesireDAO
from business_object.utilisateur import Utilisateur


class IngredientNonDesireService:
    """Classe contenant les méthodes de service des Ingrédients non desirés"""

    @log
    def ajouterIngredientNonDesire(self, nom_ingredient, utilisateur: Utilisateur) -> bool:
        """Ajout d'un ingrédient favori d'un utilisateur"""
        nouvel_ingredient_non_desire = Ingredient(
            nom=nom_ingredient,
        )
        return IngredientNonDesireDAO().ajouterIngredientNonDesire(
            nouvel_ingredient_non_desire, utilisateur
        )

    @log
    def obtenirIngredientsNonDesires(self, utilisateur: Utilisateur) -> list[Ingredient]:
        """Lister tous les ingrédients non desirés d'un utilisateur"""
        return IngredientNonDesireDAO().obtenirIngredientsNonDesires(utilisateur)

    @log
    def supprimerIngredientNonDesire(self, nom_ingredient, utilisateur) -> bool:
        """Supprimer un ingredient non desiré"""
        ingredient = Ingredient(
            nom=nom_ingredient,
        )
        return IngredientNonDesireDAO().supprimerIngredientNonDesire(ingredient)
