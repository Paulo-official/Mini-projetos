from flet import *
import sqlite3

#Conectando com o banco de dados
conexao = sqlite3.connect('BD_crud.db', check_same_thread=False)
cursor = conexao.cursor()

#Criando tabela no banco de dados
def tabela_base():
    cursor.execute(
        '''
    CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT)
'''
    )

class App(UserControl):
    def __init__(self):
        super().__init__()

        self.todos_dados = Column(auto_scroll=True)
        self.adicionar_dados = TextField(label='Insira seu nome')
        self.editar_dado = TextField(label='Editar')


    #Deletar dados - DELETE
    def deletar(self):
        pass


    #Criar função para abrir ações
    def abrir_acoes(self, e):
        id = e.control.subititel.value
        self.editar_dado.value = e.control.title.value
        self.update()

        alerta_dialogo = AlertDialog(
            title=f'Editar ID {id_editar}',
            contetnt=self.editar_dado,

            #Botões de ação
            actions=[
                ElevatedButton(
                    'Deletar'
                    color='white', bgcolor='red'
                    on_click= lambda e:self.deletar()
                )
            ]
        )

    #Criar um novo dado dentro do banco de dados - CREATE
    def adicionar_novo_dado(self, e):
        cursor.execute('INSERT INTO clientes (nome) values (?)', [self.adicionar_dados.value]),
    
        self.todos_dados.controls.clear()
        self.renderizar_todos()
        self.page.update()

    #Mostrar dados do banco de dados - READ
    def renderizar_todos(self):
        cursor.execute('SELECT * FROM clientes'),
        conexao.commit()

        meus_dados = cursor.fetchall()

        for dado in meus_dados:
            self.todos_dados.controls.append(
                ListTile(
                    subtitle=Text(dado[0]),
                    title=Text(dado[1]),
                    on_click=self.abrir_acoes
                )
            )


    def build(self):
        return Column([
            Text('Crud com SQLite', size=20, weight='bold'),
            self.adicionar_dados,
            ElevatedButton(
                'Nova informação',
                on_click=self.adicionar_novo_dado,
            ),
            self.todos_dados,
        ])


def main(page:Page):
    minha_aplicacao = App()
    page.add(
        minha_aplicacao
    )

app(target=main)











