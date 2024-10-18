from utils.log_decorator import log
from business_object.recette import Recette
from dao.recette_dao import RecetteDao
from src.business_object.ingredient import Ingredient


class RecetteService:
    """Classe contenant les méthodes de service des Recettes"""

    @log
    def ajouterNouvelleRecette(self, recette: Recette) -> bool:
        """Ajout d'une nouvelle recette à partir de ses attributs"""
        nouvelle_recette = Recette(
            idRecette=recette.idRecette,
            titre=recette.titre,
            ingredientQuantite=recette.ingredientQuantite,
            consignes=recette.consignes,
            categorie=recette.categorie,
            origine=recette.origine,
        )

        if RecetteDao().ajouterRecette(nouvelle_recette):
            return True
        else:
            return None

    @log
    def afficherRecette(self, recette: Recette) -> str:
        """Afficher les détails d'une recette
        Parameters
        ----------
        recette : Recette
        un objet de type recette
        Return
        ------
        une chaîne de caractères
        """
        return (
            f"Recette({self.idRecette}, {self.titre}, {self.ingredientQuantite}, {self.consignes},"
            "{self.categorie},"
            "{self.origine}"
        )

    @log
    def obtenirRecettesparLettre(self, lettre) -> list[Recette]:
        """Afficher toutes les recettes qui comportent les ingrédients dans la liste
        Parameters
        ----------
        lettre : str
        Return
        ------
        une liste de recette qui commence par cette lettre
        """
        return RecetteDao().obtenirRecettesparLettre(lettre=lettre)

    @log
    def obtenirRecettesParIngredient(self, ingredient: Ingredient) -> list[Recette]:
        """obtenir la liste des recettes contenant un ingrédient spécifique
        Parameters
        ----------
        ingredient : Ingredient
        Return
        -----
        Recette : une liste d'objets de type Recette
        """
        return RecetteDao().obtenirRecettesParIngredient(ingredient)

    @log
    def obtenirRecettesParIngrédients(self, ingredients: list[Ingredient]) -> list[Recette]:
        """obtenir la liste des recettes contenant deux ou plusieurs ingrédients
        Parameters
        ----------
        list : liste d'objets de type d'ingrédients
        Return
        ------
        liste d'objets de type Recette
        """
        return RecetteDao().obtenirRecettesParIngrédients()

    @log
    def obtenirRecettesParCategorie(self, categorie: str) -> list[Recette]:
        """Obtenir la liste des recettes qui sont d'une catégorie donnée
        Parameters
        ---------
        categorie : str
        Return
        -----
        list : liste d'objets de type Recette
        """
        return RecetteDao().obtenirRecettesParCategorie(categorie=categorie)
