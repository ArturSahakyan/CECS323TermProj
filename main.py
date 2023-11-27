# API Imports
from pymongo import MongoClient
import certifi

# Local Imports
from MenuDefs import menu_main

if __name__ == "__main__":
    user_action: str = ""
    while user_action != menu_main.last_action():
        user_action = menu_main.menu_prompt()
        exec(user_action)
        print("")