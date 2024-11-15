class ListeDeCourses:
    """
    Classe définissant une liste de courses

    Attributs
    ----------
    idListeDeCourses : int
        identifiant de la liste de courses
    idUtilisateur : int
        identifiant de l'utilisateur
    """

    def __init__(self, idUtilisateur, idListeDecourses=None):
        """Constructeur"""
        self.idListeDecourses = idListeDecourses
        self.idUtilisateur = idUtilisateur
        self.ingredientQuantite = {}  # Dictionnaire {Ingredient: quantite}

    def ajouterIngredient(self, Ingredient, quantite) -> bool:
        """Ajoute ou met à jour un ingrédient dans la liste.

        Parameters
        ----------
        Ingredient : Ingrédient
            L'ingrédient à ajouter
        quantite : float
            La quantité à ajouter ou mettre à jour.

        Returns
        -------
        bool
            True si l'ajout/mise à jour est un succès, False sinon.
        """
        if quantite > 0:
            self.ingredientQuantite[Ingredient.nom] = quantite
            return True
        else:
            return False
