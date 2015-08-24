import random
from time import gmtime, strftime
from imdbpie import Imdb

movies_in_top = 250
max_image_dimension = 2500
imdb = Imdb()
top250 = imdb.top_250()
movies_dict = {}


def generate_dict():

    print("Start:", strftime("%a, %d %b %Y %H:%M:%S", gmtime()))

    for movie in top250:
        images_list = get_canonical_images(imdb.get_title_images(movie.get('tconst')))
        if len(images_list) > 0:
            movies_dict[movie.get("title")] = images_list

    print("Movies with images:", str(len(movies_dict)))
    print("End:", strftime("%a, %d %b %Y %H:%M:%S", gmtime()))


def get_next_movie():
    movie_object = random.choice(list(movies_dict.items()))
    print(movie_object[0], random.choice(movie_object[1]))
    return movie_object[0], random.choice(movie_object[1])


def image_is_not_too_big(image):
    return image.height < max_image_dimension and image.width < max_image_dimension


def get_canonical_images(images_list):
    return [image for image in images_list
            if image.caption.lower().startswith("still of") and image_is_not_too_big(image)]


generate_dict()
