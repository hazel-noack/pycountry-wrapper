from __future__ import annotations
from typing import Optional
from functools import wraps
import pycountry


def none_if_empty(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.is_empty:
            return None

        return func(self, *args, **kwargs)
    
    return wrapper


class Country:
    """
    This gets countries based on the ISO 3166-1 standart.

    Two examples are:
    - Country.from_alpha_2("DE")
    - Country.from_alpha_3("DEU")

    If the country couldn't be found, it raises a ValueError, or creates an empty object.
    Empty objects return for every attribute None
    """  

    def __init__(self, country: Optional[str] = None, pycountry_object = None, allow_empty: bool = True) -> None: 
        if country is not None:
            # auto detect if alpha_2 or alpha_3
            if len(country) == 2:
                pycountry_object = pycountry.countries.get(alpha_2=country.upper())
            elif len(country) == 3:
                pycountry_object = pycountry.countries.get(alpha_3=country.upper())
        
        if pycountry_object is None and not allow_empty:
            raise ValueError(f"Country {country} couldn't be found")

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
    def is_empty(self) -> bool:
        return self.pycountry_object is None

    @property
    @none_if_empty
    def name(self) -> Optional[str]:
        return self.pycountry_object.name
    
    @property
    @none_if_empty
    def alpha_2(self) -> Optional[str]:
        return self.pycountry_object.alpha_2

    @property
    @none_if_empty
    def alpha_3(self) -> Optional[str]:
        return self.pycountry_object.alpha_3

    @property
    @none_if_empty
    def numeric(self) -> Optional[str]:
        return self.pycountry_object.numeric

    @property
    @none_if_empty
    def official_name(self) -> Optional[str]:
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
