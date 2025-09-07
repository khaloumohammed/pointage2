# Fichier : views/t_service.py

import flet as ft
import openpyxl
from t_service_data import read_t_service_data

# La fonction de lecture des détails du pointage est déjà dans t_service_data.py.
# Inutile de la définir ici, ce qui évite la confusion.

def create_service_list_tile(page, service):
    """
    Crée un ListTile pour chaque service, intégré dans une carte surélevée et stylisée.
    """
    return ft.Card(
        elevation=8,
        content=ft.Container(
            content=ft.ListTile(
                title=ft.Text(
                    f"{service['jour']} -- {service['séance']}",
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE
                ),
                subtitle=ft.Text(
                    f"{service['classe']}",
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.W_700,
                ),
                leading=ft.Icon(ft.Icons.SCHOOL_SHARP, color=ft.Colors.WHITE, size=30),
                trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, color=ft.Colors.WHITE, size=20),
                on_click=lambda _: page.go(f"/pointage/{service['classe']}/{service['séance']}")
            ),
            padding=ft.padding.all(10),
            bgcolor="#c80815",
            border_radius=ft.border_radius.all(10),
        ),
        margin=ft.margin.symmetric(vertical=8, horizontal=15),
    )

def t_service_view(page, classe):
    """
    Construit la vue pour afficher la liste des services (séances) de la classe spécifiée.
    """
    # 1. Lire toutes les données des services
    all_services_data = read_t_service_data()
    
    # 2. Filtrer les données pour ne garder que la classe sélectionnée
    filtered_services = [
        service for service in all_services_data 
        if service.get('classe').strip() == classe.strip()
    ]
    
    # 3. Créer une carte pour chaque service filtré
    service_tiles = [
        create_service_list_tile(page, service) for service in filtered_services
    ]
    
    return ft.View(
        f"/t_service/{classe}",
        [
            ft.AppBar(
                title=ft.Text(f"Séances de la classe {classe}", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                bgcolor="#c80815",
                center_title=True,
                leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color="white",
                    on_click=lambda _: page.go("/")
                )
            ),
            ft.ListView(
                controls=service_tiles,
                spacing=0,
                padding=ft.padding.only(top=10, bottom=10),
                expand=True,
            ),
            ft.Container(
                content=ft.Text(
                    "Aucune séance trouvée pour cette classe. Veuillez vérifier le fichier Excel.",
                    color=ft.Colors.GREY_500,
                    text_align=ft.TextAlign.CENTER
                ),
                alignment=ft.alignment.center,
                visible=len(filtered_services) == 0,
                padding=ft.padding.all(20)
            )
        ],
        bgcolor="#F8F8FF"
    )
