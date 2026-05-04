import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import json

# Глобальный список для хранения записей
entries = []

# Создание окна
root = tk.Tk()
root.title("Weather Diary")
root.geometry("700x500")  # Размер окна

# --- Поля для ввода данных ---

# Дата
tk.Label(root, text="Дата:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
date_entry = DateEntry(root, width=12)
date_entry.grid(row=0, column=1, padx=5, pady=5)

# Температура
tk.Label(root, text="Температура (°C):").grid(row=1, column=0, padx=5, pady=5, sticky='w')
temp_entry = tk.Entry(root)
temp_entry.grid(row=1, column=1, padx=5, pady=5)

# Описание
tk.Label(root, text="Описание:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
desc_entry = tk.Entry(root)
desc_entry.grid(row=2, column=1, padx=5, pady=5)

# Осадки
precip_var = tk.BooleanVar()
precip_check = tk.Checkbutton(root, text="Осадки", variable=precip_var)
precip_check.grid(row=3, column=1, padx=5, pady=5, sticky='w')

# --- Таблица для отображения данных ---
columns = ("date", "temp", "desc", "precip")
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col.capitalize())
tree.column("date", width=100)
tree.column("temp", width=100)
tree.column("desc", width=200)
tree.column("precip", width=70)
tree.grid(row=5, column=0, columnspan=4, padx=5, pady=10, sticky='nsew')

# Настраиваем расширение таблицы при изменении размера окна
root.grid_rowconfigure(5, weight=1)
root.grid_columnconfigure(2, weight=1)

# --- Функции ---
def refresh_table(filtered=None):
    # Очистить таблицу
    for item in tree.get_children():
        tree.delete(item)
    # Заполнять новыми данными
    data = filtered if filtered is not None else entries
    for e in data:
        tree.insert('', 'end', values=(
            e['date'],
            e['temperature'],
            e['description'],
            'Да' if e['precipitation'] else 'Нет'
        ))

def add_entry():
    date = date_entry.get()
    try:
        temperature = float(temp_entry.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректное число для температуры")
        return
    description = desc_entry.get()
    if not description:
        messagebox.showerror("Ошибка", "Заполните описание")
        return
    precip = precip_var.get()
    
    new_entry = {
        "date": date,
        "temperature": temperature,
        "description": description,
        "precipitation": precip
    }
    entries.append(new_entry)
    refresh_table()
    clear_inputs()

def clear_inputs():
    temp_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)
    precip_var.set(False)

def save_to_file():
    try:
        with open("weather_data.json", "w", encoding='utf-8') as f:
            json.dump(entries, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Успех", "Данные сохранены")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка сохранения: {e}")

def load_from_file():
    global entries
    try:
        with open("weather_data.json", "r", encoding='utf-8') as f:
            entries = json.load(f)
        refresh_table()
        messagebox.showinfo("Успех", "Данные загружены")
    except FileNotFoundError:
        messagebox.showinfo("Информация", "Файл не найден")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка загрузки: {e}")

def filter_by_date():
    selected_date = date_filter_entry.get()
    filtered = [e for e in entries if e['date'] == selected_date]
    refresh_table(filtered)

def filter_by_temp():
    try:
        temp_threshold = float(temp_filter_entry.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Введите число для фильтра по температуре")
        return
    filtered = [e for e in entries if e['temperature'] > temp_threshold]
    refresh_table(filtered)

def reset_filter():
    refresh_table()

# --- Фильтры ---
tk.Label(root, text="Фильтр по дате:").grid(row=7, column=0, padx=5, pady=5, sticky='w')
date_filter_entry = DateEntry(root)
date_filter_entry.grid(row=7, column=1, padx=5, pady=5)
tk.Button(root, text="Фильтр по дате", command=filter_by_date).grid(row=7, column=2, padx=5, pady=5)
tk.Button(root, text="Сброс фильтра", command=reset_filter).grid(row=7, column=3, padx=5, pady=5)

tk.Label(root, text="Фильтр по температуре выше:").grid(row=8, column=0, padx=5, pady=5, sticky='w')
temp_filter_entry = tk.Entry(root)
temp_filter_entry.grid(row=8, column=1, padx=5, pady=5)
tk.Button(root, text="Фильтр по температуре", command=filter_by_temp).grid(row=8, column=2, padx=5, pady=5)

# --- Кнопки ---
tk.Button(root, text="Добавить запись", command=add_entry).grid(row=4, column=1, padx=5, pady=5)
tk.Button(root, text="Сохранить", command=save_to_file).grid(row=4, column=2, padx=5, pady=5)
tk.Button(root, text="Загрузить", command=load_from_file).grid(row=4, column=3, padx=5, pady=5)
tk.Button(root, text="Показать все", command=reset_filter).grid(row=4, column=0, padx=5, pady=5)

# Загрузка данных при старте
load_from_file()

# Запуск главного цикла
root.mainloop()