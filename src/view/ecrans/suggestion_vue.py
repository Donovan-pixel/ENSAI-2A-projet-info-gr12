from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from view.session import Session

from service.suggestion_service import SuggestionService
from service.recette_service import RecetteService


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

        print("\n" + "-" * 50 + "\nVoici les recettes recommandées\n" + "-" * 50 + "\n")

        if suggestions:
            recette_choisie = inquirer.select(
                message="Sélectionnez une recette pour voir les détails ou revenir au tableau de bord :",
                choices=[recette.titre for recette in suggestions] + ["Retourner au tableau de bord"],
            ).execute()

            if recette_choisie == "Retourner au menu principal":
                from view.menu_utilisateur_vue import MenuUtilisateurVue
                return MenuUtilisateurVue()
            else:
                recette = next(rec for rec in suggestions if rec.titre == recette_choisie)
                self.afficher_details_recette(recette)
                return SuggestionVue()

        else:
            print("Vous n'avez aucune suggestion.")
            from view.menu_utilisateur_vue import MenuUtilisateurVue
            return MenuUtilisateurVue()

    def afficher_details_recette(self, recette):
        """Afficher les détails d'une recette"""

        print(f"\nDétails de la recette : {recette.titre}")
        print(f"Catégorie: {recette.categorie}")
        print(f"Origine: {recette.origine}")
        print("Ingrédients:")
        for ingredient, quantite in recette.ingredients.items():
            print(f"- {ingredient}: {quantite}")
        print("Instructions:")
        for i, instruction in enumerate(recette.instructions, 1):
            print(f"{i}. {instruction}")
        input("\nAppuyez sur Entrée pour retourner aux suggestions...")
