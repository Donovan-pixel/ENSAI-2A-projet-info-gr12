from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from view.session import Session
from service.recette_service import RecetteService

class FiltrageParLettreVue(VueAbstraite):
    """Vue pour filtrer les recettes par la première lettre du titre"""

    def __init__(self, message=""):
        self.message = message

    def choisir_menu(self):
        service_recette = RecetteService()

        # Demande à l'utilisateur de saisir une lettre
        lettre = inquirer.text(message="Entrez une lettre (A-Z) :").execute().upper()

        # Validation de l'entrée pour s'assurer que c'est une lettre valide
        if len(lettre) != 1 or not lettre.isalpha():
            print("Veuillez entrer une seule lettre valide.")
            return self.choisir_menu()

        # Récupération des recettes dont le titre commence par cette lettre
        recettes = service_recette.obtenirRecettesparLettre(lettre)

        # Si aucune recette ne correspond
        if not recettes:
            print(f"Aucune recette ne commence par la lettre {lettre}.")
            return self.choisir_menu()

        # Affichage des recettes filtrées
        self.afficher_recettes_filtrees(recettes)

    def afficher_recettes_filtrees(self, recettes):
        if not recettes:
            print("Aucune recette ne correspond à votre sélection.")
        else:
            choix_recettes = inquirer.select(
                message="Recettes correspondant à votre sélection :",
                choices=[recette.titre for recette in recettes] + ["Retourner au menu principal"],
            ).execute()

            if choix_recettes == "Retourner au menu principal":
                from view.menu_utilisateur_vue import MenuUtilisateurVue
                return MenuUtilisateurVue()

            # Affichage des détails ou ajout aux favoris
            recette = next(rec for rec in recettes if rec.titre == choix_recettes)
            choix_action = inquirer.select(
                message=f"Que souhaitez-vous faire avec {recette.titre} ?",
                choices=[
                    "Voir les détails de la recette",
                    "Ajouter cette recette aux favoris",
                    "Retourner à la liste des recettes",
                ],
            ).execute()

            match choix_action:
                case "Voir les détails de la recette":
                    service_recette = RecetteService()
                    details = service_recette.afficherRecette(recette)
                    print(details)
                case "Ajouter cette recette aux favoris":
                    from service.recette_favorites_service import RecetteFavoritesService
                    utilisateur = Session().utilisateur
                    RecetteFavoritesService().ajouter_recette_favorite(recette, utilisateur)
                    print(f"{recette.titre} a été ajoutée aux favoris.")
                case "Retourner à la liste des recettes":
                    return self.afficher_recettes_filtrees(recettes)
