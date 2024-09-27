import os
import requests
import dotenv
from typing import List


class IngredientClient:
    """Fait un appel à l'endpoint Ingrédient"""

    def __init__(self) -> None:
        dotenv.load_dotenv()
        self.__host = os.environ["WEBSERVICE_HOST"]

    def get_ingredient(self) -> List[str]:
        """
        Retourne la liste des ingrédients
        """

        # Appel du Web service
        req = requests.get(f"{self.__host}/list.php?i=list")

        # Création d'une liste puis parcours du json pour ajouter tous les ingrédients à la liste
        ingredients = []
        if req.status_code == 200:
            raw_ingredients = req.json()["meals"]
            for t in raw_ingredients:
                print(t["strIngredient"])
                ingredients.append(t["strIngredient"])

        return sorted(ingredients)


if __name__ == "__main__":
    IngredientClient().get_ingredient()
