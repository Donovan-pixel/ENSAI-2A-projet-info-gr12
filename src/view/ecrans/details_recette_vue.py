from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from view.session import Session

# from service.recette_service import RecetteService
from service.ingredient_favori_service import IngredientFavoriService
from service.ingredient_non_desire_service import IngredientNonDesireService
from service.liste_de_courses_service import ListeDeCoursesService
from service.avis_service import AvisService


class DetailsRecetteVue(VueAbstraite):
    """Vue pour afficher les détails d'une recette"""

    def __init__(self, recette):
        self.recette = recette

    def choisir_menu(self):
        utilisateur = Session().utilisateur

        print("\n" + "=" * 70)
        print(f"  🍝 Titre : {self.recette.titre}")
        print(f"  📂 Catégorie : {self.recette.categorie}")
        print(f"  🌍 Origine : {self.recette.origine}")
        print("\n  📋 Ingrédients :")
        for ingredient, quantite in self.recette.ingredientQuantite.items():
            print(f"    - {ingredient} : {quantite}")

        print("\n  📝 Consignes :")
        for step in self.recette.consignes.split("STEP"):
            if step.strip():
                print(f"    - STEP {step.strip()}")

        print("\nAvis :")
        avis_list = AvisService().obtenirAvisParRecette(self.recette)
        if avis_list:
            for avis in avis_list:
                print(f"  - Note: {avis.note}/5")
                print(f"    Commentaire: {avis.commentaire}")
                print(" - " * 50)
        else:
            print("  Aucun avis disponible pour cette recette.")

        print("=" * 70)

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
                from service.recette_favorite_service import RecetteFavoritesService

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
                from view.ecrans.liste_des_recettes_vue import ListeDesRecettesVue

                return ListeDesRecettesVue()

    def gerer_ingredients(self):
        """Permet de gérer les ingrédients d'une recette"""
        utilisateur = Session().utilisateur
        ingredients_quantites = self.recette.ingredientQuantite

        choix_ingredients = inquirer.checkbox(
            message="Sélectionnez les ingrédients à ajouter à la liste de courses :",
            choices=list(ingredients_quantites.keys()),
        ).execute()

        ingredients_a_ajouter = {
            ingredient: ingredients_quantites[ingredient] for ingredient in choix_ingredients
        }

        liste_courses_service = ListeDeCoursesService()
        success = liste_courses_service.ajouterUnIngredient(
            utilisateur.idUtilisateur, ingredients_a_ajouter
        )

        if success:
            print(
                f"Les ingrédients {', '.join(choix_ingredients)} ont "
                f"été ajoutés à votre liste de courses."
            )

        ingredients = list(self.recette.ingredientQuantite.keys())
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
                    IngredientFavoriService().ajouterIngredientFavori(
                        ingredient, Session().utilisateur
                    )
                    print(f"L'ingrédient {ingredient} a été ajouté aux favoris.")
                case "Ajouter aux non désirés":
                    IngredientNonDesireService().ajouterIngredientNonDesire(
                        ingredient, Session().utilisateur
                    )
                    print(f"L'ingrédient {ingredient} a été ajouté aux non désirés.")
                case "Ne rien faire":
                    pass

    def ajouter_avis(self):
        """Permet d'ajouter un avis à la recette"""
        avis = inquirer.text(message="Entrez votre avis :").execute()
        note = inquirer.number(message="Entrez une note (sur 5) :").execute()

        AvisService().ajouterNouvelAvis(
            Session().utilisateur.idUtilisateur, self.recette.idRecette, note, avis
        )
        print(f"Votre avis a été ajouté à la recette {self.recette.titre}.")
