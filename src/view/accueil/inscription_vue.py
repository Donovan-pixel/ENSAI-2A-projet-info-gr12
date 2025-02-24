from InquirerPy import inquirer
from InquirerPy.validator import PasswordValidator, EmptyInputValidator

from prompt_toolkit.validation import ValidationError, Validator


from view.vue_abstraite import VueAbstraite
from service.utilisateur_service import UtilisateurService


class InscriptionVue(VueAbstraite):
    def choisir_menu(self):
        # Demande à l'utilisateur de saisir pseudo, mot de passe...
        pseudo = inquirer.text(message="Entrez votre pseudo : ").execute()

        if UtilisateurService().pseudoDejaUtilise(pseudo):
            from view.accueil.accueil_vue import AccueilVue

            return InscriptionVue(f"Le pseudo {pseudo} est déjà utilisé.")

        mdp = inquirer.secret(
            message="Entrez votre mot de passe : ",
            validate=PasswordValidator(
                length=8,
                cap=True,
                number=True,
                message="Au moins 8 caractères, incluant une majuscule et un chiffre",
            ),
        ).execute()

        role = "Utilisateur"

        # Appel du service pour créer le l'utilisateur
        user = UtilisateurService().creerUnCompte(pseudo, mdp, role)

        # Si l'utilisateur a été créé
        if user:
            message = f"Votre compte {pseudo} a été créé. Vous pouvez maintenant vous connecter."
        else:
            message = "Erreur de connexion (pseudo ou mot de passe invalide)"

        return AccueilVue(message)
