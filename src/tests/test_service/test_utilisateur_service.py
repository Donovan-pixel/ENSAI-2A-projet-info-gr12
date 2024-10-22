from unittest.mock import MagicMock

from service.utilisateur_service import UtilisateurService

from dao.utilisateur_dao import UtilisateurDao

from business_object.utilisateur import Utilisateur


liste_utilisateur = [
    Utilisateur(pseudo="jp", role="Utilisateur", motDePasse="1234"),
    Utilisateur(pseudo="lea", age="Utilisateur", motDePasse="0000"),
    Utilisateur(pseudo="gg", age="Utilisateur", motDePasse="abcd"),
]


def test_creer_ok():
    """Création d'utilisateur réussie"""

    # GIVEN
    pseudo, role, motDePasse = "jp", "Utilisateur", "1234"
    UtilisateurDao().creer = MagicMock(return_value=True)

    # WHEN
    utilisateur = UtilisateurService().creerUnCompte(pseudo, role, motDePasse)

    # THEN
    assert utilisateur.pseudo == pseudo


def test_creer_echec():
    """Création d'utilisateur échouée
    (car la méthode UtilisateurDao().creer retourne False)"""

    # GIVEN
    pseudo, role, motDePasse = "jp", "Utilisateur", "1234"
    UtilisateurDao().creer = MagicMock(return_value=False)

    # WHEN
    utilisateur = UtilisateurService().creerUnCompte(pseudo, role, motDePasse)

    # THEN
    assert utilisateur is None


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
    res = UtilisateurService().lister_tous()

    # THEN
    assert len(res) == 3
    for utilisateur in res:
        assert not utilisateur.motDePasse


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


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
