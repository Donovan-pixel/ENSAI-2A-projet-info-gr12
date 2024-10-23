import pytest
from unittest import TestCase

from unittest.mock import patch, MagicMock

from src.business_object.recette import Recette

from src.service.recette_favorite_service import RecetteFavoritesService

from src.dao.recette_favorite_dao import RecettesFavoritesDao

from src.business_object.utilisateur import Utilisateur


class TestRecetteFavoriteService(TestCase):

    @patch("dao.recette_favorite_dao.RecettesFavoritesDao.ajouter_recette_favorite")
    def test_ajouter_recette_favorite(self):
        """teste l'ajout d'une recette favorite"""

        rec_fav_service = RecetteFavoritesService()
        recette = Recette(
            idRecette=1,
            titre="Recette Test",
            ingredientQuantite="2 pommes",
            consignes="Couper et cuire",
            categorie="Dessert",
            origine="France",
        )

        utilisateur = Utilisateur(pseudo="Jean", motDePasse="0000", role="utilisateur")
        RecettesFavoritesDao().ajouter_recette_favorite = MagicMock(recette, utilisateur)
        # WHEN
        resultat = rec_fav_service.ajouter_recette_favorite(recette, utilisateur)

        # THEN
        RecettesFavoritesDao().ajouter_recette_favorite.assert_called_once_with(
            recette, utilisateur
        )
        assert resultat is True

    @patch("dao.recette_favorite_dao.RecettesFavoritesDao.supprimer_recette_favorite")
    def test_supprimer_recette_favorite(self):
        """teste la suppression d'une recette favorite"""

        rec_fav_service = RecetteFavoritesService()
        recette = Recette(
            idRecette=1,
            titre="Recette Test",
            ingredientQuantite="2 pommes",
            consignes="Couper et cuire",
            categorie="Dessert",
            origine="France",
        )

        utilisateur = Utilisateur(pseudo="Jean", motDePasse="0000", role="utilisateur")
        RecettesFavoritesDao().supprimer_recette_favorite = MagicMock(recette, utilisateur)
        # WHEN
        resultat = rec_fav_service.supprimer_recette_favorite(recette, utilisateur)

        # THEN
        RecettesFavoritesDao().supprimer_recette_favorite.assert_called_once_with(
            recette, utilisateur
        )
        assert resultat is True

    @patch("dao.recette_favorite_dao.RecettesFavoritesDao.obtenirRecettesFavorite")
    def test_obtenirRecettesFavorites(self):
        """teste l'obtention de la liste des recette favorites"""

        rec_fav_service = RecetteFavoritesService()
        recette = Recette(
            idRecette=1,
            titre="Recette Test",
            ingredientQuantite="2 pommes",
            consignes="Couper et cuire",
            categorie="Dessert",
            origine="France",
        )

        utilisateur = Utilisateur(pseudo="Jean", motDePasse="0000", role="utilisateur")
        RecettesFavoritesDao().obtenirRecettesFavorites = MagicMock(recette, utilisateur)
        # WHEN
        resultat = rec_fav_service.obtenirRecettesFavorites(recette, utilisateur)

        # THEN
        RecettesFavoritesDao().obtenirRecettesFavorites.assert_called_once_with(utilisateur)
        assert isinstance(resultat, list)
        assert len(resultat) == 1
        assert resultat[0].nom == "Tarte aux pommes"


if __name__ == "__main__":
    # Run the tests

    pytest.main([__file__])
