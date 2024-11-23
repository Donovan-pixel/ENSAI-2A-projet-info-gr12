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
        resultat = ListeDeCourseDAO().creerListeDeCourses(id_utilisateur)
        if not resultat:
            return None  # Retourne None en cas d'échec
        return resultat

    @log
    def ajouterUnIngredient(self, idUtilisateur, idIngredient, quantite) -> bool:
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
        return ListeDeCourseDAO().ajouterUnIngredient(idUtilisateur, idIngredient, quantite)

    @log
    def retirerUnIngredient(self, idUtilisateur, idIngredient) -> bool:
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
        return ListeDeCourseDAO().retirerUnIngredient(idUtilisateur, idIngredient)

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
        liste_de_course = ListeDeCourseDAO().listerTous(id_utilisateur)

        return liste_de_course

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
