from utils.log_decorator import log

from business_object.avis import Avis
from dao.avis_dao import AvisDao
from business_object.recette import Recette


class AvisService:
    """Classe contenant les méthodes pour mettre des avis sur une recette"""

    @log
    def ajouterNouvelAvis(self, idUtilisateur, idRecette, note, commentaire) -> bool:
        """Ajout d'un ingrédient à la bdd à partir de son nom"""
        nouvel_avis = Avis(
            idUtilisateur=idUtilisateur,
            idRecette=idRecette,
            note=note,
            commentaire=commentaire,
        )
        return AvisDao().ajouter_avis(nouvel_avis)

    @log
    def obtenirAvisParRecette(self, recette: Recette) -> list[Avis]:
        """Lister tous les avis pour une recette"""
        return AvisDao().obtenirAvisParRecette(recette)

    @log
    def supprimer_avis(self, id_avis: int) -> bool:
        """Supprimer un ingredient"""
        return AvisDao().supprimer_avis(id_avis)

    @log
    def obtenirTousLesAvis(self) -> list[Avis]:
        """Lister tous les avis"""
        return AvisDao().obtenirTousLesAvis()
