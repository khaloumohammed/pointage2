import flet as ft
from flet import *

def details_view(page, student, student_id):

    return ft.View(
                f"/student/{student}/{student_id}",
                [
                    ft.AppBar(
                        title=ft.Container(
                            content=ft.Row(
                                [
                                    ft.Container(ft.IconButton(
                                                    ft.Icons.ARROW_BACK_IOS,
                                                    on_click=lambda _:page.go("/")
                                                ),
                                        alignment=ft.alignment.center_left,
                                        padding=1,
                                        width=20,
                                               
                                    ),
                                    ft.Container(
                                        ft.Text(f"{student['nom']}", size=24, weight=ft.FontWeight.W_600),
                                        alignment=ft.alignment.center,
                                        padding=5,
                                        expand=True,
                                        
                                        ),
                                    
                                ],
                                spacing=10
                            ),
                            height=400,
                            padding=5,
                            alignment=ft.alignment.center_left,
                            expand=True,
                            
                            )),
                    ft.Column(
                            [
                                ft.Card(
                                    content=ft.Container(
                                        content=ft.Text(f"Classe: {student['classe']}",size=18, weight=ft.FontWeight.W_400),
                                        width=page.window.width,
                                        height=60,
                                        padding=5,
                                        alignment=ft.alignment.center,
                                        bgcolor="#ffa700",
                                        border_radius=8 
                                    )
                                ),
                                ft.Card(
                                    content=ft.Container(
                                        content=ft.Text(f"Genre: {student['genre']}",size=18, weight=ft.FontWeight.W_400),
                                        width=page.window.width,
                                        height=60,
                                        padding=5,
                                        alignment=ft.alignment.center,
                                        bgcolor="#ffa700",
                                        border_radius=8
                                    )
                                ),
                            
                                ft.ElevatedButton(
                                    text="Voir assiduité",
                                    on_click= lambda _: page.go(f"/assiduité/{student_id}")

                                )
        
                    ],
                    spacing=0.5,
                    )
                ])
