# German Creation List
This script set is intended to generate a list of words that appear on the dict.cc German dictionary, but not on Wiktionary.
Its purpose is to allow myself and other Wiktionary users to know what terms to create on Wiktionary;
my belief is that this accords with the terms of dict.cc, as I do not use the dictionary's translations, but
merely list its individual headwords; the process of creating Wiktionary entries from this is still
at editors' discretion, and copying from the dict.cc database is not condoned through this project.

## Running
You will need to download the dict.cc database as a text file if you want to run the program directly; just visit
that site and navigate to the download section.
The dependency which is used to query Wiktionary is Pywikibot; please check out the Metawiki tutorial on using
it for installation and setup advice.

In order to actually run the script:
- Rename your dictionary file to `en_de.txt`.
- Run `python prune.py` with the dictionary file in the same directory.
- Now run `python wiktionary.py`. This part will take a long while.