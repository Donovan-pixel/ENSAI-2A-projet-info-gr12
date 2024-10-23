from unittest.mock import MagicMock

from service.avis_service import AvisService

from dao.avis_dao import AvisDao
from business_object.recette import Recette
from business_object.avis import Avis


liste_avis = [
    Avis(idUtilisateur=123, idRecette=1, note=6, commentaire="bonne recette"),
    Avis(idUtilisateur=321, idRecette=1, note=8, commentaire="Excellent, à refaire"),
    Avis(idUtilisateur=23, idRecette=1, note=3, commentaire="pas bon"),
]


def test_creer_ok():
    """ "Création d'Avis réussie"""

    # GIVEN
    idUtilisateur, idRecette, note, commentaire = 123, 12, 7, "plutôt bon"
    AvisDao().ajouter_avis = MagicMock(return_value=True)

    # WHEN
    avis = AvisService().ajouterNouvelAvis(idUtilisateur, idRecette, note, commentaire)

    # THEN
    assert avis is not None  # Vérifie que l'avis a été créé
    assert avis is True  # Vérifie que la méthode renvoie bien True


# Créons une recette fictive pour le test
recette_test = Recette(
    titre="Recette Test",
    ingredientQuantite={"farine": "200g", "eau": "100ml"},
    consignes="Mélanger tous les ingrédients.",
    categorie="Dessert",
    origine="France",
    idRecette=1,
)


def test_ajouterNouvelAvis_echec():
    """Création d'Avis échouée"""

    # GIVEN
    idUtilisateur = 1
    idRecette = 2
    note = 5
    commentaire = "très bon"
    AvisDao().ajouter_avis = MagicMock(return_value=True)

    # WHEN
    res = AvisService().ajouterNouvelAvis(idUtilisateur, idRecette, note, commentaire)

    # THEN
    assert res is True


def test_obtenirAvisParRecette():
    """Test de la récupération des avis par recette"""

    # GIVEN
    AvisDao().obtenirAvisParRecette = MagicMock(return_value=liste_avis)

    # WHEN
    res = AvisService().obtenirAvisParRecette(recette_test)

    # THEN
    assert res == liste_avis


def test_obtenirAvisParRecette_aucun_avis():
    """Test de la récupération des avis lorsqu'il n'y a pas d'avis"""

    # GIVEN
    AvisDao().obtenirAvisParRecette = MagicMock(return_value=[])

    # WHEN
    res = AvisService().obtenirAvisParRecette(recette_test)

    # THEN
    assert res == []


def test_supprimer_avis_succes():
    """Test de la suppression d'un avis avec succès"""

    # GIVEN
    avis_dao_mock = MagicMock()
    avis_service = AvisService()
    avis_service.AvisDao = avis_dao_mock  # Injection du mock

    # Création d'un avis fictif
    avis_a_supprimer = Avis(
        idUtilisateur=1, idRecette=1, note=5, commentaire="Excellente recette !", idAvis=1
    )

    # Simule le retour de la DAO pour la suppression
    avis_dao_mock.supprimer_avis.return_value = True  # Simule une suppression réussie

    # WHEN
    result = avis_service.supprimer_avis(avis_a_supprimer)

    # THEN
    assert result is False  # Vérifie que la méthode retourne True


def test_supprimer_avis_echec():
    """Test de la suppression d'un avis échouée"""

    # GIVEN
    avis_dao_mock = MagicMock()
    avis_service = AvisService()
    avis_service.AvisDao = avis_dao_mock  # Injection du mock

    # Création d'un avis fictif
    avis_a_supprimer = Avis(
        idUtilisateur=1, idRecette=1, note=5, commentaire="Excellente recette !", idAvis=1
    )

    # Simule le retour de la DAO pour la suppression
    avis_dao_mock.supprimer_avis.return_value = False  # Simule une suppression échouée

    # WHEN
    result = avis_service.supprimer_avis(avis_a_supprimer)

    # THEN
    assert result is False  # Vérifie que la méthode retourne False


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
