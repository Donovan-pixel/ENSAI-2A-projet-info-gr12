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

    def ajouterIngredient(self, idIngredient, quantite) -> bool:
        """Ajoute ou met à jour un ingrédient dans la liste.

        Parameters
        ----------
        idIngredient : int
            L'identifiant de l'ingrédient.
        quantite : float
            La quantité à ajouter ou mettre à jour.

        Returns
        -------
        bool
            True si l'ajout/mise à jour est un succès, False sinon.
        """
        if quantite > 0:
            if str(idIngredient) in self.ingredientQuantite:
                # Si l'ingrédient existe déjà, on ajoute la quantité
                self.ingredientQuantite[str(idIngredient)] += quantite
                return True
            else:
                # Sinon, on ajoute un nouvel ingrédient avec sa quantité
                self.ingredientQuantite[str(idIngredient)] = quantite
                return True
        else:
            return False

    def __str__(self):
        """Affichage des informations d'une liste de courses"""
        return f"L'utilisateur({self.idUtilisateur} a les courses suivantes :"
        " {self.ingredientQuantite}"
