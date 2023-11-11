# Необхідні класи для проєкту.
# tkinter - для GUI. Частина інтерфейсу.
# matplotlib - для виведення графів. Частина інтерфейсу.
# numpy - для функції range. Частина моделі.
# sympy - бібліотека для символьних обчислень. Обчислення похідної. Частина моделі.
import io
import os
import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import math
from sympy import *
from PIL import Image

# Клас для зберігання інформації та виконання обов'язків об'єкту Граф.
class Graph:
    # Атрибути класу Граф.
    # Перше - це діапазон осі Х.
    # Друге - діапазон осі X, точки розриву.
    # Третє - діапазон осі У, звичайні значення.
    # Четверте - діапазон осі У, похідна від графу.
    x = []
    bx = []
    y = []
    dy = []

    # У класа Граф також присутні ще чотири аргументи
    # - координата початку, кінця, крок і саме рівняння у форматі str.
    def __init__(self, start, end, step, eq):
        self.start = start
        self.end = end
        self.step = step
        self.eq = eq

    # Повертає усі значення осі Х.
    def getX(self):
        return 'X'

    # Повертає усі значення осі Х.
    def getBX(self):
        return 'BX'

    # Повертає значення осі У.
    def getY(self):
        return 'Y'

    # Повертає значення похідної осі У.
    def getDY(self):
        return 'DX'

    # Вивід даних класу для тестування.
    def print(self):
        str = "start {0} to an end {1} with the step of {2} of the such {3} equation.".format(self.start,
                                                                                              self.end,
                                                                                              self.step,
                                                                                              self.eq)
        return str


# Клас для реалізації зкруглених границь у кнопки. З StackOverFlow.
class RoundedButton(tk.Canvas):
    global fontx
    def __init__(self, master=None, text: str = "", radius=25, btnforeground="#000000", btnbackground="#ffffff",
                 clicked=None, *args, **kwargs):
        super(RoundedButton, self).__init__(master, *args, **kwargs)
        self.config(bg=self.master["bg"])
        self.btnbackground = btnbackground
        self.clicked = clicked

        self.radius = radius

        self.rect = self.round_rectangle(0, 0, 0, 0, tags="button", radius=radius, fill=btnbackground)
        self.text = self.create_text(0, 0, text=text, tags="button", fill=btnforeground, font=(fontx, 15),
                                     justify="center")

        self.tag_bind("button", "<ButtonPress>", self.border)
        self.tag_bind("button", "<ButtonRelease>", self.border)
        self.bind("<Configure>", self.resize)

        text_rect = self.bbox(self.text)
        if int(self["width"]) < text_rect[2] - text_rect[0]:
            self["width"] = (text_rect[2] - text_rect[0]) + 10

        if int(self["height"]) < text_rect[3] - text_rect[1]:
            self["height"] = (text_rect[3] - text_rect[1]) + 10

    def round_rectangle(self, x1, y1, x2, y2, radius=25, update=False,
                        **kwargs):
        points = [x1 + radius, y1,
                  x1 + radius, y1,
                  x2 - radius, y1,
                  x2 - radius, y1,
                  x2, y1,
                  x2, y1 + radius,
                  x2, y1 + radius,
                  x2, y2 - radius,
                  x2, y2 - radius,
                  x2, y2,
                  x2 - radius, y2,
                  x2 - radius, y2,
                  x1 + radius, y2,
                  x1 + radius, y2,
                  x1, y2,
                  x1, y2 - radius,
                  x1, y2 - radius,
                  x1, y1 + radius,
                  x1, y1 + radius,
                  x1, y1]

        if not update:
            return self.create_polygon(points, **kwargs, smooth=True)

        else:
            self.coords(self.rect, points)

    def resize(self, event):
        text_bbox = self.bbox(self.text)

        if self.radius > event.width or self.radius > event.height:
            radius = min((event.width, event.height))

        else:
            radius = self.radius

        width, height = event.width, event.height

        if event.width < text_bbox[2] - text_bbox[0]:
            width = text_bbox[2] - text_bbox[0] + 30

        if event.height < text_bbox[3] - text_bbox[1]:
            height = text_bbox[3] - text_bbox[1] + 30

        self.round_rectangle(0, 0, width, height, radius, update=True)

        bbox = self.bbox(self.rect)

        x = ((bbox[2] - bbox[0]) / 2) - ((text_bbox[2] - text_bbox[0]) / 2)
        y = ((bbox[3] - bbox[1]) / 2) - ((text_bbox[3] - text_bbox[1]) / 2)

        self.moveto(self.text, x, y)

    def border(self, event):
        if event.type == "4":
            self.itemconfig(self.rect, fill="#d2d6d3")
            if self.clicked is not None:
                self.clicked()

        else:
            self.itemconfig(self.rect, fill=self.btnbackground)


# Тимчасова порожня функція.
def func():
    print("Button pressed")


# Далі слідкують функції для команд, функціонал яких змінюється попарно у циклі.
def merge_separate1(menu):
    # entryconfigure - функція для зміни параметрів полей у меню, де перший аргумент - номер поля, починаючи з 1.
    menu.entryconfigure(3, label="Separate", command=lambda: merge_separate2(file_menu))


def merge_separate2(menu):
    menu.entryconfigure(3, label="Merge", command=lambda: merge_separate1(file_menu))


def derivative_on_off1(menu):
    menu.entryconfigure(4, label="Derivative OFF", command=lambda: derivative_on_off2(file_menu))


def derivative_on_off2(menu):
    menu.entryconfigure(4, label="Derivative ON", command=lambda: derivative_on_off1(file_menu))


def intersection_on_off1(menu):
    menu.entryconfigure(5, label="Intersection OFF", command=lambda: intersection_on_off2(file_menu))


def intersection_on_off2(menu):
    menu.entryconfigure(5, label="Intersection ON", command=lambda: intersection_on_off1(file_menu))

#Функція для збереження графіку у PDF форматі
def export_to_pdf(path, filename):
    full_path = path + "/" + filename + ".pdf"
    pdf_pages = PdfPages(full_path)

    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    pdf_pages.savefig(fig)
    pdf_pages.close()

#Функція для збереження графіку у PNG форматі
def export_to_png(path, filename):
    full_path = path + "/" + filename + ".png"
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    buf = io.BytesIO()
    canvas.print_png(buf)
    buf.seek(0)

    image = Image.open(buf)
    image.save(full_path, format="PNG")


#Функція, що відповідає за відкриття діалогу з експорту графіку
def export_dialog():
    format_choice = tk.StringVar(value="pdf")  # По замовчуванню формат - PDF

    def browse_directory():
        directory = filedialog.askdirectory()
        if directory:
            selected_path.set(directory)

    def export_selected_format():
        selected_format = format_choice.get()
        save_path = selected_path.get()
        filename = file_name_entry.get()

        # Обробка помилок: пустий рядок вводу шляху
        if not save_path:
            tkinter.messagebox.showerror("Помилка", "Шлях не може бути пустим.")
            return

        # Обробка помилик: пустий рядок вводу імені
        if not filename:
            tkinter.messagebox.showerror("Помилка", "Назва файлу не може бути пустою.")
            return

        # Обробка помилик: недійсний щлях
        if not os.path.exists(save_path):
            tkinter.messagebox.showerror("Помилка", "Вказаний шлях є недійсним.")
            return

        if selected_format == "pdf":
            export_to_pdf(save_path, filename)
        elif selected_format == "png":
            export_to_png(save_path, filename)

        dialog.destroy()

    dialog = tk.Toplevel(root)
    dialog.title("Експорт")

    program_path = os.path.dirname(os.path.abspath(__file__))

    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()

    window_width = 543
    window_height = 320
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    dialog.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")  # Установить размеры и положение

    icon_path = "logo.ico"
    if os.path.exists(icon_path):
        dialog.iconbitmap(icon_path)

    dialog.grab_set()  # Робить вікно діалогу модальним

    # Для закриття через Х
    def dialog_closed():
        dialog.destroy()

    dialog.protocol("WM_DELETE_WINDOW", dialog_closed)

    format_label = tk.Label(dialog, text="Select Format:")
    format_label.pack()

    format_frame = tk.Frame(dialog)
    format_frame.pack()

    # Радіокнопки з форматами
    pdf_radio = tk.Radiobutton(format_frame, text="PDF", variable=format_choice, value="pdf")
    pdf_radio.pack(side="left", padx=10)  # Выровнять радиокнопку влево
    png_radio = tk.Radiobutton(format_frame, text="PNG", variable=format_choice, value="png")
    png_radio.pack(side="left", padx=10)  # Выровнять радиокнопку влево

    path_label = tk.Label(dialog, text="Обрати шлях:")
    path_label.pack()

    selected_path = tk.StringVar(value=program_path)  # Шлях за замовчуванням - шлях до програми
    path_entry = tk.Entry(dialog, textvariable=selected_path)
    path_entry.pack()

    browse_button = tk.Button(dialog, text="Пошук", command=browse_directory)
    browse_button.pack()

    file_name_label = tk.Label(dialog, text="Ввести назву файлу:")
    file_name_label.pack()

    file_name_entry = tk.Entry(dialog)
    file_name_entry.insert(0, "graph")  # Значення за замовчуванням - graph
    file_name_entry.pack()

    export_button = tk.Button(dialog, text="Експортувати", command=export_selected_format)
    export_button.pack()


# Функція для показування елементів у списку.
def show(iterable):
    for el in iterable:
        el.pack(fill="x")


# Функція для закриття елементів у списку.
def close(iterable):
    for el in iterable:
        el.pack_forget()


# Функція для очищення полів Entry.
def clear(entries):
    for entry in entries:
        entry.delete(0, tk.END);


# Функція для опції меню Input.
def input_show():
    global interface
    close(interface)
    interface = []
    interface = [label_start, entry_start, label_end, entry_end, label_step, entry_step, label_eq, entry_eq]
    entries = [entry_start, entry_end, entry_step, entry_eq]
    clear(entries)
    border_color.pack(side="left", expand=tk.NO, fill=tk.Y, padx=5)
    left_frame.pack(fill=tk.Y, expand=1)
    show(interface)
    input_btn.pack(expand=True, fill="x")
    interface.append(input_btn)
    interface.append(border_color)
    interface.append(left_frame)
    entry_start.focus()


# Функція для кнопки меню Input.
def input_execute():
    global graphs, interface
    graphs = []
    comments = []
    start = entry_start.get()
    start, comments = input_check_range(start, comments, "first")
    end = entry_end.get()
    end, comments = input_check_range(end, comments, "second")
    if(start >= end):
        comments.clear()
        comments.append("first")
        comments.append("second")
    step = entry_step.get()
    step, comments = input_check_step(step, comments, "third")
    eq = entry_eq.get()
    eq, comments = input_check_eq(eq, comments, "fourth")
    if comments != []:
        try:
            del interface[interface.index(comment)]
        except:
            pass
        str = input_comment(comments)
        comment.config(text=str)
        interface.append(comment)
        comment.pack(fill="x")
    else:
        graphs.append(Graph(start, end, step, eq))
        print(graphs[0].print())
        close(interface)


# Функція для перетворення числа у число з плаваючою крапкою.
def toFloat(x):
    try:
        return float(x)
    except:
        raise TypeError


# Функція для перевірки значень діапазону.
def input_check_range(x, comments, comment):
    try:
        x = toFloat(x)
        if(x > 1000000 or x < -1000000):
            raise OverflowError
    except:
        comments.append(comment)
    return x, comments


# Функція для перевірки значень діапазону.
def input_check_step(x, comments, comment):
    try:
        x = toFloat(x)
        if(x > 1000000 or x < 0.01):
            raise OverflowError
    except:
        comments.append(comment)
    return x, comments


# Функція для перевірки рівняння.
def input_check_eq(eq, comments, comment):
    try:
        x = 0
        eval(eq)
    except (SyntaxError, ValueError, NameError):
        comments.append(comment)
    return eq, comments


# Функція для конкатенації підказки користувача.
def input_comment(comments):
    comments[0] = comments[0].capitalize()
    str = ", ".join(comments)
    ist =  "is"
    if(len(comments) > 1):
        ist = "are"
    return "{0} {1} invalid.".format(str, ist)


# Ініціалізуймо головне вікно програми.
root = tk.Tk()
# Встановлюємо назву вікна.
root.title("DeriGraph")
# Встановлюємо іконку вікна.
root.iconbitmap("logo.ico")
# Задаємо колір заднього плану.
root.config(bg="#1E7D55")

# Обчилюємо розмір вікна. Він завжди буде дорівнювати розширенню екрана.
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry("{}x{}+0+0".format(str(screen_width), str(screen_height)))

# Створюємо головне меню.
menu_bar = tk.Menu(root)

# Створюємо меню для команд програми.
file_menu = tk.Menu(menu_bar)
file_menu.add_command(label="Input", command=input_show)
file_menu.add_command(label="Change")
file_menu.add_command(label="Merge", command=lambda: merge_separate1(file_menu))
file_menu.add_command(label="Derivative ON", command=lambda: derivative_on_off1(file_menu))
file_menu.add_command(label="Intersection ON", command=lambda: intersection_on_off1(file_menu))
file_menu.add_command(label="Export", command=export_dialog)
file_menu.add_command(label="Share")

# Створюємо порожній мануал.
manual_menu = tk.Menu(menu_bar)

# Додаємо до головного меню меню команд і мануал.
menu_bar.add_cascade(label="Tasks", menu=file_menu)
menu_bar.add_cascade(label="Manual", menu=manual_menu)

# Прикріплюємо головне меню до вікна.
root.config(menu=menu_bar)

# Створюємо фрейм, в якому будуть розташовані sidebar і visualbar, з отступами 10 пікселів від границь вікна.
wrapper_frame = tk.Frame(root, bg="#1E7D55")
wrapper_frame.pack(padx=10, pady=10, expand=tk.YES, fill=tk.BOTH)

# Створюємо фрейм-контур для visualbar з різними отступами від границь wrapper_frame.
right_line_frame = tk.Frame(wrapper_frame, bd=1, bg="#000000")
right_line_frame.pack(side="right", expand=tk.YES, fill=tk.BOTH, pady=20, padx=5)

# Створюємо фрейм-фон для visualbar.
right_frame = tk.Frame(right_line_frame, bd=30, bg="#3FF3A7")
right_frame.pack(expand=tk.YES, fill=tk.BOTH, pady=5, padx=5)

# Створюємо фігуру, в якій розташовано усі графи.
fig = plt.figure()

# Тимчасова ініціалізація графами. Задаємо рівняння і знаходимо похідну.
equation = "i ** 2"
i = np.arange(0, math.pi*2, 0.05)
# Функція eval() реалізує наше текстове рівняння зверху.
y = eval(equation)
derivative = diff(equation)
# Обов'язково результат дифференцювання конвертувати обратно у рядок!
derivative = str(derivative)
dy = eval(derivative)

# plot і scatter несумісні !!!
# plot1 = fig.add_subplot(121)
# plot1.plot(i, y, color="g", label=equation)
# plot1.legend()
# plot2 = fig.add_subplot(122)
# plot2.plot(i, dy, color="b", label=derivative)
# plot2.legend()

# Створюємо плот у фігурі. (111) позначають (1 вертикаль, 1 горизонталь, номер плоту).
plot1 = fig.add_subplot(111)
# Відображаємо наши координати на плоті. scatter краще оброблює точки розриву, ніж plot.
plot1.scatter(i, y, c="#FFB526", s=5, label=equation)
plot1.scatter(i, dy, color="b", s=5, label=derivative)
plot1.legend()

# Задаємо холст, на якому буде намальовано граф. Особоливість у тому, що можна вставити граф у будь-який фрейм.
canvas = FigureCanvasTkAgg(fig, master=right_frame)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
toolbar = NavigationToolbar2Tk(canvas, right_frame)
toolbar.update()
canvas.get_tk_widget().pack()

# Встановлюємо шрифт проєкту.
fontx = "Small Fonts"

# Встановлюємо контур-фрейм лівого фрейму.
border_color = tk.Frame(wrapper_frame, bd=5, bg="#000000")

# Створюємо лівий допоміжний фрейм.
left_frame = tk.Frame(border_color, bg="#3FF3A7")

# Створюємо текст і поле вводу початку відліку.
label_start = tk.Label(left_frame, text="X starts at:", font=(fontx, 20), bg="#3FF3A7",
                       highlightbackground = "#206F23", fg = "#206F23")
entry_start = tk.Entry(left_frame, bg="#E9FD00", font=(fontx, 30, "bold"), width=5)

# Створюємо текст і поле вводу кінця відліку.
label_end = tk.Label(left_frame, text = "X ends at:", font=(fontx, 20), bg="#3FF3A7",
                       highlightbackground = "#206F23", fg = "#206F23")
entry_end = tk.Entry(left_frame, bg="#E9FD00", font=(fontx, 30, "bold"), width=5)

# Створюємо текст і поле вводу кроку відліку.
label_step = tk.Label(left_frame, text = "The step:", font=(fontx, 20), bg="#3FF3A7",
                       highlightbackground = "#206F23", fg = "#206F23")
entry_step = tk.Entry(left_frame, bg="#E9FD00", font=(fontx, 30, "bold"), width=5)

# Створюємо текст і поле вводу рівняння.
label_eq = tk.Label(left_frame, text = "The equation:", font=(fontx, 20), bg="#3FF3A7",
                       highlightbackground = "#206F23", fg = "#206F23")
entry_eq = tk.Entry(left_frame, bg="#E9FD00", font=(fontx, 30, "bold"), width=5)

# Створюємо надпис для підказок користувачу.
comment = tk.Label(left_frame, text = "", font=(fontx, 20), bg="#3FF3A7", wraplength=180,
                       highlightbackground = "#206F23", fg = "#206F23")

# Глобальна змінна для збереження об'єктів інтерфейсу.
interface = []
# Глобальна змінна для збереження графів.
graphs = []

# Створюємо кнопку з зкругленими границями.
input_btn = RoundedButton(left_frame, text="Input", highlightthickness=0,  width=100, height=60, radius=100,
                    btnbackground="#FFB526", btnforeground="#000000", clicked=input_execute)

# Основний цикл вікна tkinter.
root.mainloop()
