# Fichier: menu_view.py

import flet as ft
from utils import afficher_snack_bar
from t_service_data import read_students_data


def menu_view(page):
    page.verticalalignment = ft.MainAxisAlignment.CENTER
    page.horizontalalignment = ft.CrossAxisAlignment.CENTER

    classes = sorted(list(set(student.get('classe') for student in page.students_data)))
    classes = [c for c in classes if c]

    # Fonctions pour gérer les actions des boutons
    def on_classe_click(e, classe):
        afficher_snack_bar(page, f"Redirection vers la liste des élèves de la classe {classe}")
        page.go(f"/home/{classe}")

    def on_pointage_click(e, classe):
        # Correction ici : on inclut la classe dans l'URL
        afficher_snack_bar(page, f"Redirection vers le pointage de la classe {classe}")
        page.go(f"/t_service/{classe}")
        
    classes_list = [
        ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        # 1. Le texte en haut de la colonne
                        ft.Text(
                            f"Classe: {classe}",
                            size=18,
                            color=ft.Colors.WHITE,
                            weight=ft.FontWeight.W_600
                        ),
                        
                        # 2. La ligne de boutons en bas de la colonne
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    "Liste des élèves",
                                    expand=True,
                                    style=ft.ButtonStyle(
                                        color=ft.Colors.WHITE,
                                        bgcolor="#C80815",
                                        shape=ft.RoundedRectangleBorder(radius=8)
                                    ),
                                    on_click=lambda _, cls=classe: on_classe_click(_, cls)
                                ),
                                ft.ElevatedButton(
                                    "Pointage",
                                    expand=True,
                                    style=ft.ButtonStyle(
                                        color=ft.Colors.WHITE,
                                        bgcolor="#C80815",
                                        shape=ft.RoundedRectangleBorder(radius=8)
                                    ),
                                    on_click=lambda _, cls=classe: on_pointage_click(_, cls)
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=40,
                        ),
                    ],
                    spacing=10,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                width=400,
                padding=10,
                border_radius=10,
                bgcolor="#C80815",
                alignment=ft.alignment.center,
            ),
        ) for classe in classes
    ]


    return ft.View(
        "/",
        [
            ft.AppBar(
                title=ft.Text("Menu"),
                color=ft.Colors.WHITE,
                center_title=True,
                bgcolor="#C80815",
                # Ajoutez un bouton à droite pour quitter
            ),
            ft.ListView(controls=classes_list, expand=True),
        ]
    )