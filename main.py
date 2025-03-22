from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex
from tkinter import Tk, filedialog
from auxiliary.blockchain_logic import BlockchainLogic
from kivy.graphics import RoundedRectangle

# Фиксированный размер окна
Window.size = (1200, 800)

# Цвета для дизайна
PRIMARY_COLOR = get_color_from_hex("#4CAF50")  # Зелёный
SECONDARY_COLOR = get_color_from_hex("#FFC107")  # Жёлтый
BACKGROUND_COLOR = get_color_from_hex("#F5F5F5")  # Светло-серый
TEXT_COLOR = get_color_from_hex("#212121")  # Тёмно-серый

class AnimatedButton(Button):
    """Прямоугольные кнопки с закруглёнными краями"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)  # Прозрачный фон
        self.color = TEXT_COLOR
        self.font_size = 18
        self.size_hint_y = None
        self.height = 50
        self.border_radius = 20  # Радиус закругления углов
        self.bind(pos=self.update_canvas, size=self.update_canvas)

        # Рисуем прямоугольник с закруглёнными углами
        with self.canvas.before:
            Color(*PRIMARY_COLOR)
            self.rounded_rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[self.border_radius])

    def update_canvas(self, *args):
        """Обновляет позицию и размер прямоугольника при изменении размера или позиции кнопки"""
        self.rounded_rect.pos = self.pos
        self.rounded_rect.size = self.size

    def on_press(self):
        """Изменяет цвет кнопки при нажатии"""
        with self.canvas.before:
            Color(*SECONDARY_COLOR)
            self.rounded_rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[self.border_radius])

    def on_release(self):
        """Возвращает цвет кнопки после отпускания"""
        with self.canvas.before:
            Color(*PRIMARY_COLOR)
            self.rounded_rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[self.border_radius])

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

        # Инициализация логики блокчейна
        self.blockchain_logic = BlockchainLogic()

        # Элементы интерфейса
        self.label_data = Label(text="Введите данные для нового блока:", size_hint_y=None, height=30, color=TEXT_COLOR, font_size=20)
        self.add_widget(self.label_data)

        self.entry_data = TextInput(multiline=False, size_hint_y=None, height=50, background_color=(1, 1, 1, 1), foreground_color=TEXT_COLOR, font_size=18)
        self.add_widget(self.entry_data)

        self.btn_choose_file = AnimatedButton(text="Выбрать файл")
        self.btn_choose_file.bind(on_press=self.choose_file)  # Используем Tkinter для выбора файла
        self.add_widget(self.btn_choose_file)

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

        self.btn_download_file = AnimatedButton(text="Скачать файл", size_hint_y=None, height=50)
        self.btn_download_file.bind(on_press=self.download_file)
        self.btn_download_file.disabled = True
        self.add_widget(self.btn_download_file)

        # Загружаем список блоков при старте
        self.update_block_list()

    def _update_background(self, *args):
        """Обновляет фон при изменении размера окна"""
        self.background.size = self.size
        self.background.pos = self.pos

    def choose_file(self, instance):
        """Открывает проводник Windows для выбора файла через Tkinter"""
        root = Tk()
        root.withdraw()  # Скрываем основное окно tkinter
        file_path = filedialog.askopenfilename()  # Открываем диалоговое окно выбора файла
        if file_path:
            self.selected_file_path = file_path

    def add_block(self, instance):
        """Добавляет новый блок в блокчейн"""
        data = self.entry_data.text
        file_path = getattr(self, 'selected_file_path', None)
        self.blockchain_logic.add_block(data, file_path)
        self.entry_data.text = ""  # Очищаем поле ввода
        if hasattr(self, 'selected_file_path'):
            del self.selected_file_path
        self.update_block_list()  # Обновляем список блоков

    def update_block_list(self):
        """Обновляет список блоков на экране"""
        self.block_list.clear_widgets()
        for block in self.blockchain_logic.get_chain():
            btn = AnimatedButton(text=f"Блок #{block.index}: {block.data}")
            btn.bind(on_press=lambda btn, b=block: self.show_block_info(b))
            self.block_list.add_widget(btn)

    def show_block_info(self, block):
        """Показывает информацию о выбранном блоке"""
        info = self.blockchain_logic.get_block_info(block)
        self.text_block_info.text = info
        if block.file_data:
            self.btn_download_file.disabled = False
            self.current_block = block
        else:
            self.btn_download_file.disabled = True

    def download_file(self, instance):
        """Скачивает файл из блока с выбором пути для сохранения через Tkinter"""
        if hasattr(self, 'current_block'):
            root = Tk()
            root.withdraw()  # Скрываем основное окно tkinter
            save_path = filedialog.asksaveasfilename(defaultextension=".*", filetypes=[("All Files", "*.*")])  # Открываем диалоговое окно для выбора пути сохранения
            if save_path:
                if self.blockchain_logic.download_file(self.current_block, save_path):
                    self.text_block_info.text += "\nФайл успешно скачан!"

    def check_chain(self, instance):
        """Проверяет валидность цепочки блоков"""
        if self.blockchain_logic.is_chain_valid():
            self.text_block_info.text = "Цепочка валидная"
        else:
            self.text_block_info.text = "Цепочка не валидная"

class BlockchainApp(App):
    def build(self):
        return BlockchainUI()

# Запуск приложения
if __name__ == "__main__":
    BlockchainApp().run()