import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.utilisateur import Utilisateur
from business_object.recette import Recette


class RecettesFavoritesDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux recettes favorites des utilisateurs"""

    @log
    def ajouter_recette_favorite(self, recette: Recette, utilisateur: Utilisateur) -> bool:
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
                        """
                        INSERT INTO recettes_favorites(id_meal, id_user)
                        VALUES (%(idRecette)s, %(idUtilisateur)s)
                        RETURNING id_meal;
                        """,
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
    def supprimer_recette_favorite(self, recette: Recette, utilisateur: Utilisateur) -> bool:
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
                        "WHERE id_meal=%(idRecette)s AND id_user=%(idUtilisateur)s;",
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

    @log
    def obtenirRecettesFavorites(self, utilisateur: Utilisateur) -> list[Recette]:
        """
        Lister toutes les recettes favorites d'un utilisateur

        Parameters
        ----------
        utilisateur : Utilisateur

        Returns
        -------
        liste_recettes_favorites : list[Recette]
            renvoie la liste de toutes les recettes favorites de l'utilisateur
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT r.id_meal, r.title, r.category, r.area, r.instructions,
                        mi.id_ingredient, i.nom, mi.quantite
                        FROM recettes_favorites rf
                        JOIN recettes r ON r.id_meal = rf.id_meal
                        LEFT JOIN meals_ingredients mi ON r.id_meal = mi.id_meal
                        LEFT JOIN ingredients i ON mi.id_ingredient = i.id_ingredient
                        WHERE rf.id_user = %(id_user)s;
                        """,
                        {
                            "id_user": utilisateur.idUtilisateur,
                        },
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.exception(e)
            raise

        recettes_favorites_dict = {}
        if res:
            for row in res:
                id_meal = row["id_meal"]
                if id_meal not in recettes_favorites_dict:
                    recettes_favorites_dict[id_meal] = {
                        "idRecette": id_meal,
                        "titre": row["title"],
                        "categorie": row["category"],
                        "origine": row["area"],
                        "consignes": row["instructions"],
                        "ingredientQuantite": {},
                    }

                ingredient = row["nom"]
                quantite = row["quantite"]
                if ingredient:
                    recettes_favorites_dict[id_meal]["ingredientQuantite"][ingredient] = quantite

        liste_recettes_favorites = []
        for recette_data in recettes_favorites_dict.values():
            recette_favorite = Recette(
                idRecette=recette_data["idRecette"],
                titre=recette_data["titre"],
                categorie=recette_data["categorie"],
                origine=recette_data["origine"],
                consignes=recette_data["consignes"],
                ingredientQuantite=recette_data["ingredientQuantite"],
            )
            liste_recettes_favorites.append(recette_favorite)

        return liste_recettes_favorites
