import time
import os
from lib.constants import ADD_PRODUCT_OPTION, SEARCH_PRODUCT_OPTION, LIST_ALL_PRODUCTS_OPTION, EDIT_PRODUCT_OPTION, \
    DELETE_PRODUCT_OPTION
from lib.products import add_new_product, search_product, list_all_products, edit_product, delete_product
from lib import globals
from lib.database import Database


def clear():
    if os.name == "nt":
        os.system("cls")
    elif os.name == "posix":
        os.system("clear")
    else:
        print("<- The screen could not be cleaned ->")


def draw_header():
    date = time.localtime()
    today = str(date.tm_mon) + "/" + str(date.tm_mday) + "/" + str(date.tm_year)
    clear()

    print("==========================================================================================")
    print("            Inventory manager                                            Date: " + today)
    print("|       Developed by Julian Lucero                                                       |")
    print("==========================================================================================")


def draw_options_menu(go_to_main_menu):
    globals.initialize()
    db = Database()

    if globals.current_menu == ADD_PRODUCT_OPTION:
        first_option_label = "Add another product"
    elif globals.current_menu == SEARCH_PRODUCT_OPTION:
        first_option_label = "Look for another product"
    elif globals.current_menu == LIST_ALL_PRODUCTS_OPTION:
        first_option_label = "Update product list"
    elif globals.current_menu == EDIT_PRODUCT_OPTION:
        first_option_label = "Edit another product"
    elif globals.current_menu == DELETE_PRODUCT_OPTION:
        first_option_label = "Delete another product"
    else:
        print("An unexpected error occurred, please contact the system administrator")
        exit()

    print("------------------------------------------------------------------------------------------")
    print("\n[1]", first_option_label)
    print("[2] Main menu")
    print("[3] Stop program\n")
    opc = input("Choose an option: ")

    while opc != "1" or opc != "2" or opc != "3":
        if opc == "1":
            if globals.current_menu == ADD_PRODUCT_OPTION:
                add_new_product(go_to_main_menu)

            elif globals.current_menu == SEARCH_PRODUCT_OPTION:
                search_product(go_to_main_menu)

            elif globals.current_menu == LIST_ALL_PRODUCTS_OPTION:
                list_all_products(go_to_main_menu)

            elif globals.current_menu == DELETE_PRODUCT_OPTION:
                delete_product(go_to_main_menu)

            elif globals.current_menu == EDIT_PRODUCT_OPTION:
                edit_product(go_to_main_menu)

        elif opc == "2":
            go_to_main_menu()
        elif opc == "3":
            db.close()
            exit()
        else:
            opc = input("Invalid operation, please try again")
