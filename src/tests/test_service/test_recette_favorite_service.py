import pytest
from unittest import TestCase

from unittest.mock import patch, MagicMock

from src.business_object.recette import Recette

from src.service.recette_service import RecetteService


class TestRecetteFavoriteService(TestCase):

    def test_ajouter_recette_favorite(self):
        """teste l'ajout d'une recette favorite"""

    def test_supprimer_recette_favorite(self):
        """teste la suppression d'une recette favorite"""
