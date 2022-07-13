"""
This module serves to cut down the invalid contents of the dict.cc
dictionary file by removing those words that start with punctuation.
It also removes redundant labels, leaving behind only the vocabulary itself.
"""
from io import TextIOWrapper
import re

# LETTER_PATTERN = re.compile(r"[A-zäöüÄÖÜß]")
LABEL_PATTERN = re.compile(r"\[.+\]|<.+>")
GENDER_PATTERN = re.compile(r"{.+}")
MULTIPLE_SPACES = re.compile(r" {2,}")

def generate_pruned_dictionary(dict_file: TextIOWrapper) -> set[str]:
    """Takes in the dictionary file object and reads each line, removing
    terms that do not fit the desired requirements. Returns a set, as duplicate
    words are not counted."""
    s = {
        process_line(line)
        for line in dict_file
        if line[0].isalpha()
    }
    s.remove("")
    return s

def process_line(line: str) -> str:
    """Receives a dictionary entry and removes all data besides the German term."""
    # Format of each entry: term \t translation \t part of speech \t label (optional, but there is always a preceding tab)
    term, _, pos, _ = line.split("\t")
    
    # Return if we see declined verb forms without meaningful adjectival uses
    if pos == "past-p":
        # Note that past-participles with additional adjective senses have the pos label "adj past-p",
        # so they aren't affected.
        return ""

    # Return in cases where whole sentences or phrases involving punctuation are met
    if "/" in term:
        return ""
    elif "..." in term:
        return ""
    elif "!" in term:
        return ""

    term = re.sub(LABEL_PATTERN, "", term)

    is_noun = pos == "noun"
    if is_noun:
        try:
            gender = re.search(GENDER_PATTERN, term).group(0)
        except AttributeError:
            # Gender is ill-defined, so word is likely not relevant
            return ""
        if gender == "{pl}":
            return ""
        term = re.sub(GENDER_PATTERN, "", term)

    term = re.sub(MULTIPLE_SPACES, " ", term)

    word_count = len(term.split(" "))
    if (word_count > 1 and not is_noun) or word_count > 2:
        return ""

    return term.strip()

def main() -> None:
    """
    Assumes that the dictionary file is named 'de_en.txt',
    located within the Python file's current working directory.
    """
    with open("de_en.txt", mode="r", encoding="utf-8") as dict_file:
        # with open("pruned.txt", mode="w", encoding="utf-8") as pruned_file:
        wordlist = generate_pruned_dictionary(dict_file)
        to_write = "\n".join(wordlist)
    with open("pruned.txt", mode="w", encoding="utf-8") as pruned_file:
        pruned_file.write(to_write)

if __name__ == "__main__":
    main()