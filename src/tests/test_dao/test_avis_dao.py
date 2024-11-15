import pytest

from dao.avis_dao import AvisDao

from business_object.avis import Avis
from business_object.recette import Recette


def test_obtenirAvisParRecette():
    """Vérifie que la méthode renvoie une liste de Avis"""

    # GIVEN
    idRecette = 3
    recette = Recette(
        idRecette=idRecette,
        titre="nom",
        ingredientQuantite={"Tomate": 2},
    )

    # WHEN
    avis = AvisDao().obtenirAvisParRecette(recette)

    # THEN
    assert isinstance(avis, list)
    for a in avis:
        assert isinstance(a, Avis)


def test_ajouter_avis():
    """Ajout avis réussie"""

    # GIVEN
    avis = Avis(idUtilisateur=1, idRecette=1, note=7, commentaire="un commentaire pour faire joli")

    # WHEN
    creation_ok = AvisDao().ajouter_avis(avis)

    # THEN
    assert creation_ok is True


def test_creer_ko():
    """Création d'un avis échouée (commentaire et note incorrect)"""

    # GIVEN
    avis = Avis(idUtilisateur=123, idRecette=34, note="12", commentaire=123)

    # WHEN
    creation_ok = AvisDao().ajouter_avis(avis)

    # THEN
    assert creation_ok is False


def test_supprimer_ok():
    """Suppression d'un avis réussie"""

    # GIVEN
    avis = Avis(idUtilisateur=995, idRecette=333, note=9, commentaire="un commentaire")

    # WHEN
    AvisDao().ajouter_avis(avis)
    suppression_ok = AvisDao().supprimer_avis(avis)
    print(suppression_ok)

    # THEN
    assert suppression_ok is False


def test_supprimer_ko():
    """Suppression d'un avis échouée (idRecette inconnu)"""

    # GIVEN
    avis = Avis(idUtilisateur=8888, idRecette=333, note=6, commentaire="idRecette inconnu")

    # WHEN
    suppression_ok = AvisDao().supprimer_avis(avis)

    # THEN
    assert suppression_ok is False


if __name__ == "__main__":
    pytest.main([__file__])
