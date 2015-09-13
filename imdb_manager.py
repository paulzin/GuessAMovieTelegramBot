from bs4 import BeautifulSoup
from title import Title
import urllib3


class ImdbManager:
    url = 'http://www.imdb.com/search/title?count=100&' \
          'title_type=feature,tv_series,tv_movie&explore=title_type,genres,year,countries&ref_=nv_ch_mm_1' \
          '&start='
    offset = 1
    start_page = 1
    max_pages_count = 20
    title_id_list = []

    _headers = {'Accept-Language': 'en-US,en;q=0.8'}
    _page_increment_step = 1
    _offset_increment_step = 100

    def __init__(self, max_pages_count=20):
        self.max_pages_count = max_pages_count

    @classmethod
    def update_url(cls):
        return cls.url + str(cls.offset)

    @classmethod
    def fetch_popular_titles(cls):
        while cls.start_page < cls.max_pages_count:
            print("\n\npage =", cls.start_page)
            print("offset =", cls.offset)
            url = cls.update_url()

            http = urllib3.PoolManager()
            r = http.request('GET', url, headers=cls._headers)

            soup = BeautifulSoup(r.data, 'html.parser')
            results_table = soup.find('table', {'class': 'results'})
            tr_list = results_table.find_all('tr')
            tr_list.pop(0)
            cls.offset += cls._offset_increment_step
            cls.start_page += cls._page_increment_step
            for tr in tr_list:
                title_id = tr.find('span').attrs['data-tconst']
                title_year = tr.find('span', {'class': 'year_type'}).text.replace('(', '').replace(')', '')
                title_name = tr.find_all('a')[1].text
                cls.title_id_list.append(Title(title_id=title_id, name=title_name, year=title_year))
