from unittest.mock import MagicMock

from src.business_object.recette import Recette

from src.service.recette_service import RecetteService

from src.dao.recette_dao import RecetteDao

#on remplace la DAO par le mock
RecetteService(). RecetteDao = MagicMock

#exemple de recette et d'ingrédient
recette = Recette(
            idRecette=1,
            titre="Recette Test",
            ingredientQuantite="2 pommes",
            consignes="Couper et cuire",
            categorie="Dessert",
            origine="France")

def test_nouvellerecette_succes():
    """Ajout d'une nouvelle recette réussie"""

    # Configurer le mock pour simuler un ajout réussi
    self.mock_dao.ajouterRecette.return_value = True

    # Appel de la méthode
    result = self.service.ajouterNouvelleRecette(self.recette)

    # Vérification que la méthode a retourné True
    self.assertTrue(result)

        # Vérification que la méthode ajouterRecette a été appelée avec la bonne recette
        self.mock_dao.ajouterRecette.assert_called_once_with(self.recette)

def test_nouvellerecette_echec():
    """Ajout d'une nouvelle recette échouée
    car la méthode recetteDAO.ajouter renvoie FAlse"""

def test_afficherRecette():
    """Vérifier l'affichage d'une recette"""

    #GIVEN
    output = "Recette(1, Recette Test, 2 pommes, Couper et cuire, Dessert, France)"

    #WHEN
    resultat = RecetteService().afficherRecette(recette)

    #THEN
    assertEqual(output, resultat)

def test_obtenirRecettesparLettre():
    """Teste de l'affichage d'une recette par lettre """

    result = self.service.obtenirRecettesparLettre('R')
    self.assertEqual(result, [self.recette])

def test_obtenirRecettesParIngredient():

def test_obtenirRecettesParIngrédients():

if __name__ == "__main__":
    import pytest

    pytest.main([__file__])