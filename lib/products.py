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

    print('¡Si ingreso erroneamente escriba la palabra "menu" sin comillas para regresar!\n')
    nombre = input("\tNombre del producto (Ejemplo: Yogurt): ").lower()

    if nombre.lower() == "menu":
        go_to_main_menu()
    else:
        pass
    presentacion = input("\tPresentacion del producto (Ejemplo: 1kg, 1.5l): ")
    preciocompra = float(input("\tPrecio de compra (Sin IVA): "))
    iva = preciocompra * 0.21
    recomendable = preciocompra + (preciocompra * 20 / 100) + iva
    print("\tPrecio de venta recomendado  $", round(recomendable))
    precioventa = float(input("\tPrecio de venta: "))
    marca = input("\tMarca (Ejemplo: Sancor): ").lower()
    proveedor = input(
        "\tProveedor (Ejemplo: Distribuidor mayorista Gral. Pico): ").lower()
    unidades = int(input("\tCantidad de unidades que desea agregar: "))
    print("")
    screen.draw_header()
    print("")
    print("\t¿Desea agregar el siguiente producto?")
    print("")
    print("\tNombre del producto:", nombre.capitalize())
    print("\t       Presentacion:", presentacion)
    print("\t   Precio de compra:", preciocompra)
    print("\t    Precio de venta:", precioventa)
    print("\t Marca o Fabricante:", marca.capitalize())
    print("\t Unidades a agregar:", unidades)
    print("")
    opc = input(
        'Escriba "Si" para confirmar o "No" para cancelar (Sin las comillas): ')

    while opc.lower() != "si" or opc.lower() != "s" or opc.lower() != "no" or opc.lower() != "n":
        if opc.lower() == "si" or opc.lower() == "s":
            table_info = "productos(nombre,presentacion,preciocompra,precioventa,marca,proveedor,unidades)"
            db.execute(
                "INSERT INTO " + table_info + " VALUES(?,?,?,?,?,?,?)",
                nombre, presentacion, preciocompra, precioventa, marca, proveedor, unidades)

            db.commit()
            print(
                "------------------------------------------------------------------------------------------")
            print("\tOperacion realizada con exito.")
            break
        elif opc.lower() == "no" or opc.lower() == "n":
            print("")
            print(
                "------------------------------------------------------------------------------------------")
            print("Se ha cancelado la operacion")
            break
        else:
            opc = input("La respuesta es incorrecta, intenta denuevo: ")

    screen.draw_options_menu(go_to_main_menu)


def edit_product(go_to_main_menu):
    globals.initialize()
    globals.current_menu = EDIT_PRODUCT_OPTION
    screen.draw_header()
    db = Database()

    print(' ¡Si ingreso erroneamente escriba la palabra "menu" sin comillas para regresar!')
    print("      ---------------------------------------------------------               ")
    print('  Si no recuerda el codigo del articulo escriba "buscar" sin las comillas')
    print("==========================================================================================")

    if globals.error:
        print("\t\t\t¡ERROR! EL CODIGO INGRESADO NO EXISTE")
    else:
        print("")
    id = input("\tCodigo del producto a editar: ")
    if id.lower() == "menu":
        go_to_main_menu()
    elif id.lower() == "buscar":
        search_product(go_to_main_menu)
    else:
        pass

    try:
        db.execute("SELECT * FROM productos WHERE id=?", id)
        found = db.fetchone()

        print("")
        print("==========================================================================================\n")
        print("\t             Codigo:", found[0])
        print("\t             Nombre:", found[1])
        print("\t   Fabricante/Marca:", found[5])
        print("\t       Presentacion:", found[2])
        print("\t   Precio de compra:", found[3])
        print("\t    Precio de venta:", found[4])
        print("\t          Proveedor:", found[6])
        print("\t   Stock disponible:", found[7])
        print("")
        print("\n==========================================================================================")
        globals.error = False

    except:
        globals.error = True
        edit_product(go_to_main_menu)

    print(" Para no editar algun dato preciona ENTER y en los precios coloca un 0 (Cero)")
    print("------------------------------------------------------------------------------------------")
    newname = input("\n\tNuevo nombre: ")
    if newname.lower() == "menu":
        go_to_main_menu()
    elif newname.lower() == "buscar":
        search_product(go_to_main_menu)
    else:
        pass
    newmarca = input("\n\tNuevo/a fabricante/Marca: ")
    newpresentacion = input("\n\tNuevo presentacion: ")
    newpreciocompra = float(input("\n\tNuevo precio de compra: "))
    newprecioventa = float(input("\n\tNuevo precio de venta: "))
    newproveedor = input("\n\tNuevo proveedor: ")
    newstock = int(input("\n\tActualizar stock disponible: "))

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

    opc = input("\n ¿Esta seguro que desea aplicar estos cambios? si o no: ")

    if opc.lower() == "si" or opc.lower() == "s":
        db.commit()
        print("\nSe han aplicado los cambios")
        screen.draw_options_menu()
    elif opc.lower() == "no" or opc.lower() == "n":
        print("\n Los cambios han sido cancelados.")
        screen.draw_options_menu()


def delete_product(go_to_main_menu):
    globals.initialize()
    globals.current_menu = DELETE_PRODUCT_OPTION
    screen.clear()
    screen.draw_header()
    db = Database()

    print(' ¡Si ingreso erroneamente escriba la palabra "menu" sin comillas para regresar!\n')
    print("")
    id = input("Codigo del producto a eliminar: ")
    if id.lower() == "menu":
        go_to_main_menu()
    else:
        pass

    db.execute("SELECT * FROM productos WHERE id=?", id)
    found = db.fetchone()

    if len(found) != 0:
        print("\n El codigo ingresado pertenece al producto\n")
        print("\t          Codigo:", found[0])
        print("\t          Nombre:", found[1])
        print("\tMarca/Fabricante:", found[5])
        print("\t    Presentacion:", found[2])
        print("\tStock disponible:", found[7])
        opc = input("\n ¿Esta seguro desea eliminar el producto? si o no: ")

        if opc.lower() == "si" or opc.lower() == "s":
            db.execute("DELETE FROM productos WHERE id= ?", id)
            db.commit()
            screen.draw_options_menu(go_to_main_menu)

        elif opc.lower() == "no" or opc.lower() == "n":
            print("\nSe ha cancelado la operacion\n")
            screen.draw_options_menu(go_to_main_menu)

    elif len(found) == 0:
        print("\nEl codigo ingresado no existe")
        screen.draw_options_menu(go_to_main_menu)

    else:
        print("\n¡Error! Ponganse en contacto con el administrador del sistema")


def search_product(go_to_main_menu):
    globals.initialize()
    globals.current_menu = SEARCH_PRODUCT_OPTION
    screen.draw_header()
    db = Database()

    print(' ¡Si ingreso erroneamente escriba la palabra "menu" sin comillas para regresar!\n')
    print(" Puedes buscar por nombre del producto, marca, codigo o presentacion\n")
    search = input("\tBuscar: ").lower()

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
        print("\tNo se ha encontrado ningun resultado")
        print("")

    else:
        print("En total hay", len(found), "coincidencias")
        print("")
        print("------------------------------------------------------------------------------------------")
        print("| Codigo | Nombre del producto | Fabricante/Marca | Presentacion | Stock disponible      |")
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
    print("| Codigo | Nombre del producto | Presentacion | Precio+IVA | Fabricante/Marca | Unidades |")
    print("|        |                     |              |            |                  |          |")
    print("|----------------------------------------------------------------------------------------|")
    for row in results:
        print("|", row[0], " " * (6 - len(str(row[0]))), "", row[1].capitalize(), " " * (19 - len(str(row[1]))), "",
              row[2], " " * (12 - len(str(row[2]))),
              "", row[4], " " * (10 - len(str(row[4]))), "", row[5].capitalize(), " " * (16 - len(str(row[5]))), "",
              row[7], " " * (7 - len(str(row[7]))), "|")
        print("|----------------------------------------------------------------------------------------|")

        time.sleep(0.07)
    print("\t\t\t\t\t\tEn total hay", len(results), "productos agregados")

    screen.draw_options_menu(go_to_main_menu)
