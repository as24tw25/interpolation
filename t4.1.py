import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QLabel, QPushButton, QVBoxLayout, QLineEdit, QWidget

from PyQt5.QtWidgets import QFileDialog

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Интерполяция данных') # Устанавливаем текст для заголовка окна
        self.setGeometry(100, 100, 800, 600) # Указываем координаты размещения окна
        # Создаем центральный виджет и устанавливаем его
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Основной макет окна
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Надпись для тесктового поля ввода имени файла
        file_label = QLabel('Введите имя файла (например, data.csv):')
        layout.addWidget(file_label)

        self.button = QPushButton('Выбрать файл', self)
        #self.button.setText('Выбрать файл')
        self.button.move(10, 100)
        self.button.clicked.connect(self.selectFile)

        # Кнопка для загрузки данных и интерполяции
        load_button = QPushButton('Загрузить данные и интерполировать', self)
        load_button.clicked.connect(self.load_and_interpolate_data)
        layout.addWidget(load_button)

        # Лейбл для ввода точки
        point_label = QLabel('Введите точку для интерполяции:')
        layout.addWidget(point_label)

        # Поле для ввода значения 'Концетрация' для которой нужно определить значение 'Плотность'
        self.point_input = QLineEdit(self)
        layout.addWidget(self.point_input)

        # Кнопка для вычисления значения в заданной точке
        interpolate_button = QPushButton('Выполнить интерполяцию', self)
        interpolate_button.clicked.connect(self.interpolate_point) # устанавливаем обработчик на нажатие на кнопку
        layout.addWidget(interpolate_button)

        # Лейбл для отображения результата
        self.result_label = QLabel('Результат')
        layout.addWidget(self.result_label)
        self.file_name = '' # поле для хранения имени файла с исходными данными

    def selectFile(self):
        self.file_name, _ = QFileDialog.getOpenFileName(None, 'Выбор файла', '.', 'Текстовые файлы (*.txt)')

    def load_and_interpolate_data(self):
        file_name = self.file_name 
        if not file_name:
            self.result_label.setText('Выберите файл для загрузки')
            return
        try:
            data = np.loadtxt(file_name, delimiter=',') # Загрузка данных из файла
            if data.shape[1] != 2:
                raise ValueError("Файл должен содержать два столбца данных.")
            
            x = data[:, 0]
            y = data[:, 1]

            # Проводим интерполяцию
            self.interpolator = interp1d(x, y, kind='linear')

            # Отрисовываем график
            plt.figure(figsize=(8, 6))
            plt.plot(x, y, 'o', label='Исходные данные')
            x_new = np.linspace(min(x), max(x), 300)
            y_new = self.interpolator(x_new)
            plt.plot(x_new, y_new, '-', label='Интерполяционная кривая')
            plt.xlabel('Концентрация, ммоль/л')
            plt.ylabel('Плотность, ед')
            plt.title('График интерполированных данных')
            plt.legend()
            plt.show()

        except Exception as e:
            self.result_label.setText(f"Ошибка: {e}")

    def interpolate_point(self):
        try:
            point = float(self.point_input.text())
            if hasattr(self, 'interpolator'):
                result = self.interpolator(point)
                self.result_label.setText(f"Значение в точке {point}: {result}")
            else:
                raise ValueError("Сначала загрузите и интерполируйте данные.")
        except Exception as e:
            self.result_label.setText(f"Ошибка: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())



