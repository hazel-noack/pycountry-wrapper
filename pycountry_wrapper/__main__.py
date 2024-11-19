from .__about__ import __name__, __version__
from . import Country


def cli():
    print(f"Running {__name__} version {__version__} from __main__.py")

    print(Country.from_alpha_2("DE"))
