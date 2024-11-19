from __future__ import annotations
import pycountry

class CountryDoesNotExist(Exception): pass


class Country:
    """
    This gets countries based on the ISO 3166-1 standart.

    Two examples are:
    - Country.from_alpha_2("DE")
    - Country.from_alpha_3("DEU")

    If the country couldn't be found, it raises the pycountry_wrapper.CountryDoesNotExist exception.
    """

    def __init__(self, country: str = None, pycountry_object = None):
        if country is not None:
            # auto detect if alpha_2 or alpha_3
            if len(country) == 2:
                pycountry_object = pycountry.countries.get(alpha_2=country.upper())
            elif len(country) == 3:
                pycountry_object = pycountry.countries.get(alpha_3=country.upper())

        if pycountry_object is None:
            raise CountryDoesNotExist()

        self.pycountry_object = pycountry_object

    @classmethod
    def from_alpha_2(cls, alpha_2: str) -> Country:
        return cls(pycountry_object=pycountry.countries.get(alpha_2=alpha_2.upper()))
    
    @classmethod
    def from_alpha_3(cls, alpha_3: str) -> Country:
        return cls(pycountry_object=pycountry.countries.get(alpha_3=alpha_3.upper()))   

    @classmethod
    def from_fuzzy(cls, fuzzy: str) -> Country:
        return cls(pycountry_object=pycountry.countries.search_fuzzy(fuzzy))

    @property
    def name(self) -> str:
        return self.pycountry_object.name
    
    @property
    def alpha_2(self) -> str:
        return self.pycountry_object.alpha_2

    @property
    def alpha_3(self) -> str:
        return self.pycountry_object.alpha_3

    @property
    def numeric(self) -> str:
        return self.pycountry_object.numeric

    @property
    def official_name(self) -> str:
        return self.pycountry_object.official_name

    def __str__(self) -> str:
        return self.pycountry_object.__str__()

    def __repr__(self) -> str:
        return self.pycountry_object.__repr__()
