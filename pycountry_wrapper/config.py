import typing as _t

# defines the fallback country if a country can't be found
# alpha_2 or alpha_3 of ISO 3166-1
fallback_country: _t.Optional[str] = None

# should use fuzzy search if it cant find the country with alpha_2 or alpha_3
allow_fuzzy_search: bool = True
