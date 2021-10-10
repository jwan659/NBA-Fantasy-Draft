import os
from tkinter import *
import tkinter as tk
from tkinter import ttk
import pandas as pd

# player grid
class PlayerGrid(tk.Frame):
    def __init__(self, df, players_drafted, dfs, other_players_drafted):
        df = self.refresh_list(players_drafted, dfs, other_players_drafted)
        # Add a Treeview widget
        tree = ttk.Treeview(column=('Punt Type',"Guard", "LName", "Roll No"), show='headings', height=5)
        tree.column("# 1", anchor=tk.CENTER)
        tree.heading("# 1", text="Punt Type")
        tree.column("# 2", anchor=tk.CENTER)
        tree.heading("# 2", text="Guard")
        tree.column("# 3", anchor=tk.CENTER)
        tree.heading("# 3", text="Forward")
        tree.column("# 4", anchor=tk.CENTER)
        tree.heading("# 4", text="Centre")
        
        # Insert the data in Treeview widget
        
        if len(players_drafted) != 0:
            tree.insert('', 'end', text="1", values=(df.iloc[0,0], df.iloc[0,1], df.iloc[0,2], df.iloc[0,3]))
            tree.insert('', 'end', text="1", values=(df.iloc[1,0], df.iloc[1,1], df.iloc[1,2], df.iloc[1,3]))
            tree.insert('', 'end', text="1", values=(df.iloc[2,0], df.iloc[2,1], df.iloc[2,2], df.iloc[2,3]))
        else:
            tree.insert('', 'end', text="1", values=(df.iloc[0,0], df.iloc[0,1], df.iloc[0,2], df.iloc[0,3]))

        tree.grid(row=8, column=0)

    # refresh list of players to draft next
    def refresh_list(self, players_drafted, dfs, other_players_drafted):
        # return three best punts?
        best_C, best_F, best_G = None, None, None
        
        if len(players_drafted) == 0:
            best_punts_files = ['Base.csv']
        else:
            # get best punts
            best_punts_files = self.get_current_score(players_drafted, dfs)

        list = []
        # find best players available
        for file in best_punts_files:
            df = dfs[file].sort_values('PRED', axis=0, ascending=False)
            punt_type = file.split('.')[0]
            best_G = self.best_guard(df, players_drafted, other_players_drafted)
            best_F = self.best_forward(df, players_drafted, other_players_drafted)
            best_C = self.best_centre(df, players_drafted, other_players_drafted)
            print(best_G, best_F, best_C)

            list.append([punt_type, best_G, best_F, best_C])

            new_df = pd.DataFrame(list, columns=['Punt Type', 'G', 'F', 'C'])
            print(new_df)
        # return matrix of best players list of lists
        return new_df

    def Update(self, data):
        tk.Listbox.delete(0, 'end')
        # put new data
        for item in data:
            tk.Listbox.insert('end', item)

    def get_current_score(self, players_drafted, dfs):
        punts = []
        punt_scores = {}

        # calculate score for each punt type based on current players
        for key, df in dfs.items():
            score = df[df['PLAYER'].isin(players_drafted)]['PRED'].sum()
            punt_scores[key] = score

        punts = sorted(punt_scores, key=punt_scores.get, reverse=True)[:3]
    
        return punts

    def best_guard(self, df, players_drafted, other_players_drafted):
        #get best guard, forward, and centre
        i = 0
        while df[(df['POS_PG'] == 1) | (df['POS_SG'] == 1)].iloc[i]['PLAYER'] in (players_drafted + other_players_drafted):
            i += 1

        return df[(df['POS_PG'] == 1) | (df['POS_SG'] == 1)].iloc[i]['PLAYER'] + ' - ' + str(round((df[(df['POS_PG'] == 1) | (df['POS_SG'] == 1)].iloc[i]['PRED']),2))

    def best_forward(self, df, players_drafted, other_players_drafted):
        #get best guard, forward, and centre
        i = 0
        while df[(df['POS_PF'] == 1) | (df['POS_SF'] == 1)].iloc[i]['PLAYER'] in (players_drafted + other_players_drafted):
            i += 1

        return df[(df['POS_PF'] == 1) | (df['POS_SF'] == 1)].iloc[i]['PLAYER'] + ' - ' + str(round((df[(df['POS_PF'] == 1) | (df['POS_SF'] == 1)].iloc[i]['PRED']),2))

    def best_centre(self, df, players_drafted, other_players_drafted):
        #get best guard, forward, and centre
        i = 0
        while df[(df['POS_C'] == 1)].iloc[i]['PLAYER'] in (players_drafted + other_players_drafted):
            i += 1

        return df[(df['POS_C'] == 1)].iloc[i]['PLAYER'] + ' - ' + str(round((df[(df['POS_C'] == 1)].iloc[i]['PRED']),2))

# player available players class
class PlayersAvailable(tk.Frame):
    def __init__(self):
    # search bar
        self.entry = tk.Entry()
        self.entry.grid(row=6, column=0)
        self.entry.bind('<KeyRelease>', self.Scankey)
        self.listbox = tk.Listbox()
        self.listbox.grid(row=7, column=0)
    
    def Scankey(self, event):
        val = event.widget.get()
        if val == '':
            data = list
        else:
            data = []
            for item in self.list:
                if val.lower() in item.lower():
                    data.append(item)
        self.Update(data)

    def Update(self, data):
        self.listbox.delete(0, 'end')
        for item in data:
            self.listbox.insert('end', item)

# players drafted class
class DraftedPlayers(tk.Frame):
    def __init__(self, avail_players, list, base_df, listbox, players_drafted, dfs, other_players_drafted):
        Button(text='Drafted By Me', command= lambda:self.drafted_by_me(avail_players, list, base_df, players_drafted, other_players_drafted)).grid(row=10, column=0) #TODO fix this
        Button(text='Drafted By Someone Else', command= lambda:self.drafted_by_me(avail_players, list, base_df, players_drafted, other_players_drafted)).grid(row=11, column=0)
        self.yoyo = listbox
        
        self.l1 = tk.Listbox()
        for item in players_drafted:
            self.l1.insert(tk.END, item)
        self.l1.grid(row=1, column=0)

        self.l2 = tk.Listbox()
        self.l2.grid(row=1, column=1)

    def drafted_by_me(self, avail_players, list, base_df, players_drafted, other_players):
        player = self.yoyo.get(self.yoyo.curselection())
        self.add_player(avail_players, list, base_df, players_drafted, other_players, player, 1)

    def drafted_by_other(self, avail_players, list, base_df, players_drafted, other_players):
        player = self.yoyo.get(self.yoyo.curselection())
        self.add_player(avail_players, list, base_df, players_drafted, other_players, player, 2)

    # add player if they are available
    def add_player(self, avail_players, list, base_df, players_drafted, other_players_drafted, entry, button):
        # check if player valid
        
        if entry in base_df['PLAYER'].values: # if valid player entry
            if (entry not in players_drafted) and (entry not in other_players_drafted):
                if button == 1:
                    players_drafted.append(entry)
                    print('Drafted' + entry) # TODO convert this to message 
                    self.l1.insert(tk.END, entry)
                
                else:
                    other_players_drafted.append(entry)
                    print('Drafted' + entry) # TODO convert this to message
                    self.l2.insert(tk.END, entry)

                list.remove(entry)
                avail_players.Update(list)
                avail_players.refresh_list()

                return 1

        elif entry_status == - 1:
            print(entry + 'has already been drafted.') # TODO convert this to message
        else:
            print(entry + 'could not be found.') # TODO convert this to message

        return

    def check_player_valid(self, base_df, players_drafted, other_players_drafted, entry):
        status = 0
        if entry in base_df['PLAYER'].values:
            if (entry not in players_drafted) and (entry not in other_players_drafted):
                status = 1
            else:
                status = -1
        return status
        
# create application class
class Application(tk.Frame):
    def __init__(self, parent):
        super(Application, self).__init__()
        
        self.label = tk.Label(text="2021-2022 NBA Fantasy Drafter", foreground='white', background='black')
        self.label.grid(row=0, column=0)

        # define class variables
        self.dfs = {}
        self.directory = './data/PRED/'
        for filename in os.listdir(self.directory):
            self.dfs[filename] = pd.read_csv(os.path.join(self.directory, filename))
        
        self.players_drafted = []
        self.other_players_drafted = []
        self.base_df = pd.read_csv('data/PRED/Base.csv')
        self.list = self.base_df['PLAYER'].tolist()
        
        self.player_grid = PlayerGrid(self.base_df, self.players_drafted, self.dfs, self.other_players_drafted)
        self.players_available = PlayersAvailable()
        self.my_players = DraftedPlayers(self.players_available, self.list, self.base_df, self.players_available.listbox, self.players_drafted, self.dfs, self.other_players_drafted)

        self.player_grid.refresh_list(self.players_drafted, self.dfs, self.other_players_drafted)
        self.players_available.Update(self.list)
        
        self.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    Application(root)
    root.mainloop()