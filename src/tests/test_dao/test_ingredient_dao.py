import pytest

from unittest.mock import patch
from unittest.mock import MagicMock

from dao.ingredient_dao import IngredientDao
from business_object.ingredient import Ingredient


@patch("dao.db_connection.DBConnection")
def test_ajouterIngredient_succes(mock_db):

    # GIVEN un ingrédient à ajouter et un base de données

    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1,)  # L'ingrédient est ajouté avec succès
    mock_db().connection.__enter__().cursor.return_value = mock_cursor

    ingredient = Ingredient(nom="Tomate")

    # WHEN : on tente d'ajouter l'ingrédient

    res = IngredientDao().ajouterIngredient(ingredient)

    # THEN

    assert res is True


@patch("dao.db_connection.DBConnection")
def test_ajouterIngredient_echec(mock_db):

    # GIVEN

    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None  # L'ajout échoue
    mock_db().connection.__enter__().cursor.return_value = mock_cursor

    ingredient = Ingredient(nom="Tomate")

    # WHEN

    res = IngredientDao().ajouterIngredient(ingredient)

    # THEN

    assert res is False


@patch("dao.db_connection.DBConnection")
def test_obtenirTousLesIngredients_succes(mock_db):

    # GIVEN

    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        {"id_ingredient": 1, "nom": "Tomate"},
        {"id_ingredient": 2, "nom": "Carotte"},
    ]
    mock_db().connection.__enter__().cursor.return_value = mock_cursor

    # WHEN

    res = IngredientDao().obtenirTousLesIngredients()

    # THEN

    assert len(res) == 2
    assert res[0].nom == "Tomate"
    assert res[1].nom == "Carotte"


@patch("dao.db_connection.DBConnection")
def test_obtenirTousLesIngredients_echec(mock_db):

    # GIVEN

    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = []
    mock_db().connection.__enter__().cursor.return_value = mock_db

    # WHEN

    res = IngredientDao().obtenirTousLesIngredients()

    # THEN

    assert res == []


@patch("dao.db_connection.DBConnection")
def test_supprimerIngredient_succes(mock_db):

    # GIVEN

    mock_cursor = MagicMock()
    mock_cursor.rowcount = 1  # Suppression réussie
    mock_db().connection.__enter__().cursor.return_value = mock_cursor

    ingredient = Ingredient(nom="Tomate")

    # WHEN

    res = IngredientDao().supprimerIngredient(ingredient)

    # THEN

    assert res is True


@patch("dao.db_connection.DBConnection")
def test_supprimerIngredient_echec(mock_db):

    # GIVEN

    mock_cursor = MagicMock()
    mock_cursor.rowcount = 0  # Aucune ligne supprimée
    mock_db().connection.__enter__().cursor.return_value = mock_cursor

    ingredient = Ingredient(idIngredient=1, nom="Tomate")

    # WHEN

    res = IngredientDao().supprimerIngredient(ingredient)

    # THEN

    assert res is False


@patch("dao.db_connection.DBConnection")
def test_obtenirIdParNom_succes(mock_db):

    # GIVEN

    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1,)
    mock_db().connection.__enter__().cursor.return_value = mock_cursor

    # WHEN

    res = IngredientDao().obtenirIdParNom("Tomate")

    # THEN

    assert res == 1


@patch("dao.db_connection.DBConnection")
def test_obtenirIdParNom_echec(mock_db):

    # GIVEN

    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_db().connection.__enter__().cursor.return_value = mock_cursor

    # WHEN

    res = IngredientDao().obtenirIdParNom("Tomate")

    # THEN

    assert res is None


if __name__ == "__main__":
    pytest.main([__file__])
