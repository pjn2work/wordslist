__author__ = "Pedro Nunes <pjn2work@gmail.com>"


import sys


class ArgsParser:
    """
    Flags       Starts with --, ex: --version
    Options     Starts with -, ex: -name Joe
    Arguments   value or values NOT starting with -, ex: *.txt d*s.xml
    """

    def __init__(self, argv_list):
        self.__argv_dict = dict()
        self.__args2dict(argv_list)
    
    # returns dict, keys are = flags options _arguments_, values are the options value or arguments
    def __args2dict(self, argv_list):
        total = len(argv_list)
    
        def insert(key, value):
            if key in self.__argv_dict:
                self.__argv_dict[key].append(value)
            else:
                self.__argv_dict[key] = [value]
    
        i = 0
        while i < total:
            args = argv_list[i]
    
            if args.startswith("--"):
                self.__argv_dict[args] = ""
            elif args.startswith("-"):
                i += 1
                insert(args, argv_list[i])
            else:
                insert("_arguments_", args)
    
            i += 1

    # returns dict
    def get_dict(self):
        return self.__argv_dict

    # returns dict_keys
    def get_keys(self):
        return self.__argv_dict.keys()

    # returns str or list from __argv_dict
    def get_value(self, key, default_value=None):
        return self.__argv_dict.get(key, default_value)

    # returns list of flags
    def get_flags(self) -> list[str]:
        return [key for key in self.__argv_dict if key.startswith("--")]

    # returns dict of options
    def get_options(self) -> dict[str, list[str]]:
        result = dict()
        for key, value in self.__argv_dict.items():
            if key.startswith("-") and not key.startswith("--"):
                result[key] = value
        return result

    # returns list of arguments
    def get_arguments(self, default_value=None) -> list[str]:
        return self.__argv_dict.get("_arguments_", default_value)

    def __str__(self):
        return str(self.__argv_dict)


# returns ArgsParser of sys.argv
def args_parser_from_sys_args():
    return ArgsParser(sys.argv[1:])


# returns ArgsParser from string args
def args_parser_from_str(args):
    return ArgsParser(args.split(" "))


# For testing this class
if __name__ == "__main__":
    ap = args_parser_from_str("-f sdf -f 11 --g -pe Pedro 1 2 3")
    print(ap.get_dict())
    print("keys", ap.get_keys())
    print("flags", ap.get_flags())
    print("options", ap.get_options())
    print("arguments", ap.get_arguments())
    print(ap)
