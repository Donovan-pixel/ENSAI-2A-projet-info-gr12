from utils.log_decorator import log
from utils.securite import hash_password

from business_object.utilisateur import Utilisateur
from dao.utilisateur_dao import UtilisateurDao


class UtilisateurService:
    """Classe contenant les méthodes de service des Utilisateurs"""

    @log
    def creerUnCompte(
        self,
        pseudo,
        motDePasse,
        role,
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

        utilisateur.motDePasse = hash_password(utilisateur.motDePasse, utilisateur.pseudo)
        return UtilisateurDao().modifier(utilisateur)

    @log
    def supprimerUnCompte(self, id_utilisateur: int) -> bool:
        """Supprimer le compte d'un utilisateur"""
        return UtilisateurDao().supprimer(id_utilisateur)

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
