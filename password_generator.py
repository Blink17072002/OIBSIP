import random
import string
from tkinter import *
from tkinter import messagebox


# Colors
co0 = "#444466" # Black
co1 = "#feffff" # White
co2 = "#6f9fbd" # Blue
co3 = "#f05a43" # Red

back_color = co1

root = Tk()
root.title('Random Password Generator')
root.geometry('500x360')
root.configure(bg=back_color)

# Creating frames
frame_main = Frame(root, width=500, height=110, bg=back_color)
frame_main.grid(row=0, column=0)

frame_box = Frame(root, width=500, height=220, bg=back_color)
frame_box.grid(row=1, column=0)

# App name
app_name = Label(frame_main, text='PASSWORD GENERATOR', width=20, height=1, padx=0, anchor="nw", font=('Ivy 14 bold'), bg=co1, fg=co0)
app_name.place(x=140, y=2)

app_line = Label(frame_main, width=500, height=1, padx=0, anchor="nw", font=('Aria 1'), bg=co3, fg=co1)
app_line.place(x=0, y=35)


# function to generate password
def generate_password():
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    numbers = '0123456789'
    symbols = "!@#$%^&*()_-+={}[]:>;',</?~|"

    combine = ""

    # Uppercase letters condition
    if state_1.get() == uppercase_letters:
        combine = uppercase_letters
    else:
        pass

    # Lowercase letters condition
    if state_2.get() == lowercase_letters:
        combine += lowercase_letters
    else:
        pass

    # Numbers condition
    if state_3.get() == numbers:
        combine += numbers    
    else:
        pass

    # Symbols condition
    if state_4.get() == symbols:
        combine += symbols   
    else:
        pass
    
    # Check if any character set is selected
    
    
    # Getting password length from user's spin
    length = int(spin.get())

    # Check if length is at least 4 characters
    if length < 4:
        messagebox.showwarning("Warning", "Password length must be at least 4 characters for security reasons")
        return
    
    if not combine:
        messagebox.showerror("Error", "Please select at least one character set")
        return

    
    password = "".join(random.sample(combine, length))
    app_password['text'] = password

    # Function to copy the password
    def copy_password():
        info = password
        frame_box.clipboard_clear()
        frame_box.clipboard_append(info)
        messagebox.showinfo("The password has been copied successfully.")

    b_copy = Button(frame_box, command=copy_password, text='Copy', width=7, overrelief=SOLID, bg=co1, fg=co0, font=('Ivy 10 bold'), anchor='center', relief=RAISED)
    b_copy.grid(row=0, column=2, sticky=NSEW, pady=10, columnspan=2)


# defining variables
lowercase_letters = string.ascii_lowercase
uppercase_letters = string.ascii_uppercase
numbers = '0123456789'
symbols = "!@#$%^&*()_-+={}[]:>;',</?~|"


# working in frame main
var = IntVar()
var.set(8)
app_info = Label(frame_main, text='Number of characters in password', height=1, padx=0, anchor="nw", font=('Ivy 10 bold'), bg=co1, fg=co0)
app_info.place(x=100, y=60)

# Spinbox
spin = Spinbox(frame_main, width=5, from_=0, to=20, textvariable=var)
spin.place(x=330, y=62)


# working in frame box
app_password = Label(frame_box, text='- - -', width=20, height=2, relief='solid', padx=0, anchor="center", font=('Ivy 10 bold'), bg=co1, fg=co0)
app_password.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=2, pady=10)


# Uppercase letters
app_info = Label(frame_box, text='Uppercase leters (ABC)', height=1, padx=0, anchor="nw", justify='center', font=('Ivy 10 bold'), bg=co1, fg=co0)
app_info.grid(row=1, column=1, sticky=NSEW, padx=2, pady=5)

state_1 = StringVar()
state_1.set(False)  # Set check state

check_1 = Checkbutton(frame_box, width=1, var=state_1, onvalue=uppercase_letters, offvalue='off', bg=back_color)
check_1.grid(row=1, column=0, sticky=NSEW, padx=2, pady=5)


# Lowercase letters
app_info = Label(frame_box, text='Lowercase leters (abc)', height=1, padx=0, anchor="nw", justify='center', font=('Ivy 10 bold'), bg=co1, fg=co0)
app_info.grid(row=2, column=1, sticky=NSEW, padx=2, pady=5)

state_2 = StringVar()
state_2.set(False)  # Set check state

check_2 = Checkbutton(frame_box, width=1, var=state_2, onvalue=lowercase_letters, offvalue='off', bg=back_color)
check_2.grid(row=2, column=0, sticky=NSEW, padx=2, pady=5)


# Numbers
app_info = Label(frame_box, text='Numbers (123)', height=1, padx=0, anchor="nw", justify='center', font=('Ivy 10 bold'), bg=co1, fg=co0)
app_info.grid(row=3, column=1, sticky=NSEW, padx=2, pady=5)

state_3 = StringVar()
state_3.set(False)  # Set check state

check_3 = Checkbutton(frame_box, width=1, var=state_3, onvalue=numbers, offvalue='off', bg=back_color)
check_3.grid(row=3, column=0, sticky=NSEW, padx=2, pady=5)


# Symbols
app_info = Label(frame_box, text='Symbols (!@#)', height=1, padx=0, anchor="nw", justify='center', font=('Ivy 10 bold'), bg=co1, fg=co0)
app_info.grid(row=4, column=1, sticky=NSEW, padx=2, pady=5)

state_4 = StringVar()
state_4.set(False)  # Set check state

check_4 = Checkbutton(frame_box, width=1, onvalue=symbols, offvalue='off', var=state_4, bg=back_color)
check_4.grid(row=4, column=0, sticky=NSEW, padx=2, pady=5)


# Generate password button
b_generate_password = Button(frame_box, command=generate_password, text='Generate password', width=32, overrelief=SOLID, bg=co3, fg=co1, font=('Ivy 10 bold'), anchor='center', relief=FLAT)
b_generate_password.grid(row=5, column=0, sticky=NSEW, padx=0, pady=20, columnspan=5)

root.mainloop()