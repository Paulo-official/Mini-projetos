import flet
from flet import(
    Checkbox,
    Column,
    FloatingActionButton,
    IconButton,
    OutlinedButton,
    Page,
    Row,
    Tabs,
    Tab,
    Text,
    TextField,
    UserControl,
    colors,
    icons
) #importando ferramentas

#Classe de tarefas
class Task(UserControl):
    def __init__(self, task_name, task_status_change, task_delete):
        super().__init__()
        self.complete = False
        self.task_name = task_name
        self.task_status_change = task_status_change
        self.task_delete = task_delete

    def build(self):
        self.display_task = Checkbox(
            value=False, label=self.task_name, on_change=self.task_status_change
        )

        self.edit_name = TextField(expand=1)

        self.display_view = Row(
            alignment='sapceBetween',
            vertical_alignment= 'center',
            controls=[
                self.display_task,
                Row(
                    spacing=0,
                    controls=[
                        IconButton(
                            icon=icons.CREATE_OUTLINED,
                            tooltip='Editar tarefa',
                            on_click=self.edit_clicked,
                            icon_color=colors.BLUE,
                        ),
                        IconButton(
                            icon=icons.DELETE_OUTLINED,
                            tooltip='Deleter tarefa',
                            on_click=self.delete_clicked,
                            icon_color=colors.RED,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view = Row(
            visible=False,
            alignment='spaceBetween',
            vertical_alignment='center',
            controls=[
                IconButton(
                    icon=icons.DONE_OUTLINE_OUTLINED,
                    icon_color=colors.GREEN,
                    tooltip='Atualizar tarefa',
                    on_click=self.save_clicked,
                )
            ]
        )
        return Column(controls=[self.display_view, self.edit_view])

    def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update
        

    def delete_clicked(self, e):
        self.task_delete(self)
        self.update

    def status_changed(self, e):
        self.complete = self.display_task.value
        self.task_status_change(self)

    def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update
#Classe da aplicação inteira
class base(UserControl):
    def build(self):
        self.new_task = TextField(
            hint_text ='Digite a tarefa aqui',
            expand=True,
            on_submit = self.add_clicked,
        )
        self.task = Column()

        self.filter = Tabs(
            selected_index = 0,
            on_change = self.tabs_change,
            tabs=[Tab(text='Todas tarefas'), Tab(text='Ativas'), Tab(text='Completas')]
        )

        self.items_left = Text('0 tarefas adicionadas')

        return Column(
            width=600,
            controls=[
                Row([Text(value='Tarefas',
                        style = 'headlineMedium')], alignment='center'),
                Row(
                    controls=[
                        self.new_task,
                        FloatingActionButton(icon=icons.ADD, on_click = self.add_clicked)
                    ],
                ),
                Column(
                    spacing=20,
                    controls=[
                        self.filter,
                        self.task,
                        Row(
                            alignment='spaceBetween',
                            vertical_alignment='center',
                            controls=[
                                self.items_left,
                                OutlinedButton(
                                    text='Limpar',
                                    on_click = self.clear_clicked
                                ),
                                OutlinedButton(
                                    text='Limpar tarefas completas'.upper(),
                                    on_click=self.clear_clicked
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )
    
    def add_clicked(self, e):
        if self.new_task.value:
            task = Task(self.new_task.value, self.task_status_change, self.task_delete)
            self.task.controls.append(task)
            self.new_task.value = ''
            self.new_task.focus()
            self.update()
    
    def task_status_change(self, task):
        self.update()

    def task_delete(self, task):
        self.task.controls.remove(task)
        self.update()

    def tabs_change(self, e):
        self.update()

    def clear_clicked(self, task):
        for task in self.task.controls[:]:
            if (task.complete):
                self.task_delete(task)
        self.update()

    def update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        count = 0
        for task in self.task.controls:
            task.visible = (
                status == 'Todas tarefas'
                or (status == 'Tarefas ativas' and task.complete == False)
                or (status == 'Tarefas completas' and task.complete == True)
            )
            if not task.complete:
                count += 1
        self.items_left.value = f'{count} tarefa(s) adicionadas'
        super().update()

#Função principal
def main(page: Page):
    page.title = 'To-do'
    page.horizontal_alignment = 'center'
    page.scroll = 'adaptative'
    page.update()

    # Classe principal
    app = base()
    
    # Colocando os dados no app
    page.add(app)

flet.app(target=main)