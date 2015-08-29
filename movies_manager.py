import random
import pickle
from time import gmtime, strftime
from imdbpie import Imdb

movies_in_top = 250
max_image_dimension = 2500
imdb = Imdb()
top250 = imdb.top_250()
movies_dict = {}
file_name = 'movie_data.pickle'


def init():
    global movies_dict

    loaded_dict = None

    try:
        try:
            with open(file_name, 'rb') as f:
                loaded_dict = pickle.load(f)
        except FileNotFoundError:
            open(file_name, 'wb+')
        if loaded_dict is not None:
            print("Loaded from cache")
            movies_dict = loaded_dict
            return
    except ValueError:
        print("Cannot read json")

    print("Start generating:", strftime("%a, %d %b %Y %H:%M:%S", gmtime()))

    total_images_count = 0
    movies_count = 0

    for movie in top250:
        images_list = get_canonical_images(imdb.get_title_images(movie.get('tconst')))
        total_images_count += len(images_list)
        movies_count += 1
        print(movies_count)
        if len(images_list) > 0:
            movies_dict[(movie.get("title"), movie.get("year"))] = images_list

    with open(file_name, 'wb') as f:
        pickle.dump(movies_dict, f, pickle.HIGHEST_PROTOCOL)

    print("Movies with images:", str(len(movies_dict)))
    print("Total images:", str(total_images_count))
    print("End generating:", strftime("%a, %d %b %Y %H:%M:%S", gmtime()))


def get_next_movie():
    movie_object = random.choice(list(movies_dict.items()))
    photo_object = random.choice(movie_object[1])
    movie_title = movie_object[0][0]
    movie_year = movie_object[0][1]
    movie_photo = photo_object.url
    print(movie_title + " (" + movie_year + ") " + movie_photo)
    return movie_object[0], random.choice(movie_object[1])


def image_is_not_too_big(image):
    return image.height < max_image_dimension and image.width < max_image_dimension


def get_canonical_images(images_list):
    return [image for image in images_list
            if image.caption.lower().startswith("still of") and image_is_not_too_big(image)]


def create_caption(title, year):
    result_caption = ''
    title_words = title.split(' ')

    for word in title_words:
        result_caption += "*" * len(word)
        result_caption += ' '

    return result_caption.strip() + " (" + year + ")"
