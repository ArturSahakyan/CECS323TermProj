# Local Imports
from ClientMgr import ClientMgr
from MenuDefs import menu_main


""" I like to keep my main file clean :p """
if __name__ == "__main__":
    # Connect to Atlas Cloud DB
    clientMgr = ClientMgr()
    clientMgr.genClusterLink()
    clientMgr.connectClient()

    # Example Database
    db = clientMgr.client["Demonstration"]

    # Test Connection by printing out collections
    print(db.list_collection_names())

    # Main Menu Loop
    user_action: str = ""
    while user_action != menu_main.last_action():
        user_action = menu_main.menu_prompt()
        exec(user_action)
        print("")

