# matchapp
a fuzzy matching tool for joining tables on one or more inexact keys

## What/Why
This a GUI that makes it convenient to perform fast fuzzy matching between two data tables. It implements a LEFT JOIN operation on one or more inexact keys. This is useful for integrating external data into an existing database when the new data lack unique IDs.

This project is a work in progress. It still needs some polish but it is pretty functional.

<img width="50%" src="https://github.com/probablyfine/matchapp/raw/main/screenshots/1%20load.png">

## How
Matching computations are performed by the excellent [string_grouper](https://github.com/Bergvca/string_grouper) library. The author has a nice [blog post](https://bergvca.github.io/2017/10/14/super-fast-string-matching.html) explaining how it works. It is *much* faster than computing the Levenshtein distance between strings.

The GUI is written using [kivy](https://kivy.org).

There are two ways to get this running:
1. Make sure your Python environment meets the [requirements](https://github.com/probablyfine/matchapp#requirements), clone this repository, change directory to where you cloned it, and type `python main.py` (or `python3 main.py` depending on your system)
2. If you're on Windows, download a [pre-built executable](https://github.com/probablyfine/matchapp#pre-built-executable). This is a fully-contained package that does not even require you to have Python installed.

## More details
The matching process occurs in two steps. First, the user selects a primary key from each table to use for matching. The primary keys are used to sift through the universe of possible matches and return the top *n* matches for each record (*n* is configurable but defaults to 10). 

<img width="50%" src="https://github.com/probablyfine/matchapp/raw/main/screenshots/2%20narrowby.png">

Then, the user can optionally select one or more secondary keys from each table to refine the match result:

<img width="50%" src="https://github.com/probablyfine/matchapp/raw/main/screenshots/3%20alsocompare.png">

For example, if the primary key is 'Name', an individual record 'Jim Smith' might have multiple plausible matches, e.g. 'Jim Smith' and 'Jimmy Smith'. You could then add a secondary key, say 'Department', to help decide which is the correct match.

As an alternative, you could instead create a new key based on the concatenation of 'Name' and 'Department', and then match solely on that new key. A column merging feature is provided in the matchapp GUI to make this approach more convenient. However, this isn't necessarily the best strategy; in the 'Name+Department' example, long Department strings would have greater importance than short Name strings. In that case, the two-step process might behave more predictably. Creating merged columns may still be useful in many cases, though, e.g. for matching on First+Last or Address+City+State+Zip.

Once the keys have been selected, the user can optionally append additional columns from each table:

<img width="50%" src="https://github.com/probablyfine/matchapp/raw/main/screenshots/4%20append.png">

Finally, the user can configure how they'd like to export the match results. You can export just the best possible match for each row, or you can export a few alternatives to review:

<img width="50%" src="https://github.com/probablyfine/matchapp/raw/main/screenshots/5%20export.png">

There are also a bunch of configuration options you can play with before you start matching. Most of these just configure built-in options from string_grouper, but there are a few other convenient behaviors in there as well, including:
- ASCII transliteration for stripping accents/diacritics (handled by [unidecode](https://pypi.org/project/Unidecode/))
- Ampersand replacement so that '&' == 'and'
- Short string padding so scores can be computed for strings shorter than the n-gram size

<img width="50%" src="https://github.com/probablyfine/matchapp/raw/main/screenshots/0%20config.png">

## What's missing
#### Explicit mode for finding duplicates
This software can be used to find duplicate records in a single table. However, I have not yet implemented an explicit way to perform this operation. For now, there are a couple of steps you can follow to make it work:
- Load the same spreadsheet for both the Left ('Populate to') and Right ('Populate from') tables.
- Select primary and secondary keys as you would normally.
- Append the unique ID column for *both* copies of the table.
- Export at least 2 alternate matches for each record.
- Find all rows where the unique ID is the same for both copies of the table, and delete those rows.

This works because the top match for every record is likely to be itself, so you need to manually remove the self-matches to isolate the potential duplicates.

#### Matching on more than 1 primary key
A current limitation of this software is that the universe of potential matches is determined using only a single column from each table (the 'primary' key). Secondary keys are only used to aid in ranking those potential matches. A more flexible approach would be to narrow the match universe on an arbitrary number of primary keys. I hope to add this feature eventually, but I need to find time to experiment a little.

## Requirements
This project has some dependencies:
- Python3 (I'm using 3.7.1)
- kivy (>= 2.0.0. I recommend using the latest dev version on Windows)
- pandas (and xlrd or openpyxl for Excel support)
- string_grouper
- unidecode

## Pre-built executable
If you don't want to set up a development environment, you can [download a pre-built (Windows) executable](https://www.dropbox.com/s/2thpc3lgidl7l6z/matchapp.zip?dl=1). It was generated using PyInstaller per the [kivy docs](https://kivy.org/doc/stable/guide/packaging-windows.html).

## License
TBD

## Contact
Questions/comments/issues/suggestions can be sent to ssuway@gmail.com.
