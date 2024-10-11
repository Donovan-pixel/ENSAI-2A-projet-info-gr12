class Recette:
    """
    Classe représentant une recette

    Attributs
    ----------
    idRecette : int
        identifiant
    titre : str
        nom de la recette
    ingredientQuantite : dict
        dictionnaire des ingrédients et leur quantité associée
    consignes : str
        instructions
    categorie : str
        catégorie du régime alimentaire
    origine : str
        origine géographique de la recette

    """

    def __init__(self, idRecette, titre, ingredientQuantite, consignes, categorie, origine):
        """Constructeur"""
        self.idRecette = idRecette
        self.titre = titre
        self.ingredientQuantite = ingredientQuantite
        self.consignes = consignes
        self.categorie = categorie
        self.origine = origine

    def __str__(self):
        """Permet d'afficher les informations d'une recette"""
        return (
            f"Recette({self.titre}, {self.ingredientQuantite}, {self.consignes}, {self.categorie},"
            "{self.origine}"
        )
