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
    Option("Departments", "CollManager.GetCollection('departments').addDoc()"),
    Option("Majors", "CollManager.GetCollection('departments').addMajor()"),
    Option("Students", "CollManager.GetCollection('students').addDoc()"),
    Option("Courses", "CollManager.GetCollection('courses').addDoc()"),
    Option("Exit", "pass")
])

menu_select = Menu('select', 'Please Select Which Collection to Select From:', [
    Option("Departments", "pprint(CollManager.GetCollection('departments').selectDoc())"),
    Option("Students", "pprint(CollManager.GetCollection('students').selectDoc())"),
    Option("Courses", "pprint(CollManager.GetCollection('courses').selectDoc())"),
    Option("Exit", "pass")
])

menu_list = Menu('list', 'Please Select Which Collection to List:', [
    Option("Departments", "CollManager.GetCollection('departments').listAll()"),
    Option("Majors", "CollManager.GetCollection('departments').listMajors()"),
    Option("Students", "CollManager.GetCollection('students').listAll()"),
    Option("Courses", "CollManager.GetCollection('courses').listAll()"),
    Option("Exit", "pass")
])

menu_delete = Menu('delete', 'Please Select Which Collection to Delete From:', [
    Option("Departments", "CollManager.GetCollection('departments').deleteDoc()"),
    Option("Majors", "CollManager.GetCollection('departments').deleteMajor()"),
    Option("Students", "CollManager.GetCollection('students').deleteDoc()"),
    Option("Courses', CollManager.GetCollection('courses').deleteDoc()"),
    Option("Exit", "pass")
])
