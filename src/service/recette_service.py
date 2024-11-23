import logging

from utils.log_decorator import log
from business_object.recette import Recette
from dao.recette_dao import RecetteDao
from business_object.ingredient import Ingredient


class RecetteService:
    """Classe contenant les méthodes de service des Recettes"""

    @log
    def ajouterNouvelleRecette(self, recette: dict) -> bool:
        """Ajout d'une nouvelle recette à partir de ses attributs"""

        if isinstance(recette, dict) and isinstance(recette.get("titre"), str):
            titre = recette.get("titre")
            ingredientQuantite = recette.get("ingredientQuantite")
            consignes = recette.get("consignes")
            categorie = recette.get("categorie")
            origine = recette.get("origine")

            if not all([titre, ingredientQuantite, consignes, categorie, origine]):
                logging.error("Recette invalide: certains champs sont manquants ou vides")
                return False

            nouvelle_recette = Recette(
                titre=titre,
                ingredientQuantite=ingredientQuantite,
                consignes=consignes,
                categorie=categorie,
                origine=origine,
            )
        else:
            logging.error(
                """
                Format de recette invalide: le format attendu est un
                dictionnaire avec un titre non vide.
                """
            )
            return False

        try:
            success = RecetteDao().ajouterRecette(nouvelle_recette)
            if success:
                logging.info(f"Recette '{nouvelle_recette.titre}' ajoutée avec succès.")
            else:
                logging.warning(
                    f"L'ajout de la recette '{nouvelle_recette.titre}' a échoué sans exception."
                )
            return success
        except Exception as e:
            logging.error(f"Erreur lors de l'ajout de la recette '{nouvelle_recette.titre}': {e}")
            return False

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
    def obtenirRecettesParIngredients(self, ingredients: list[Ingredient]) -> list[Recette]:
        """obtenir la liste des recettes contenant deux ou plusieurs ingrédients
        Parameters
        ----------
        list : liste d'objets de type d'ingrédients
        Return
        ------
        liste d'objets de type Recette
        """
        return RecetteDao().obtenirRecettesParIngredients(ingredients)

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
        """Obtention de toutes les catégories de recettes de la base de données"""
        return RecetteDao().obtenirToutesLesCategories()
