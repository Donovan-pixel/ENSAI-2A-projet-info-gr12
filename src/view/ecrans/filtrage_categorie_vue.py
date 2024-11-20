from InquirerPy import inquirer
from InquirerPy.separator import Separator
from view.vue_abstraite import VueAbstraite
from view.ecrans.liste_des_recettes_vue import ListeDesRecettesVue

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
            choices=[Separator("------------------")]
            + categories
            + [Separator("------------------")]
            + ["Retourner à la liste des recettes"],
        ).execute()

        if categorie_choisie == "Retourner à la liste des recettes":
            return ListeDesRecettesVue().choisir_menu()

        recettes = RecetteService().obtenirRecettesParCategorie(categorie_choisie)

        if recettes:
            recettes_choisies = inquirer.select(
                message=f"Recettes dans la catégorie '{categorie_choisie}' :",
                choices=[Separator("------------------")]
                + [recette.titre for recette in recettes]
                + [Separator("------------------")]
                + ["Retourner à la liste des catégories"],
            ).execute()

            if recettes_choisies == "Retourner à la liste des catégories":
                self.choisir_menu()
            else:
                recette_selectionnee = next(
                    recette for recette in recettes if recette.titre == recettes_choisies
                )
                from view.ecrans.details_recette_vue import DetailsRecetteVue

                return DetailsRecetteVue(recette_selectionnee).choisir_menu()
        else:
            print(f"Aucune recette trouvée dans la catégorie '{categorie_choisie}'.")
            return self.choisir_menu()
