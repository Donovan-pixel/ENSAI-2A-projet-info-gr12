class ListeDeCourses:
    """
    Classe représentant une liste de courses

    Attributs
    ----------
    idListeDeCourses : int
        identifiant de la liste de courses
    idUtilisateur : int
        identifiant de l'utilisateur
    IngredientQuantites : dict
        quantité de chaque ingrédient
    """

    def __init__(self, idListeDeCourses, idUtilisateur, IngredientQuantites):
        """Constructeur"""
        self.idListeDeCourses = idListeDeCourses
        self.idUtilisateur = idUtilisateur
        self.IngredientQuantites = IngredientQuantites

    def __str__(self):
        """Permet d'afficher les informations d'une liste de courses"""
        return f"L'utilisateur({self.idUtilisateur} a dans sa liste de courses"
        f"{self.IngredientQuantites})"
