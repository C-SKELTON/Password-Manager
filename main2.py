import json
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import pyperclip

MY_FONT = "Times New Roman", 11, "bold"



#----------------------------- Search Website ----------------------------------- #
def find_password():
    website = web_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
            user_email = data[website]['email']
            user_pass = data[website]['password']
            messagebox.showinfo(title=f"{website}", message=f"Email: {user_email} \nPassword: {user_pass}")
            window.clipboard_clear()
            window.clipboard_append(user_pass)
    except KeyError:
        if len(website) == 0:
            messagebox.showerror(title="Error", message=f"Please enter a website.")
        else:
            messagebox.showerror(title="Error", message=f"No Details for {website} exists.")

    except json.JSONDecodeError:
        messagebox.showerror(title="Error", message="No Data File Found.")

    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found.")



# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    password_list += [random.choice(letters) for letter in range(nr_letters)]
    password_list += [random.choice(symbols) for symbol in range(nr_symbols)]
    password_list += [random.choice(numbers) for number in range(nr_numbers)]

    random.shuffle(password_list)

    password = "".join(password_list)
    pass_entry.insert(tk.END, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():

    website = web_entry.get()
    email = email_entry.get()
    password = pass_entry.get()
    new_data = {
        website: {
        "email": email,
        "password": password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showerror(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("data.json", "r") as data_file:
                #Reading old data
                data = json.load(data_file)
                #Updating old data
                data.update(new_data)
            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        except json.JSONDecodeError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        finally:
            web_entry.delete(0, tk.END)
            pass_entry.delete(0, tk.END)
#json.dump(new_data, data_file, indent=2) writing to the json file
# ---------------------------- UI SETUP ------------------------------- #

window = tk.Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, background="black")


mycanvas = tk.Canvas(width=200, height=200, bg="black", highlightthickness=0)
logo_img = tk.PhotoImage(file="logo.png")
mycanvas.create_image(100, 100, image=logo_img)
mycanvas.grid(column=1, row=0)


#website_text
web_text = ttk.Label(text="Website: ", font=(MY_FONT), background="black", foreground="#DC7260", width=10)
web_text.grid(column=0, row=1)

#email_username_text
email_text = ttk.Label(text="Email/Username: ", font=(MY_FONT), background="black", foreground="#DC7260", width=15)
email_text.grid(column=0, row=2)

#password_text
password_text = ttk.Label(text="Password: ", font=(MY_FONT), background="black", foreground="#DC7260", width=10)
password_text.grid(column=0, row=3)

#password_button
password_button =tk.Button(text="Generate Password", highlightthickness=0, width=14, command=generate_password, bg="#DC7260", fg="#151515", font=(MY_FONT))
password_button.grid(column=2, row=3, sticky="ew")

#search_button
search_button =tk.Button(text="Search", highlightthickness=0, width=14, command=find_password, bg="#DC7260", fg="#151515", font=(MY_FONT))
search_button.grid(column=2, row=1, sticky="ew")

#add_button
add_button =tk.Button(text="Add", width=43, highlightthickness=0, command=save, bg="#DC7260", fg="#151515", font=(MY_FONT))
add_button.grid(column=1, row=4, columnspan=2, sticky="ew")

#password_entry
pass_entry = tk.Entry(width=41, bg="#6B6D6C", fg="#d3d3d3")
pass_entry.grid(column=1, row=3, sticky="w")

#email_username entry
email_entry = tk.Entry(width=42, bg="#6B6D6C", fg="#d3d3d3")
email_entry.insert(tk.END, "connor@gmail.com")
email_entry.grid(column=1, row=2, columnspan=2, sticky="ew")

#website_entry
web_entry = tk.Entry(width=41, bg="#6B6D6C", fg="#d3d3d3")
web_entry.focus()
web_entry.grid(column=1, row=1, sticky="w")


window.mainloop()