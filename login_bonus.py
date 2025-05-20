import flet as ft
import requests
import json

# const
CONTENT_WIDTH = 400
CONTENT_HIGHT = 400

def main(page: ft.Page):

    # ログインボタン押下
    def login_auth(e):
        loginid = tfLoginid.value
        password = tfPassword.value

        url = "http://172.20.63.23/api/01_login"
        header = {
            "Content-Type": "application/json"
        }
        data = {"id": loginid}
        response = requests.post(url, data=json.dumps(data), headers=header)
        statusCode = response.status_code
        result_login = response.json()

        if statusCode == 201:
            result_login_bonus = get_logion_bonus_info(loginid)
            if result_login_bonus["result"]:
                txtMesssage.value = f"ログイン成功！ {result_login['name']} {result_login['address']} {statusCode}"
                txtMesssage.color = ft.Colors.GREEN
                page.open(snackBar)
                page.update()
                page.go("/view2")
        else:
            txtMesssage.value = f"ログイン失敗！ {loginid} {password} {statusCode}"
            txtMesssage.color = ft.Colors.RED
            page.open(snackBar)
            page.update()
    
    # ログインボーナス情報取得
    def get_logion_bonus_info(login_id):
        url = "http://172.20.63.23/api/02_search_login_bonus"
        header = {
            "Content-Type": "application/json"
        }
        data = {"id": login_id}
        response = requests.post(url, data=json.dumps(data), headers=header)
        statusCode = response.status_code
        result = response.json()

        return result
        
    
    # 画面1生成
    def create_view1():
        return ft.View("/view1", [
            ft.AppBar(title=ft.Text("view1"),
                      bgcolor=ft.colors.BLUE),
            ft.TextField(value="view1"),
            ft.ElevatedButton(
                "Go to view2", on_click=lambda _: page.go("/view2")),
        ])
    
    # 画面2生成
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

    # I/O Controls
    txtMesssage = ft.Text(size=30)
    snackBar = ft.SnackBar(txtMesssage)

    # Page レイアウト
    page.title = "Login form"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.add(ft.Divider())

    # I/O Controls
    tfLoginid = ft.TextField(label="Login ID", autofocus=True)
    tfPassword = ft.TextField(label="Password", password=True, can_reveal_password=True)
    btnLogin = ft.ElevatedButton("ログイン", on_click=login_auth)

    # Content
    header = ft.Container(
        ft.Text("ログイン", style=ft.TextThemeStyle.DISPLAY_MEDIUM, weight=ft.FontWeight.BOLD,
                width=CONTENT_WIDTH, text_align=ft.TextAlign.CENTER),
        margin=ft.margin.only(bottom=20),
    )
    body = ft.Column(
        [
            tfLoginid,
            tfPassword,
        ],
    )
    footer = ft.Row(
        [
            btnLogin,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    page.add(
        ft.Container(
            ft.Column(
                [
                    header,
                    body,
                    ft.Divider(),
                    footer,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            width=CONTENT_WIDTH,
            height=CONTENT_HIGHT,
            padding=30,
        ),
    )


if __name__ == "__main__":
    ft.app(target=main)