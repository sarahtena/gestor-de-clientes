from tkinter import *
from tkinter import ttk
import database as db  # Asegúrate de que este módulo exista y sea correcto

class CenterWidgetMixin:
    def center(self):
        self.update()
        w = self.winfo_width()
        h = self.winfo_height()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = int((ws / 2) - (w / 2))
        y = int((hs / 2) - (h / 2))
        self.geometry(f"{w}x{h}+{x}+{y}")

class MainWindow(Tk, CenterWidgetMixin):
    def __init__(self):
        super().__init__()
        self.title('Gestor de clientes')
        self.build()
        self.center()

    def build(self):
        # Main frame
        main_frame = Frame(self)
        main_frame.pack(fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(main_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.treeview = ttk.Treeview(main_frame, yscrollcommand=scrollbar.set)
        self.treeview['columns'] = ('DNI', 'Nombre', 'Apellido')
        self.treeview.column("#0", width=0, stretch=NO)
        self.treeview.column("DNI", anchor=CENTER)
        self.treeview.column("Nombre", anchor=CENTER)
        self.treeview.column("Apellido", anchor=CENTER)
        self.treeview.heading("#0", text="", anchor=CENTER)
        self.treeview.heading("DNI", text="DNI", anchor=CENTER)
        self.treeview.heading("Nombre", text="Nombre", anchor=CENTER)
        self.treeview.heading("Apellido", text="Apellido", anchor=CENTER)
        self.treeview.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar.config(command=self.treeview.yview)

        # Populate the treeview with data
        self.populate_treeview()

        # Button frame
        button_frame = Frame(self)
        button_frame.pack(pady=20)

        # Buttons
        Button(button_frame, text="Crear", command=self.create_client).grid(row=0, column=0, padx=5)
        Button(button_frame, text="Modificar", command=self.modify_client).grid(row=0, column=1, padx=5)
        Button(button_frame, text="Borrar", command=self.delete_client).grid(row=0, column=2, padx=5)

    def populate_treeview(self):
        for cliente in db.Clientes.lista:
            self.treeview.insert(
                parent='', index='end', iid=cliente.dni,
                values=(cliente.dni, cliente.nombre, cliente.apellido)
            )

    def create_client(self):
        # Lógica para crear un cliente
        pass

    def modify_client(self):
        # Lógica para modificar un cliente
        pass

    def delete_client(self):
        # Lógica para borrar un cliente
        pass

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()

from tkinter.messagebox import askokcancel, WARNING

def delete(self):
    cliente = self.treeview.focus()
    if cliente:
        campos = self.treeview.item(cliente, 'values')
        confirmar = askokcancel(
            title='Confirmación', 
            message=f'¿Borrar a {campos[1]} {campos[2]}?', 
            icon=WARNING
        )
        if confirmar:
            # remove the row
            self.treeview.delete(cliente)

class CreateClientWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Crear cliente')
        self.build()
        self.center()
        # Obligar al usuario a interactuar con la subventana
        self.transient(parent)
        self.grab_set()

    def build(self):
        # Top frame
        frame = Frame(self)
        frame.pack(padx=20, pady=10)
        # Labels
        Label(frame, text="DNI (2 ints y 1 upper char)").grid(row=0, column=0)
        Label(frame, text="Nombre (2 a 30 chars)").grid(row=0, column=1)
        Label(frame, text="Apellido (2 a 30 chars)").grid(row=0, column=2)
        # Entries
        dni = Entry(frame)
        dni.grid(row=1, column=0)
        nombre = Entry(frame)
        nombre.grid(row=1, column=1)
        apellido = Entry(frame)
        apellido.grid(row=1, column=2)
        # Bottom frame
        frame = Frame(self)
        frame.pack(pady=10)
        # Buttons
        crear = Button(frame, text="Crear", command=self.create_client)
        crear.configure(state=DISABLED)
        crear.grid(row=0, column=0)
        Button(frame, text="Cancelar", command=self.close).grid(row=0, column=1)

    def create_client(self):
        pass
    
    def close(self):
        self.destroy()
        self.update()

    def create_client_window(self):
        CreateClientWindow(self)

    def validate(self, event, index):
        valor = event.widget.get()
        import helpers  # Ensure helpers module is imported
        valido = helpers.dni_valido(valor, db.Clientes.lista) if index == 0 else (valor.isalpha() and len(valor) >= 2 and len(valor) <= 30)
        event.widget.configure({"bg": "Green" if valido else "Red"})
        # Cambiar estado del botón en base a las validaciones
        self.validaciones[index] = valido
        self.crear.config(state=NORMAL if self.validaciones == [1, 1, 1] else DISABLED)

    def create_client(self):
        self.master.treeview.insert(
            parent='', index='end', iid=self.dni.get(),
            values=(self.dni.get(), self.nombre.get(), self.apellido.get())
        )
        self.close()

    def build(self):
        # Top frame
        frame = Frame(self)
        frame.pack(padx=20, pady=10)
        # Labels
        Label(frame, text="DNI (2 ints y 1 upper char)").grid(row=0, column=0)
        Label(frame, text="Nombre (2 a 30 chars)").grid(row=0, column=1)
        Label(frame, text="Apellido (2 a 30 chars)").grid(row=0, column=2)
        # Entries
        dni = Entry(frame)
        dni.grid(row=1, column=0)
        dni.bind("<KeyRelease>", lambda ev: self.validate(ev, 0))
        nombre = Entry(frame)
        nombre.grid(row=1, column=1)
        nombre.bind("<KeyRelease>", lambda ev: self.validate(ev, 1))
        apellido = Entry(frame)
        apellido.grid(row=1, column=2)
        apellido.bind("<KeyRelease>", lambda ev: self.validate(ev, 2))
        # Bottom frame
        frame = Frame(self)
        frame.pack(pady=10)
        # Buttons
        crear = Button(frame, text="Crear", command=self.create_client)
        crear.configure(state=DISABLED)
        crear.grid(row=0, column=0)
        Button(frame, text="Cancelar", command=self.close).grid(row=0, column=1)

        # Class exports
        self.crear = crear
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

def create_client(self):
    self.master.treeview.insert(
        parent='', index='end', iid=self.dni.get(),
        values=(self.dni.get(), self.nombre.get(),
                self.apellido.get()))
    self.close()

class EditClientWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Actualizar cliente')
        self.build()
        self.center()
        # Obligar al usuario a interactuar con la subventana
        self.transient(parent)
        self.grab_set()

    def build(self):
        # Top frame
        frame = Frame(self)
        frame.pack(padx=20, pady=10)
        # Labels
        Label(frame, text="DNI (no editable)").grid(row=0, column=0)
        Label(frame, text="Nombre (2 a 30 chars)").grid(row=0, column=1)
        Label(frame, text="Apellido (2 a 30 chars)").grid(row=0, column=2)
        # Entries
        dni = Entry(frame)
        dni.grid(row=1, column=0)
        nombre = Entry(frame)
        nombre.grid(row=1, column=1)
        nombre.bind("<KeyRelease>", lambda ev: self.validate(ev, 0))
        apellido = Entry(frame)
        apellido.grid(row=1, column=2)
        apellido.bind("<KeyRelease>", lambda ev: self.validate(ev, 1))
        # Set entries initial values
        cliente = self.master.treeview.focus()
        campos = self.master.treeview.item(cliente, 'values')
        dni.insert(0, campos[0])
        dni.config(state=DISABLED)
        nombre.insert(0, campos[1])
        apellido.insert(0, campos[2])
        # Bottom frame
        frame = Frame(self)
        frame.pack(pady=10)
        # Buttons
        actualizar = Button(frame, text="Actualizar", command=self.update_client)
        actualizar.grid(row=0, column=0)
        Button(frame, text="Cancelar", command=self.close).grid(row=0, column=1)
        # Update button activation
        self.validaciones = [1, 1]  # True, True
        # Class exports
        self.actualizar = actualizar
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    def validate(self, event, index):
        valor = event.widget.get()
        valido = valor.isalpha() and 2 <= len(valor) <= 30
        event.widget.configure({"bg": "Green" if valido else "Red"})
        # Cambiar estado del botón en base a las validaciones
        self.validaciones[index] = valido
        self.actualizar.config(state=NORMAL if self.validaciones == [1, 1] else DISABLED)

    def update_client(self):
        cliente = self.master.treeview.focus()
        # Sobreescribimos los datos de la fila seleccionada
        self.master.treeview.item(
            cliente, values=(self.dni.get(), self.nombre.get(), self.apellido.get())
        )
        self.close()

    def close(self):
        self.destroy()
        self.update()
def delete(self):
    cliente = self.treeview.focus()
    if cliente:
        campos = self.treeview.item(cliente, 'values')
        confirmar = askokcancel(
            title='Confirmación',
            message=f'¿Borrar a {campos[1]} {campos[2]}?',
            icon=WARNING
        )
        if confirmar:
            self.treeview.delete(cliente)
            # Borrar también en el fichero
            db.Clientes.borrar(campos[0])

def create_client(self):
    self.master.treeview.insert(
        parent='', index='end', iid=self.dni.get(),
        values=(self.dni.get(), self.nombre.get(), self.apellido.get())
    )
    # Crear también en el fichero
    db.Clientes.crear(self.dni.get(), self.nombre.get(), self.apellido.get())
    self.close()

def update_client(self):
    cliente = self.master.treeview.focus()
    # Sobreescribir los datos
    self.master.treeview.item(
        cliente, values=(self.dni.get(), self.nombre.get(), self.apellido.get())
    )
    # Modificar también en el fichero
    db.Clientes.modificar(self.dni.get(), self.nombre.get(), self.apellido.get())
    self.close()

import sys
import menu
import ui
if __name__ == "__main__":
    # Si pasamos un argumento -t lanzamos el modo terminal
    if len(sys.argv) > 1 and sys.argv[1] == "-t":
        menu.iniciar()
    # En cualquier otro caso lanzamos el modo gráfico
    else:
        app = ui.MainWindow()
        app.mainloop()
