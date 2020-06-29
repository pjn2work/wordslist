import re
from args_parser import argsParser_from_sys_args


DEFAULT_WL = "wl_pt_preao.txt"


def convert_to_utf8(filename):
    with open(filename, mode="rb") as source:
        with open(filename+".utf8.txt", mode="wb") as target:
            for line in source:
                target.write(line.decode("latin-1").encode("utf-8"))


def find_word(regex_pattern_str, filename=DEFAULT_WL, max_matches=0):
    pattern = re.compile(regex_pattern_str)
    matches = list()
    with open(filename, mode="rb") as words_file:
        for text in words_file:
            matches += pattern.findall(text.decode("latin-1"))
            if max_matches and len(matches) == max_matches:
                break
    return matches


if __name__ == "__main__":
    # get parameters
    ap = argsParser_from_sys_args()
    wordlist_filename = ap.get_value("-w", [DEFAULT_WL])[-1]
    regex_pattern_str = ap.get_value("-p", ["^A[blmnps].*í.*$"])[-1]
    max_matches = int(ap.get_value("-m", [0])[-1])

    # find matches
    a = find_word(regex_pattern_str, filename=wordlist_filename, max_matches=max_matches)

    # show matches
    print(f"found {len(a)} words:")
    for x in a:
        print(x)
