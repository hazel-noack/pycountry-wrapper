from __future__ import annotations
from typing import Optional
from functools import wraps
import pycountry
import pycountry.db

from . import config


class EmptyCountryException(ValueError):
    pass


class Country:
    """
    This gets countries based on the ISO 3166-1 standart.

    Two examples are:
    - Country.from_alpha_2("DE")
    - Country.from_alpha_3("DEU")

    If the country couldn't be found, it raises a ValueError, or creates an empty object.
    Empty objects return for every attribute None
    """  

    def __init__(self, country: Optional[str] = None, pycountry_object: Optional[pycountry.db.Country] = None) -> None: 
        if pycountry_object is None:
            # search for the country string instead if the pycountry_object isn't given
            # this also implements the optional fallback
            pycountry_object = self._search_pycountry_object(country=country)

        if pycountry_object is None:
            raise EmptyCountryException(f"the country {country} was not found and config.fallback_country isn't set")

        self.pycountry_object: pycountry.db.Country = pycountry_object


    @classmethod
    def _search_pycountry_object(cls, country: Optional[str], is_fallback: bool = False) -> Optional[pycountry.db.Country]:
        # fallback to configured country if necessary 
        if country is None:
            if is_fallback:
                return None
            
            return cls._search_pycountry_object(country=config.fallback_country, is_fallback=True)
            
        pycountry_object = None

        # the reason I don't immediately return the result is because then there would be a chance 
        # I would return None even though a country could be found through fuzzy search
        country = country.strip()
        if len(country) == 2:
            pycountry_object = pycountry.countries.get(alpha_2=country.upper())
        elif len(country) == 3:
            pycountry_object = pycountry.countries.get(alpha_3=country.upper())
        if pycountry_object is not None:
            return cls(pycountry_object=pycountry_object)
        
        # fuzzy search if enabled
        if config.allow_fuzzy_search:
            found_countries = pycountry.countries.search_fuzzy(country)
            if len(found_countries):
                return cls(pycountry_object=found_countries[0]) 

    @classmethod
    def search(cls, country: Optional[str]) -> Optional[Country]:
        return cls(pycountry_object=cls._search_pycountry_object(country=country))

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


class StrictCountry(Country):
    """
    This works just like Country,
    but the object cant be empty
    """

    def __init__(self, country: Optional[str] = None, pycountry_object = None) -> None: 
        super().__init__(country=country, pycountry_object=pycountry_object, allow_empty=False)

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
