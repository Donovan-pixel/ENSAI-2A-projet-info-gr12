from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from view.session import Session

from service.recette_favorites_service import RecetteFavoritesService
from service.recette_service import RecetteService


class RecettesFavoritesVue(VueAbstraite):
    """Vue qui affiche :
    - La liste des recettes favorites de l'utilisateur
    - La possibilité d'afficher les détails d'une recette
    - La possibilité d'ajouter ou de supprimer une recette de la liste
    """

    def __init__(self, message=""):
        self.message = message

    def choisir_menu(self):
        utilisateur = Session().utilisateur
        service_recettes_favorites = RecetteFavoritesService()

        recettes_favorites = service_recettes_favorites.obtenirRecettesFavorites(utilisateur)

        print("\n" + "-" * 50 + "\nVos recettes favorites\n" + "-" * 50 + "\n")

        if recettes_favorites:
            for i, recette in enumerate(recettes_favorites):
                print(f"{i + 1} -- {recette.titre} (Catégorie: {recette.categorie}, Origine: {recette.origine})")
        else:
            print("Vous n'avez aucune recette favorite.")

        choix = inquirer.select(
            message="Que voulez-vous faire ?",
            choices=[
                "Ajouter une recette aux favoris",
                "Supprimer une recette des favoris",
                "Retourner au menu principal",
            ],
        ).execute()

        match choix:
            case "Ajouter une recette aux favoris":
                self.ajouter_recette_favorite(service_recettes_favorites, utilisateur)
                return RecettesFavoritesVue("Recette ajoutée aux favoris.")

            case "Supprimer une recette des favoris":
                self.supprimer_recette_favorite(service_recettes_favorites, recettes_favorites, utilisateur)
                return RecettesFavoritesVue("Recette retirée des favoris.")

            case "Retourner au menu principal":
                from view.menu_utilisateur_vue import MenuUtilisateurVue
                return MenuUtilisateurVue()

    def afficher_details_recette(self, recette):
        """Afficher les détails complets d'une recette."""
        print(f"\n{'-' * 50}\nDétails de la recette : {recette.titre}\n{'-' * 50}")
        print(f"Catégorie : {recette.categorie}")
        print(f"Origine : {recette.origine}")
        print(f"Ingrédients : {', '.join([ingredient.nom for ingredient in recette.ingredients])}")
        print(f"Instructions : {recette.instructions}\n")

    def ajouter_recette_favorite(self, service_recettes_favorites, utilisateur):
        recettes = RecetteService().obtenirToutesLesRecettes()
        recette_choisie = inquirer.select(
            message="Choisissez une recette à ajouter aux favoris :",
            choices=[recette.titre for recette in recettes]
        ).execute()

        recette = next(rec for rec in recettes if rec.titre == recette_choisie)
        service_recettes_favorites.ajouter_recette_favorite(recette, utilisateur)

    def supprimer_recette_favorite(self, service_recettes_favorites, recettes_favorites, utilisateur):
        recette_choisie = inquirer.select(
            message="Choisissez une recette à retirer des favoris :",
            choices=[recette.titre for recette in recettes_favorites]
        ).execute()

        recette = next(rec for rec in recettes_favorites if rec.titre == recette_choisie)
        service_recettes_favorites.supprimer_recette_favorite(recette, utilisateur)
