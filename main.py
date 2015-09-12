import telegram
import time
import sched
import movies_manager
import config
import strings_util


LAST_UPDATE_ID = None
bot = telegram.Bot(config.TOKEN)

s = sched.scheduler(time.time, time.sleep)
chats_dict = {}


def main():
    global LAST_UPDATE_ID

    try:
        LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
    except IndexError:
        LAST_UPDATE_ID = None

    movies_manager.init()
    s.enter(1, 1, get_update)
    s.run()


def get_update():
    global LAST_UPDATE_ID

    for update in bot.getUpdates(offset=LAST_UPDATE_ID):
        if LAST_UPDATE_ID < update.update_id:
            chat_id = update.message.chat_id
            message = update.message

            if strings_util.COMMAND_NEXT in message.text:
                # show next movie image
                movie = movies_manager.get_next_movie()
                bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
                movie_caption = strings_util.create_caption(movie)
                bot.sendPhoto(chat_id=chat_id, photo=movie[1].url, caption=movie_caption)
                chats_dict[chat_id] = (movie[0][0], None)
            elif strings_util.COMMAND_HINT in message.text:
                if not chats_dict.get(chat_id):
                    continue
                title = chats_dict.get(chat_id)[0]
                old_hint = chats_dict.get(chat_id)[1]
                new_hint = strings_util.get_hint(title, old_hint)
                chats_dict[chat_id] = (chats_dict.get(chat_id)[0], new_hint)

                if not new_hint:
                    continue

                if new_hint == title:
                    bot.sendMessage(chat_id=chat_id, text=new_hint)
                    chats_dict.pop(chat_id)
                    continue

                new_hint = strings_util.Emoji.FINGER_POINTS_RIGHT + " " + new_hint
                bot.sendMessage(chat_id=chat_id, text=new_hint)
            else:
                # check the answer
                actual_movie_title = chats_dict.get(chat_id)[0]

                if not actual_movie_title:
                    continue

                if str.lower(message.text) == str.lower(actual_movie_title):
                    bot.sendMessage(chat_id=chat_id, text=strings_util.get_correct_message())
                    chats_dict.pop(chat_id)
                else:
                    bot.sendMessage(chat_id=chat_id, text=strings_util.get_wrong_message())

            LAST_UPDATE_ID = update.update_id

    s.enter(1, 1, get_update)

if __name__ == '__main__':
    main()
