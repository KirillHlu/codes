import flet as ft
from flet_map import Map, MapLatitudeLongitude, MarkerLayer, Marker, TileLayer, MapInteractionConfiguration, \
    MapInteractiveFlag, RichAttribution, TextSourceAttribution
import requests
from numpy.ma.core import repeat


def main(page: ft.Page):
    page.title = "Secure maps"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    page.bgcolor = "#303030"
    page.scroll = True

    marker_layer_ref = ft.Ref[MarkerLayer]()
    map_instance = None

    def create_map():
        nonlocal map_instance
        map_instance = Map(
            width=800,
            height=500,
            initial_center=MapLatitudeLongitude(30, 0),
            initial_zoom=2,
            interaction_configuration=MapInteractionConfiguration(
                flags=MapInteractiveFlag.ALL
            ),
            layers=[
                TileLayer(
                    url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                ),
                MarkerLayer(
                    ref=marker_layer_ref,
                    markers=[]
                ),
                RichAttribution(
                    attributions=[
                        TextSourceAttribution(
                            text="OpenStreetMap",
                            on_click=lambda e: page.launch_url("https://openstreetmap.org")
                        )
                    ],
                    alignment=ft.alignment.bottom_right
                )
            ]
        )

        link = "https://kkhludov.pythonanywhere.com/api/main"
        response = requests.get(link)
        marks = response.json()
        for el in marks:
            add_marker(el["latitude"], el["longitude"], el["name_of_mark"], "", "BLUE")
        return map_instance

    def show_add_marker_dialog(lat, lng):
        title = ft.TextField(label="Название метки")
        description = ft.TextField(label="Описание", multiline=True)
        color = ft.Dropdown(
            label="Цвет метки",
            options=[
                ft.dropdown.Option("RED"),
                ft.dropdown.Option("BLUE"),
                ft.dropdown.Option("GREEN"),
                ft.dropdown.Option("YELLOW"),
            ],
            value="RED"
        )

        def close_dlg(e):
            add_marker(
                lat=lat,
                lng=lng,
                title=title.value,
                description=description.value,
                color=color.value
            )
            dlg_modal.open = False
            page.update()

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Добавить новую метку"),
            content=ft.Column([title, description, color], tight=True),
            actions=[
                ft.TextButton("Отмена", on_click=lambda e: setattr(dlg_modal, "open", False)),
                ft.TextButton("Добавить", on_click=close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

    def add_marker(lat, lng, title="", description="", color="RED"):
        if marker_layer_ref.current:
            marker_color = getattr(ft.colors, color)

            # Создаем контейнер для маркера
            marker_container = ft.Container(
                content=ft.Icon(ft.icons.PLACE, color=marker_color),
                tooltip=f"{title}\n\n{description}" if description else title
            )

            marker_layer_ref.current.markers.append(
                Marker(
                    content=marker_container,
                    coordinates=MapLatitudeLongitude(lat, lng)
                )
            )
            page.update()

    def handle_map_click(e):
        show_add_marker_dialog(e.coordinates.latitude, e.coordinates.longitude)

    def go_to_map(e):
        map_page = ft.Column(
            controls=[
                ft.Text("World Map", size=30, weight="bold", color=ft.colors.WHITE),
                ft.Container(
                    content=create_map(),
                    border_radius=10,
                    shadow=ft.BoxShadow(blur_radius=10, color=ft.colors.BLUE_100)
                ),
                ft.ElevatedButton(
                    "Back to Home",
                    on_click=go_back,
                    style=ft.ButtonStyle(
                        bgcolor="#4CCD77",
                        color=ft.colors.WHITE,
                        padding=20,
                        shape=ft.RoundedRectangleBorder(radius=10)
                    )),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        if map_instance:
            map_instance.on_tap = handle_map_click

        page.clean()
        page.add(map_page)

    def go_back(e):
        page.clean()
        page.add(main_page)

    def go_to_news(e):
        page.clean()
        news_page = ft.Column(
            controls=[
                ft.ElevatedButton(
                    "Back to Home",
                    on_click=go_back,
                    style=ft.ButtonStyle(
                        bgcolor="#4CCD77",
                        color=ft.colors.WHITE,
                        padding=20,
                        shape=ft.RoundedRectangleBorder(radius=10)
                    ))
            ]
        )
        page.add(news_page)

        response = requests.get("https://kkhludov.pythonanywhere.com/api/news")
        news = response.json()
        for article in news:
            article_image = article['images'].split()[0]
            article_date = article["date"]
            article_short_description = article["short_description"]
            article_box = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Image(
                            src=article_image,
                            width=700,
                            height=200,
                            fit=ft.ImageFit.FILL,  # Изменено на FILL для заполнения всего пространства
                            border_radius=ft.border_radius.only(top_left=10, top_right=10)
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        article_short_description,
                                        size=16,
                                        weight="bold",
                                        color=ft.colors.WHITE
                                    ),
                                    ft.Text(
                                        article_date,
                                        size=12,
                                        color=ft.colors.WHITE60
                                    ),
                                ],
                                spacing=5
                            ),
                            padding=10
                        )
                    ],
                    spacing=0,  # Уменьшено расстояние между элементами
                    alignment=ft.MainAxisAlignment.START,
                ),
                bgcolor="#363636",
                border_radius=10,
                width=700,
                margin=ft.margin.only(bottom=10))
            page.add(article_box)


    main_page = ft.Column(
        controls=[
            ft.Text("Welcome to Secure maps",
                    size=30,
                    weight="bold",
                    color=ft.colors.WHITE),
            ft.ElevatedButton(
                "Show World Map",
                on_click=go_to_map,
                style=ft.ButtonStyle(
                    bgcolor="#4CCD77",
                    color=ft.colors.WHITE,
                    padding=20,
                    shape=ft.RoundedRectangleBorder(radius=10)
                )
            ),
            ft.ElevatedButton(
                "News",
                on_click=go_to_news,
                style=ft.ButtonStyle(
                    bgcolor="#4CCD77",
                    color=ft.colors.WHITE,
                    padding=20,
                    shape=ft.RoundedRectangleBorder(radius=10)
                ))
        ],
        spacing=40,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    page.add(main_page)

ft.app(target=main)
