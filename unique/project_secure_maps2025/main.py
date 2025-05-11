import flet as ft
from flet_map import Map, MapLatitudeLongitude, MarkerLayer, Marker, TileLayer, MapInteractionConfiguration, \
    MapInteractiveFlag, RichAttribution, TextSourceAttribution
import requests
from datetime import datetime
import pytz


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
            add_marker(el["latitude"], el["longitude"], el["name_of_mark"], "", "BLUE", int(el["time"]))
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

    def add_marker(lat, lng, title="", description="", color="BLUE", mark_time=0):
        if marker_layer_ref.current:
            marker_color = getattr(ft.colors, color)

            ny_time = datetime.now(pytz.timezone('America/New_York'))
            ny_time = int(ny_time.strftime('%H'))

            hour_diff = (ny_time - mark_time) % 24

            if hour_diff >= 24 or ny_time == mark_time:
                marker_color = ft.colors.GREEN
            elif hour_diff >= 12:
                marker_color = ft.colors.YELLOW
            elif hour_diff >= 4:
                marker_color = ft.colors.ORANGE
            else:
                marker_color = ft.colors.RED


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

    def open_full_description(e, full_description, images, date):
        page.clean()

        back_button = ft.Container(
            content=ft.ElevatedButton(
                "Back to Home",
                on_click=go_back,
                style=ft.ButtonStyle(
                    bgcolor="#4CCD77",
                    color=ft.colors.WHITE,
                    padding=20,
                    shape=ft.RoundedRectangleBorder(radius=10)
                )
            ),
            alignment=ft.alignment.center,
            padding=10
        )

        images_row = ft.Row(
            scroll=True,
            wrap=False,
            alignment=ft.MainAxisAlignment.CENTER
        )

        for image in images:
            if image:
                images_row.controls.append(
                    ft.Image(
                        src=image,
                        width=700,
                        height=200,
                        fit=ft.ImageFit.CONTAIN,
                        border_radius=ft.border_radius.only(top_left=10, top_right=10),
                    )
                )

        text_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        full_description,
                        size=16,
                        weight="bold",
                        color=ft.colors.WHITE,
                    ),
                    ft.Text(
                        date,
                        size=12,
                        color=ft.colors.WHITE60,
                    )
                ],
                spacing=10,
            ),
            padding=20,
            width=700,
        )

        full_description_page = ft.Column(
            controls=[
                back_button,
                ft.Container(
                    content=images_row,
                    alignment=ft.alignment.center,
                    padding=10
                ),
                text_container
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=True,
            expand=True
        )

        page.add(full_description_page)

    def go_to_news(e):
        try:
            response = requests.get("https://kkhludov.pythonanywhere.com/api/news")
            news = response.json()
        except Exception as e:
            print(f"Error: {e}")
            news = []

        # Функция создания карточки новости
        def create_article_box(article):
            images = article["images"].split()
            main_image = images[0] if images else None

            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Image(
                                src=main_image,
                                width=700,
                                height=500,
                                fit=ft.ImageFit.FILL,  # Изменено с COVER на CONTAIN
                                border_radius=10,
                                gapless_playback=True,
                                error_content=ft.Icon(ft.icons.IMAGE_NOT_SUPPORTED, size=50, color=ft.colors.GREY_400),
                            ) if main_image else ft.Container(
                                height=500,
                                bgcolor=ft.colors.GREY_800,
                                alignment=ft.alignment.center,
                                content=ft.Icon(ft.icons.IMAGE_NOT_SUPPORTED, size=50, color=ft.colors.GREY_400),
                                border_radius=10
                            ),
                            height=400,  # Фиксированная высота контейнера
                            width=700,  # Фиксированная ширина контейнера
                            alignment=ft.alignment.center,  # Выравнивание по центру
                            clip_behavior=ft.ClipBehavior.HARD_EDGE,
                            border_radius=10,
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        article["short_description"],
                                        size=16,
                                        weight="bold",
                                        color=ft.colors.WHITE
                                    ),
                                    ft.Text(
                                        article["date"],
                                        size=12,
                                        color=ft.colors.WHITE60,
                                    ),
                                    ft.Text(
                                        "Read more",
                                        size=14,
                                        color=ft.colors.BLUE_200,
                                    )
                                ],
                                spacing=5
                            ),
                            padding=10,
                        )
                    ],
                    spacing=0,
                ),
                bgcolor="#363636",
                border_radius=10,
                width=700,
                on_click=lambda e, desc=article["full_description"],
                                imgs=images,
                                dt=article["date"]: open_full_description(e, desc, imgs, dt),
                margin=ft.margin.only(bottom=10),
            )

        def search_articles(e):
            search_query = search_field.value.lower()
            filtered_articles = [
                article for article in news
                if search_query in article["short_description"].lower()
            ]

            news_list.controls.clear()

            if not filtered_articles:
                news_list.controls.append(
                    ft.Text("No articles found", color=ft.colors.WHITE)
                )
            else:
                for article in filtered_articles:
                    news_list.controls.append(create_article_box(article))

            page.update()

        search_field = ft.TextField(
            width=500,
            hint_text="Search news...",
            focused_bgcolor="#282828",
            focused_border_color="#4CCD77",
            bgcolor="#282828",
            border_color="#282828",
            focused_color="white",
            color="white",
        )

        news_list = ft.Column(scroll=True)

        for article in news:
            news_list.controls.append(create_article_box(article))

        news_page = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            "Back to Home",
                            on_click=go_back,
                            style=ft.ButtonStyle(
                                bgcolor="#4CCD77",
                                color=ft.colors.WHITE,
                                padding=20,
                                shape=ft.RoundedRectangleBorder(radius=10)
                            ),)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    controls=[
                        search_field,
                        ft.ElevatedButton(
                            content=ft.Text("Search", color=ft.colors.WHITE),
                            on_click=search_articles,
                            bgcolor="#4CCD77",
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                news_list
            ],
            scroll=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        page.clean()
        page.add(news_page)

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
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    page.add(main_page)

ft.app(target=main)
