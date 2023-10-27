import sqlite3
import re

# Conectar a la base de datos
conn = sqlite3.connect('imagenes.db')
cursor = conn.cursor()

# Pedir al usuario que ingrese el nombre del archivo RSC que desea consultar
filename_to_check = input("Por favor, ingresa el nombre del archivo RSC que deseas consultar (ejemplo: RSC #3.png): ")

# Expresión regular para validar el formato
pattern = r'RSC #(\d+)\.png'
match = re.match(pattern, filename_to_check)

if match:
    rsc_number = match.group(1)

    # Consultar las capas asociadas al archivo RSC
    query = "SELECT background, bodies, eyes, hats FROM imagenes WHERE filename = ?"
    cursor.execute(query, (filename_to_check,))
    result = cursor.fetchone()

    if result:
        background, bodies, eyes, hats = result

        # Consultar el número de veces que ha aparecido cada elemento en la base de datos
        rareza = 0

        for layer, filename in {'background': background, 'bodies': bodies, 'eyes': eyes, 'hats': hats}.items():
            query = "SELECT COUNT(*) FROM imagenes WHERE {} = ?".format(layer)
            cursor.execute(query, (filename,))
            count = cursor.fetchone()[0]

            # Asignar un valor de rareza en función de cuántas veces ha aparecido
            rareza += count

        # Consultar la rareza de todas las imágenes en la base de datos
        query = "SELECT filename, background, bodies, eyes, hats FROM imagenes"
        cursor.execute(query)
        all_results = cursor.fetchall()

        # Calcular la rareza de todas las imágenes y ordenarlas
        all_rarities = []
        for row in all_results:
            image_filename, image_background, image_bodies, image_eyes, image_hats = row
            rarity = 0

            for layer, filename in {'background': image_background, 'bodies': image_bodies, 'eyes': image_eyes, 'hats': image_hats}.items():
                query = "SELECT COUNT(*) FROM imagenes WHERE {} = ?".format(layer)
                cursor.execute(query, (filename,))
                count = cursor.fetchone()[0]
                rarity += count

            all_rarities.append((image_filename, rarity))

        all_rarities.sort(key=lambda x: x[1])  # Ordenar por rareza

        # Encontrar la posición de la imagen en el ranking
        image_rank = [index + 1 for index, (filename, rarity) in enumerate(all_rarities) if filename == filename_to_check][0]

        # Imprimir la rareza y posición en el ranking
        print(f"Rareza de la imagen {filename_to_check}: {rareza}")
        print(f"Posición en el ranking: {image_rank}")
    else:
        print(f"No se encontró el archivo RSC: {filename_to_check}")
else:
    print("Nombre de archivo RSC no válido. Debe seguir el formato 'RSC #[número].png'")

conn.close()
