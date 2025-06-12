import unittest

from pycountry_wrapper import Country, EmptyCountry, config, EmptyCountryException


class TestCountry(unittest.TestCase):
    def test_alpha_2(self):
        config.fallback_country = "US"
        c = Country("DE")
        self.assertEqual(c.alpha_2, "DE")

    def test_alpha_3(self):
        config.fallback_country = "US"
        c = Country("DEU")
        self.assertEqual(c.alpha_2, "DE")

    def test_fuzzy(self):
        config.fallback_country = "US"
        c = Country("Germany")
        self.assertEqual(c.alpha_2, "DE")

    def test_not_found(self):
        config.fallback_country = "US"
        c = Country("does not exist")
        self.assertEqual(c.alpha_2, "US")


class TestEmptyCountry(unittest.TestCase):
    def test_found(self):
        config.fallback_country = "US"
        c = EmptyCountry("DE")
        self.assertEqual(type(c), Country)
        self.assertEqual(c.alpha_2, "DE")

    def test_not_found(self):
        config.fallback_country = "US"
        c = EmptyCountry("does not exist")
        self.assertEqual(type(c), EmptyCountry)
        self.assertEqual(c.alpha_2, None)


if __name__ == '__main__':
    unittest.main()
