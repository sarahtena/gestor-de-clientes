import os
import helpers
from gestor import db

def mostrar_menu():
    os.system('cls' if os.name == 'nt' else 'clear')  # cls en Windows, clear en otros sistemas
    print("========================")
    print(" BIENVENIDO AL Manager ")
    print("========================")
    print("[1] Listar clientes ")
    print("[2] Buscar cliente ")
    print("[3] Añadir cliente ")
    print("[4] Modificar cliente ")
    print("[5] Borrar cliente ")
    print("[6] Cerrar el Manager ")
    print("========================")

def listar_clientes():
    print("Listando los clientes...\n")
    for cliente in db.Clientes.lista:
        print(cliente)

def buscar_cliente():
    print("Buscando un cliente...\n")
    dni = helpers.leer_texto(3, 3, "DNI (2 ints y 1 char)").upper()
    cliente = db.Clientes.buscar(dni)
    print(cliente) if cliente else print("Cliente no encontrado.")

def añadir_cliente():
    print("Añadiendo un cliente...\n")
    dni = helpers.leer_texto(3, 3, "DNI (2 ints y 1 char)").upper()
    nombre = helpers.leer_texto(2, 30, "Nombre (de 2 a 30 chars)").capitalize()
    apellido = helpers.leer_texto(2, 30, "Apellido (de 2 a 30 chars)").capitalize()
    db.Clientes.crear(dni, nombre, apellido)
    print("Cliente añadido correctamente.")

def modificar_cliente():
    print("Modificando un cliente...\n")
    dni = helpers.leer_texto(3, 3, "DNI (2 ints y 1 char)").upper()
    cliente = db.Clientes.buscar(dni)
    if cliente:
        nombre = helpers.leer_texto(2, 30, f"Nombre (de 2 a 30 chars) [{cliente.nombre}]").capitalize()
        apellido = helpers.leer_texto(2, 30, f"Apellido (de 2 a 30 chars) [{cliente.apellido}]").capitalize()
        db.Clientes.modificar(cliente.dni, nombre, apellido)
        print("Cliente modificado correctamente.")
    else:
        print("Cliente no encontrado.")

def borrar_cliente():
    print("Borrando un cliente...\n")
    dni = helpers.leer_texto(3, 3, "DNI (2 ints y 1 char)").upper()
    print("Cliente borrado correctamente.") if db.Clientes.borrar(dni) else print("Cliente no encontrado.")

def iniciar():
    while True:
        mostrar_menu()
        opcion = input("> ")
        os.system('cls' if os.name == 'nt' else 'clear')  # cls en Windows, clear en otros sistemas

        if opcion == '1':
            listar_clientes()
        elif opcion == '2':
            buscar_cliente()
        elif opcion == '3':
            añadir_cliente()
        elif opcion == '4':
            modificar_cliente()
        elif opcion == '5':
            borrar_cliente()
        elif opcion == '6':
            print("Saliendo...\n")
            break
        else:
            print("Opción no válida.")

        input("\nPresiona ENTER para continuar...")
        
        if opcion == '3':
            print("Añadiendo un cliente...\n")
            while 1:
                dni = helpers.leer_texto(3, 3, "DNI (2 ints y 1 har)").upper()
                if helpers.dni_valido(dni, db.Clientes.lista):
                    break
            nombre = helpers.leer_texto(
                2, 30, "Nombre (de 2 a 30 chars)").capitalize()
            apellido = helpers.leer_texto(
                2, 30, "Apellido (de 2 a 30 chars)").capitalize()
            db.Clientes.crear(dni, nombre, apellido)
