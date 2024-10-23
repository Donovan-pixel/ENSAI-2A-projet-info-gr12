from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from view.session import Session
from service.ingredient_service import IngredientService
from service.recette_service import RecetteService

class FiltrageParIngredientsVue(VueAbstraite):
    """Vue pour filtrer les recettes par ingrédients"""

    def __init__(self, message=""):
        self.message = message

    def choisir_menu(self):
        service_ingredient = IngredientService()
        ingredients = service_ingredient.obtenirTousLesIngredients()

        # Affichage des ingrédients disponibles pour le filtrage
        choix_ingredients = inquirer.checkbox(
            message="Sélectionnez les ingrédients que vous souhaitez utiliser pour filtrer les recettes :",
            choices=[ingredient.nom for ingredient in ingredients] + ["Retourner au menu principal"],
        ).execute()

        if "Retourner au menu principal" in choix_ingredients:
            from view.menu_utilisateur_vue import MenuUtilisateurVue
            return MenuUtilisateurVue()

        # Confirmation des ingrédients choisis
        print(f"Ingrédients sélectionnés : {', '.join(choix_ingredients)}")
        confirmation = inquirer.select(
            message="Que souhaitez-vous faire ?",
            choices=[
                "Confirmer et afficher les recettes filtrées",
                "Modifier la sélection",
                "Retourner au menu principal",
            ],
        ).execute()

        if confirmation == "Retourner au menu principal":
            from view.menu_utilisateur_vue import MenuUtilisateurVue
            return MenuUtilisateurVue()
        elif confirmation == "Modifier la sélection":
            return self.choisir_menu()

        # Filtrer les recettes par ingrédients
        ingredients_objets = [ingredient for ingredient in ingredients if ingredient.nom in choix_ingredients]
        service_recette = RecetteService()
        recettes = service_recette.obtenirRecettesParIngredients(ingredients_objets)

        # Affichage des recettes filtrées
        self.afficher_recettes_filtrees(recettes)

    def afficher_recettes_filtrees(self, recettes):
        if not recettes:
            print("Aucune recette ne correspond à votre sélection.")
        else:
            choix_recettes = inquirer.select(
                message="Recettes correspondant à votre sélection :",
                choices=[recette.titre for recette in recettes] + ["Retourner au menu principal"],
            ).execute()

            if choix_recettes == "Retourner au menu principal":
                from view.menu_utilisateur_vue import MenuUtilisateurVue
                return MenuUtilisateurVue()

            # Affichage des détails ou ajout aux favoris
            recette = next(rec for rec in recettes if rec.titre == choix_recettes)
            choix_action = inquirer.select(
                message=f"Que souhaitez-vous faire avec {recette.titre} ?",
                choices=[
                    "Voir les détails de la recette",
                    "Ajouter cette recette aux favoris",
                    "Retourner à la liste des recettes",
                ],
            ).execute()

            match choix_action:
                case "Voir les détails de la recette":
                    details = service_recette.afficherRecette(recette)
                    print(details)
                case "Ajouter cette recette aux favoris":
                    from service.recette_favorites_service import RecetteFavoritesService
                    utilisateur = Session().utilisateur
                    RecetteFavoritesService().ajouter_recette_favorite(recette, utilisateur)
                    print(f"{recette.titre} a été ajoutée aux favoris.")
                case "Retourner à la liste des recettes":
                    return self.afficher_recettes_filtrees(recettes)
