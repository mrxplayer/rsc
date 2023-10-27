import sqlite3
from PIL import Image
import random

# Crear una conexión a la base de datos SQLite (o crear un nuevo archivo si no existe)
conn = sqlite3.connect('imagenes.db')
cursor = conn.cursor()

# Crear una tabla para almacenar información sobre las imágenes
cursor.execute('''
    CREATE TABLE IF NOT EXISTS imagenes (
        id INTEGER PRIMARY KEY,
        background TEXT,
        eyes TEXT,
        bodies TEXT,
        hats TEXT,
        tamaño TEXT DEFAULT 'pequeño',
        filename TEXT
    )
''')
conn.commit()

# Definir listas de rutas y rarezas de las imágenes de fondo, ojos, cuerpos y gorros
backgrounds = ["B1.png", "B2.png", "B3.png", "B4.png", "B5.png", "B6.png", "B7.png"]
background_weights = [4, 4, 4, 4, 3, 2, 1]  # Ponderación de rareza
eyes = ["C1.png", "C2.png", "C3.png", "C4.png", "C5.png", "C6.png", "C7.png", "C8.png", "C9.png"]
eyes_weights = [1, 2, 2, 2, 2, 2, 2, 2, 2]  # Ponderación de rareza
bodies = ["O1.png", "O2.png", "O3.png", "O4.png", "O5.png", "O6.png", "O7.png", "O8.png"]
hats = ["G1.png", "G2.png", "G3.png", "G4.png", "G5.png", "G6.png", "G7.png", "G8.png", "G9.png", "G10.png", "G11.png", "G12.png", "G13.png", "G14.png", "G15.png", "G16.png", "G17.png", "G18.png", "G19.png", "G20.png", "G21.png", "G22.png", "G23.png", "G24.png", "G25.png", "G26.png", "G27.png", "G28.png", "G29.png", "G30.png", "G31.png", "G32.png", "G33.png", "G34.png", "G35.png","G36.png"]
hat_weights = [2, 4, 1, 2, 3, 4, 4, 1, 4, 3, 2, 4, 3, 2, 2, 4, 2, 3, 4, 4, 2, 2, 3, 2, 3, 4, 2, 1, 1, 4, 3, 3, 2, 2, 3, 2]  # Ponderación de rareza

# Número de imágenes a generar
num_images = 10
generated_combinations = set()  # Conjunto para rastrear combinaciones generadas

# Proceso de combinación y guardado
for i in range(num_images):
    while True:
        selected_background = Image.open(random.choices(backgrounds, background_weights)[0])
        selected_eye = Image.open(random.choices(eyes, eyes_weights)[0])
        selected_body = Image.open(random.choice(bodies))
        selected_hat = Image.open(random.choices(hats, hat_weights)[0])

        # Generar una cadena única que represente la combinación actual
        combination_str = f"{selected_background.filename}-{selected_eye.filename}-{selected_body.filename}-{selected_hat.filename}"

        # Verificar si la combinación ya se ha generado antes
        if combination_str not in generated_combinations:
            generated_combinations.add(combination_str)  # Agregar la combinación al conjunto

            # Guardar la información en la base de datos
            cursor.execute("INSERT INTO imagenes (background, eyes, bodies, hats, filename) VALUES (?, ?, ?, ?, ?)",
                           (selected_background.filename, selected_eye.filename, selected_body.filename, selected_hat.filename, f"RSC #{i}.png"))
            conn.commit()
            break  # Continuar con la siguiente imagen si la combinación es única

    # Superponer las imágenes
    selected_background.paste(selected_eye, (0, 0), selected_eye)
    selected_background.paste(selected_body, (0, 0), selected_body)
    selected_background.paste(selected_hat, (0, 0), selected_hat)

    # Guardar la imagen resultante
    selected_background.save(f"RSC #{i}.png")

print(f"Se han generado {num_images} imágenes únicas.")

# Cerrar la conexión a la base de datos al final del programa
conn.close()
