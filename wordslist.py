import re
from args_parser import args_parser_from_sys_args
from tkinter import Tk, Label, Entry, Listbox, Button, END


DEFAULT_WL = "wl_pt_preao.txt"
DEFAULT_MAX_MATCHES = 50
DEFAULT_REGEX_PATTERN = "^A[blmnps].*í.*$"


def convert_unicode(filename, uc_from="latin-1", uc_to="utf-8"):
    with open(filename, mode="rb") as source:
        with open(f"{uc_to}_{filename}", mode="wb") as target:
            for line in source:
                target.write(line.decode(uc_from).encode(uc_to))


def find_words(regex_pattern_str, filename=DEFAULT_WL, max_matches=0):
    pattern = re.compile(regex_pattern_str)
    matches = list()
    with open(filename, mode="rb") as words_file:
        for text in words_file:
            matches += pattern.findall(text.decode("latin-1"))
            if max_matches and len(matches) == max_matches:
                break
    return matches


def shell_mode(ap):
    # get parameters
    wordlist_filename = ap.get_value("-w", [DEFAULT_WL])[-1]
    regex_pattern_str = ap.get_value("-p", [DEFAULT_REGEX_PATTERN])[-1]
    max_matches = int(ap.get_value("-m", [DEFAULT_MAX_MATCHES])[-1])

    # find matches
    results = find_words(regex_pattern_str, filename=wordlist_filename, max_matches=max_matches)

    # show matches
    print(f"found {len(results)} words:")
    for word in results:
        print(word)


def gui_mode():
    def search():
        try:
            words = find_words(e_rp.get(), e_wlf.get(), int(e_mm.get()))

            message.config(text=f"found {len(words)} words")
            results.delete(0, END)
            for x in words:
                results.insert(END, f"{x}")
        except Exception as e:
            message.config(text=str(e))

    root = Tk()

    Label(root, text="Word list filename:").grid(row=0, column=0, padx=2, sticky="w")
    Label(root, text="Max matches (0 for infinite):").grid(row=1, column=0, padx=2, sticky="w")
    Label(root, text="Regex pattern:").grid(row=2, column=0, padx=2, sticky="w")

    e_wlf = Entry(root)
    e_mm = Entry(root)
    e_rp = Entry(root)

    button = Button(root, text="search", command=search)
    message = Label(root, text=" ", bg="yellow")
    results = Listbox(root)

    e_wlf.grid(row=0, column=1, padx=2, pady=5, sticky="we")
    e_mm.grid(row=1, column=1, padx=2, pady=5, sticky="we")
    e_rp.grid(row=2, column=1, padx=2, pady=5, sticky="we")

    button.grid(row=3, column=0, columnspan=2, padx=4, pady=2, sticky="we")
    message.grid(row=4, column=0, columnspan=2, padx=4, pady=2, sticky="we")
    results.grid(row=5, column=0, columnspan=2, padx=2, pady=2, sticky="nsew")

    e_wlf.insert(0, DEFAULT_WL)
    e_mm.insert(0, DEFAULT_MAX_MATCHES)
    e_rp.insert(0, DEFAULT_REGEX_PATTERN)

    root.grid_rowconfigure(5, weight=1)
    root.mainloop()


if __name__ == "__main__":
    ap = args_parser_from_sys_args()
    if len(ap.get_keys()):
        shell_mode(ap)
    else:
        gui_mode()
