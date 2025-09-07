import flet as ft
from t_service_data import read_students_data
import openpyxl

def home_view(page, classe):
    
    students_data = read_students_data()
    
    filtered_students = [
        s for s in students_data
        if str(s.get('classe', '')).strip() == str(classe).strip()
    ]

    def delete_student_from_excel(student_id):
        try:
            workbook = openpyxl.load_workbook("students.xlsx")
            sheet = workbook['student']
            
            row_to_delete_index = -1
            for row_index, row in enumerate(sheet.iter_rows()):
                if str(row[0].value).strip() == str(student_id).strip():
                    row_to_delete_index = row_index + 1
                    break
            
            if row_to_delete_index != -1:
                sheet.delete_rows(row_to_delete_index)
                workbook.save("students.xlsx")
                return True
            else:
                return False
        except Exception as ex:
            print(f"Erreur lors de la suppression depuis Excel: {ex}")
            return False

    def confirm_delete_dialog(page, student_id, student_name):
            # Définition de close_dialog à l'intérieur de la fonction
            def close_dialog(e):
                page.close(page.dialog)
                #page.dialog.open = False
                page.update()

            def on_confirm(e):
                if delete_student_from_excel(student_id):
                    page.students_data = [s for s in page.students_data if s.get('id_eleve') != student_id]
                    
                    # Mise à jour de l'interface utilisateur pour rafraîchir la liste
                    page.views[-1].controls[1].controls = [
                        create_student_card(page, student)
                        for student in page.students_data
                        if str(student.get('classe', '')).strip() == str(classe).strip()
                    ]
                    page.update()
                    
                    snack_home = ft.SnackBar(ft.Text("Élève supprimé avec succès !"))
                    page.open(snack_home)
                else:
                    snack_home = ft.SnackBar(ft.Text("Erreur lors de la suppression de l'élève."))
                    page.open(snack_home)
                
                close_dialog(e)

            page.dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Confirmer la suppression"),
                content=ft.Text(f"Êtes-vous sûr de vouloir supprimer l'élève {student_name} ? Cette action est irréversible."),
                actions=[
                    ft.TextButton("Annuler", on_click=close_dialog),
                    ft.TextButton("Confirmer", on_click=on_confirm),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            #page.dialog.open = True
            page.open(page.dialog)
            page.update()

    def create_student_card(page, student):
        id_eleve = student.get('id_eleve', 'N/A')
        student_name = student.get('nom', 'Nom non trouvé')
        genre_eleve = student.get('genre', 'g')
        avatar_url = "assets/avatars/avatar_G.png" if str(genre_eleve).strip() == "G" else "assets/avatars/avatar_F.png"
        
        return ft.Card(
            content=ft.Container(
                bgcolor="#C80815",
                padding=10,
                border_radius=ft.border_radius.all(10),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Row(
                            controls=[
                                ft.CircleAvatar(
                                    content=ft.Image(src=avatar_url),
                                    radius=25,
                                ),
                                ft.Column(
                                    spacing=2,
                                    controls=[
                                        ft.Text(
                                            f"N° {str(id_eleve).split('_')[-1]} : {student_name}",
                                            size=16,
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.Colors.WHITE
                                        ),
                                        ft.Text(
                                            f"Genre: {genre_eleve}",
                                            size=12,
                                            color=ft.Colors.WHITE
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        ft.Row(
                            controls=[
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    icon_color=ft.Colors.WHITE,
                                    on_click=lambda _: page.go(f"/student_edit/{id_eleve}/{classe}"),
                                    tooltip="Modifier l'élève",
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_FOREVER_SHARP,
                                    icon_color=ft.Colors.WHITE,
                                    on_click=lambda _: confirm_delete_dialog(page, id_eleve, student_name),
                                    tooltip="Supprimer l'élève"
                                ),
                            ],
                        ),
                    ],
                ),
            )
        )

    student_cards = [create_student_card(page, student) for student in filtered_students]

    return ft.View(
        f"/home/{classe}",
        [
            ft.AppBar(
                title=ft.Text(f"Liste des élèves de la classe {classe}", color="white"),
                bgcolor="#C80815",
                center_title=True,
                leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color="white",
                    on_click=lambda _: page.go("/")
                )
            ),
            ft.ListView(
                controls=student_cards,
                expand=True,
                spacing=5,
                padding=ft.padding.symmetric(vertical=15, horizontal=10),
            ),
            ft.FloatingActionButton(
                content=ft.Icon(
                    name=ft.Icons.ADD,
                    color=ft.Colors.WHITE
                ),
                on_click=lambda _: page.go(f"/add_student/{classe}"),
                tooltip="Ajouter un nouvel élève",
                bgcolor="#C80815",
            )
        ]
    )
