from unittest.mock import MagicMock

from service.utilisateur_service import UtilisateurService

from dao.utilisateur_dao import UtilisateurDao

from business_object.utilisateur import Utilisateur


liste_utilisateur = [
    Utilisateur(idUtilisateur=1, pseudo="jp", role="Utilisateur", motDePasse="1234"),
    Utilisateur(idUtilisateur=2, pseudo="lea", role="Utilisateur", motDePasse="0000"),
    Utilisateur(idUtilisateur=3, pseudo="gg", role="Utilisateur", motDePasse="abcd"),
]


def test_creer_ok():
    """Création d'utilisateur réussie"""

    # GIVEN
    pseudo, role, motDePasse = "jp", "Utilisateur", "1234"
    UtilisateurDao().creer = MagicMock(return_value=True)

    # WHEN
    utilisateur = UtilisateurService().creerUnCompte(pseudo, role, motDePasse)

    # THEN
    assert utilisateur is True


def test_creer_echec():
    """Création d'utilisateur échouée
    (car la méthode UtilisateurDao().creer retourne False)"""

    # GIVEN
    pseudo, role, motDePasse = "jp", "Utilisateur", "1234"
    UtilisateurDao().creer = MagicMock(return_value=False)

    # WHEN
    utilisateur = UtilisateurService().creerUnCompte(pseudo, role, motDePasse)

    # THEN
    assert utilisateur is False


def test_lister_tous_inclure_mdp_true():
    """Lister les Utilisateurs en incluant les mots de passe"""

    # GIVEN
    UtilisateurDao().lister_tous = MagicMock(return_value=liste_utilisateur)

    # WHEN
    res = UtilisateurService().lister_tous(inclure_mdp=True)

    # THEN
    assert len(res) == 3
    for utilisateur in res:
        assert utilisateur.motDePasse is not None


def test_lister_tous_inclure_mdp_false():
    """Lister les utilisateurs en excluant les mots de passe"""

    # GIVEN
    UtilisateurDao().lister_tous = MagicMock(return_value=liste_utilisateur)

    # WHEN
    res = UtilisateurService().lister_tous(inclure_mdp=False)

    # THEN
    assert len(res) == 3
    for user in res:
        assert user.mot_de_Passe is None


def test_pseudo_deja_utilise_oui():
    """Le pseudo est déjà utilisé dans liste_utilisateur"""

    # GIVEN
    pseudo = "lea"

    # WHEN
    UtilisateurDao().lister_tous = MagicMock(return_value=liste_utilisateur)
    res = UtilisateurService().pseudoDejaUtilise(pseudo)

    # THEN
    assert res


def test_pseudo_deja_utilise_non():
    """Le pseudo n'est pas utilisé dans liste_utilisateur"""

    # GIVEN
    pseudo = "chaton"

    # WHEN
    UtilisateurDao().lister_tous = MagicMock(return_value=liste_utilisateur)
    res = UtilisateurService().pseudoDejaUtilise(pseudo)

    # THEN
    assert not res


def test_trouver_par_id_ok():
    """l'id existe bien dans la bdd"""

    # GIVEN
    idUtilisateur = 123
    utilisateur = Utilisateur(
        idUtilisateur=123, pseudo="jp", motDePasse="ipzuferf", role="Utilisateur"
    )
    UtilisateurDao().trouver_par_id = MagicMock(return_value=utilisateur)

    # WHEN
    res = UtilisateurService().trouver_par_id(idUtilisateur)

    # THEN
    assert res == utilisateur


def test_modifier_ok():
    """Modification d'un utilisateur réussie pour le pseudo"""

    # GIVEN
    utilisateur = Utilisateur(
        idUtilisateur=1, pseudo="jean-pierre", role="Utilisateur", motDePasse="1234"
    )
    UtilisateurDao().modifier = MagicMock(return_value=True)

    # WHEN
    res = UtilisateurService().modifier(utilisateur=utilisateur)

    # THEN
    assert res is True


def test_modifier_echec():
    """Modification d'un utilisateur échouée pour un mauvais identifiant"""

    # GIVEN
    utilisateur = Utilisateur(
        idUtilisateur=56, pseudo="jean-pierre", role="Utilisateur", motDePasse="1234"
    )
    UtilisateurDao().modifier = MagicMock(return_value=False)

    # WHEN
    res = UtilisateurService().modifier(utilisateur=utilisateur)

    # THEN
    assert res is False


def test_supprimerUnCompte_ok():
    """Suppression d'un compte réussie"""

    # GIVEN
    utilisateur = liste_utilisateur[0]
    UtilisateurDao().supprimer = MagicMock(return_value=True)

    # WHEN
    res = UtilisateurService().supprimerUnCompte(utilisateur)

    # THEN
    assert res is True


def test_supprimerUnCompte_echec():
    """Suppression d'un compte échouée pour mauvais identifiant"""

    # GIVEN
    utilisateur = Utilisateur(
        idUtilisateur=56, pseudo="jean-pierre", role="Utilisateur", motDePasse="1234"
    )
    UtilisateurDao().supprimer = MagicMock(return_value=False)

    # WHEN
    res = UtilisateurService().supprimerUnCompte(utilisateur)

    # THEN
    assert res is False


def test_seConnecter_ok():
    """Connexion à un compte ok"""

    # GIVEN
    pseudo = "jp"
    motDePasse = "1234"
    utilisateur = liste_utilisateur[0]
    UtilisateurDao().se_connecter = MagicMock(return_value=utilisateur)

    # WHEN
    res = UtilisateurService().seConnecter(pseudo, motDePasse)

    # THEN
    assert res == utilisateur


def test_seConnecter_echec():
    """Connexion à un compte échouée mauvais pseudo"""

    # GIVEN
    pseudo = "zltjhietf"
    motDePasse = "1234"
    UtilisateurDao().se_connecter = MagicMock(return_value=None)

    # WHEN
    res = UtilisateurService().seConnecter(pseudo, motDePasse)

    # THEN
    assert res is None


def test_pseudoDejaUtilise_oui():
    """Le pseudo est indisponible"""

    # GIVEN
    pseudo = "jp"
    UtilisateurDao().lister_tous = MagicMock(return_value=liste_utilisateur)

    # WHEN
    res = UtilisateurService().pseudoDejaUtilise(pseudo)

    # THEN
    assert res is True


def test_pseudoDejaUtilise_non():
    """Le pseudo est disponible"""

    # GIVEN
    pseudo = "koen"
    UtilisateurDao().lister_tous = MagicMock(return_value=liste_utilisateur)

    # WHEN
    res = UtilisateurService().pseudoDejaUtilise(pseudo)

    # THEN
    assert res is False


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
