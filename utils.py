# Mettez cette fonction dans un fichier utilitaire, par exemple 'utils.py'
import flet as ft

def afficher_snack_bar(page, classe):
    # Crée un objet SnackBar avec le message désiré
    snack_bar = ft.SnackBar(
        content=ft.Text(f"Vous avez sélectionné la classe : {classe}"),
        action="Fermer",
        on_action=lambda e: print("SnackBar fermé."), # Action optionnelle
    )
    
    # Attache le SnackBar à la page
    page.snack_bar = snack_bar
    
    # Affiche le SnackBar
    #page.open(snack_bar)
    page.snack_bar.open=True
<<<<<<< HEAD
    page.update()
=======
    page.update()
>>>>>>> 105fb96 (Ajout des fichiers de base du projet pour la fusion)
