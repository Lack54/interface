# ask if registering account or logging in
import json
import hashlib
import os
import colorama
from colorama import Fore
import time
import uuid

def main():
    check = input("Register account or Login"+Fore.BLUE+": "+Fore.RESET).lower().strip()
    if check == "register":
        clear()
        register_account()
    else: 
        clear()
        login()

def generate_invite(user):
    item = str(uuid.uuid4()) + f"|{user}|{time.asctime()}|"
    filename = 'invites.json'
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        data = []

    data.append(item)

    with open(filename, 'w') as f:
        json.dump(data, f)
    print(f"{Fore.RED}Generated invintation{Fore.WHITE}:{Fore.BLUE} {item}")
    return

def invite_check(item):
    filename = 'invites.json'
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        print(Fore.RED+"Invite Error"+Fore.RESET)

    if item in data:
        data.remove(item)
        with open(filename, 'w') as f:
            json.dump(data, f)

        return True

    else:
        print(Fore.RED+"Invalid invite."+Fore.RESET)
        register_account()

def clear():
    os.system("cls")

# hash password

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# select user program

def program_select():
    dir = os.getcwd()
    clear()
    print(Fore.RED +"""
  _            _         _____         _    
 | |   __ _ __| |__ ___ |_   _|__  ___| |___
 | |__/ _` / _| / /(_-<   | |/ _ \/ _ \ (_-<
 """+Fore.BLUE+"""|____\__,_\__|_\_\/__/   |_|\___/\___/_/__/ 
"""+Fore.RESET+"""
 ["""+Fore.BLUE+"1"+Fore.RESET+"""] Password Multi-Tool
 ["""+Fore.BLUE+"2"+Fore.RESET+"""] Geolocate IP
 ["""+Fore.BLUE+"3"+Fore.RESET+"""] Keylogger Options
 ["""+Fore.BLUE+"4"+Fore.RESET+"""] Exit
    """)
    print(Fore.CYAN + "> ",Fore.RESET, end="")
    selection = input(Fore.RESET)
    while selection != "4":
        clear()
        print(Fore.RED +"""
  _            _         _____         _    
 | |   __ _ __| |__ ___ |_   _|__  ___| |___
 | |__/ _` / _| / /(_-<   | |/ _ \/ _ \ (_-<
 """+Fore.BLUE+"""|____\__,_\__|_\_\/__/   |_|\___/\___/_/__/ 
"""+Fore.RESET+"""
 ["""+Fore.BLUE+"1"+Fore.RESET+"""] Password Multi-Tool
 ["""+Fore.BLUE+"2"+Fore.RESET+"""] Geolocate IP
 ["""+Fore.BLUE+"3"+Fore.RESET+"""] Keylogger Options
 ["""+Fore.BLUE+"4"+Fore.RESET+"""] Exit
    """)
        if selection == "1":
            clear()
            print(Fore.RED+"Press enter to continue."+Fore.RESET)
            os.system("python "+dir+"\Projects\Password_Generater\main.py")
        elif selection == "2":
            clear()
            os.system("python "+dir+"\Projects\Ip_Logger\geolocate.py")
        elif selection == "3":
            clear()
            print(Fore.RED +"""
 _  __         _                        
| |/ /___ _  _| |___  __ _ __ _ ___ _ _ 
| ' </ -_) || | / _ \/ _` / _` / -_) '_|
"""+Fore.BLUE+"""|_|\_\___|\_, |_\___/\__, \__, \___|_|  
            |__/       |___/|___/         
"""+Fore.RESET+"""
["""+Fore.BLUE+"1"+Fore.RESET+"""] Go back
["""+Fore.BLUE+"2"+Fore.RESET+"""] Install keylogger to a usb for use on another machine
        """)
            x = input(Fore.BLUE+"> "+Fore.RESET)
            if x == "1":
                clear()
                pass
            elif x == "2":
                clear()
                os.system("python "+dir+"\Projects\Keylogger\\USB_VERSION\install.py")
            else:
                pass
        elif selection == "4":
            exit()
        else:
            pass
        selection = input(Fore.CYAN+"> "+Fore.RESET)

# log the user in
def login():
    # load existing user data from the file
    try:
        with open("database.json", "r") as file:
            users = json.load(file)
    except FileNotFoundError:
        users = {}

    # prompt the user to enter their username and password
    username = input("Enter your username"+Fore.BLUE+": "+Fore.RESET)
    clear()
    password = input("Enter your password"+Fore.BLUE+": "+Fore.RESET)
    clear()
    
    # check if the username and password are correct
    if username in users and users[username]["password"] == hash_password(password):
        _2fa = users[username]["question"]
        print("Answer this security question"+Fore.BLUE+":"+Fore.RESET, _2fa)
        answer = input("Question Answer"+Fore.BLUE+": "+Fore.RESET)
        if answer == users[username]["answer"] and users[username]["banned"] == False:
            clear()
            print(Fore.RED+"Log in succsessful!"+Fore.RESET)
            if users[username]["is_admin"]:
                admin_panel(username, users)
            elif not users[username]["is_admin"]:
                print(Fore.RED+"Continuing in 5 seconds."+Fore.RESET)
                time.sleep(5)
                clear()
                program_select()
        elif users[username]["banned"]:
            clear()
            print(Fore.RED+"You have been banned from this application."+Fore.RESET)
        else:
            clear()
            print(Fore.RED+"Incorrect security question answer."+Fore.RESET)
    else:
        clear()
        print(Fore.RED+"Account not found."+Fore.RESET)

# register a account and add it to json

def register_account():  
    user_invite = input("Invintation code"+Fore.BLUE+": "+Fore.RESET)
    invite_check(user_invite)
    username = input("Username"+Fore.BLUE+": "+Fore.RESET)
    password = input("Password"+Fore.BLUE+": "+Fore.RESET)
    twofactor = input("Please input a two factor authentication question"+Fore.BLUE+": "+Fore.RESET)
    answer = input("Question Answer"+Fore.BLUE+": "+Fore.RESET)

    try:
        with open("database.json", "r") as file:
            users = json.load(file)
    except FileNotFoundError:
        users = {}    

    users[username] = {"password": hash_password(password), "is_admin": False, "banned" : False, "question" : twofactor, "answer" : answer}
    with open("database.json", "w") as file:
        json.dump(users, file)

    print(Fore.RED+"Signup successful!"+Fore.RESET)
    return

def admin_panel(username, users):
    clear()
    print("| Welcome "+Fore.BLUE+username+Fore.RESET+" |")
    print("""
["""+Fore.BLUE+"0"+Fore.RESET+"""] Generate invintation code
["""+Fore.BLUE+"1"+Fore.RESET+"""] Open program select
["""+Fore.BLUE+"2"+Fore.RESET+"""] Create a new account
["""+Fore.BLUE+"3"+Fore.RESET+"""] Remove a account
["""+Fore.BLUE+"4"+Fore.RESET+"""] Ban or unban a account
["""+Fore.BLUE+"5"+Fore.RESET+"""] Admin or unadmin a account
["""+Fore.BLUE+"6"+Fore.RESET+"""] Show all registered accounts
["""+Fore.BLUE+"7"+Fore.RESET+"""] Exit
["""+Fore.BLUE+"8"+Fore.RESET+"""] Show all commands
["""+Fore.BLUE+"9"+Fore.RESET+"""] Clear terminal
        """) 
    option = input(Fore.BLUE+"> "+Fore.RESET)
    while option != "7":
        if option == "0":
            clear()
            generate_invite(username)
        # open tool select 
        elif option == "1":
            clear()
            program_select()

        # add account
        elif option == "2":
            clear()
            register_account()

        # remove a account
        elif option == "3":
            remove_username = input("Enter the username of the user to remove"+Fore.BLUE+": "+Fore.RESET)
            if remove_username in users:
                del users[remove_username]
                with open("database.json", "w") as file:
                    json.dump(users, file)
                print(Fore.RED+"User removed successfully."+Fore.RESET)
            else:
                print(Fore.RED+"User not found."+Fore.RESET)

        # Ban a account 
        elif option == "4":
            ban_username = input("Enter the username of the user to ban/unban"+Fore.BLUE+": "+Fore.RESET)
            action = input("Ban or unban: ").lower().strip()
            if ban_username in users:
                if action == "ban":
                    users[ban_username]["banned"] = True
                else:
                    users[ban_username]["banned"] = False
                print(Fore.RED+f"{action}'ed user {ban_username}."+Fore.RESET)
                with open("database.json", "w") as file:
                    json.dump(users, file)
            else:
                print(Fore.RED+"User not found."+Fore.RESET)
        
        elif option == "5":
            admin_username = input("Enter the username of the user to admin/unadmin"+Fore.BLUE+": "+Fore.RESET)
            action = input("Admin or unadmin account: ").lower().strip()
            if admin_username in users:
                if action == "admin":
                    users[admin_username]["is_admin"] = True
                    print(Fore.RED+f"Gave admin to user {admin_username}."+Fore.RESET)
                else:
                    users[admin_username]["is_admin"] = False
                    print(Fore.RED+f"Removed admin from user {admin_username}."+Fore.RESET)
                with open("database.json", "w") as file:
                    json.dump(users, file)
            else:
                print(Fore.RED+f"Username {admin_username} not found."+Fore.RESET)
        
        # show all registered user
        elif option == "6":

            with open("database.json", "r") as file:
                users = json.load(file)

            for user in users:
                print(f"| {user} | Banned:", users[user]["banned"], " | Admin:", users[user]["is_admin"])

        # exit
        elif option == "7":
            exit()
        
        # show all cmds
        elif option == "8" or option == "cmds" or option == "help" or option == "commands":
            clear()
            print(f"| Welcome "+Fore.BLUE+username+Fore.RESET+" |")
            print("""
["""+Fore.BLUE+"0"+Fore.RESET+"""] Generate invintation code
["""+Fore.BLUE+"1"+Fore.RESET+"""] Open program select
["""+Fore.BLUE+"2"+Fore.RESET+"""] Create a new account
["""+Fore.BLUE+"3"+Fore.RESET+"""] Remove a account
["""+Fore.BLUE+"4"+Fore.RESET+"""] Ban or unban a account
["""+Fore.BLUE+"5"+Fore.RESET+"""] Admin or unadmin a account
["""+Fore.BLUE+"6"+Fore.RESET+"""] Show all registered accounts
["""+Fore.BLUE+"7"+Fore.RESET+"""] Exit
["""+Fore.BLUE+"8"+Fore.RESET+"""] Show all commands
["""+Fore.BLUE+"9"+Fore.RESET+"""] Clear terminal
                """) 

        elif option == "9" or option == "cls" or option == "clear":
            clear()

        # handles invalid choice
        else:
            print(Fore.RED+"Command not found."+Fore.RESET)    
        option = input(Fore.BLUE+"> "+Fore.RESET)

main()