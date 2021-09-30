import tkinter as tk

window = tk.Tk()
label = tk.Label(
    text="2021-2022 NBA Fantasy Drafter",
    foreground='white',
    background='black'
)

my_entries = tk.Entry(fg="yellow", bg="blue", width=50)
other_entries = tk.Entry(fg="yellow", bg="blue", width=50)

# packs
label.pack()
my_entries.pack()
other_entries.pack()

# refresh list of players to draft next
def refresh_list():
    return 0

# add player to list of
def on_change(e):
    print(e.widget.get())
    refresh_list()

# add player to others drafted list
def in_change(e):
    print(e.widget.get())
    refresh_list()

my_entries.bind("<Return>", on_change)
other_entries.bind("<Return>", in_change)

window.mainloop()


# Three buttons:
# 1. Add a player I just drafted
# 2. Add a player someone else drafted
# 3. Check who I should draft next -> button? or 
##  Grid layout? Position and punting strategy