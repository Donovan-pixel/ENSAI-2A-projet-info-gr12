class Ingredient:
    """
    Classe représentant un ingrédient

    Attributs
    ----------
    idIngrédient : int
        identifiant
    nom : str
        nom de l'ingrédient
    """

    def __init__(self, idIngredient, nom):
        """Constructeur"""
        self.idIngredient = idIngredient
        self.nom = nom

    def __str__(self):
        """Permet d'afficher les informations d'un ingrédient"""
        return f"Ingredient({self.nom})"
