import logging
import telegram
import time
import random
from imdbpie import Imdb

LAST_UPDATE_ID = None
TOKEN = '116612566:AAGjN2chPXvtc-3inkiuAsRLfdDiyPTCy8c'

imdb = Imdb()
top250 = imdb.top_250()
current_movie = top250[random.randint(0, 249)]
current_images_count = len(imdb.get_title_images(current_movie.get('tconst')))
current_images = imdb.get_title_images(current_movie.get('tconst'))
image = current_images[random.randint(0, current_images_count)]


def main():
    global LAST_UPDATE_ID

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Telegram Bot Authorization Token
    bot = telegram.Bot(TOKEN)

    # This will be our global variable to keep the latest update_id when requesting
    # for updates. It starts with the latest update_id if available.
    try:
        LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
    except IndexError:
        LAST_UPDATE_ID = None

    while True:
        echo(bot)
        time.sleep(3)


def echo(bot):
    global LAST_UPDATE_ID

    # Request updates from last updated_id
    for update in bot.getUpdates(offset=LAST_UPDATE_ID):
        if LAST_UPDATE_ID < update.update_id:
            # chat_id is required to reply any message
            chat_id = update.message.chat_id
            message = update.message.text

            if '/next' in message:
                next_image()
                print(image)

                # Reply the message
                bot.sendPhoto(chat_id=chat_id, photo=image.url)

                # Updates global offset to get the new updates
                LAST_UPDATE_ID = update.update_id


def next_image():
    global current_movie
    current_movie = top250[random.randint(0, 249)]

    global current_images_count
    current_images_count = len(imdb.get_title_images(current_movie.get('tconst')))

    global current_images
    current_images = imdb.get_title_images(current_movie.get('tconst'))

    global image
    image = current_images[random.randint(0, current_images_count)]

    # if image.width < image.height:
    #     next_image()

if __name__ == '__main__':
    main()
