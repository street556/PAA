
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import copy
import threading
import queue

from eightpuzzle.actions import *
from eightpuzzle.eight_puzzle_state import read_state_from_txt_file
from eightpuzzle.eight_puzzle_problem import EightPuzzleProblem
from eightpuzzle.heuristic_tiles_out_of_place import HeuristicTilesOutOfPlace
from eightpuzzle.heuristic_tile_distance import HeuristicTileDistance
from agents.agent import Agent
from search_methods.solution import Solution


class Window(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        self.agent = Agent()
        self.agent.add_heuristic(HeuristicTilesOutOfPlace())
        self.agent.add_heuristic(HeuristicTileDistance())
        self.initial_state = create_default_initial_state()
        self.problem = None
        self.solution = None

        self.solver = None
        self.solution_runner = None

        self.title('Search')

        self.protocol('WM_DELETE_WINDOW', self.on_closing)

        self.images = [[tk.PhotoImage(file='images/tile0.png'), tk.PhotoImage(file='images/tile1.png'), tk.PhotoImage(file='images/tile2.png')],
                       [tk.PhotoImage(file='images/tile3.png'), tk.PhotoImage(file='images/tile4.png'), tk.PhotoImage(file='images/tile5.png')],
                       [tk.PhotoImage(file='images/tile6.png'), tk.PhotoImage(file='images/tile7.png'), tk.PhotoImage(file='images/tile8.png')]]

        self.frame = tk.Frame(master=self)

        # GENERAL STRUCTURE ----------------------------------------------------

        self.panel_buttons = tk.PanedWindow(self.frame)
        self.panel_search_methods = tk.PanedWindow(self.frame)
        self.panel_bottom = tk.PanedWindow(self.frame)

        # BUTTONS PANEL --------------------------------------------------------

        self.button_initial_state = tk.Button(master=self.panel_buttons, text='Read initial state',
                                              command=self.initial_state_button_clicked)
        self.button_initial_state.pack(side='left', padx=5)
        self.button_solve = tk.Button(master=self.panel_buttons, text='Solve', command=self.solve_button_clicked)
        self.button_solve.pack(side='left', padx=5)
        self.button_stop = tk.Button(master=self.panel_buttons, text="Stop", state=tk.DISABLED,
                                     command=self.stop_button_clicked)
        self.button_stop.pack(side="left", padx=5)
        self.button_show_solution = tk.Button(master=self.panel_buttons, text="Show solution", state=tk.DISABLED,
                                              command=self.show_solution_button_clicked)
        self.button_show_solution.pack(side="left", padx=5)
        self.button_reset = tk.Button(master=self.panel_buttons, text="Reset to initial state", state=tk.DISABLED,
                                      command=self.reset_button_clicked)
        self.button_reset.pack(side="left", padx=5)

        # SEARCH METHODS PANEL ------------------------------------------------

        self.combo_search_methods = ttk.Combobox(master=self.panel_search_methods, state="readonly",
                                                 values=self.agent.search_methods)
        self.combo_search_methods.set(self.agent.search_methods[0])
        self.combo_search_methods.pack(side="left", padx=5)

        self.label_search_param = tk.Label(master=self.panel_search_methods, text="limit/beam size: ")
        self.label_search_param.pack(side="left", padx=5)

        self.entry_search_param = tk.Entry(master=self.panel_search_methods, width=3)
        self.entry_search_param.insert(tk.END, "0")
        self.entry_search_param.pack(side="left", padx=3)

        self.combo_heuristics = ttk.Combobox(master=self.panel_search_methods, state="readonly",
                                             values=self.agent.heuristics)
        self.combo_heuristics.set(self.agent.heuristics[0])
        self.combo_heuristics.pack(side="left", padx=5)

        # BOTTOM PANEL -------------------------------------------------------

        self.panel_puzzle = tk.PanedWindow(self.panel_bottom)

        self.canvas_puzzle = tk.Canvas(self.panel_puzzle, height=200, width=200)
        self.panel_puzzle.add(self.canvas_puzzle)
        self.canvas_puzzle.pack(side="left")
        self.draw_state(self.initial_state)
        self.panel_puzzle.pack(side="left")

        self.text_statistics = tk.Text(master=self.panel_bottom, state="normal", height=10, width=32)
        self.text_statistics.pack(side="left", padx=5)

        self.panel_buttons.pack()
        self.panel_search_methods.pack()
        self.panel_bottom.pack()
        self.frame.pack()

        # --------------------------------------------------------------------

        self.frame.bind('<<AgentStopped>>', self.agent_stopped)

        self.after_id = None
        self.queue = queue.Queue()

        # End of constructor ------------------------------------------------

    def initial_state_button_clicked(self):
        filename = fd.askopenfilename(initialdir='.')
        self.initial_state = read_state_from_txt_file(filename)
        self.solution = None
        self.draw_state(self.initial_state)

        self.manage_buttons(initial_state=tk.NORMAL, solve=tk.NORMAL,
                            stop=tk.DISABLED, show_solution=tk.DISABLED, reset=tk.DISABLED)

    def solve_button_clicked(self):
        search_methods_index = self.combo_search_methods.current()
        self.agent.set_search_method(search_methods_index)

        if search_methods_index == 3:  # limited depth first search
            self.agent.search_method.limit = int(self.entry_search_param.get())
        elif search_methods_index == 7:  # beam search
            self.agent.search_method.beam_size = int(self.entry_search_param.get())

        self.agent.heuristic = self.agent.heuristics[self.combo_heuristics.current()]

        goal_state = read_state_from_txt_file("states/goal_state_1.txt")
        self.problem = EightPuzzleProblem(copy.deepcopy(self.initial_state), goal_state)

        self.text_statistics.delete("1.0", "end")

        if not self.problem.is_solvable():
            self.text_statistics.insert(tk.END, "Puzzle has no solution!")
            return

        self.text_statistics.insert(tk.END, "Running...")

        self.manage_buttons(initial_state=tk.DISABLED, solve=tk.DISABLED,
                            stop=tk.NORMAL, show_solution=tk.DISABLED, reset=tk.DISABLED)

        self.solution = None

        self.solver = Solver(self, self.agent, self.problem)
        self.solver.daemon = True
        self.solver.start()

    def stop_button_clicked(self):
        if self.solver:
            self.solver.stop()
        if self.solution_runner:
            self.solution_runner.stop()
            self.solution_runner = None
            self.queue.queue.clear()
            self.after_cancel(self.after_id)
            self.manage_buttons(initial_state=tk.NORMAL, solve=tk.DISABLED,
                                stop=tk.DISABLED, show_solution=tk.DISABLED, reset=tk.NORMAL)

    def show_solution_button_clicked(self):
        self.manage_buttons(initial_state=tk.DISABLED, solve=tk.DISABLED,
                            stop=tk.NORMAL, show_solution=tk.DISABLED, reset=tk.DISABLED)
        self.queue.queue.clear()
        self.solution_runner = SolutionRunner(self, self.solution, copy.deepcopy(self.initial_state))
        self.solution_runner.daemon = True
        self.solution_runner.start()
        self.update_idletasks()
        self.after_id = self.after(0, self.show_solution_step)

    def reset_button_clicked(self):
        self.draw_state(self.initial_state)
        if self.solution:
            self.manage_buttons(initial_state=tk.NORMAL, solve=tk.NORMAL,
                                stop=tk.DISABLED, show_solution=tk.NORMAL, reset=tk.DISABLED)
        else:
            self.manage_buttons(initial_state=tk.NORMAL, solve=tk.NORMAL,
                                stop=tk.DISABLED, show_solution=tk.DISABLED, reset=tk.DISABLED)

    def on_closing(self):
        if self.solver:
            self.solver.stop()
        if self.solution_runner:
            self.solution_runner.stop()
        self.destroy()

    def manage_buttons(self, initial_state, solve, stop, show_solution, reset):
        self.button_initial_state['state'] = initial_state
        self.button_solve['state'] = solve
        self.button_stop['state'] = stop
        self.button_show_solution['state'] = show_solution
        self.button_reset['state'] = reset

    def agent_stopped(self, event):
        self.text_statistics.delete("1.0", "end")
        self.solver = None
        if self.solution:
            self.manage_buttons(initial_state=tk.NORMAL, solve=tk.NORMAL,
                                stop=tk.DISABLED, show_solution=tk.NORMAL, reset=tk.DISABLED)
            self.text_statistics.insert(tk.END, self.agent.search_method)
            self.text_statistics.insert(tk.END, "\nSolution cost: " + str(self.solution.cost))
            self.text_statistics.insert(tk.END, "\nNum of expanded nodes: " + str(self.agent.search_method.num_expanded_nodes))
            self.text_statistics.insert(tk.END, "\nMax frontier size: " + str(self.agent.search_method.max_frontier_size))
            self.text_statistics.insert(tk.END, "\nNum of generated states: " + str(self.agent.search_method.num_generated_states))
        else:
            self.text_statistics.insert(tk.END, "No solution found")
            self.manage_buttons(initial_state=tk.NORMAL, solve=tk.NORMAL,
                                stop=tk.DISABLED, show_solution=tk.DISABLED, reset=tk.DISABLED)

    def show_solution_step(self):
        if not self.queue.empty():
            state, done = self.queue.get()
            if done:
                self.queue.queue.clear()
                self.after_cancel(self.after_id)
                self.solution_runner = None
                self.manage_buttons(initial_state=tk.NORMAL, solve=tk.DISABLED,
                                    stop=tk.DISABLED, show_solution=tk.DISABLED, reset=tk.NORMAL)
                return
            self.draw_state(state)
        self.update_idletasks()
        self.after_id = self.after(500, self.show_solution_step)

    def draw_state(self, state: EightPuzzleState):
        for row in range(3):
            for col in range(3):
                tile_value = state.get_tile_value(row, col)
                self.canvas_puzzle.create_image(25 + col * 50, 25 + row * 50,
                                                image=self.images[tile_value // 3][tile_value % 3], anchor=tk.NW)


def create_default_initial_state() -> EightPuzzleState:
    return read_state_from_txt_file("./states/initial_state_28.txt")


class Solver(threading.Thread):

    def __init__(self, gui: Window, agent: Agent, problem: EightPuzzleProblem):
        super(Solver, self).__init__()
        self.gui = gui
        self.agent = agent
        self.problem = problem

    def stop(self):
        self.agent.stop()

    def run(self):
        self.gui.solution = self.agent.solve_problem(self.problem)
        self.gui.frame.event_generate('<<AgentStopped>>', when='tail')


class SolutionRunner(threading.Thread):

    def __init__(self, gui: Window, solution: Solution, state: EightPuzzleState):
        super(SolutionRunner, self).__init__()
        self.gui = gui
        self.solution = solution
        self.state = state
        self.thread_running = False

    def stop(self):
        self.thread_running = False

    def run(self):
        self.thread_running = True
        actions = self.solution.actions
        iteration = 0
        while iteration < len(actions) and self.thread_running:
            actions[iteration].execute(self.state)
            iteration += 1
            self.gui.queue.put((copy.deepcopy(self.state), False))  # False: still running

        self.gui.queue.put((None, True))  # Done
