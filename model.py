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
    
    def _find_word(self, date, word) -> Tuple[Word, int] | int | None:
        """
            Returns a tuple with the word object and its index in the list of words of the date.
            returns 0 if the date does not exist.
            returns None if the word does not exist.
        """
        if date in self.dictionary:
            for i, word_d in enumerate(self.dictionary[date]):
                if word_d.word.lower() == word:
                    return (word_d, i)
            else:
                print(f"Word '{word}' not found on date '{date}'.")
                return None
        else:
            print(f"Date '{date}' not found.")
            return 0


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

    def remove_word(self, date: str, word: str):
        word = word.lower()

        word_d = self._find_word(date, word)
        if word_d:
            del self.dictionary[date][word_d[1]]
            print(f"Word '{word}' removed on date '{date}'.")


    def add_word_meaning(self, date: str, word: str, new_meaning: str):
        word = word.lower()
        word_d = self._find_word(date, word)
        if word_d:
            word_d[0].meanings.append(new_meaning)
            print(f"Meaning '{new_meaning}' added to word '{word}' on date '{date}'.")

    def reset_word_meanings(self, date:str, word:str, meanings:list):
        word = word.lower()
        word_d = self._find_word(date, word)
        if word_d:
            word_d[0].meanings = meanings
            print(f"Meanings reset for word '{word}' on date '{date}'.")

    def update_word_note(self, date:str, word:str, notes:str):
        word = word.lower()
        word_d = self._find_word(date, word)
        if word_d:
            word_d[0].notes = notes
            print(f"Notes updated for word '{word}' on date '{date}'.")

    def update_word_pav(self, date:str, word:str, pav:str):
        word = word.lower()
        word_d = self._find_word(date, word)
        if word_d:
            word_d[0].pav = pav
            print(f"PAV updated for word '{word}' on date '{date}'.")

    def get_date_words(self, date:str) -> list[Word]:
        return self.dictionary.get(date, [])
    
    def get_n_days_ago_words(self, n:int) -> list[Word]:
        today = datetime.now().date()
        days_ago = today - timedelta(n)
        days_ago_str = days_ago.strftime('%Y-%m-%d')
        
        return self.get_date_words(days_ago_str)
    
    def get_all_dates(self) -> list[str]:
        return list(self.dictionary.keys())
    
    def get_random_word(self) -> Tuple[str, Word]:
        random_date = random.choice(self.get_all_dates())
        random_word = random.choice(self.dictionary[random_date])
        return (random_date, random_word)
    
    def get_last_n_dates_words(self, n:int) -> list[Word]:
        all_dates = self.get_all_dates()
        all_dates.sort(reverse=True)
        result = []
        for date in all_dates[:n]:
            result += self.get_date_words(date)
            
        return result

        