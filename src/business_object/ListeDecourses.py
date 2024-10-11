class ListeDeCourse:
    def __init__(self, idListeDecourses, idUtilisateur):
        self.idListeDecourses = idListeDecourses
        self.idUtilisateur = idUtilisateur
        self.ingredientQuantite = {}  # Dictionnaire {Ingredient: quantite}

    def ajouter_ingredient(self, idIngredient, quantite):
        """Ajoute ou met à jour un ingrédient dans la liste de courses"""
        if idIngredient in self.ingredientQuantite:
            # Si l'ingrédient existe déjà, on augmente la quantité
            self.ingredientQuantite[idIngredient] += quantite
        else:
            # Sinon, on ajoute l'ingrédient avec sa quantité
            self.ingredientQuantite[idIngredient] = quantite
