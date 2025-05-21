import flet as ft
import requests
import json

# const
CONTENT_WIDTH = 400
CONTENT_HIGHT = 400

def main(page: ft.Page):

    # 変数
    login_id = ""
    login_bonus_flg = "0"
    login_point = 0

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
            global login_id
            login_id = result_login["id"]
            result_login_bonus = get_logion_bonus_info(login_id)
            if result_login_bonus["result"]:
                global login_bonus_flg
                login_bonus_flg = result_login_bonus["login_bonus_flg"]
                global login_point
                login_point = result_login_bonus["user_info"]["login_point"]
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
    
    # ログインボーナス取得
    def get_login_bonus(e):
        global login_id
        url = "http://172.20.63.23/api/03_update_login_bonus"
        header = {
            "Content-Type": "application/json"
        }
        data = {"id": login_id, "process_kbn": "0"}
        response = requests.post(url, data=json.dumps(data), headers=header)
        statusCode = response.status_code
        result = response.json()
        global login_point
        login_point = result["login_point"]

        txtMesssage.value = f"ログインボーナスを取得しました！ 現在のポイントは{login_point}です"
        txtMesssage.color = ft.Colors.GREEN
        page.open(snackBar)
        point_textfield.value = f"現在のポイント：{login_point}"
        app_bar_text.value = "今日のログインボーナスは受取済みです"
        get_bonus_button.disabled = True
        if login_point >= 7:
            use_bonus_button.disabled = False
        else:
            use_bonus_button.disabled = True
        page.update()
        # page.go("/view2")
    
    # ログインボーナス使用
    def use_login_bonus(e):
        global login_id
        url = "http://172.20.63.23/api/03_update_login_bonus"
        header = {
            "Content-Type": "application/json"
        }
        data = {"id": login_id, "process_kbn": "1"}
        response = requests.post(url, data=json.dumps(data), headers=header)
        statusCode = response.status_code
        result = response.json()
        global login_point
        login_point = result["login_point"]

        txtMesssage.value = f"ログインボーナスを使用しました！ 現在のポイントは{login_point}です"
        txtMesssage.color = ft.Colors.BLUE
        page.open(snackBar)
        point_textfield.value = f"現在のポイント：{login_point}"
        get_bonus_button.disabled = False
        use_bonus_button.disabled = True
        page.update()
        # page.go("/view2")
        
    
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
        global login_bonus_flg
        global login_point
        point_textfield.value = f"現在のポイント：{login_point}"
        if login_point >= 7:
            use_bonus_button.disabled = False
        else:
            use_bonus_button.disabled = True
        
        if login_bonus_flg == "1":
            app_bar_text.value = "ログインボーナスを受け取ることができます"
            get_bonus_button.disabled = False
            return ft.View("/view2", [
            ft.AppBar(title=app_bar_text,
                      bgcolor=ft.Colors.GREEN),
            point_textfield,
            get_bonus_button,
            use_bonus_button,
            ])
        else:
            app_bar_text.value = "今日のログインボーナスは受取済みです"
            get_bonus_button.disabled = True
            return ft.View("/view2", [
            ft.AppBar(title=app_bar_text,
                      bgcolor=ft.Colors.RED),
            point_textfield,
            get_bonus_button,
            use_bonus_button,
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

    # View2のI/O
    app_bar_text = ft.Text("ログインボーナスを受け取ることができます")
    point_textfield = ft.TextField(value=f"現在のポイント：{str(login_point)}")
    get_bonus_button = ft.ElevatedButton(
                "ログインボーナスを受け取る", on_click=get_login_bonus)
    use_bonus_button = ft.ElevatedButton(
                "ログインボーナスを使う", on_click=use_login_bonus)


if __name__ == "__main__":
    ft.app(target=main)