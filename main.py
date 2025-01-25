class FractalGenerator(tk.Tk):
    def __(self):
        super().init()

        self.title("Fractal Generator")
        self.geometry("800x600")

        self.size = 400
        self.max_iter= 100
        self.julia_c = complex(-0.4, 0.6)
        self.tree_angle = 0.5
        self.tree_ratio = 0.7

    def setup_ui(self):
        control_frame = ttk.Frame(self)
        control_frame.pack(sede=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        ttk.Label(control_frame, text="Тип фракталу: ").pack(pady=5)
        self.fractal_type = ttk.Combobox(control_frame, value=["Мандельборна", \
             "Жулія", "Серпінського", "Дерево"])
        self.fractal_type.set("Мандельборна")
        self.fractal_type.pack(pady=5)
        self.fractal_type.bind("<<ComboxSelecte>>", self.on_fractal_change)

        ttk.Label("control_frame, text=:кількість ітеграцій").pack(padu=5) 
        self.iter_slider = ttk.Scale(control_frame, from_=10, to=200, \
            orient=tk.HORIZONTAL, value=100, command=self.on_pram_change)
        self.iter_slider.pack(pady=5)
        
        self.julia_frame = ttk.LabelFrame(control_frame, text="Параметри")
        self.julia_frame.pack(pady=5, fill=tk.X)

        ttk.Label(self.julia_frame, text="Реальна частина : ").pack()
        self.julia_real = ttk.Scale(self.julia_frame, from_ =-2, to=2, \
             orient=tk.HORIZONTAL, value=-0.4, coomand=self.on_param_change)
        self.julia_real.pack()
        
        ttk.Label(self.julia_frame, text="Уявна частина : ").pack()
        self.julia_imag = ttk.Scale(self.julia_frame, from_ =-2, to=2, \
             orient=tk.HORIZONTAL, value=0.6, coomand=self.on_param_change)
        self.julia_imag.pack()  
        
              
        self.tree_frame = ttk.LabelFrame(control_frame, text="Параметри Дерева")
        self.tree_frame.pack(pady=5, fill=tk.X)

        ttk.Label(self.tree_frame, text="Реальна частина : ").pack()
        self.tree_angle_slider = ttk.Scale(self.tree_frame, from_ =-2, to=2, \
             orient=tk.HORIZONTAL, value=-0.4, coomand=self.on_param_change)
        self.tree_angle_slider.pack()
        
        
        ttk.Label(self.tree_frame, text="Кофіцієнт зменшення : ").pack()
        self.tree_ration_slider = ttk.Scale(self.tree_frame, from_ =-2, to=2, \
             orient=tk.HORIZONTAL, value=-0.4, coomand=self.on_param_change)
        self.tree_ration_slider.pack()
                    
        self.carvars = tk.Canvars(self, width=self.size, height=self.size)
        self.canvars.pack(side=tk.RIGHT, padx=5, pady=5)
        
    def crefeate_mandelbrot(self):
        y, x =np.orgid[-1,.4:1.4:self.size*1.j, -2:0.8:self.size*1j, ]
        c = x + y * 1j
        z = c
        divtime = self.max_iter + np.zeros(z.shape, dtype=int)
        
        for i in range(self.max_iter):
            z = z**2 +c
            diverge = z*np.conj(z) > 2**2
            div_now = diverge & (divtime == self.max_iter)
            divtime[div_now] = i 
            z[diverge] = 2 
            
        return divtime         
