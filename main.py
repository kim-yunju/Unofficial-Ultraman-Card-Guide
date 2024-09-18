from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window  # 창 크기 가져오기 위한 모듈
from kivy.uix.anchorlayout import AnchorLayout  # AnchorLayout 가져오기
import pandas as pd
from kivy.resources import resource_add_path
import os

# 앱 실행 디렉토리를 리소스 경로로 추가
resource_add_path(os.path.dirname(__file__))

# CSV 파일 읽기
df = pd.read_csv('data2.csv')  # 'data.csv' 파일 경로를 적절히 설정하세요.

# 폰트 경로 설정
font_name = 'NanumGothic.ttf'  # 다운로드한 폰트 파일명과 경로를 적절히 설정하세요.

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

        # 입력창 추가
        self.input_label = Label(text='번호를 입력하세요:', font_name=font_name, size_hint=(1, None), height=100)
        input_layout.add_widget(self.input_label)

        self.text_input = TextInput(multiline=False, font_name=font_name, size_hint=(1, None), height=100)
        input_layout.add_widget(self.text_input)

        # 검색 버튼 추가
        self.search_button = Button(text='검색', font_name=font_name, size_hint=(1, None), height=100)
        self.search_button.bind(on_press=self.on_search_button_click)
        input_layout.add_widget(self.search_button)

        # 입력 레이아웃을 메인 레이아웃에 추가
        main_layout.add_widget(input_layout)

        # 빈 공간을 추가하여 입력창과 검색 버튼을 화면 중앙에 배치
        main_layout.add_widget(BoxLayout(size_hint_y=1))  # 하단의 빈 공간

        # 설명 버튼 레이아웃 설정 (맨 아래에 배치)
        info_button_layout = BoxLayout(size_hint=(1, None), height=100)
        self.info_button = Button(text='앱 설명', font_name=font_name, size_hint=(1, None), height=100)
        self.info_button.bind(on_press=self.on_info_button_click)
        info_button_layout.add_widget(self.info_button)

        # 설명 버튼 레이아웃을 메인 레이아웃에 추가
        main_layout.add_widget(info_button_layout)

        # 메인 레이아웃을 화면에 추가
        self.add_widget(main_layout)

    def on_search_button_click(self, instance):
        # 사용자가 입력한 텍스트를 가져옴
        user_input = self.text_input.text.upper()
        
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
        self.result_label = Label(text='', font_name=font_name, size_hint_y=None)
        self.layout.add_widget(self.result_label)
        
        # 스크롤뷰를 메인 레이아웃에 추가
        main_layout.add_widget(scroll_view)

        # 뒤로 가기 버튼 추가
        self.back_button = Button(text='뒤로', font_name=font_name, size_hint_y=None, height=100)
        self.back_button.bind(on_press=self.go_back)
        main_layout.add_widget(self.back_button)
        
        self.add_widget(main_layout)

        # 윈도우 크기 변경 이벤트 바인딩
        Window.bind(on_resize=self.on_window_resize)

    def display_result(self, code):
        # 사용자가 입력한 번호를 CSV 파일에서 검색
        if code in df['번호'].values:
            result_row = df[df['번호'] == code].iloc[0]
            
            # 카드명 정보가 없는 경우에 대한 처리
            if pd.isna(result_row['카드명']) or result_row['카드명'].strip() == '':
                result_text = '\n\n아직 해당 번호 카드에 대한 정보가 업데이트되지 않았습니다.'
            else:
                result_text = f"\n\n카드명: {result_row['카드명']}\n\n효과:\n{result_row['효과']}"
        else:
            result_text = '\n\n번호를 찾을 수 없습니다.'

        # 결과를 화면에 표시하고 줄바꿈 처리
        self.result_label.text = result_text
        self.update_label_width()  # 현재 창 크기에 맞게 라벨의 너비 업데이트

    def update_label_width(self, *args):
        # 창의 크기에 맞춰 라벨의 text_size를 업데이트
        self.result_label.text_size = (Window.width - 40, None)  # 창의 너비에 맞춰 줄바꿈 (패딩을 고려하여 40을 뺌)
        self.result_label.bind(texture_size=self.result_label.setter('size'))  # 라벨 크기를 텍스처 크기에 맞게 조정

    def on_window_resize(self, window, width, height):
        # 창 크기가 변경될 때마다 라벨의 너비를 업데이트
        self.update_label_width()

    def go_back(self, instance):
        # 입력 화면으로 돌아가기
        self.manager.current = 'input_screen'


class InfoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 메인 레이아웃 설정
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # 스크롤 가능한 영역 설정
        scroll_view = ScrollView(size_hint=(1, 1))

        # 텍스트 레이아웃 설정
        text_layout = BoxLayout(size_hint_y=None)
        text_layout.bind(minimum_height=text_layout.setter('height'))

        # 설명 라벨 추가
        info_label = Label(
            text="\n\n본 어플리케이션은 @uo_ucg_kr 님께서 제공하신 울트라맨 카드게임의 카드 번역 자료를 기반으로 하는 비공식 울트라맨 카드게임 정보 검색 어플리케이션입니다. 관련하여 문의사항이 생길 경우 X(구, 트위터)를 통해 문의를 남기시길 바랍니다.",
            font_name=font_name,
            size_hint=(1, None),
            halign='left',  # 수평 정렬
            valign='top',  # 수직 정렬
            padding=(10, 10)
        )

        # 자동 줄바꿈을 위해 text_size 설정
        info_label.bind(
            width=lambda *x: info_label.setter('text_size')(info_label, (info_label.width, None))
        )
        info_label.bind(texture_size=info_label.setter('size'))

        # 라벨을 텍스트 레이아웃에 추가
        text_layout.add_widget(info_label)
        scroll_view.add_widget(text_layout)

        # 스크롤 뷰를 메인 레이아웃에 추가
        layout.add_widget(scroll_view)

        # 뒤로 가기 버튼 추가
        back_button = Button(text='뒤로', font_name=font_name, size_hint=(1, None), height=100)
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        # 메인 레이아웃을 화면에 추가
        self.add_widget(layout)

    def go_back(self, instance):
        # 입력 화면으로 돌아가기
        self.manager.current = 'input_screen'

class MyApp(App):
    def build(self):
        # ScreenManager 설정
        sm = ScreenManager()
        sm.add_widget(InputScreen(name='input_screen'))
        sm.add_widget(ResultScreen(name='result_screen'))
        sm.add_widget(InfoScreen(name='info_screen'))  # 새로운 InfoScreen 추가
        return sm

if __name__ == '__main__':
    MyApp().run()
