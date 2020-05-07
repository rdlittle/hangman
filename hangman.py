import tkinter as tk
from tkinter import BooleanVar, Button, Canvas, Entry, Frame, Label, StringVar, messagebox
import random
from images import Picture
import pdb
import sys
from themes import themes

theme = themes['sea']

class Game():
    def __init__(self, parent):
        
        self.theme_var = StringVar()
        self.theme_var.trace('w', self.set_theme)
        
        main_menu = tk.Menu(parent)
        theme_menu = tk.Menu(main_menu, tearoff=False)

        for key in themes.keys():
            theme_menu.add_radiobutton(label=key.capitalize(), value=key, variable=self.theme_var)

        main_menu.add_cascade(label="Theme", menu=theme_menu)
        parent.configure(menu=main_menu)
        
        button_spacing = 1
        if sys.platform[:3] == 'win':
            button_spacing = 6
        self.drawing = {
            'base': [100, 199, 200, 199],
            'upright': [150, 20, 150, 200],
            'top': [75, 20, 150, 20],
            'rope': [75, 20, 75, 40],
            'head': [65, 40, 85, 55],
            'body': [75, 55, 75, 90],
            'left_arm': [75, 75, 50, 60],
            'right_arm': [75, 75, 100, 60],
            'left_leg': [75, 90, 70, 125],
            'right_leg': [75, 90, 80, 125]
        }
        
        self.alphabet = ['A', 'B', 'D', 'C', 'E', 'F', 'G',
            'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 
            'Q', 'R', 'S', 'T', 'U', 'V', 
            'W', 'X', 'Y', 'Z']
        
        self.vowels = ['A', 'E', 'I', 'O', 'U']
        
        self.tally = {
            'right': 0,
            'wrong': 0,
            'credit': 0,
            'only_vowels': False,
            'msg_shown': False
        }
        
        self._guessed_word = StringVar()
        self._right = StringVar()
        self._wrong = StringVar()
        self._credits = StringVar()
        
        self._right.set(0)
        self._wrong.set(0)
        self._credits.set(0)
        
        self._parent = parent
        self._letter_box = []
        self._used_words = []
        self._word_list = []
        self._used_letters = []
        self._letter_buttons = {}
        
        # Define top-level child frames
        self._header_frame = Frame(self._parent)
        self._word_frame = Frame(self._parent)
        self._button_frame = Frame(self._parent)
        self._action_frame = Frame(self._parent)
        
        # Define child panels of word_frame
        self._canvas_panel = Frame(self._word_frame)
        self._word_panel = Frame(self._word_frame)
        self._score_panel = Frame(self._word_frame)
        
        self._letters_panel = Frame(self._word_panel)
        
        self._header_frame.columnconfigure(0, weight=2)
        self._word_frame.columnconfigure(0, weight=1, uniform='center')
        self._word_frame.columnconfigure(1, weight=1, uniform='center')
        self._word_frame.columnconfigure(2, weight=1, uniform='center')
        
        self._action_frame.configure(height=50)

        # Place the top-level child frames
        self._header_frame.grid(column=0, row=0, sticky=tk.W+tk.E)
        self._word_frame.grid(column=0, row=1, pady=20, sticky=tk.W+tk.E)
        self._button_frame.grid(column=0, row=2, ipady=20, sticky=tk.W+tk.E)
        self._action_frame.grid(column=0, row=3, pady=20)
        
        # Place the 2nd level child panels
        self._canvas_panel.grid(column=0, row=0)
        self._word_panel.grid(column=1, row=0)
        self._score_panel.grid(column=2,row=0)
        self._letters_panel.grid(column=0, row=0, sticky=tk.E) # child of word_panel
        
        self._canvas = Canvas(self._canvas_panel, height=200, width=200)
        self._canvas.grid(column=0, row=1, pady=20, padx=10, sticky=tk.W)
        
        self._header = Label(self._header_frame, text='UniVerse Keywords', font='-size 20')
        self._header.grid(column=0, row=0)
        
        self._right_lbl = Label(self._score_panel, text='Right', font='-size 18')
        self._right_holder = Label(self._score_panel)
        self._right_holder.configure(font='-size 18', textvariable=self._right)
        
        self._wrong_lbl = Label(self._score_panel, text='Wrong', font='-size 18')
        self._wrong_holder = Label(self._score_panel)
        self._wrong_holder.configure(font='-size 18', textvariable=self._wrong)
        
        self._credit_lbl = Label(self._score_panel, text='Credits', font='-size 18')
        self._credit_holder = Label(self._score_panel)
        self._credit_holder.configure(font='-size 18', textvariable=self._credits)
        
        self._right_lbl.grid(column=0, row=0, padx=20, sticky=tk.W)
        self._right_holder.grid(column=1, row=0)
        self._wrong_lbl.grid(column=0, row=1, padx=20, sticky=tk.W)
        self._wrong_holder.grid(column=1, row=1)        
        self._credit_lbl.grid(column=0, row=2, padx=20, sticky=tk.W)
        self._credit_holder.grid(column=1, row=2)
                
        if len(self._word_list) == 0:
            with open('UV_Reserved_Words.txt', 'rt') as text_file:
                for word in text_file:
                    if len(word) > 3:
                        self._word_list.append(word.strip())

        for idx in range(len(self.alphabet)):
            self._letter_buttons[idx] = Button(self._button_frame, text=self.alphabet[idx])
            self._letter_buttons[idx].configure(command = lambda l=self.alphabet[idx],btn=self._letter_buttons[idx]: self.use_letter(l, btn))
            self._letter_buttons[idx].grid(row=0, column=idx, padx=button_spacing)
            
        self._guess_entry = Entry(self._action_frame, textvariable=self._guessed_word)
        self._guess_entry.bind('<Return>', self.guess_word)
        self._guess_entry.grid(column=0, row=1, padx=10)
        
        self._guess_button = Button(self._action_frame, text='Guess')
        self._guess_button.configure(command=self.guess_word)
        self._guess_button.grid(column=2, row=1, padx=10)
        
        self._new_game_button = Button(self._action_frame, text='New Game')
        self._new_game_button.configure(command=self.new_game)
        self._new_game_button.grid(column=3, row=1, padx=10)
        
        self._give_up_button = Button(self._action_frame, text='I Give Up')
        self._give_up_button.configure(command=self.give_up)
        self._give_up_button.grid(column=4, row=1, padx=10)
        
        self._buy_vowel_button = Button(self._action_frame, text='Buy a Vowel')
        self._buy_vowel_button.configure(command=self.buy_vowel, state='disabled')
        self._buy_vowel_button.grid(column=5, row=1, padx=10)
        self._buy_vowel_button
        
        self._credits.trace('w', self.check_credit)
        try:
            with open('theme.txt', 'rt') as tfile:
                t = tfile.readline()
        except:
            t = 'sea'
        with open('theme.txt', 'wt') as tfile:
            tfile.write(t)
        
        self.theme_var.set(t)
       
        self.new_game()
            
    def announce(self, winner_loser):
        self.clear_canvas()
        if winner_loser not in ['winner', 'loser']:
            return

        if winner_loser == 'loser':
            msg = "You're dead\nYou're dead\nYou're dead\nAnd not of this world"
            image_name = 'loser.gif'
            self.tally['wrong'] += 1
            self._wrong.set(str(self.tally['wrong']))
        else:
            msg = 'You\'re a winner'
            image_name = 'winner.gif'
            self.tally['right'] += 1
            self._right.set(str(self.tally['right']))
            
        l = Picture(self._canvas, image_name)
        messagebox.showinfo(message=msg)
        self.new_game()
        
    def apply_theme(self):
        global theme
        self._parent.configure(bg=theme['dark'])
        self._header_frame.configure(bg=theme['medium'])
        self._button_frame.configure(bg=theme['accent'])
        self._action_frame.configure(bg=theme['dark'])
        
        self._word_frame.configure(bg=theme['light'])
        self._letters_panel.configure(bg=theme['light'])
        self._canvas_panel.configure(bg=theme['light'])
        self._score_panel.configure(bg=theme['light'])
        
        self._canvas.configure(bg=theme['light'],highlightbackground=theme['dark'])
        self._right_holder.configure(bg=theme['light'])
        self._wrong_holder.configure(bg=theme['light'])
        self._credit_holder.configure(bg=theme['light'])
        self._header.configure(bg=theme['medium'])
        self._right_lbl.configure(bg=theme['light'])
        self._wrong_lbl.configure(bg=theme['light'])
        self._credit_lbl.configure(bg=theme['light'])
        for lbl in self._letter_box:
            lbl.configure(bg=theme['light'])
            
    def buy_vowel(self):
        self.toggle_vowel_buttons('normal')
        self.tally['credit'] -= 1
        if self.tally['credit'] < 0:
            self.tally['credit'] = 0
        self._credits.set(str(self.tally['credit']))
        
    def check_done(self):
        #pdb.set_trace()
        self.tally['only_vowels'] = True
        for l in self._secret_word:
            if l not in self.vowels and l not in self._used_letters:
                self.tally['only_vowels'] = False
                break
        if self._tries == len(self.drawing):
            return True
        for lbl in self._letter_box:
            txt = lbl.cget('text')
            if txt == '_':
                return False   
        return True
    
    def check_credit(self, *args):
        c = int(self._credits.get())
        bstate = 'disabled'
        if c > 0:
            bstate = 'normal'
        self._buy_vowel_button.configure(state=bstate)
        
    def clear_canvas(self):
        items = self._canvas.find_all()
        for item in items:
            self._canvas.delete(item)
            
    def draw_figure(self):
        try:
            k = next(self.seg_iterator)
            if k == 'head':
                self._canvas.create_oval(self.drawing[k])
            else:
                self._canvas.create_line(self.drawing[k])
            self._tries += 1
        except StopIteration:
            self.announce('loser')
            
    def get_segment(self):
        for k in self.drawing.keys():
            yield k
    
    def get_word(self):
        while True:
            if len(self._word_list) == len(self._used_words):
                return None
            word = self._word_list[random.randrange(0,len(self._word_list)-1)]
            if word not in self._used_words:
                self._used_words.append(word)
                #print(word)
                return word
            
    def give_up(self):
        self.tally['wrong'] += 1
        self._wrong.set(str(self.tally['wrong']))
        
        self.reveal()
        for btn in self._letter_buttons.values():
            btn.configure(state='disabled')
   
    def guess_word(self, *args):
        word = self._guessed_word.get().upper()
        if word == '':
            return
        if word == self._secret_word:
            self.reveal()
            self._guessed_word.set('')
            self.announce('winner')
        else:
            messagebox.showinfo(message='Wrong!')
            self._guessed_word.set('')
            self.tally['credit'] -= 1
            '''Should we allow negative credits?'''
            self._credits.set(str(self.tally['credit']))
            self.draw_figure()
            if self.check_done():
                self.announce('loser')
    
    def new_game(self):
        global theme
        for lbl in self._letter_box:
            lbl.grid_remove()
        self.seg_iterator = self.get_segment()
        self._letters = []
        self._used_letters = []
        self._letter_box = []
        self._tries = 0
        self._secret_word = self.get_word()
        self.tally['credit'] = 0
        self.tally['only_vowels'] = False
        self.tally['msg_shown'] = False
        self._credits.set(0)
        
        for idx,btn in self._letter_buttons.items():
            txt = btn.cget('text')
            if txt in self.vowels:
                btn.configure(state='disabled')
            else:
                btn.configure(state='normal')
        for l in range(len(self._secret_word)):
            text = '_'
            if self._secret_word[l] == '.':
                text = '.'
            lbl = Label(self._letters_panel, text=text)
            lbl.configure(font='-size 14', bg=theme['light'])
            lbl.grid(column=l+1, row=1, padx=4)
            self._letter_box.append(lbl)
        self.clear_canvas()
                
    def reveal(self):
        for t in range(len(self._secret_word)):
            self._letter_box[t].configure(text=self._secret_word[t])
            
    def set_theme(self, *args):
        global theme
        t = self.theme_var.get().lower()
        with open('theme.txt', 'wt') as file:
            file.write(t)
            
        if t in themes.keys():
            theme = themes[t] 
            self.apply_theme()
            
    def toggle_vowel_buttons(self, set_state='disabled'):
        cons_state = 'normal'
        if set_state == 'normal':
            cons_state = 'disabled'
        for idx in range(len(self.alphabet)):
            button = self._letter_buttons[idx]
            if self.alphabet[idx] in self._used_letters:
                continue
            if self.alphabet[idx] in self.vowels:
                button.configure(state=set_state)
            else:
                button.configure(state=cons_state)   
    
    def use_letter(self, letter, button):
        button.configure(state='disabled')
        self._used_letters.append(letter)
        self.toggle_vowel_buttons()
        
        if letter in self._secret_word:
            self.tally['credit'] += 1
            self._credits.set(str(self.tally['credit']))
            for l in range(len(self._secret_word)):
                if self._secret_word[l] == letter:
                    self._letter_box[l].configure(text=letter)
            if self.check_done():
                self.announce('winner')
        else:
            self.draw_figure()
            if self.check_done():
                self.reveal()
                self.announce('loser')
                
        if self.tally['only_vowels']:
            if not self.tally['msg_shown']:
                self.tally['msg_shown'] = True
                messagebox.showinfo(message="Only vowels remain")
                for btn in self._letter_buttons.values():
                    btn.configure(state='disabled')
    

class GameBoard(tk.Tk):
    def __init__(self, *args, **kwargs):
        super(GameBoard, self).__init__(*args, **kwargs)
        geo_string = '1000x475+350+100'
        if sys.platform[:3] == 'win':
            geo_string = '790x450+350+100'
        self.geometry(geo_string)
        self.title('Cheat the Hangman')
        Game(self)
        
        
def main():
    app = GameBoard()
    app.mainloop()


if __name__ == '__main__':
    main()
