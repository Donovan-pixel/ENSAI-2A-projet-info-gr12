from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from view.session import Session
from service.recette_service import RecetteService
from service.ingredient_favoris_service import IngredientFavorisService
from service.ingredient_non_desire_service import IngredientNonDesireService
from service.liste_courses_service import ListeCoursesService
from service.avis_service import AvisService

class DetailsRecetteVue(VueAbstraite):
    """Vue pour afficher les détails d'une recette"""

    def __init__(self, recette):
        self.recette = recette

    def choisir_menu(self):
        utilisateur = Session().utilisateur

        # Affichage des détails de la recette
        print(f"\nTitre : {self.recette.titre}")
        print(f"Catégorie : {self.recette.categorie}")
        print(f"Origine : {self.recette.origine}")
        print("Ingrédients :")
        for ingredient, quantite in self.recette.ingredientQuantite.items():
            print(f" - {ingredient} : {quantite}")
        print(f"Consignes : {self.recette.consignes}")
        print(f"Avis : {self.recette.avis}\n")

        # Options disponibles avec un curseur
        choix = inquirer.select(
            message="Que voulez-vous faire ?",
            choices=[
                "Ajouter cette recette aux favoris",
                "Gérer les ingrédients",
                "Ajouter un avis",
                "Retourner à la liste des recettes",
            ],
        ).execute()

        match choix:
            case "Ajouter cette recette aux favoris":
                from service.recette_favorites_service import RecetteFavoritesService
                RecetteFavoritesService().ajouter_recette_favorite(self.recette, utilisateur)
                print(f"La recette {self.recette.titre} a été ajoutée à vos favoris.")
                return self.choisir_menu()

            case "Gérer les ingrédients":
                self.gerer_ingredients()
                return self.choisir_menu()

            case "Ajouter un avis":
                self.ajouter_avis()
                return self.choisir_menu()

            case "Retourner à la liste des recettes":
                from view.liste_recettes_vue import ListeRecettesVue
                return ListeRecettesVue()

    def gerer_ingredients(self):
        """Permet de gérer les ingrédients d'une recette"""
        ingredients = list(self.recette.ingredientQuantite.keys())

        choix_ingredients = inquirer.checkbox(
            message="Sélectionnez les ingrédients à ajouter à la liste de courses :",
            choices=ingredients,
        ).execute()

        # Ajouter les ingrédients sélectionnés à la liste de courses
        liste_courses_service = ListeCoursesService()
        for ingredient in choix_ingredients:
            liste_courses_service.ajouterIngredientAListe(ingredient)
        print(f"Les ingrédients {', '.join(choix_ingredients)} ont été ajoutés à votre liste de courses.")

        # Gestion des favoris et non désirés pour les ingrédients
        for ingredient in ingredients:
            choix_ingredient = inquirer.select(
                message=f"Que voulez-vous faire avec l'ingrédient {ingredient} ?",
                choices=[
                    "Ajouter aux favoris",
                    "Ajouter aux non désirés",
                    "Ne rien faire",
                ],
            ).execute()

            match choix_ingredient:
                case "Ajouter aux favoris":
                    IngredientFavorisService().ajouterIngredientFavori(ingredient, Session().utilisateur)
                    print(f"L'ingrédient {ingredient} a été ajouté aux favoris.")
                case "Ajouter aux non désirés":
                    IngredientNonDesireService().ajouterIngredientNonDesire(ingredient, Session().utilisateur)
                    print(f"L'ingrédient {ingredient} a été ajouté aux non désirés.")
                case "Ne rien faire":
                    pass

    def ajouter_avis(self):
        """Permet d'ajouter un avis à la recette"""
        avis = inquirer.text(message="Entrez votre avis :").execute()
        note = inquirer.number(message="Entrez une note (sur 5) :").execute()

        avis_service = AvisService()
        avis_service.ajouterAvis(self.recette, Session().utilisateur, avis, note)
        print(f"Votre avis a été ajouté à la recette {self.recette.titre}.")
