from InquirerPy import inquirer
from InquirerPy.base import Choice
from InquirerPy.separator import Separator

from view.vue_abstraite import VueAbstraite
from view.session import Session

from service.suggestion_service import SuggestionService


class SuggestionVue(VueAbstraite):
    """Vue qui affiche :
    - La liste des recettes suggérées à l'utilisateur
    - La possibilité d'accéder aux details d'une recette
    """

    def __init__(self, message=""):
        self.message = message

    def choisir_menu(self):
        utilisateur = Session().utilisateur
        service_suggestions = SuggestionService()

        suggestions = service_suggestions.obtenirSuggestionRecette(utilisateur)

        print("\n" + "-" * 70)
        print(" Voici les recettes recommandées ".center(70))
        print("-" * 70 + "\n")

        if suggestions:
            choices = (
                [Separator("------------------")]
                + [Choice(recette.titre) for recette in suggestions]
                + [Separator("------------------")]
            )
            choices.append(Choice("Retourner au tableau de bord"))

            recette_choisie = inquirer.select(
                message=(
                    "Sélectionnez une recette pour voir les détails"
                    " ou revenir au tableau de bord :"
                ),
                choices=choices,
            ).execute()

            if recette_choisie == "Retourner au tableau de bord":
                from view.menu_utilisateur_vue import MenuUtilisateurVue

                return MenuUtilisateurVue()
            else:
                recette = next(rec for rec in suggestions if rec.titre == recette_choisie)
                from view.ecrans.details_recette_vue import DetailsRecetteVue

                return DetailsRecetteVue(recette).choisir_menu()

        else:
            print("Vous n'avez aucune suggestion.")
            from view.menu_utilisateur_vue import MenuUtilisateurVue

            return MenuUtilisateurVue()
