from utils.log_decorator import log
from business_object.liste_de_course import ListeDeCourses
from dao.liste_de_course_dao import ListeDeCourseDAO


class ListeDeCoursesService:
    """Classe contenant les méthodes de service des Listes de Courses"""

    @log
    def creerListeDeCourses(self, idUtilisateur) -> ListeDeCourses:
        """Création d'une liste de courses"""
        nouvelle_ListeDeCourses = ListeDeCourses(idUtilisateur)

        if ListeDeCourseDAO(nouvelle_ListeDeCourses).creerListeDeCourses:
            return nouvelle_ListeDeCourses
        else:
            return None

    @log
    def listerTous(self, idUtilisateur) -> list[ListeDeCourses]:
        """lister toutes les listes de courses de l'utilisateur grâce à son id"""
        liste_DeCourses = ListeDeCourseDAO().listerTous(idUtilisateur)
        return liste_DeCourses

    @log
    def ajouterUnIngredient(self, idUtilisateur, IngredientQuantite) -> bool:
        """Ajoute ou met à jour un ingrédient dans la liste de courses."""
        return ListeDeCourseDAO().ajouterUnIngredient(idUtilisateur, IngredientQuantite)

    @log
    def retirerUnIngredient(self, idUtilisateur, Ingredient) -> bool:
        """Retire un ingrédient de la liste de courses."""
        return ListeDeCourseDAO().retirerUnIngredient(idUtilisateur, Ingredient)
