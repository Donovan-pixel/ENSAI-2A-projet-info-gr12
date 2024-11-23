from InquirerPy import inquirer
from view.vue_abstraite import VueAbstraite
from service.avis_service import AvisService
from view.menu_administrateur_vue import MenuAdministrateurVue


class ModerationAvisVue(VueAbstraite):
    """Vue qui affiche :
    - La liste des avis
    - La possibilité de supprimer un avis inaproprié
    """

    def __init__(self, message=""):
        self.message = message

    def choisir_menu(self):
        avis = AvisService().obtenirTousLesAvis()

        if not avis:
            print("\nAucun avis.\n")
            return MenuAdministrateurVue().choisir_menu()

        choix_avis = [
            {
                "name": f"ID: {avis.idAvis}, Note: {avis.note}/5, Commentaire: {avis.commentaire}",
                "value": avis.idAvis,
            }
            for avis in avis
        ]
        choix_avis.append({"name": "Retourner au tableau de bord", "value": None})

        id_avis_selectionne = inquirer.select(
            message="Sélectionnez un avis à modérer ou revenez au menu principal :",
            choices=choix_avis,
        ).execute()

        if id_avis_selectionne is None:
            return MenuAdministrateurVue().choisir_menu()

        self.gerer_avis(id_avis_selectionne)

    def gerer_avis(self, id_avis):
        """Permet de gérer un avis sélectionné (supprimer ou revenir)."""
        choix_action = inquirer.select(
            message="Que souhaitez-vous faire avec l'avis sélectionné ?",
            choices=[
                "Supprimer cet avis",
                "Revenir à la liste des avis",
            ],
        ).execute()

        match choix_action:
            case "Supprimer cet avis":
                self.supprimer_avis(id_avis)
            case "Revenir à la liste des avis":
                self.choisir_menu()

    def supprimer_avis(self, id_avis):
        """Supprime un avis après confirmation."""
        confirmation = inquirer.confirm(
            message="Êtes-vous sûr de vouloir supprimer l'avis sélectionné ?"
        ).execute()

        if confirmation:
            succes = AvisService().supprimerAvis(id_avis)
            if succes:
                print("L'avis a été supprimé avec succès.")
            else:
                print("Échec de la suppression de l'avis.")
        else:
            print("Suppression annulée.")

        self.choisir_menu()
