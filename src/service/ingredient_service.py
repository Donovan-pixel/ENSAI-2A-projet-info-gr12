from utils.log_decorator import log

from business_object.ingredient import Ingredient
from dao.ingredient_dao import IngredientDao


class IngredientService:
    """Classe contenant les méthodes de service des Ingrédients"""

    @log
    def ajouterNouvelIngredient(self, nom) -> bool:
        """Ajout d'un ingrédient à la bdd à partir de son nom"""
        nouvel_ingredient = Ingredient(
            nom=nom,
        )
        return IngredientDao().ajouterIngredient(nouvel_ingredient)

    @log
    def obtenirTousLesIngredients(self) -> list[Ingredient]:
        """Lister tous les ingrédients"""
        return IngredientDao().obtenirTousLesIngredients()

    @log
    def supprimer(self, ingredient) -> bool:
        """Supprimer un ingredient"""
        return IngredientDao().supprimerIngredient(ingredient)

    @log
    def obtenirIdPArNom(self, nom) -> int:
        """Récupérer l'id d'un ingrédient par son nom"""
        return IngredientDao().obtenirIdParNom(nom)
