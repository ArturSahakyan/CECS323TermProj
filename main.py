# API Imports
from pprint import pprint

# Local Imports
from ClientMgr import ClientMgr
from MenuDefs import menu_main, menu_add, menu_select, menu_list, menu_delete
from CollManager import CollManager
from DepartmentsCollection import DepartmentsCollection
from StudentsCollection import StudentsCollection
from CoursesCollection import CoursesCollection
from SectionsCollection import SectionsCollection

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

    CollManager.AddCollection("departments", DepartmentsCollection(db))
    CollManager.AddCollection("students", StudentsCollection(db))
    CollManager.AddCollection("courses", CoursesCollection(db))
    CollManager.AddCollection("sections", SectionsCollection(db))

    # Main Menu Loop
    exec_menu(menu_main)
