import os
import pytest

from unittest.mock import patch

from utils.reset_database import ResetDatabase

from dao.avis_dao import AvisDao

from business_object.avis import Avis


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialisation des données de test"""
    with patch.dict(os.environ, {"SCHEMA": "projet_test_dao"}):
        ResetDatabase().lancer(test_dao=True)
        yield


def test_obtenirAvisParRecette():
    """Vérifie que la méthode renvoie une liste de Avis"""

    # GIVEN

    # WHEN
    avis = AvisDao().obtenirAvisParRecette()

    # THEN
    assert isinstance(avis, list)
    for a in avis:
        assert isinstance(a, Avis)


def test_ajouter_avis():
    """Ajout avis réussie"""

    # GIVEN
    avis = Avis(
        idUtilisateur=123, idRecette=34, note=7, commentaire="un commentaire pour faire joli"
    )

    # WHEN
    creation_ok = AvisDao().ajouter_avis(avis)

    # THEN
    assert creation_ok
    assert avis.idAvis


def test_creer_ko():
    """Création d'un avis échouée (commentaire et note incorrect)"""

    # GIVEN
    avis = Avis(idUtilisateur=123, idRecette=34, note="12", commentaire=123)

    # WHEN
    creation_ok = AvisDao().ajouter_avis(avis)

    # THEN
    assert not creation_ok


def test_supprimer_ok():
    """Suppression d'un avis réussie"""

    # GIVEN
    avis = Avis(idUtilisateur=995, idRecette=333, note=9, comentaire="un commentaire")

    # WHEN
    suppression_ok = AvisDao().supprimer_avis(avis)

    # THEN
    assert suppression_ok


def test_supprimer_ko():
    """Suppression d'un avis échouée (idRecette inconnu)"""

    # GIVEN
    avis = Avis(idUtilisateur=8888, idRecette=333, note=6, commentaire="idRecette inconnu")

    # WHEN
    suppression_ok = AvisDao().supprimer_avis(avis)

    # THEN
    assert not suppression_ok


if __name__ == "__main__":
    pytest.main([__file__])
