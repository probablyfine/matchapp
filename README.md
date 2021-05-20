# matchapp
a fuzzy matching tool for joining tables on one or more inexact keys

## What/Why
This a GUI that makes it convenient to perform fast fuzzy matching between two data tables. It implements a LEFT JOIN operation on one or more inexact keys. This is useful for integrating external data into an existing database when the new data lack unique IDs.

This project is a work in progress. It still needs some polish but it is pretty functional.

## How
Matching computations are performed by the excellent [string_grouper](https://github.com/Bergvca/string_grouper) library. The author has a nice [blog post](https://bergvca.github.io/2017/10/14/super-fast-string-matching.html) explaining how it works. It is *much* faster than computing the Levenshtein distance between strings.

The GUI is written using [kivy](https://kivy.org).

## More details
The matching process occurs in two steps. First, the user selects a primary key from each table to use for matching. The primary keys are used to sift through the universe of possible matches and return the top *n* matches for each record (*n* is configurable but defaults to 10). 
<details>
<summary>Show screenshot</summary>
<br>
<img width="50%" src="https://github.com/probablyfine/matchapp/raw/main/screenshots/2%20narrowby.png">
</details>

Then, the user can optionally select one or more secondary keys from each table to refine the match result.
<details>
<summary>Show screenshot</summary>
<br>
<img width="50%" src="https://github.com/probablyfine/matchapp/raw/main/screenshots/3%20alsocompare.png">
</details>

For example, if the primary key is 'Name', an individual record 'Jim Smith', might have multiple plausible matches: 'Jim Smith' and 'Jimmy Smith'. You could then add a seconday key, say 'Department', to help decide which is the correct match.

As an alternative, you could instead create a new key based on the concatenation of 'Name' and 'Department', and then match solely on that key. A column merging feature is provided in the matchapp GUI. However, this isn't necessarily the best strategy; in the 'Name+Department' example, long Department strings would have greater importance than short Name strings. In that case, the two-step process might behave more predictably.

Once the keys have been selected, the user can optionally append additional columns from each table.
<details>
<summary>Show screenshot</summary>
<br>
<img width="50%" src="https://github.com/probablyfine/matchapp/raw/main/screenshots/4%20append.png">
</details>

Finally, the user can configure how they'd like to export the match results. You can export just the best possible match for each row, or you can export a few alternatives to review.
<details>
<summary>Show screenshot</summary>
<br>
<img width="50%" src="https://github.com/probablyfine/matchapp/raw/main/screenshots/5%20export.png">
</details>

There are also a bunch of configuration options you can play with before you start matching. Most of these just configure built-in options from string_grouper, but there are a few other convenient behaviors in there as well, including:
- ASCII transliteration for stripping accents/diacritics (handled by [unidecode](https://pypi.org/project/Unidecode/))
- Ampersand replacement so that '&' == 'and'
- Short string padding so scores can be computed for strings shorter than the n-gram size

<details>
<summary>Show screenshot</summary>
<br>
<img width="50%" src="https://github.com/probablyfine/matchapp/raw/main/screenshots/0%20config.png">
</details>

## Requirements
This project has some dependencies:
- Python3 (I'm using 3.7)
- kivy (>= 2.0.0)
- pandas (and xlrd or openpyxl for Excel support)
- string_grouper
- unidecode

## Pre-built executable
If you don't want to set up a development environment, you can [download a pre-built (Windows) executable](https://www.dropbox.com/s/2thpc3lgidl7l6z/matchapp.zip?dl=1). It was generated using PyInstaller per the [kivy docs](https://kivy.org/doc/stable/guide/packaging-windows.html).

## License
TBD
