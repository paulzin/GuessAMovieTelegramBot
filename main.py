import telegram
import time
import sched
import movies_manager
import config


LAST_UPDATE_ID = None
bot = telegram.Bot(config.TOKEN)

s = sched.scheduler(time.time, time.sleep)


def main():
    global LAST_UPDATE_ID

    try:
        LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
    except IndexError:
        LAST_UPDATE_ID = None

    s.enter(1, 1, get_update)
    s.run()


def create_caption(movie_title):
    result_caption = ''
    title_words = movie_title.split(' ')

    for word in title_words:
        result_caption += str(telegram.Emoji.WHITE_MEDIUM_SQUARE) * len(word)
        result_caption += '  '

    return result_caption.strip()


def get_update():
    global LAST_UPDATE_ID

    for update in bot.getUpdates(offset=LAST_UPDATE_ID):
        if LAST_UPDATE_ID < update.update_id:
            chat_id = update.message.chat_id
            message = update.message.text

            if '/next' in message:
                movie = movies_manager.get_next_movie()
                movie_title = movie[0]
                movie_photo = movie[1]
                bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
                bot.sendPhoto(chat_id=chat_id, photo=movie_photo.url, caption=movie_title)
                LAST_UPDATE_ID = update.update_id
            else:
                print("")

    s.enter(1, 1, get_update)

if __name__ == '__main__':
    main()
