import tkinter as tk

class TextViewer:
    def __init__(self, master):
        self.master = master
        self.text_widget = tk.Text(master, height=10, width=40)
        self.text_widget.pack()
        button_close = tk.Button(self.master, text="Close",  command=self.close_viewer)
        button_close.pack(side=tk.BOTTOM, pady=5)
        self.selected_choice = None  # Attribute to store the selected choice

    def display_text(self, text):
        current_text = self.text_widget.get("1.0", tk.END)
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert(tk.END, current_text + text + "\n")
        
    def close_viewer(self):
        self.master.destroy()

    def display_choice(self, choices):
        center_frame = tk.Frame(self.master)
        center_frame.pack()

        for choice in choices:
            button_choice = tk.Button(center_frame, text=choice, command=lambda c=choice: self.on_choice_selected(c))
            button_choice.pack(side=tk.LEFT, padx=10)
        
            
    def on_choice_selected(self, choice):
        self.selected_choice = choice
        self.master.destroy()
    