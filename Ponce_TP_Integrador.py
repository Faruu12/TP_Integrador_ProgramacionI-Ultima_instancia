import os

# ============================================================
# 1. Persistencia (Cargar y Guardar)
# ============================================================

def cargar_paises(nombre_archivo):
    paises = []

    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, mode="r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()

            for linea in lineas[1:]:  # Ignorar encabezado
                datos = linea.strip().split(",")

                if len(datos) == 4:
                    nombre = datos[0].strip()
                    pob_str = datos[1].strip()
                    sup_str = datos[2].strip()
                    continente = datos[3].strip()

                    if pob_str.isdigit() and sup_str.isdigit():
                        paises.append({
                            "nombre": nombre,
                            "poblacion": int(pob_str),
                            "superficie": int(sup_str),
                            "continente": continente
                        })

    return paises


def guardar_paises(nombre_archivo, paises):
    with open(nombre_archivo, mode="w", newline="", encoding="utf-8") as archivo:
        archivo.write("nombre,poblacion,superficie,continente\n")

        for pais in paises:
            linea = f"{pais['nombre']},{pais['poblacion']},{pais['superficie']},{pais['continente']}\n"
            archivo.write(linea)


# ============================================================
# 2. Funciones Auxiliares
# ============================================================

def pedir_entero(mensaje):
    while True:
        valor = input(mensaje)
        if valor.isdigit():
            return int(valor)
        else:
            print("Debe ingresar un numero entero positivo.")


def normalizar(texto):
    return texto.strip().lower()


def buscar_pais(paises, nombre):
    nombre = normalizar(nombre)
    for pais in paises:
        if nombre in normalizar(pais["nombre"]):
            return pais
    return None


# ============================================================
# 3. Funcionalidades del Sistema
# ============================================================

def agregar_pais(paises):
    nombre = input("Nombre: ").strip()
    if nombre == "":
        print("El nombre no puede ser vacio.")
        return

    if buscar_pais(paises, nombre):
        print("Ese pais ya existe.")
        return

    poblacion = pedir_entero("Poblacion: ")
    superficie = pedir_entero("Superficie: ")
    continente = input("Continente: ").strip()

    if continente == "":
        print("El continente no puede ser vacio.")
        return

    paises.append({
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente
    })

    print("País agregado correctamente.")


def actualizar_pais(paises):
    nombre = input("Nombre del pais a actualizar: ")
    pais = buscar_pais(paises, nombre)

    if pais is None:
        print("No se encontro el pais.")
        return

    nueva_pob = pedir_entero("Nueva poblacion: ")
    nueva_sup = pedir_entero("Nueva superficie: ")

    pais["poblacion"] = nueva_pob
    pais["superficie"] = nueva_sup

    print("Datos actualizados correctamente.")


def buscar_paises(paises):
    nombre = input("Buscar pais: ")
    nombre = normalizar(nombre)
    encontrados = []

    for pais in paises:
        if nombre in normalizar(pais["nombre"]):
            encontrados.append(pais)

    if len(encontrados) == 0:
        print("No se encontraron coincidencias.")
    else:
        for p in encontrados:
            print(p)


def filtrar_continente(paises):
    cont = normalizar(input("Continente: "))
    filtrados = [p for p in paises if normalizar(p["continente"]) == cont]

    if filtrados:
        for p in filtrados:
            print(p)
    else:
        print("No se encontraron paises en ese continente.")


def filtrar_poblacion(paises):
    mini = pedir_entero("Poblacion minima: ")
    maxi = pedir_entero("Poblacion maxima: ")

    for p in paises:
        if mini <= p["poblacion"] <= maxi:
            print(p)


def filtrar_superficie(paises):
    mini = pedir_entero("Superficie minima: ")
    maxi = pedir_entero("Superficie maxima: ")

    for p in paises:
        if mini <= p["superficie"] <= maxi:
            print(p)


def ordenar_paises(paises):
    print("""
1. Nombre
2. Población
3. Superficie
""")
    op = input("Opción: ")

    orden = input("Ascendente (a) / Descendente (d): ").lower()
    descendente = (orden == "d")

    if op == "1":
        clave = "nombre"
    elif op == "2":
        clave = "poblacion"
    elif op == "3":
        clave = "superficie"
    else:
        print("Opción inválida.")
        return

    # ORDENAMIENTO 
    n = len(paises)
    for i in range(n - 1):
        for j in range(n - 1 - i):

            a = paises[j][clave]
            b = paises[j + 1][clave]

            # Comparación para ascendente o descendente
            if descendente:
                if a < b:
                    paises[j], paises[j + 1] = paises[j + 1], paises[j]
            else:
                if a > b:
                    paises[j], paises[j + 1] = paises[j + 1], paises[j]

    # Mostrar resultado
    print("Paises ordenados:")
    for p in paises:
        print(p)

def estadisticas(paises):
    if len(paises) == 0:
        print("No hay datos cargados.")
        return

    # Mayor y menor población
    mayor = paises[0]
    menor = paises[0]

    for p in paises:
        if p["poblacion"] > mayor["poblacion"]:
            mayor = p
        if p["poblacion"] < menor["poblacion"]:
            menor = p

    total_pob = 0
    total_sup = 0

    for p in paises:
        total_pob += p["poblacion"]
        total_sup += p["superficie"]

    prom_pob = total_pob / len(paises)
    prom_sup = total_sup / len(paises)

    # Conteo por continente
    continentes = {}

    for p in paises:
        cont = p["continente"]
        if cont not in continentes:
            continentes[cont] = 0
        continentes[cont] += 1

    print("\n--- ESTADÍSTICAS ---")
    print("Mayor población:", mayor)
    print("Menor población:", menor)
    print("Promedio población:", prom_pob)
    print("Promedio superficie:", prom_sup)
    print("Cantidad por continente:", continentes)



# ============================================================
# 4. Menú Principal
# ============================================================

def menu():
    ARCHIVO = "paises.csv"
    paises = cargar_paises(ARCHIVO)

    while True:
        print("""
-------------------------
1. Agregar pais
2. Actualizar pais
3. Buscar pais
4. Filtrar por continente
5. Filtrar por poblacion
6. Filtrar por superficie
7. Ordenar paises
8. Estadisticas
9. Guardar y salir
-------------------------
""")
        opcion = input("Opcion: ")

        match opcion:
            case "1":
                agregar_pais(paises)
                guardar_paises(ARCHIVO, paises)
            case "2":
                actualizar_pais(paises)
                guardar_paises(ARCHIVO, paises)
            case "3":
                buscar_paises(paises)
            case "4":
                filtrar_continente(paises)
            case "5":
                filtrar_poblacion(paises)
            case "6":
                filtrar_superficie(paises)
            case "7":
                ordenar_paises(paises)
            case "8":
                estadisticas(paises)
            case "9":
                guardar_paises(ARCHIVO, paises)
                print("Datos guardados. Saliendo...")
                break
            case _:
                print("Opcion no valida.")


if __name__ == "__main__":
    menu()
