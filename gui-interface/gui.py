from os import getenv

from dotenv import load_dotenv
from guizero import (App, Box, ButtonGroup, ListBox, Picture, PushButton, Text,
                     TextBox, Window)

from crud import DataBase

def check_number(valor):
    value_str = valor.replace(',', '.')
    try:
        float(value_str)
    except Exception:
        return
    else:
        return value_str
    

def add(window,id,title, value, description):
    connect = DataBase(
        host=getenv('HOST', ''),
        user=getenv('USER', ''),
        password=getenv('PASSWORD', ''),
        db_name=getenv('DB_NAME', ''),
        db_port=getenv('PORT', )
    )
    checked_number = check_number(value.value)
    if '' in (title.value, value.value, description.value):
        window.info(title='info', text='Informe valores para todos os atributos!')
    elif checked_number is None:
        window.info(title='info', text='Informe um valor númerico válido!')
    else:
        description = description.value.replace('\n','')
        if description == "Descrição do produto":
            connect.create('produtos', fields=['id_loja','titulo', 'valor'], values=[
            id,title.value, checked_number
        ])
        else:
            connect.create('produtos', fields=['id_loja','titulo', 'valor', 'descricao'], values=[
                id,title.value, checked_number, description
            ])
        connect.close()
        window.destroy() 


def edit(window, connection, reg, new_reg):
    checked_number = check_number(new_reg[1].value)
    if '' in (new_reg[0].value, new_reg[2].value, new_reg[1].value):
        window.info(title='info', text='Informe valores para todos os atributos!')
    elif checked_number is None:
        window.info(title='info', text='Informe um valor númerico válido!')
    else:
        reg_modified = {'titulo': new_reg[0].value, 'valor': checked_number,
                        'descricao': new_reg[2].value.replace('\n','')}
        changed_values = [(k, v) for k, v in reg_modified.items() if not reg[k] == v]
        for key in reg.keys():
            if key in ('id_produto', 'id_loja'):
                pass
            else:
                connection.update('produtos', key, reg_modified[key], 'id_produto', reg['id_produto'])
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
    connection.delete('produtos', 'id_produto', registry_remove['id_produto'])
    connection.close()
    close_window_search()


def window_add(id):
    window = Window(app, width=400, height=250, title='Adicionar Produto')
    window.bg = '#EDE7DF'
    box_inputs = Box(window,layout='grid',width='fill')
    text_title = Text(box_inputs, text='Título:', grid=[0, 0])
    input_title = TextBox(box_inputs, grid=[1, 0], width=20)
    text_value = Text(box_inputs, text='Valor:', grid=[2, 0])
    value_input =TextBox(box_inputs,grid=[3,0],width=20)
    ghost_box = Box(window, height='20', width='fill')
    box_descriptions = Box(window,width='fill',height=100)
    description = TextBox(box_descriptions,width='fill', height=100,multiline=True, text="Descrição do produto")
    ghost_box_3 = Box(window,height=50,width='fill')
    button = PushButton(window, text="Cadastrar", command=add, args=[
                window,id, input_title, value_input, description])
    text_title.font = text_value.font = button.font = 'Calibri'
    input_title.bg = value_input.bg = description.bg =  'white'
    button.bg = '#CB9888'
    window.tk.resizable(0, 0)
    window.show(wait=True)


def window_edit(connect, reg):
    try:
        reg_dict = eval(reg.value)
    except TypeError:
        return

    window = Window(app, width=400, height=250, title='Janela de Edição')
    window.bg = '#EDE7DF'
    box_inputs = Box(window,layout='grid',width='fill')
    text_title = Text(box_inputs, text='Título:', grid=[0, 0])
    input_title = TextBox(box_inputs, grid=[1, 0], width=20,text=reg_dict['titulo'])
    text_value = Text(box_inputs, text='Valor:', grid=[2, 0])
    value_input =TextBox(box_inputs,grid=[3,0],width=20,text=reg_dict['valor'])
    ghost_box = Box(window, height='20', width='fill')
    box_descriptions = Box(window,width='fill',height=100)
    description = TextBox(box_descriptions,width='fill', height=100,multiline=True, text=reg_dict['descricao'])
    ghost_box_3 = Box(window,height=50,width='fill')
    new_reg = [input_title, value_input, description]
    button = PushButton(window, grid=[2, 4], text="Atualizar", command=edit, args=[window, connect, reg_dict, new_reg])
    text_title.font = text_value.font = description.font = button.font = 'Calibri'
    input_title.bg = value_input.bg = description.bg = 'white'
    button.bg = '#CB9888'
    window.tk.resizable(0, 0)
    window.show(wait=True)


def search(window,id):
    search_method = window.question('Método de busca', "Insira o nome dos registros que deseja buscar\nou "
                                    "deixe em branco para obter todos os registros.")
    if search_method is None:
        return
    connect = DataBase(
        host=getenv('HOST', ''),
        user=getenv('USER', ''),
        password=getenv('PASSWORD', ''),
        db_name=getenv('DB_NAME', ''),
        db_port =getenv('PORT',)
    )
    if search_method not in (None, ''):
        rows = connect.read(fields='', table='produtos', where_fields=['titulo', 'id_loja'], where_values=[search_method.lower(),id],
                            exact_match_attr=['titulo'])
    else:
        rows = connect.read(fields='', table='produtos', where_fields=['id_loja'], where_values=[id])
    if len(rows) == 0:
        window.info("Info", "Sua busca não resultou em nenhum registro!")
    else:
        result_search = []
        for reg in rows:
            result_search.append({'id_produto': reg[0], 'id_loja': reg[1],
                                 'valor': reg[3], 'titulo': reg[4],'descricao': reg[2]})
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
    if pwd_show.image == 'img/senha_nao_visivel.png/':
        pwd_show.image = 'img/senha_visivel.png/'
        pwd_input.hide_text = False
    else:
        pwd_show.image = 'img/senha_nao_visivel.png/'
        pwd_input.hide_text = True


def submit():
    connect = DataBase(
            host=getenv('HOST', ''),
            user=getenv('USER', ''),
            password=getenv('PASSWORD', ''),
            db_name=getenv('DB_NAME', ''),
            db_port=getenv('PORT', )
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
            options = Window(app, width=400, height=250, bg='#EDE7DF', title='Janela de Opções')
            options.when_closed = app.destroy
            box_options = Box(options, layout='grid')
            options.tk.resizable(0, 0)
            ghost_box = Box(box_options, grid=[0, 0], width=10)
            button_add = PushButton(box_options, text="Adicionar", command=window_add, grid=[1, 0],args=[id_store])
            button_search = PushButton(box_options, text="Buscar", command=search, grid=[2, 0], args=[options,id_store])
            button_add.bg = button_search.bg = 'white'
            app.hide()
            options.show()
        else:
            app.warn(title='Inform', text='Email e/ou senha inválidos')
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
pwd_show = Picture(box_info, image="img/senha_nao_visivel.png/", grid=[2, 1])
pwd_show.when_clicked = show_password
ghost_box_2 = Box(box_info, grid=[1, 2], height=15, width=1)
button_submit = PushButton(box_info, text="Fazer login", grid=[1, 3], width='13', command=submit)
button_submit.font = "Calibri"
button_submit.bg = "#CB9888"
app.display()
