from utils.log_decorator import log

from business_object.ingredient import Ingredient
from dao.ingredient_dao import IngredientDao


class IngredientService:
    """Classe contenant les méthodes de service des Ingrédients"""

    @log
    def ajouterNouvelIngredient(self, idIngredient, nom) -> Ingredient:
        """Création d'un ingrédient à partir de ses attributs"""

        nouvel_ingredient = Ingredient(
            idIngredient=idIngredient,
            nom=nom,
        )

        return nouvel_ingredient if IngredientDao().ajouterIngredient(nouvel_ingredient) else None

    @log
    def obtenirTousLesIngredients(self) -> list[Ingredient]:
        """Lister tous les ingrédients"""
        return IngredientDao().obtenirTousLesIngredients()

    @log
    def supprimer(self, ingredient) -> bool:
        """Supprimer un ingredient"""
        return IngredientDao().supprimerIngredient(ingredient)
