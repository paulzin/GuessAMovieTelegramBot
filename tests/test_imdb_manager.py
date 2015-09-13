from imdb_manager import ImdbManager
import unittest


class ImdbManagerTest(unittest.TestCase):
    def test_fetch_popular(self):
        imdb_manager = ImdbManager(max_pages_count=1)
        imdb_manager.fetch_popular_titles()

if __name__ == '__main__':
    unittest.main()
