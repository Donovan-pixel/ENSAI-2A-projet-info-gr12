from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from view.session import Session

from service.suggestion_service import SuggestionService
from service.recette_service import RecetteService

class SuggestionVue(VueAbstraite):
    """Vue qui affiche :
    - La liste des recettes suggérées à l'utilisateur
    """

    def __init__(self, message=""):
        self.message = message

    def choisir_menu(self):
        utilisateur = Session().utilisateur
        service_suggestions = SuggestionService()

        suggestions = service_suggestions.obtenirSuggestionRecette(utilisateur)

        print("\n" + "-" * 50 + "\nVoici les recettes recommandées\n" + "-" * 50 + "\n")

        if suggestions:
            for suggestion in suggestions:
                print(f"- {recette.titre} (Catégorie: {recette.categorie}, Origine: {recette.origine})")
        else:
            print("Vous n'avez aucune suggestion.")

        choix = inquirer.select(
            message="Que voulez-vous faire ?",
            choices=[
                "Retourner au menu principal",
            ],
        ).execute()

        match choix:
            case "Retourner au menu principal":
                from view.menu_utilisateur_vue import MenuUtilisateurVue
                return MenuUtilisateurVue()