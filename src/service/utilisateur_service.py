from tabulate import tabulate

from utils.log_decorator import log
from utils.securite import hash_password

from business_object.utilisateur import Utilisateur
from dao.utilisateur_dao import UtilisateurDao
from dao.recettes_favorites_dao import RecettesFavoritesDao


class UtilisateurService:
    """Classe contenant les méthodes de service des Utilisateurs"""

    @log
    def creerUnCompte(
        self,
        pseudo,
        motDePasse,
        role,
        ingredients_favoris,
        recettes_favorites,
        ingredients_non_desires,
    ) -> bool:
        """Création d'un utilisateur à partir de ses attributs"""

        nouvel_utilisateur = Utilisateur(
            pseudo=pseudo,
            motDePasse=hash_password(motDePasse, pseudo),
            role=role,
        )

        return True if UtilisateurDao().creer(nouvel_utilisateur) else False

    @log
    def lister_tous(self, inclure_mdp=False) -> list[Utilisateur]:
        """Lister tous les utilisateurs
        Si inclure_mdp=True, les mots de passe seront inclus
        Par défaut, tous les mdp des utilisateurs sont à None
        """
        utilisateurs = UtilisateurDao().lister_tous()
        if not inclure_mdp:
            for user in utilisateurs:
                user.mot_de_Passe = None
        return utilisateurs

    @log
    def trouver_par_id(self, idUtilisateur) -> Utilisateur:
        """Trouver un utilisateur à partir de son id"""
        return UtilisateurDao().trouver_par_id(idUtilisateur)

    @log
    def modifier(self, utilisateur) -> Utilisateur:
        """Modification d'un utilisateur"""

        utilisateur.mdp = hash_password(utilisateur.motDePasse, utilisateur.pseudo)
        return utilisateur if UtilisateurDao().modifier(utilisateur) else None

    @log
    def supprimerUnCompte(self, utilisateur) -> bool:
        """Supprimer le compte d'un utilisateur"""
        return UtilisateurDao().supprimer(utilisateur)

    @log
    def afficher_tous(self) -> str:
        """Afficher tous les utilisateurs
        Sortie : Une chaine de caractères mise sous forme de tableau
        """
        entetes = ["pseudo", "role"]

        utilisateurs = UtilisateurDao().lister_tous()

        for user in utilisateurs:
            if user.role == "admin":
                utilisateurs.remove(user)

        utilisateurs_as_list = [user.as_list() for user in utilisateurs]

        str_utilisateurs = "-" * 100
        str_utilisateurs += "\nListe des utilisateurs \n"
        str_utilisateurs += "-" * 100
        str_utilisateurs += "\n"
        str_utilisateurs += tabulate(
            tabular_data=utilisateurs_as_list,
            headers=entetes,
            tablefmt="psql",
            floatfmt=".2f",
        )
        str_utilisateurs += "\n"

        return str_utilisateurs

    @log
    def seConnecter(self, pseudo, motDePasse) -> Utilisateur:
        """Se connecter à partir de pseudo et mdp"""
        return UtilisateurDao().se_connecter(pseudo, hash_password(motDePasse, pseudo))

    @log
    def pseudoDejaUtilise(self, pseudo) -> bool:
        """Vérifie si le pseudo est déjà utilisé
        Retourne True si le pseudo existe déjà en BDD"""
        utilisateurs = UtilisateurDao().lister_tous()
        return pseudo in [user.pseudo for user in utilisateurs]

    def seDeconnecter(self) -> None:
        """Permet à l'utilisateur de se déconnecter et de revenir à l'écran d'acceuil"""
        return view.ecran_acceuil
