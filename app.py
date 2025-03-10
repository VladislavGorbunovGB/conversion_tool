import json
import streamlit as st
import numpy as np
from src.visualization import plot_substrate_removal
import base64

# Загрузка конфигурации
def load_config():
    with open('config.json', 'r') as config_file:
        return json.load(config_file)

def save_config(config):
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)

config = load_config()

# Заголовок приложения
st.title(config['title'])

# Создание вкладок для настройки
tab1, tab2, tab3 = st.sidebar.tabs(["Добавить новый образец", "Настройка образцов", "Настройка графика"])

# Вкладка для добавления нового образца
with tab1:
    st.subheader("Добавить новый образец")
    new_sample_name = st.text_input("Название образца", "Sample")
    new_sample_color = st.color_picker("Цвет образца", "#000000")
    new_sample_line_type = st.selectbox("Тип линии", ["solid", "dashed", "dotted"])
    new_sample_time = st.text_input("Время (например, [0, 1, 2, 3, 4])", "[0, 1, 2, 3, 4]")
    new_sample_removal = st.text_input("Удаление (например, [0, 0, 0, 0, 0])", "[0, 0, 0, 0, 0]")
    new_sample_show_line = st.checkbox("Показать линию", value=True)
    new_sample_line_label = st.text_input("Название линии", "")

    # Кнопка для добавления нового образца
    if st.button("Добавить образец"):
        try:
            # Преобразуем строки в списки
            time_values = json.loads(new_sample_time)
            removal_values = json.loads(new_sample_removal)

            # Проверяем, что значения являются списками чисел
            if not all(isinstance(i, (int, float)) for i in time_values):
                raise ValueError("Время должно содержать только числа.")
            if not all(isinstance(i, (int, float)) for i in removal_values):
                raise ValueError("Удаление должно содержать только числа.")

            new_sample = {
                "name": new_sample_name,
                "color": new_sample_color,
                "line_type": new_sample_line_type,
                "time": time_values,  # Сохраняем как список
                "removal": removal_values,  # Сохраняем как список
                "show_line": new_sample_show_line,
                "line_label": new_sample_line_label
            }
            config['samples'].append(new_sample)
            save_config(config)
            st.success("Образец добавлен!")
        except json.JSONDecodeError:
            st.error("Ошибка: убедитесь, что время и удаление указаны в правильном формате (например, [0, 1, 2, 3, 4]).")
        except ValueError as e:
            st.error(f"Ошибка: {e}. Убедитесь, что значения времени и удаления являются корректными списками чисел.")

# Настройка образцов
with tab2:
    st.subheader("Существующие образцы")
    for i, sample in enumerate(config['samples']):
        with st.expander(sample['name'], expanded=True):  # Создаем сворачиваемый блок для каждого образца
            sample['time'] = st.text_input(f"Время для {sample['name']}", value=json.dumps(sample['time']))
            sample['removal'] = st.text_input(f"Удаление для {sample['name']}", value=json.dumps(sample['removal']))
            sample['color'] = st.color_picker(f"Цвет для {sample['name']}", value=sample['color'])
            sample['line_type'] = st.selectbox(f"Тип линии для {sample['name']}", ["solid", "dashed", "dotted"], index=["solid", "dashed", "dotted"].index(sample['line_type']))
            sample['show_line'] = st.checkbox(f"Показать линию для {sample['name']}", value=sample['show_line'])
            sample['line_label'] = st.text_input(f"Название линии для {sample['name']}", value=sample.get('line_label', ''))  # Название линии

            # Кнопка для удаления образца
            if st.button(f"Удалить {sample['name']}"):
                config['samples'].pop(i)
                save_config(config)
                st.success(f"{sample['name']} удален!")
                break  # Прерываем цикл, чтобы избежать ошибок индексации

# Настройка графика
with tab3:
    st.subheader("Настройка графика")
    x_axis_label = st.text_input("Подпись оси X", "Time (hours)")
    y_axis_label = st.text_input("Подпись оси Y", "Substrate Removal (%)")
    plot_title = st.text_input("Название графика", config['title'])

    # Ползунки для изменения размера подписей осей и тиков
    x_label_size = st.slider("Размер подписей оси X", 8, 30, 12)
    y_label_size = st.slider("Размер подписей оси Y", 8, 30, 12)
    tick_label_size = st.slider("Размер подписей тиков", 8, 30, 10)

    # Ползунок для настройки величины ошибок
    error_bar_value = st.slider("Величина ошибок (error bars)", 0.0, 10.0, 0.0)

    # Кнопка для сохранения конфигурации
    if st.button("Сохранить конфигурацию"):
        save_config(config)
        st.success("Конфигурация сохранена!")

# Ввод данных для визуализации
data_dict = {}
for sample in config['samples']:
    time_values = sample['time'] if isinstance(sample['time'], list) else json.loads(sample['time'])
    removal_values = sample['removal'] if isinstance(sample['removal'], list) else json.loads(sample['removal'])
    
    if sample.get('show_line', True):  # Проверяем, нужно ли показывать линию
        data_dict[sample['name']] = {
            'time': time_values,
            'removal': removal_values,
            'color': sample['color'],
            'line_type': sample['line_type'],
            'error': None,  # Здесь можно добавить реальные данные об ошибках, если они есть
            'line_label': sample['line_label']  # Название линии
        }

# Визуализация данных с учетом ошибок
plot_substrate_removal(data_dict, 
                        save_path='output.png', 
                        title=plot_title, 
                        x_label=x_axis_label, 
                        y_label=y_axis_label, 
                        x_label_size=x_label_size,
                        y_label_size=y_label_size,
                        tick_label_size=tick_label_size,
                        noise_level=0.0)  # Убираем шум, так как он больше не нужен

# Отображение графика в приложении
st.image('output.png', caption='График удаления субстрата')

# Функция для скачивания изображения
def get_image_download_link(image_file):
    with open(image_file, "rb") as f:
        img_data = f.read()
    b64 = base64.b64encode(img_data).decode()  # Кодируем в base64
    return f'<a href="data:file/png;base64,{b64}" download="{image_file}">Скачать изображение</a>'

# Кнопка для скачивания изображения
download_link = get_image_download_link('output.png')
st.markdown(download_link, unsafe_allow_html=True)
