from . import __name__
from . import Country, EmptyCountry, config


def cli():
    print(f"Running {__name__} from __main__.py")
    import pycountry
    config.fallback_country = "US"
    t = pycountry.countries.get(alpha_2="DE")

    country = EmptyCountry(pycountry_object=t)
    print(type(country))
    print(country)

    print()
    empty_country = EmptyCountry(country="zwx")
    print(type(empty_country))
    print(empty_country)

    print()
    normal_country = Country("UK")
    print(type(normal_country))
    print(normal_country)

    print()
    fallback_country = Country("zwx")
    print(type(fallback_country))
    print(fallback_country)