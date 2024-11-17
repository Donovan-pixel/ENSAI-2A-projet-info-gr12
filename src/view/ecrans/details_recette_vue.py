from InquirerPy import inquirer
import textwrap
from view.vue_abstraite import VueAbstraite
from view.session import Session

# from service.recette_service import RecetteService
from service.ingredient_service import IngredientService
from service.recette_favorite_service import RecetteFavoritesService
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
        import re

        etapes = re.split(r"(?<=[.!?])\s+", self.recette.consignes.strip())

        for i, etape in enumerate(etapes, start=1):
            if etape:
                wrapped_text = textwrap.fill(
                    etape,
                    width=110,
                    initial_indent=f"      {i}. ",
                    subsequent_indent="         ",
                )
                print(wrapped_text)

        print("\nAvis :")
        avis_list = AvisService().obtenirAvisParRecette(self.recette)
        if avis_list:
            for avis in avis_list:
                print(f"  - Note: {avis.note}/5")
                print(f"    Commentaire: {avis.commentaire}")
                print("-" * 50)
        else:
            print("  Aucun avis disponible pour cette recette.")

        print("=" * 70)

        choices = [
            "Gérer les ingrédients",
            "Ajouter un avis",
            "Retourner à la liste des recettes",
        ]

        favorites = RecetteFavoritesService().obtenirRecettesFavorites(utilisateur)

        if self.recette not in favorites:
            choices.insert(0, "Ajouter cette recette aux favorites")
        else:
            choices.insert(0, "Retirer cette recette des favorites")

        choix = inquirer.select(
            message="Que voulez-vous faire ?",
            choices=choices,
        ).execute()

        match choix:
            case "Ajouter cette recette aux favorites":
                RecetteFavoritesService().ajouter_recette_favorite(self.recette, utilisateur)
                print(f"La recette {self.recette.titre} a été ajoutée à vos favorites.")
                return self.choisir_menu()

            case "Retirer cette recette des favorites":
                RecetteFavoritesService().supprimer_recette_favorite(self.recette, utilisateur)
                print(f"La recette {self.recette.titre} a été supprimée des favorites.")
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

        for ingredient_nom, details in ingredients_a_ajouter.items():
            idIngredient = IngredientService().obtenirIdPArNom(ingredient_nom)
            quantite = ingredients_quantites[ingredient_nom]

            if idIngredient is None or quantite is None:
                print(f" Impossible d'ajouter {ingredient_nom} : informations manquantes.")
                continue

            success = ListeDeCoursesService().ajouterUnIngredient(
                utilisateur.idUtilisateur, idIngredient, quantite
            )

            if success:
                print(f"{ingredient_nom} ({quantite}) ajouté à la liste de courses.")
            else:
                print(f"Échec lors de l'ajout de {ingredient_nom} ({quantite}).")

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
