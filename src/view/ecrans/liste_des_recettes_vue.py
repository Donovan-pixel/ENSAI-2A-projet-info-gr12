from InquirerPy import inquirer
from InquirerPy.separator import Separator

from view.vue_abstraite import VueAbstraite

from service.recette_service import RecetteService


class ListeDesRecettesVue(VueAbstraite):
    """Vue qui affiche :
    - La liste des recettes
    - La possibilité de filtrer les recettes par ingrédients/catégorie/lettre
    """

    def __init__(self, message=""):
        self.message = message
        self.recettes = []

    def choisir_menu(self):
        service_recette = RecetteService()

        filtre_choix = inquirer.select(
            message="Comment souhaitez-vous filtrer les recettes ?",
            choices=[
                Separator("-----------------------"),
                "Par ingrédient",
                "Par catégorie",
                "Par lettre",
                Separator("-----------------------"),
                "Afficher toutes les recettes",
                Separator("-----------------------"),
                "Retourner au tableau de bord",
            ],
        ).execute()

        if filtre_choix == "Par ingrédient":
            from view.ecrans.filtrage_ingredients_vue import FiltrageParIngredientsVue

            return FiltrageParIngredientsVue()

        elif filtre_choix == "Par catégorie":
            from view.ecrans.filtrage_categorie_vue import FiltrageParCategorieVue

            return FiltrageParCategorieVue()

        elif filtre_choix == "Par lettre":
            from view.ecrans.filtrage_lettre_vue import FiltrageParLettreVue

            return FiltrageParLettreVue()

        elif filtre_choix == "Afficher toutes les recettes":
            self.recettes = service_recette.obtenirToutesLesRecettes()

        elif filtre_choix == "Retourner au tableau de bord":
            from view.menu_utilisateur_vue import MenuUtilisateurVue

            return MenuUtilisateurVue()

        if not self.recettes:
            print("Aucune recette trouvée pour ce filtre.")
            return self.choisir_menu()

        return self.afficher_recettes()

    def afficher_recettes(self):
        """
        Affiche les recettes et permet de choisir une action.
        """
        recette_choisie = inquirer.select(
            message="Sélectionnez une recette ou retournez au menu principal :",
            choices=[recette.titre for recette in self.recettes]
            + [Separator("-----------------------")]
            + ["Retourner au menu des recettes"],
        ).execute()

        if recette_choisie == "Retourner au menu des recettes":
            return self.choisir_menu()

        recette = next(rec for rec in self.recettes if rec.titre == recette_choisie)

        action_choix = inquirer.select(
            message=f"Que souhaitez-vous faire avec {recette.titre} ?",
            choices=[
                "Voir les détails de la recette",
                "Retourner à la liste des recettes",
            ],
        ).execute()

        if action_choix == "Voir les détails de la recette":
            from view.ecrans.details_recette_vue import DetailsRecetteVue

            return DetailsRecetteVue(recette)

        elif action_choix == "Retourner à la liste des recettes":
            return self.afficher_recettes()
