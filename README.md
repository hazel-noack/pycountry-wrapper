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

You can call create an instance of `pycountry_wrapper.Country` in three ways.

Using **ISO 3166-1** with either 2 or 3 letters:

```python
from pycountry_wrapper import Country

Country.from_alpha_2("DE")
Country.from_alpha_2("DEU")
```

Or you can do a fuzzy search in a similar way:

```python
from pycountry_wrapper import Country

Country.from_fuzzy("Deutschland")
```

Or you can pass a pycountry object in the constructor:

```python
import pycountry
from pycountry_wrapper import Country

Country(pycountry.countries.get(alpha_2="DE"))
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
