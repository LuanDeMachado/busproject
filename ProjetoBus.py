from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from datetime import datetime, timedelta
from dados_onibus import dados_onibus

class BusApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Título
        self.titulo = Label(text="Horários de Ônibus (Somente Horários Completos)", font_size=24, bold=True)
        self.layout.add_widget(self.titulo)
        
        # Spinners
        self.spinner_linha = Spinner(
            text="Selecione a linha",
            values=sorted(dados_onibus.keys()),
            size_hint=(1, 0.1)
        )
        
        self.spinner_dia = Spinner(
            text="Selecione o dia",
            values=[],
            size_hint=(1, 0.1),
            disabled=True
        )
        
        self.spinner_ponto = Spinner(
            text="Selecione o ponto",
            values=[],
            size_hint=(1, 0.1),
            disabled=True
        )
        
        # Botão
        self.botao = Button(
            text="Ver próximo horário",
            size_hint=(1, 0.2),
            background_color=(0, 0.7, 0, 1),
            disabled=True
        )
        
        # Resultado
        self.resultado = Label(
            text="",
            font_size=18,
            halign="center",
            valign="middle",
            size_hint_y=0.4
        )
        
        # Adicionando widgets
        for widget in [
            self.spinner_linha,
            self.spinner_dia,
            self.spinner_ponto,
            self.botao,
            self.resultado
        ]:
            self.layout.add_widget(widget)
        
        # Eventos
        self.spinner_linha.bind(text=self.atualizar_dias)
        self.spinner_dia.bind(text=self.atualizar_pontos)
        self.spinner_ponto.bind(text=self.verificar_botao)
        self.botao.bind(on_press=self.calcular_proximo_horario)
        
        return self.layout
    
    def atualizar_dias(self, spinner, linha):
        if linha in dados_onibus:
            dias = list(dados_onibus[linha].keys())
            self.spinner_dia.values = dias
            self.spinner_dia.disabled = False
            self.spinner_dia.text = "Selecione o dia"
            
            self.spinner_ponto.values = []
            self.spinner_ponto.text = "Selecione o ponto"
            self.spinner_ponto.disabled = True
            self.botao.disabled = True
            self.resultado.text = ""
    
    def atualizar_pontos(self, spinner, dia):
        linha = self.spinner_linha.text
        if linha in dados_onibus and dia in dados_onibus[linha]:
            pontos = list(dados_onibus[linha][dia]['pontos'].keys())
            self.spinner_ponto.values = pontos
            self.spinner_ponto.disabled = False
            self.spinner_ponto.text = "Selecione o ponto"
            self.botao.disabled = True
            self.resultado.text = ""
    
    def verificar_botao(self, spinner, ponto):
        if ponto:
            self.botao.disabled = False
    
    def calcular_proximo_horario(self, instance):
        linha = self.spinner_linha.text
        dia = self.spinner_dia.text
        ponto = self.spinner_ponto.text
        
        if not all([linha, dia, ponto]):
            self.resultado.text = "Selecione todas as opções"
            return
        
        try:
            horario_atual = datetime.now().strftime("%H:%M")
            tempo_atual = datetime.strptime(horario_atual, "%H:%M")
            
            horarios = dados_onibus[linha][dia]['horarios']
            tempos = [datetime.strptime(h, "%H:%M") for h in horarios]
            
            ponto_minutos = dados_onibus[linha][dia]['pontos'][ponto]
            
            for horario in tempos:
                horario_chegada = horario + timedelta(minutes=ponto_minutos)
                if horario_chegada > tempo_atual:
                    self.resultado.text = (
                        f"Próximo ônibus para {linha}\n"
                        f"Ponto: {ponto}\n"
                        f"Chegada prevista: {horario_chegada.strftime('%H:%M')}"
                    )
                    return
            
            self.resultado.text = "Não há mais ônibus hoje."
        except:
            self.resultado.text = "Erro ao calcular horário"

if __name__ == '__main__':
    BusApp().run()
