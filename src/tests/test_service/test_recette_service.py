from unittest import TestCase

from unittest.mock import patch, MagicMock

from business_object.recette import Recette

from service.recette_service import RecetteService

from dao.recette_dao import RecetteDao

from business_object.ingredient import Ingredient

recettes_exemples = [
    Recette(
        idRecette=1,
        titre="Recette Test 1",
        ingredientQuantite={"pomme": 2, "Tomate": 2},
        consignes="Couper et cuire",
        categorie="Entrée",
        origine="France",
    ),
    Recette(
        idRecette=2,
        titre="Recette Test 2",
        ingredientQuantite={"bananes": 3},
        consignes="Mixer",
        categorie="Boisson",
        origine="Brésil",
    ),
    Recette(
        idRecette=3,
        titre="Recette Test",
        ingredientQuantite={"pommes": 2, "Avocat": 1},
        consignes="Couper et cuire",
        categorie="Dessert",
        origine="France",
    ),
    Recette(
        idRecette=4,
        titre="Recette Test 3",
        ingredientQuantite={"bananes": 3, "Carotte": 3},
        consignes="Mixer",
        categorie="Boisson",
        origine="Brésil",
    ),
    Recette(
        idRecette=5,
        titre="Recette Test 4",
        ingredientQuantite={"Carotte": 2, "Tomate": 2},
        consignes="Couper et cuire",
        categorie="Dessert",
        origine="France",
    ),
]


class TestRecetteService(TestCase):

    @patch("service.recette_service.RecetteDao.ajouterRecette")
    def test_ajouterNouvelleRecette_succes(self, mock_ajouter_recette):
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
        RecetteDao().ajouterRecette = MagicMock(return_value=True)

        # WHEN
        result = recette_service.ajouterNouvelleRecette(recette)

        # THEN
        self.assertTrue(result)

    @patch("dao.recette_dao.RecetteDao.ajouterRecette")
    def test_nouvellerecette_echec(self, mock_ajouter_recette_echec):
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
        mock_ajouter_recette_echec.return_value = False

        # WHEN

        result = recette_service.ajouterNouvelleRecette(recette)

        # THEN
        self.assertIsNone(result)

    def test_afficherRecette(self):
        """Vérifier l'affichage d'une recette"""

        # GIVEN
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
        resultat = RecetteService().afficherRecette(recette)

        # THEN
        self.assertEqual(resultat, sortie_attendu)

    @patch("dao.recette_dao.RecetteDao.obtenirToutesLesRecettes")
    def test_obtenirToutesLesRecettes(self, mock_obtenirtouteslesrecettes):
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
        mock_obtenirtouteslesrecettes.return_value = [recette1, recette2]

        # WHEN
        resultat = RecetteService().obtenirToutesLesRecettes()

        # THEN
        self.assertEqual(resultat, [recette1, recette2])  # Vérifier que le retour est correct
        self.assertTrue(isinstance(resultat, list))  # Vérifier que c'est une liste
        self.assertEqual(len(resultat), 2)  # Vérifier que deux recettes sont retournées
        self.assertEqual(
            resultat[0].titre, "Recette Test 1"
        )  # Vérifier que la première recette a le bon titre
        self.assertEqual(
            resultat[1].titre, "Recette Test 2"
        )  # Vérifier que la deuxième recette a le bon titre

    @patch("dao.recette_dao.RecetteDao.obtenirRecettesparLettre")
    def test_obtenirRecettesparLettre(self, mock_obtenirrecetteparlettre):
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
        mock_obtenirrecetteparlettre.return_value = [recette]

        # WHEN
        result = recette_service.obtenirRecettesparLettre("R")

        # THEN
        self.assertEqual(result, [recette])

    @patch("dao.recette_dao.RecetteDao.obtenirRecettesParIngredient")
    def test_obtenirRecettesParIngredient(self, mock_obtenirparingredient):
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
        ingredient = Ingredient(nom="Pommes")
        mock_obtenirparingredient.return_value = [recette]
        # WHEN

        result = recette_service.obtenirRecettesParIngredient(ingredient)

        # THEN
        self.assertEqual(result, [recette])

    @patch("dao.recette_dao.RecetteDao.obtenirRecettesParIngredients")
    def test_obtenirRecettesParIngredients(self, mock_obtenirparingredients):
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
        ingredients = [Ingredient(nom="Pommes")]
        mock_obtenirparingredients.return_value = [recette]

        # WHEN
        result = recette_service.obtenirRecettesParIngredients(ingredients)

        # THEN
        self.assertEqual(result, [recette])

    @patch("dao.recette_dao.RecetteDao.obtenirRecettesParCategorie")
    def test_obtenirRecettesParCategorie(self, mock_obtenirRecettesParCategorie):
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
        mock_obtenirRecettesParCategorie.return_value = [recette]
        # WHEN
        result = recette_service.obtenirRecettesParCategorie("Dessert")

        # THEN
        self.assertEqual(result, [recette])

    @patch("dao.recette_dao.RecetteDao.obtenirToutesLesCategories")
    def test_obtenirToutesLesCategories(self, mock_obtenirToutesLesCategories):
        """Teste que la fonction renvoie bien les catégories de repas"""

        # GIVEN
        categories = ["Dessert", "Boisson", "Entrée"]
        mock_obtenirToutesLesCategories.return_value = categories

        # WHEN
        res = RecetteService().obtenirToutesLesCategories()

        # THEN
        assert isinstance(res, list)
        for i in res:
            assert isinstance(i, str)


if __name__ == "__main__":
    # Run the tests
    import pytest

    pytest.main([__file__])
