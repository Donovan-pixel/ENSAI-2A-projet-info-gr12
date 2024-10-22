from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from view.session import Session

from service.liste_de_courses_service import ListeDeCoursesService
from service.ingredient_service import IngredientService

class ListeDeCoursesVue(VueAbstraite):
    """Vue qui affiche :
    - La liste de courses de l'utilisateur
    """

    def __init__(self, message=""):
        self.message = message

    def choisir_menu(self):
        utilisateur = Session().get_utilisateur()
        service_liste_courses = ListeDeCoursesService()

        # Obtenir la liste de courses de l'utilisateur
        liste_de_courses = service_liste_courses.listerTous(utilisateur.idUtilisateur)

        print("\n" + "-" * 50 + "\nVotre liste de courses\n" + "-" * 50 + "\n")

        # Affichage des ingrédients dans la liste de courses
        if liste_de_courses:
            for i, ingredient in enumerate(liste_de_courses):
                print(f"{i + 1}. {ingredient.nom} (quantité: {ingredient.quantite})")
        else:
            print("Votre liste de courses est vide.")

        # Choix d'actions possibles
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
                # L'utilisateur peut ajouter un ingrédient
                self.ajouter_ingredient(service_liste_courses, utilisateur.idUtilisateur)
                return ListeDeCoursesVue("Ingrédient ajouté à la liste de courses.")

            case "Retirer un ingrédient de la liste":
                # L'utilisateur peut retirer un ingrédient
                self.retirer_ingredient(service_liste_courses, liste_de_courses, utilisateur.idUtilisateur)
                return ListeDeCoursesVue("Ingrédient retiré de la liste de courses.")

            case "Retourner au tableau de bord":
                from view.menu_utilisateur_vue import MenuUtilisateurVue
                return MenuUtilisateurVue()

    def ajouter_ingredient(self, service_liste_courses, idUtilisateur):
        # Choisir l'ingrédient à ajouter depuis une liste d'ingrédients disponibles
        ingredients = IngredientService().listerTous()  # Suppose une méthode pour obtenir les ingrédients disponibles
        ingredient_choisi = inquirer.select(
            message="Choisissez un ingrédient à ajouter :",
            choices=[ing.nom for ing in ingredients]
        ).execute()

        quantite = inquirer.text(message="Entrez la quantité : ").execute()

        # Ajouter l'ingrédient à la liste de courses
        ingredient = next(ing for ing in ingredients if ing.nom == ingredient_choisi)
        service_liste_courses.ajouterUnIngredient(idUtilisateur, ingredient.idIngredient, quantite)

    def retirer_ingredient(self, service_liste_courses, liste_de_courses, idUtilisateur):
        # Choisir l'ingrédient à retirer depuis la liste de courses actuelle
        ingredient_choisi = inquirer.select(
            message="Choisissez un ingrédient à retirer :",
            choices=[ing.nom for ing in liste_de_courses]
        ).execute()

        # Retirer l'ingrédient de la liste de courses
        ingredient = next(ing for ing in liste_de_courses if ing.nom == ingredient_choisi)
        service_liste_courses.retirerUnIngredient(idUtilisateur, ingredient.idIngredient)
