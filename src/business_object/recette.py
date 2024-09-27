class Recette:
    """
    Classe représentant une recette

    Attributs
    ----------
    idRecette : int
        identifiant
    titre : str
        nom de la recette
    ingredients : List[Ingredient]
        liste des ingrédients
    consignes : str
        instructions
    categorie : str
        catégorie du régime alimentaire
    origine : str
        origine géographique de la recette
    noteMoyenne : float
        note moyenne donnée par les utilisateurs pour cette recette
    """

    def __init__(self, idRecette, titre, ingredients, consignes, categorie, origine, noteMoyenne):
        """Constructeur"""
        self.idRecette = idRecette
        self.titre = titre
        self.ingredients = ingredients
        self.consignes = consignes
        self.categorie = categorie
        self.origine = origine
        self.noteMoyenne = noteMoyenne

    def __str__(self):
        """Permet d'afficher les informations d'une recette"""
        return f"Recette({self.titre}, {self.ingredients}, {self.consignes}, {self.categorie},"
        f"{self.origine}, {self.noteMoyenne})"
