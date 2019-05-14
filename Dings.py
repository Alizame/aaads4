from LinkedList import LinkedList
from StudiObject import StudiObject


def empty():
    raise NotImplementedError("Ey du Wurst! Hier is nüx.")


delete_all_data = empty
print_ll_by_name = empty
print_ll_by_matr = empty
search_by_name = empty
search_by_matr = empty
add_new_studiobject = empty
delete_by_name = empty
delete_by_matr = empty
change_name = empty
change_matr = empty


class TUI:
    def __init__(self):
        self.options = {
            "L":  ("Alle daten löschen", self._del_all),
            "Z":  ("Gib den Array aus", self._print_array),
            "ZN": ("Liste nach Namen anzeigen", self._print_by_name),
            "ZM": ("Liste nach Matrikelnummer anzeigen", self._print_by_matr),
            "SN": ("Studi mit bestimmtenm Namen suchen", search_by_name),
            "SM": ("Studi mit bestimmter Matrikelnummer suchen", search_by_matr),
            "N":  ("Neuen Studi einfügen", add_new_studiobject),
            "LN": ("Studi nach Namen löschen", delete_by_name),
            "LM": ("Studi nache Matrikelnummer löschen", delete_by_matr),
            "MN": ("Studinamen ändern", change_name),
            "MM": ("Matrikelnummer ändern", change_matr),
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
        inp = input("Please choose one of the options above: ").upper()
        self.options.get(inp, self._invalid_input)[1]()

    def _invalid_input(self):
        print("invalid input")

    def _print_by_matr(self):
        print("print_by_matr: ")
        for studi in reversed(list(self.ll_by_matr)):
            print(" - {}".format(studi.get_data()))

    def _print_by_name(self):
        print("print_by_name: ")

        for studi in reversed(list(self.ll_by_name)):
            print(" - {}".format(studi.get_data()))

    def _save(self, filepath=None):
        if filepath is None:
            filepath = "studidaten.txt"
        with open(filepath, "w", encoding="UTF-8") as file:
            for obj in self.unsorted_array:
                name, matr = obj.get_name(), obj.get_matr()
                file.write(str(name) + ", " + str(matr) + "\n")

    def _load(self, filepath=None):
        if filepath is None:
            filepath = "studidaten.txt"
        try:
            with open(filepath, "r", encoding="UTF-8") as file:
                for line in file:
                    name, matr = line.strip("\n").split(",")
                    new_studi = StudiObject(name, int(matr))
                    self.unsorted_array.append(new_studi)
                    self.ll_by_name.attach_sorted(new_studi, key=lambda studi: studi.get_name())
                    self.ll_by_matr.attach_sorted(new_studi, key=lambda studi: studi.get_matr())
        except Exception as e:
            print("Error while reading file")
            print(e)

    def _del_all(self):
        self.unsorted_array = []
        self.ll_by_name = LinkedList()
        self.ll_by_matr = LinkedList()

    def _print_array(self):
        print("Studenten:")
        for studi in self.unsorted_array:
            print(" - {}".format(studi))


if __name__ == "__main__":
    tui = TUI()

    while True:
        tui.menu()

