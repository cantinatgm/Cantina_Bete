from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
import cantina_backend as backend  # Conecta diretamente ao seu script do Google Sheets

class PDVScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(PDVScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15

        # Título
        self.add_widget(Label(text="🛒 Frente de Caixa - Cantina", font_size=22, size_hint_y=None, height=40))

        # Aluno
        self.add_widget(Label(text="Aluno / Cliente:", size_hint_y=None, height=30))
        try:
            self.alunos_dict = backend.obter_alunos().get("alunos_detalhado", {})
        except Exception:
            self.alunos_dict = {}
            
        nomes_alunos = ["VENDA AVULSA"] + list(self.alunos_dict.keys())
        
        self.spinner_aluno = Spinner(text="VENDA AVULSA", values=nomes_alunos, size_hint_y=None, height=45)
        self.add_widget(self.spinner_aluno)

        # Produto
        self.add_widget(Label(text="Produto:", size_hint_y=None, height=30))
        try:
            self.produtos_dict = backend.obter_produtos().get("produtos_detalhado", {})
        except Exception:
            self.produtos_dict = {}
            
        nomes_produtos = list(self.produtos_dict.keys()) if self.produtos_dict else ["Nenhum produto"]

        self.spinner_produto = Spinner(text="Selecione o produto", values=nomes_produtos, size_hint_y=None, height=45)
        self.add_widget(self.spinner_produto)

        # Quantidade com botões - e +
        self.add_widget(Label(text="Quantidade:", size_hint_y=None, height=30))
        
        qtd_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=45, spacing=10)
        
        btn_menos = Button(text="-", font_size=20, size_hint_x=None, width=60)
        btn_menos.bind(on_press=self.decrementar_qtd)
        qtd_layout.add_widget(btn_menos)

        self.txt_qtd = TextInput(text="1", multiline=False, halign="center", font_size=18)
        qtd_layout.add_widget(self.txt_qtd)

        btn_mais = Button(text="+", font_size=20, size_hint_x=None, width=60)
        btn_mais.bind(on_press=self.incrementar_qtd)
        qtd_layout.add_widget(btn_mais)

        self.add_widget(qtd_layout)

        # Botão Adicionar
        btn_add = Button(text="➕ Adicionar Item", background_color=(0, 0.6, 0, 1), size_hint_y=None, height=50)
        btn_add.bind(on_press=self.adicionar_item)
        self.add_widget(btn_add)

        # Visor do Carrinho
        self.lbl_carrinho = Label(text="Carrinho Vazio", font_size=14, halign="left", valign="top")
        self.lbl_carrinho.bind(size=self.lbl_carrinho.setter('text_size'))
        self.add_widget(self.lbl_carrinho)

        self.carrinho = []

    def incrementar_qtd(self, instance):
        try:
            val = int(self.txt_qtd.text)
            self.txt_qtd.text = str(val + 1)
        except ValueError:
            self.txt_qtd.text = "1"

    def decrementar_qtd(self, instance):
        try:
            val = int(self.txt_qtd.text)
            if val > 1:
                self.txt_qtd.text = str(val - 1)
        except ValueError:
            self.txt_qtd.text = "1"

    def adicionar_item(self, instance):
        aluno = self.spinner_aluno.text
        produto = self.spinner_produto.text
        
        if produto not in self.produtos_dict:
            return

        try:
            qtd = int(self.txt_qtd.text)
        except ValueError:
            qtd = 1

        preco = self.produtos_dict[produto].get("valor", 0)
        self.carrinho.append([produto, qtd, preco])
        
        # Atualizar visor do carrinho
        texto_resumo = f"Cliente: {aluno}\n--------------------\n"
        total = 0
        for item in self.carrinho:
            sub = item[1] * item[2]
            total += sub
            texto_resumo += f"{item[0]} (x{item[1]}) - R$ {sub:.2f}\n"
        texto_resumo += f"\nTOTAL: R$ {total:.2f}"
        
        self.lbl_carrinho.text = texto_resumo
        self.txt_qtd.text = "1"

class CantinaApp(App):
    def build(self):
        return PDVScreen()

if __name__ == '__main__':
    CantinaApp().run()