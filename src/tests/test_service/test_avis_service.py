from unittest.mock import MagicMock

from service.avis_service import AvisService

from dao.avis_dao import AvisDao

from business_object.avis import Avis


liste_avis = [
    Avis(idUtilisateur=123, idRecette=34, note=6, commentaire="bonne recette"),
    Avis(idUtilisateur=321, idRecette=12, note=8, commentaire="Excellent, à refaire"),
    Avis(idUtilisateur=23, idRecette=5, note=3, commentaire="pas bon"),
]


def test_creer_ok():
    """ "Création d'Avis réussie"""

    # GIVEN
    idUtilisateur, idRecette, note, commentaire = 123, 12, 7, "plutôt bon"
    AvisDao().ajouter_avis = MagicMock(return_value=True)

    # WHEN
    avis = AvisService().ajouterNouvelAvis(idUtilisateur, idRecette, note, commentaire)

    # THEN
    assert avis.commentaire == commentaire


def test_creer_echec():
    """Création d'avis échouée
    (car la méthode AvisDao().ajouter_avis retourne False)"""

    # GIVEN
    idUtilisateur, idRecette, note, commentaire = 123, 12, 7, "plutôt bon"
    AvisDao().ajouter_avis = MagicMock(return_value=False)

    # WHEN
    avis = AvisService().ajouterNouvelAvis(idUtilisateur, idRecette, note, commentaire)

    # THEN
    assert avis is None


def test_obtenirAvisParRecette():
    """Lister les avis pour une recette"""

    # GIVEN
    recette = random.choice(RecetteService().obtenirToutesLesRecettes())
    AvisDao().obtenirAvisParRecette = MagicMock(return_value=liste_avis)

    # WHEN
    res = AvisService().obtenirAvisParRecette(recette)

    # THEN
    assert len(res) == 3
    for avis in res:
        assert avis.mdp is not None


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
