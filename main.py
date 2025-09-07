# Fichier : main.py

import flet as ft
from flet import *
import openpyxl
import pandas as pd
import asyncio
import time
from views.menu import menu_view
from views.home import home_view
from views.details import details_view
from views.assiduite import assiduite_view
from views.edit_student_view import edit_student_view
from views.add_student_view import add_student_view
from views.t_service import t_service_view

from views.pointage import pointage_view
from views.pointage_details import pointage_details_view
from views.splash import splash_view
from t_service_data import read_students_data, read_pointage_data

# extraction des données de l'élève par son id:
# La fonction prend maintenant "page" comme argument
def get_student_by_id(page, student_id):
    # La recherche se fait sans normalisation pour éviter les erreurs
    for student in page.students_data:
        if student.get('id_eleve') == student_id:
            return student
    return None

# fonction main
def main(page: ft.Page):
    page.title='Navigation avec passage de paramètres...'
    page.window.width = 480
    page.window.height = 800
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = "auto",
    page.padding=5
    
    appbar_theme = ft.AppBarTheme(
        toolbar_height = 400,
        bgcolor="#002e63"
    )
    page.theme = ft.Theme(appbar_theme=appbar_theme)

    # Charge les données de pointage au démarrage
    page.absences = read_pointage_data()

    # CHARGEMENT DES DONNÉES UNE SEULE FOIS, DIRECTEMENT SUR L'OBJET PAGE
    page.students_data = read_students_data()
    
    # On affiche d'abord le splash screen
    page.views.append(splash_view(page))
    page.update()

    # Attendez 3 secondes sans bloquer l'interface
    time.sleep(3) 

    # Remplacez le splash screen par la vue principale
    page.views.clear()
    page.views.append(menu_view(page))
    #page.views.append(t_service_view(page))
    page.update()

    # On définit le routeur après le splash screen
    def route_change(e):
        page.views.clear()
        
        # Le reste de votre logique de routage
        if page.route == "/":
            page.views.append(menu_view(page))
        elif page.route.startswith("/home/"):
            parts = page.route.split("/")
            classe = parts[2]
            page.views.append(home_view(page, classe))
        elif page.route.startswith("/t_service/"):           
            classe = page.route.split("/")[-1]
            page.views.append(t_service_view(page, classe))
        elif page.route.startswith("/add_student/"):
            parts = page.route.split("/")
            classe = parts[2]
            page.views.append(add_student_view(page, classe))
        elif page.route.startswith("/student_edit/"):
            parts = page.route.split("/")
            student_id = parts[2]
            classe = parts[3]
            page.views.append(edit_student_view(page, student_id, classe))
        elif page.route.startswith("/pointage/"):
            parts = page.route.split("/")
            classe = parts[2]
            seance = parts[3]
            page.views.append(pointage_view(page, classe, seance))
        elif page.route.startswith("/pointage_details/"):
            parts = page.route.split("/")
            student_id = parts[2]
            seance = parts[3]
            page.views.append(pointage_details_view(page, student_id, seance))
        elif page.route.startswith("/student/"):
            parts = page.route.split("/")
            student = parts[2]
            student_id = parts[3]
            page.views.append(details_view(page, student, student_id))
        page.update()

    page.on_route_change = route_change

ft.app(target=main, assets_dir="assets")
