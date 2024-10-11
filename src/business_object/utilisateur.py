class Utilisateur:
    """
    Classe représentant un utilisateur

    Attributs
    ----------
    idUtilisateur : int
        identifiant
    pseudo : str
        pseudo de l'utilisateur
    motDePasse : str
        mot de passe de l'utilisateur
    role : str
        rôle de l'utilisateur
    """

    def __init__(self, idUtilisateur, pseudo, motDePasse, role, recettes_favorites = [], ingredients_favoris = []):
        """Constructeur"""
        self.idUtilisateur = idUtilisateur
        self.pseudo = pseudo
        self.motDePasse = motDePasse
        self.role = role
        self.recettes_favorites = recettes_favorites
        self.ingredients_favoris = ingredients_favoris

    def __str__(self):
        """Permet d'afficher les informations de l'utilisateur"""
        return f"Utilisateur({self.pseudo}, {self.role})"
