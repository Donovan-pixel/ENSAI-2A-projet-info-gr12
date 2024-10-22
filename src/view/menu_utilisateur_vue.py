from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from view.session import Session

from service.utilisateur_service import UtilisateurService
from service.recette_service import RecetteService

class MenuUtilisateurVue(VueAbstraite):
    """Vue du menu de l'utilisateur

    Attributes
    ----------
    message=''
        str

    Returns
    ------
    view
        Retourne la prochaine vue, celle qui est choisie par l'utilisateur
    """

    def choisir_menu(self):
        """Choix du menu suivant de l'utilisateur

        Return
        ------
        vue
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        print("\n" + "-" * 50 + "\nTableau de bord\n" + "-" * 50 + "\n")

        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=[
                "Afficher la liste des recettes",
                "Voir mes recettes favorites",
                "Gérer mes ingrédients favoris/non désirés",
                "Obtenir des suggestions de recettes",
                "Accéder à ma liste de courses",
                "Se déconnecter",
            ],
        ).execute()

        match choix:
            case "Se déconnecter":
                Session().deconnexion()
                from view.accueil.accueil_vue import AccueilVue
                return AccueilVue()

            case "Voir mes recettes favorites":
                from view.écrans.recettes_favorites_vue import RecettesFavoritesVue
                return RecettesFavoritesVue()

            case "Afficher la liste des recettes":
                from view.écrans.liste_des_recettes_vue import L
                return liste_des_recettes_vue(rece)

            case "Gérer mes ingrédients favoris/non désirés":
                from view.écrans.ingredients_fav_non_desire_vue import IngredientsFavorisNonDesiresVue
                return IngredientsFavorisNonDesiresVue()

            case "Obtenir des suggestions de recettes": 
                from view.écrans.suggestion_vue import SuggestionVue
                return SuggestionVue()

            case "Accéder à ma liste de courses":
                from view.écrans.liste_de_courses_vue import ListeDeCoursesVue
                return ListeDeCoursesVue()