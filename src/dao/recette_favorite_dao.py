import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.utilisateur import Utilisateur
from business_object.recette import Recette


class RecettesFavoritesDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux recettes favorites des utilisateurs"""

    @log
    def ajouter_recette_favorite(self, recette:Recette, utilisateur:Utilisateur) -> bool:
        """Ajout d'une recette favorite pour un utilisateur

        Parameters
        ----------
        recette : Recette
            La recette qu'il faut ajouter aux favorites
        utilisateur : Utilisateur
            L'utilisateur qui en fait la demande
        
        Returns
        -------
        bool :
            True si l'ajout est un succès
            False sinon
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO recettes_favorite(id_meal, id_user)"
                        "VALUES (%(idRecette)s, %(idUtilisateur)s       "
                        "RETURNING id_meal;                             ",
                        {
                            "idRecette": recette.idRecette,
                            "idUtilisateur": utilisateur.idUtilisateur,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.exception(e)
            raise

        return bool(res)

    @log
    def supprimer_recette_favorite(self, recette:Recette, utilisateur:Utilisateur) -> bool:
        """Suppression d'une recette favorite pour un utilisateur

        Parameters
        ----------
        recette : Recette
            La recette à supprimer des favorites
        utilisateur : Utilisateur
            L'utilisateur qui en fait la demande
        
        Returns
        -------
        bool :
            True si la suppression est un succès
            False sinon
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM recettes_favorites                             "
                        " WHERE id_meal=%(idRecette)s AND id_user=%(idUtilisateur)s;",
                        {
                            "idRecette": recette.idRecette,
                            "idUtilisateur": utilisateur.idUtilisateur,
                        },
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.exception(e)
            raise

        return res > 0