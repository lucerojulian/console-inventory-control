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
    print("\t[1] Agregar productos")
    print("\t[2] Buscar productos")
    print("\t[3] Todos los productos")
    print("\t[4] Editar producto")
    print("\t[5] Eliminar producto")
    print("\t[6] Salir")

    opc = input("\n¿Que operacion desea realizar? ")

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
        print("\nIngreso una opcion no valida.")


menu()
