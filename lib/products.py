import time
from lib import globals
from lib.constants import ADD_PRODUCT_OPTION, EDIT_PRODUCT_OPTION, SEARCH_PRODUCT_OPTION, LIST_ALL_PRODUCTS_OPTION, \
    DELETE_PRODUCT_OPTION
from lib import screen
from lib.database import Database


def add_new_product(go_to_main_menu):
    globals.initialize()
    globals.current_menu = ADD_PRODUCT_OPTION
    screen.clear()
    screen.draw_header()
    db = Database()

    print('Type "menu" without quotes to return to the main menu\n')
    nombre = input("\tProduct name (Example: Tablet): ").lower()

    if nombre.lower() == "menu":
        go_to_main_menu()
    else:
        pass

    presentacion = input('\tProduct presentation (Example: 32", 1kg, 1.5l): ')
    preciocompra = float(input("\tPurchase cost (Without IVA): "))
    iva = preciocompra * 0.21
    recomendable = preciocompra + (preciocompra * 20 / 100) + iva
    print("\tRecommended sale price  $", round(recomendable))
    precioventa = float(input("\tSale price: "))
    marca = input("\tBrand (Example: Apple, LG): ").lower()
    proveedor = input(
        "\tSupplier: ").lower()
    unidades = int(input("\tNumber of units to add: "))
    print("")
    screen.draw_header()
    print("")
    print("\tDo you want to add the following product")
    print("")
    print("\t               Name:", nombre.capitalize())
    print("\t       Presentation:", presentacion)
    print("\t      Purchase cost:", preciocompra)
    print("\t         Sale price:", precioventa)
    print("\t              Brand:", marca.capitalize())
    print("\t       Units to add:", unidades)
    print("")
    opc = input('Type "yes" to confirm or "no" to cancel ( Without quotes ): ')

    while opc.lower() != "yes" or opc.lower() != "y" or opc.lower() != "no" or opc.lower() != "n":
        if opc.lower() == "yes" or opc.lower() == "y":
            table_info = "productos(nombre,presentacion,preciocompra,precioventa,marca,proveedor,unidades)"
            db.execute(
                "INSERT INTO " + table_info + " VALUES(?,?,?,?,?,?,?)",
                nombre, presentacion, preciocompra, precioventa, marca, proveedor, unidades)

            db.commit()
            print(
                "------------------------------------------------------------------------------------------")
            print("\t¡Product added successfully!")
            break
        elif opc.lower() == "no" or opc.lower() == "n":
            print("")
            print(
                "------------------------------------------------------------------------------------------")
            print("The operation was canceled")
            break
        else:
            opc = input("The answer is invalid, try again: ")

    screen.draw_options_menu(go_to_main_menu)


def edit_product(go_to_main_menu):
    globals.initialize()
    globals.current_menu = EDIT_PRODUCT_OPTION
    screen.draw_header()
    db = Database()

    print('  Type "menu" without quotes to return to the main menu')
    print("  ---------------------------------------------------------               ")
    print('  Type "search" without quotes to search for a product')
    print("==========================================================================================")

    if globals.error:
        print("\t\t\t¡Error! The code entered does not exist")
    else:
        print("")
    id = input("\tProduct code: ")
    if id.lower() == "menu":
        go_to_main_menu()
    elif id.lower() == "search":
        search_product(go_to_main_menu)
    else:
        pass

    try:
        db.execute("SELECT * FROM productos WHERE id=?", id)
        found = db.fetchone()

        print("")
        print("==========================================================================================\n")
        print("\t               Code:", found[0])
        print("\t               Name:", found[1])
        print("\t              Brand:", found[5])
        print("\t       Presentation:", found[2])
        print("\t      Purchase cost:", found[3])
        print("\t         Sale price:", found[4])
        print("\t           Supplier:", found[6])
        print("\t              Stock:", found[7])
        print("")
        print("\n==========================================================================================")
        globals.error = False

    except:
        globals.error = True
        edit_product(go_to_main_menu)

    print(' To skip a field press "ENTER"')
    print("------------------------------------------------------------------------------------------")
    newname = input("\n\tNew product name: ")
    if newname.lower() == "menu":
        go_to_main_menu()
    elif newname.lower() == "search":
        search_product(go_to_main_menu)
    else:
        pass

    newmarca = input("\n\tNew brand: ")
    newpresentacion = input("\n\tNew presentation: ")
    newpreciocompra = float(input("\n\tNew purchase cost: "))
    newprecioventa = float(input("\n\tNew sale price: "))
    newproveedor = input("\n\tNew supplier: ")
    newstock = int(input("\n\tNew stock: "))

    if newname != "":
        db.execute("UPDATE productos SET nombre=? WHERE id=?", newname.lower(), id)
    if newmarca != "":
        db.execute("UPDATE productos SET marca=? WHERE id=?", newmarca.lower(), id)
    if newpresentacion != "":
        db.execute("UPDATE productos SET presentacion=? WHERE id=?", newpresentacion.lower(), id)
    if newpreciocompra != 0:
        db.execute("UPDATE productos SET preciocompra=? WHERE id=?", newpreciocompra, id)
    if newprecioventa != 0:
        db.execute("UPDATE productos SET precioventa=? WHERE id=?", newprecioventa, id)
    if newproveedor != "":
        db.execute("UPDATE productos SET proveedor=? WHERE id=?", newproveedor.lower(), id)
    if newstock != 0:
        db.execute("UPDATE productos SET preciocompra=? WHERE id=?", newstock, id)
    else:
        pass

    opc = input('\n To confirm and apply this changes type "yes" or "no" to cancel: ')

    if opc.lower() == "yes" or opc.lower() == "y":
        db.commit()
        print("\n¡Changes were applied successfully!")
        screen.draw_options_menu(go_to_main_menu)
    elif opc.lower() == "no" or opc.lower() == "n":
        print("\n Changes are canceled.")
        screen.draw_options_menu(go_to_main_menu)


def delete_product(go_to_main_menu):
    globals.initialize()
    globals.current_menu = DELETE_PRODUCT_OPTION
    screen.clear()
    screen.draw_header()
    db = Database()

    print('  Type "menu" without quotes to return to the main menu\n')
    print("")
    id = input("Product code: ")
    if id.lower() == "menu":
        go_to_main_menu()
    else:
        pass

    db.execute("SELECT * FROM productos WHERE id=?", id)
    found = db.fetchone()

    if len(found) != 0:
        print("\n Information of product you want to delete\n")
        print("\t            Code:", found[0])
        print("\t            Name:", found[1])
        print("\t           Brand:", found[5])
        print("\t    Presentation:", found[2])
        print("\t           Stock:", found[7])
        opc = input('\n To confirm and delete this product type "yes" or "no" to cancel: ')

        if opc.lower() == "yes" or opc.lower() == "y":
            db.execute("DELETE FROM productos WHERE id= ?", id)
            db.commit()
            screen.draw_options_menu(go_to_main_menu)

        elif opc.lower() == "no" or opc.lower() == "n":
            print("\nThe operation was canceled\n")
            screen.draw_options_menu(go_to_main_menu)

    elif len(found) == 0:
        print("\nThe code does not exist")
        screen.draw_options_menu(go_to_main_menu)

    else:
        print("\nAn unexpected error occurred, please contact the system administrator")


def search_product(go_to_main_menu):
    globals.initialize()
    globals.current_menu = SEARCH_PRODUCT_OPTION
    screen.draw_header()
    db = Database()

    print(' Type "menu" without quotes to return to the main menu\n')
    print(" You can search by name, brand, code or presentation of the product\n")
    search = input("\tSearch: ").lower()

    if search == "menu":
        go_to_main_menu()
    else:
        pass

    search_pattern = '%' + search + '%'
    db.execute(
        "SELECT * FROM productos WHERE nombre LIKE ? OR marca LIKE ? OR id LIKE ? OR presentacion LIKE ?",
        search_pattern, search_pattern, search_pattern, search_pattern)
    found = db.fetchall()

    print("")

    if len(found) == 0:
        print("\tNo results were found")
        print("")

    else:
        print(len(found), "results found.")
        print("")
        print("------------------------------------------------------------------------------------------")
        print("|   Code   |      Product Name      |      Brand       |    Presentation    |   Stock    |")
        print("------------------------------------------------------------------------------------------")
        for row in found:
            time.sleep(0.1)
            print(" ", row[0], " " * (6 - len(str(row[0]))), "", row[1], " " * (19 - len(str(row[1]))), "", row[5],
                  " " * (
                          16 - len(str(row[5]))), "", row[2], " " * (12 - len(str(row[2]))), "", row[7],
                  " " * (6 - len(str(row[7]))), "")
        print("")

    screen.draw_options_menu(go_to_main_menu)


def list_all_products(go_to_main_menu):
    globals.initialize()
    globals.current_menu = LIST_ALL_PRODUCTS_OPTION
    screen.clear()
    screen.draw_header()
    db = Database()

    show = "SELECT * FROM productos"
    db.execute(show)
    results = db.fetchall()

    print("|        |                     |              |            |                  |          |")
    print("|  Code  |         Name        | Presentation | Price+IVA  |       Brand      |  Stock   |")
    print("|        |                     |              |            |                  |          |")
    print("|----------------------------------------------------------------------------------------|")
    for row in results:
        print("|", row[0], " " * (6 - len(str(row[0]))), "", row[1].capitalize(), " " * (19 - len(str(row[1]))), "",
              row[2], " " * (12 - len(str(row[2]))),
              "", row[4], " " * (10 - len(str(row[4]))), "", row[5].capitalize(), " " * (16 - len(str(row[5]))), "",
              row[7], " " * (7 - len(str(row[7]))), "|")
        print("|----------------------------------------------------------------------------------------|")

        time.sleep(0.07)
    print("\t\t\t\t\t\tIn total there are", len(results), "products")

    screen.draw_options_menu(go_to_main_menu)
