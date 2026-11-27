import csv


menu = """
===== SISTEMA DE INVENTARIO =====

1. Registrar producto
2. Registrar entrada
3. Registrar salida
4. Consultar producto
5. Ver inventario
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
def cargar_inventario():
  try:
    with open('inventario.csv', 'r', newline='') as archivo:
      lector = csv.reader(archivo)
      for fila in lector:
        if len(fila) == 4:
          id, nombre, precio, cantidad = fila
          productos[id] = [nombre, float(precio), int(cantidad)]
  except FileNotFoundError:
    pass

def buscar_producto(id):
  if id in productos.keys():
    return True
  else:
    return False

def registrar_producto(id, nombre, precio, cantidad_disponible):
  id = id.lower()
  if id == '' or nombre == '':
    print('el id y el nombre no pueden estar vacios')
    raise ValueError
  if buscar_producto(id):
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

  productos[id] = [nombre, precio, cantidad_disponible]
  assert productos[id] == [nombre, precio, cantidad_disponible], "El producto no se registro correctamente"

def registrar_entrada(id, cantidad_entrada):
  id = id.lower()
  if not buscar_producto(id):
    print('Dicho producto no existe')
    raise ValueError

  cantidad_entrada = int(cantidad_entrada)
  if cantidad_entrada <= 0:
    print('la cantidad debe ser mayor a 0')
    raise ValueError

  cantidad_anterior = productos[id][2]
  productos[id][2] += cantidad_entrada
  print(f'Nuevo total de {productos[id][0]}: {productos[id][2]}')
  assert productos[id][2] == cantidad_anterior + cantidad_entrada, "La entrada no se sumo correctamente"

def registrar_salida(id, cantidad_salida):
  id = id.lower()
  if not buscar_producto(id):
    print('Dicho producto no existe')
    raise ValueError

  cantidad_salida = int(cantidad_salida)
  if cantidad_salida <= 0:
    print('la cantidad debe ser mayor a 0')
    raise ValueError
  elif cantidad_salida > productos[id][2]:
    print('No hay suficiente cantidad de producto')
    raise ValueError

  cantidad_anterior = productos[id][2]
  productos[id][2] -= cantidad_salida
  print(f'Salida registrada correctamente. Nuevo total de {productos[id][0]}: {productos[id][2]}')
  assert productos[id][2] == cantidad_anterior - cantidad_salida, "La salida no se resto correctamente"

def mostrar_inventario():
  if len(productos) == 0:
    print('El inventario esta vacio')
    return
  mostrados = 0
  for id in productos:
    nombre, precio, cantidad = productos[id]
    print(f'id: {id}\nNombre: {nombre}\nPrecio: {precio}\nCantidad disponible: {cantidad}\nValor total en inventarios: {precio * cantidad}')
    mostrados += 1
  assert mostrados == len(productos), "No se mostraron todos los productos del inventario"

def encontrar_producto_mayor():
  if len(productos) == 0:
    raise ValueError

  producto_mayor = list(productos)[0]

  for producto in productos:
    if productos[producto][2] > productos[producto_mayor][2]:
      producto_mayor = producto

  return productos[producto_mayor][0]

def calcular_estadisticas():
  valor_total = 0
  for id in productos:
    nombre, precio, cantidad = productos[id]
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
      id, nombre, precio, cantidad_disponible = input("Cual sera el id del producto?\n"), input("Cual sera el nombre del producto?\n"), input('Cual sera el precio del producto?\n'), input("Cual sera la cantidad disponible del producto?\n")
      registrar_producto(id, nombre, precio, cantidad_disponible)
    case 2:
      id, cantidad_entrada = input('Cual es el id del producto?\n'), input('Cual es la cantidad recibida?\n')
      registrar_entrada(id, cantidad_entrada)
    case 3:
      id, cantidad_salida = input('Cual es el id del producto?\n'), input('Cual es la cantidad a retirar?\n')
      registrar_salida(id, cantidad_salida)
    case 4:
      id = input('Cual es el id del producto?\n').lower()
      if buscar_producto(id):
        nombre, precio, cantidad = productos[id]
        print(f'id: {id}\nNombre: {nombre}\nPrecio: {precio}\nCantidad disponible: {cantidad}\nValor total en inventarios: {precio * cantidad}')
      else:
        print('Dicho producto no existe')
      assert buscar_producto(id) == (id in productos), "La consulta del producto fallo"
    case 5:
      mostrar_inventario()

cargar_inventario()

while True:
  opcion = elegir_opcion()

  if opcion == 6:
    if len(productos.keys()) != 0:
      with open('inventario.csv', 'w', newline='') as archivo:
        escritor = csv.writer(archivo)
        for id in productos:
          nombre, precio, cantidad_disponible = productos[id]
          escritor.writerow([id, nombre, precio, cantidad_disponible])
      with open('inventario.csv', 'r', newline='') as archivo:
        assert len(list(csv.reader(archivo))) == len(productos), "No se guardaron todos los productos en el archivo"
    break
  try:
    opcion_n(opcion)
  except ValueError:
    print('No se ha podido concretar tu opcion, intentalo de nuevo.')
