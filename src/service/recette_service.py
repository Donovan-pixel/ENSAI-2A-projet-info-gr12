from utils.log_decorator import log
from business_object.recette import Recette
from dao.recette_dao import RecetteDao
from business_object.ingredient import Ingredient


class RecetteService:
    """Classe contenant les méthodes de service des Recettes"""

    @log
    def ajouterNouvelleRecette(self, recette: Recette) -> bool:
        """Ajout d'une nouvelle recette à partir de ses attributs"""

        # Vérifier si 'recette' est un dictionnaire et le convertir en objet Recette si nécessaire
        if isinstance(recette, dict):
            recette = Recette(
                titre=recette.get("titre"),
                ingredientQuantite=recette.get("ingredientQuantite"),
                consignes=recette.get("consignes"),
                categorie=recette.get("categorie"),
                origine=recette.get("origine"),
            )

        # Maintenant que nous avons un objet Recette, nous pouvons l'utiliser
        nouvelle_recette = Recette(
            titre=recette.titre,
            ingredientQuantite=recette.ingredientQuantite,
            consignes=recette.consignes,
            categorie=recette.categorie,
            origine=recette.origine,
        )

        if 
        return RecetteDao().ajouterRecette(nouvelle_recette)

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
            f"Recette({recette.titre}, {recette.ingredientQuantite}, {recette.consignes}, "
            f"{recette.categorie}, "
            f"{recette.origine})"
        )

    @log
    def obtenirToutesLesRecettes(self) -> list[Recette]:
        """Récupère et retourne toutes les recettes disponibles dans la base de données.

        Returns:
        -------
        list[Recette]:
            Liste des recettes récupérées.
        """
        return RecetteDao().obtenirToutesLesRecettes()

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
    def obtenirRecettesParIngredients(self, ingredients: list[Ingredient]) -> list[Recette]:
        """obtenir la liste des recettes contenant deux ou plusieurs ingrédients
        Parameters
        ----------
        list : liste d'objets de type d'ingrédients
        Return
        ------
        liste d'objets de type Recette
        """
        return RecetteDao().obtenirRecettesParIngredients()

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

    @log
    def obtenirToutesLesCategories(self):
        """Obtenir la liste de toutes les catégories de recettes disponibles"""
        return RecetteDao().obtenirToutesLesCategories()
