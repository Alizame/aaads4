from LinkedList import LinkedList
from StudiObject import StudiObject


def empty():
    raise NotImplementedError("Ey du Wurst! Hier is nüx.")

delete_by_name = empty
delete_by_matr = empty
change_name = empty
change_matr = empty

_sort_name = lambda studi: studi.get_name()
_sort_matr = lambda studi: studi.get_matr()


class TUI:

    def _search_by(self, lst, key, cast_to=None):
        name = input(">>> ")
        if cast_to is None:
            res = lst.search(name, key=key)
        else:
            res = lst.search(cast_to(name), key=key)
        return res

    def _add_new_studi(self):
        name = input("name: ")
        matr = int(input("matr: "))
        self._add(StudiObject(name, matr))

    def _add(self, studi):
        self.unsorted_array.append(studi)
        self.ll_by_name.attach_sorted(studi, key=_sort_name)
        self.ll_by_matr.attach_sorted(studi, key=_sort_matr)

    def _del(self, node):  # deletes all occurences!!!!!!!!!!?
        self.unsorted_array.remove()


    def __init__(self, filepath=None):
        if filepath is None:
            filepath = "studidaten.txt"

        self.filepath = filepath
        self.options = {
            "L":  ("Alle daten löschen",
                   self._del_all),
            "Z":  ("Gib den Array aus",
                   lambda: self._print(self.unsorted_array)),
            "ZN": ("Liste nach Namen anzeigen",
                   lambda: self._print(self.ll_by_name)),
            "ZM": ("Liste nach Matrikelnummer anzeigen",
                   lambda: self._print(self.ll_by_matr)),
            "SN": ("Studi mit bestimmtenm Namen suchen",
                   lambda: self._print(self._search_by(self.ll_by_name, _sort_name))),
            "SM": ("Studi mit bestimmter Matrikelnummer suchen",
                   lambda: self._print(self._search_by(self.ll_by_matr, _sort_matr, int))),
            "N":  ("Neuen Studi einfügen",
                   self._add_new_studi),
            "LN": ("Studi nach Namen löschen",
                   delete_by_name),
            "LM": ("Studi nache Matrikelnummer löschen",
                   delete_by_matr),
            "MN": ("Studinamen ändern",
                   change_name),
            "MM": ("Matrikelnummer ändern",
                   change_matr),
            "S":  ("Daten speichern", self._save),
            "E":  ("Programmende", exit)
        }
        self.unsorted_array = []
        self.ll_by_name = LinkedList()
        self.ll_by_matr = LinkedList()

        self._load()

    def menu(self):
        print()  # space menu from former output
        for key, menu_item in self.options.items():
            print(" # {} - {}".format(key, menu_item[0]))
        inp = input("Please choose one of the options above: \n>>> ").upper()
        self.options.get(inp, ("invalid", self._invalid_input))[1]()

    def _invalid_input(self):
        print("invalid input")

    @staticmethod
    def _print(what):
        l = list(reversed(list(what)))
        if len(l) == 0:
            return print("nothing here")
        for studi in l:
            print(" - {}".format(studi))

    def _save(self):
        with open(self.filepath, "w", encoding="UTF-8") as file:
            for obj in self.unsorted_array:
                name, matr = obj.get_name(), obj.get_matr()
                file.write(str(name) + ", " + str(matr) + "\n")

    def _load(self):
        try:
            with open(self.filepath, "r", encoding="UTF-8") as file:
                for line in file:
                    name, matr = line.strip("\n").split(",")
                    new_studi = StudiObject(name, int(matr))
                    self._add(new_studi)
        except Exception as e:
            print("Error while reading file")
            print(e)

    def _del_all(self):
        self.unsorted_array = []
        self.ll_by_name = LinkedList()
        self.ll_by_matr = LinkedList()



if __name__ == "__main__":
    tui = TUI()

    while True:
        tui.menu()

