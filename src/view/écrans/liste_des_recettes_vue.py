from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from view.session import Session

from service.recette_service import RecetteService
from service.recette_favorites_service import RecetteFavoritesService


class ListeRecettesVue(VueAbstraite):
    """Vue qui affiche :
    - La liste des recettes
    - La possibilité de filtrer les recettes par ingrédients/catégorie/lettre
    """

    def __init__(self, message=""):
        self.message = message

    def choisir_menu(self):
        utilisateur = Session().utilisateur
        service_recette = RecetteService()
        service_recette_favorites = RecetteFavoritesService()

        # Step 1: Ask user for filter preference
        filtre_choix = inquirer.select(
            message="Comment souhaitez-vous filtrer les recettes ?",
            choices=[
                "Par ingrédient",
                "Par catégorie",
                "Par lettre",
                "Afficher toutes les recettes",
                "Retourner au menu principal",
            ],
        ).execute()

        if filtre_choix == "Par ingrédient":
            from filtrage_ingredients_vue import FiltrageParIngredientsVue
            return FiltrageParIngredientsVue()
            
        elif filtre_choix == "Par catégorie":
            categorie = inquirer.text(message="Entrez une catégorie de recette :").execute()
            recettes = service_recette.obtenirRecettesParCategorie(categorie)

        elif filtre_choix == "Par lettre":
            lettre = inquirer.text(message="Entrez la première lettre de la recette :").execute()
            recettes = service_recette.obtenirRecettesparLettre(lettre)

        elif filtre_choix == "Afficher toutes les recettes":
            recettes = service_recette.obtenirToutesLesRecettes()

        elif filtre_choix == "Retourner au menu principal":
            from view.menu_utilisateur_vue import MenuUtilisateurVue
            return MenuUtilisateurVue()

        # If no recipes found after filtering
        if not recettes:
            print("Aucune recette trouvée pour ce filtre.")
            return self.choisir_menu()

        # Step 2: Display recipes and allow the user to interact with them
        recette_choisie = inquirer.select(
            message="Sélectionnez une recette ou retournez au menu principal :",
            choices=[recette.titre for recette in recettes] + ["Retourner au menu principal"],
        ).execute()

        if recette_choisie == "Retourner au menu principal":
            from view.menu_utilisateur_vue import MenuUtilisateurVue
            return MenuUtilisateurVue()

        # Step 3: After choosing a recipe, offer to view details or add to favorites
        recette = next(rec for rec in recettes if rec.titre == recette_choisie)

        action_choix = inquirer.select(
            message=f"Que souhaitez-vous faire avec {recette.titre} ?",
            choices=[
                "Voir les détails de la recette",
                "Ajouter cette recette aux favoris",
                "Retourner à la liste des recettes",
            ],
        ).execute()

        if action_choix == "Voir les détails de la recette":
            self.afficher_details_recette(recette)
            return self.choisir_menu()

        elif action_choix == "Ajouter cette recette aux favoris":
            service_recette_favorites.ajouter_recette_favorite(recette, utilisateur)
            print(f"Recette {recette.titre} ajoutée aux favoris !")
            return self.choisir_menu()

        elif action_choix == "Retourner à la liste des recettes":
            return self.choisir_menu()

    def afficher_details_recette(self, recette):
        """Afficher les détails d'une recette"""
        print(f"\nDétails de la recette : {recette.titre}")
        print(f"Catégorie: {recette.categorie}")
        print(f"Origine: {recette.origine}")
        print("Ingrédients:")
        for ingredient, quantite in recette.ingredients.items():
            print(f"- {ingredient}: {quantite}")
        print("Instructions:")
        for i, instruction in enumerate(recette.instructions, 1):
            print(f"{i}. {instruction}")
        input("\nAppuyez sur Entrée pour retourner à la liste des recettes...")
