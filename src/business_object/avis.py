class Avis:
    """
    Classe représentant un avis

    Attributs
    ----------
    idAvis : int
        identifiant de l'avis
    idUtilisateur : int
        identifiant de l'utilisateur
    idRecette : int
        identifiant de la recette
    note : float
        note donnée par cet utilisateur pour la recette
    commentaire : str
        commentaire donnée par l'utilisateur pour la recette
    """

    def __init__(self, idAvis, idUtilisateur, idRecette, note, commentaire):
        """Constructeur"""
        self.idAvis = idAvis
        self.idUtilisateur = idUtilisateur
        self.idRecette = idRecette
        self.note = note
        self.commentaire = commentaire

    def __str__(self):
        """Permet d'afficher les informations d'un avis"""
        return (
            f"Avis donné par({self.idUtilisateur}, pour la recette {self.idRecette}"
            "avec la note {self.note} et le commentaire {self.commentaire}"
        )


