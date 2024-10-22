from unittest.mock import MagicMock

from service.avis_service import AvisService

from dao.avis_dao import AvisDao
from business_object.recette import Recette
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
    assert avis is not None  # Vérifie que l'avis a été créé
    assert avis is True  # Vérifie que la méthode renvoie bien True


def test_creer_echec():
    """Création d'Avis échouée"""

    # GIVEN*
    # idUtilisateur, idRecette, note, commentaire = 123, 12, 7, "plutôt bon"
    avis_dao_mock = MagicMock()
    AvisDao.__new__ = MagicMock(return_value=avis_dao_mock)  # Injection du mock

    avis_dao_mock.ajouter_avis.return_value = False  # Simule un échec de la DAO

    # WHEN
    avis = AvisService().ajouterNouvelAvis(avis_dao_mock)

    # THEN
    assert (
        avis is False
    )  # Vérifie que la méthode retourne True (ou ce que votre méthode retourne en cas d'échec)


# Créons une recette fictive pour le test
recette_test = Recette(
    titre="Recette Test",
    ingredientQuantite={"farine": "200g", "eau": "100ml"},
    consignes="Mélanger tous les ingrédients.",
    categorie="Dessert",
    origine="France",
    idRecette=1,
)


def test_obtenirAvisParRecette():
    """Test de la récupération des avis par recette"""

    # GIVEN
    avis_dao_mock = MagicMock()
    avis_service = AvisService()
    avis_service.AvisDao = avis_dao_mock  # Injection du mock

    avis_dao_mock.obtenirAvisParRecette.return_value = liste_avis  # Simule le retour de la DAO

    # WHEN
    result = avis_service.obtenirAvisParRecette(recette_test)

    # THEN
    assert len(result) == 2  # Vérifie qu'on obtient deux avis
    assert result[0].commentaire == "Excellente recette !"  # Vérifie le premier commentaire
    assert result[1].note == 4  # Vérifie la note du deuxième avis
    assert result[0].idUtilisateur == 1  # Vérifie l'ID utilisateur du premier avis
    assert result[1].idRecette == 1  # Vérifie l'ID de la recette du deuxième avis


def test_obtenirAvisParRecette_aucun_avis():
    """Test de la récupération des avis lorsqu'il n'y a pas d'avis"""

    # GIVEN
    avis_dao_mock = MagicMock()
    avis_service = AvisService()
    avis_service.AvisDao = avis_dao_mock  # Injection du mock

    avis_dao_mock.obtenirAvisParRecette.return_value = []  # Simule l'absence d'avis

    # WHEN
    result = avis_service.obtenirAvisParRecette(recette_test)

    # THEN
    assert len(result) == 0  # Vérifie qu'aucun avis n'est retourné


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
