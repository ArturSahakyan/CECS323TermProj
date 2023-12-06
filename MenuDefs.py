from Menu import Menu
from Menu import Option

# The main options for operating on Departments and Courses.
menu_main = Menu('main', 'Please select one of the following options:', [
    Option("Add", "exec_menu(menu_add)"),
    Option("Select", "exec_menu(menu_select)"),
    Option("List", "exec_menu(menu_list)"),
    Option("Delete", "exec_menu(menu_delete)"),
    Option("Exit this application", "pass")
])

menu_add = Menu('add', 'Please Select Which Collection To Add To:', [
    Option("Departments", "collMgr['departments'].addDoc()"),
    Option("Exit", "pass")
])

menu_select = Menu('select', 'Please Select Which Collection to Select From:', [
    Option("Departments", "pprint(collMgr['departments'].selectDoc())"),
    Option("Exit", "pass")
])

menu_list = Menu('list', 'Please Select Which Collection to List:', [
    Option("Departments", "collMgr['departments'].listAll()"),
    Option("Exit", "pass")
])

menu_delete = Menu('delete', 'Please Select Which Collection to Delete From:', [
    Option("Departments", "collMgr['departments'].deleteDoc()"),
    Option("Exit", "pass")
])
