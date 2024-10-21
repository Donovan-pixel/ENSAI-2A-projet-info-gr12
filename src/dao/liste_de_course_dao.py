import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection
from business_object.liste_de_course import ListeDeCourses


class ListeDeCourseDAO(metaclass=Singleton):
    """Classe contenant les méthodes pour interagir avec la liste de courses de la base"""

    @log
    def creerListeDeCourses(self, listeDeCourse) -> bool:
        """Création d'une nouvelle liste de courses dans la base de données.

        Parameters
        ----------
        listeDeCourse : ListeDeCourses
             L'objet ListeDeCourses contenant les informations de la liste à créer.

        Returns
        -------
        created : bool
        True si la création est un succès, False sinon.
        """
        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO ListeDeCourses(idUtilisateur, IngredientQuantite) "
                        "VALUES (%(idUtilisateur)s, %(ingredientQuantite)s) "
                        "RETURNING idListeDeCourses;",
                        {
                            "idUtilisateur": listeDeCourse.idUtilisateur,
                            "ingredientQuantite": listeDeCourse.ingredientQuantite,
                        },
                    )
                res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        created = False
        if res:
            listeDeCourse.idListeDeCourses = res["idListeDeCourses"]
            created = True

        return created

    @log
    def listerTous(self, idUtilisateur) -> list[ListeDeCourses]:
        """lister toutes les listes de courses de l'utilisateur grâce à son id

        Parameters
        ----------
        idUtilisateur : int
              L'identifiant de l'utilisateur

        Returns
        -------
        ListeDeCourses : list[ListeDecourses]
            renvoie la liste de toutes les listes de courses de l'utilisateur
            dans la base de données.
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
                Listecourses = ListeDecourses(
                    idListeDeCourses=res["idListeDeCourses"],
                    idUtilisateur=res["idUtilisateur"],
                    ingredientQuantite=res["ingredientQuantite"],
                )
                ListeDecourses.append(Listecourses)

        return ListeDecourses

    @log
    def ajouterUnIngredient(self, idListeDeCourses, idIngredient, quantite) -> bool:
        """Ajoute ou met à jour un ingrédient dans la liste de courses.

        Parameters
        ----------

        idIngredient : int
            L'identifiant de l'ingrédient.
        quantite : float
            La quantité à ajouter ou mettre à jour.
        idListeDeCourses : int
            L'identifiant de la liste de courses.


        Returns
        -------
        bool
            True si l'ajout/mise à jour est un succès, False sinon.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Récupérer la liste de courses depuis la base de données
                    cursor.execute(
                        "SELECT * "
                        "FROM ListeDeCourses "
                        "WHERE idListeDeCourses = %(idListeDeCourses)s;",
                        {"idListeDeCourses": idListeDeCourses},
                    )
                    res = cursor.fetchone()

                    if res:
                        # Instancier un objet ListeDeCourses avec les données récupérées
                        liste_de_courses = ListeDeCourses(
                            idListeDeCourses=res["idListeDeCourses"],
                            idUtilisateur=res["idUtilisateur"],
                            ingredientQuantite=res["ingredientQuantite"],
                        )

                        # Utiliser la méthode ajouterIngredient de l'objet ListeDeCourses
                        liste_de_courses.ajouterIngredient(idIngredient, quantite)

                        # Mettre à jour la base de données
                        cursor.execute(
                            "UPDATE ListeDeCourses "
                            "SET ingredientQuantite = %(ingredientQuantite)s "
                            "WHERE idListeDeCourses = %(idListeDeCourses)s;",
                            {
                                "ingredientQuantite": liste_de_courses.ingredientQuantite,
                                "idListeDeCourses": idListeDeCourses,
                            },
                        )
                        res = cursor.rowcount
        except Exception as e:
            logging.info(e)

        return res == 1

    @log
    def retirerUnIngredient(self, idListeDeCourses, idIngredient) -> bool:
        """Retire un ingrédient de la liste de courses.
        Parameters
        ----------
        idListeDeCourses : int
            L'identifiant de la liste de courses.
        idIngredient : int
            L'identifiant de l'ingrédient à retirer.

        Returns
        -------
        bool
        True si le retrait est un succès, False sinon.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Obtenir le dictionnaire ingredientQuantite
                    cursor.execute(
                        "SELECT IngredientQuantite "
                        "FROM ListeDeCourses"
                        "WHERE idListeDeCourses = %(idListeDeCourses)s;",
                        {"idListeDeCourses": idListeDeCourses},
                    )
                res = cursor.fetchone()

                if res:
                    # Retirer l'ingrédient du dictionnaire
                    if str(idIngredient) in res:
                        del res[str(idIngredient)]

                        # Mettre à jour la base de données
                        cursor.execute(
                            "UPDATE ListeDeCourses "
                            "SET ingredientQuantite = %(ingredientQuantite)s "
                            "WHERE idListeDeCourses = %(idListeDeCourses)s;",
                            {"ingredientQuantite": res, "idListeDeCourses": idListeDeCourses},
                        )
                        res = cursor.rowcount

        except Exception as e:
            logging.info(e)

        return res == 1
