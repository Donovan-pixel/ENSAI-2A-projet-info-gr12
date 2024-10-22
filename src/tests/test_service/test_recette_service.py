import unittest

from unittest import TestCase, mock

from unittest.mock import patch, MagicMock

from src.business_object.recette import Recette

from src.service.recette_service import RecetteService

from src.dao.recette_dao import RecetteDao

from src.business_object.ingredient import Ingredient


class TestRecetteService(unittest.TestCase):

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
        RecetteDao().ajouterRecette = unittest.mock.MagicMock(return_value=True)

        # WHEN
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
        RecetteDao().ajouterRecette = unittest.mock.MagicMock(return_value=False)

        # WHEN

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

        recette1 = Recette(
            idRecette=1,
            titre="Recette Test 1",
            ingredientQuantite="2 pommes",
            consignes="Couper et cuire",
            categorie="Dessert",
            origine="France",
        )
        recette2 = Recette(
            idRecette=2,
            titre="Recette Test 2",
            ingredientQuantite="3 bananes",
            consignes="Mixer",
            categorie="Boisson",
            origine="Brésil",
        )

        # GIVEN
        RecetteDao().obtenirToutesLesRecettes = MagicMock(return_value=[recette1, recette2])

        # WHEN
        resultat = RecetteService().obtenirToutesLesRecettes()

        # THEN
        self.assertEqual(
            resultat, [self.recette1, self.recette2]
        )  # Vérifier que le retour est correct
        self.assertTrue(isinstance(result, list))  # Vérifier que c'est une liste
        self.assertEqual(len(result), 2)  # Vérifier que deux recettes sont retournées
        self.assertEqual(
            resultat[0].titre, "Recette Test 1"
        )  # Vérifier que la première recette a le bon titre
        self.assertEqual(
            resultat[1].titre, "Recette Test 2"
        )  # Vérifier que la deuxième recette a le bon titre

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
        RecetteDao().obtenirRecettesparLettre = unittest.mock.MagicMock(return_value=[recette])

        # WHEN
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
        RecetteDao().obtenirRecettesParIngredient = unittest.mock.MagicMock(return_value=[recette])
        # WHEN

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
        RecetteDao().obtenirRecettesParIngredients = unittest.mock.MagicMock(return_value=[recette])

        # WHEN
        result = recette_service.obtenirRecettesParIngrédients(ingredients)

        # THEN
        self.assertEqual(result, [recette])

    @patch("dao.recette_dao.RecetteDao.obtenirRecettesParCategorie")
    def test_obtenirRecettesParCategorie(self):
        """Teste l'affichage des recettes selon une catégorie donnée"""

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


if __name__ == "__main__":
    # Run the tests
    import pytest

    pytest.main([__file__])
