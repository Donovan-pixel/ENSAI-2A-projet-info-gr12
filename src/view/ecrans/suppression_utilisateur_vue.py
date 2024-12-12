from InquirerPy import inquirer
from view.vue_abstraite import VueAbstraite
from service.utilisateur_service import UtilisateurService
from view.menu_administrateur_vue import MenuAdministrateurVue


class SuppressionUtilisateurVue(VueAbstraite):
    """Vue qui affiche :
    - La liste des utilisateurs
    - La possibilité de supprimer un utilisateur
    """

    def __init__(self, message=""):
        self.message = message

    def choisir_menu(self):
        utilisateurs = UtilisateurService().lister_tous()
        utilisateurs.pop(0)

        if not utilisateurs:
            print("\nAucun utilisateur trouvé.\n")
            return MenuAdministrateurVue().choisir_menu()

        choix_utilisateurs = [
            {
                "name": f"ID: {u.idUtilisateur}, Nom: {u.pseudo}",
                "value": u.idUtilisateur,
            }
            for u in utilisateurs
        ]
        choix_utilisateurs.append({"name": "Revenir au tableau de bord", "value": None})

        id_utilisateur_selectionne = inquirer.select(
            message="Sélectionnez un utilisateur à supprimer ou revenez au tableau de bord :",
            choices=choix_utilisateurs,
        ).execute()

        if id_utilisateur_selectionne is None:
            return MenuAdministrateurVue().choisir_menu()

        self.confirmer_suppression(id_utilisateur_selectionne)

    def confirmer_suppression(self, id_utilisateur):
        confirmation = inquirer.confirm(
            message="Êtes-vous sûr de vouloir supprimer cet utilisateur ?"
        ).execute()

        if confirmation:
            succes = UtilisateurService().supprimerUnCompte(id_utilisateur)
            if succes:
                print("L'utilisateur a été supprimé avec succès.")
            else:
                print("Échec de la suppression de l'utilisateur.")
        else:
            print("Suppression annulée.")

        self.choisir_menu()
