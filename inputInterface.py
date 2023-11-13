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
import matplotlib as mpl
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import math
from sympy import *
from PIL import Image
from pathlib import Path
import matplotlib.pylab as pylab

# Встановлюємо шрифт проєкту.
mpl.rcParams['font.size'] = 20
params = {'legend.fontsize': 15,
         'axes.labelsize': 10,
         'axes.titlesize': 30,
          'xtick.labelsize': 10,
          'ytick.labelsize': 10}
pylab.rcParams.update(params)
fontx = "Small Fonts"
fpath = Path("small_font.ttf")

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
    deri = ""

    # У класа Граф також присутні ще чотири аргументи
    # - координата початку, кінця, крок і саме рівняння у форматі str.
    def __init__(self, start, end, step, eq):
        self.start = start
        self.end = end
        self.step = step
        self.eq = eq
        self.getDeri()
        self.getX()
        self.getBX()
        self.getY()
        self.getDY()

    # Повернення початку координат.
    def getStart(self):
        return self.start

    # Повернення кінця координат.
    def getEnd(self):
        return self.end

    # Повернення кроку обчислень.
    def getStep(self):
        return self.step

    # Повернення рівняння.
    def getEq(self):
        return self.eq

    # Повертає список допустимих значень осі Х.
    def getXlist(self):
        return self.x

    # Повертає список значень осі У, коли рівняння звичайне.
    def getYlist(self):
        return self.y

    # Повертає список точок розриву.
    def getBXlist(self):
        return self.bx

    # Повертає список значень осі У, коли рівняння - похідна.
    def getDYlist(self):
        return self.dy

    # Повертає похідну.
    def getDerifield(self):
        return self.deri

    # Повертає усі значення осі Х.
    def getX(self):
        self.x = []
        x_list = np.arange(self.start, self.end, self.step)
        for x in x_list:
            try:
                y = eval(self.eq)
                self.x.append(x)
            except:
                pass
        return self.x

    # Повертає усі значення осі Х, які є точками розриву.
    def getBX(self):
        self.bx = []
        bx_list = np.arange(self.start, self.end, self.step)
        for x in bx_list:
            try:
                y = eval(self.eq)
            except:
                self.bx.append(x)
        return self.bx

    # Повертає значення осі У.
    def getY(self):
        self.y = []
        for x in self.x:
            self.y.append(eval(self.eq))
        return self.y

    # Повертає значення похідної осі У.
    def getDY(self):
        self.dy = []
        for x in self.x:
            self.dy.append(eval(self.deri))
        return self.dy

    # Повертає рівняння похідної.
    def getDeri(self):
        deriDiff = diff(self.eq)
        deriStr = str(deriDiff)
        self.deri = deriStr
        return self.deri

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


# Далі слідкують функції для команд, функціонал яких змінюється попарно у циклі.
def merge_separate1(menu, ax1, ax2):
    global graphs
    ax1.remove()
    ax2.remove()
    graph = graphs[0]
    ax1 = fig.add_subplot(1, 1, 1)
    try:
        file_menu.index("Derivative ON")
        ax1.set_title(label="Function and derivative", color="black", loc="left")
        ax1.scatter(graph.getXlist(), graph.getYlist(), s=5, color="#FFB526", label=graph.getEq())
        ax1.scatter(graph.getXlist(), graph.getDYlist(), s=5, color="b", label=graph.getDerifield())
    except:
        ax1.set_title(label="Function", color="black", loc="left")
        ax1.scatter(graph.getXlist(), graph.y, s=5, color="#FFB526", label=graph.getEq())
    ax1.legend()
    canvas.draw()
    # entryconfigure() - функція для зміни параметрів полей у меню, де перший аргумент - номер поля, починаючи з 1.
    menu.entryconfigure(3, label="Separate", command=lambda: merge_separate2(file_menu, ax1, ax2))


def merge_separate2(menu, ax1, ax2):
    menu.entryconfigure(3, label="Merge", command=lambda: merge_separate1(file_menu, ax1, ax2))



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
            tkinter.messagebox.showerror("Error", "The path cannot be empty.")
            return

        # Обробка помилик: пустий рядок вводу імені
        if not filename:
            tkinter.messagebox.showerror("Error", "Name of the file cannot be empty.")
            return

        # Обробка помилик: недійсний щлях
        if not os.path.exists(save_path):
            tkinter.messagebox.showerror("Error", "Such path doesn\'t exist.")
            return

        if selected_format == "pdf":
            export_to_pdf(save_path, filename)
        elif selected_format == "png":
            export_to_png(save_path, filename)

        dialog.destroy()

    dialog = tk.Toplevel(root)
    dialog.title("Export")

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

    path_label = tk.Label(dialog, text="Select path:")
    path_label.pack()

    selected_path = tk.StringVar(value=program_path)  # Шлях за замовчуванням - шлях до програми
    path_entry = tk.Entry(dialog, textvariable=selected_path)
    path_entry.pack()

    browse_button = tk.Button(dialog, text="Search", command=browse_directory)
    browse_button.pack()

    file_name_label = tk.Label(dialog, text="Input file name:")
    file_name_label.pack()

    file_name_entry = tk.Entry(dialog)
    file_name_entry.insert(0, "graph")  # Значення за замовчуванням - graph
    file_name_entry.pack()

    export_button = tk.Button(dialog, text="Export", command=export_selected_format)
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
    # Закрити попереднє вікно.
    close(interface)
    # Зробити interface порожнім.
    interface = []
    # Додати до списку інтерфейсу набор елементів поточного вікна.
    interface = [label_start, entry_start, label_end, entry_end, label_step, entry_step, label_eq, entry_eq]
    entries = [entry_start, entry_end, entry_step, entry_eq]
    # Зробити поля введення порожніми, оскільки додається повністю новий екземпляр Graph.
    clear(entries)
    # Показати фрейм-контур.
    border_color.pack(side="left", expand=tk.NO, fill=tk.Y, padx=5)
    # Показати фрейм-фон.
    left_frame.pack(fill=tk.Y, expand=1)
    # Показати елементи інтерфейсу з однотипним методом pack().
    show(interface)
    # Показати кнопку для підтвердження дії.
    input_btn.pack(expand=True, fill="x")
    # Додати до списку інтерфейсу елементи з нестандартним методом pack().
    interface.append(input_btn)
    interface.append(border_color)
    interface.append(left_frame)
    # Задати фокус на поле уведення.
    entry_start.focus()


# Функція для кнопки меню Input.
def input_execute(menu, ax1, ax2):
    global graphs, interface
    graphs = []
    comments = []
    # Перевірка початку координат. Діапазон [-1000000, 1000000].
    start = entry_start.get()
    start, comments = input_check_range(start, comments, "the first")
    # Перевірка кінця координат. Діапазон [-1000000, 1000000].
    end = entry_end.get()
    end, comments = input_check_range(end, comments, "the second")
    # Якщо початок більше або дорівнює кінцю - вивести повідомлення користувачу.
    if(start >= end):
        comments.clear()
        comments.append("first")
        comments.append("second")
    # Перевірка кроку координат. Діапазон [0.01, 1000000].
    step = entry_step.get()
    step, comments = input_check_step(step, comments, "the third")
    # Перевірка синтаксису рівняння. Воно може містити лише аргумент х.
    eq = entry_eq.get()
    eq, comments = input_check_eq(eq, comments, "the fourth")
    # Якщо список comments не пустий, то вивести користувачу повідомлення з вказівкою невірних полей.
    if comments != []:
        # Якщо елемент не знайдено, то ловиться ValueError і нічого не відбувається.
        try:
            del interface[interface.index(comment)]
        except ValueError:
            pass
        # Перетворення рядка.
        str = input_comment(comments)
        comment.config(text=str)
        interface.append(comment)
        comment.pack(fill="x")
    # Інакше - створити екземпляр Graph і додати його до глобального списку графів.
    else:
        graphs.append(Graph(start, end, step, eq))
        print(graphs[0].print())
        try:
            file_menu.index("Merge")
            merge_separate2(menu, ax1, ax2)
        except:
            merge_separate1(menu, ax1, ax2)
        close(interface)


# Функція для перетворення числа у число з плаваючою крапкою.
def toFloat(x):
    try:
        temp = x
        return float(temp)
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
    except (ZeroDivisionError, ArithmeticError):
        pass
    return eq, comments


# Функція для конкатенації підказки користувача.
def input_comment(comments):
    comments[0] = comments[0].capitalize()
    str = ", ".join(comments)
    ist =  "is"
    if(len(comments) > 1):
        ist = "are"
    return "{0} {1} invalid.".format(str, ist)


def set_canvas():
    global canvas
    canvas = FigureCanvasTkAgg(fig, master=right_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
    toolbar = NavigationToolbar2Tk(canvas, right_frame)
    toolbar.update()
    canvas.get_tk_widget().pack()

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
file_menu.add_command(label="Merge", command=lambda: merge_separate1(file_menu, ax1, ax2))
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

# Глобальна змінна для збереження графів.
graphs = []

# Створюємо фігуру, в якій розташовано усі графи.
fig = plt.figure()

# Тимчасова ініціалізація графами. Задаємо рівняння і знаходимо похідну.
graphs.append(Graph(0, math.pi*2, 0.05, "x**2"))
graph = graphs[0]

# Створюємо вісь у фігурі. (121) позначають (1 вертикаль, 2 горизонталь, 1 номер плоту).
ax1 = fig.add_subplot(121)
ax1.set_title(label="Function", color='black', loc='left', font=fpath)
# Відображаємо наши координати на плоті. scatter краще оброблює точки розриву, ніж plot.
ax1.scatter(graph.x, graph.y, c="#FFB526", s=5, label=graph.eq)
ax1.legend()

# Створюємо вісь у фігурі. (122) позначають (1 вертикаль, 1 горизонталь, 2 номер плоту).
ax2 = fig.add_subplot(122)
ax2.set_title(label="Derivative", color='black', loc='left', font=fpath)
# Відображаємо наши координати на плоті. scatter краще оброблює точки розриву, ніж plot.
ax2.scatter(graph.x, graph.dy, color="b", s=5, label=graph.deri)
ax2.legend()

# Задаємо холст, на якому буде намальовано граф. Особоливість у тому, що можна вставити граф у будь-який фрейм.
set_canvas()

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

# Створюємо кнопку з зкругленими границями.
input_btn = RoundedButton(left_frame, text="Input", highlightthickness=0,  width=100, height=60, radius=100,
                          btnbackground="#FFB526", btnforeground="#000000",
                          clicked=lambda: input_execute(file_menu, ax1, ax2))

# Основний цикл вікна tkinter.
root.mainloop()
