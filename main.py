from lib import screen
from lib.database import Database
from lib.products import add_new_product, search_product, list_all_products, edit_product, delete_product

__author__ = "Julian Andres Lucero"
__copyright__ = "Copyright 2019, Julian Lucero"
__license__ = "GNU General Public Licence v3.0"
__version__ = "1.1"
__maintainer__ = "Julian Andres Lucero"
__email__ = "julianlucero2012@gmail.com"
__status__ = "Alpha"


def menu():
    screen.clear()
    screen.draw_header()
    db = Database()

    print(" ")
    print("\t[1] Add new products")
    print("\t[2] Search products")
    print("\t[3] List all products")
    print("\t[4] Edit a product")
    print("\t[5] Delete a product")
    print("\t[6] Stop program")

    opc = input("\nChoose an option: ")

    if opc == "1":
        add_new_product(menu)
    elif opc == "2":
        search_product(menu)
    elif opc == "3":
        list_all_products(menu)
    elif opc == "4":
        edit_product(menu)
    elif opc == "5":
        delete_product(menu)
    elif opc == "6":
        db.close()
        exit()
    else:
        menu()
        print("\nYou chose and invalid option!")


menu()
