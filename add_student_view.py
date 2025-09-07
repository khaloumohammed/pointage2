# Fichier: add_student_view.py

import flet as ft
import openpyxl
import uuid
from t_service_data import read_students_data, check_student_id_exists

def add_student_view(page, classe):
    
    def on_id_field_focus(e):
        if not id_field.value:
            id_field.value = f"{classe}_"
            page.update()
    
    id_field = ft.TextField(
        label="ID = Classe + _ + n° de l'élève",
        on_focus=on_id_field_focus
    )
    
    classe_field = ft.TextField(label="Classe", value=classe)
    nom_field = ft.TextField(label="Nom")
    genre_field = ft.TextField(label="Genre (G ou F)")
    note_field = ft.TextField(label="Note")
    
    def save_new_student(e):
        new_student_id = id_field.value
        
        if not new_student_id or not nom_field.value or not classe_field.value:
            page.snack_bar = ft.SnackBar(ft.Text("Veuillez remplir tous les champs obligatoires."), bgcolor=ft.Colors.RED_700)
            page.open(page.snack_bar)
            page.update()
            return

        if check_student_id_exists(new_student_id):
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Erreur : L'ID '{new_student_id}' existe déjà. Veuillez en saisir un autre."), 
                bgcolor=ft.Colors.RED_700
            )
            page.open(page.snack_bar)
            page.update()
            return
        
        try:
            new_student_data = {
                'id_eleve': new_student_id,
                'nom': nom_field.value,
                'genre': genre_field.value,
                'classe': classe_field.value,
                'note': note_field.value,
            }
            
            workbook = openpyxl.load_workbook("students.xlsx")
            sheet = workbook['student']
            sheet.append([
                new_student_data['id_eleve'],
                new_student_data['classe'],
                new_student_data['nom'],
                new_student_data['genre'],
                new_student_data['note'],
            ])
            workbook.save("students.xlsx")
            
            page.students_data = read_students_data()
            page.snack_bar = ft.SnackBar(ft.Text("Nouvel élève ajouté !"))
            page.open(page.snack_bar)
            page.update()
            
            page.go(f"/home/{new_student_data['classe']}")
    
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erreur d'enregistrement : {ex}"), bgcolor=ft.Colors.RED_700)
            page.open(page.snack_bar)
            page.update()

    def cancel_add_student(e):
        page.go(f"/home/{classe}")

    return ft.View(
        f"/add_student/{classe}",
        [
            ft.AppBar(
                title=ft.Text("Ajouter un élève", color="white"),
                leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color="white",
                    on_click=cancel_add_student,
                ),
                bgcolor="#C80815"
            ),
            ft.Column(
                [
                    ft.Text("Remplissez les champs pour ajouter un élève", size=18),
                    id_field,
                    nom_field,
                    genre_field,
                    classe_field,
                    note_field,
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.TextButton(
                                    content=ft.Text("Annuler", size=16),
                                    style=ft.ButtonStyle(color="black", bgcolor="white"),
                                    on_click=cancel_add_student,
                                ),
                                ft.TextButton(
                                    content=ft.Text("Sauvegarder", size=16),
                                    style=ft.ButtonStyle(color="black", bgcolor="white"),
                                    on_click=save_new_student,
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=60,
                            
                        ),
                        alignment=ft.alignment.center,
                        padding=20,
                    )

                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            ),
        ],
    )
