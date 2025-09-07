# Fichier: views/splash.py

import flet as ft

def splash_view(page: ft.Page):
    return ft.View(
        "/splash",
        [
            ft.Container(
                content=ft.Column(
                    controls=[
                        # Une ligne vide pour espacer
                        ft.Container(height=20),
                        # L'image du splash screen
                        ft.Image(
                            src=f"assets/ensignant_prend_notes2.png",
                            width=400,
                            height=600,
                            fit=ft.ImageFit.CONTAIN
                        ),
                        # L'indicateur de chargement
                        ft.ProgressRing(
                            width=40,
                            height=40,
                            stroke_width=3,
                            color=ft.Colors.WHITE
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                alignment=ft.alignment.center,
                expand=True,
                bgcolor=ft.Colors.RED_700 # Le conteneur entier est rouge
            )
        ],
        bgcolor=ft.Colors.RED_700 # La vue a un fond rouge pour éviter les bords blancs
    )