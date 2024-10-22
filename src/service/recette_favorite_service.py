from utils.log_decorator import log
from business_object.recette import Recette
from dao.recette_favorite_dao import RecettesFavoritesDao
from business_object.utilisateur import Utilisateur


class RecetteFavoritesService:
    """Classe contenant les méthodes de service des Recettes favorites"""

    @log
    def ajouter_recette_favorite(self, recette: Recette, utilisateur: Utilisateur) -> bool:
        """Ajout d'une nouvelle recette favorite pour un utilisateur"""

        return RecettesFavoritesDao().ajouter_recette_favorite(recette, utilisateur)

    @log
    def supprimer_recette_favorite(self, recette: Recette, utilisateur: Utilisateur) -> str:
        """Suppression d'une recette favorite pour un utilisateur"""
        return RecettesFavoritesDao().supprimer_recette_favorite(recette, utilisateur)

    @log
    def obtenirRecettesFavorites(self, utilisateur: Utilisateur) -> list[Recette]:
        """Obtenir toutes les recettes favorites d'un utilisateur"""
        return RecettesFavoritesDao().obtenirRecettesFavorites(utilisateur)
