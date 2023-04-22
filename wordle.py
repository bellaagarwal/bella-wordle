import tkinter
import random
import tkinter.messagebox

dark_grey = "#777b7d"
yellow = "#c9b458"
green = "#6aaa64"
light_grey = "#d3d6da"
white = "#ffffff"
black = "#000000"

class Button:      
    def colorChange(self,color):
        if color == light_grey:
            self.button.configure(bg=color,fg=black)  
        else:
            self.button.configure(bg=color,fg=white)  

    def letterChoose(self,row:int,column:int):
        return [x for x in self.form.letters if x.row == row and x.column == column][0]
		
    def chooseWord(self,row:int):
        letters = [x.square["text"] for x in self.form.letters if x.row == row and x.column <= 5]
        return "".join(letters)

    def currentRowColor(self,target:str,word:str,row:int):
        newWord = ""
        new_target = ""

        for pos in range(0,5):
            if word[pos] == target[pos]:
                newWord += "*"
                new_target += "*"
            else:
                newWord += word[pos]
                new_target += target[pos]

        newest_target = ""
        for pos in range(0,5):

            letter = new_target[pos]
            if letter != "*":

                for this_postion, guess_letter in enumerate(newWord):
                    if guess_letter == letter:
                        newWord = newWord[:this_postion] + "?" + newWord[this_postion+1:]
                        break

                
        for pos in range(0,5):

            letter = newWord[pos]            
            this_letter = self.letterChoose(row,pos + 1)

            if letter == "*":                        
                this_letter.colorChange(green)
            elif letter == "?":
                this_letter.colorChange(yellow)
            else:
                this_letter.colorChange(dark_grey)

        if newWord.count("*") == 5:
            tkinter.messagebox.showinfo("Congratulations!","Congratulations you won!")
        else:
            if row >= 6:
                tkinter.messagebox.showinfo(
                    "End of game",
                    "Out of guesses!"
                )
				
    def letterColorButton(self,guesses,buttons):
        letterGuess = "".join(guesses).upper()
        letterGuess = list(set(letterGuess))

        for button in buttons:
            if button.letter not in letterGuess:
                continue

            # if it's been guessed but isn't in target word, color it dark grey
            if button.letter not in targetChooseWord().upper():
                button.colorChange(dark_grey)
                continue
            correct_pos = targetChooseWord().find(button.letter)

            if_green = False
            for guess in guesses:
                if guess[correct_pos].upper() == button.letter.upper():
                    if_green = True
                    break

            if if_green:
                button.colorChange(green)
            else:
                button.colorChange(yellow)

            continue	

    def ok_clicked(self):
        if self.letter.lower() == "enter":
            if self.form.current_column > 5:

                this_word = self.chooseWord(self.form.current_row).lower()

               # self.currentRowColor(self.form.targetChooseWord().upper(),this_word.upper(),self.form.current_row)

                self.form.current_column = 1
                self.form.current_row += 1
                
                self.form.guesses.append(this_word)

                self.letterColorButton(self.form.guesses,self.form.letter_buttons)

            return

        # if we're on column 6, nothing to do
        if self.form.current_column > 5:
            return

        # shouldn't be possible, but can't choose letters after row 6
        if self.form.current_row > 6:
            return

        # show this letter has been clicked
        # self.colorChange(dark_grey)

        # select the next letter, and move on one
        current_letter = self.letterChoose(self.form.current_row,self.form.current_column)
        current_letter.square["text"] = self.letter
        current_letter.colorChange(light_grey)

        # move on to next column
        self.form.current_column += 1

    def __init__(self,form,*,left:int,top:int,width:int,letter:str):

        self.id = "button_" + letter.lower()
        self.form = form
        self.letter = letter
        self.button = tkinter.Button(
            form,
            text=letter,
            command=self.ok_clicked,
            width=width,
            height=2,
            relief="flat"
        )

        # color it
        self.colorChange(light_grey)
        self.button
        self.button["padx"] = 5
        self.button["pady"] = 5
        self.button.place(x=left, y=top+370)

class Letter:
    def colorChange(self,color):
        if color == light_grey:
            self.square.configure(bg=color,fg=black)  
        else:
            self.square.configure(bg=color,fg=white)  

    def __init__(self,form,*,left:int,top:int,row:int,col:int):
        self.row = row
        self.column = col
        self._letter = None
        
        self.square = tkinter.Label(
            form,
            font=("Arial", 10, "bold"),
            text="",    #"X{0}{1}".format(row,col) ,
            width=8,
            height=4,
            borderwidth=1,
            relief="ridge",
            anchor="center"
        )

        self.colorChange(white)

        self.square
        self.square.place(x=left, y=top)

def create_main_window():

    wordle_form = tkinter.Tk()

    wordle_form.title("Bella's Wordle")
    form_width = 600
    form_height = 700

    screen_width = wordle_form.winfo_screenwidth()
    screen_height = wordle_form.winfo_screenheight()

    horizontal_offset = \
        int((screen_width/2) - (form_width/2))
    vertical_offset = \
        int((screen_height/2) - (form_height/2))
    wordle_form.geometry('{0}x{1}+{2}+{3}'.format(form_width,form_height,horizontal_offset,vertical_offset))
    wordle_form.resizable(False,False)

    return wordle_form

def add_letter_buttons(wordle_form):
        
    letter_buttons = []

    first_row = "QWERTYUIOP"
    second_row = "ASDFGHJKL"
    third_row = "ZXCVBNM"
    start_top = 130

    start_left = 45
    for letter in first_row:
        letter_buttons.append(Button(wordle_form,left=start_left,top=start_top,width=4,letter=letter))
        start_left += 50

    start_left = 70
    for letter in second_row:
        letter_buttons.append(Button(wordle_form,left=start_left,top=start_top + 55,width=4,letter=letter))
        start_left += 50
        
    letter_buttons.append(Button(wordle_form,left=50,top=start_top + 110,width=7,letter="ENTER"))

    start_left = 120
    for letter in third_row:
        letter_buttons.append(Button(wordle_form,left=start_left,top=start_top + 110,width=4,letter=letter))
        start_left += 50
    return letter_buttons

def add_letters(wordle_form):
    letters = []

    for r in range(1,7):
        for c in range(1,6):
            letters.append(Letter(wordle_form,left=45 + c * 70,top= -30 + r * 70,row=r,col=c)
        )

    return letters

def targetChooseWord():
    words = []
    with open('LOW.txt') as f:
        listofwords = [lines.rstrip() for lines in f]
    for i in range(len(listofwords)):
        selected = listofwords[i]
        words.append(selected)
    return random.choice(words)


wordle_form = create_main_window()
wordle_form.letter_buttons = add_letter_buttons(wordle_form)
wordle_form.letters = add_letters(wordle_form)
wordle_form.current_row = 1
wordle_form.current_column = 1
wordle_form.guesses = []
wordle_form.mainloop() 