import sys
from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite


class AccueilVue(VueAbstraite):
    """Vue d'accueil de l'application"""

    def choisir_menu(self):
        """Choix du menu suivant

        Return
        ------
        view
            Retourne la vue choisie par l'utilisateur dans le terminal
        """                

        print(
            r"""
            ___  ___        _   ___ _       _                
            |  \/  |       | | / (_) |     | |               
            | .  . |_   _  | |/ / _| |_ ___| |__   ___ _ __  
            | |\/| | | | | |    \| | __/ __| '_ \ / _ \ '_ \ 
            | |  | | |_| | | |\  \ | || (__| | | |  __/ | | |
            \_|  |_/\__, | \_| \_/_|\__\___|_| |_|\___|_| |_|
                     __/ |                                   
                    |___/   
            """                              
        )


        print("\n" + "-" * 50 + "\nAccueil\n" + "-" * 50 + "\n")

        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=[
                "Se connecter",
                "Créer un compte",
                "Quitter",
            ],
        ).execute()

        match choix:
            case "Quitter":
                print("Merci d'avoir utilisé l'application. À bientôt !")
                sys.exit()

            case "Se connecter":
                from view.accueil.connexion_vue import ConnexionVue
                return ConnexionVue("Connexion à l'application")

            case "Créer un compte":
                from view.accueil.inscription_vue import InscriptionVue
                return InscriptionVue("Création de compte utilisateur")
