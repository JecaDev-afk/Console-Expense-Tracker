import json
import requests

def load_data():
    # if not os.path.exists("history.json") or os.path.getsize("history.json") == 0:
    #     return []
    
    try:
        with open("history.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
     
history = load_data()

def save_data():
    with open("history.json", "w", encoding="utf-8") as file:
        return json.dump(history, file, indent=4, ensure_ascii=False)

def add_transaction():
    operation = {}

    while True:
        op_type = input("choose type (income / costs) or return")
        if op_type == "income" or op_type == "costs":
            operation["type"] = op_type
            break
        elif op_type == "return":
            break
        else:
            print("wrong type! Try again")
    if op_type == "return":
       return 
    while True:
        op_amount = input("enter the amount of money")
        try:
            operation["amount"] = float(op_amount)
            break
        except ValueError:
            print("pls only numbers")
    history.append(operation)
    save_data()
    print("operation successfully added !")
    # print(history)
    return history

def check_balance():

    balance = 0
    for op in history:
        if op["type"] == "income":
            balance += op["amount"]
        elif op["type"] == "costs":
            balance -= op["amount"]
    # print(balance)
    return balance

def show_balance_usd():

    current_balance = check_balance()
    
    try:
        response = requests.get("https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json")
    except Exception:
        print("Connection error!")
        return 
    
    data = response.json()
    balance_usd = 0
    current_usd = 0
    for d in data:
        if d["cc"] == "USD":
            current_usd = d["rate"]
            balance_usd = current_balance / current_usd
            break
    if current_usd > 0:
        print(f"USD exchange rate: {current_usd}")
        print(f"Your balance, converted to USD: {balance_usd}")
    else: 
        print("Cannot find USD exchange rate!") 


while True:
    user_choice = input("What do we do?\n \"1 - add transaction\"\n \"2 - see your balance\"\n \"3\" - convert to USD \n \"4\" to leave \n" )

    if user_choice == "1":
        current_history = add_transaction()
        print(history)
    elif user_choice == "2":
        current_balance = check_balance()
        print(f"Your balance: {current_balance}")
    elif user_choice == "3":
        show_balance_usd()
    elif user_choice == "4":
        break
    else:
        print ("that command is not recognized, try: \"1 - add amount of money\" / \"2 - add spendings\", or type \"3\" to leave ") 
