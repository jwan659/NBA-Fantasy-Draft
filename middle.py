
import os
import tkinter as tk
from tkinter import ttk
import pandas as pd

# remaining players class

# player draft grid class

# players drafted class

# players other ppl drafted class

# create application class
class Application(tk.Frame):
    def __init__(self, parent):
        label = tk.Label(text="2021-2022 NBA Fantasy Drafter", foreground='white', background='black')
        label.grid(row=0, column=0)

        # define class variables
        self.dfs = {}
        self.directory = './data/PRED/'
        for filename in os.listdir(self.directory):
            self.dfs[filename] = pd.read_csv(os.path.join(self.directory, filename))
        
        self.players_drafted = []
        self.other_players_drafted = []
        self.base_df = pd.read_csv('data/PRED/Base.csv')

        self.refresh_matrix()
        self.l1 = tk.Listbox()
        for item in self.players_drafted:
            self.l1.insert(tk.END, item)

        self.l1.grid(row=1, column=0)
        self.l2 = tk.Listbox()
        self.l2.grid(row=1, column=1)

        self.list = self.base_df['PLAYER'].tolist()

        entry = tk.Entry(window)
        entry.grid(row=6, column=0)
        entry.bind('<KeyRelease>', self.Scankey)

        listbox = tk.Listbox(window)
        listbox.grid(row=7, column=0)
        (list)

        tk.Button(window, text='Drafted By Me', command=self.drafted_by_me).grid(row=10, column=0)
        tk.Button(window, text='Drafted By Someone Else', command=self.drafted_by_other).grid(row=11, column=0)
        show = tk.Label(window)

    # refresh list of players to draft next
    def refresh_list(self):
        # return three best punts?
        
        best_C, best_F, best_G = None, None, None
        
        if len(self.players_drafted) == 0:
            best_punts_files = ['Base.csv']
        else:
            # get best punts
            best_punts_files = self.get_current_score()

        list = []
        # find best players available
        for file in best_punts_files:
            df = self.dfs[file].sort_values('PRED', axis=0, ascending=False)
            punt_type = file.split('.')[0]
            best_G = self.best_guard(df)
            best_F = self.best_forward(df)
            best_C = self.best_centre(df)
            print(best_G, best_F, best_C)

            list.append([punt_type, best_G, best_F, best_C])

        new_df = pd.DataFrame(list, columns=['Punt Type', 'G', 'F', 'C'])
        print(new_df)
        # return matrix of best players list of lists
        return new_df
    
    def get_current_score(self):
        punts = []
        punt_scores = {}

        # calculate score for each punt type based on current players
        for key, df in self.dfs.items():
            score = df[df['PLAYER'].isin(self.players_drafted)]['PRED'].sum()
            punt_scores[key] = score
        print(punt_scores)
        punts = sorted(punt_scores, key=punt_scores.get, reverse=True)[:3]
    
        return punts

    def best_guard(self, df):
        #get best guard, forward, and centre
        i = 0
        while df[(df['POS_PG'] == 1) | (df['POS_SG'] == 1)].iloc[i]['PLAYER'] in (self.players_drafted + self.other_players_drafted):
            i += 1

        return df[(df['POS_PG'] == 1) | (df['POS_SG'] == 1)].iloc[i]['PLAYER'] + ' - ' + str(round((df[(df['POS_PG'] == 1) | (df['POS_SG'] == 1)].iloc[i]['PRED']),2))

    def best_forward(self, df):
        #get best guard, forward, and centre
        i = 0
        while df[(df['POS_PF'] == 1) | (df['POS_SF'] == 1)].iloc[i]['PLAYER'] in (self.players_drafted + self.other_players_drafted):
            i += 1

        return df[(df['POS_PF'] == 1) | (df['POS_SF'] == 1)].iloc[i]['PLAYER'] + ' - ' + str(round((df[(df['POS_PF'] == 1) | (df['POS_SF'] == 1)].iloc[i]['PRED']),2))

    def best_centre(self, df):
        #get best guard, forward, and centre
        i = 0
        while df[(df['POS_C'] == 1)].iloc[i]['PLAYER'] in (self.players_drafted + self.other_players_drafted):
            i += 1

        return df[(df['POS_C'] == 1)].iloc[i]['PLAYER'] + ' - ' + str(round((df[(df['POS_C'] == 1)].iloc[i]['PRED']),2))

    # add player if they are available
    def add_player(self, entry, button):
        # check if player valid
        entry_status = self.check_player_valid(entry)
        if entry_status == 1: # if valid player entry
            if button == 1:
                self.players_drafted.append(entry)
                print('Drafted' + entry) # TODO convert this to message 
                self.l1.insert(tk.END, entry)
            else:
                self.other_players_drafted.append(entry)
                print('Drafted' + entry) # TODO convert this to message
                self.l2.insert(tk.END, entry)

            list.remove(entry)
            self.Update(list)
            self.refresh_matrix()

            return 1
            
        elif entry_status == - 1:
            print(entry + 'has already been drafted.') # TODO convert this to message
        else:
            print(entry + 'could not be found.') # TODO convert this to message
        return

    def check_player_valid(self, entry):
        status = 0
        if entry in self.base_df['PLAYER'].values:
            if (entry not in self.players_drafted) and (entry not in self.other_players_drafted):
                status = 1
            else:
                status = -1 
        return status

    # player matrix
    def refresh_matrix(self):
        df = self.refresh_list()
        # Add a Treeview widget
        tree = ttk.Treeview(self, column=('Punt Type',"Guard", "LName", "Roll No"), show='headings', height=5)

        tree.column("# 1", anchor=tk.CENTER)
        tree.heading("# 1", text="Punt Type")
        tree.column("# 2", anchor=tk.CENTER)
        tree.heading("# 2", text="Guard")
        tree.column("# 3", anchor=tk.CENTER)
        tree.heading("# 3", text="Forward")
        tree.column("# 4", anchor=tk.CENTER)
        tree.heading("# 4", text="Centre")
        
        # Insert the data in Treeview widget
        
        if len(self.players_drafted) != 0:
            tree.insert('', 'end', text="1", values=(df.iloc[0,0], df.iloc[0,1], df.iloc[0,2], df.iloc[0,3]))
            tree.insert('', 'end', text="1", values=(df.iloc[1,0], df.iloc[1,1], df.iloc[1,2], df.iloc[1,3]))
            tree.insert('', 'end', text="1", values=(df.iloc[2,0], df.iloc[2,1], df.iloc[2,2], df.iloc[2,3]))
        else:
            tree.insert('', 'end', text="1", values=(df.iloc[0,0], df.iloc[0,1], df.iloc[0,2], df.iloc[0,3]))

        tree.grid(row=8, column=0)

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
        tk.Listbox.delete(0, 'end')
        # put new data
        for item in data:
            tk.Listbox.insert('end', item)

    def drafted_by_me(self):
        player = tk.Listbox.get(tk.Listbox.curselection())
        self.add_player(player, 1)

    def drafted_by_other(self):
        player = tk.Listbox.get(tk.Listbox.curselection())
        self.add_player(player, 2)

if __name__ == "__main__":
    root = tk.Tk()
    Application(root)
    root.mainloop()