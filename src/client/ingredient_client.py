import os
import requests
import dotenv
import logging
from typing import List
from utils.log_decorator import log


class IngredientClient:
    """Fait un appel à l'endpoint Ingrédient"""

    def __init__(self) -> None:
        dotenv.load_dotenv()
        self.__host = os.getenv("WEBSERVICE_HOST")

    @log
    def get_ingredient(self) -> List[str]:
        """Retourne la liste des ingrédients"""

        ingredients = []
        try:
            response = requests.get(f"{self.__host}/list.php?i=list")
            response.raise_for_status()

            raw_ingredients = response.json().get("meals")
            if raw_ingredients:
                ingredients = [t["strIngredient"] for t in raw_ingredients]
            else:
                logging.info("Aucun ingrédient trouvé")

        except requests.RequestException as e:
            logging.error(f"Échec de la récupération des ingrédients: {e}")

        return sorted(ingredients)


if __name__ == "__main__":
    ingredients = IngredientClient().get_ingredient()
