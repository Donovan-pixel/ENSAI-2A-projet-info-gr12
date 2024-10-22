import unittest
from unittest import TestCase, mock
from unittest.mock import patch, MagicMock

from src.business_object.recette import Recette

from src.service.recette_service import RecetteService

from src.business_object.ingredient import Ingredient


class TestRecetteService(TestCase):

    @patch("service.recette_service.RecetteDao.ajouterRecette")
    def test_ajouterNouvelleRecette_succes(self):
        """Ajout d'une nouvelle recette réussie"""

        # GIVEN
        recette_service = RecetteService()
        recette = Recette(
            idRecette=1,
            titre="Recette Test",
            ingredientQuantite="2 pommes",
            consignes="Couper et cuire",
            categorie="Dessert",
            origine="France",
        )

        # WHEN
        mock_ajouterRecette.return_value = True
        result = recette_service.ajouterNouvelleRecette(recette)

        # THEN
        self.assertTrue(result)

    @patch("dao.recette_dao.RecetteDao.ajouterRecette")
    def test_nouvellerecette_echec(self):
        """Ajout d'une nouvelle recette échouée
        car la méthode recetteDAO.ajouter renvoie FAlse"""

        # GIVEN
        recette_service = RecetteService()
        recette = Recette(
            idRecette=1,
            titre="Recette Test",
            ingredientQuantite="2 pommes",
            consignes="Couper et cuire",
            categorie="Dessert",
            origine="France",
        )

        # WHEN
        mock_ajouterRecette.return_value = False
        result = recette_service.ajouterNouvelleRecette(recette)

        # THEN
        self.assertIsNone(result)

    def test_afficherRecette(self):
        """Vérifier l'affichage d'une recette"""

        # GIVEN
        recette_service = RecetteService()
        recette = Recette(
            idRecette=1,
            titre="Recette Test",
            ingredientQuantite="2 pommes",
            consignes="Couper et cuire",
            categorie="Dessert",
            origine="France",
        )

        # WHEN
        sortie_attendu = "Recette(1, Recette Test, 2 pommes, Couper et cuire, Dessert, France)"
        resultat = recette_service.afficherRecette(recette)

        # THEN
        self.assertEqual(resultat, sortie_attendu)

    @patch("dao.recette_dao.RecetteDao.obtenirToutesLesRecettes")
    def test_obtenirToutesLesRecettes(self):
        """Teste l'obtention de toutes les recettes de la base de données"""

    @patch("dao.recette_dao.RecetteDao.obtenirRecettesparLettre")
    def test_obtenirRecettesparLettre(self):
        """Teste de l'affichage d'une recette par lettre"""

        # GIVEN
        recette_service = RecetteService()
        recette = Recette(
            idRecette=1,
            titre="Recette Test",
            ingredientQuantite="2 pommes",
            consignes="Couper et cuire",
            categorie="Dessert",
            origine="France",
        )

        # WHEN
        mock_obtenirRecettesparLettre.return_value = [recette]
        result = recette_service.obtenirRecettesparLettre("R")

        # THEN
        self.assertEqual(result, [recette])

    @patch("dao.recette_dao.RecetteDao.obtenirRecettesParIngredient")
    def test_obtenirRecettesParIngredient(self):
        """Teste l'affichage des recettes qui ont un ingrédient spécifique"""
        # GIVEN
        recette_service = RecetteService()
        recette = Recette(
            idRecette=1,
            titre="Recette Test",
            ingredientQuantite="2 pommes",
            consignes="Couper et cuire",
            categorie="Dessert",
            origine="France",
        )
        ingredient = Ingredient(id=1, nom="Pommes")

        # WHEN
        mock_obtenirRecettesParIngredient.return_value = [recette]
        result = recette_service.obtenirRecettesParIngredient(ingredient)

        # THEN
        self.assertEqual(result, [recette])

    @patch("dao.recette_dao.RecetteDao.obtenirRecettesParIngredients")
    def test_obtenirRecettesParIngrédients(self):
        """Teste l'affichage des recettes selon des ingrédients"""
        # GIVEN
        recette_service = RecetteService()
        recette = Recette(
            idRecette=1,
            titre="Recette Test",
            ingredientQuantite="2 pommes",
            consignes="Couper et cuire",
            categorie="Dessert",
            origine="France",
        )
        ingredients = [Ingredient(id=1, nom="Pommes")]

        # WHEN
        mock_obtenirRecettesParIngrédients.return_value = [recette]
        result = recette_service.obtenirRecettesParIngrédients(ingredients)

        # THEN
        self.assertEqual(result, [recette])

    @patch("dao.recette_dao.RecetteDao.obtenirRecettesParCategorie")
    def test_obtenirRecettesParCategorie(self):
        """Teste l'affichage des recettes selon une catégorie donnée"""


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
