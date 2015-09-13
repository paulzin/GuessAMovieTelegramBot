import random
import pickle
from time import gmtime, strftime
from imdbpie import Imdb
from imdb_manager import ImdbManager
from title import Title

movies_in_top = 250
max_image_dimension = 2500

imdb = Imdb()
imdb_manager = ImdbManager()

titles = []

file_name = 'movie_data.pickle'


def init():
    global titles

    loaded_titles = None

    try:
        try:
            with open(file_name, 'rb') as f:
                loaded_titles = pickle.load(f)
        except FileNotFoundError:
            open(file_name, 'wb+')
        if loaded_titles is not None:
            print("Loaded from cache")
            titles = loaded_titles
            return
    except ValueError:
        print("Cannot read json")

    print("Start generating:", strftime("%a, %d %b %Y %H:%M:%S", gmtime()))
    print("Fetching popular started...:", strftime("%a, %d %b %Y %H:%M:%S", gmtime()))
    imdb_manager.fetch_popular_titles()
    print("Fetching popular ended...:", strftime("%a, %d %b %Y %H:%M:%S", gmtime()))
    popular_titles = imdb_manager.title_id_list

    total_images_count = 0
    movies_count = 0

    for title in popular_titles:
        images_list = get_canonical_images(imdb.get_title_images(title.title_id))
        total_images_count += len(images_list)
        movies_count += 1
        if len(images_list) > 0:
            titles.append(Title(title.name, title.year, images_list))

    with open(file_name, 'wb') as f:
        pickle.dump(titles, f, pickle.HIGHEST_PROTOCOL)

    print("Movies with images:", str(len(titles)))
    print("Total images:", str(total_images_count))
    print("End generating:", strftime("%a, %d %b %Y %H:%M:%S", gmtime()))


def get_next_movie():
    title_object = random.choice(list(titles))
    print(title_object.name, '(' + title_object.year + ')', '- images count: ' + str(len(title_object.images)))
    return title_object


def image_is_not_too_big(image):
    return image.height < max_image_dimension and image.width < max_image_dimension


def get_canonical_images(images_list):
    return [image for image in images_list
            if image.caption.lower().startswith("still of") and image_is_not_too_big(image)]



