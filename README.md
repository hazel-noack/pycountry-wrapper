# Pycountry-Wrapper

This is a wrapper for pycountry, to make said library more usable.

## Installation

You can install the library by using pip:

```bash
pip install pycountry-wrapper
```

## Usage

```python
from pycountry_wrapper import Country

germany = Country.from_alpha_2("DE")
print(germany)
print(germany.name)

try:
    does_not_exist = Country.from_alpha_2("EN")
except ValueError:
    # if the country wasn't found, a ValueError is raised
    pass
```

### Creating country class

You can call create an instance of `Country` in multiple slightly different ways.

The [**ISO 3166-1**](https://en.wikipedia.org/wiki/ISO_3166-1) standart can either use 2 or 3 letters (alpha_2 or alpha_3).

```python
from pycountry_wrapper import Country

# auto detects if alpha_2 or alpha_3
Country("DE")
Country("DEU")

# you can specify what to use, if required.
Country.from_alpha_2("DE")
Country.from_alpha_3("DEU")
```

If the country can't be found it will raise a `EmptyCountryException` or use the fallback defined in `config.fallback_country`.

Alternatively you can get an instance of `Country` by using `Country.search`. This will return `None` if no country was found.

I also implemented a null-object pattern of `Country`, meaning you can get an `EmptyCountry` object. If you create a country from this object you'll get an instance of `Country` if it was found, and an instance of `EmptyCountry` if it wasn't.

```python
empty = EmptyCountry("InvalidCountry")
print(type(empty))  # <class 'pycountry_wrapper.country.EmptyCountry'>

found = EmptyCountry("US")
print(type(found))  # <class 'pycountry_wrapper.country.Country'>
```

### Accessing information

There are only a handful (readonly) attributes.

```python
from pycountry_wrapper import Country

country = Country("DE")

country.name
country.alpha_2
country.alpha_3
country.official_name
```

If you have an `EmptyCountry` these attributes will all be `None`.

### Configuring behavior

If you want to set a fallback country or disable fuzzy search you can do that with the config module.

```python
from pycountry_wrapper import config

config.fallback_country = "US"
config.allow_fuzzy_search = False
```
