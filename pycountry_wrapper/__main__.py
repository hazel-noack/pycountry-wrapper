from .__about__ import __name__, __version__
from . import Country, EmptyCountry


def cli():
    print(f"Running {__name__} version {__version__} from __main__.py")

    print(EmptyCountry(country="doesn't exist").name)