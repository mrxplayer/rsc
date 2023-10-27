import sqlite3
import re
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

# Variable para realizar un seguimiento de la etapa de la conversación
RANKING = 1

# Función para manejar el comando /ranking
def ranking(update: Update, context: CallbackContext):
    update.message.reply_text("Please enter your Radical Shroom Club NFT number to check your ranking:")
    return RANKING

# Función para manejar el número de RSC ingresado por el usuario
def handle_rsc_number(update: Update, context: CallbackContext):
    rsc_number = update.message.text

    # A continuación, coloca la lógica para calcular la rareza y la posición en el ranking según el número de RSC

    # Conectar a la base de datos
    conn = sqlite3.connect('imagenes.db')
    cursor = conn.cursor()

    # Formatear el nombre del archivo RSC
    filename_to_check = f"RSC #{rsc_number}.png"

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

        # Generar la respuesta
        respuesta = f"Congratulations. You've secured the #{image_rank} position in the ranking!"

        # Envía la respuesta al usuario
        update.message.reply_text(respuesta)
    else:
        update.message.reply_text(f"No se encontró el archivo RSC: {filename_to_check}")

    # Cerrar la conexión a la base de datos
    conn.close()
    return ConversationHandler.END  # Finaliza la conversación

# Configuración del bot
updater = Updater(token='6951359823:AAG2Z2IAsdydHpObZNwJJDclMUEHBshSFpo', use_context=True)
dispatcher = updater.dispatcher

# Agregar manejadores para el comando /ranking y para manejar el número de RSC
ranking_handler = ConversationHandler(
    entry_points=[CommandHandler('ranking', ranking)],
    states={
        RANKING: [MessageHandler(Filters.text & ~Filters.command, handle_rsc_number)]
    },
    fallbacks=[]
)

dispatcher.add_handler(ranking_handler)

# Iniciar el bot
updater.start_polling()

# Mantener el bot en ejecución
updater.idle()
