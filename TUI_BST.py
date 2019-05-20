from BinarySearchTree import BinarySearchTree
from StudiObject import StudiObject

_sort_name = lambda studi: studi.get_name()
_sort_matr = lambda studi: studi.get_matr()
no_cast = lambda x: x
_invalid_input = lambda: print("ungültige Eingabe")

class TUI:

    def _input(self, text, cast_to=no_cast):
        try:
            inpt_str = input(text)
            if inpt_str == "":
                raise ValueError()
            inpt = cast_to(inpt_str)
        except ValueError:
            print("bad input, try again")
            return self._input(text, cast_to)
        return inpt

    def _search(self, lst, key, cast_to=no_cast):
        what = self._input(">>> ", cast_to)
        return lst.search(what, key=key)

    def _add_new_studi(self):
        name = self._input("name: ")
        matr = self._input("matr: ", int)
        self._add(StudiObject(name, matr))

    def _add(self, studi):
        self.unsorted_array.append(studi)
        self.ll_by_name.insert(studi)
        self.ll_by_matr.insert(studi)

    def __init__(self, filepath=None):
        if filepath is None:
            filepath = "studidaten.txt"

        self.filepath = filepath
        self.options = {
            "L":  ("Alle daten löschen",
                   self._del_all),
            "Z":  ("Gib das Array aus",
                   lambda: self._print(self.unsorted_array)),
            "ZN": ("Liste nach Namen anzeigen",
                   lambda: self._print(self.ll_by_name)),
            "ZM": ("Liste nach Matrikelnummer anzeigen",
                   lambda: self._print(self.ll_by_matr)),
            "SN": ("Studi mit bestimmtenm Namen suchen",
                   lambda: self._print(self._search(self.ll_by_name, _sort_name))),
            "SM": ("Studi mit bestimmter Matrikelnummer suchen",
                   lambda: self._print(self._search(self.ll_by_matr, _sort_matr, int))),
            "N":  ("Neuen Studi einfügen",
                   self._add_new_studi),
            "S":  ("Daten speichern", self._save),
            "E":  ("Programmende", exit)
        }
        self.unsorted_array = []
        self.ll_by_name = BinarySearchTree(key=_sort_name)
        self.ll_by_matr = BinarySearchTree(key=_sort_matr)

        self._load()

    def menu(self):
        print()  # space menu from former output
        for key, menu_item in self.options.items():
            print(" # {} - {}".format(key, menu_item[0]))
        inp = self._input("Wähle weise: \n>>> ").upper()
        sel = self.options.get(inp, ("ungültige Eingabe", _invalid_input))
        print("'{}' ausgewählt:".format(sel[0]))
        sel[1]()

    @staticmethod
    def _print(what):
        objlist = list(what)  # cast to list [needed if obj is an iterator/generator]
        if len(objlist) == 0:
            return print("nothing here")
        for number, obj in enumerate(objlist):
            print(" - #{}\t {}".format(number + 1, obj))

    def _save(self):
        try:
            with open(self.filepath, "w", encoding="UTF-8") as file:
                for obj in self.unsorted_array:
                    name, matr = obj.get_name(), obj.get_matr()
                    file.write(str(name) + ", " + str(matr) + "\n")
        except (IOError, ValueError) as e:
            print("Fehler beim schreiben der Datei, möglicherweise Schreibschutz." + str(e))

    def _load(self):
        try:
            with open(self.filepath, "r", encoding="UTF-8") as file:
                for line in file:
                    name, matr = line.strip("\n").split(",")
                    new_obj = StudiObject(name, int(matr))
                    self._add(new_obj)
        except (IOError, ValueError) as e:
            print("Fehler beim lesen der Datei." + str(e))

    def _del_all(self):
        self.unsorted_array = []
        self.ll_by_name = BinarySearchTree(key=_sort_name)
        self.ll_by_matr = BinarySearchTree(key=_sort_matr)


if __name__ == "__main__":
    tui = TUI()

    while True:
        tui.menu()
