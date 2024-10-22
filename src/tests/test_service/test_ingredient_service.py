import pytest

from unittest import TestCase

from unittest.mock import patch, MagicMock

from src.service.ingredient_service import IngredientService

from src.dao.ingredient_dao import IngredientDao

from src.business_object.ingredient import Ingredient


class TestIngredientService(TestCase):
    """Classe pour tester les ingrédients service"""

    @patch("dao.ingredient_dao.IngredientDao.ajouterIngredient")
    def test_ajouterNouvelIngredient_succes(self):
        """Teste le succès de l'ajout d'un nouvel ingrédient"""
        ingredient_service = IngredientService()

        # GIVEN
        nom_ingredient = "Tomate"
        IngredientDao().ajouterIngredient = MagicMock(return_value=True)

        # WHEN
        resultat = ingredient_service.ajouterNouvelIngredient(nom_ingredient)

        # THEN
        assert resultat is True

    @patch("dao.ingredient_dao.IngredientDao.ajouterIngredient")
    def test_ajouterNouvelIngredient_echec(self):
        """Teste l'échec de l'ajout d'un nouvel ingrédient"""
        ingredient_service = IngredientService()

        # GIVEN
        nom_ingredient = "Tomate"
        IngredientDao().ajouterIngredient = MagicMock(return_value=False)

        # WHEN
        resultat = ingredient_service.ajouterNouvelIngredient(nom_ingredient)

        # THEN
        assert resultat is False

    @patch("dao.ingredient_dao.IngredientDao.obtenirTousLesIngredients")
    def test_obtenirTousLesIngredients(self):
        """Teste l'obtention de tous les ingrédients"""
        # GIVEN
        ingredient_service = IngredientService()
        ingredient1 = Ingredient(id=1, nom="Tomate")
        ingredient2 = Ingredient(id=2, nom="Pomme")
        IngredientDao().obtenirTousLesIngredients = MagicMock(
            return_value=[ingredient1, ingredient2]
        )

        # WHEN
        result = ingredient_service.obtenirTousLesIngredients()

        # THEN
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0].nom == "Tomate"
        assert result[1].nom == "Pomme"

    @patch("dao.ingredient_dao.IngredientDao.supprimerIngredient")
    def test_supprimer(self):
        """Teste la suppression d'un ingrédient"""

        # GIVEN
        ingredient_service = IngredientService()
        ingredient = Ingredient(id=1, nom="Tomate")
        IngredientDao().supprimerIngredient = MagicMock(return_value=True)

        # WHEN
        result = ingredient_service.supprimer(ingredient)

        # THEN
        assert result is True

    @patch("dao.ingredient_dao.IngredientDao.obtenirIdParNom")
    def test_obtenirIdPArNom(self):
        """Teste l'obtention de l'id d'un ingrédient par son nom"""
        # GIVEN
        ingredient_service = IngredientService()
        nom_ingredient = "Tomate"
        IngredientDao().obtenirIdParNom = MagicMock(return_value=1)

        # WHEN
        result = ingredient_service.obtenirIdPArNom(nom_ingredient)

        # THEN
        assert result == 1


if __name__ == "__main__":
    # Lancer les tests
    pytest.main([__file__])
