# API Imports
from pprint import pprint

# Local Imports
from ClientMgr import ClientMgr
from MenuDefs import menu_main, menu_add, menu_select, menu_list, menu_delete
from CollectionBase import CollectionBase
from DepartmentsCollection import DepartmentsCollection

""" I like to keep my main file clean :p """

def exec_menu(menu):
    user_action : str = ""
    while user_action != menu.last_action():
        user_action = menu.menu_prompt()
        print("")
        exec(user_action)
        print("")

if __name__ == "__main__":
    # Connect to Atlas Cloud DB
    clientMgr = ClientMgr()
    clientMgr.genClusterLink()
    clientMgr.connectClient()

    # Setup DataBase and Collections
    db = clientMgr.client["Demonstration"]
    collMgr = {
        "departments": DepartmentsCollection(db),
    }

    # Main Menu Loop
    exec_menu(menu_main)
