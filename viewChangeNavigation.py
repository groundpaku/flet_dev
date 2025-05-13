import flet as ft


def main(page: ft.Page):

    def create_view1():
        return ft.View("/view1", [
            ft.AppBar(title=ft.Text("view1"),
                      bgcolor=ft.colors.BLUE),
            ft.TextField(value="view1"),
            ft.ElevatedButton(
                "Go to view2", on_click=lambda _: page.go("/view2")),
        ])

    def create_view2():
        return ft.View("/view2", [
            ft.AppBar(title=ft.Text("view2"),
                      bgcolor=ft.colors.RED),
            ft.TextField(value="view2"),
            ft.ElevatedButton(
                "Go to view1", on_click=lambda _: page.go("/view1")),
        ])

    def route_change(handler):
        troute = ft.TemplateRoute(handler.route)
        if troute.match("/view1"):
            page.views.append(create_view1())
        elif troute.match("/view2"):
            page.views.append(create_view2())
        page.update()

    # ルート変更時のロジック設定
    page.on_route_change = route_change

    def view_pop(handler):
        page.views.pop()  # 1つ前に戻る
        page.go("/back")
        # page.update()
        # update() だと route が変更されない。
        # そうなると1つ戻ってまた進むことができなくなるので go("/back") で回避。不具合？

    # 戻る時のロジック設定
    page.on_view_pop = view_pop

    # Page レイアウト
    page.title = "Navigation and routing"
    # 初期表示
    page.views.clear()
    page.go("/view1")


if __name__ == "__main__":
    ft.app(target=main)
