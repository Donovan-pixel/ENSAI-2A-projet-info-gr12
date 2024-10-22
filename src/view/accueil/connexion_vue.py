from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from view.session import Session
from view.menu_administrateur_vue import MenuAdministrateurVue
from view.menu_utilisateur_vue import MenuUtilisateurVue
from view.accueil.accueil_vue import AccueilVue

from src.service.utilisateur_service import UtilisateurService


class ConnexionVue(VueAbstraite):
    """Vue de Connexion (saisie de pseudo et mdp)"""

    def choisir_menu(self):
        # Demande à l'utilisateur de saisir pseudo et mot de passe
        pseudo = inquirer.text(message="Entrez votre pseudo : ").execute()
        mdp = inquirer.secret(message="Entrez votre mot de passe :").execute()

        # Appel du service pour trouver l'utilisateur
        user = UtilisateurService().seConnecter(pseudo, mdp)

        # Si l'utilisateur a été trouvé à partir des ses identifiants de connexion
        if user:
            message = f"Vous êtes connecté sous le pseudo {user.pseudo}"
            Session().connexion(user)

            if user.role == "Administrateur":
                return MenuAdministrateurVue(message)

            return MenuUtilisateurVue(message)

        message = "Erreur de connexion (pseudo ou mot de passe invalide)"

        return AccueilVue(message)
