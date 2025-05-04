class Cliente:
    def __init__(self, dni, nombre, apellido):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
    def __str__(self):
        return f"({self.dni}) {self.nombre} {self.apellido}"
    
class Clientes:
    lista = []
    @staticmethod
    def buscar(dni):
        for cliente in Clientes.lista:
            if cliente.dni == dni:
                return cliente
            
@staticmethod
def crear(dni, nombre, apellido):
    cliente = Cliente(dni, nombre, apellido)
    Clientes.lista.append(cliente)
    return cliente

@staticmethod
def modificar(dni, nombre, apellido):
    for i, cliente in enumerate(Clientes.lista):
        if cliente.dni == dni:
            Clientes.lista[i].nombre = nombre
            Clientes.lista[i].apellido = apellido
            return Clientes.lista[i]
        
@staticmethod
def borrar(dni):
    for i, cliente in enumerate(Clientes.lista):
        if cliente.dni == dni:
            cliente = Clientes.lista.pop(i)
            return cliente
        
import config  # Ensure the config module is imported and defined elsewhere

class Clientes:
    lista = []

    @staticmethod
    def guardar():
        with open(config.DATABASE_PATH, "w", newline="\n") as fichero:
            for cliente in Clientes.lista:
                fichero.write(f"{cliente.dni},{cliente.nombre},{cliente.apellido}\n")