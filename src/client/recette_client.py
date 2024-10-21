import os
import requests

from utils.log_decorator import log
from typing import List


class RecetteClient:
    """Faire appel à mealdb endpoint"""

    def __init__(self) -> None:
        self.__host = os.environ["WEBSERVICE_HOST"]

    @log
    def get_recette(self) -> List[str]:
        """Retourne la liste des recettes"""

        # appel du webservice
        req = requests.get(f"{self.__host}/list.php?i=list")

        # Création d'une liste puis parcours du json pour ajouter toutes les recettes à la liste
        recettes = []
        if req.status_code == 200:
            raw_recettes = req.json()["meals"]
            for t in raw_recettes:
                print(t["strMeal"], t["strCategory"], t["strArea"], t["strInstructions"])
                recettes.append(t["strMeal"])

        return sorted(recettes)


if __name__ == "__main__":
    RecetteClient().get_recette()
