import os
from tkinter import *
import tkinter as tk
from tkinter import ttk
import pandas as pd

class PlayerGrid(tk.Frame):
    '''player grid class'''
    def __init__(self, root, players_drafted, dfs, other_players_drafted):    
        tk.Frame.__init__(self, root)
        # Add a Treeview widget
        self.tree = ttk.Treeview(column=('Punt Type',"Guard", "LName", "Roll No"), show='headings', height=5)
        self.tree.column("# 1", anchor=tk.CENTER)
        self.tree.heading("# 1", text="Punt Type")
        self.tree.column("# 2", anchor=tk.CENTER)
        self.tree.heading("# 2", text="Guard")
        self.tree.column("# 3", anchor=tk.CENTER)
        self.tree.heading("# 3", text="Forward")
        self.tree.column("# 4", anchor=tk.CENTER)
        self.tree.heading("# 4", text="Centre")
        
        # Insert the data in Treeview widget
        self.df = self.refresh_list(players_drafted, dfs, other_players_drafted)
        self.tree.insert('', 'end', text="1", values=(self.df.iloc[0,0], self.df.iloc[0,1], self.df.iloc[0,2], self.df.iloc[0,3]))
        self.tree.grid(row=8, column=0)

    # refresh list of players to draft next
    def refresh_list(self, players_drafted, dfs, other_players_drafted):
        
        if len(players_drafted) == 0:
            best_punts_files = ['Base.csv']
        else:
            best_punts_files = self.get_current_score(players_drafted, dfs)

        list = []
        # find best players available
        for file in best_punts_files:
            temp = dfs[file].sort_values('PRED', axis=0, ascending=False)
            punt_type = file.split('.')[0]
            best_guard = self.best_guard(temp, players_drafted, other_players_drafted)
            best_forward = self.best_forward(temp, players_drafted, other_players_drafted)
            best_centre = self.best_centre(temp, players_drafted, other_players_drafted)
            print(best_guard, best_forward, best_centre)

            list.append([punt_type, best_guard, best_forward, best_centre])

        df = pd.DataFrame(list, columns=['Punt Type', 'Guard', 'Forward', 'Centre'])
        
        return df

    def refresh_matrix(self, players_drafted, dfs, other_players_drafted):
        self.tree.delete(*self.tree.get_children())
        df = self.refresh_list(players_drafted, dfs, other_players_drafted)
        self.tree.insert('', 'end', text="1", values=(df.iloc[0,0], df.iloc[0,1], df.iloc[0,2], df.iloc[0,3]))
        self.tree.insert('', 'end', text="1", values=(df.iloc[1,0], df.iloc[1,1], df.iloc[1,2], df.iloc[1,3]))
        self.tree.insert('', 'end', text="1", values=(df.iloc[2,0], df.iloc[2,1], df.iloc[2,2], df.iloc[2,3]))


    def get_current_score(self, players_drafted, dfs):
        punts = []
        punt_scores = {}

        # calculate score for each punt type based on current players
        for key, frame in dfs.items():
            score = frame[frame['PLAYER'].isin(players_drafted)]['PRED'].sum()
            punt_scores[key] = score

        punts = sorted(punt_scores, key=punt_scores.get, reverse=True)[:3]
    
        return punts

    def best_guard(self, df, players_drafted, other_players_drafted):
        i = 0
        while df[(df['POS_PG'] == 1) | (df['POS_SG'] == 1)].iloc[i]['PLAYER'] in (players_drafted + other_players_drafted):
            i += 1

        return df[(df['POS_PG'] == 1) | (df['POS_SG'] == 1)].iloc[i]['PLAYER'] + ' - ' + str(round((df[(df['POS_PG'] == 1) | (df['POS_SG'] == 1)].iloc[i]['PRED']),2))

    def best_forward(self, df, players_drafted, other_players_drafted):
        i = 0
        while df[(df['POS_PF'] == 1) | (df['POS_SF'] == 1)].iloc[i]['PLAYER'] in (players_drafted + other_players_drafted):
            i += 1

        return df[(df['POS_PF'] == 1) | (df['POS_SF'] == 1)].iloc[i]['PLAYER'] + ' - ' + str(round((df[(df['POS_PF'] == 1) | (df['POS_SF'] == 1)].iloc[i]['PRED']),2))

    def best_centre(self, df, players_drafted, other_players_drafted):
        i = 0
        while df[(df['POS_C'] == 1)].iloc[i]['PLAYER'] in (players_drafted + other_players_drafted):
            i += 1

        return df[(df['POS_C'] == 1)].iloc[i]['PLAYER'] + ' - ' + str(round((df[(df['POS_C'] == 1)].iloc[i]['PRED']),2))

class PlayersAvailable(tk.Frame):
    '''asdf'''
    def __init__(self, i_list):
        tk.Frame.__init__(self, root)
        self.entry = tk.Entry()
        self.entry.grid(row=6, column=0)
        self.entry.bind('<KeyRelease>', self.scankey)
        self.listbox = tk.Listbox()
        self.listbox.grid(row=7, column=0)
        self.list = i_list

    def scankey(self, event):
        '''search bar'''
        val = event.widget.get()
        if val == '':
            data = list
        else:
            data = []
            for item in self.list:
                if val.lower() in item.lower():
                    data.append(item)
        self.update(data)

    def update(self, data):
        self.listbox.delete(0, 'end')
        for item in data:
            self.listbox.insert('end', item)


class DraftedPlayers(tk.Frame):
    '''asdfasdf'''
    def __init__(self, grid, avail_players, players, base_df, listbox, players_drafted, dfs, other_players_drafted):
        ''' players drafted class '''
        tk.Frame.__init__(self, root)
        Button(text='Drafted By Me', command= lambda:self.add_player(dfs, grid, avail_players, players, base_df, players_drafted, other_players_drafted, 1)).grid(row=10, column=0) #TODO fix this
        Button(text='Drafted By Someone Else', command= lambda:self.add_player(dfs, grid, avail_players, players, base_df, players_drafted, other_players_drafted, 2)).grid(row=11, column=0)
        self.yoyo = listbox
        
        self.l1 = tk.Listbox()
        for item in players_drafted:
            self.l1.insert(tk.END, item)
        self.l1.grid(row=1, column=0)

        self.l2 = tk.Listbox()
        self.l2.grid(row=1, column=1)

    # add player if they are available
    def add_player(self, dfs, grid, avail_players, players, base_df, players_drafted, other_players_drafted, button):
        '''method to add player'''
        player = self.yoyo.get(self.yoyo.curselection())
        if player in base_df['PLAYER'].values: # if valid player entry
            if (player not in players_drafted) and (player not in other_players_drafted):
                if button == 1:
                    players_drafted.append(player)
                    print('Drafted' + player) # TODO convert this to message 
                    self.l1.insert(tk.END, player)
                
                else:
                    other_players_drafted.append(player)
                    print('Drafted' + player) # TODO convert this to message
                    self.l2.insert(tk.END, player)

                players.remove(player)
                avail_players.update(players)
                grid.refresh_matrix(players_drafted, dfs, other_players_drafted)

                return 1
        return
    
    def check_player_valid(self, base_df, players_drafted, other_players_drafted, entry):
        '''method to check whether a player can play'''
        status = 0
        if entry in base_df['PLAYER'].values:
            if (entry not in players_drafted) and (entry not in other_players_drafted):
                status = 1
            else:
                status = -1
        return status
        

class Application(tk.Frame):
    '''docstring'''
    def __init__(self, root):
        tk.Frame.__init__(self, root)
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
        self.all_players = self.base_df['PLAYER'].tolist()
        
        self.player_grid = PlayerGrid(root, self.players_drafted, self.dfs, self.other_players_drafted)
        self.players_available = PlayersAvailable(self.all_players)
        self.drafted_players = DraftedPlayers(self.player_grid, self.players_available, self.all_players, self.base_df, self.players_available.listbox, self.players_drafted, self.dfs, self.other_players_drafted)

        self.players_available.update(self.all_players)
        
        self.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    Application(root)
    root.mainloop()