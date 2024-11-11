from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from view.vue_abstraite import VueAbstraite
from view.session import Session

from service.recette_favorite_service import RecetteFavoritesService
from service.recette_service import RecetteService


class RecettesFavoritesVue(VueAbstraite):
    """Vue qui affiche :
    - La liste des recettes favorites de l'utilisateur
    - La possibilité d'afficher les détails d'une recette
    - Ajouter et supprimer des recettes favorites
    """

    def __init__(self, message=""):
        self.message = message

    def choisir_menu(self):
        utilisateur = Session().utilisateur
        service_recettes_favorites = RecetteFavoritesService()

        recettes_favorites = service_recettes_favorites.obtenirRecettesFavorites(utilisateur)

        print("\n" + "═" * 70)
        print(" Vos recettes favorites ".center(70))
        print("═" * 70 + "\n")

        if not recettes_favorites:
            print("Vous n'avez aucune recette favorite.\n")

        choix_recettes = [Choice(recette.titre) for recette in recettes_favorites] + [
            Choice("Ajouter une recette aux favoris"),
            Choice("Supprimer une recette des favoris"),
            Choice("Retourner au menu principal"),
        ]

        choix = inquirer.select(
            message="Sélectionnez une recette pour afficher les détails ou une action :",
            choices=choix_recettes,
            vi_mode=True,
        ).execute()

        if choix == "Retourner au menu principal":
            from view.menu_utilisateur_vue import MenuUtilisateurVue

            return MenuUtilisateurVue()

        if choix == "Ajouter une recette aux favoris":
            self.ajouter_recette_favorite(service_recettes_favorites, utilisateur)
            return RecettesFavoritesVue("Recette ajoutée aux favoris.")

        # Si l'utilisateur choisit "Supprimer une recette des favoris"
        if choix == "Supprimer une recette des favoris":
            self.supprimer_recette_favorite(
                service_recettes_favorites, recettes_favorites, utilisateur
            )
            return RecettesFavoritesVue("Recette retirée des favoris.")

        # Trouver la recette sélectionnée et afficher ses détails
        recette_choisie = next((rec for rec in recettes_favorites if rec.titre == choix), None)

        if recette_choisie:
            from view.ecrans.details_recette_vue import DetailsRecetteVue

            return DetailsRecetteVue(recette_choisie).choisir_menu()

        return RecettesFavoritesVue()

    def ajouter_recette_favorite(self, service_recettes_favorites, utilisateur):
        """Ajouter une recette aux favoris."""
        recettes = RecetteService().obtenirToutesLesRecettes()
        recette_choisie = inquirer.select(
            message="Choisissez une recette à ajouter aux favoris :",
            choices=[recette.titre for recette in recettes],
        ).execute()

        recette = next(rec for rec in recettes if rec.titre == recette_choisie)
        service_recettes_favorites.ajouter_recette_favorite(recette, utilisateur)

    def supprimer_recette_favorite(
        self, service_recettes_favorites, recettes_favorites, utilisateur
    ):
        """Supprimer une recette des favoris."""
        recette_choisie = inquirer.select(
            message="Choisissez une recette à retirer des favoris :",
            choices=[recette.titre for recette in recettes_favorites],
        ).execute()

        recette = next(rec for rec in recettes_favorites if rec.titre == recette_choisie)
        service_recettes_favorites.supprimer_recette_favorite(recette, utilisateur)
