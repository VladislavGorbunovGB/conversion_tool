import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

def plot_substrate_removal(data_dict, save_path='output.png', title='Substrate Removal Over Time', x_label='Time (hours)', y_label='Substrate Removal (%)', x_label_size=12, y_label_size=12, tick_label_size=10, noise_level=0.0):
    """
    Функция для визуализации удаления субстрата с течением времени.
    
    :param data_dict: Словарь с данными для визуализации
    :param save_path: Путь для сохранения графика
    :param title: Заголовок графика
    :param x_label: Подпись оси X
    :param y_label: Подпись оси Y
    :param x_label_size: Размер подписи оси X
    :param y_label_size: Размер подписи оси Y
    :param tick_label_size: Размер подписей тиков
    :param noise_level: Уровень случайного шума для добавления к данным
    """
    plt.figure(figsize=(10, 6))
    
    for sample, data in data_dict.items():
        time = np.array(data['time'])  # Используем значения X из конфигурации
        removal = np.array(data['removal']).astype(float)  # Используем значения Y из конфигурации и преобразуем в float
        error = data.get('error', 0)  # Устанавливаем значение ошибок по умолчанию
        
        # Добавление случайного шума
        if noise_level > 0:
            noise = np.random.normal(0, noise_level, size=removal.shape)
            removal += noise
        
        # Отображение данных с ошибками
        plt.errorbar(time, removal, yerr=error, label=data['line_label'] if data['line_label'] else sample, fmt='o', capsize=5, color=data['color'])
        
        # Сглаживание кривой
        f = interp1d(time, removal, kind='cubic')
        x_smooth = np.linspace(time.min(), time.max(), 300)
        plt.plot(x_smooth, f(x_smooth), linestyle=data['line_type'], color=data['color'])
    
    plt.title(title)
    plt.xlabel(x_label, fontsize=x_label_size)
    plt.ylabel(y_label, fontsize=y_label_size)
    plt.xticks(fontsize=tick_label_size)
    plt.yticks(fontsize=tick_label_size)
    plt.xlim(left=0)  # Устанавливаем нижнюю границу по оси X на 0
    plt.ylim(bottom=0)  # Устанавливаем нижнюю границу по оси Y на 0
    plt.legend()
    
    # Удаление сетки
    plt.grid(False)
    
    # Удаление верхней и правой границы
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    
    plt.savefig(save_path)
    plt.show()