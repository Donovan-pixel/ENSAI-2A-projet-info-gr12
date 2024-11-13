from InquirerPy import inquirer
from view.vue_abstraite import VueAbstraite

# from view.session import Session
from service.recette_service import RecetteService


class FiltrageParCategorieVue(VueAbstraite):
    """Vue pour filtrer les recettes par catégorie"""

    def __init__(self, message=""):
        self.message = message

    def choisir_menu(self):
        categories = RecetteService().obtenirToutesLesCategories()

        categorie_choisie = inquirer.select(
            message="Choisissez une catégorie :",
            choices=categories,
        ).execute()

        recettes = RecetteService().obtenirRecettesParCategorie(categorie_choisie)

        if recettes:
            recettes_choisies = inquirer.select(
                message=f"Recettes dans la catégorie '{categorie_choisie}' :",
                choices=[recette.titre for recette in recettes] + ["Retour au menu principal"],
            ).execute()

            if recettes_choisies == "Retour au menu principal":
                from view.menu_utilisateur_vue import MenuUtilisateurVue

                return MenuUtilisateurVue()
            else:
                recette_selectionnee = next(
                    recette for recette in recettes if recette.titre == recettes_choisies
                )
                from view.ecrans.details_recette_vue import DetailsRecetteVue

                return DetailsRecetteVue(recette_selectionnee).choisir_menu()
        else:
            print(f"Aucune recette trouvée dans la catégorie '{categorie_choisie}'.")
            return self.choisir_menu()
