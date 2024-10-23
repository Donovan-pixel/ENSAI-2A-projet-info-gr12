from utils.log_decorator import log
from dao.liste_de_course_dao import ListeDeCourseDAO
from business_object.liste_de_course import ListeDeCourses


class ListeDeCoursesService:
    """Classe contenant les méthodes de service des Listes de Courses"""

    @log
    def creerListeDeCourses(self, id_utilisateur) -> ListeDeCourses:
        """
        Création d'une nouvelle liste de courses pour un utilisateur.

        Parameters
        ----------
        id_utilisateur : int
            L'identifiant de l'utilisateur.

        Returns
        -------
        ListeDeCourses : ListeDeCourses
            Retourne l'objet ListeDeCourses créé, ou None en cas d'échec.
        """
        nouvelle_liste = ListeDeCourses(idUtilisateur=id_utilisateur)
        return nouvelle_liste if ListeDeCourseDAO().creerListeDeCourses(nouvelle_liste) else None

    @log
    def ajouterUnIngredient(self, id_utilisateur, ingredient_quantite) -> bool:
        """
        Ajoute des ingrédients à la liste de courses d'un utilisateur.

        Parameters
        ----------
        id_utilisateur : int
            L'identifiant de l'utilisateur.
        ingredient_quantite : dict
            Un dictionnaire contenant les ingrédients et leurs quantités.

        Returns
        -------
        bool
            Retourne True si l'ajout est réussi, False sinon.
        """
        return ListeDeCourseDAO().ajouterUnIngredient(id_utilisateur, ingredient_quantite)

    @log
    def retirerUnIngredient(self, id_utilisateur, ingredient) -> bool:
        """
        Retire un ingrédient de la liste de courses d'un utilisateur.

        Parameters
        ----------
        id_utilisateur : int
            L'identifiant de l'utilisateur.
        ingredient : Ingredient
            L'ingrédient à retirer.

        Returns
        -------
        bool
            Retourne True si le retrait est réussi, False sinon.
        """
        return ListeDeCourseDAO().retirerUnIngredient(id_utilisateur, ingredient)

    @log
    def listerTous(self, id_utilisateur) -> str:
        """
        Afficher toutes les listes de courses d'un utilisateur sous forme de tableau.

        Parameters
        ----------
        id_utilisateur : int
            L'identifiant de l'utilisateur.

        Returns
        -------
        str
            Retourne une chaîne de caractères formatée pour afficher les listes de courses.
        """
        listes = ListeDeCourseDAO().listerTous(id_utilisateur)
        if not listes:
            return "Aucune liste de courses disponible pour cet utilisateur."

        entetes = ["Ingrédient", "Quantité"]
        listes_as_list = []

        for liste in listes:
            for ingredient, quantite in liste.ingredientQuantite.items():
                listes_as_list.append([ingredient, quantite])

        from tabulate import tabulate

        str_listes = "-" * 50
        str_listes += f"\nListes de courses de l'utilisateur {id_utilisateur}\n"
        str_listes += "-" * 50
        str_listes += "\n"
        str_listes += tabulate(tabular_data=listes_as_list, headers=entetes, tablefmt="psql")
        str_listes += "\n"

        return str_listes

    @log
    def obtenirIdListeDeCourses(self, id_utilisateur) -> int:
        """
        Obtenir l'ID de la liste de courses d'un utilisateur.

        Parameters
        ----------
        id_utilisateur : int
            L'identifiant de l'utilisateur.

        Returns
        -------
        int
            Retourne l'ID de la liste de courses.
        """
        return ListeDeCourseDAO().obtenirIdListeDeCourses(id_utilisateur)
