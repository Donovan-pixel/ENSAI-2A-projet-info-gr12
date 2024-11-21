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
            "Retourner au tableau de bord",
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

            case "Retourner au tableau de bord":
                from view.menu_utilisateur_vue import MenuUtilisateurVue

                return MenuUtilisateurVue().choisir_menu()

    def gerer_ingredients(self):
        while True:
            # Afficher le menu pour choisir une action
            choix_action = inquirer.select(
                message="Que voulez-vous faire ?",
                choices=[
                    "Ajouter des ingrédients à la liste de courses",
                    "Ajouter des ingrédients aux favoris",
                    "Ajouter des ingrédients aux non désirés",
                    "Revenir au menu principal",
                ],
            ).execute()

            match choix_action:
                case "Ajouter des ingrédients à la liste de courses":
                    self.ajouter_ingredients_liste_de_courses()
                case "Ajouter des ingrédients aux favoris":
                    self.ajouter_ingredients_favoris()
                case "Ajouter des ingrédients aux non désirés":
                    self.ajouter_ingredients_non_desires()
                case "Revenir au menu principal":
                    self.choisir_menu()

    def ajouter_ingredients_favoris(self):
        """Ajoute des ingrédients de la recette affichée aux favoris en évitant les doublons."""
        utilisateur = Session().utilisateur
        favoris_service = IngredientFavoriService()
        ingredients_favoris = favoris_service.obtenirIngredientsFavoris(utilisateur)
        ingredients_non_desires = IngredientNonDesireService().obtenirIngredientsNonDesires(
            utilisateur
        )

        ingredients_a_afficher = [
            ingredient
            for ingredient in self.recette.ingredientQuantite.keys()
            if ingredient
            not in [ing.nom for ing in (ingredients_favoris + ingredients_non_desires)]
        ]

        if not ingredients_a_afficher:
            print(
                "Tous les ingrédients de la recette sont déjà dans les favoris ou les non désirés."
            )
            return

        choix_favoris = inquirer.checkbox(
            message="Sélectionnez les ingrédients à ajouter aux favoris :",
            choices=ingredients_a_afficher,
        ).execute()

        for ingredient_nom in choix_favoris:
            favoris_service.ajouterIngredientFavori(ingredient_nom, utilisateur)
            print(f"L'ingrédient {ingredient_nom} a été ajouté aux favoris.")

    def ajouter_ingredients_non_desires(self):
        """Ajoute des ingrédients de la recette affichée aux non désirés en évitant les doublons."""
        utilisateur = Session().utilisateur
        non_desire_service = IngredientNonDesireService()
        ingredients_favoris = IngredientFavoriService().obtenirIngredientsFavoris(utilisateur)
        ingredients_non_desires = non_desire_service.obtenirIngredientsNonDesires(utilisateur)

        ingredients_a_afficher = [
            ingredient
            for ingredient in self.recette.ingredientQuantite.keys()
            if ingredient
            not in [ing.nom for ing in (ingredients_favoris + ingredients_non_desires)]
        ]

        if not ingredients_a_afficher:
            print(
                "Tous les ingrédients de la recette sont déjà dans les favoris ou les non désirés."
            )
            return

        choix_non_desires = inquirer.checkbox(
            message="Sélectionnez les ingrédients à ajouter aux non désirés :",
            choices=ingredients_a_afficher,
        ).execute()

        for ingredient_nom in choix_non_desires:
            non_desire_service.ajouterIngredientNonDesire(ingredient_nom, utilisateur)
            print(f"L'ingrédient {ingredient_nom} a été ajouté aux non désirés.")

    def ajouter_ingredients_liste_de_courses(self):
        """Ajoute des ingrédients sélectionnés à la liste de courses."""
        utilisateur = Session().utilisateur
        ingredients_quantites = self.recette.ingredientQuantite

        choix_ingredients = inquirer.checkbox(
            message="Sélectionnez les ingrédients à ajouter à la liste de courses :",
            choices=list(ingredients_quantites.keys()),
        ).execute()

        # Ajouter chaque ingrédient sélectionné
        for ingredient_nom in choix_ingredients:
            idIngredient = IngredientService().obtenirIdPArNom(ingredient_nom)
            quantite = ingredients_quantites[ingredient_nom]

            if idIngredient is None or quantite is None:
                print(f"Impossible d'ajouter {ingredient_nom} : informations manquantes.")
                continue

            succes = ListeDeCoursesService().ajouterUnIngredient(
                utilisateur.idUtilisateur, idIngredient, quantite
            )

            if succes:
                print(f"{ingredient_nom} ({quantite}) ajouté à la liste de courses.")
            else:
                print(f"Échec lors de l'ajout de {ingredient_nom} ({quantite}).")

    def ajouter_avis(self):
        """Permet d'ajouter un avis à la recette"""
        avis = inquirer.text(message="Entrez votre avis :").execute()
        note = inquirer.number(
            message="Entrez une note (sur 5) :",
            min_allowed=0,
            max_allowed=5,
        ).execute()

        AvisService().ajouterNouvelAvis(
            Session().utilisateur.idUtilisateur, self.recette.idRecette, note, avis
        )
        print(f"Votre avis a été ajouté à la recette {self.recette.titre}.")
