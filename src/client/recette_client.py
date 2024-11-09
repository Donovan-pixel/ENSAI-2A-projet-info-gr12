import os
import requests
import string
import logging
from utils.log_decorator import log
from typing import List, Dict
from dotenv import load_dotenv


class RecetteClient:
    """Fait appel à mealdb endpoint"""

    def __init__(self) -> None:
        load_dotenv()
        self.__host = os.getenv("WEBSERVICE_HOST")

    @log
    def get_recette(self) -> List[Dict]:
        """Retourne la liste des recettes"""
        recettes = []

        for letter in string.ascii_lowercase:
            try:
                response = requests.get(f"{self.__host}/search.php?f={letter}")
                response.raise_for_status()
            except requests.RequestException as e:
                logging.error(
                    f"Échec de la récupération des recettes" f"pour la lettre '{letter}': {e}"
                )

            raw_recettes = response.json().get("meals")

            if not raw_recettes:
                logging.info(f"Aucune recette trouvée pour la lettre '{letter}'.")
                continue

            for t in raw_recettes:
                try:
                    ingredients = {
                        t.get(f"strIngredient{i}"): t.get(f"strMeasure{i}", "")
                        for i in range(1, 21)
                        if t.get(f"strIngredient{i}")
                    }

                    recettes.append(
                        {
                            "titre": t.get("strMeal", "Unknown Title"),
                            "categorie": t.get("strCategory", "Uncategorized"),
                            "origine": t.get("strArea", "Unknown Area"),
                            "consignes": t.get("strInstructions", ""),
                            "ingredientQuantite": ingredients,
                        }
                    )

                except KeyError as e:
                    logging.error(f"Erreur : clé manquante dans {t} - {e}")

        return recettes


if __name__ == "__main__":
    recettes = RecetteClient().get_recette()
