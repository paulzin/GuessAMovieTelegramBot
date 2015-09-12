import random

COMMAND_NEXT = '/next'
COMMAND_HINT = '/hint'

correct_answer_msg_list = ["Correct!", "Nice job!", "Right!", "Yes! How did you know that?", "Very good!",
                           "Well done!", "Genius!", "Good job!", "Yes! I'm impressed...", "Yeah, not bad",
                           "That's correct!", "Perfect answer!", "Great answer!"]

wrong_answer_msg_list = ["Wrong", "Nope", "Not even close", "No", "Bad guess",
                         "Incorrect", "Try again", "Try harder", "That's not correct", "No, it's cold",
                         "Nope, that's not it", "Wrong answer"]


def get_correct_message():
    return Emoji.THUMB_UP + ' ' + random.choice(correct_answer_msg_list) + ' ' + random.choice(Emoji.positive)


def get_wrong_message():
    return Emoji.THUMB_DOWN + ' ' + random.choice(wrong_answer_msg_list) + ' ' + random.choice(Emoji.negative)


def convert_to_stars(text):
    return '*' * len(text)


def create_caption(movie):
    title = movie[0][0]
    year = movie[0][1]

    result_caption = ''
    title_words = title.split(' ')

    for word in title_words:
        result_caption += convert_to_stars(word)
        result_caption += ' '

    return result_caption.strip() + ' (' + year + ')'


def get_hint(title, old_hint):
    new_hint = ''
    title_words = title.split(' ')

    if len(title_words) > 1:
        if old_hint is None:
            hint_word = random.choice(title_words)
            for word in title_words:
                if word == hint_word:
                    new_hint += word
                else:
                    new_hint += convert_to_stars(word)
                new_hint += ' '
            return new_hint.strip()
        else:
            hidden_positions = [i for i, word in enumerate(old_hint.split(' ')) if '*' in word]
            if not hidden_positions:
                return old_hint
            hint_position = random.choice(hidden_positions)
            for i, word in enumerate(old_hint.split(' ')):
                if i == hint_position:
                    new_hint += title_words[hint_position]
                else:
                    new_hint += word
                new_hint += ' '
            return new_hint.strip()

    return None


class Emoji:
    THUMB_UP = '👍'
    THUMB_DOWN = '👎'
    FINGER_POINTS_RIGHT = '👉'
    SMILEY_FACE_1 = '😀'
    WINK_FACE = '😉'
    COOL_FACE = '😎'
    SAD_FACE_1 = '😟'
    SAD_FACE_2 = '😕'
    POKER_FACE_1 = '😐'
    POKER_FACE_2 = '😑'
    POKER_FACE_3 = '😶'

    positive = [SMILEY_FACE_1, WINK_FACE, COOL_FACE]
    negative = [SAD_FACE_1, SAD_FACE_2, POKER_FACE_1, POKER_FACE_2, POKER_FACE_3]
