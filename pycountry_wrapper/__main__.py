from .__about__ import __name__, __version__
from . import Country, EmptyCountry

import pycountry


def cli():
    print(f"Running {__name__} version {__version__} from __main__.py")
    t = pycountry.countries.get(alpha_2="DE")

    country = EmptyCountry(pycountry_object=t)
    print(type(country))
    print(country)

    print()
    empty_country = EmptyCountry(country="zwx")
    print(type(empty_country))
    print(empty_country)