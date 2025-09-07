import flet as ft

def assiduite_view(page, student, student_id):
    return ft.View(
                f"/student/{student_id}",
                [
                    ft.AppBar(title=ft.Text(f"page compte rendu de l'assiduité de: {student['nom']}")),
                    ft.Text(f"Classe: {student['classe']}"),
                    ft.Text(f"Genre: {student['genre']}"),
                    ft.Text(f"Note: {student['note']}"),
                    ft.ElevatedButton(
                        text="Accueil ",
                        on_click= lambda _: page.go("/")
                    )

                ]
            )