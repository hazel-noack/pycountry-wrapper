import unittest

from pycountry_wrapper import Country, EmptyCountry, config, EmptyCountryException




class TestCountry(unittest.TestCase):
    def test_alpha_2(self):
        config.fallback_country = None
        c = Country("DE")
        self.assertEqual(c.alpha_2, "DE")

    def test_alpha_3(self):
        config.fallback_country = None
        c = Country("DEU")
        self.assertEqual(c.alpha_2, "DE")

    def test_fuzzy(self):
        config.fallback_country = None
        c = Country("Germany")
        self.assertEqual(c.alpha_2, "DE")

    def test_not_found(self):
        config.fallback_country = None
        with self.assertRaises(EmptyCountryException):
            Country("does not exist")


class TestEmptyCountry(unittest.TestCase):
    def test_found(self):
        config.fallback_country = None
        c = EmptyCountry("DE")
        self.assertEqual(type(c), Country)

    def test_data(self):
        config.fallback_country = None
        c = EmptyCountry("DE")
        self.assertEqual(c.alpha_2, "DE")

    def test_not_found(self):
        config.fallback_country = None
        c = EmptyCountry("does not exist")
        self.assertEqual(type(c), EmptyCountry)


if __name__ == '__main__':
    unittest.main()
