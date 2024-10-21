from utils.log_decorator import log

from business_object.ingredient import Ingredient
from dao.ingredient_dao import IngredientDao


class IngredientService:
    """Classe contenant les méthodes de service des Ingrédients"""

    @log
    def ajouterNouvelIngredient(self, nom_ingredient) -> bool:
        """Ajout d'un ingrédient à la bdd à partir de son nom"""
        return IngredientDao().ajouterIngredient(nom_ingredient)

    @log
    def obtenirTousLesIngredients(self) -> list[Ingredient]:
        """Lister tous les ingrédients"""
        return IngredientDao().obtenirTousLesIngredients()

    @log
    def supprimer(self, ingredient) -> bool:
        """Supprimer un ingredient"""
        return IngredientDao().supprimerIngredient(ingredient)
