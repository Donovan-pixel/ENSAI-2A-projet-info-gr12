import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.avis import Avis
from business_object.recette import Recette


class AvisDao(metaclass=Singleton):
    "Classe contenant les méthodes pour accéder aux avis de la base de données"

    @log
    def ajouter_avis(self, avis:Avis) -> bool:
        """Ajout d'un avis dans la base de données

        Parameters
        ----------
        avis : Avis
            L'avis à ajouter

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
                        "INSERT INTO avis(id_avis, id_user, id_meal, note, commentaire) VALUES"
                        "(%(id_user)s, %(id_meal)s, %(note)s, %(commentaire)s)             "
                        "  RETURNING id_avis;                                              ",
                        {
                            "id_user": avis.idUtilisateur,
                            "id_meal": avis.idRecette,
                            "note": avis.note,
                            "commentaire": avis.commentaire,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.exception(e)
            return False

        return bool(res)

        @log
        def obtenirAvisParRecette(self, recette:Recette) -> list[Avis]:
            """Obtention des avis par recette

            Parameters
            ----------
            recette : Recette 
                La recette à partir de laquelle faire la recherche

            Returns
            -------
            list[Avis]
                Liste contenant les avis correspondant à la recette indiquée
            """

            res = None

            try:
                with DBConnection().connection as connection:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "SELECT * FROM avis" 
                            "JOIN recettes ON recettes.id_meal = avis.id_meal"
                            "WHERE id_meals = %(id_recette)s;", 
                            {
                                "id_recette": recette.id_meal,
                            },
                        )
                        res = cursor.fetchall()
            except Exception as e:
                logging.exception(e)
                return []

            liste = []

            if res:
                for row in res:
                    avis = Avis(
                        id_avis = res["id_avis"],
                        id_user = res["id_user"],
                        id_meal = res["id_meal"],
                        note = res["note"],
                        commentaire = res["commentaire"]
                    )
                    liste.append(avis)

            return liste
    
    @log
    def supprimer_avis(self, avis: Avis) -> bool:
        """Suppression d'un avis dans la base de données

        Parameters
        ----------
        avis : Avis
            L'avis à supprimer

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
                        "DELETE FROM avis WHERE id_avis = %(id_avis)s;",
                        {"id_avis": avis.idAvis},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.exception(e)
            return False

        return res > 0

            

