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

    def __init__(self, nom, idIngredient=None):
        """Constructeur"""
        self.idIngredient = idIngredient
        self.nom = nom

    def __str__(self):
        """Permet d'afficher les informations d'un ingrédient"""
        return f"Ingredient({self.nom})"

    def __eq__(self, other):
        return self.idIngredient == other.idIngredient
