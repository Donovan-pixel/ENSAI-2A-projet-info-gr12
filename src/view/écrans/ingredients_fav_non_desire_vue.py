from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from view.session import Session

from service.ingredient_favoris_service import IngredientFavorisService
from service.ingredient_non_desire_service import IngredientNonDesireService

class IngredientsFavorisNonDesiresVue(VueAbstraite):
    """Vue qui affiche :
    - La liste des ingrédients favoris et non désirés
    - La possibilité d'ajouter/supprimer des ingrédients de la liste
    """

    def __init__(self, message=""):
        self.message = message

    def choisir_menu(self):
        utilisateur = Session().utilisateur

        favoris_service = IngredientFavorisService()
        non_desires_service = IngredientNonDesireService()

        ingredients_favoris = favoris_service.obtenirIngredientsFavoris(utilisateur)
        ingredients_non_desires = non_desires_service.obtenirIngredientsNonDesires(utilisateur)

        print("\n" + "-" * 50 + "\nIngrédients favoris\n" + "-" * 50 + "\n")
        if ingredients_favoris:
            for ingredient in ingredients_favoris:
                print(f"- {ingredient.nom}")
        else:
            print("Vous n'avez pas d'ingrédients favoris.")

        print("\n" + "-" * 50 + "\nIngrédients non désirés\n" + "-" * 50 + "\n")
        if ingredients_non_desires:
            for ingredient in ingredients_non_desires:
                print(f"- {ingredient.nom}")
        else:
            print("Vous n'avez pas d'ingrédients non désirés.")

        choix = inquirer.select(
            message="Que voulez-vous faire ?",
            choices=[
                "Ajouter un ingrédient favori",
                "Retirer un ingrédient favori",
                "Ajouter un ingrédient non désiré",
                "Retirer un ingrédient non désiré",
                "Retourner au menu principal",
            ],
        ).execute()

        match choix:
            case "Ajouter un ingrédient favori":
                self.ajouter_ingredient_favori(favoris_service, utilisateur)
                return IngredientsFavorisNonDesiresVue("Ingrédient favori ajouté.")

            case "Retirer un ingrédient favori":
                self.retirer_ingredient_favori(favoris_service, ingredients_favoris, utilisateur)
                return IngredientsFavorisNonDesiresVue("Ingrédient favori retiré.")

            case "Ajouter un ingrédient non désiré":
                self.ajouter_ingredient_non_desire(non_desires_service, utilisateur)
                return IngredientsFavorisNonDesiresVue("Ingrédient non désiré ajouté.")

            case "Retirer un ingrédient non désiré":
                self.retirer_ingredient_non_desire(non_desires_service, ingredients_non_desires, utilisateur)
                return IngredientsFavorisNonDesiresVue("Ingrédient non désiré retiré.")

            case "Retourner au menu principal":
                from view.menu_utilisateur_vue import MenuUtilisateurVue
                return MenuUtilisateurVue()

    def ajouter_ingredient_favori(self, favoris_service, utilisateur):
        nom_ingredient = inquirer.text(message="Entrez le nom de l'ingrédient favori :").execute()
        favoris_service.ajouterIngredientFavori(nom_ingredient, utilisateur)

    def retirer_ingredient_favori(self, favoris_service, ingredients_favoris, utilisateur):
        if ingredients_favoris:
            ingredient_choisi = inquirer.select(
                message="Choisissez un ingrédient favori à retirer :",
                choices=[ing.nom for ing in ingredients_favoris]
            ).execute()
            favoris_service.supprimerIngredientFavori(ingredient_choisi, utilisateur)

    def ajouter_ingredient_non_desire(self, non_desires_service, utilisateur):
        nom_ingredient = inquirer.text(message="Entrez le nom de l'ingrédient non désiré :").execute()
        non_desires_service.ajouterIngredientNonDesire(nom_ingredient, utilisateur)

    def retirer_ingredient_non_desire(self, non_desires_service, ingredients_non_desires, utilisateur):
        if ingredients_non_desires:
            ingredient_choisi = inquirer.select(
                message="Choisissez un ingrédient non désiré à retirer :",
                choices=[ing.nom for ing in ingredients_non_desires]
            ).execute()
            non_desires_service.supprimerIngredientNonDesire(ingredient_choisi, utilisateur)
