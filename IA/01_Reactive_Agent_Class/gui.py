
import tkinter as tk

import queue
import numpy as np
from environment import Environment


class Window(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        self.title("Reactive Agent")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.frame = tk.Frame(master=self)

        self.panel_iterations = tk.PanedWindow(self.frame)
        self.panel_iterations.pack()

        self.label_iterations = tk.Label(master=self.panel_iterations, text="Iterations: ")
        self.label_iterations.pack(side="left", padx=5)

        self.entry_iterations = tk.Entry(master=self.panel_iterations, width=4)
        self.entry_iterations.insert(tk.END, "100")
        self.entry_iterations.pack(side="left", padx=3)

        self.label_current_iteration = tk.Label(master=self.panel_iterations, text="Current iteration: ")
        self.label_current_iteration.pack(side="left", padx=5)

        self.entry_current_iteration = tk.Entry(master=self.panel_iterations, width=4)
        self.entry_current_iteration.insert(tk.END, '0')
        self.entry_current_iteration.pack(side="left", padx=3)

        self.canvas = tk.Canvas(self.frame, bg="white", height=303, width=303)
        self.canvas.pack()

        self.panel_buttons = tk.PanedWindow(self.frame)
        self.panel_buttons.pack()

        self.btn_run = tk.Button(master=self.panel_buttons, text="Start", command=self.run_button_clicked)
        self.btn_run.pack(side='left')

        self.btn_stop = tk.Button(master=self.panel_buttons, text="Stop", command=self.stop_button_clicked)
        self.btn_stop.pack(side='left')
        self.btn_stop['state'] = tk.DISABLED

        self.frame.pack()

        self.after_id = None
        self.queue = queue.Queue()

        self.environment = Environment(10, 10, int(self.entry_iterations.get()))
        self.environment.add_listener(self)
        self.draw_environment(self.environment.grid)

    def run_button_clicked(self):
        self.btn_run['state'] = tk.DISABLED
        self.btn_stop['state'] = tk.NORMAL
        self.queue.queue.clear()
        self.environment = Environment(10, 10, int(self.entry_iterations.get()))
        self.environment.add_listener(self)
        self.environment.daemon = True
        self.environment.start()
        self.update_idletasks()
        self.after_id = self.after(0, self.environment_updated)

    def stop_button_clicked(self):
        self.btn_run['state'] = tk.NORMAL
        self.btn_stop['state'] = tk.DISABLED
        self.entry_current_iteration.delete(0, tk.END)
        self.entry_current_iteration.insert(0, '0')
        self.queue.queue.clear()
        self.environment = Environment(10, 10, int(self.entry_iterations.get()))
        self.draw_environment(self.environment.grid)
        self.after_cancel(self.after_id)

    def on_closing(self):
        self.environment.stop()
        self.destroy()

    def environment_updated(self) -> None:
        if not self.queue.empty():
            grid, iteration, done = self.queue.get()
            if done:
                self.queue.queue.clear()
                self.after_cancel(self.after_id)
                self.btn_run['state'] = tk.NORMAL
                self.btn_stop['state'] = tk.DISABLED
                return
            self.draw_environment(grid)
            self.entry_current_iteration.delete(0, tk.END)
            self.entry_current_iteration.insert(0, str(iteration))
        self.update_idletasks()
        self.after_id = self.after(1000, self.environment_updated)

    def draw_environment(self, grid: np.ndarray) -> None:
        rows, columns = grid.shape
        cell_size = 30
        for row in range(rows):
            for column in range(columns):
                color = grid[row][column].color
                rect = self.canvas.create_rectangle(0, 0, cell_size, cell_size, fill=color)
                self.canvas.move(rect, column * cell_size + 3, row * cell_size + 3)
