import time
import sqlite3
from lib import screen

__author__ = "Julian Andres Lucero"
__copyright__ = "Copyright 2019, Julian Lucero"
__license__ = "GNU General Public Licence v3.0"
__version__ = "1.1"
__maintainer__ = "Julian Andres Lucero"
__email__ = "julianlucero2012@gmail.com"
__status__ = "Alpha"

sql_connection = sqlite3.connect('database.s3db')
sql_cursor = sql_connection.cursor()
current_menu = ""
error = False


def optionmenu():
    global current_menu
    textomenu = ""
    if current_menu == "agregar_articulo":
        textomenu = "Agregar otro articulo"
    elif current_menu == "buscar_articulos":
        textomenu = "Buscar otro producto"
    elif current_menu == "mostrar_articulos":
        textomenu = "Actualizar lista"
    elif current_menu == "modificar_articulo":
        textomenu = "Modificar otro articulo"
    elif current_menu == "eliminar_articulo":
        textomenu = "Eliminar otro articulo"
    else:
        print("Error, ponganse en contacto con el administrador del sistema")
        exit()
    print("------------------------------------------------------------------------------------------")
    print("\n[1]", textomenu)
    print("[2] Menu principal")
    print("[3] Salir del programa\n")
    opc = input("Seleccionar opcion: ")

    while opc != "1" or opc != "2" or opc != "3":
        if opc == "1":
            if current_menu == "agregar_articulo":
                agregar_articulo()
            elif current_menu == "buscar_articulos":
                buscar_articulos()
            elif current_menu == "mostrar_articulos":
                mostrar_articulos()
            elif current_menu == "eliminar_articulo":
                eliminar_articulo()
            elif current_menu == "modificar_articulo":
                modificar_articulo()
        elif opc == "2":
            menu()
        elif opc == "3":
            sql_connection.close()
            exit()
        else:
            opc = input("Operacion no valida, intente denuevo: ")


def agregar_articulo():
    global current_menu
    current_menu = "agregar_articulo"
    screen.clear()
    screen.draw_header()
    print(' ¡Si ingreso erroneamente escriba la palabra "menu" sin comillas para regresar!\n')
    nombre = input("\tNombre del producto (Ejemplo: Yogurt): ")
    if nombre.lower() == "menu":
        menu()
    else:
        pass
    presentacion = input("\tPresentacion del producto (Ejemplo: 1kg, 1.5l): ")
    preciocompra = float(input("\tPrecio de compra (Sin IVA): "))
    iva = preciocompra * 0.21
    recomendable = preciocompra + (preciocompra * 20 / 100) + iva
    print("\tPrecio de venta recomendado  $", round(recomendable))
    precioventa = float(input("\tPrecio de venta: "))
    marca = input("\tMarca (Ejemplo: Sancor): ")
    proveedor = input(
        "\tProveedor (Ejemplo: Distribuidor mayorista Gral. Pico): ")
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
            sql_cursor.execute(
                "INSERT INTO productos(nombre,presentacion,preciocompra,precioventa,marca,proveedor,unidades) VALUES(?,?,?,?,?,?,?)",
                (nombre.lower(), presentacion, preciocompra, precioventa, marca.lower(), proveedor.lower(), unidades))
            sql_connection.commit()
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

    optionmenu()


def buscar_articulos():
    global current_menu
    current_menu = "buscar_articulos"
    screen.draw_header()
    print(' ¡Si ingreso erroneamente escriba la palabra "menu" sin comillas para regresar!\n')
    print(" Puedes buscar por nombre del producto, marca, codigo o presentacion\n")
    search = input("\tBuscar: ").lower()
    if search == "menu":
        menu()
    else:
        pass

    searchPattern = '%' + search + '%'
    sql_cursor.execute(
        "SELECT * FROM productos WHERE nombre LIKE ? OR marca LIKE ? OR id LIKE ? OR presentacion LIKE ?",
        (searchPattern, searchPattern, searchPattern, searchPattern,))
    found = sql_cursor.fetchall()

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

    optionmenu()


def mostrar_articulos():
    global current_menu
    current_menu = "mostrar_articulos"
    screen.clear()
    screen.draw_header()
    show = "SELECT * FROM productos"
    sql_cursor.execute(show)
    results = sql_cursor.fetchall()
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

    optionmenu()


def modificar_articulo():
    global current_menu
    global error
    current_menu = "modificar_articulo"
    screen.draw_header()
    print(' ¡Si ingreso erroneamente escriba la palabra "menu" sin comillas para regresar!')
    print("      ---------------------------------------------------------               ")
    print('  Si no recuerda el codigo del articulo escriba "buscar" sin las comillas')
    print("==========================================================================================")
    if error:
        print("\t\t\t¡ERROR! EL CODIGO INGRESADO NO EXISTE")
    else:
        print("")
    id = input("\tCodigo del producto a editar: ")
    if id.lower() == "menu":
        menu()
    elif id.lower() == "buscar":
        buscar_articulos()
    else:
        pass

    try:
        sql_cursor.execute("SELECT * FROM productos WHERE id=?", (id,))
        found = sql_cursor.fetchone()
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
        error = False

    except:
        error = True
        modificar_articulo()

    print(" Para no editar algun dato preciona ENTER y en los precios coloca un 0 (Cero)")
    print("------------------------------------------------------------------------------------------")
    newname = input("\n\tNuevo nombre: ")
    if newname.lower() == "menu":
        menu()
    elif newname.lower() == "buscar":
        buscar_articulos()
    else:
        pass
    newmarca = input("\n\tNuevo/a fabricante/Marca: ")
    newpresentacion = input("\n\tNuevo presentacion: ")
    newpreciocompra = float(input("\n\tNuevo precio de compra: "))
    newprecioventa = float(input("\n\tNuevo precio de venta: "))
    newproveedor = input("\n\tNuevo proveedor: ")
    newstock = int(input("\n\tActualizar stock disponible: "))

    if newname != "":
        sql_cursor.execute("UPDATE productos SET nombre=? WHERE id=?",
                           (newname.lower(), id,))
    if newmarca != "":
        sql_cursor.execute("UPDATE productos SET marca=? WHERE id=?",
                           (newmarca.lower(), id,))
    if newpresentacion != "":
        sql_cursor.execute("UPDATE productos SET presentacion=? WHERE id=?",
                           (newpresentacion.lower(), id,))
    if newpreciocompra != 0:
        sql_cursor.execute(
            "UPDATE productos SET preciocompra=? WHERE id=?", (newpreciocompra, id,))
    if newprecioventa != 0:
        sql_cursor.execute(
            "UPDATE productos SET precioventa=? WHERE id=?", (newprecioventa, id,))
    if newproveedor != "":
        sql_cursor.execute("UPDATE productos SET proveedor=? WHERE id=?",
                           (newproveedor.lower(), id,))
    if newstock != 0:
        sql_cursor.execute(
            "UPDATE productos SET preciocompra=? WHERE id=?", (newstock, id,))
    else:
        pass
    opc = input("\n ¿Esta seguro que desea aplicar estos cambios? si o no: ")
    if opc.lower() == "si" or opc.lower() == "s":
        sql_connection.commit()
        print("\nSe han aplicado los cambios")
        optionmenu()
    elif opc.lower() == "no" or opc.lower() == "n":
        print("\n Los cambios han sido cancelados.")
        optionmenu()


def eliminar_articulo():
    global current_menu
    current_menu = "eliminar_articulo"
    pavaiable = False
    screen.clear()
    screen.draw_header()
    print(' ¡Si ingreso erroneamente escriba la palabra "menu" sin comillas para regresar!\n')
    print("")
    id = input("Codigo del producto a eliminar: ")
    if id.lower() == "menu":
        menu()
    else:
        pass

    sql_cursor.execute("SELECT * FROM productos WHERE id=?", (id,))
    found = sql_cursor.fetchone()
    if len(found) != 0:

        print("\n El codigo ingresado pertenece al producto\n")
        print("\t          Codigo:", found[0])
        print("\t          Nombre:", found[1])
        print("\tMarca/Fabricante:", found[5])
        print("\t    Presentacion:", found[2])
        print("\tStock disponible:", found[7])
        opc = input("\n ¿Esta seguro desea eliminar el producto? si o no: ")

        if opc.lower() == "si" or opc.lower() == "s":
            sql_cursor.execute("DELETE FROM productos WHERE id= ?", (id,))
            sql_connection.commit()
            optionmenu()

        elif opc.lower() == "no" or opc.lower() == "n":
            print("\nSe ha cancelado la operacion\n")
            optionmenu()

    elif len(found) == 0:
        print("\nEl codigo ingresado no existe")
        optionmenu()

    else:
        print("\n¡Error! Ponganse en contacto con el administrador del sistema")


def menu():
    screen.clear()
    screen.draw_header()
    print(" ")
    print("\t[1] Agregar productos")
    print("\t[2] Buscar productos")
    print("\t[3] Todos los productos")
    print("\t[4] Editar producto")
    print("\t[5] Eliminar producto")
    print("\t[6] Salir")

    opc = input("\n¿Que operacion desea realizar? ")

    if opc == "1":
        agregar_articulo()
    elif opc == "2":
        buscar_articulos()
    elif opc == "3":
        mostrar_articulos()
    elif opc == "4":
        modificar_articulo()
    elif opc == "5":
        eliminar_articulo()
    elif opc == "6":
        sql_connection.close()
        exit()
    else:
        menu()
        print("\nIngreso una opcion no valida.")


menu()
