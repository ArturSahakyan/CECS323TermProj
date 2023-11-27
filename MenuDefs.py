from Menu import Menu
from Menu import Option

# The main options for operating on Departments and Courses.
menu_main = Menu('main', 'Please select one of the following options:', [
    Option("Add", "print('Temp Add')"),
    Option("List", "print('Temp List')"),
    Option("Delete", "print('Temp Delete')"),
    Option("Exit this application", "pass")
])
