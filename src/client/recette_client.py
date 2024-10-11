import os
import requests

from typing import List


class RecetteClient:
    """Faire appel à mealdb endpoint"""

    def __init__(self) -> None:
        self.__host = os.environ["WEBSERVICE_HOST"]
