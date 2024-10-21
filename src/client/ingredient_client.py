import os
import requests
import dotenv
from typing import List
from utils.log_decorator import log


class IngredientClient:
    """Fait un appel à l'endpoint Ingrédient"""

    def __init__(self) -> None:
        dotenv.load_dotenv()
        self.__host = os.environ["WEBSERVICE_HOST"]

    @log
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
                # boucle sur les 20 colonnes ingredients
                for i in range(1, 21):
                    ingredient_key = f"strIngredient{i}"  # Génère les clés strIngredient1,...20
                    ingredient = t.get(ingredient_key)  # Récupère l'ingrédient correspondant

                    if ingredient:
                        ingredients.append(ingredient)

        return sorted(ingredients)


if __name__ == "__main__":
    IngredientClient().get_ingredient()
