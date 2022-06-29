from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")



# ---------------------------Create Flash Cards---------------------------#
def create_cards():
    global current_card, timer
    window.after_cancel(timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(title, text="French", fill="white")
    canvas.itemconfig(word, text=current_card["French"], fill="white")
    canvas.itemconfig(card_background, image=back_card_img)
    timer = window.after(3000, func=flip_card)


# ---------------------------Flip Card---------------------------#
def flip_card():
    canvas.itemconfig(card_background, image=front_card_img)
    canvas.itemconfig(word, text=current_card['English'], fill="black")
    canvas.itemconfig(title, text="English", fill="black")


# ---------------------------Pass word---------------------------#
def pass_word():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    create_cards()


# ---------------------------UI---------------------------#
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

timer = window.after(3000, func=flip_card)

# Flashcard
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)
front_card_img = PhotoImage(file="images/card_front.png")
back_card_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=back_card_img)
title = canvas.create_text(400, 150, text="", fill="white", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 263, text="", fill="white", font=("Ariel", 60, "bold"))

# Buttons
x_img = PhotoImage(file="images/wrong.png")
checkmark_img = PhotoImage(file="images/right.png")

wrong_button = Button(image=x_img, highlightthickness=0, command=create_cards)
wrong_button.grid(row=1, column=0)
right_button = Button(image=checkmark_img, highlightthickness=0, command=pass_word)
right_button.grid(row=1, column=1)

create_cards()
window.mainloop()
