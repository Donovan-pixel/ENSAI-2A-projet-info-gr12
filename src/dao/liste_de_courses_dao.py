import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection
from business_object.ListeDecourses import ListeDeCourse


class ListeDeCourseDAO(metaclass=Singleton):
    """Classe contenant les méthodes pour interagir avec la base de données pour les listes de courses"""

    # Il faut la supprimer car on ne se servira pas de l'id dans les recherches
    @log
    def trouver_par_id(self, idListeDeCourses) -> ListeDeCourses:
        """trouver une liste de course grace à son id

        Parameters
        ----------
        idListeDeCourses : int
            numéro id de la liste de course que l'on souhaite trouver

        Returns
        -------
        ListeDeCourses : ListeDecourses
            renvoie la liste de course que l'on cherche par id
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                           "
                        "  FROM ListeDeCourses                      "
                        " WHERE idListeDeCourses = %(idListeDeCourses)s;  ",
                        {"idListeDeCourses": idListeDeCourses},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)
            raise

        ListeDecourses = None
        if res:
            ListeDecourses = ListeDecourses(
                idListeDeCourses=res["idListeDeCourses"],
                idUtilisateur=res["idUtilisateur"],
                ingredientQuantite=res["ingredientQuantite"],
            )

        return ListeDecourses

    @log
    def lister_tous(self, idUtlisateur) -> list[ListeDeCourses]:
        """lister toutes les listes de courses du joeur grâce à son id

        Parameters
        ----------
        idUtilisateur : int
              L'identifiant de l'utilisateur

        Returns
        -------
        ListeDeCourses : list[ListeDecourses]
            renvoie la liste de toutes les listes de courses de l'utilisateur dans la base de données
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                              "
                        "  FROM ListeDeCourses                 "
                        "  WHERE idUtilisateur=%(idUtilisateur)s;  ",
                        {"idUtilisateur": idUtilisateur},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)
            raise

        ListeDecourses = []

        if res:
            for row in res:
                ListeDecourse = ListeDecourses(
                    idListeDeCourses=res["idListeDeCourses"],
                    idUtilisateur=res["idUtilisateur"],
                    ingredientQuantite=res["ingredientQuantite"],
                )
                ListeDecourses.append(ListeDecourse)

        return ListeDecourses
    @log
    def ajouter_un_ingredient(self, idUtilisateur,idListeDeCourses,idIngredient,quantite) -> bool:
        """Ajout d'un ingrédient à la liste de courses dans la base de données

        Parameters
        ----------
        idUtilisateur : int
            L'identifiant de l'utilisateur
        idListeDeCourses : int
            L'identifiant de la liste de Courses
        idIngredient : int
            L'identifiant de la liste de Courses
        quantite : float
            Quantité de l'ingrédient

        Returns
        -------
        created : bool
            True si la création est un succès
            False sinon
        """

        res = None

        try:
            with DBConnection().connection as connection:
