from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from view.session import Session


class MenuUtilisateurVue(VueAbstraite):
    """Vue du menu de l'utilisateur

    Attributes
    ----------
    None

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

        print("\n" + "═" * 70)
        print(" Tableau de bord ".center(70))
        print("═" * 70 + "\n")

        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=[
                "Afficher la liste des recettes",
                "Voir mes recettes favorites",
                "Gérer mes ingrédients favoris/non désirés",
                "Obtenir des suggestions de recettes",
                "Accéder à ma liste de courses",
                "Modifier mon profil",
                "Se déconnecter",
            ],
        ).execute()

        match choix:
            case "Se déconnecter":
                Session().deconnexion()
                from view.accueil.accueil_vue import AccueilVue

                return AccueilVue().choisir_menu()

            case "Voir mes recettes favorites":
                from view.ecrans.recettes_favorites_vue import RecettesFavoritesVue

                return RecettesFavoritesVue().choisir_menu()

            case "Afficher la liste des recettes":
                from view.ecrans.liste_des_recettes_vue import ListeDesRecettesVue

                return ListeDesRecettesVue().choisir_menu()

            case "Gérer mes ingrédients favoris/non désirés":
                from view.ecrans.ingredients_fav_non_desire_vue import (
                    IngredientsFavorisNonDesiresVue,
                )

                return IngredientsFavorisNonDesiresVue().choisir_menu()

            case "Obtenir des suggestions de recettes":
                from view.ecrans.suggestion_vue import SuggestionVue

                return SuggestionVue().choisir_menu()

            case "Accéder à ma liste de courses":
                from view.ecrans.liste_de_courses_vue import ListeDeCoursesVue

                return ListeDeCoursesVue().choisir_menu()
            case "Modifier mon profil":
                from view.ecrans.modifier_profile_vue import ModifierProfilVue

                ModifierProfilVue().choisir_menu()
