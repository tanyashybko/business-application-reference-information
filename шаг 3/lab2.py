import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import pymysql

# Подключение к базе данных
connector = pymysql.connect(
    host='localhost',
    user='root',
    password='041219921337@Tan',
    database='buisness',
    cursorclass=pymysql.cursors.DictCursor
)

# Функции для работы с базой данных и создания GUI
def execute_query(query, params=None, fetch_all=False):
    with connector.cursor() as cursor:
        try:
            cursor.execute(query, params)
            if fetch_all:
                return cursor.fetchall()
            return cursor.fetchone()
        except Exception as e:
            print(f"Error executing query: {query}\nError details: {e}")
            return None

# Получение информации о колонках таблицы
def fetch_table_columns(table_name):
    query = f"SHOW COLUMNS FROM {table_name}"
    return execute_query(query, fetch_all=True)

# Получение данных из таблицы
def fetch_table_data(table_name):
    query = f"SELECT * FROM {table_name}"
    return execute_query(query, fetch_all=True)

# Добавление записи в таблицу
def insert_record(table_name, values):
    columns = ', '.join(values.keys())
    placeholders = ', '.join(['%s'] * len(values))
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    # Извлечение значений из виджетов
    record_values = [value.get() if isinstance(value, tk.Entry) else str(value.get_date()) for value in values.values()]
    execute_query(query, tuple(record_values))
    connector.commit()

# Обновление записи в таблице
def update_record(table_name, record_id, values):
    set_clause = ', '.join([f"{column}=%s" for column in values.keys()])
    query = f"UPDATE {table_name} SET {set_clause} WHERE ID=%s"
    # Создаем кортеж значений для подстановки в запрос
    record_values = tuple(value.get() if isinstance(value, tk.Entry) else value.get_date() for value in values.values()) + (record_id,)
    execute_query(query, record_values)
    connector.commit()

# Удаление записи из таблицы
def delete_record(table_name, record_id):
    query = f"DELETE FROM {table_name} WHERE ID=%s"
    execute_query(query, (record_id,))
    connector.commit()

# Отображение таблицы в графическом интерфейсе
def display_table(table_name):
    global tree_view, combo, label_info
    columns = fetch_table_columns(table_name)
    data = fetch_table_data(table_name)

    for widget in root.winfo_children():
        widget.destroy()

    # Добавляем надписи
    label_info = tk.Label(root, text="Шибко Татьяна Александровна\n3 курс 12 группа\n2023 год", font=('Helvetica', 10))
    label_info.pack()

    label = tk.Label(root, text="Выберите справочник:")
    label.pack()

    combo = ttk.Combobox(root, textvariable=selected_table_var)
    combo.pack()
    combo["values"] = get_table_names()
    combo.set(table_name)
    combo.bind("<<ComboboxSelected>>", on_table_select)

    tree_view = ttk.Treeview(root)
    tree_view["columns"] = tuple(column['Field'] for column in columns)

    for column in columns:
        tree_view.column(column['Field'], width=100)
        tree_view.heading(column['Field'], text=column['Field'])

    for record in data:
        tree_view.insert("", "end", values=tuple(record.values()))

    tree_view.pack()

    add_button = tk.Button(root, text="Добавить", command=lambda: add_record(table_name))
    add_button.pack()

    edit_button = tk.Button(root, text="Редактировать", command=lambda: edit_record(table_name))
    edit_button.pack()

    delete_button = tk.Button(root, text="Удалить", command=lambda: perform_delete_record(table_name))
    delete_button.pack()

    view_button = tk.Button(root, text="Просмотреть", command=lambda: view_record(table_name))
    view_button.pack()

    refresh_button = tk.Button(root, text="Обновить", command=lambda: refresh_table(table_name))
    refresh_button.pack()

# Обработчик события выбора таблицы в комбобоксе
def on_table_select(event):
    selected_table = selected_table_var.get()
    display_table(selected_table)

# Получение списка имен таблиц в базе данных
def get_table_names():
    query = "SHOW TABLES"
    tables = execute_query(query, fetch_all=True)
    return [table['Tables_in_buisness'] for table in tables]

# Добавление записи в таблицу (отдельное окно)
def add_record(table_name):
    add_window = tk.Toplevel(root)
    add_window.title("Добавить запись")

    values = {}
    for column in fetch_table_columns(table_name):
        label = tk.Label(add_window, text=column['Field'] + ":")
        label.grid(row=len(values), column=0, padx=5, pady=5)

        if "DATE" in column['Type']:
            date_entry = DateEntry(add_window, width=12, background='darkblue',
                                   foreground='white', borderwidth=2)
            date_entry.grid(row=len(values), column=1, padx=5, pady=5)
            values[column['Field']] = date_entry
        else:
            entry = tk.Entry(add_window)
            entry.grid(row=len(values), column=1, padx=5, pady=5)
            values[column['Field']] = entry

    button_add = tk.Button(add_window, text="Добавить", command=lambda: insert_record(table_name, values))
    button_add.grid(row=len(values) + 1, column=0, columnspan=2, padx=5, pady=5)

# Редактирование записи в таблице (отдельное окно)
def edit_record(table_name):
    selected_item = tree_view.selection()
    if not selected_item:
        messagebox.showwarning("Предупреждение", "Выберите запись для редактирования")
        return

    item_values = tree_view.item(selected_item)['values']
    if not item_values:
        messagebox.showwarning("Предупреждение", "Выберите запись для редактирования")
        return

    edit_window = tk.Toplevel(root)
    edit_window.title("Редактировать запись")

    values = {}
    for i, column in enumerate(fetch_table_columns(table_name)):
        label = tk.Label(edit_window, text=column['Field'] + ":")
        label.grid(row=i, column=0, padx=5, pady=5)

        if "DATE" in column['Type']:
            date_entry = DateEntry(edit_window, width=12, background='darkblue',
                                   foreground='white', borderwidth=2)
            date_entry.grid(row=i, column=1, padx=5, pady=5)
            date_entry.set(item_values[i])
            values[column['Field']] = date_entry
        else:
            entry = tk.Entry(edit_window)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entry.insert(0, item_values[i])
            values[column['Field']] = entry

    button_edit = tk.Button(edit_window, text="Редактировать", command=lambda: update_record(table_name, item_values[0], values))
    button_edit.grid(row=i + 1, column=0, columnspan=2, padx=5, pady=5)

# Просмотр записи в таблице (отдельное окно)
def view_record(table_name):
    selected_item = tree_view.selection()
    if not selected_item:
        messagebox.showwarning("Предупреждение", "Выберите запись для просмотра")
        return

    item_values = tree_view.item(selected_item)['values']
    if not item_values:
        messagebox.showwarning("Предупреждение", "Выберите запись для просмотра")
        return

    view_window = tk.Toplevel(root)
    view_window.title("Просмотр записи")

    for i, column in enumerate(fetch_table_columns(table_name)):
        label_name = tk.Label(view_window, text=column['Field'] + ":")
        label_name.grid(row=i, column=0, padx=5, pady=5)

        label_value = tk.Label(view_window, text=item_values[i])
        label_value.grid(row=i, column=1, padx=5, pady=5)

    button_close = tk.Button(view_window, text="Закрыть", command=view_window.destroy)
    button_close.grid(row=i + 1, column=0, columnspan=2, padx=5, pady=5)

# Удаление записи из таблицы и обновление отображения таблицы
def perform_delete_record(table_name):
    selected_item = tree_view.selection()
    if not selected_item:
        messagebox.showwarning("Предупреждение", "Выберите запись для удаления")
        return

    item_values = tree_view.item(selected_item)['values']
    if not item_values:
        messagebox.showwarning("Предупреждение", "Выберите запись для удаления")
        return

    record_id = item_values[0]

    confirmation = messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить запись?")

    if confirmation:
        delete_record(table_name, record_id)
        messagebox.showinfo("Успех", "Запись успешно удалена")
        refresh_table(table_name)

# Обновление отображения таблицы
def refresh_table(table_name):
    display_table(table_name)

# Создание главного окна
root = tk.Tk()
root.title("Справочники")
root.geometry("800x600")

# Инициализация начальных данных
selected_table_var = tk.StringVar()
display_table("Cities")

# Запуск главного цикла
root.mainloop()