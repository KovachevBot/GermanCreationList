import pywikibot
import os

if not os.path.exists("checked.txt"):
    with open("checked.txt", mode="w", encoding="utf-8"):
        pass


def get_checked_words() -> dict[str, bool]:
    checked_dict = {}
    with open("checked.txt", mode="r", encoding="utf-8") as checked:
        for line in checked:
            line = line.strip()
            word, is_checked = line.split("\t")
            checked_dict[word] = is_checked
    return checked_dict


def get_absent_words(checked_dict: dict) -> set[str]:
    return {word for word, is_checked in checked_dict.items() if is_checked}


def dump_checked_words(checked_dict: dict) -> None:
    with open("checked.txt", mode="w", encoding="utf-8") as checked:
        for word, is_checked in checked_dict.items():
            checked.write(f"{word}\t{is_checked}\n")


def generate_missing_words_page(missing_words: set) -> str:
    return "\n".join(f"[[{word}]]" for word in missing_words)


def has_german(page: pywikibot.Page) -> bool:
    if not page.exists():
        return False
    
    return "==German==" in page.text


def main():
    site = pywikibot.Site("en", "wiktionary")

    checked_words = get_checked_words()
    absent_words = get_absent_words(checked_words)
    try:
        with open("pruned.txt", mode="r", encoding="utf-8") as pruned:
            for line in pruned:
                word = line.strip()
                if word in checked_words:
                    continue
                else:
                    # Word has not yet been checked, so we don't know whether it is on Wiktionary or not
                    page = pywikibot.Page(site, word)
                    if has_german(page):
                        checked_words[word] = True
                    else:
                        # The word is not on Wiktionary
                        checked_words[word] = False
                        absent_words.add(word)
    except KeyboardInterrupt:
        pass

    dump_checked_words(checked_words)
    with open("missing_words.txt", mode="w", encoding="utf-8") as missing_words:
        missing_words.write(generate_missing_words_page(absent_words))

if __name__ == "__main__":
    main()
