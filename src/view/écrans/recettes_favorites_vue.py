from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from view.vue_abstraite import VueAbstraite
from view.session import Session

from service.recette_favorites_service import RecetteFavoritesService
from service.recette_service import RecetteService


class RecettesFavoritesVue(VueAbstraite):
    """Vue qui affiche :
    - La liste des recettes favorites de l'utilisateur
    - La possibilité d'afficher les détails d'une recette
    - Ajouter et supprimer des recettes aux favoris
    """

    def __init__(self, message=""):
        self.message = message

    def choisir_menu(self):
        utilisateur = Session().utilisateur
        service_recettes_favorites = RecetteFavoritesService()

        # Obtenir les recettes favorites de l'utilisateur
        recettes_favorites = service_recettes_favorites.obtenirRecettesFavorites(utilisateur)

        # Vérification de l'existence de recettes favorites
        if not recettes_favorites:
            print("Vous n'avez aucune recette favorite.")
            return self.retourner_menu_principal()

        print("\n" + "-" * 50 + "\nVos recettes favorites\n" + "-" * 50 + "\n")

        # Créer une liste d'options avec les titres des recettes
        choix_recettes = [
            Choice(recette.titre, extra_data=recette) for recette in recettes_favorites
        ] + [Choice("Ajouter une recette aux favoris"), Choice("Supprimer une recette des favoris"), Choice("Retourner au menu principal")]

        # Sélectionner une recette ou une action
        choix = inquirer.select(
            message="Sélectionnez une recette pour afficher les détails ou une action :",
            choices=choix_recettes,
            vi_mode=True  # Active le mode de navigation avec vi (optionnel)
        ).execute()

        # Si l'utilisateur choisit "Retourner au menu principal"
        if choix == "Retourner au menu principal":
            return self.retourner_menu_principal()

        # Si l'utilisateur choisit "Ajouter une recette aux favoris"
        if choix == "Ajouter une recette aux favoris":
            self.ajouter_recette_favorite(service_recettes_favorites, utilisateur)
            return RecettesFavoritesVue("Recette ajoutée aux favoris.")

        # Si l'utilisateur choisit "Supprimer une recette des favoris"
        if choix == "Supprimer une recette des favoris":
            self.supprimer_recette_favorite(service_recettes_favorites, recettes_favorites, utilisateur)
            return RecettesFavoritesVue("Recette retirée des favoris.")

        # Trouver la recette sélectionnée et afficher ses détails
        recette_choisie = next(
            (rec for rec in recettes_favorites if rec.titre == choix), None
        )

        if recette_choisie:
            self.afficher_details_recette(recette_choisie)

        # Revenir à la vue des recettes favorites après avoir affiché les détails
        return RecettesFavoritesVue()

    def afficher_details_recette(self, recette):
        """Afficher les détails complets d'une recette."""
        print(f"\n{'-' * 50}\nDétails de la recette : {recette.titre}\n{'-' * 50}")
        print(f"Catégorie : {recette.categorie}")
        print(f"Origine : {recette.origine}")
        print(f"Ingrédients : {', '.join([ingredient.nom for ingredient in recette.ingredients])}")
        print(f"Instructions : {recette.instructions}\n")

        inquirer.confirm(message="Appuyez sur Entrée pour revenir au menu", default=True).execute()

    def ajouter_recette_favorite(self, service_recettes_favorites, utilisateur):
        """Ajouter une recette aux favoris."""
        recettes = RecetteService().obtenirToutesLesRecettes()
        recette_choisie = inquirer.select(
            message="Choisissez une recette à ajouter aux favoris :",
            choices=[recette.titre for recette in recettes]
        ).execute()

        recette = next(rec for rec in recettes if rec.titre == recette_choisie)
        service_recettes_favorites.ajouter_recette_favorite(recette, utilisateur)

    def supprimer_recette_favorite(self, service_recettes_favorites, recettes_favorites, utilisateur):
        """Supprimer une recette des favoris."""
        recette_choisie = inquirer.select(
            message="Choisissez une recette à retirer des favoris :",
            choices=[recette.titre for recette in recettes_favorites]
        ).execute()

        recette = next(rec for rec in recettes_favorites if rec.titre == recette_choisie)
        service_recettes_favorites.supprimer_recette_favorite(recette, utilisateur)

    def retourner_menu_principal(self):
        """Retourner au menu principal."""
        from view.menu_utilisateur_vue import MenuUtilisateurVue
        return MenuUtilisateurVue()
