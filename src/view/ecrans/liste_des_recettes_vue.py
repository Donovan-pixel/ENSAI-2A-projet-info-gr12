from InquirerPy import inquirer
from InquirerPy.separator import Separator

from view.vue_abstraite import VueAbstraite
from view.session import Session

from service.recette_service import RecetteService
from service.recette_favorite_service import RecetteFavoritesService


class ListeDesRecettesVue(VueAbstraite):
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

        filtre_choix = inquirer.select(
            message="Comment souhaitez-vous filtrer les recettes ?",
            choices=[
                Separator("-----------------------"),
                "Par ingrédient",
                "Par catégorie",
                "Par lettre",
                Separator("-----------------------"),
                "Afficher toutes les recettes",
                Separator("-----------------------"),
                "Retourner au tableau de bord",
            ],
        ).execute()

        if filtre_choix == "Par ingrédient":
            from view.ecrans.filtrage_ingredients_vue import FiltrageParIngredientsVue

            return FiltrageParIngredientsVue()

        elif filtre_choix == "Par catégorie":
            from view.ecrans.filtrage_categorie_vue import FiltrageParCategorieVue

            return FiltrageParCategorieVue()

        elif filtre_choix == "Par lettre":
            from view.ecrans.filtrage_lettre_vue import FiltrageParLettreVue

            return FiltrageParLettreVue()

        elif filtre_choix == "Afficher toutes les recettes":
            recettes = service_recette.obtenirToutesLesRecettes()

        elif filtre_choix == "Retourner au tableau de bord":
            from view.menu_utilisateur_vue import MenuUtilisateurVue

            return MenuUtilisateurVue()

        if not recettes:
            print("Aucune recette trouvée pour ce filtre.")
            return self.choisir_menu()

        recette_choisie = inquirer.select(
            message="Sélectionnez une recette ou retournez au menu principal :",
            choices=[recette.titre for recette in recettes] + ["Retourner au tableau de bord"],
        ).execute()

        if recette_choisie == "Retourner au tableau de bord":
            from view.menu_utilisateur_vue import MenuUtilisateurVue

            return MenuUtilisateurVue()

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
            from view.ecrans.details_recette_vue import DetailsRecetteVue

            return DetailsRecetteVue(recette)

        elif action_choix == "Ajouter cette recette aux favoris":
            service_recette_favorites.ajouter_recette_favorite(recette, utilisateur)
            print(f"Recette {recette.titre} ajoutée aux favoris !")
            return self.choisir_menu()

        elif action_choix == "Retourner à la liste des recettes":
            return self.choisir_menu()
