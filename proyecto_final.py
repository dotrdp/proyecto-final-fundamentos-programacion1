
import csv


menu = """
===== SISTEMA DE INVENTARIO =====

1. Registrar producto
2. Mostrar inventario
3. Buscar producto
4. Registrar salida
5. Guardar y salir

Seleccione una opción:
"""

def elegir_opcion():
  '''
  Devuelve una opcion valida directamente atada a las opciones mostradas en el menu.
  '''
  # hacer docstring permite a servidores de lenguaje mostrar datos sobre una funcion directamente en el editor de texto

  rango_valido = range(1, 6)
  opcion = input(menu)

  # si funciona el return va a devolver la opcion
  try:
    # intenta hacerlo un entero
    opcion = int(opcion)

    # si no esta en el rango valido, tambien dispara un error
    if opcion not in rango_valido:
      raise ValueError

    # si funciona entonces se devuelve la salida
    return opcion
  # aqui llega si las anteriores verificaciones fallaron
  except ValueError:
    # se le notifica al usuario
    print("Se ha intentado ingresar una opción no valida")
    print('intentalo de nuevo')

    # se devuelve la misma funcion anidada, lo cual hace que se repita hasta que no fallen las verificaciones
    return elegir_opcion()

productos = {}
def buscar_producto(nombre):
  if nombre in productos.keys():
    return True
  else:
    return False

def registrar_producto(nombre, precio, cantidad_disponible):
  if buscar_producto(nombre):
    print("Dicho producto, ya existe")
    raise ValueError()

  precio = float(precio)
  cantidad_disponible = int(cantidad_disponible)

  if precio <= 0:
    print('el precio no puede ser 0 o negativo')
    raise ValueError
  elif cantidad_disponible < 0:
    print('la cantidad disponible no puede ser negativa')
    raise ValueError

  productos[nombre.lower()] = [precio, cantidad_disponible]

def mostrar_inventario():
  for nombre in productos:
    precio, cantidad = productos[nombre]
    print(f'Nombre: {nombre}\nPrecio: {precio}\nCantidad disponible: {cantidad}\nValor total en inventarios: {precio * cantidad}')

def encontrar_producto_mayor():
  if len(productos) == 0:
    raise ValueError

  producto_mayor = list(productos)[0]

  # algoritmo sort raro
  for producto in productos:
    if productos[producto][1] > productos[producto_mayor][1]:
      producto_mayor = producto

  return producto_mayor


def calcular_estadisticas():
  valor_total = 0
  for nombre in productos:
    precio, cantidad = productos[nombre]
    valor_total += precio * cantidad

  producto_mayor = encontrar_producto_mayor()
  estadisticas = f'''
===== ESTADÍSTICAS =====

Productos registrados: {len(productos.keys())}
Valor total: ${valor_total}
Mayor existencia: {producto_mayor}
'''
  print(estadisticas)



def opcion_n(opcion):
  match opcion:
    case 1:
      nombre, precio, cantidad_disponible = input("Cual sera el nombre del producto?\n"), input('Cual sera el precio del producto?\n'), input("Cual sera la cantidad disponible del producto?\n")
      registrar_producto(nombre, precio, cantidad_disponible)
    case 2:
      mostrar_inventario()

    case 3:
      nombre = input('Cual es el nombre del producto?\n').lower()
      if buscar_producto(nombre):
        precio, cantidad = productos[nombre]
        print(f'Nombre: {nombre}\nPrecio: {precio}\nCantidad disponible: {cantidad}\nValor total en inventarios: {precio * cantidad}')
      else:
        print('Dicho producto no existe')

    # Rafa funcionalidad de Registrar salida
    case 4:

      nombre = input("Ingrese el nombre del producto: \n")

      if nombre not in productos:
        print("Ingresa otro producto, este no")
        return

      cantidad_salida = int(input("Ingresa la cantidad de productos a retirar: \n"))
      if cantidad_salida <= 0:
        print("No hay cantidad a retirar")
        return

      if cantidad_salida > productos[nombre][1]:
        print("No hay esa cantidad de producto")
        return
      productos[nombre][1] -= cantidad_salida
      print("Salida registrada correctamente")


      # Aqui implementa la funcionalidad de registrar salida
      # Es lo mismo que agregar producto, pero es tipo que lo quita
      # Tiene que exitir, y revisa que se pueda quitar esa cantidad
      # de producto, si no se puede, entonces le devuelve un error al usuario
      # el error se devuelve con `raise ValueError()`, donde sea que lo pongas
      # el codigo try en el ciclo abajo, lo va a capturar, entonces ahi puedes poner un print con el mensaje para el usuario como se muestra en la linea 64
      

# ciclo principal
while True:
  opcion = elegir_opcion()

  if opcion == 5:
    if len(productos.keys()) != 0:
      with open('inventario.txt', 'w') as archivo:
        escritor = csv.writer(archivo)
        for producto in productos:
          precio, cantidad_disponible = productos[producto]
          escritor.writerow([producto, precio, cantidad_disponible])
    break
  try:
    opcion_n(opcion)
  except ValueError:
    print('No se ha podido concretar tu opcion, intentalo de nuevo.')

