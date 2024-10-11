import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.utilisateur import Utilisateur
from business_object.recette import Recette


class RecettesFavoritesDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux recettes favorites des utilisateurs"""

    @log
    def ajouter_recette_favorite(self, utilisateur, recette) -> bool:
        """Ajout d'une recette comme favorite pour un utilisateur

        Parameters
        ----------
        utilisateur : Utilisateur
        recette : Recette

        Returns
        -------
        created : bool
            True si l'ajout est un succès
            False sinon
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO recettes_favorites(id_meal, id_user) VALUES        "
                        "(%(idRecette)s, %(idUtilisateur)s             "
                        {
                            "idRecette": recette.idRecette,
                            "idUtilisateur": utilisateur.idUtilisateur,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        created = False
        if res:
            created = True

        return created

    @log
    def supprimer_recette_favorite(self, utilisateur, recette) -> bool:
        """Suppression d'une recette favorite pour un utilisateur

        Parameters
        ----------
        utilisateur : Utilisateur
        recette : Recette

        Returns
        -------
        deleted : bool
            True si la suppression est un succès
            False sinon
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM recettes_favorites      "
                        " WHERE id_meal=%(idRecette)s AND id_user=%(idUtilisateur)s      ",
                        {"idRecette": recette.idRecette,
                        "idUtilisateur": utilisateur.idUtilisateur},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)
            raise

        deleted = False
        if res:
            deleted = True
        return deleted