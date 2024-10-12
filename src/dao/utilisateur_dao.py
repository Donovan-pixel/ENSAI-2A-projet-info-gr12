import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.utilisateur import Utilisateur


class UtilisateurDao(metaclass=Singleton):
    """Classe contenant les méthodes pour gérer les utilisateurs de la base de données"""

    @log
    def creer(self, utilisateur) -> bool:
        """Creation d'un utilisateur dans la base de données

        Parameters
        ----------
        utilisateur : Utilisateur
            L'utilisateur à créer

        Returns
        -------
        created : bool
            True si la création est un succès
            False sinon
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO users(pseudo, mot_de_Passe, role) VALUES"
                        "(%(pseudo)s, %(motDePasse)s, %(role)s)              "
                        "RETURNING id_user;                                ",
                        {
                            "pseudo": utilisateur.pseudo,
                            "motDePasse": utilisateur.motDePasse,
                            "role": utilisateur.role,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        created = False

        if res:
            utilisateur.idUtilisateur = res["idUtilisateur"]
            created = True

        return created

    @log
    def trouver_par_id(self, idUtilisateur) -> Utilisateur:
        """trouver un utilisateur grâce à son id

        Parameters
        ----------
        idUtilisateur : int
            numéro id de l'utilisateur que l'on souhaite trouver

        Returns
        -------
        utilisateur : Utilisateur
            renvoie l'utilisateur que l'on cherche par id
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                           "
                        "  FROM users                      "
                        " WHERE id_user = %(idUtilisateur)s;  ",
                        {"idUtilisateur": idUtilisateur},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)
            raise

        utilisateur = None
        if res:
            utilisateur = Utilisateur(
                pseudo=res["pseudo"],
                motDePasse=res["motDePasse"],
                role=res["role"],
                idUtilisateur=res["idUtilisateur"],
            )

        return utilisateur

    @log
    def lister_tous(self) -> list[Utilisateur]:
        """lister tous les utilisateurs

        Parameters
        ----------
        None

        Returns
        -------
        liste_utilisateurs : list[Utilisateurs]
            renvoie la liste de tous les utilisateurs dans la base de données
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                              "
                        "  FROM users;                        "
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)
            raise

        liste_utilisateur = []

        if res:
            for row in res:
                utilisateur = Utilisateur(
                    idUtilisateur=row["id_user"],
                    pseudo=row["pseudo"],
                    motDePasse=row["mot_de_Passe"],
                    role=row["role"],
                )

                liste_utilisateur.append(utilisateur)

        return liste_utilisateur

    @log
    def modifier(self, utilisateur: Utilisateur) -> bool:
        """Modification d'un utilisateur dans la base de données

        Parameters
        ----------
        utilisateur : Utilisateur

        Returns
        -------
        created : bool
            True si la modification est un succès
            False sinon
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE users                                 "
                        "   SET pseudo             = %(pseudo)s,            "
                        "       mot_de_Passe         = %(motDePasse)s,      "
                        "       role               = %(role)s,              "
                        " WHERE id_user = %(idUtilisateur)s;                ",
                        {
                            "pseudo": utilisateur.pseudo,
                            "motDePasse": utilisateur.motDePasse,
                            "role": utilisateur.role,
                            "idUtilisateur": utilisateur.idUtilisateur,
                        },
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)

        return res == 1

    @log
    def supprimer(self, utilisateur) -> bool:
        """Suppression d'un utilisateur dans la base de données

        Parameters
        ----------
        utilisateur : Utilisateur
            utilisateur à supprimer de la base de données

        Returns
        -------
            True si le joueur a bien été supprimé
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Supprimer le compte d'un joueur
                    cursor.execute(
                        "DELETE FROM users                  "
                        " WHERE id_user=%(idUtilisateur)s      ",
                        {"idUtilisateur": user.idUtilisateur},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)
            raise

        return res > 0

    @log
    def se_connecter(self, pseudo, motDePasse) -> Utilisateur:
        """se connecter grâce à son pseudo et son mot de passe

        Parameters
        ----------
        pseudo : str
            pseudo de l'utilisateur que l'on souhaite trouver
        motDePasse : str
            mot de passe de l'utilisateur

        Returns
        -------
        utilisateur : Utilisateur
            renvoie l'utilisateur que l'on cherche
        """
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                           "
                        "  FROM users                      "
                        " WHERE pseudo = %(pseudo)s         "
                        "   AND mot_de_Passe = %(motDePasse)s;              ",
                        {
                            "pseudo": utilisateur.pseudo, 
                            "motDePasse": utilisateur.motDePasse
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        utilisateur = None

        if res:
            utilisateur = Utilisateur(
                id_joueur=res["id_joueur"],
                pseudo=res["pseudo"],
                motDePasse=res["motDePasse"],
                role=res["role"],
            )

        return utilisateur
