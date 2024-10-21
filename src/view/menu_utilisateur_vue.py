from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from view.session import Session

from service.utilisateur_service import UtilisateurService
from service.recette_service import RecetteService

class MenuUtilisateurVue(VueAbstraite):
    """Vue du menu du joueur

    Attributes
    ----------
    message=''
        str

    Returns
    ------
    view
        retourne la prochaine vue, celle qui est choisie par l'utilisateur
    """

    def choisir_menu(self):
        """Choix du menu suivant de l'utilisateur

        Return
        ------
        vue
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        print("\n" + "-" * 50 + "\nTableau de bord\n" + "-" * 50 + "\n")

        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=[
                "Afficher la liste des recettes",
                "Voir mes recettes favorites",
                "Gérer mes ingrédients favoris/non désirés",
                "Obtenir des suggestions de recettes",
                "Accéder à ma liste de courses"
                "Se déconnecter",
            ],
        ).execute()

        match choix:
            case "Se déconnecter":
                Session().deconnexion()
                from view.accueil.accueil_vue import AccueilVue
                return AccueilVue()

            case "Afficher la liste des recettes":
                recettes_str = RecetteService().afficherTous()

            case "Gérer mes ingrédients favoris/non désirés":

            case "Obtenir des suggestions de recettes": 

            case "Accéder à ma liste de courses":
                liste_de_courses_str = 
                return 

            case "Infos de session":
                return MenuUtilisateurVue(Session().afficher())

            case "Afficher les joueurs de la base de données":
                joueurs_str = JoueurService().afficher_tous()
                return MenuUtilisateurVue(joueurs_str)

            case "Afficher des pokemons (par appel à un Webservice)":
                from view.pokemon_vue import PokemonVue
                return PokemonVue()
