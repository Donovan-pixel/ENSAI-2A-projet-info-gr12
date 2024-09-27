class Ingredient:
    """
    Classe représentant un ingrédient

    Attributs
    ----------
    idIngrédient : int
        identifiant
    nom : str
        nom de l'ingrédient
    quantite : float
        quantité variable de l'ingrédient
    """

    def __init__(self, idIngredient, nom, quantite):
        """Constructeur"""
        self.idIngredient = idIngredient
        self.nom = nom
        self.quantite = quantite

    def __str__(self):
        """Permet d'afficher les informations d'un ingrédient"""
        return f"Ingredient({self.nom})"
