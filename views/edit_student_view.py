import flet as ft
import openpyxl
from t_service_data import read_students_data

def edit_student_view(page, student_id, classe):
    
    # 1. Trouver les données de l'étudiant à modifier
    # Cette logique dépend de la structure de votre `page.students_data'
    #students_data = next((s for s in page.students_data if s['id_eleve'] == student_id), None)
    students_data = next((s for s in page.students_data if s.get('id_eleve') == student_id), None)
    if not students_data:
        # Gérer le cas où l'étudiant n'est pas trouvé

        snack_b1=ft.SnackBar(ft.Text("Élève non trouvé."))
        page.snack_bar = snack_b1
        page.open(snack_b1)
        return ft.View("/error")

    # 2. Créer des champs de saisie pré-remplis
    id_field = ft.TextField(label="Id non modifiable", value=students_data['id_eleve'], read_only=True)
    classe_field = ft.TextField(label="Classe", value=students_data['classe'])
    nom_field = ft.TextField(label="Nom", value=students_data['nom'])
    genre_field = ft.TextField(label="Genre (G/F)", value=students_data['genre'])
    note_field = ft.TextField(label="Note", value=students_data['note'])
    #classe = students_data['classe']
    def save_changes(e):
        try:
            # 3. Mettre à jour les données dans le dictionnaire
            students_data['id_eleve'] = id_field.value
            students_data['classe'] = classe_field.value
            students_data['nom'] = nom_field.value
            students_data['genre'] = genre_field.value
            students_data['note'] = note_field.value
            
            # 4. Enregistrer les modifications dans le fichier Excel
            workbook = openpyxl.load_workbook("students.xlsx")
            sheet = workbook['student']
            
            # Trouver la ligne de l'étudiant par son ID
            row_to_update = None
            for row in sheet.iter_rows():
                if row[0].value == student_id: # Supposons que l'ID est dans la première colonne
                    row_to_update = row
                    break
            
            if row_to_update:
                # Mise à jour des cellules
                row_to_update[0].value = students_data['id_eleve']
                row_to_update[1].value = students_data['classe']
                row_to_update[2].value = students_data['nom']
                row_to_update[3].value = students_data['genre']
                row_to_update[4].value = students_data['note']
                
                workbook.save("students.xlsx")
                
                snack2_b=ft.SnackBar(ft.Text("Modifications enregistrées !"))
                page.snack_bar = snack2_b
                page.open(snack2_b)

                page.update()
                # Revenir à la vue précédente après l'ajout
            page.go(f"/home/{classe}")
                
        except Exception as ex:
            snack3_b=ft.SnackBar(ft.Text(f"Erreur d'enregistrement : {ex}"))
            page.snack_bar = snack3_b
            page.open(snack3_b)
            page.update()

    def cancel_edit_student(e):
        page.go(f"/home/{classe}")

    return ft.View(
        f"/student_edit/{student_id}/{classe}",
        [
            ft.AppBar(
                title=ft.Text(f"Modifier {students_data['nom']}", color="white"),
                leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color="white",
                    on_click=lambda _: page.go(f"/home/{classe}"), # Revenir à la liste des étudiants
                    
                ),
                bgcolor="#C80815"
            ),
            ft.Column(
                [
                    ft.Text("Modifier les informations de l'élève", size=20, weight="bold"),
                    id_field,
                    nom_field,
                    genre_field,
                    classe_field,
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.TextButton(
                                    content=ft.Text("Annuler", size=16),
                                    style=ft.ButtonStyle(color="black", bgcolor="white"),
                                    on_click=cancel_edit_student,
                                ),
                                ft.TextButton(
                                content=ft.Text("Sauvegarder", size=16),
                                style=ft.ButtonStyle(color="black", bgcolor="white"),
                            on_click=save_changes),

                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=50,
                        ),
                        alignment=ft.alignment.center,
                        padding=20,
                    ),
                    
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            ),
        ],
    )