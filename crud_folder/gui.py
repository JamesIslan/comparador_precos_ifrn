from os import getenv

from dotenv import load_dotenv
from guizero import (App, Box, ButtonGroup, ListBox, Picture, PushButton, Text,
                     TextBox, Window)

from crud import DataBase


def add(window, name, email, sex, phone):
    connect = DataBase(
        host=getenv('HOST', ''),
        user=getenv('USER', ''),
        password=getenv('PASSWORD', ''),
        db_name=getenv('DB_NAME', '')
    )
    if '' in (name.value, email.value, sex.value, phone.value):
        window.info(title='info', text='Informe valores para todos os atributos!')
    else:
        connect.create('cliente', fields=['nome', 'email', 'sexo', 'telefone'], values=[
            name.value, email.value, sex.value, phone.value
        ])
        connect.close()
        window.destroy()


def edit(window, connection, reg, new_reg):
    reg_modified = {'nome': new_reg[0].value, 'email': new_reg[1].value,
                    'sexo': new_reg[2].value, 'telefone': new_reg[3].value}
    changed_values = [(k, v) for k, v in reg_modified.items() if not reg[k] == v]
    for key in reg.keys():
        if key == 'id_cliente':
            pass
        else:
            connection.update('cliente', key, reg_modified[key], 'id_cliente', reg['id_cliente'])
    connection.close()
    window.destroy()
    close_window_search()


def close_window_search():
    window_search_result.hide()
    options.show()


def remove(connection, reg):
    try:
        registry_remove = eval(reg.value)
    except TypeError:
        return
    connection.delete('cliente', 'id_cliente', registry_remove['id_cliente'])
    connection.close()
    close_window_search()


def window_add():
    window = Window(app, width=400, height=250, layout='grid')
    window.bg = '#EDE7DF'
    text_name = Text(window, text='Nome:', grid=[0, 0])
    input_name = TextBox(window, grid=[1, 0], width=20)
    sex_name = Text(window, text='  Sexo:', grid=[2, 0])
    sex_input = ButtonGroup(window, options=['m', 'f'], selected='m', grid=[3, 0], horizontal=True)
    ghost_box = Box(window, height='20', grid=[0, 1])
    text_email = Text(window, text='Email:', grid=[0, 2])
    input_email = TextBox(window, grid=[1, 2], width=20)
    phone_text = Text(window, text='   Telefone:', grid=[2, 2])
    phone_input = TextBox(window, grid=[3, 2], width=20)
    ghost_box_3 = Box(window, grid=[0, 3], height=50)
    button = PushButton(window, grid=[2, 4], text="Cadastrar", command=add, args=[
                        window, input_name, input_email, sex_input, phone_input])
    text_name.font = sex_name.font = text_email.font = phone_text.font = button.font = 'Calibri'
    input_name.bg = input_email.bg = phone_input.bg = 'white'
    button.bg = '#CB9888'
    window.tk.resizable(0, 0)
    window.show(wait=True)


def window_edit(connect, reg):
    try:
        reg_dict = eval(reg.value)
    except TypeError:
        return

    window = Window(app, width=400, height=250, layout='grid')
    window.bg = '#EDE7DF'
    text_name = Text(window, text='Nome:', grid=[0, 0])
    name = TextBox(window, grid=[1, 0], width=20, text=reg_dict['nome'])
    sex_name = Text(window, text='  Sexo:', grid=[2, 0])
    sex = ButtonGroup(window, options=['m', 'f'], selected=reg_dict['sexo'], grid=[3, 0], horizontal=True)
    ghost_box = Box(window, height='20', grid=[0, 1])
    text_email = Text(window, text='Email:', grid=[0, 2])
    email = TextBox(window, grid=[1, 2], width=20, text=reg_dict['email'])
    phone_text = Text(window, text='   Telefone:', grid=[2, 2])
    phone = TextBox(window, grid=[3, 2], width=20, text=reg_dict['telefone'])
    ghost_box_3 = Box(window, grid=[0, 3], height=50)
    new_reg = [name, email, sex, phone]
    button = PushButton(window, grid=[2, 4], text="Atualizar", command=edit, args=[window, connect, reg_dict, new_reg])
    text_name.font = sex_name.font = email.font = phone_text.font = button.font = 'Calibri'
    name.bg = email.bg = phone.bg = 'white'
    button.bg = '#CB9888'
    window.tk.resizable(0, 0)
    window.show(wait=True)


def search(window,id):
    print(id)
    search_method = window.question('Método de busca', "Insira o nome dos registros que deseja buscar\nou "
                                    "deixe em branco para obter todos os registros.")
    connect = DataBase(
        host=getenv('HOST', ''),
        user=getenv('USER', ''),
        password=getenv('PASSWORD', ''),
        db_name=getenv('DB_NAME', '')
    )
    if search_method not in (None, ''):
        rows = connect.read(fields='', table='produtos', where_fields=['titulo', 'id_loja'], where_values=[search_method,id])
    else:
        rows = connect.read(fields='', table='produtos', where_fields=['id_loja','titulo'], where_values=[id])
    if len(rows) == 0:
        window.info("Info", "Sua busca não resultou em nenhum registro!")
    else:
        result_search = []
        for reg in rows:
            result_search.append({'id_produto': reg[0], 'id_loja': reg[1],
                                 'descricao': reg[2], 'valor': reg[3], 'titulo': reg[4]})
        global window_search_result
        window_search_result = Window(window, width=580, height=345, title='Resultados da busca')
        window_search_result.bg = '#EDE7DF'
        box = Box(window_search_result, width='fill')
        listbox = ListBox(box, items=result_search, scrollbar=True, width=550, height=250)
        ghost_box = Box(window_search_result, width='fill', height=50)
        box_options = Box(window_search_result, width='fill', height=50, layout='grid')
        ghost_box_options = Box(box_options, grid=[0, 0], width=250)
        button_edit = PushButton(box_options, text="Editar", command=window_edit, grid=[1, 0], args=[connect, listbox])
        button_remove = PushButton(box_options, text="Excluir", command=remove, grid=[2, 0], args=[connect, listbox])
        button_edit.bg = button_remove.bg = "#CB9888"
        button_edit.font = button_remove.font = "Calibri"
        listbox.bg = 'white'
        window_search_result.when_closed = close_window_search
        window_search_result.tk.resizable(0, 0)
        window.hide()
        window_search_result.show()


def show_password():
    if pwd_show.image == 'crud_folder/img/senha_nao_visivel.png/':
        pwd_show.image = 'crud_folder/img/senha_visivel.png/'
        pwd_input.hide_text = False
    else:
        pwd_show.image = 'crud_folder/img/senha_nao_visivel.png/'
        pwd_input.hide_text = True


def submit():
    connect = DataBase(
            host=getenv('HOST', ''),
            user=getenv('USER', ''),
            password=getenv('PASSWORD', ''),
            db_name=getenv('DB_NAME', '')
        )
    if pwd_input.value.strip() == '' or email_input.value.strip() == '':
        app.info("Inform", "Informe um valor de email e senha para de efetuar o login!")
        pwd_input.value = email_input.value = ''
    else:
        rows = connect.read(fields=['email','password_hash'], table='lojas')
        data_input = (email_input.value, pwd_input.value)
        if data_input in rows:
            id_store = connect.read(fields=['id_loja'],table='lojas', where_fields=['email'], where_values=[email_input.value])[0][0]
            global options
            options = Window(app, width=400, height=250, bg='#EDE7DF',)
            options.when_closed = app.destroy
            box_options = Box(options, layout='grid')
            options.tk.resizable(0, 0)
            ghost_box = Box(box_options, grid=[0, 0], width=10)
            button_add = PushButton(box_options, text="Adicionar", command=window_add, grid=[1, 0])
            button_search = PushButton(box_options, text="Buscar", command=search, grid=[2, 0], args=[options,id_store])
            button_add.bg = button_search.bg = 'white'
            app.hide()
            options.show()
        else:
            app.warn(title='Inform', text='Usuário e/ou senha inválidos')
            pwd_input.value = email_input.value = ''
    connect.close()


def focus_email():
    email_input.focus()


def focus_password():
    pwd_input.focus()


load_dotenv()
app = App(title="Gerenciador MePoupe", bg='#EDE7DF', width='400', height='250')
app.tk.resizable(0, 0)
ghost_box_1 = Box(app, width='fill', height=75)
box_info = Box(app, layout='grid')
email_text = Text(box_info, text="Email:", grid=[0, 0], size=15, font='Times')
email_text.when_clicked = focus_email
email_input = TextBox(box_info, grid=[1, 0], width='fill')
email_input.bg = 'white'
pwd_text = Text(box_info, text="Senha:", grid=[0, 1], size=15, font='Times')
pwd_text.when_clicked = focus_password
pwd_input = TextBox(box_info, hide_text=True, grid=[1, 1], width='fill')
pwd_input.bg = 'white'
pwd_show = Picture(box_info, image="crud_folder/img/senha_nao_visivel.png/", grid=[2, 1])
pwd_show.when_clicked = show_password
ghost_box_2 = Box(box_info, grid=[1, 2], height=15, width=1)
button_submit = PushButton(box_info, text="Fazer login", grid=[1, 3], width='13', command=submit)
button_submit.font = "Calibri"
button_submit.bg = "#CB9888"
app.display()