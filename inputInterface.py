import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
import math


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
                        **kwargs):  # if update is False a new rounded rectangle's id will be returned else updates existing rounded rect.
        # source: https://stackoverflow.com/a/44100075/15993687
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


def func():
    print("Button pressed")


def clicked(menu):
    menu.entryconfigure(1, label="Clicked!")


root = tk.Tk()
root.title("DeriGraph")
root.iconbitmap("logo.ico")
root.config(bg="skyblue")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry("{}x{}+0+0".format(str(screen_width), str(screen_height)))


menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar)
file_menu.add_command(label="Input values", command=lambda: clicked(file_menu))
menu_bar.add_cascade(label="Tasks", menu=file_menu)
root.config(menu=menu_bar)

wrapper_frame = tk.Frame(root, bg="skyblue")
wrapper_frame.pack(padx=10, pady=10, expand=tk.YES, fill=tk.BOTH)
right_frame = tk.Frame(wrapper_frame, bd=5, bg="orange")
right_frame.pack(side="right", expand=tk.YES, fill=tk.BOTH, pady=20, padx=5)

fig = Figure(figsize=(1, 1),
             dpi=100)

equation = "i ** 2"
i = np.arange(0, math.pi*2, 0.05)
y = eval(equation)

plot1 = fig.add_subplot(121)
plot1.plot(i, y, color="g", label=equation)
plot1.legend()
plot2 = fig.add_subplot(122)
plot2.plot(i, y)
canvas = FigureCanvasTkAgg(fig,
                           master=right_frame)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
toolbar = NavigationToolbar2Tk(canvas,
                               right_frame)
toolbar.update()

canvas.get_tk_widget().pack()

fontx = "Small Fonts"
border_color = tk.Frame(wrapper_frame, bd=5, relief="ridge", bg="white")
border_color.pack(side="left", expand=tk.NO, fill=tk.Y, padx=5)
left_frame = tk.Frame(border_color, bg="blue")
left_frame.pack(fill=tk.Y, expand=1)
label = tk.Label(left_frame, text="hello", bg="red", font=(fontx, 15), width=10).pack(fill=tk.X, expand=1)
btn = RoundedButton(left_frame, text="Input", highlightthickness=0,  width=100, height=60, radius=100, btnbackground="#0078ff", btnforeground="#ffffff", clicked=func)
btn.pack(expand=True, fill="x")
root.mainloop()
