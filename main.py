import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.utils import get_color_from_hex
from Blockchain.blockchain import Blockchain

# Фиксированный размер окна
Window.size = (1200, 800)

# Цвета для дизайна
PRIMARY_COLOR = get_color_from_hex("#4CAF50")  # Зелёный
SECONDARY_COLOR = get_color_from_hex("#FFC107")  # Жёлтый
BACKGROUND_COLOR = get_color_from_hex("#F5F5F5")  # Светло-серый
TEXT_COLOR = get_color_from_hex("#212121")  # Тёмно-серый

class AnimatedButton(Button):
    """Кнопка с анимацией при наведении и нажатии"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = PRIMARY_COLOR
        self.color = TEXT_COLOR
        self.font_size = 18
        self.size_hint_y = None
        self.height = 50
        self.border_radius = [25]  # Закруглённые углы

        # Анимация при наведении
        self.bind(on_enter=self.on_enter)
        self.bind(on_leave=self.on_leave)

    def on_enter(self, *args):
        """Анимация при наведении"""
        Animation(background_color=SECONDARY_COLOR, duration=0.2).start(self)

    def on_leave(self, *args):
        """Анимация при уходе курсора"""
        Animation(background_color=PRIMARY_COLOR, duration=0.2).start(self)

class BlockchainUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 15
        self.bind(size=self._update_background)

        # Устанавливаем фон
        with self.canvas.before:
            Color(*BACKGROUND_COLOR)
            self.background = Rectangle(size=self.size, pos=self.pos)

        # Инициализация блокчейна
        self.blockchain = Blockchain()

        # Элементы интерфейса
        self.label_data = Label(text="Введите данные для нового блока:", size_hint_y=None, height=30, color=TEXT_COLOR, font_size=20)
        self.add_widget(self.label_data)

        self.entry_data = TextInput(multiline=False, size_hint_y=None, height=50, background_color=(1, 1, 1, 1), foreground_color=TEXT_COLOR, font_size=18)
        self.add_widget(self.entry_data)

        self.btn_add_block = AnimatedButton(text="Добавить блок")
        self.btn_add_block.bind(on_press=self.add_block)
        self.add_widget(self.btn_add_block)

        self.btn_check_chain = AnimatedButton(text="Проверить цепочку")
        self.btn_check_chain.bind(on_press=self.check_chain)
        self.add_widget(self.btn_check_chain)

        self.label_blocks = Label(text="Список блоков:", size_hint_y=None, height=30, color=TEXT_COLOR, font_size=20)
        self.add_widget(self.label_blocks)

        # Прокручиваемый список блоков
        self.scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, 200))
        self.block_list = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.block_list.bind(minimum_height=self.block_list.setter('height'))
        self.scroll_view.add_widget(self.block_list)
        self.add_widget(self.scroll_view)

        self.label_block_info = Label(text="Информация о блоке:", size_hint_y=None, height=30, color=TEXT_COLOR, font_size=20)
        self.add_widget(self.label_block_info)

        self.text_block_info = TextInput(readonly=True, size_hint_y=None, height=150, background_color=(1, 1, 1, 1), foreground_color=TEXT_COLOR, font_size=16)
        self.add_widget(self.text_block_info)

        # Загружаем список блоков при старте
        self.update_block_list()

    def _update_background(self, *args):
        """Обновляет фон при изменении размера окна"""
        self.background.size = self.size
        self.background.pos = self.pos

    def add_block(self):
        """Добавляет новый блок в блокчейн"""
        data = self.entry_data.text
        if data:
            self.blockchain.add_block(data)
            self.entry_data.text = ""  # Очищаем поле ввода
            self.update_block_list()  # Обновляем список блоков

    def update_block_list(self):
        """Обновляет список блоков на экране"""
        self.block_list.clear_widgets()
        for block in self.blockchain.chain:
            btn = AnimatedButton(text=f"Блок #{block.index}: {block.data}")
            btn.bind(on_press=lambda btn, b=block: self.show_block_info(b))
            self.block_list.add_widget(btn)

    def show_block_info(self, block):
        """Показывает информацию о выбранном блоке"""
        unix_time = block.timestamp
        normal_time = datetime.datetime.fromtimestamp(unix_time)
        info = (
            f"Индекс блока: {block.index}\n"
            f"Хэш блока: {block.hash}\n"
            f"Хэш предыдущего блока: {block.previous_hash}\n"
            f"Данные: {block.data}\n"
            f"Время создания: {normal_time}"
        )
        self.text_block_info.text = info

    def check_chain(self, instance):
        """Проверяет валидность цепочки блоков"""
        if self.blockchain.is_chain_valid():
            self.text_block_info.text = "Цепочка валидная ✅"
        else:
            self.text_block_info.text = "Цепочка не валидная ❌"

class BlockchainApp(App):
    def build(self):
        return BlockchainUI()

# Запуск приложения
if __name__ == "__main__":
    BlockchainApp().run()