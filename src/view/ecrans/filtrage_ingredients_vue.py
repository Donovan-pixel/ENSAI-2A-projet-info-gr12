from InquirerPy import inquirer
from InquirerPy.separator import Separator

from view.vue_abstraite import VueAbstraite

from service.ingredient_service import IngredientService
from service.recette_service import RecetteService


class FiltrageParIngredientsVue(VueAbstraite):
    """Vue pour filtrer les recettes par ingrédients"""

    def __init__(self, message=""):
        self.message = message

    def choisir_menu(self):
        service_ingredient = IngredientService()
        ingredients = service_ingredient.obtenirTousLesIngredients()

        choix_ingredients = inquirer.checkbox(
            message="Sélectionnez les ingrédients que vous souhaitez\n"
            "utiliser pour filtrer les recettes :",
            choices=[ingredient.nom for ingredient in ingredients]
            + ["Retourner au menu des recettes"],
        ).execute()

        if "Retourner au menu des recettes" in choix_ingredients:
            from view.ecrans.liste_des_recettes_vue import ListeDesRecettesVue

            return ListeDesRecettesVue().choisir_menu()

        print(f"Ingrédients sélectionnés : {', '.join(choix_ingredients)}")
        confirmation = inquirer.select(
            message="Que souhaitez-vous faire ?",
            choices=[
                "Confirmer et afficher les recettes filtrées",
                "Modifier la sélection",
                "Retourner au menu des recettes",
            ],
        ).execute()

        if confirmation == "Retourner au menu des recettes":
            from view.ecrans.liste_des_recettes_vue import ListeDesRecettesVue

            return ListeDesRecettesVue().choisir_menu()
        elif confirmation == "Modifier la sélection":
            return self.choisir_menu()

        ingredients_objets = [
            ingredient for ingredient in ingredients if ingredient.nom in choix_ingredients
        ]
        service_recette = RecetteService()
        recettes = service_recette.obtenirRecettesParIngredients(ingredients_objets)

        self.afficher_recettes_filtrees(recettes)

    def afficher_recettes_filtrees(self, recettes):
        if not recettes:
            print("\nAucune recette ne correspond à votre sélection.\n")
            return self.choisir_menu()
        else:
            choix_recettes = inquirer.select(
                message="Recettes correspondant à votre sélection :",
                choices=[Separator("------------------")]
                + [recette.titre for recette in recettes]
                + [Separator("------------------")]
                + ["Retourner au tableau de bord"],
            ).execute()

            if choix_recettes == "Retourner au tableau de bord":
                from view.menu_utilisateur_vue import MenuUtilisateurVue

                return MenuUtilisateurVue().choisir_menu()

            recette = next(rec for rec in recettes if rec.titre == choix_recettes)
            choix_action = inquirer.select(
                message=f"Que souhaitez-vous faire avec {recette.titre} ?",
                choices=[
                    "Voir les détails de la recette",
                    "Retourner à la liste des recettes",
                ],
            ).execute()

            match choix_action:
                case "Voir les détails de la recette":
                    from view.ecrans.details_recette_vue import DetailsRecetteVue

                    return DetailsRecetteVue(recette).choisir_menu()
                case "Retourner à la liste des recettes":
                    return self.afficher_recettes_filtrees(recettes)
