from utils.log_decorator import log
from business_object.recette import Recette
from dao.recette_favorite_dao import RecettesFavoritesDao
from business_object.utilisateur import Utilisateur
from dao.recette_dao import RecetteDao


class SuggestionDao:
    """Classe contenant les méthodes pour faire une suggestion de recette à l'utilisateur"""

    @log
    def obtenirSuggestionRecette(self, utilisateur: Utilisateur) -> Recette:
        """
        Suggerer à l'utilisateur une recette n'étant pas dans ses recettes favorites,
        sans ingredient non désiré et avec au moins un ingredient favori

        Parameters
        ----------
        utilisateur : Utilisateur

        Returns
        -------
        recette : Recettes
            renvoie une recettes à l'utilisateur
        """
        # On récupère toutes les recettes de la bdd
