import json
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator Project


letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generate_password():
    password_entry.delete(0, END)
    password_list = (([choice(letters) for _ in range(randint(8, 10))] +
                      [choice(symbols) for _ in range(randint(2, 4))]) +
                     [choice(numbers) for _ in range(randint(2, 4))])
    shuffle(password_list)
    password = "".join(password_list)
    print(f"Your password is {password}")
    password_entry.insert(0, f"{password}")
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if website == "" or email == "" or len(password) == 0:
        messagebox.showinfo(title="Oops", message="fields empty !")
    else:
        # messagebox.showinfo(title="Title", message="message")
        is_ok = messagebox.askokcancel(title=website,
                                       message=f"It's ok to save these details? \nemail: {email}"
                                               f" \npassword: {password}")

        if is_ok:
            # with open("data.txt", "a") as data:
            #     data.write(f"{website} | {email} | {password}\n")

            try:
                with open("data.json", "r") as data_file:
                    # Reading old data
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                # Updating old data with new data
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    # Saving updated data
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, "end")
                password_entry.delete(0, END)
                website_entry.focus()


# ---------------------------- Find PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Oops", message="No Data File Found")
    else:
        if website in data:
            messagebox.showinfo(title=f"{website} Login infos: ", message=f"email = {data[website]["email"]}\n"
                                                                          f"password = {data[website]["password"]}")
        else:
            messagebox.showinfo(title="Oops", message=f"No details for  {website} exists")


# ---------------------------- UI SETUP ------------------------------- #
def handle_focus(event):
    event.widget.insert(0, f"{pyperclip.paste}")


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)
logo_img = PhotoImage(file="logo.png")
canvas = Canvas(width=200, height=200, highlightthickness=5, highlightbackground="black")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website: ")
website_label.grid(column=0, row=1)
email_label = Label(text="Email/Username: ")
email_label.grid(column=0, row=2)
password_label = Label(text="Password: ")
password_label.grid(column=0, row=3)

# Entries
website_entry = Entry(width=32)
website_entry.grid(column=1, row=1, columnspan=1)
website_entry.focus()

email_entry = Entry(width=50)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, "example@email.com")
password_entry = Entry(width=32)
password_entry.grid(column=1, row=3)

search_btn = Button(text="Search", width=14, command=find_password)
search_btn.grid(column=2, row=1)
generate_password_btn = Button(text="Generate Password", command=generate_password)
generate_password_btn.grid(column=2, row=3)
add_btn = Button(text="Add", width=40, command=save)
add_btn.grid(column=1, row=4, columnspan=2)

window.mainloop()
