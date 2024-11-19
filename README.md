# Pycountry-Wrapper

This is a wrapper for pycountry, to make said library more usable.

## Installation

You can install the library by using pip:

```bash
pip install pycountry-wrapper
```

## Usage

```python
from pycountry_wrapper import Country, CountryDoesNotExist

germany = Country.from_alpha_2("DE")
print(germany)
print(germany.name)

try:
    does_not_exist = Country.from_alpha_2("EN")
except CountryDoesNotExist:
    # if the country wasn't found, this exception is thrown
    pass
```

### Creating country class

You can call create an instance of `pycountry_wrapper.Country` in multiple slightly different ways.

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

If you want to use fuzzy search, you will have to use `Country.from_fuzzy()`.

```python
from pycountry_wrapper import Country

Country.from_fuzzy("Deutschland")
```


### Accessing information

There are only a handful (readonly) attributes.

```python
from pycountry_wrapper import Country

country = Country.from_alpha_2("DE")

country.name
country.alpha_2
country.alpha_3
country.official_name
```
