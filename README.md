# Word list generator

## About
WLGEN pretends to be something between crunch and CUPP. Permutations are based on a list of keywords and then you can add different options (connectors,abbreviations, reverse, replacements ...) to extend the final wordlist.

## Use
There are seceral options in `config.cfg`:

### Params
- `keywords` (list): Main list to permutate.
- `connectors` (list): For each permutation we will use this list to concatenate keywords.
- `num_tails` (list): For each permutation we will add (at the end of the string) a number (`10`) or a range of numbers (`20-40`)
- `tails` (list): We will add an extra string (i.e. `@hotmail.com`)

### Options
This options will **extend** our wordlist generated with `[Params]` section.
- `string_replacements` (bool): If true we will replace strings defined in `[Replacements]` section for each element of `keywords` param. i.e. `hello` -> `h3ll0`
- `abbreviation` (bool): If true we will use elements abbreviations of `keywords` param. i.e. `hello` -> `h`
- `reverse` (bool): If true we will reverse elements of `keywords`. i.e. `hello` -> `olleh`
- `min_length` and `max_length` (num): We filter result list by length element.

### Files
- `output`: Output file name.