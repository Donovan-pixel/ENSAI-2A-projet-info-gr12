from InquirerPy import inquirer
from InquirerPy.validator import PasswordValidator
from service.utilisateur_service import UtilisateurService
from view.vue_abstraite import VueAbstraite
from view.session import Session
from utils.securite import hash_password


class ModifierProfilVue(VueAbstraite):
    """Vue pour modifier le profil utilisateur."""

    def choisir_menu(self):
        utilisateur = Session().utilisateur
        utilisateur_service = UtilisateurService()

        choix_modification = inquirer.select(
            message="Que souhaitez-vous modifier ?",
            choices=[
                "Changer mon pseudo",
                "Changer mon mot de passe",
                "Retourner au menu principal",
            ],
        ).execute()

        match choix_modification:
            case "Changer mon pseudo":
                # Demander le mot de passe actuel pour vérifier l'identité
                mot_de_passe_actuel = self.controle_user(utilisateur)
                if not mot_de_passe_actuel:
                    return self.choisir_menu()

                nouveau_pseudo = inquirer.text(
                    message="Entrez votre nouveau pseudo :",
                    validate=lambda x: len(x) > 0,
                ).execute()

                if utilisateur_service.pseudoDejaUtilise(nouveau_pseudo):
                    print(
                        f"❌ Le pseudo '{nouveau_pseudo}' est déjà utilisé."
                        "Veuillez en choisir un autre."
                    )
                    return self.choisir_menu()

                # Mise à jour
                utilisateur.pseudo = nouveau_pseudo
                utilisateur.motDePasse = mot_de_passe_actuel
                if utilisateur_service.modifier(utilisateur):
                    print(f"✅ Votre pseudo a été mis à jour avec succès en '{nouveau_pseudo}'.")
                    utilisateur = utilisateur_service.trouver_par_id(utilisateur.idUtilisateur)
                    Session().utilisateur = utilisateur
                    return self.choisir_menu()
                else:
                    print("❌ Une erreur s'est produite lors de la mise à jour de votre pseudo.")
                    return self.choisir_menu()

            case "Changer mon mot de passe":
                # Demander le mot de passe actuel pour vérifier l'identité
                mot_de_passe_actuel = self.controle_user(utilisateur)
                if not mot_de_passe_actuel:
                    return self.choisir_menu()

                nouveau_mdp = inquirer.secret(
                    message="Entrez votre nouveau mot de passe :",
                    validate=PasswordValidator(
                        length=8,
                        cap=True,
                        number=True,
                        message="Au moins 8 caractères, incluant une majuscule et un chiffre",
                    ),
                ).execute()

                # Mise à jour du mot de passe
                utilisateur.motDePasse = nouveau_mdp
                if utilisateur_service.modifier(utilisateur):
                    print("✅ Votre mot de passe a été mis à jour avec succès.")
                    utilisateur = utilisateur_service.trouver_par_id(utilisateur.idUtilisateur)
                    Session().utilisateur = utilisateur
                    return self.choisir_menu()
                else:
                    print(
                        "❌ Une erreur s'est produite lors de la mise à jour de votre mot de passe."
                    )
                    return self.choisir_menu()

            case "Retourner au menu principal":
                from view.menu_utilisateur_vue import MenuUtilisateurVue

                return MenuUtilisateurVue().choisir_menu()

    def controle_user(self, utilisateur) -> str:
        """Demande le mot de passe actuel et vérifie s'il est correct.

        Retourne le mot de passe actuel si valide, sinon False."""
        mot_de_passe_actuel = inquirer.secret(
            message="Entrez votre mot de passe actuel :",
            validate=PasswordValidator(
                length=8,
                cap=True,
                number=True,
                message="Au moins 8 caractères, incluant une majuscule et un chiffre",
            ),
        ).execute()

        pass_word_hash = hash_password(mot_de_passe_actuel, utilisateur.pseudo)
        if not pass_word_hash == utilisateur.motDePasse:
            print("❌ Mot de passe actuel incorrect. Vous ne pouvez pas modifier votre profil.")
            return False

        return mot_de_passe_actuel
