"""
Simulador Monte Carlo - Módulo Base
Herramienta de propósito general para simulaciones Monte Carlo
Autor: Diseñado para análisis estadístico flexible
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import scipy.stats as stats


class Variable:
    """
    Representa una variable aleatoria con su distribución de probabilidad
    """
    
    def __init__(self, nombre, distribucion, parametros):
        """
        Args:
            nombre (str): Nombre de la variable
            distribucion (str): Tipo de distribución ('normal', 'uniforme', 'triangular', 'lognormal', 'binomial', 'poisson')
            parametros (dict): Parámetros específicos de la distribución
        """
        self.nombre = nombre
        self.distribucion = distribucion
        self.parametros = parametros
        self._validar_parametros()
    
    def _validar_parametros(self):
        """Valida que los parámetros sean correctos para la distribución"""
        distribuciones_validas = ['normal', 'uniforme', 'triangular', 'lognormal', 'binomial', 'poisson']
        if self.distribucion not in distribuciones_validas:
            raise ValueError(f"Distribución '{self.distribucion}' no soportada. Use: {distribuciones_validas}")
    
    def generar_muestra(self, n):
        """
        Genera n valores aleatorios según la distribución
        
        Args:
            n (int): Número de valores a generar
            
        Returns:
            numpy.array: Array con los valores generados
        """
        if self.distribucion == 'normal':
            mu = self.parametros['media']
            sigma = self.parametros['desviacion']
            return np.random.normal(mu, sigma, n)
        
        elif self.distribucion == 'uniforme':
            minimo = self.parametros['minimo']
            maximo = self.parametros['maximo']
            return np.random.uniform(minimo, maximo, n)
        
        elif self.distribucion == 'triangular':
            minimo = self.parametros['minimo']
            moda = self.parametros['moda']
            maximo = self.parametros['maximo']
            return np.random.triangular(minimo, moda, maximo, n)
        
        elif self.distribucion == 'lognormal':
            mu = self.parametros['media_log']
            sigma = self.parametros['desviacion_log']
            return np.random.lognormal(mu, sigma, n)
        
        elif self.distribucion == 'binomial':
            n_trials = self.parametros['n']
            p = self.parametros['p']
            return np.random.binomial(n_trials, p, n)
        
        elif self.distribucion == 'poisson':
            lam = self.parametros['lambda']
            return np.random.poisson(lam, n)


class Modelo:
    """
    Define la relación entre variables mediante una fórmula
    """
    
    def __init__(self, formula, variables):
        """
        Args:
            formula (str): Fórmula que relaciona las variables (ej: "x + y * 2")
            variables (dict): Diccionario de objetos Variable {nombre: Variable}
        """
        self.formula = formula
        self.variables = variables
        self._validar_formula()
    
    def _validar_formula(self):
        """Valida que la fórmula use solo variables definidas"""
        # Extraer nombres de variables en la fórmula
        import re
        nombres_en_formula = re.findall(r'\b[a-zA-Z_]\w*\b', self.formula)
        
        # Filtrar funciones matemáticas comunes
        funciones_permitidas = {'sqrt', 'exp', 'log', 'sin', 'cos', 'tan', 'abs', 'min', 'max', 'pow'}
        nombres_en_formula = [n for n in nombres_en_formula if n not in funciones_permitidas]
        
        # Verificar que todas las variables existan
        for nombre in nombres_en_formula:
            if nombre not in self.variables:
                raise ValueError(f"Variable '{nombre}' en la fórmula no está definida")
    
    def evaluar(self, valores_variables):
        """
        Evalúa la fórmula con valores específicos de las variables
        
        Args:
            valores_variables (dict): Diccionario {nombre_variable: valor}
            
        Returns:
            float: Resultado de evaluar la fórmula
        """
        # Crear namespace seguro con funciones matemáticas y variables
        namespace = {
            'sqrt': np.sqrt,
            'exp': np.exp,
            'log': np.log,
            'sin': np.sin,
            'cos': np.cos,
            'tan': np.tan,
            'abs': abs,
            'min': min,
            'max': max,
            'pow': pow,
            **valores_variables
        }
        
        try:
            return eval(self.formula, {"__builtins__": {}}, namespace)
        except Exception as e:
            raise ValueError(f"Error al evaluar la fórmula: {e}")


class Simulador:
    """
    Motor principal que ejecuta las simulaciones Monte Carlo
    """
    
    def __init__(self, modelo, n_simulaciones=10000):
        """
        Args:
            modelo (Modelo): Modelo a simular
            n_simulaciones (int): Número de simulaciones a ejecutar
        """
        self.modelo = modelo
        self.n_simulaciones = n_simulaciones
    
    def ejecutar(self):
        """
        Ejecuta las simulaciones
        
        Returns:
            Resultados: Objeto con los resultados de las simulaciones
        """
        resultados_simulaciones = []
        
        # Generar muestras para todas las variables
        muestras_variables = {}
        for nombre, variable in self.modelo.variables.items():
            muestras_variables[nombre] = variable.generar_muestra(self.n_simulaciones)
        
        # Evaluar el modelo para cada simulación
        for i in range(self.n_simulaciones):
            valores_actuales = {nombre: muestras_variables[nombre][i] 
                              for nombre in self.modelo.variables.keys()}
            resultado = self.modelo.evaluar(valores_actuales)
            resultados_simulaciones.append(resultado)
        
        return Resultados(np.array(resultados_simulaciones))


class Resultados:
    """
    Almacena y analiza los resultados de las simulaciones
    """
    
    def __init__(self, datos):
        """
        Args:
            datos (numpy.array): Array con los resultados de todas las simulaciones
        """
        self.datos = datos
    
    def estadisticas(self):
        """
        Calcula estadísticas descriptivas
        
        Returns:
            dict: Diccionario con estadísticas
        """
        return {
            'media': np.mean(self.datos),
            'mediana': np.median(self.datos),
            'desviacion': np.std(self.datos),
            'minimo': np.min(self.datos),
            'maximo': np.max(self.datos),
            'percentil_2_5': np.percentile(self.datos, 2.5),
            'percentil_25': np.percentile(self.datos, 25),
            'percentil_75': np.percentile(self.datos, 75),
            'percentil_97_5': np.percentile(self.datos, 97.5)
        }
    
    def graficar(self, ax):
        """
        Genera histograma de resultados
        
        Args:
            ax: Axes de matplotlib donde graficar
        """
        ax.clear()
        ax.hist(self.datos, bins=50, density=True, alpha=0.7, color='steelblue', edgecolor='black')
        ax.axvline(np.mean(self.datos), color='red', linestyle='--', linewidth=2, label=f'Media: {np.mean(self.datos):.2f}')
        ax.axvline(np.percentile(self.datos, 2.5), color='orange', linestyle=':', linewidth=1.5, label='IC 95%')
        ax.axvline(np.percentile(self.datos, 97.5), color='orange', linestyle=':', linewidth=1.5)
        ax.set_xlabel('Valor')
        ax.set_ylabel('Densidad de Probabilidad')
        ax.set_title('Distribución de Resultados - Simulación Monte Carlo')
        ax.legend()
        ax.grid(True, alpha=0.3)


class AplicacionMonteCarlo:
    """
    Interfaz gráfica principal de la aplicación
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Monte Carlo - Módulo Base")
        self.root.geometry("1200x800")
        
        # Variables de control
        self.variables = {}  # {nombre: Variable}
        self.resultados = None
        
        # Configurar el layout principal
        self._crear_interfaz()
    
    def _crear_interfaz(self):
        """Crea todos los elementos de la interfaz"""
        
        # Frame principal con dos paneles
        panel_izquierdo = ttk.Frame(self.root, padding="10")
        panel_izquierdo.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Panel derecho con scrollbar
        # Crear un frame contenedor para el canvas y scrollbar
        container_derecho = ttk.Frame(self.root)
        container_derecho.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Crear canvas y scrollbar
        canvas_derecho = tk.Canvas(container_derecho, highlightthickness=0)
        scrollbar_derecho = ttk.Scrollbar(container_derecho, orient="vertical", command=canvas_derecho.yview)
        
        # Frame que contendrá todo el contenido (con scroll)
        panel_derecho = ttk.Frame(canvas_derecho, padding="10")
        
        # Configurar el canvas
        canvas_derecho.configure(yscrollcommand=scrollbar_derecho.set)
        
        # Empaquetar scrollbar y canvas
        scrollbar_derecho.pack(side=tk.RIGHT, fill=tk.Y)
        canvas_derecho.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Crear ventana en el canvas para el panel_derecho
        canvas_window = canvas_derecho.create_window((0, 0), window=panel_derecho, anchor=tk.NW)
        
        # Función para actualizar la región scrollable
        def _configurar_scroll(event=None):
            canvas_derecho.configure(scrollregion=canvas_derecho.bbox("all"))
            # Ajustar el ancho del frame al ancho del canvas
            canvas_ancho = canvas_derecho.winfo_width()
            if canvas_ancho > 1:
                canvas_derecho.itemconfig(canvas_window, width=canvas_ancho)
        
        panel_derecho.bind("<Configure>", _configurar_scroll)
        canvas_derecho.bind("<Configure>", _configurar_scroll)
        
        # Habilitar scroll con la rueda del mouse
        def _on_mousewheel(event):
            canvas_derecho.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas_derecho.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Configurar pesos para el grid
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=2)
        self.root.rowconfigure(0, weight=1)
        
        # ===== PANEL IZQUIERDO: Configuración =====
        
        # Sección 1: Variables
        ttk.Label(panel_izquierdo, text="VARIABLES", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=5)
        
        ttk.Label(panel_izquierdo, text="Nombre:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.nombre_var = tk.StringVar()
        ttk.Entry(panel_izquierdo, textvariable=self.nombre_var, width=20).grid(row=1, column=1, pady=2)
        
        ttk.Label(panel_izquierdo, text="Distribución:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.dist_var = tk.StringVar()
        self.combo_dist = ttk.Combobox(panel_izquierdo, textvariable=self.dist_var, width=18, state='readonly')
        self.combo_dist['values'] = ('normal', 'uniforme', 'triangular', 'lognormal', 'binomial', 'poisson')
        self.combo_dist.grid(row=2, column=1, pady=2)
        self.combo_dist.bind('<<ComboboxSelected>>', self._actualizar_parametros)
        
        # Frame para parámetros dinámicos
        self.frame_parametros = ttk.LabelFrame(panel_izquierdo, text="Parámetros", padding="5")
        self.frame_parametros.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(panel_izquierdo, text="Agregar Variable", command=self._agregar_variable).grid(row=4, column=0, columnspan=2, pady=5)
        
        # Lista de variables agregadas
        ttk.Label(panel_izquierdo, text="Variables Agregadas:", font=('Arial', 10, 'bold')).grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=(10, 2))
        self.lista_variables = tk.Listbox(panel_izquierdo, height=6)
        self.lista_variables.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Button(panel_izquierdo, text="Eliminar Variable", command=self._eliminar_variable).grid(row=7, column=0, columnspan=2, pady=2)
        
        # Sección 2: Modelo
        ttk.Label(panel_izquierdo, text="MODELO", font=('Arial', 12, 'bold')).grid(row=8, column=0, columnspan=2, pady=(15, 5))
        
        ttk.Label(panel_izquierdo, text="Fórmula:").grid(row=9, column=0, columnspan=2, sticky=tk.W, pady=2)
        self.formula_text = scrolledtext.ScrolledText(panel_izquierdo, height=4, width=40)
        self.formula_text.grid(row=10, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        
        # Sección 3: Simulación
        ttk.Label(panel_izquierdo, text="SIMULACIÓN", font=('Arial', 12, 'bold')).grid(row=11, column=0, columnspan=2, pady=(15, 5))
        
        ttk.Label(panel_izquierdo, text="Número de simulaciones:").grid(row=12, column=0, sticky=tk.W, pady=2)
        self.n_sim_var = tk.StringVar(value="10000")
        ttk.Entry(panel_izquierdo, textvariable=self.n_sim_var, width=20).grid(row=12, column=1, pady=2)
        
        ttk.Button(panel_izquierdo, text="EJECUTAR SIMULACIÓN", command=self._ejecutar_simulacion, 
                  style='Accent.TButton').grid(row=13, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        # ===== PANEL DERECHO: Resultados =====
        
        ttk.Label(panel_derecho, text="RESULTADOS", font=('Arial', 12, 'bold')).pack(pady=5)
        
        # Frame para gráfico
        self.frame_grafico = ttk.Frame(panel_derecho)
        self.frame_grafico.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Crear figura de matplotlib
        self.figura = Figure(figsize=(8, 5), dpi=100)
        self.ax = self.figura.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figura, self.frame_grafico)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Frame para estadísticas
        self.frame_estadisticas = ttk.LabelFrame(panel_derecho, text="Estadísticas", padding="10")
        self.frame_estadisticas.pack(fill=tk.BOTH, pady=5)
        
        self.texto_estadisticas = scrolledtext.ScrolledText(self.frame_estadisticas, height=10, width=70, state='disabled')
        self.texto_estadisticas.pack(fill=tk.BOTH, expand=True)
        
        # ===== HERRAMIENTAS DE ANÁLISIS =====
        frame_herramientas = ttk.LabelFrame(panel_derecho, text="🎯 HERRAMIENTAS DE ANÁLISIS", padding=10)
        frame_herramientas.pack(pady=10, fill=tk.X)
        
        # Evaluador de Metas
        frame_evaluador = ttk.LabelFrame(frame_herramientas, text="Evaluador de Metas", padding=10)
        frame_evaluador.pack(pady=5, fill=tk.X)
        
        ttk.Label(frame_evaluador, text="Valor Meta (Y):").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.meta_entry = ttk.Entry(frame_evaluador, width=20)
        self.meta_entry.grid(row=0, column=1, padx=5)
        self.meta_entry.bind('<KeyRelease>', self._actualizar_evaluador)
        
        self.meta_resultado_label = ttk.Label(frame_evaluador, text="→ Simule primero para usar esta herramienta", 
                                              foreground="gray", font=('Arial', 9))
        self.meta_resultado_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        
        # Estimador de Resultados
        frame_estimador = ttk.LabelFrame(frame_herramientas, text="Estimador de Resultados", padding=10)
        frame_estimador.pack(pady=5, fill=tk.X)
        
        ttk.Label(frame_estimador, text="Valor de X:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.x_entry = ttk.Entry(frame_estimador, width=20)
        self.x_entry.grid(row=0, column=1, padx=5)
        self.x_entry.bind('<KeyRelease>', self._actualizar_estimador)
        
        self.estimador_resultado_label = ttk.Label(frame_estimador, text="→ Simule primero para usar esta herramienta", 
                                                   foreground="gray", font=('Arial', 9))
        self.estimador_resultado_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
    
    def _actualizar_parametros(self, event=None):
        """Actualiza los campos de parámetros según la distribución seleccionada"""
        # Limpiar frame de parámetros
        for widget in self.frame_parametros.winfo_children():
            widget.destroy()
        
        dist = self.dist_var.get()
        self.params_entries = {}
        
        if dist == 'normal':
            ttk.Label(self.frame_parametros, text="Media:").grid(row=0, column=0, sticky=tk.W)
            self.params_entries['media'] = ttk.Entry(self.frame_parametros, width=15)
            self.params_entries['media'].grid(row=0, column=1)
            
            ttk.Label(self.frame_parametros, text="Desviación:").grid(row=1, column=0, sticky=tk.W)
            self.params_entries['desviacion'] = ttk.Entry(self.frame_parametros, width=15)
            self.params_entries['desviacion'].grid(row=1, column=1)
        
        elif dist == 'uniforme':
            ttk.Label(self.frame_parametros, text="Mínimo:").grid(row=0, column=0, sticky=tk.W)
            self.params_entries['minimo'] = ttk.Entry(self.frame_parametros, width=15)
            self.params_entries['minimo'].grid(row=0, column=1)
            
            ttk.Label(self.frame_parametros, text="Máximo:").grid(row=1, column=0, sticky=tk.W)
            self.params_entries['maximo'] = ttk.Entry(self.frame_parametros, width=15)
            self.params_entries['maximo'].grid(row=1, column=1)
        
        elif dist == 'triangular':
            ttk.Label(self.frame_parametros, text="Mínimo:").grid(row=0, column=0, sticky=tk.W)
            self.params_entries['minimo'] = ttk.Entry(self.frame_parametros, width=15)
            self.params_entries['minimo'].grid(row=0, column=1)
            
            ttk.Label(self.frame_parametros, text="Moda:").grid(row=1, column=0, sticky=tk.W)
            self.params_entries['moda'] = ttk.Entry(self.frame_parametros, width=15)
            self.params_entries['moda'].grid(row=1, column=1)
            
            ttk.Label(self.frame_parametros, text="Máximo:").grid(row=2, column=0, sticky=tk.W)
            self.params_entries['maximo'] = ttk.Entry(self.frame_parametros, width=15)
            self.params_entries['maximo'].grid(row=2, column=1)
        
        elif dist == 'lognormal':
            ttk.Label(self.frame_parametros, text="Media log:").grid(row=0, column=0, sticky=tk.W)
            self.params_entries['media_log'] = ttk.Entry(self.frame_parametros, width=15)
            self.params_entries['media_log'].grid(row=0, column=1)
            
            ttk.Label(self.frame_parametros, text="Desv. log:").grid(row=1, column=0, sticky=tk.W)
            self.params_entries['desviacion_log'] = ttk.Entry(self.frame_parametros, width=15)
            self.params_entries['desviacion_log'].grid(row=1, column=1)
        
        elif dist == 'binomial':
            ttk.Label(self.frame_parametros, text="n (ensayos):").grid(row=0, column=0, sticky=tk.W)
            self.params_entries['n'] = ttk.Entry(self.frame_parametros, width=15)
            self.params_entries['n'].grid(row=0, column=1)
            
            ttk.Label(self.frame_parametros, text="p (probabilidad):").grid(row=1, column=0, sticky=tk.W)
            self.params_entries['p'] = ttk.Entry(self.frame_parametros, width=15)
            self.params_entries['p'].grid(row=1, column=1)
        
        elif dist == 'poisson':
            ttk.Label(self.frame_parametros, text="λ (lambda):").grid(row=0, column=0, sticky=tk.W)
            self.params_entries['lambda'] = ttk.Entry(self.frame_parametros, width=15)
            self.params_entries['lambda'].grid(row=0, column=1)
    
    def _agregar_variable(self):
        """Agrega una nueva variable al modelo"""
        nombre = self.nombre_var.get().strip()
        dist = self.dist_var.get()
        
        if not nombre:
            messagebox.showerror("Error", "Debe ingresar un nombre para la variable")
            return
        
        if nombre in self.variables:
            messagebox.showerror("Error", f"La variable '{nombre}' ya existe")
            return
        
        if not dist:
            messagebox.showerror("Error", "Debe seleccionar una distribución")
            return
        
        # Extraer parámetros
        try:
            parametros = {}
            for key, entry in self.params_entries.items():
                valor = entry.get().strip()
                if not valor:
                    messagebox.showerror("Error", f"Debe ingresar el parámetro '{key}'")
                    return
                parametros[key] = float(valor)
            
            # Crear variable
            variable = Variable(nombre, dist, parametros)
            self.variables[nombre] = variable
            
            # Actualizar lista
            self.lista_variables.insert(tk.END, f"{nombre} ({dist})")
            
            # Limpiar campos
            self.nombre_var.set("")
            self.dist_var.set("")
            self._actualizar_parametros()
            
            messagebox.showinfo("Éxito", f"Variable '{nombre}' agregada correctamente")
        
        except ValueError as e:
            messagebox.showerror("Error", f"Error en los parámetros: {e}")
    
    def _eliminar_variable(self):
        """Elimina la variable seleccionada"""
        seleccion = self.lista_variables.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una variable para eliminar")
            return
        
        idx = seleccion[0]
        texto = self.lista_variables.get(idx)
        nombre = texto.split(" (")[0]
        
        del self.variables[nombre]
        self.lista_variables.delete(idx)
        
        messagebox.showinfo("Éxito", f"Variable '{nombre}' eliminada")
    
    def _ejecutar_simulacion(self):
        """Ejecuta la simulación Monte Carlo"""
        if not self.variables:
            messagebox.showerror("Error", "Debe agregar al menos una variable")
            return
        
        formula = self.formula_text.get("1.0", tk.END).strip()
        if not formula:
            messagebox.showerror("Error", "Debe ingresar una fórmula")
            return
        
        try:
            n_sim = int(self.n_sim_var.get())
            if n_sim <= 0:
                raise ValueError("El número debe ser positivo")
        except ValueError:
            messagebox.showerror("Error", "Número de simulaciones inválido")
            return
        
        try:
            # Crear modelo
            modelo = Modelo(formula, self.variables)
            
            # Ejecutar simulación
            simulador = Simulador(modelo, n_sim)
            self.resultados = simulador.ejecutar()
            
            # Mostrar resultados
            self._mostrar_resultados()
            
            messagebox.showinfo("Éxito", f"Simulación completada: {n_sim} iteraciones")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error en la simulación:\n{e}")
    
    def _mostrar_resultados(self):
        """Muestra los resultados gráficos y estadísticos"""
        if self.resultados is None:
            return
        
        # Graficar
        self.resultados.graficar(self.ax)
        self.canvas.draw()
        
        # Mostrar estadísticas
        stats_dict = self.resultados.estadisticas()
        
        texto = f"""
╔══════════════════════════════════════════════════════════════╗
║              ESTADÍSTICAS DE LA SIMULACIÓN                   ║
╚══════════════════════════════════════════════════════════════╝

  Medidas de Tendencia Central:
  ─────────────────────────────────────
  • Media:                {stats_dict['media']:>20,.4f}
  • Mediana:              {stats_dict['mediana']:>20,.4f}

  Medidas de Dispersión:
  ─────────────────────────────────────
  • Desviación Estándar:  {stats_dict['desviacion']:>20,.4f}
  • Mínimo:               {stats_dict['minimo']:>20,.4f}
  • Máximo:               {stats_dict['maximo']:>20,.4f}

  Percentiles:
  ─────────────────────────────────────
  • Percentil 2.5:        {stats_dict['percentil_2_5']:>20,.4f}
  • Percentil 25 (Q1):    {stats_dict['percentil_25']:>20,.4f}
  • Percentil 75 (Q3):    {stats_dict['percentil_75']:>20,.4f}
  • Percentil 97.5:       {stats_dict['percentil_97_5']:>20,.4f}

  Intervalo de Confianza 95%:
  ─────────────────────────────────────
  [{stats_dict['percentil_2_5']:,.4f}  -  {stats_dict['percentil_97_5']:,.4f}]
"""
        
        self.texto_estadisticas.config(state='normal')
        self.texto_estadisticas.delete("1.0", tk.END)
        self.texto_estadisticas.insert("1.0", texto)
        self.texto_estadisticas.config(state='disabled')
    
    def _actualizar_evaluador(self, event=None):
        """Actualiza el evaluador de metas en tiempo real"""
        if self.resultados is None:
            return
        
        try:
            valor_y = self.meta_entry.get().strip()
            if not valor_y:
                self.meta_resultado_label.config(text="", foreground="gray")
                return
            
            valor_y = float(valor_y)
            
            # Calcular percentil del valor Y en la distribución de resultados
            percentil = stats.percentileofscore(self.resultados.datos, valor_y)
            probabilidad = 100 - percentil  # Probabilidad de alcanzar o superar
            
            # Formatear mensaje
            texto = f"→ Percentil: {percentil:.2f} | Probabilidad de alcanzar: {probabilidad:.2f}%"
            
            # Color según probabilidad
            if probabilidad >= 50:
                color = "green"
            elif probabilidad >= 25:
                color = "orange"
            else:
                color = "red"
            
            self.meta_resultado_label.config(text=texto, foreground=color, font=('Arial', 10, 'bold'))
        
        except ValueError:
            self.meta_resultado_label.config(text="→ Ingrese un número válido", foreground="gray")
    
    def _actualizar_estimador(self, event=None):
        """Actualiza el estimador de resultados en tiempo real"""
        if self.resultados is None:
            return
        
        try:
            valor_x = self.x_entry.get().strip()
            if not valor_x:
                self.estimador_resultado_label.config(text="", foreground="gray")
                return
            
            valor_x = float(valor_x)
            
            # Obtener la fórmula actual
            formula = self.formula_text.get("1.0", tk.END).strip()
            
            # Crear namespace con el valor de X
            # Asumimos que la variable en la fórmula es la primera variable agregada
            if not self.variables:
                self.estimador_resultado_label.config(text="→ No hay variables definidas", foreground="gray")
                return
            
            # Obtener el nombre de la primera variable (asumiendo es la X)
            nombre_var = list(self.variables.keys())[0]
            
            # Evaluar la fórmula con el valor de X
            namespace = {
                'sqrt': np.sqrt,
                'exp': np.exp,
                'log': np.log,
                'sin': np.sin,
                'cos': np.cos,
                'tan': np.tan,
                'abs': abs,
                'min': min,
                'max': max,
                'pow': pow,
                nombre_var: valor_x
            }
            
            valor_y = eval(formula, {"__builtins__": {}}, namespace)
            
            # Calcular en qué percentil de la distribución cae ese Y
            percentil = stats.percentileofscore(self.resultados.datos, valor_y)
            
            # Formatear el valor Y para mostrarlo
            if abs(valor_y) >= 1_000_000_000:
                y_formateado = f"${valor_y/1_000_000_000:,.2f}B"
            elif abs(valor_y) >= 1_000_000:
                y_formateado = f"${valor_y/1_000_000:,.2f}M"
            else:
                y_formateado = f"${valor_y:,.2f}"
            
            # Mensaje
            texto = f"→ Valor esperado (Y): {y_formateado} | Percentil: {percentil:.2f}"
            
            self.estimador_resultado_label.config(text=texto, foreground="green", font=('Arial', 10, 'bold'))
        
        except ValueError:
            self.estimador_resultado_label.config(text="→ Ingrese un número válido", foreground="gray")
        except Exception as e:
            self.estimador_resultado_label.config(text=f"→ Error: {str(e)}", foreground="red")


def main():
    """Función principal para ejecutar la aplicación"""
    root = tk.Tk()
    app = AplicacionMonteCarlo(root)
    root.mainloop()


if __name__ == "__main__":
    main()
