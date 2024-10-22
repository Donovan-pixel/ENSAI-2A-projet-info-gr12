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
    """ "Création d'utilisateur réussie"""

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
    joueur = JoueurService().creer(pseudo, mdp, age, mail, fan_pokemon)

    # THEN
    assert joueur is None


def test_lister_tous_inclure_mdp_true():
    """Lister les Joueurs en incluant les mots de passe"""

    # GIVEN
    JoueurDao().lister_tous = MagicMock(return_value=liste_joueurs)

    # WHEN
    res = JoueurService().lister_tous(inclure_mdp=True)

    # THEN
    assert len(res) == 3
    for joueur in res:
        assert joueur.mdp is not None


def test_lister_tous_inclure_mdp_false():
    """Lister les Joueurs en excluant les mots de passe"""

    # GIVEN
    JoueurDao().lister_tous = MagicMock(return_value=liste_joueurs)

    # WHEN
    res = JoueurService().lister_tous()

    # THEN
    assert len(res) == 3
    for joueur in res:
        assert not joueur.mdp


def test_pseudo_deja_utilise_oui():
    """Le pseudo est déjà utilisé dans liste_joueurs"""

    # GIVEN
    pseudo = "lea"

    # WHEN
    JoueurDao().lister_tous = MagicMock(return_value=liste_joueurs)
    res = JoueurService().pseudo_deja_utilise(pseudo)

    # THEN
    assert res


def test_pseudo_deja_utilise_non():
    """Le pseudo n'est pas utilisé dans liste_joueurs"""

    # GIVEN
    pseudo = "chaton"

    # WHEN
    JoueurDao().lister_tous = MagicMock(return_value=liste_joueurs)
    res = JoueurService().pseudo_deja_utilise(pseudo)

    # THEN
    assert not res


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
