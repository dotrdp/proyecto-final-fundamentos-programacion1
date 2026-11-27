import csv


menu = """
===== SISTEMA DE INVENTARIO =====

1. Registrar producto
2. Registrar entrada
3. Registrar salida
4. Buscar producto
5. Mostrar inventario
6. Guardar y salir

Seleccione una opción:
"""

def elegir_opcion():
  rango_valido = range(1, 7)
  opcion = input(menu)

  try:
    opcion = int(opcion)

    if opcion not in rango_valido:
      raise ValueError

    return opcion
  except ValueError:
    print("Se ha intentado ingresar una opción no valida")
    print('intentalo de nuevo')

    return elegir_opcion()

productos = {}
def buscar_producto(nombre):
  if nombre in productos.keys():
    return True
  else:
    return False

def registrar_producto(nombre, precio, cantidad_disponible):
  if buscar_producto(nombre.lower()):
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

def registrar_entrada(nombre, cantidad_entrada):
  nombre = nombre.lower()
  if not buscar_producto(nombre):
    print('Dicho producto no existe')
    raise ValueError

  cantidad_entrada = int(cantidad_entrada)
  if cantidad_entrada <= 0:
    print('la cantidad debe ser mayor a 0')
    raise ValueError

  productos[nombre][1] += cantidad_entrada
  print(f'Nuevo total de {nombre}: {productos[nombre][1]}')

def registrar_salida(nombre, cantidad_salida):
  nombre = nombre.lower()
  if not buscar_producto(nombre):
    print('Dicho producto no existe')
    raise ValueError

  cantidad_salida = int(cantidad_salida)
  if cantidad_salida <= 0:
    print('la cantidad debe ser mayor a 0')
    raise ValueError
  elif cantidad_salida > productos[nombre][1]:
    print('No hay suficiente cantidad de producto')
    raise ValueError

  productos[nombre][1] -= cantidad_salida
  print(f'Salida registrada correctamente. Nuevo total de {nombre}: {productos[nombre][1]}')

def mostrar_inventario():
  if len(productos) == 0:
    print('El inventario esta vacio')
    return
  for nombre in productos:
    precio, cantidad = productos[nombre]
    print(f'Nombre: {nombre}\nPrecio: {precio}\nCantidad disponible: {cantidad}\nValor total en inventarios: {precio * cantidad}')

def encontrar_producto_mayor():
  if len(productos) == 0:
    raise ValueError

  producto_mayor = list(productos)[0]

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
      nombre, cantidad_entrada = input('Cual es el nombre del producto?\n'), input('Cual es la cantidad recibida?\n')
      registrar_entrada(nombre, cantidad_entrada)
    case 3:
      nombre, cantidad_salida = input('Cual es el nombre del producto?\n'), input('Cual es la cantidad a retirar?\n')
      registrar_salida(nombre, cantidad_salida)
    case 4:
      nombre = input('Cual es el nombre del producto?\n').lower()
      if buscar_producto(nombre):
        precio, cantidad = productos[nombre]
        print(f'Nombre: {nombre}\nPrecio: {precio}\nCantidad disponible: {cantidad}\nValor total en inventarios: {precio * cantidad}')
      else:
        print('Dicho producto no existe')
    case 5:
      mostrar_inventario()

while True:
  opcion = elegir_opcion()

  if opcion == 6:
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
