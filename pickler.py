import pygame 
import sky 
from consts import *
from pickle import load, dump


#[{"titles":[movie], "data":[(rating, url)]}, [account name, account avatar], first time, version]
class Pickler:
    def __init__(self):
        self.account = None
        
    def get_first_time(self):
        with open(P_SAVE, "rb") as f:
            return load(f)[2]
    
    def change_first_time(self):
        with open(P_SAVE, "rb") as f:
            save = load(f)
            save[2] = False
        with open(P_SAVE, "wb") as f:
            dump(save, f)
        
    def change_rating(self, title, rating):
        index = self.titles.index(title)
        self.data[index] = (rating, self.data[index][1])
        self.update_save()
        self.list.load()
        
    def get_rating(self, title):
        index = self.titles.index(title)
        return self.data[index][0]
            
    def open_account(self, index):
        with open(P_SAVE, "rb") as f:
            account = load(f)[0][index]
            self.titles = account["titles"]
            self.data = account["data"]
            self.account = index
            
    def get_accounts(self):
        with open(P_SAVE, "rb") as file:
            return load(file)[1]
            
    def update_save(self):
        with open(P_SAVE, "rb") as file:
            save = load(file)
        save[0][self.account] = {"titles":self.titles,
                                 "data":self.data}
        with open(P_SAVE, "wb") as file:
            dump(save, file)
        
    def reset(self):
        with open(P_SAVE, "wb") as file:
            dump([[], [], True, VERSION], file)
            
    def add_account(self, name, avatar):
        with open(P_SAVE, "rb") as file:
            save = load(file)
        with open(P_SAVE, "wb") as file:
            save[0].append({"titles":[],
                            "data":[]})
            save[1].append((name, avatar))
            dump(save, file)
                         
    def remove_account(self, index):
        with open(P_SAVE, "rb") as file:
            save = load(file)
            del save[0][index]
            del save[1][index]
        with open(P_SAVE, "wb") as file:
            dump(save, file)
        
    def add_title(self, title, rating, link):
        self.titles.append(title)
        self.data.append((rating, link))
        self.update_save()
        self.list.load()
            
    def remove_title(self, title):
        index = self.titles.index(title)
        del self.titles[index]
        del self.data[index]
        self.update_save()
        self.list.load()
        
    def contains(self, link):
        for i in self.data:
            if i[1] == link:
                return True 
        return False
        
    def show(self):
        with open(P_SAVE, "rb") as file:
            print(load(file))
            
    def pickle_changelog(self):
        with open("changelog.txt") as txt:
            with open(P_CHANGELOG, "wb") as p:
                dump([line.strip() for line in txt.readlines()], p)

    def get_changelog(self):
        with open(P_CHANGELOG, "rb") as f:
            return load(f)