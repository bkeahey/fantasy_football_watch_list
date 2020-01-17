import tkinter as tk
from tkinter import messagebox
from db import Database

# Instanciate database object
db = Database('rankings.db')

# Main Application/GUI class
class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title('Fantasy Players to Watch 2020')
        # Width x height
        master.geometry("440x485")
        # Background color
        master.configure(bg="#4C5B70")
        # Create widgets/grid
        self.create_widgets()
        self.selected_player = 0
        # Populate initial list
        self.populate_list()

    def create_widgets(self):
        # Player Name
        self.player_text = tk.StringVar()
        self.player_label = tk.Label(
            self.master, text='Player Name', font=('bold', 14), bg=("#4C5B70"), fg=("#FFFFFF"), pady=10)
        self.player_label.grid(row=0, column=0, columnspan=2, sticky=tk.W)
        self.player_entry = tk.Entry(self.master, textvariable=self.player_text)
        self.player_entry.grid(row=0, column=2, columnspan=2)
        # Position
        self.position_text = tk.StringVar()
        self.position_label = tk.Label(
            self.master, text='Position', font=('bold', 14), bg=("#4C5B70"), fg=("#FFFFFF"), pady=10)
        self.position_label.grid(row=1, column=0, columnspan=2, sticky=tk.W)
        self.position_entry = tk.Entry(
            self.master, textvariable=self.position_text)
        self.position_entry.grid(row=1, column=2, columnspan=2)
        # Position Rank
        self.rank_text = tk.StringVar()
        self.rank_label = tk.Label(
            self.master, text='2019 Position Rank', font=('bold', 14), bg=("#4C5B70"), fg=("#FFFFFF"), pady=10)
        self.rank_label.grid(row=2, column=0, columnspan=2, sticky=tk.W)
        self.rank_entry = tk.Entry(
            self.master, textvariable=self.rank_text)
        self.rank_entry.grid(row=2, column=2, columnspan=2)
        # 2020 Estimated Value
        self.value_text = tk.StringVar()
        self.value_label = tk.Label(
            self.master, text='2020 Estimated Value', font=('bold', 14), bg=("#4C5B70"), fg=("#FFFFFF"), pady=10)
        self.value_label.grid(row=3, column=0, columnspan=2, sticky=tk.W)
        self.value_entry = tk.Entry(self.master, textvariable=self.value_text)
        self.value_entry.grid(row=3, column=2, columnspan=2)

        # Players list using a listbox
        self.players_list = tk.Listbox(self.master, height=13, width=70, border=0)
        self.players_list.grid(row=5, column=0, columnspan=4,
                             rowspan=10, pady=5)
        # Create scrollbar
        self.scrollbar = tk.Scrollbar(self.master)
        self.scrollbar.grid(row=5, column=4, rowspan=10, sticky=tk.NS, pady=5)
        # Set the scrollbar to players
        self.players_list.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.players_list.yview)

        # Bind select to listbox
        self.players_list.bind('<<ListboxSelect>>', self.select_player)

        # Buttons
        self.add_btn = tk.Button(
            self.master, text="Add Player", width=12, command=self.add_player)
        self.add_btn.grid(row=4, column=0, sticky=tk.W, pady=20)

        self.remove_btn = tk.Button(
            self.master, text="Remove Player", width=12, command=self.remove_player)
        self.remove_btn.grid(row=4, column=1, sticky=tk.W)

        self.update_btn = tk.Button(
            self.master, text="Update Player", width=12, command=self.update_player)
        self.update_btn.grid(row=4, column=2)

        self.exit_btn = tk.Button(
            self.master, text="Clear", width=12, command=self.clear_text)
        self.exit_btn.grid(row=4, column=3)

    def populate_list(self):
        # Deletes players before update
        self.players_list.delete(0, tk.END)
        # Loop through records and insert each record into the list
        for row in db.fetch():
            self.players_list.insert(tk.END, row)

    # Add a new player
    def add_player(self):
        if self.player_text.get() == '' or self.position_text.get() == '' or self.rank_text.get() == '' or self.value_text.get() == '':
            messagebox.showerror(
                "Required Fields", "Please include all fields")
            return
        print(self.player_text.get())
        # Insert into the database
        db.insert(self.player_text.get(), self.position_text.get(),
                  self.rank_text.get(), self.value_text.get())
        # Clear the list
        self.players_list.delete(0, tk.END)
        # Insert into the list
        self.players_list.insert(tk.END, (self.player_text.get(), self.position_text.get(
        ), self.rank_text.get(), self.value_text.get()))
        self.clear_text()
        self.populate_list()

    # Runs when a player is selected
    def select_player(self, event):
        try:
            # Get index
            index = self.players_list.curselection()[0]
            # Get selected player
            self.selected_player = self.players_list.get(index)
            # print(selected_player)

            # Add text to entries
            self.player_entry.delete(0, tk.END)
            self.player_entry.insert(tk.END, self.selected_player[1])
            self.position_entry.delete(0, tk.END)
            self.position_entry.insert(tk.END, self.selected_player[2])
            self.rank_entry.delete(0, tk.END)
            self.rank_entry.insert(tk.END, self.selected_player[3])
            self.value_entry.delete(0, tk.END)
            self.value_entry.insert(tk.END, self.selected_player[4])
        except IndexError:
            pass

    # Remove player
    def remove_player(self):
        db.remove(self.selected_player[0])
        self.clear_text()
        self.populate_list()

    # Update player
    def update_player(self):
        db.update(self.selected_player[0], self.player_text.get(
        ), self.position_text.get(), self.rank_text.get(), self.value_text.get())
        self.populate_list()

    # Clear all of the text fields
    def clear_text(self):
        self.player_entry.delete(0, tk.END)
        self.position_entry.delete(0, tk.END)
        self.rank_entry.delete(0, tk.END)
        self.value_entry.delete(0, tk.END)


root = tk.Tk()
app = Application(master=root)
app.mainloop()