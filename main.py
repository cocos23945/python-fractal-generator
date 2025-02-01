import tkinter as tk
from tkinter import ttk
import numpy as np
from PIL import Image, ImageTk
import colorsys
import cmath

class FractalGenerator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Генератор фракталів")
        self.geometry("800x600")

        # Параметри за замовчуванням
        self.size = 400
        self.max_iter = 100
        self.julia_c = complex(-0.4, 0.6)
        self.tree_angle = 0.5
        self.tree_ratio = 0.7

        self.setup_ui()
        self.current_fractal = "mandelbrot"
        self.update_fractal()

    def setup_ui(self):
        # Фрейм для елементів керування
        control_frame = ttk.Frame(self)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        # Вибір фракталу
        ttk.Label(control_frame, text="Тип фракталу:").pack(pady=5)
        self.fractal_type = ttk.Combobox(control_frame, 
            values=["Мандельброт", "Жюліа", "Серпінський", "Дерево"])
        self.fractal_type.set("Мандельброт")
        self.fractal_type.pack(pady=5)
        self.fractal_type.bind('<<ComboboxSelected>>', self.on_fractal_change)

        # Повзунок для ітерацій
        ttk.Label(control_frame, text="Кількість ітерацій:").pack(pady=5)
        self.iter_slider = ttk.Scale(control_frame, from_=10, to=200, 
            orient=tk.HORIZONTAL, value=100, command=self.on_param_change)
        self.iter_slider.pack(pady=5)

        # Параметри для множини Жюліа
        self.julia_frame = ttk.LabelFrame(control_frame, text="Параметри Жюліа")
        self.julia_frame.pack(pady=5, fill=tk.X)
        
        ttk.Label(self.julia_frame, text="Реальна частина c:").pack()
        self.julia_real = ttk.Scale(self.julia_frame, from_=-2, to=2, 
            orient=tk.HORIZONTAL, value=-0.4, command=self.on_param_change)
        self.julia_real.pack()
        
        ttk.Label(self.julia_frame, text="Уявна частина c:").pack()
        self.julia_imag = ttk.Scale(self.julia_frame, from_=-2, to=2, 
            orient=tk.HORIZONTAL, value=0.6, command=self.on_param_change)
        self.julia_imag.pack()

        # Параметри для дерева
        self.tree_frame = ttk.LabelFrame(control_frame, text="Параметри дерева")
        self.tree_frame.pack(pady=5, fill=tk.X)
        
        ttk.Label(self.tree_frame, text="Кут:").pack()
        self.tree_angle_slider = ttk.Scale(self.tree_frame, from_=0.1, to=1.0, 
            orient=tk.HORIZONTAL, value=0.5, command=self.on_param_change)
        self.tree_angle_slider.pack()
        
        ttk.Label(self.tree_frame, text="Коефіцієнт зменшення:").pack()
        self.tree_ratio_slider = ttk.Scale(self.tree_frame, from_=0.5, to=0.9, 
            orient=tk.HORIZONTAL, value=0.7, command=self.on_param_change)
        self.tree_ratio_slider.pack()

        # Канвас для відображення фракталу
        self.canvas = tk.Canvas(self, width=self.size, height=self.size)
        self.canvas.pack(side=tk.RIGHT, padx=5, pady=5)

    def create_mandelbrot(self):
        y, x = np.ogrid[-1.4:1.4:self.size*1j, -2:0.8:self.size*1j]
        c = x + y*1j
        z = c
        divtime = self.max_iter + np.zeros(z.shape, dtype=int)

        for i in range(self.max_iter):
            z = z**2 + c
            diverge = z*np.conj(z) > 2**2
            div_now = diverge & (divtime == self.max_iter)
            divtime[div_now] = i
            z[diverge] = 2

        return divtime

    def create_julia(self):
        y, x = np.ogrid[-1.5:1.5:self.size*1j, -1.5:1.5:self.size*1j]
        z = x + y*1j
        divtime = self.max_iter + np.zeros(z.shape, dtype=int)

        for i in range(self.max_iter):
            z = z**2 + self.julia_c
            diverge = z*np.conj(z) > 2**2
            div_now = diverge & (divtime == self.max_iter)
            divtime[div_now] = i
            z[diverge] = 2

        return divtime
    
    def create_sierpinski(self):
        image = np.zeros((self.size, self.size))
        
        def sierpinski_recursive(x, y, size):
            if size < 2:
                image[int(y)][int(x)] = 1
                return
            
            size = size // 2
            sierpinski_recursive(x, y, size)
            sierpinski_recursive(x + size, y, size)
            sierpinski_recursive(x + size//2, y + size, size)
        
        sierpinski_recursive(0, 0, self.size)
        return image

    def create_tree(self):
        image = Image.new('RGB', (self.size, self.size), 'white')
        from PIL import ImageDraw
        draw = ImageDraw.Draw(image)
        
        def draw_branch(x, y, length, angle, depth):
            if depth == 0:
                return
            
            x2 = x + length * np.cos(angle)
            y2 = y - length * np.sin(angle)
            draw.line([(int(x), int(y)), (int(x2), int(y2))], 
                     fill='black', width=max(1, depth))
            
            draw_branch(x2, y2, length * self.tree_ratio, 
                       angle + self.tree_angle, depth - 1)
            draw_branch(x2, y2, length * self.tree_ratio, 
                       angle - self.tree_angle, depth - 1)
        
        draw_branch(self.size//2, self.size-50, self.size//4, 
                   np.pi/2, int(self.max_iter/10))
        return np.array(image)

    def generate_fractal(self):
        if self.current_fractal == "mandelbrot":
            fractal = self.create_mandelbrot()
        elif self.current_fractal == "julia":
            fractal = self.create_julia()
        elif self.current_fractal == "sierpinski":
            fractal = self.create_sierpinski()
        else:  # treegit 
            fractal = self.create_tree()
            return Image.fromarray(fractal)

        if self.current_fractal in ["mandelbrot", "julia"]:
            hues = fractal / fractal.max()
            colors = np.array([[colorsys.hsv_to_rgb(h, 1.0, 1.0) 
                              for h in row] for row in hues])
            return Image.fromarray(np.uint8(colors * 255))
        else:
            return Image.fromarray(np.uint8(fractal * 255))

    def update_fractal(self, *args):
        image = self.generate_fractal()
        self.photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def on_fractal_change(self, *args):
        fractal_name = self.fractal_type.get()
        if fractal_name == "Мандельброт":
            self.current_fractal = "mandelbrot"
        elif fractal_name == "Жюліа":
            self.current_fractal = "julia"
        elif fractal_name == "Серпінський":
            self.current_fractal = "sierpinski"
        else:
            self.current_fractal = "tree"
        self.update_fractal()

    def on_param_change(self, *args):
        self.max_iter = int(self.iter_slider.get())
        self.julia_c = complex(self.julia_real.get(), self.julia_imag.get())
        self.tree_angle = self.tree_angle_slider.get()
        self.tree_ratio = self.tree_ratio_slider.get()
        self.update_fractal()

app = FractalGenerator()
app.mainloop()