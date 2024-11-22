from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from view.session import Session


class MenuAdministrateurVue(VueAbstraite):
    """Vue du menu de l'administrateur

    Attributes
    ----------
    None

    Returns
    ------
    view
        Retourne la prochaine vue, celle qui est choisie par l'administrateur
    """

    def choisir_menu(self):
        """Choix du menu suivant de l'administrateur

        Return
        ------
        vue
            Retourne la vue choisie par l'administrateur dans le terminal
        """

        print("\n" + "═" * 70)
        print(" Tableau de bord ".center(70))
        print("═" * 70 + "\n")

        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=[
                "Modérer les avis",
                "Supprimer un utilisateur",
                "Se déconnecter",
            ],
        ).execute()

        match choix:
            case "Se déconnecter":
                Session().deconnexion()
                from view.accueil.accueil_vue import AccueilVue

                return AccueilVue().choisir_menu()

            case "Modérer les avis":
                from view.ecrans.moderation_avis_vue import ModerationAvisVue

                return ModerationAvisVue().choisir_menu()

            case "Supprimer un utilisateur":
                from view.ecrans.suppression_utilisateur_vue import SuppressionUtilisateurVue

                return SuppressionUtilisateurVue().choisir_menu()
