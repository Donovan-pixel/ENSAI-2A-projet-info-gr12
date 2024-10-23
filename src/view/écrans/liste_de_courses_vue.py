from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from view.session import Session

from service.liste_de_courses_service import ListeDeCoursesService
from service.ingredient_service import IngredientService

class ListeDeCoursesVue(VueAbstraite):
    """Vue qui affiche :
    - La liste de courses de l'utilisateur
    """

    def choisir_menu(self):
        utilisateur = Session().utilisateur
        service_liste_courses = ListeDeCoursesService()

        # Obtenir la liste de courses de l'utilisateur
        liste_de_courses = service_liste_courses.listerTous(utilisateur.idUtilisateur)

        print("\n" + "-" * 50 + "\nVotre liste de courses\n" + "-" * 50 + "\n")

        if liste_de_courses:
            for ingredient, quantite in liste_de_courses.ingredientQuantite.items():
                print(f"- {ingredient} (quantité: {quantite})")
        else:
            print("Votre liste de courses est vide.")

        choix = inquirer.select(
            message="Que voulez-vous faire ?",
            choices=[
                "Ajouter un ingrédient à la liste",
                "Retirer un ingrédient de la liste",
                "Retourner au menu principal",
            ],
        ).execute()

        match choix:
            case "Ajouter un ingrédient à la liste":
                self.ajouter_ingredient(service_liste_courses, utilisateur.idUtilisateur)
                return ListeDeCoursesVue("Ingrédient ajouté à la liste de courses.")

            case "Retirer un ingrédient de la liste":
                self.retirer_ingredient(service_liste_courses, liste_de_courses, utilisateur.idUtilisateur)
                return ListeDeCoursesVue("Ingrédient retiré de la liste de courses.")

            case "Retourner au tableau de bord":
                from view.menu_utilisateur_vue import MenuUtilisateurVue
                return MenuUtilisateurVue()

    def ajouter_ingredient(self, service_liste_courses, idUtilisateur):
        ingredients = IngredientService().obtenirTousLesIngredients()
        ingredient_choisi = inquirer.select(
            message="Choisissez un ingrédient à ajouter :",
            choices=[ing.nom for ing in ingredients]
        ).execute()

        quantite = inquirer.number(
            message="Entrez la quantité :",
            float_allowed=True,  
            min_allowed=1 
        ).execute()

        ingredient = next(ing for ing in ingredients if ing.nom == ingredient_choisi)
        service_liste_courses.ajouterUnIngredient(idUtilisateur, ingredient.idIngredient, quantite)

    def retirer_ingredient(self, service_liste_courses, liste_de_courses, idUtilisateur):
        ingredient_choisi = inquirer.select(
            message="Choisissez un ingrédient à retirer :",
            choices=[ing.nom for ing in liste_de_courses]
        ).execute()

        ingredient = next(ing for ing in liste_de_courses if ing.nom == ingredient_choisi)
        service_liste_courses.retirerUnIngredient(idUtilisateur, ingredient.idIngredient)
