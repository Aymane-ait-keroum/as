import tkinter as tk
from tkinter import ttk, simpledialog
import json
import os

class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                return json.load(f)
        return []

    def save_tasks(self):
        with open(self.filename, "w") as f:
            json.dump(self.tasks, f, indent=2)

    def add_task(self, task):
        self.tasks.append({"task": task, "done": False})
        self.save_tasks()

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()

    def toggle_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index]["done"] = not self.tasks[index]["done"]
            self.save_tasks()

    def get_filtered_tasks(self, filter_by, search=""):
        filtered = self.tasks
        if filter_by == "Done":
            filtered = [t for t in self.tasks if t["done"]]
        elif filter_by == "Undone":
            filtered = [t for t in self.tasks if not t["done"]]
        if search:
            filtered = [t for t in filtered if search.lower() in t["task"].lower()]
        return filtered

class TaskApp:
    def __init__(self, root):
        self.manager = TaskManager()
        self.root = root
        self.root.title("Gestionnaire de Tâches")
        self.search_var = tk.StringVar()
        self.filter_var = tk.StringVar(value="All")
        self.setup_ui()
        self.refresh_list()

    def setup_ui(self):
        top = ttk.Frame(self.root)
        top.pack(pady=10)
        ttk.Label(top, text="Recherche :").grid(row=0, column=0)
        ttk.Entry(top, textvariable=self.search_var).grid(row=0, column=1, padx=5)
        self.search_var.trace_add("write", lambda *_: self.refresh_list())

        ttk.OptionMenu(top, self.filter_var, "All", "All", "Done", "Undone", command=lambda _: self.refresh_list()).grid(row=0, column=2)

        self.listbox = tk.Listbox(self.root, width=60, height=15)
        self.listbox.pack(pady=10)

        buttons = ttk.Frame(self.root)
        buttons.pack()
        ttk.Button(buttons, text="Ajouter", command=self.add_task).grid(row=0, column=0, padx=5)
        ttk.Button(buttons, text="Supprimer", command=self.remove_task).grid(row=0, column=1, padx=5)
        ttk.Button(buttons, text="Compléter", command=self.toggle_task).grid(row=0, column=2, padx=5)

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        tasks = self.manager.get_filtered_tasks(self.filter_var.get(), self.search_var.get())
        for task in tasks:
            status = "[X]" if task["done"] else "[ ]"
            self.listbox.insert(tk.END, f"{status} {task['task']}")

    def add_task(self):
        task = simpledialog.askstring("Nouvelle tâche", "Entrez une tâche :")
        if task:
            self.manager.add_task(task)
            self.refresh_list()

    def remove_task(self):
        index = self.listbox.curselection()
        if index:
            actual_index = self.get_actual_index(index[0])
            self.manager.remove_task(actual_index)
            self.refresh_list()

    def toggle_task(self):
        index = self.listbox.curselection()
        if index:
            actual_index = self.get_actual_index(index[0])
            self.manager.toggle_task(actual_index)
            self.refresh_list()

    def get_actual_index(self, visible_index):
        filtered = self.manager.get_filtered_tasks(self.filter_var.get(), self.search_var.get())
        visible_task = filtered[visible_index]
        for i, t in enumerate(self.manager.tasks):
            if t == visible_task:
                return i
        return -1

if __name__ == "__main__":
    root = tk.Tk()
    TaskApp(root)
    root.mainloop()
