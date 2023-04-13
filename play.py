import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from auth import Auth
from reg import Reg
from master import Master
from main import connection_to_db

app = QtWidgets.QApplication(sys.argv)

SignIn = QtWidgets.QWidget()
ui = Auth()
ui.setupUi(SignIn)
SignIn.show()

def Main():
    global main_w
    main_w = QtWidgets.QWidget()
    ui_main_w = Master()
    ui_main_w.setupUi(main_w)
    login = ui.lineEdit.text()
    password = ui.lineEdit_2.text()
    conn = connection_to_db()
    with conn.cursor() as cursor:
        cursor.execute(f'select login, password from users')
        users = cursor.fetchall()
        for user in users:
            if user[0] == login and user[1] == password:
                SignIn.close()
                main_w.show()
                break


ui.pushButton.clicked.connect(Main)

def LogIn():
    global auth_w
    auth_w = QtWidgets.QWidget()
    ui_auth_w = Reg()
    ui_auth_w.setupUi(auth_w)
    SignIn.close()  # закрыть
    # SignIn.hide() спрятать
    auth_w.show()

    def back():
        login = ui_auth_w.lineEdit.text()
        password = ui_auth_w.lineEdit_2.text()
        if len(login) > 0 and len(password) > 0:
            conn = connection_to_db()
            is_login = False
            with conn.cursor() as cursor:
                cursor.execute(f'select login from users')
                users = cursor.fetchall()
                for user in users:
                    if login in user:
                        is_login = True
                        break
            with conn.cursor() as cursor:
                if not is_login:
                    query = f"INSERT INTO users (login, password) VALUES ('{login}', '{password}');"
                    cursor.execute(query)
                    conn.commit()
                    print(f'Зарегистрирован пользователь {login}')
                    auth_w.close()
                    SignIn.show()
                else:
                    print('Логин занят')

    ui_auth_w.pushButton.clicked.connect(back)

ui.pushButton_2.clicked.connect(LogIn)

sys.exit(app.exec_())