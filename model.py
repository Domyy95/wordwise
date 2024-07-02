import json
import random
from datetime import datetime, timedelta
from typing import Tuple


class Word:
    def __init__(self, word: str, meanings: list, notes: str|None, pav: str|None):
        self.word = word
        self.meanings = meanings
        self.notes = notes 
        self.pav = pav

    def __str__(self):
        str_meanings = '; '.join(self.meanings)
        str_final = f"\nWord: {self.word} \nMeaning: {str_meanings}"
        str_final += f"\nNote: {self.notes}" if self.notes else ""
        str_final += f"\nPAV: {self.pav}" if self.pav else ""
        return str_final 

    def __repr__(self):
        str_meanings = ', '.join(self.meanings)
        str_final = f"{self.word} {str_meanings}"
        str_final += f" {self.notes}" if self.notes else ""
        str_final += f" {self.pav}" if self.pav else ""
        return str_final
    
    def to_dict(self):
        result = {
            "word": self.word,
            "meanings": self.meanings
        }   
        if self.notes:
            result["notes"] = self.notes
        if self.pav:
            result["pav"] = self.pav

        return result
    

class Dictionary:
    def __init__(self, file_name:str):
        file = json.load(open(file_name))

        result = {}
        for date in file:
            result[date] = []
            for word in file[date]:
                word_obj = Word(word["word"], list(word["meanings"]), word.get("notes"), word.get("pav"))
                result[date].append(word_obj)

        self.dictionary = result 

    def print_all_words(self):
        for date in self.dictionary:
            print(date)
            for word in self.dictionary[date]:
                print(str(word))

    def save_file_model(self, file_name:str):
        result = {}
        for date in self.dictionary:
            result[date] = []
            for word in self.dictionary[date]:
                result[date].append(word.to_dict())

        with open(file_name, "w") as file:
            json.dump(result, file, indent=4)

    def _add_word(self, date:str, word:Word):
        if date not in self.dictionary:
            self.dictionary[date] = []
        self.dictionary[date].append(word)

    def add_word(self, date:str, word_name:str, meanings:list, notes= None, pav= None):
        new_word = Word(word_name, meanings, notes, pav)
        self._add_word(date, new_word)

    def remove_word(self, date:str, word:str):
        word = word.lower()
        if date in self.dictionary:
            for i, word_d in enumerate(self.dictionary[date]):
                if word_d.word.lower() == word:
                    del self.dictionary[date][i]
                    break
        
        else:
            print("Date not found")
        
    def update_word(self, date:str, word:Word):
        if date in self.dictionary:
            for i in range(len(self.dictionary[date])):
                if self.dictionary[date][i].word == word.word:
                    self.dictionary[date][i] = word
                    break

    def get_date_words(self, date:str) -> list[Word]:
        return self.dictionary.get(date, [])
    
    def get_n_days_ago_words(self, n:int) -> list[Word]:
        today = datetime.now().date()
        days_ago = today - timedelta(n)
        days_ago_str = days_ago.strftime('%Y-%m-%d')
        
        return self.get_date_words(days_ago_str)
    
    def get_all_dates(self) -> list[str]:
        return list(self.dictionary.keys())
    
    def get_random_word(self) -> list[Word]:
        random_date = random.choice(self.get_all_dates())
        random_word = random.choice(self.dictionary[random_date])
        return (random_word)
    
    def get_last_n_dates_words(self, n:int) -> list[Word]:
        all_dates = self.get_all_dates()
        all_dates.sort(reverse=True)
        result = []
        for date in all_dates[:n-1]:
            result += self.get_date_words(date)
            
        return result

        