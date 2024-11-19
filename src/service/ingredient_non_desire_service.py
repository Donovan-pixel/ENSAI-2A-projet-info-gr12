from utils.log_decorator import log

from business_object.ingredient import Ingredient
from dao.ingredient_non_desire_dao import IngredientNonDesireDao
from dao.ingredient_dao import IngredientDao
from business_object.utilisateur import Utilisateur


class IngredientNonDesireService:
    """Classe contenant les méthodes de service des Ingrédients non desirés"""

    @log
    def ajouterIngredientNonDesire(self, nom_ingredient, utilisateur: Utilisateur) -> bool:
        """Ajout d'un ingrédient non désiré d'un utilisateur"""

        id_ingredient = IngredientDao().obtenirIdParNom(nom_ingredient)

        nouvel_ingredient_non_desire = Ingredient(
            idIngredient=id_ingredient,
            nom=nom_ingredient,
        )

        return IngredientNonDesireDao().ajouterIngredientNonDesire(
            nouvel_ingredient_non_desire, utilisateur
        )

    @log
    def obtenirIngredientsNonDesires(self, utilisateur: Utilisateur) -> list[Ingredient]:
        """Lister tous les ingrédients non desirés d'un utilisateur"""

        return IngredientNonDesireDao().obtenirIngredientsNonDesires(utilisateur)

    @log
    def supprimerIngredientNonDesire(self, nom_ingredient, utilisateur) -> bool:
        """Supprimer un ingredient non desiré"""

        id_ingredient = IngredientDao().obtenirIdParNom(nom_ingredient)

        ingredient = Ingredient(
            idIngredient=id_ingredient,
            nom=nom_ingredient,
        )

        return IngredientNonDesireDao().supprimerIngredientNonDesire(ingredient, utilisateur)
