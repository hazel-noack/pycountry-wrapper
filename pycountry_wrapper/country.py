from __future__ import annotations
from typing import Optional, Union
from functools import wraps
import pycountry
import pycountry.db

from . import config


class EmptyCountryException(ValueError):
    pass


class Country:
    """
    A class representing a country based on the ISO 3166-1 standard, wrapping the pycountry library.

    This class provides multiple ways to look up countries:
    - By 2-letter alpha-2 code (e.g., "DE" for Germany)
    - By 3-letter alpha-3 code (e.g., "DEU" for Germany)
    - By fuzzy search of country names
    - Directly from pycountry Country objects

    The class supports optional fallback behavior when a country isn't found,
    configurable through the module's config settings.

    Examples:
    >>> Country("Germany")  # Automatic detection
    >>> Country.search("Germany")
    >>> 
    >>> Country.from_alpha_2("DE")  # Germany by alpha-2 code
    >>> Country.from_alpha_3("DEU")  # Germany by alpha-3 code
    >>> Country.from_fuzzy("Germany")  # Germany by name search

    Raises:
        EmptyCountryException: If the country cannot be found and no fallback is configured.  
    
    If you don't want to raise an Exception if no country you can create a Country instance by the following methods:  
    - Country.search: returns None if nothing is found  
    - initialize EmptyCountry instead: gives you either a Country instance or an EmptyCountry instance
    """
    def __init__(
        self, 
        country: Optional[str] = None, 
        pycountry_object: Optional[pycountry.db.Country] = None, 
        disable_fallback: bool = False
    ) -> None: 
        if pycountry_object is None:
            # search for the country string instead if the pycountry_object isn't given
            # this also implements the optional fallback
            pycountry_object = self._search_pycountry_object(country=country, disable_fallback=disable_fallback)

        if pycountry_object is None:
            raise EmptyCountryException(f"the country {country} was not found and config.fallback_country isn't set")

        self.pycountry_object: pycountry.db.Country = pycountry_object


    @classmethod
    def _search_pycountry_object(cls, country: Optional[str], disable_fallback: bool = False) -> Optional[pycountry.db.Country]:
        pycountry_object = None

        if country is not None:
            # the reason I don't immediately return the result is because then there would be a chance 
            # I would return None even though a country could be found through fuzzy search
            country = country.strip()
            if len(country) == 2:
                pycountry_object = pycountry.countries.get(alpha_2=country.upper())
            elif len(country) == 3:
                pycountry_object = pycountry.countries.get(alpha_3=country.upper())
            if pycountry_object is not None:
                return pycountry_object
            
            # fuzzy search if enabled
            if config.allow_fuzzy_search:
                # fuzzy search raises lookup error if nothing was found
                try:
                    found_countries = pycountry.countries.search_fuzzy(country)
                    if len(found_countries):
                        return found_countries[0]
                except LookupError:
                    pass
        
        if pycountry_object is not None:
            return pycountry_object

        if config.fallback_country is not None and not disable_fallback:
            return cls._search_pycountry_object(country=config.fallback_country, disable_fallback=True)
            

    @classmethod
    def search(cls, country: Optional[str]) -> Optional[Country]:
        """
        Search for a country and return None instead of raising if not found.

        Args:
            country: String to search for (name, alpha-2, or alpha-3 code)

        Returns:
            Country object if found, None otherwise
        """
        return cls(pycountry_object=cls._search_pycountry_object(country=country))

    @classmethod
    def from_alpha_2(cls, alpha_2: str) -> Country:
        return cls(pycountry_object=pycountry.countries.get(alpha_2=alpha_2.upper()))
    
    @classmethod
    def from_alpha_3(cls, alpha_3: str) -> Country:
        return cls(pycountry_object=pycountry.countries.get(alpha_3=alpha_3.upper()))   

    @classmethod
    def from_fuzzy(cls, fuzzy: str) -> Country:
        return cls(pycountry_object=pycountry.countries.search_fuzzy(fuzzy)) # type: ignore

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


class EmptyCountry(Country):
    """
    A null-object pattern implementation of Country that returns None for all attributes.

    >>> empty = EmptyCountry("InvalidCountry")
    >>> print(empty.name)  # None
    >>> print(empty)  # EmptyCountry()

    It doubles as a factory, so if you instantiate the class you'll either get a Country object or EmptyCountry depending if it found a country.

    >>> empty = EmptyCountry("InvalidCountry")
    >>> print(type(empty))  # <class 'pycountry_wrapper.country.EmptyCountry'>
    >>> 
    >>> found = EmptyCountry("US")
    >>> print(type(found))  # <class 'pycountry_wrapper.country.Country'>
    """
    def __new__(cls, country: Optional[str] = None, pycountry_object: Optional[pycountry.db.Country] = None, **kwargs) -> Union[Country, EmptyCountry]:
        try:
            return Country(country=country, pycountry_object=pycountry_object, disable_fallback=True)
        except EmptyCountryException:
            return super().__new__(cls)
        
    def __init__(self, *args, **kwargs) -> None:
        pass

    name = None # type: ignore
    alpha_2 = None # type: ignore
    alpha_3 = None # type: ignore
    numeric = None # type: ignore

    def __str__(self) -> str:
        return "EmptyCountry()"

    def __repr__(self) -> str:
        return "EmptyCountry()"

