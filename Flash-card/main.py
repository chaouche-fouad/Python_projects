from tkinter import *
from tkinter import messagebox

import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

# ---------------- Read data from french_words.csv -------------------- #
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    print(original_data)
    to_learn = original_data.to_dict(orient="records")
except pandas.errors.EmptyDataError:
    messagebox.showinfo(title="Oops", message="No words left!")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    try:
        current_card = random.choice(to_learn)
    except IndexError:
        messagebox.showinfo(title="Oops", message="No words left!")
        canvas.itemconfig(card_word, text="No words left!", fill="red")
    else:
        canvas.itemconfig(card_title, text="French", fill="black")
        canvas.itemconfig(card_word, text=current_card["French"], fill="black")
        canvas.itemconfig(card_background, image=card_front_img)
        flip_timer = window.after(3000, func=flip_card)
    # print(current_card["French"])


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


def is_known():
    try:
        to_learn.remove(current_card)
    except AttributeError:
        messagebox.showinfo(title="Oops", message="No words left!")
    except ValueError:
        messagebox.showinfo(title="Oops", message="No words left!")
    else:
        print(len(to_learn))
        data = pandas.DataFrame(to_learn)
        data.to_csv("data/words_to_learn.csv", index=False)

        next_card()


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Flash card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="Title", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="word", font=("Arial", 60, "bold"))
canvas.config(highlightthickness=0, highlightbackground="black", bg=BACKGROUND_COLOR)
canvas.grid(column=0, row=0, columnspan=2)

cross_img = PhotoImage(file="images/wrong.png")
unknown_btn = Button(image=cross_img, highlightthickness=0, command=next_card)
unknown_btn.grid(column=0, row=1)

check_img = PhotoImage(file="images/right.png")
known_btn = Button(image=check_img, highlightthickness=0, command=is_known)
known_btn.grid(column=1, row=1)

next_card()

window.mainloop()
