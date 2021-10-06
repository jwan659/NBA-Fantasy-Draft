import os
import tkinter as tk
from tkinter import ttk
import pandas as pd


def get_current_score():
    punts = []
    punt_scores = {}

    # calculate score for each punt type based on current players
    for key, df in dfs.items(): 
        score = df[df['PLAYER'].isin(players_drafted)]['PRED'].sum()
        punt_scores[key] = score
    print(punt_scores)
    punts = sorted(punt_scores, key=punt_scores.get, reverse=True)[:3]
    
    return punts

def best_guard(df):
    #get best guard, forward, and centre
    i = 0
    while df[(df['POS_PG'] == 1) | (df['POS_SG'] == 1)].iloc[i]['PLAYER'] in (players_drafted + other_players_drafted):
        i += 1

    return df[(df['POS_PG'] == 1) | (df['POS_SG'] == 1)].iloc[i]['PLAYER'] + ' - ' + str(round((df[(df['POS_PG'] == 1) | (df['POS_SG'] == 1)].iloc[i]['PRED']),2))

def best_forward(df):
    #get best guard, forward, and centre
    i = 0
    while df[(df['POS_PF'] == 1) | (df['POS_SF'] == 1)].iloc[i]['PLAYER'] in (players_drafted + other_players_drafted):
        i += 1

    return df[(df['POS_PF'] == 1) | (df['POS_SF'] == 1)].iloc[i]['PLAYER'] + ' - ' + str(round((df[(df['POS_PF'] == 1) | (df['POS_SF'] == 1)].iloc[i]['PRED']),2))

def best_centre(df):
    #get best guard, forward, and centre
    i = 0
    while df[(df['POS_C'] == 1)].iloc[i]['PLAYER'] in (players_drafted + other_players_drafted):
        i += 1

    return df[(df['POS_C'] == 1)].iloc[i]['PLAYER'] + ' - ' + str(round((df[(df['POS_C'] == 1)].iloc[i]['PRED']),2))

# refresh list of players to draft next
def refresh_list():
    # return three best punts?
    
    best_C, best_F, best_G = None, None, None
    
    if len(players_drafted) == 0:
        best_punts_files = ['Base.csv']
    else:
        # get best punts
        best_punts_files = get_current_score()

    list = []
    # find best players available
    for file in best_punts_files:
        df = dfs[file].sort_values('PRED', axis=0, ascending=False)
        punt_type = file.split('.')[0]
        best_G = best_guard(df)
        best_F = best_forward(df)
        best_C = best_centre(df)
        print(best_G, best_F, best_C)

        list.append([punt_type, best_G, best_F, best_C])

    new_df = pd.DataFrame(list, columns=['Punt Type', 'G', 'F', 'C'])
    print(new_df)
    # return matrix of best players list of lists
    return new_df

# add player if they are available
def add_player(entry, button):
    # check if player valid
    entry_status = check_player_valid(entry)
    if entry_status == 1: # if valid player entry
        if button == 1:
            players_drafted.append(entry)
            print('Drafted' + entry) # TODO convert this to message 
            l1.insert(tk.END, entry)
        else:
            other_players_drafted.append(entry)
            print('Drafted' + entry) # TODO convert this to message
            l2.insert(tk.END, entry)

        list.remove(entry)
        Update(list)
        refresh_matrix()

        return 1
        
    elif entry_status == - 1:
        print(entry + 'has already been drafted.') # TODO convert this to message
    else:
        print(entry + 'could not be found.') # TODO convert this to message
    return

# check to see if player is in valid list of players, my list of drafted of players, and players drafted by other opponents
# 0 means the player was not found
# 1 means the player was found and available to draft
# -1 means the player was found but already drafted
def check_player_valid(entry):
    status = 0
    if entry in base_df['PLAYER'].values:
        if (entry not in players_drafted) and (entry not in other_players_drafted):
            status = 1
        else:
            status = -1 
    return status

# add lists for 

# player matrix
def refresh_matrix():
    df = refresh_list()
    print("hello")
    print(df)
    # Add a Treeview widget
    tree = ttk.Treeview(window, column=('Punt Type',"Guard", "LName", "Roll No"), show='headings', height=5)

    tree.column("# 1", anchor=CENTER)
    tree.heading("# 1", text="Punt Type")
    tree.column("# 2", anchor=CENTER)
    tree.heading("# 2", text="Guard")
    tree.column("# 3", anchor=CENTER)
    tree.heading("# 3", text="Forward")
    tree.column("# 4", anchor=CENTER)
    tree.heading("# 4", text="Centre")
    
    # Insert the data in Treeview widget
    
    if len(players_drafted) != 0:
        tree.insert('', 'end', text="1", values=(df.iloc[0,0], df.iloc[0,1], df.iloc[0,2], df.iloc[0,3]))
        tree.insert('', 'end', text="1", values=(df.iloc[1,0], df.iloc[1,1], df.iloc[1,2], df.iloc[1,3]))
        tree.insert('', 'end', text="1", values=(df.iloc[2,0], df.iloc[2,1], df.iloc[2,2], df.iloc[2,3]))
    else:
        tree.insert('', 'end', text="1", values=(df.iloc[0,0], df.iloc[0,1], df.iloc[0,2], df.iloc[0,3]))

    tree.grid(row=8, column=0)

def Scankey(event):
	val = event.widget.get()
	if val == '':
		data = list
	else:
		data = []
		for item in list:
			if val.lower() in item.lower():
				data.append(item)
	Update(data)

def Update(data):
	listbox.delete(0, 'end')
	# put new data
	for item in data:
		listbox.insert('end', item)

def drafted_by_me():
    player = listbox.get(listbox.curselection())
    add_player(player, 1)

def drafted_by_other():
    player = listbox.get(listbox.curselection())
    add_player(player, 2)
# read csv files

directory = './data/PRED/'
dfs = {}
for filename in os.listdir(directory):
    dfs[filename] = pd.read_csv(os.path.join(directory,filename))

players_drafted = []
other_players_drafted = []
base_df = pd.read_csv('data/PRED/Base.csv')

window = tk.Tk()
label = tk.Label(
    text="2021-2022 NBA Fantasy Drafter",
    foreground='white',
    background='black'
)

frame = tk.Frame(window)

# packs
label.grid(row=0, column=0) #done

refresh_matrix()
l1 = Listbox()
for item in players_drafted:
    l1.insert(END, item)

l1.grid(row=1, column=0)
l2 = Listbox()
l2.grid(row=1, column=1)

list = base_df['PLAYER'].tolist()

entry = Entry(window)
entry.grid(row=6, column=0)
entry.bind('<KeyRelease>', Scankey)

listbox = Listbox(window)
listbox.grid(row=7, column=0)
(list)

Button(window, text='Drafted By Me', command=drafted_by_me).grid(row=10, column=0)
Button(window, text='Drafted By Someone Else', command=drafted_by_other).grid(row=11, column=0)
show = Label(window)

window.mainloop()