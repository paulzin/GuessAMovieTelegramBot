import telegram
import time
import random
import logging
from imdbpie import Imdb

TOKEN = '116612566:AAGjN2chPXvtc-3inkiuAsRLfdDiyPTCy8c'

LAST_UPDATE_ID = None
MOVIES_IN_TOP = 250

imdb = Imdb()
top250 = imdb.top_250()
current_image = None
logger = None


def main():
    global LAST_UPDATE_ID

    bot = telegram.Bot(TOKEN)
    init_logger()
    generate_image()

    try:
        LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
    except IndexError:
        LAST_UPDATE_ID = None

    while True:
        echo(bot)
        time.sleep(1)


def echo(bot):
    global LAST_UPDATE_ID

    for update in bot.getUpdates(offset=LAST_UPDATE_ID):
        if LAST_UPDATE_ID < update.update_id:
            chat_id = update.message.chat_id
            message = update.message.text

            if '/next' in message:
                if current_image is None:
                    return

                bot.sendPhoto(chat_id=chat_id, photo=current_image.url)
                generate_image()
                LAST_UPDATE_ID = update.update_id


def generate_image():
    global current_image

    current_movie = top250[random.randint(0, MOVIES_IN_TOP - 1)]
    current_images_list = get_canonical_images(imdb.get_title_images(current_movie.get('tconst')))

    if len(current_images_list) == 0:
        generate_image()
        return

    current_image = current_images_list[random.randint(0, len(current_images_list) - 1)]
    logging.warning(current_image.caption + " " + current_image.url)


def get_canonical_images(images_list):
    return [image for image in images_list
            if image.caption.lower().startswith("still of")]


def init_logger():
    global logger
    logger = logging.getLogger('BOT')
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

if __name__ == '__main__':
    main()
