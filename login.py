import flet as ft
import requests

# const
CONTENT_WIDTH = 400
CONTENT_HIGHT = 400

def main(page: ft.Page):

    def open_login(e):
        # dlgLogin.open = True
        page.update()

    def close_login(e):
        # dlgLogin.open = False
        page.update()

    def login_auth(e):
        loginid = tfLoginid.value
        password = tfPassword.value

        url = "https://api.github.com/user"
        data = {"login": loginid, "password": password}
        response = requests.post(url, data=data, auth=(loginid, password))
        statusCode = response.status_code

        if loginid == "hoge" and password == "hoge":
            txtMesssage.value = f"ログイン成功！ {loginid} {password} {statusCode}"
            txtMesssage.color = ft.Colors.GREEN
        else:
            txtMesssage.value = f"ログイン失敗！ {loginid} {password} {statusCode}"
            txtMesssage.color = ft.Colors.RED
        page.open(snackBar)
        page.update()

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