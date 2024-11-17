import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.recette import Recette
from business_object.ingredient import Ingredient
from dao.ingredient_dao import IngredientDao
from service.ingredient_service import IngredientService


class RecetteDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux recettes de la base de données"""

    @log
    def ajouterRecette(self, recette: Recette) -> bool:
        """Ajout d'une recette dans la base de données"""

        res = None
        created = False

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO recettes(title, category, area, instructions)
                        VALUES (%(title)s, %(category)s, %(area)s, %(instructions)s)
                        RETURNING id_meal;
                        """,
                        {
                            "title": recette.titre,
                            "category": recette.categorie,
                            "area": recette.origine,
                            "instructions": recette.consignes,
                        },
                    )
                    res = cursor.fetchone()

        except Exception as e:
            logging.exception(e)
            raise

        if res:
            recette.idRecette = res["id_meal"]
            created = True

        if created:
            for ingredient, quantite in recette.ingredientQuantite.items():
                id_ingredient = IngredientDao().obtenirIdParNom(ingredient)
                if id_ingredient is None:
                    IngredientService().ajouterNouvelIngredient(ingredient)
                    id_ingredient = IngredientDao().obtenirIdParNom(ingredient)

                try:
                    with DBConnection().connection as connection:
                        with connection.cursor() as cursor:
                            # Vérifier si la relation existe déjà
                            cursor.execute(
                                "SELECT 1 FROM meals_ingredients "
                                "WHERE id_meal = %(id_meal)s"
                                " AND id_ingredient = %(id_ingredient)s; ",
                                {"id_meal": recette.idRecette, "id_ingredient": id_ingredient},
                            )
                            # Si la relation n'existe pas, insérer la ligne
                            if cursor.fetchone() is None:
                                cursor.execute(
                                    "INSERT INTO "
                                    "meals_ingredients(id_meal, id_ingredient, quantite)  "
                                    "VALUES (%(id_meal)s, %(id_ingredient)s, %(quantite)s); ",
                                    {
                                        "id_meal": recette.idRecette,
                                        "id_ingredient": id_ingredient,
                                        "quantite": quantite,
                                    },
                                )
                                logging.info(
                                    f"Ingrédient {ingredient} ajouté à la recette {recette.titre}."
                                )
                            else:
                                logging.info(
                                    f"La relation pour l'ingrédient {ingredient} existe déjà."
                                )
                except Exception as e:
                    logging.exception(e)
                    raise

        return created

    @log
    def obtenirToutesLesRecettes(self) -> list[Recette]:
        """Obtention de toutes les recettes de la base de données

        Returns:
        -------
        list[Recette]:
            Liste des recettes
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT r.id_meal, r.title, r.category, r.area, r.instructions,
                        mi.id_ingredient, i.nom, mi.quantite FROM recettes r
                        LEFT JOIN meals_ingredients mi ON r.id_meal = mi.id_meal
                        LEFT JOIN ingredients i ON mi.id_ingredient = i.id_ingredient;
                        """
                    )
                    res = cursor.fetchall()

        except Exception as e:
            logging.exception(e)
            raise

        recettes = []
        recettes_dict = {}

        if res:
            for row in res:
                id_meal = row["id_meal"]

                if id_meal not in recettes_dict:
                    recettes_dict[id_meal] = {
                        "idRecette": id_meal,
                        "titre": row["title"],
                        "categorie": row["category"],
                        "origine": row["area"],
                        "consignes": row["instructions"],
                        "ingredientQuantite": {},
                    }

                ingredient_name = row["nom"]
                quantite = row["quantite"]
                recettes_dict[id_meal]["ingredientQuantite"][ingredient_name] = quantite

            for recette_data in recettes_dict.values():
                recette = Recette(
                    idRecette=recette_data["idRecette"],
                    titre=recette_data["titre"],
                    categorie=recette_data["categorie"],
                    origine=recette_data["origine"],
                    consignes=recette_data["consignes"],
                    ingredientQuantite=recette_data["ingredientQuantite"],
                )
                recettes.append(recette)

        return recettes

    @log
    def obtenirRecettesparLettre(self, lettre: str) -> list[Recette]:
        """Search for recipes starting with a given letter.

        Parameters
        ----------
        lettre : str
            The first letter of the recipes to search for

        Returns
        -------
        list[Recette]
            List of recipes starting with the given letter
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT r.id_meal, r.title, r.category, r.area, r.instructions,
                        mi.id_ingredient, i.nom, mi.quantite
                        FROM recettes r
                        LEFT JOIN meals_ingredients mi ON r.id_meal = mi.id_meal
                        LEFT JOIN ingredients i ON mi.id_ingredient = i.id_ingredient
                        WHERE r.title ILIKE %(pattern)s
                        """,
                        {"pattern": f"{lettre}%"},
                    )
                    res = cursor.fetchall()

        except Exception as e:
            logging.exception(e)
            raise

        recettes = []
        recettes_dict = {}

        if res:
            for row in res:
                id_meal = row["id_meal"]
                if id_meal not in recettes_dict:
                    recettes_dict[id_meal] = {
                        "idRecette": id_meal,
                        "titre": row["title"],
                        "categorie": row["category"],
                        "origine": row["area"],
                        "consignes": row["instructions"],
                        "ingredientQuantite": {},
                    }

                ingredient = row["nom"]
                quantite = row["quantite"]
                if ingredient:
                    recettes_dict[id_meal]["ingredientQuantite"][ingredient] = quantite

        for recette_data in recettes_dict.values():
            recette = Recette(
                idRecette=recette_data["idRecette"],
                titre=recette_data["titre"],
                categorie=recette_data["categorie"],
                origine=recette_data["origine"],
                consignes=recette_data["consignes"],
                ingredientQuantite=recette_data["ingredientQuantite"],
            )
            recettes.append(recette)

        return recettes

    @log
    def obtenirRecettesParIngredients(self, ingredients: list[Ingredient]) -> list[Recette]:
        """Retrieve recipes containing specific ingredients.

        Parameters
        ----------
        ingredients : list[Ingredient]
            List of ingredients included in the desired recipes

        Returns
        -------
        list[Recette]
            List of recipes containing the specified ingredients
        """
        ingredients_id = tuple([ing.idIngredient for ing in ingredients])

        if not ingredients_id:
            logging.info("Aucun ingrédient fourni.")
            return []

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    nb_ingredients = len(ingredients_id)
                    cursor.execute(
                        """
                        SELECT r.id_meal, r.title, r.category, r.area, r.instructions,
                        mi.id_ingredient, i.nom, mi.quantite
                        FROM recettes r
                        JOIN meals_ingredients mi ON r.id_meal = mi.id_meal
                        JOIN ingredients i ON mi.id_ingredient = i.id_ingredient
                        WHERE mi.id_ingredient IN %(ingredients_id)s
                        GROUP BY r.id_meal, r.title, r.category, r.area, r.instructions,
                        mi.id_ingredient, i.nom, mi.quantite
                        HAVING COUNT(DISTINCT mi.id_ingredient) = %(nb_ingredients)s;
                        """,
                        {"ingredients_id": ingredients_id, "nb_ingredients": nb_ingredients},
                    )
                    res = cursor.fetchall()

        except Exception as e:
            logging.exception(e)
            raise

        recettes = []
        recettes_dict = {}

        if res:
            for row in res:
                id_meal = row["id_meal"]
                if id_meal not in recettes_dict:
                    recettes_dict[id_meal] = {
                        "idRecette": id_meal,
                        "titre": row["title"],
                        "categorie": row["category"],
                        "origine": row["area"],
                        "consignes": row["instructions"],
                        "ingredientQuantite": {},
                    }

                ingredient = row["nom"]
                quantite = row["quantite"]
                if ingredient:
                    recettes_dict[id_meal]["ingredientQuantite"][ingredient] = quantite

        for recette_data in recettes_dict.values():
            recette = Recette(
                idRecette=recette_data["idRecette"],
                titre=recette_data["titre"],
                categorie=recette_data["categorie"],
                origine=recette_data["origine"],
                consignes=recette_data["consignes"],
                ingredientQuantite=recette_data["ingredientQuantite"],
            )
            recettes.append(recette)

        return recettes

    @log
    def obtenirRecettesParCategorie(self, categorie: str) -> list[Recette]:
        """Obtains recipes by category from the database.

        Parameters
        ----------
        categorie : str
            Category of the recipes to retrieve

        Returns
        -------
        list[Recette]
            List of recipes in the specified category
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT r.id_meal, r.title, r.category, r.area, r.instructions,
                        mi.id_ingredient, i.nom, mi.quantite
                        FROM recettes r
                        LEFT JOIN meals_ingredients mi ON r.id_meal = mi.id_meal
                        LEFT JOIN ingredients i ON mi.id_ingredient = i.id_ingredient
                        WHERE r.category = %(categorie)s;
                        """,
                        {"categorie": categorie},
                    )
                    res = cursor.fetchall()

        except Exception as e:
            logging.exception(e)
            raise

        recettes = []
        recettes_dict = {}

        if res:
            for row in res:
                id_meal = row["id_meal"]
                if id_meal not in recettes_dict:
                    recettes_dict[id_meal] = {
                        "idRecette": id_meal,
                        "titre": row["title"],
                        "categorie": row["category"],
                        "origine": row["area"],
                        "consignes": row["instructions"],
                        "ingredientQuantite": {},
                    }

                ingredient = row["nom"]
                quantite = row["quantite"]
                if ingredient:
                    recettes_dict[id_meal]["ingredientQuantite"][ingredient] = quantite

        for recette_data in recettes_dict.values():
            recette = Recette(
                idRecette=recette_data["idRecette"],
                titre=recette_data["titre"],
                categorie=recette_data["categorie"],
                origine=recette_data["origine"],
                consignes=recette_data["consignes"],
                ingredientQuantite=recette_data["ingredientQuantite"],
            )
            recettes.append(recette)

        return recettes

    @log
    def obtenirToutesLesCategories(self) -> list[str]:
        """Obtention de toutes les catégories de recettes de la base de données

        Returns:
        -------
        list[str]:
            Liste des catégories
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT DISTINCT category FROM recettes;
                        """
                    )
                    res = cursor.fetchall()

        except Exception as e:
            logging.exception(e)
            raise

        categories = [row["category"] for row in res if row["category"] is not None]

        return categories
