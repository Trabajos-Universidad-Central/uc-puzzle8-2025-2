import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import List, Optional

from puzzle import (
    State,
    read_puzzle_file,
    is_solvable,
    manhattan_distance,
    state_to_str,
)
from searches.dfs import dfs
from searches.bpp import bpp
from searches.hill_climbing import hill_climbing
from searches.astar import astar
from searches.genetic import genetic_simple


class Puzzle8GUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title("Puzzle-8 | Métodos de Búsqueda")

        self.start_state: Optional[State] = None
        self.goal_state: Optional[State] = None

        self._build_ui()

    def _build_ui(self) -> None:
        frm = ttk.Frame(self.root, padding=10)
        frm.grid(row=0, column=0, sticky='nsew')
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

    # Cargadores de archivos
        file_bar = ttk.Frame(frm)
        file_bar.grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 8))
        ttk.Button(file_bar, text="Cargar Inicial", command=self.load_start).grid(row=0, column=0, padx=(0, 6))
        ttk.Button(file_bar, text="Cargar Meta", command=self.load_goal).grid(row=0, column=1, padx=(0, 6))

    # Selección de método y parámetros
        opt_bar = ttk.Frame(frm)
        opt_bar.grid(row=1, column=0, columnspan=2, sticky='w', pady=(0, 8))
        ttk.Label(opt_bar, text="Método:").grid(row=0, column=0, padx=(0, 6))
        self.method_var = tk.StringVar(value='DFS (Profundidad)')
        self.method_combo = ttk.Combobox(
            opt_bar,
            textvariable=self.method_var,
            state='readonly',
            values=['DFS (Profundidad)', 'BPP (Profundidad)', 'Ascenso de Colina', 'A*', 'Genético (Simple)'],
        )
        self.method_combo.grid(row=0, column=1, padx=(0, 12))
        self.method_combo.bind('<<ComboboxSelected>>', self._on_method_change)

        ttk.Label(opt_bar, text="Límite profundidad (DFS/BPP):").grid(row=0, column=2, padx=(0, 6))
        self.depth_var = tk.StringVar()
        self.depth_entry = ttk.Entry(opt_bar, textvariable=self.depth_var, width=8)
        self.depth_entry.grid(row=0, column=3, padx=(0, 12))

    # Parámetros del Algoritmo Genético (widgets creados pero ocultos por defecto)
        self.ga_pop_lbl = ttk.Label(opt_bar, text="Población (GA):")
        self.ga_pop_var = tk.StringVar(value='80')
        self.ga_pop_entry = ttk.Entry(opt_bar, textvariable=self.ga_pop_var, width=6)

        self.ga_len_lbl = ttk.Label(opt_bar, text="L. crom (GA):")
        self.ga_len_var = tk.StringVar(value='30')
        self.ga_len_entry = ttk.Entry(opt_bar, textvariable=self.ga_len_var, width=6)

        self.ga_gen_lbl = ttk.Label(opt_bar, text="Gens (GA):")
        self.ga_gen_var = tk.StringVar(value='150')
        self.ga_gen_entry = ttk.Entry(opt_bar, textvariable=self.ga_gen_var, width=6)

        self.ga_mevery_lbl = ttk.Label(opt_bar, text="Mutar cada m (GA):")
        self.ga_mevery_var = tk.StringVar(value='1')
        self.ga_mevery_entry = ttk.Entry(opt_bar, textvariable=self.ga_mevery_var, width=6)

        self.ga_elite_lbl = ttk.Label(opt_bar, text="Elitismo (GA):")
        self.ga_elite_var = tk.StringVar(value='2')
        self.ga_elite_entry = ttk.Entry(opt_bar, textvariable=self.ga_elite_var, width=6)

        ttk.Button(opt_bar, text="Resolver", command=self.solve).grid(row=0, column=12)

    # Configurar la visibilidad inicial de los parámetros GA
        self._update_ga_params_visibility()

    # Visualización de los tableros
        boards = ttk.Frame(frm)
        boards.grid(row=2, column=0, sticky='nw')
        self.start_lbl = ttk.Label(boards, text="Inicial:\n-", justify='left')
        self.start_lbl.grid(row=0, column=0, sticky='w', padx=(0, 16))
        self.goal_lbl = ttk.Label(boards, text="Meta:\n-", justify='left')
        self.goal_lbl.grid(row=0, column=1, sticky='w')

    # Resultados
        result = ttk.Frame(frm)
        result.grid(row=3, column=0, columnspan=2, sticky='nsew', pady=(8, 0))
        frm.rowconfigure(3, weight=1)
        frm.columnconfigure(0, weight=1)

    # Estadísticas (los movimientos se muestran en la trayectoria)
        side = ttk.Frame(result)
        side.grid(row=0, column=0, sticky='ns')

        self.stats_lbl = ttk.Label(
            side,
            text=(
                "Nodos generados: 0\n"
                "Nodos expandidos: 0\n"
                "Dist. Manhattan (inicial→meta): -\n"
                "Profundidad de la solución: -"
            ),
            justify='left',
        )
        self.stats_lbl.grid(row=0, column=0, sticky='w', pady=(0, 8))

    # Trayectoria de tableros con barra de desplazamiento
        center = ttk.Frame(result)
        center.grid(row=0, column=1, sticky='nsew', padx=(16, 0))
        result.columnconfigure(1, weight=1)
        result.rowconfigure(0, weight=1)
        ttk.Label(center, text="Puzzles generados (trayectoria - secuencia):").grid(row=0, column=0, sticky='w')
        text_frame = ttk.Frame(center)
        text_frame.grid(row=1, column=0, sticky='nsew')
        center.rowconfigure(1, weight=1)
        center.columnconfigure(0, weight=1)

        self.path_txt = tk.Text(text_frame, height=20, wrap='none')
        self.v_scroll = ttk.Scrollbar(text_frame, orient='vertical', command=self.path_txt.yview)
        self.path_txt.configure(yscrollcommand=self.v_scroll.set)
        self.path_txt.grid(row=0, column=0, sticky='nsew')
        self.v_scroll.grid(row=0, column=1, sticky='ns')

        text_frame.rowconfigure(0, weight=1)
        text_frame.columnconfigure(0, weight=1)
        self.path_txt.configure(state='disabled')

    def load_start(self) -> None:
        path = filedialog.askopenfilename(
            title='Seleccione archivo de puzzle inicial',
            filetypes=[('Texto', '*.txt')],
        )
        if not path:
            return
        try:
            st = read_puzzle_file(path)
            self.start_state = st
            self.start_lbl.config(text=f"Inicial:\n{state_to_str(st)}")
        except Exception as e:
            messagebox.showerror('Error', f'No se pudo leer el puzzle inicial:\n{e}')

    def load_goal(self) -> None:
        path = filedialog.askopenfilename(
            title='Seleccione archivo de puzzle meta',
            filetypes=[('Texto', '*.txt'), ('Todos', '*.*')],
        )
        if not path:
            return
        try:
            st = read_puzzle_file(path)
            self.goal_state = st
            self.goal_lbl.config(text=f"Meta:\n{state_to_str(st)}")
        except Exception as e:
            messagebox.showerror('Error', f'No se pudo leer el puzzle meta:\n{e}')

    def solve(self) -> None:
        if self.start_state is None or self.goal_state is None:
            messagebox.showwarning('Faltan datos', 'Cargue los puzzles inicial y meta (archivos de texto).')
            return

        if not is_solvable(self.start_state, self.goal_state):
            messagebox.showerror(
                'No resoluble',
                'El par (inicial, meta) no es resoluble (paridad distinta de inversiones).',
            )
            return

        method = self.method_var.get()
        max_depth = None
        max_nodes = None
        if self.depth_var.get().strip():
            try:
                max_depth = int(self.depth_var.get().strip())
                if max_depth < 0:
                    raise ValueError
            except Exception:
                messagebox.showerror('Parámetro inválido', 'Límite de profundidad debe ser un entero ≥ 0.')
                return

    # Ejecutar el algoritmo de resolución deseado
        try:
            if method.startswith('DFS'):
                sol = dfs(self.start_state, self.goal_state, max_depth=max_depth, max_nodes=max_nodes)
            elif method.startswith('BPP'):
                if max_depth is None:
                    messagebox.showerror('Parámetro requerido', 'Para BPP debe indicar el límite de profundidad (nProf).')
                    return
                sol = bpp(self.start_state, self.goal_state, nProf=max_depth, max_nodes=max_nodes)
            elif method.startswith('Ascenso'):
                sol = hill_climbing(self.start_state, self.goal_state, max_nodes=max_nodes)
            elif method == 'A*':
                sol = astar(self.start_state, self.goal_state)
            elif method.startswith('Genético'):
                # Leer parámetros GA
                try:
                    pop = int(self.ga_pop_var.get().strip())
                    length = int(self.ga_len_var.get().strip())
                    gens = int(self.ga_gen_var.get().strip())
                    mevery = int(self.ga_mevery_var.get().strip())
                    elite = int(self.ga_elite_var.get().strip())
                    if pop <= 0 or length <= 0 or gens <= 0 or mevery < 0 or elite < 0 or elite > pop:
                        raise ValueError
                except Exception:
                    messagebox.showerror('Parámetros GA inválidos', 'Use enteros positivos para Población, Longitud, Generaciones, Mutar cada m (>=0) y Elitismo (0..Población).')
                    return
                sol = genetic_simple(
                    self.start_state,
                    self.goal_state,
                    pop_size=pop,
                    chrom_len=length,
                    generations=gens,
                    mutate_every=mevery,
                    elitism=elite,
                )
            else:
                messagebox.showerror('Método no soportado', f'Método no soportado: {method}')
                return
        except Exception as e:
            messagebox.showerror('Error en búsqueda', str(e))
            return

    # La distancia Manhattan en las estadísticas solo aplica para métodos heurísticos
        mdist_text = (
            'no aplica' if (method.startswith('DFS') or method.startswith('BPP')) else str(manhattan_distance(self.start_state, self.goal_state))
        )

        if sol is None:
            self.stats_lbl.config(
                text=(
                    f"Nodos generados: -\n"
                    f"Nodos expandidos: -\n"
                    f"Dist. Manhattan (inicial → meta): {mdist_text}\n"
                    f"Profundidad de la solución: -"
                )
            )
            self._set_path([self.start_state], [])
            messagebox.showinfo('Resultado', 'Fracaso: no se encontró solución.')
            return

        self.stats_lbl.config(
            text=(
                f"Nodos generados: {sol.nodes_generated}\n"
                f"Nodos expandidos: {sol.nodes_expanded}\n"
                f"Dist. Manhattan (inicial→meta): {mdist_text}\n"
                f"Profundidad de la solución: {len(sol.moves)}"
            )
        )
        self._set_path(sol.path, sol.moves)
        messagebox.showinfo('Resultado', f"Éxito: solución encontrada en {len(sol.moves)} movimientos.")

    def _set_path(self, path: List[State], moves: List[str]) -> None:
        self.path_txt.configure(state='normal')
        self.path_txt.delete('1.0', tk.END)
        for i, st in enumerate(path):
            if i == 0:
                step_title = f"Paso {i}: Estado inicial"
            elif i == len(path) - 1:
                step_title = f"Paso {i}: Estado final - solución"
            else:
                step_title = f"Paso {i}: {moves[i-1]}"
            self.path_txt.insert(tk.END, f"{step_title}\n{state_to_str(st)}\n\n")
        self.path_txt.configure(state='disabled')

    def _on_method_change(self, event=None):
        self._update_ga_params_visibility()

    def _update_ga_params_visibility(self):
        method = self.method_var.get()
        show = method.startswith('Genético')
        # Posiciones fijas
        if show:
            self.ga_pop_lbl.grid(row=0, column=4, padx=(0, 6))
            self.ga_pop_entry.grid(row=0, column=5, padx=(0, 12))
            self.ga_len_lbl.grid(row=0, column=6, padx=(0, 6))
            self.ga_len_entry.grid(row=0, column=7, padx=(0, 12))
            self.ga_gen_lbl.grid(row=0, column=8, padx=(0, 6))
            self.ga_gen_entry.grid(row=0, column=9, padx=(0, 12))
            self.ga_mevery_lbl.grid(row=0, column=10, padx=(0, 6))
            self.ga_mevery_entry.grid(row=0, column=11, padx=(0, 12))
            self.ga_elite_lbl.grid(row=1, column=4, padx=(0, 6), pady=(6, 0), sticky='w')
            self.ga_elite_entry.grid(row=1, column=5, padx=(0, 12), pady=(6, 0))
        else:
            for w in [
                self.ga_pop_lbl, self.ga_pop_entry,
                self.ga_len_lbl, self.ga_len_entry,
                self.ga_gen_lbl, self.ga_gen_entry,
                self.ga_mevery_lbl, self.ga_mevery_entry,
                self.ga_elite_lbl, self.ga_elite_entry,
            ]:
                w.grid_remove()
