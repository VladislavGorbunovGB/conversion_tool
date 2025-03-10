import json
from src.visualization import plot_substrate_removal

# Загрузка конфигурации
with open('config.json', 'r') as config_file:
    config = json.load(config_file)


# Пример структуры данных для визуализации
data_dict = {}
for sample in config['samples']:
    data_dict[sample['name']] = {
        'time': sample['time'],  # Используем значения X из конфигурации
        'removal': sample['removal'],  # Используем значения Y из конфигурации
        'color': sample['color'],  # Цвет для точек и линий
        'line_type': sample['line_type'],  # Тип линии для сглаживания
    }

# Визуализация данных
plot_substrate_removal(data_dict, 
                        save_path='output.png', 
                        title=config['title'], 
                        noise_level=config['noise_level'],
                        error=config['error'])
