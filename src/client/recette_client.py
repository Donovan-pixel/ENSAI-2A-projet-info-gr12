import os
import requests
import string
from utils.log_decorator import log
from typing import List, Dict
from dotenv import load_dotenv


class RecetteClient:
    """Fait appel à mealdb endpoint"""

    def __init__(self) -> None:
        load_dotenv()
        self.__host = os.environ["WEBSERVICE_HOST"]

    @log
    def get_recette(self) -> List[Dict]:
        """Retourne la liste des recettes"""

        recettes = []
        for letter in list(string.ascii_lowercase):
            req = requests.get(f"{self.__host}/search.php?f={letter}")

            if req.status_code == 200:
                raw_recettes = req.json()["meals"]

                if raw_recettes:
                    for t in raw_recettes:
                        try:
                            # Création d'un dictionnaire pour les ingrédients
                            ingredients = {}
                            for i in range(1, 21):
                                ingredient = t.get(f"strIngredient{i}")
                                measure = t.get(f"strMeasure{i}")

                                if ingredient:
                                    ingredients[ingredient] = (
                                        measure or ""
                                    )  # Utilise '' si la mesure est None

                            # Ajoute la recette au format souhaité
                            recettes.append(
                                {
                                    "titre": t["strMeal"],
                                    "categorie": t["strCategory"],
                                    "origine": t["strArea"],
                                    "consignes": t["strInstructions"],
                                    "ingredientQuantite": ingredients,
                                }
                            )
                        except KeyError as e:
                            print(f"Erreur : clé manquante dans {t} - {e}")

        return recettes


if __name__ == "__main__":
    recettes = RecetteClient().get_recette()
    for recette in recettes:
        print(recette)  # Affiche les recettes pour vérification
