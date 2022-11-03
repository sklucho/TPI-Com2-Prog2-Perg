import sqlite3
class ProgramaPrincipal:

    def menu(self):

        while True:
            print("*** Monopatines Eléctricos ***")
            print("")
            print("1- Cargar monopatin")
            print("2- Modificar precio")
            print("3- Borrar monopatin")
            print("4- Agregar disponibilidad")
            print("5- Mostrar lista de productos")
            print("6- Actualizar precios a inflación del 23%")
            print("7- Mostrar lista por fecha")
            print("0- Salir de menu")
            
            nro = 10

            try:
                while nro < 0 or nro > 7:
                    nro = int(input("Ingrese una opcion del 0 al 7: "))
            except:
                print("")
                print("Error: ingrese un valor numerico")
                print("")
            finally:
                if nro == 1: #Carga 
                    marca = (input("Por favor ingrese la marca del monopatin: ")).lower()
                    modelo = (input("Por favor ingrese el modelo: ")).lower()
                    precio = input("Por favor ingrese el precio del monopatin: ")
                    potencia = input("Por favor ingrese la potencia del monopatin: ")
                    color = (input("Por favor ingrese el color del monopatin: ")).lower()
                    fechaUltimoPrecio = input("Por favor ingrese la fecha en la que carga los datos (Formato AAAA-MM-DD): ")
                    cantidadDisponibles = input("Ingrese la cantidad de monopatines: ")
                    nuevo_monopatin = Monopatin(marca,modelo,precio,potencia,color,fechaUltimoPrecio,cantidadDisponibles)
                    nuevo_monopatin.cargar_monopatin()

                elif nro == 2: #Modificar Precio
                    marca = (input("Por favor ingrese el nombre de la marca: ")).lower()
                    modelo = (input("Por favor ingrese el modelo del monopatin: ")).lower()
                    precio = input("Por favor ingrese el nuevo precio: ")
                    monopatin_a_modificar=Monopatin(marca,modelo,precio)
                    monopatin_a_modificar.modificar_monopatines()

                elif nro == 3: #Borrar Datos
                    marca = (input("Por favor ingrese la marca del monopatin: ")).lower()
                    modelo = (input("Por favor ingrese el modelo: ")).lower()
                    monopatin_a_eliminar = Monopatin(marca,modelo)
                    monopatin_a_eliminar.eliminar_monopatines()

                elif nro == 4: #Agregar Stock
                    marca = (input("Por favor ingrese el nombre de la marca: ")).lower()
                    modelo = (input("Por favor ingrese el modelo: ")).lower()
                    cantidadDisponibles = input("Por favor ingrese el nuevo stock: ")
                    monopatin_ingresado = Monopatin(marca, modelo, 0,0,0,0,cantidadDisponibles)
                    monopatin_ingresado.aumentar_stock()

                elif nro == 5: #Mostrar Ordenadamente
                    print("")
                    lista_monopatines=Monopatin(0,0)
                    lista_monopatines.cargar_lista()

                elif nro == 6: #Actualizar Precios a la Inflación
                    print("")
                    historia_monopatines=Monopatin(0,0)
                    historia_monopatines.actualizar_lista()

                elif nro == 7: #Lista por fecha
                    fechaUltimoPrecio= input("Ingrese la fecha: ")
                    mostrar_por_fecha= Monopatin(0,0,0,0,0,fechaUltimoPrecio)
                    mostrar_por_fecha.lista_por_fecha()

                elif nro == 0: #Salir del Programa
                    print("Ha salido del programa...")
                    break

    
    #creacion de base de datos
    def crearDB(self): 
        conn = sqlite3.connect("Monopatines.db") 
        conn.commit()
        conn.close()

    #se crean las tablas
    def crearTablas(self): 

        conexion = Conexiones()
        conexion.abrirConexion()

        conexion.miCursor.execute(
            """CREATE TABLE IF NOT EXISTS MONOPATINES(
                ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                marca VARCHAR(30),
                modelo INTEGER,
                precio FLOAT NOT NULL,
                potencia Varchar(30),
                color Varchar(30),
                fechaUltimoPrecio datetime,
                cantidadDisponibles INTEGER NOT NULL
            )"""
        )
        conexion.miConexion.commit()
        conexion.cerrarConexion()
 

    #tabla historica
    def crear_historial(self): 
        conexion = Conexiones()
        conexion.abrirConexion()

        conexion.miCursor.execute(
            """CREATE TABLE IF NOT EXISTS HISTORICO_MONO(
                NUM INTEGER PRIMARY KEY AUTOINCREMENT,
                ID INTEGER,
                marca VARCHAR(30),
                modelo INTEGER,
                precio FLOAT NOT NULL,
                potencia Varchar(30),
                color Varchar(30),
                fechaUltimoPrecio datetime,
                cantidadDisponibles INTEGER NOT NULL
            )"""
        )
        conexion.miConexion.commit()
        conexion.cerrarConexion()
    
class Monopatin:
    def __init__(self, marca, modelo,precio=None,potencia=None,color=None,fechaUltimoPrecio=None, cantidadDisponibles=None,id=None, inflacion=None):
        self.marca = marca
        self.modelo = modelo
        self.potencia = potencia
        self.color = color
        self.precio = precio
        self.fechaUltimoPrecio = fechaUltimoPrecio
        self.cantidadDisponibles = cantidadDisponibles
        self.id = id
        self.inflacion = inflacion

    #1
    def cargar_monopatin(self): 
        conexion = Conexiones()
        conexion.abrirConexion()

        try:
            conexion.miCursor.execute(f"INSERT INTO MONOPATINES (marca,modelo,precio,potencia,color,fechaUltimoPrecio,cantidadDisponibles) VALUES ('{self.marca}', '{self.modelo}','{self.precio}','{self.potencia}','{self.color}','{self.fechaUltimoPrecio}','{self.cantidadDisponibles}')")
            conexion.miConexion.commit()
            print("")
            print("monopatin cargado exitosamente")
        except:
            print("")
            print("Error al agregar un monopatin")
        finally:
            conexion.miCursor.execute(F"INSERT INTO HISTORICO_MONO (ID, marca, modelo, precio, potencia, color, fechaUltimoPrecio, cantidadDisponibles) SELECT ID, marca, modelo, precio, potencia, color, fechaUltimoPrecio, cantidadDisponibles FROM MONOPATINES where marca='{self.marca}' AND modelo='{self.modelo}' AND precio='{self.precio}' AND potencia='{self.potencia}' AND color='{self.color}' AND fechaUltimoPrecio= '{self.fechaUltimoPrecio}' AND cantidadDisponibles='{self.cantidadDisponibles}'")
            conexion.miConexion.commit()    
            conexion.cerrarConexion()

    #2
    def modificar_monopatines(self): 
        
        conexion = Conexiones()
        conexion.abrirConexion()
        instruccion= f"UPDATE MONOPATINES SET precio='{self.precio}' where marca='{self.marca}' AND modelo='{self.modelo}'"
        try:
            conexion.miCursor.execute(instruccion)
            conexion.miConexion.commit()
            print("")
            print("Precio modificado correctamente")
        except:
            print("")
            print('Error al actualizar un monopatin')
        finally:
            conexion.cerrarConexion()  

    #3
    def eliminar_monopatines(self): 
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute(f"DELETE FROM MONOPATINES WHERE marca='{self.marca}' AND modelo='{self.modelo}'")
            conexion.miConexion.commit()
            print("")
            print("Monopatin eliminado correctamente")
        except:
            print("")
            print('Error al eliminar un monopatin')
        finally:
            conexion.cerrarConexion() 

    #4
    def aumentar_stock(self): 
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute(f"UPDATE MONOPATINES SET cantidadDisponibles={self.cantidadDisponibles} WHERE marca='{self.marca}' AND modelo='{self.modelo}'")
            conexion.miConexion.commit()
            print("")
            print("Stock actualizado correctamente")
        except:
            print("")
            print('Error al aumentar el stock')
        finally:
            conexion.miCursor.execute(f"INSERT INTO HISTORICO_MONO (ID, marca, modelo, precio, potencia, color, fechaUltimoPrecio, cantidadDisponibles) SELECT ID, marca, modelo, precio, potencia, color, fechaUltimoPrecio, cantidadDisponibles FROM MONOPATINES WHERE marca='{self.marca}' AND modelo='{self.modelo}'")
            conexion.miConexion.commit()           
            conexion.cerrarConexion()


    #5
    def cargar_lista(self): 
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute("SELECT * FROM MONOPATINES")
            datos = conexion.miCursor.fetchall()
            print(datos)
            conexion.miConexion.commit()
            print("[ID, MARCA, MODELO, PRECIO, POTENCIA, COLOR, FECHA, DISPONIBLE]")
            print("")
            print("Lista cargada correctamente")
        except:
            print("")
            print('Error al mostrar la lista de productos')
        finally:
            conexion.cerrarConexion()

    #6
    def actualizar_lista(self): 
        conexion = Conexiones()
        conexion.abrirConexion()
        self.inflacion = 0.23

        try:
            conexion.miCursor.execute(f"UPDATE MONOPATINES SET precio='{self.inflacion}'*precio+precio")
            conexion.miConexion.commit()            
            print("")
            print("Precios actualizados correctamente")
        except:
            print("")
            print("Error al actualizar los precios segun el aumento del dolar")
        finally:
            conexion.miCursor.execute("INSERT INTO HISTORICO_MONO (ID, marca, modelo, precio, potencia, color, fechaUltimoPrecio, cantidadDisponibles) SELECT ID, marca, modelo, precio, potencia, color, fechaUltimoPrecio, cantidadDisponibles FROM MONOPATINES")
            conexion.miConexion.commit()            
            conexion.cerrarConexion()

    #7
    def lista_por_fecha(self): 
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute(f"SELECT * FROM MONOPATINES WHERE fechaUltimoPrecio>='{self.fechaUltimoPrecio}' ORDER BY fechaUltimoPrecio")
            datos = conexion.miCursor.fetchall()
            print("")
            print(datos)
        except:
            print("")
            print('Error, fecha no encontrada')
        finally:
            conexion.cerrarConexion()

#conexiones y salidas
class Conexiones: 
    
    def abrirConexion(self): 
        self.miConexion = sqlite3.connect("Monopatines.db")
        self.miCursor = self.miConexion.cursor()
        
    def cerrarConexion(self):
        self.miConexion.close()   


programa = ProgramaPrincipal() 
programa.crearDB()  
programa.crearTablas() 
programa.crear_historial()
programa.menu()  