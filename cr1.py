import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from tkinter import ttk
import csv


TASKS_FILE = 'tasks.csv'

class TodoApp:
    PRIORITY_OPTIONS = ["High", "Medium", "Low"]
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry('650x410+300+150')

        self.tasks = self.load_tasks()

        self.task_listbox = tk.Listbox(root, selectmode=tk.SINGLE,height=9, bd=5, width=50, font="arial 12 italic bold")
        self.task_listbox.pack(pady=10)

        self.refresh_task_list()

        add_button = tk.Button(root, text="Add Task", command=self.show_add_task_window,height=2, bd=2, width=18,font="sarif 10 bold italic")
        add_button.pack(pady=5)

        remove_button = tk.Button(root, text="Remove Task", command=self.remove_task,height=2, bd=2, width=18,font="sarif 10 bold italic")
        remove_button.pack(pady=5)

        complete_button = tk.Button(root, text="Mark as Completed", command=self.complete_task,height=2, bd=2, width=18,font="sarif 10 bold italic")
        complete_button.pack(pady=5)

    

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        

    def load_tasks(self):
        tasks = []
        try:
            with open(TASKS_FILE, 'r', newline='') as file:
                reader = csv.DictReader(file, delimiter=',')
                for row in reader:
                    task = {
                        'description': row['Description'],
                        'priority': row['Priority'],
                        'due_date': row['Due Date'],
                        'completed': row['Completed'] == 'True'
                    }
                    tasks.append(task)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"An error occurred: {e}")

        return tasks
  
    def save_tasks(self):
        try:
            with open(TASKS_FILE, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['Description', 'Priority', 'Due Date', 'Completed']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for task in self.tasks:
                    writer.writerow({
                        'Description': task['description'],
                        'Priority': task['priority'],
                        'Due Date': task['due_date'],
                        'Completed': str(task['completed'])
                    })
        except Exception as e:
            print(f"An error occurred while saving tasks: {e}")

   
   
    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for i, task in enumerate(self.tasks):
            status = "Completed" if task['completed'] else "Not Completed"
            self.task_listbox.insert(tk.END, f"{i + 1}. {task['description']} - Priority: {task['priority']} - Due Date: {task['due_date']} - {status}")

    def show_add_task_window(self):
        add_window = tk.Toplevel(self.root,)
        add_window.title("Add Task")
        add_window.geometry('400x300')
        
        tk.Label(add_window, text="Description:").pack()
        description_entry = tk.Entry(add_window)
        description_entry.pack()
        
        tk.Label(add_window, text="Priority:").pack()
        priority_var = tk.StringVar()
        priority_combobox = ttk.Combobox(add_window, textvariable=priority_var, values=self.PRIORITY_OPTIONS)
        priority_combobox.pack()
        
        tk.Label(add_window, text="Due Date(MM/DD/YY):").pack()
        due_date_entry =DateEntry(add_window, width=12, background='darkblue', foreground='white', borderwidth=2)
        due_date_entry.pack()

        
        add_button = tk.Button(add_window, text="Add", command=lambda: self.add_task(description_entry.get(), priority_var.get(), due_date_entry.get(), add_window))
        add_button.pack()
        
        
    def add_task(self, description, priority, due_date, add_window):
        if not description or not priority or not due_date:
            messagebox.showwarning("Warning", "Please fill in all fields.")
            return

            
    def add_task(self, description, priority, due_date, add_window):
        # Validate priority value
        if priority not in self.PRIORITY_OPTIONS or not description or not priority or not due_date:
            messagebox.showwarning("Warning", "Invalid data. Please Enter Vaild data.")
            return
        
            
        new_task = {
            'description': description,
            'priority': priority,
            'due_date': due_date,
            'completed': False
        }

        self.tasks.append(new_task)
        self.save_tasks()
        self.refresh_task_list()
        add_window.destroy()

    def remove_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            removed_task = self.tasks.pop(index)
            self.save_tasks()
            self.refresh_task_list()
            messagebox.showinfo("Task Removed", f"Task '{removed_task['description']}' has been removed.")
        else:
            messagebox.showwarning("Warning", "Please select a task to remove.")

    def complete_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            self.tasks[index]['completed'] = True
            self.save_tasks()
            self.refresh_task_list()
            messagebox.showinfo("Task Completed", f"Task '{self.tasks[index]['description']}' has been marked as completed.")
        else:
            messagebox.showwarning("Warning", "Please select a task to mark as completed.")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
