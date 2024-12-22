import csv
from tkinter import *
from tkinter import ttk
import subprocess
from functools import partial

# Function to write user data to a file
def write_user_data(username, password, country, state, role):
    with open('user_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username.strip(), password, country, state, role])  # Strip whitespaces from username

# Function to read user data from the file
def read_user_data():
    users = {}
    try:
        with open('user_data.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and len(row) == 5:  # Ensure the row has exactly 5 values
                    username, password, country, state, role = row
                    users[username.strip()] = {'password': password, 'country': country, 'state': state, 'role': role}  # Strip whitespace
                else:
                    print(f"Skipping invalid row: {row}")  # Optional: Log invalid rows
    except FileNotFoundError:
        pass  # If file doesn't exist, return an empty dictionary
    return users


# Function to handle login details
def user_credential(username, password, country, state, role, status_label):
    entered_username = username.get().strip()  # Strip any whitespace from entered username
    entered_password = password.get()
    entered_country = country.get()
    entered_state = state.get()
    selected_role = role.get()  # Get selected role (Head/User)

    # Read the stored user data from the file
    users = read_user_data()

    # Check if the username exists in the stored user data
    if entered_username in users:
        user_info = users[entered_username]
        # Check if the password, country/state, and role match
        if user_info['password'] == entered_password and user_info['country'] == entered_country and user_info['state'] == entered_state:
            if user_info['role'] == selected_role:
                status_label.config(text="Login Successful", fg="green")
                # Run different Python scripts based on the role
                if selected_role == "Head":
                    run_head_script()
                else:
                    run_user_script()
            else:
                status_label.config(text="Role mismatch", fg="red")
        else:
            status_label.config(text="Incorrect credentials or location", fg="red")
    else:
        status_label.config(text="Username not found", fg="red")

# Function to run a script for Head
def run_head_script():
    subprocess.run(["python3", "home page 2.py"])  # Replace with your Head-specific script

# Function to run a script for User
def run_user_script():
    subprocess.run(["python3", "HEAD SERVER.py"])  # Replace with your User-specific script

# Create the login window
def login_window():
    global tkWindow
    tkWindow = Tk()
    tkWindow.title("Login Form")
    tkWindow.geometry("400x400")

    Label(tkWindow, text="Please enter details below", width="300", bg="orange", fg="white").pack()

    # Username label and text entry box
    usernameLabel = Label(tkWindow, text="Username *").place(x=20, y=40)
    username = StringVar()
    usernameEntry = Entry(tkWindow, textvariable=username).place(x=90, y=42)

    # Password label and password entry box
    passwordLabel = Label(tkWindow, text="Password *").place(x=20, y=80)
    password = StringVar()
    passwordEntry = Entry(tkWindow, textvariable=password, show='*').place(x=90, y=82)

    # Country label and ComboBox
    countryLabel = Label(tkWindow, text="Country *").place(x=20, y=120)
    country = StringVar()
    countryCombo = ttk.Combobox(tkWindow, textvariable=country, values=["USA", "India"], state="readonly").place(x=90, y=122)

    # State label and ComboBox
    stateLabel = Label(tkWindow, text="State *").place(x=20, y=160)
    state = StringVar()
    stateCombo = ttk.Combobox(tkWindow, textvariable=state, values=["California", "Uttrakhand"], state="readonly").place(x=90, y=162)

    # Role label and ComboBox for Head/User selection
    roleLabel = Label(tkWindow, text="Role *").place(x=20, y=200)
    role = StringVar()
    roleCombo = ttk.Combobox(tkWindow, textvariable=role, values=["Head", "User"], state="readonly").place(x=90, y=202)

    # Label to show login status
    status_label = Label(tkWindow, text="", width=30, bg="white")
    status_label.place(x=20, y=240)

    user_credential_func = partial(user_credential, username, password, country, state, role, status_label)

    # Login button
    loginButton = Button(tkWindow, text="Login", width=10, height=1, bg="orange", command=user_credential_func).place(x=105, y=270)

    # Signup redirect button
    signupButton = Button(tkWindow, text="Signup", width=10, height=1, bg="blue", command=signup_window).place(x=105, y=310)

    tkWindow.mainloop()

# Create the signup window
def signup_window():
    global tkWindow
    tkWindow = Tk()
    tkWindow.title("Signup Form")
    tkWindow.geometry("400x450")

    Label(tkWindow, text="Please enter details below", width="300", bg="orange", fg="white").pack()

    # Full Name label and text entry box
    fullnameLabel = Label(tkWindow, text="Full Name *").place(x=20, y=40)
    fullname = StringVar()
    fullnameEntry = Entry(tkWindow, textvariable=fullname).place(x=90, y=42)

    # Email label and text entry box
    emailLabel = Label(tkWindow, text="Email *").place(x=20, y=80)
    email = StringVar()
    emailEntry = Entry(tkWindow, textvariable=email).place(x=90, y=82)

    # Username label and text entry box
    usernameLabel = Label(tkWindow, text="Username *").place(x=20, y=120)
    username = StringVar()
    usernameEntry = Entry(tkWindow, textvariable=username).place(x=90, y=122)

    # Password label and password entry box
    passwordLabel = Label(tkWindow, text="Password *").place(x=20, y=160)
    password = StringVar()
    passwordEntry = Entry(tkWindow, textvariable=password, show='*').place(x=90, y=162)

    # Country label and ComboBox
    countryLabel = Label(tkWindow, text="Country *").place(x=20, y=200)
    country = StringVar()
    countryCombo = ttk.Combobox(tkWindow, textvariable=country, values=["USA", "India"], state="readonly").place(x=90, y=202)

    # State label and ComboBox
    stateLabel = Label(tkWindow, text="State *").place(x=20, y=240)
    state = StringVar()
    stateCombo = ttk.Combobox(tkWindow, textvariable=state, values=["California", "Uttarakhand"], state="readonly").place(x=90, y=242)

    # Role label and ComboBox for Head/User selection
    roleLabel = Label(tkWindow, text="Role *").place(x=20, y=280)
    role = StringVar()
    roleCombo = ttk.Combobox(tkWindow, textvariable=role, values=["Head", "User"], state="readonly").place(x=90, y=282)

    # Label to show signup status
    status_label = Label(tkWindow, text="", width=30, bg="white")
    status_label.place(x=20, y=320)

    user_signup_func = partial(user_signup, username, password, email, fullname, country, state, role, status_label)

    # Signup button
    signupButton = Button(tkWindow, text="Signup", width=10, height=1, bg="green", command=user_signup_func).place(x=105, y=350)

    # Login redirect button
    loginButton = Button(tkWindow, text="Back to Login", width=15, height=1, bg="blue", command=login_window).place(x=90, y=380)

    tkWindow.mainloop()

# Function to handle signup details
def user_signup(username, password, email, fullname, country, state, role, status_label):
    entered_username = username.get().strip()  # Strip any whitespace from entered username

    # Read the stored user data from the file
    users = read_user_data()

    # Check if the username already exists (case-insensitive comparison)
    if entered_username.lower() in [user.lower() for user in users]:  # Compare usernames case-insensitively
        status_label.config(text="Username already exists", fg="red")
    else:
        # Write user data to the file
        write_user_data(entered_username, password.get(), country.get(), state.get(), role.get())
        status_label.config(text="Signup Successful, please login!", fg="green")
        # Optionally, switch to the login page after signup
        tkWindow.after(2000, login_window)  # Switch after 2 seconds

# Run the login window
login_window()
