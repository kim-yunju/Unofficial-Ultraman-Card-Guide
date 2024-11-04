from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner  # 스크롤 버튼 추가
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
import pandas as pd
from kivy.resources import resource_add_path
import os

# 앱 실행 디렉토리를 리소스 경로로 추가
resource_add_path(os.path.dirname(__file__))

# CSV 파일 읽기
df = pd.read_csv('data1104.CSV')

# 폰트 경로 설정
font_name = 'NanumGothic.ttf'

class InputScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 전체 화면 레이아웃 설정
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # 빈 공간을 추가하여 입력창과 검색 버튼을 화면 중앙에 배치
        main_layout.add_widget(BoxLayout(size_hint_y=1))  # 상단의 빈 공간

        # 입력창과 검색 버튼 레이아웃 설정 (중앙에 배치)
        input_layout = BoxLayout(orientation='vertical', spacing=20, size_hint=(1, None))
        input_layout.pos_hint = {"center_x": 0.5}

        # 앞부분 선택 스크롤 버튼과 뒷부분 입력 텍스트를 한 행에 배치할 레이아웃
        selection_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, None), height=100)

        # 앞부분 선택 스크롤 버튼 추가 (4:6 비율로 설정)
        self.prefix_spinner = Spinner(
            text='시리즈 코드 선택',
            values=('SD01', 'SD02', 'BP01', 'PR'),  # 선택 가능한 값들
            size_hint=(0.4, 1),  # 4:6 비율로 설정
            font_name=font_name,
            font_size=48  # 폰트 크기 설정
        )
        selection_layout.add_widget(self.prefix_spinner)

        # 뒷부분 입력 텍스트 추가 (4:6 비율로 설정)
        self.text_input = TextInput(
            hint_text='카드 번호 입력',
            multiline=False,
            font_name=font_name,
            size_hint=(0.6, 1),
            font_size=48, # 폰트 크기 설정
            padding=[15, 15] 
        )
        selection_layout.add_widget(self.text_input)

        # 입력란과 스크롤 버튼 레이아웃을 입력 레이아웃에 추가
        input_layout.add_widget(selection_layout)

        # 검색 버튼 추가
        self.search_button = Button(text='검색', font_name=font_name, size_hint=(1, None), height=100, font_size=48)
        self.search_button.bind(on_press=self.on_search_button_click)
        input_layout.add_widget(self.search_button)

        # 입력 레이아웃을 메인 레이아웃에 추가
        main_layout.add_widget(input_layout)
        main_layout.add_widget(BoxLayout(size_hint_y=1))  # 하단의 빈 공간

        # 설명 버튼 추가
        info_button_layout = BoxLayout(size_hint=(1, None), height=100)
        self.info_button = Button(text='앱 설명', font_name=font_name, size_hint=(1, None), height=100, font_size=48)
        self.info_button.bind(on_press=self.on_info_button_click)
        info_button_layout.add_widget(self.info_button)

        main_layout.add_widget(info_button_layout)
        self.add_widget(main_layout)

    def on_search_button_click(self, instance):
        # 앞부분과 뒷부분을 결합하여 코드 생성
        user_input = f"{self.prefix_spinner.text}-{self.text_input.text.zfill(3)}"  # 003 형식 유지

        # ScreenManager를 통해 결과 화면에 접근
        result_screen = self.manager.get_screen('result_screen')
        result_screen.display_result(user_input)
        
        # 결과 화면으로 전환
        self.manager.current = 'result_screen'

    def on_info_button_click(self, instance):
        # 설명 화면으로 전환
        self.manager.current = 'info_screen'


class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # 전체 레이아웃 설정
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # 스크롤뷰 추가
        scroll_view = ScrollView()
        self.layout = GridLayout(cols=1, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        scroll_view.add_widget(self.layout)

        # 결과 라벨 추가
        self.result_label = Label(text='', font_name=font_name, size_hint_y=None, font_size=48)
        self.layout.add_widget(self.result_label)
        
        # 스크롤뷰를 메인 레이아웃에 추가
        main_layout.add_widget(scroll_view)

        # 뒤로 가기 버튼 추가
        self.back_button = Button(text='뒤로', font_name=font_name, size_hint_y=None, height=100, font_size=48)
        self.back_button.bind(on_press=self.go_back)
        main_layout.add_widget(self.back_button)
        
        self.add_widget(main_layout)
        Window.bind(on_resize=self.on_window_resize)

    def display_result(self, code):
        if code in df['번호'].values:
            result_row = df[df['번호'] == code].iloc[0]
            if pd.isna(result_row['카드명']) or result_row['카드명'].strip() == '':
                result_text = '\n\n\n\n아직 해당 번호 카드에 대한 정보가 업데이트되지 않았습니다.'
            else:
                result_text = f"\n\n\n\n번호: {result_row['번호']}\n\n카드명: {result_row['카드명']}\n\n효과:\n{result_row['효과']}"
        else:
            result_text = '\n\n\n\n번호를 찾을 수 없습니다.'

        self.result_label.text = result_text
        self.update_label_width()

    def update_label_width(self, *args):
        self.result_label.text_size = (Window.width - 40, None)
        self.result_label.bind(texture_size=self.result_label.setter('size'))

    def on_window_resize(self, window, width, height):
        self.update_label_width()

    def go_back(self, instance):
        self.manager.current = 'input_screen'


class InfoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        scroll_view = ScrollView(size_hint=(1, 1))

        text_layout = BoxLayout(size_hint_y=None)
        text_layout.bind(minimum_height=text_layout.setter('height'))

        info_label = Label(
            text="\n\n본 어플리케이션은 @uo_ucg_kr 님께서 제공하신 울트라맨 카드게임의 카드 번역 자료를 기반으로 하는 비공식 울트라맨 카드게임 정보 검색 어플리케이션입니다. 관련하여 문의사항이 생길 경우 X(구, 트위터)를 통해 문의를 남기시길 바랍니다.",
            font_name=font_name,
            size_hint=(1, None),
            halign='left',
            valign='top',
            padding=(10, 10),
            font_size=48  # 폰트 크기 설정
        )

        info_label.bind(
            width=lambda *x: info_label.setter('text_size')(info_label, (info_label.width, None))
        )
        info_label.bind(texture_size=info_label.setter('size'))
        text_layout.add_widget(info_label)
        scroll_view.add_widget(text_layout)

        layout.add_widget(scroll_view)
        back_button = Button(text='뒤로', font_name=font_name, size_hint=(1, None), height=100, font_size=48)
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'input_screen'


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(InputScreen(name='input_screen'))
        sm.add_widget(ResultScreen(name='result_screen'))
        sm.add_widget(InfoScreen(name='info_screen'))
        return sm

if __name__ == '__main__':
    MyApp().run()
