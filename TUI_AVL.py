from AvlTree import AvlTree
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
        if len(self.ll_by_matr.search(matr)) >= 1:
            return print("Matrikelnummer bereits vorhanden, einfügen abgebrochen!")
        self._add(StudiObject(name, matr))

    def _add(self, studi):
        self.unsorted_array.append(studi)
        self.ll_by_name.insert(studi)
        self.ll_by_matr.insert(studi)

    def _modify_name(self):
        print("Wähle Nummer:")
        self._print(self.ll_by_name)
        studi_node = list(self.ll_by_name)[self._input(">>> ", int)-1]
        new_name = self._input("Ändere {}: neuer Name: \n>>> ".format(studi_node))
        #self.__del_node(studi_node)  # delete from lists
        self.unsorted_array.remove(studi_node)
        self.ll_by_matr.delete_node(self.ll_by_matr.search(id(studi_node), lambda x: id(x))[0])
        self.ll_by_name.delete_node(self.ll_by_name.search(id(studi_node), lambda x: id(x))[0])

        studi_node.set_name(new_name)  # change student
        self._add(studi_node)  # reinsert student (to maintain sorted lists)-+*9


    def _modify_matr(self):
        print("Wähle Nummer:")
        self._print(self.ll_by_matr)
        studi_node = list(self.ll_by_matr)[self._input(">>> ", int)-1]
        new_age = self._input("Ändere {}: neue matr: \n>>> ".format(studi_node), int)
        self.unsorted_array.remove(studi_node)
        self.ll_by_matr.delete_node(self.ll_by_matr.search(id(studi_node), lambda x: id(x))[0])
        self.ll_by_name.delete_node(self.ll_by_name.search(id(studi_node), lambda x: id(x))[0])
        studi_node.set_matr(new_age)  # change student
        self._add(studi_node)  # reinsert student (to maintain sorted lists)

    def __del_node(self, node):
        self.unsorted_array.remove(node)
        self.ll_by_name.delete(node, key=lambda x: (x.name, x.matr))
        self.ll_by_matr.delete(node, key=lambda x: (x.name, x.matr))

    def _del_search(self, key, cast_to=no_cast):
        key_to_delete = self._input(">>> ", cast_to)
        delete_candidates = self.ll_by_matr.search(key_to_delete, key=key)
        if len(delete_candidates) == 0:
            return print("Konnte keinen passenden Studenten finden.")
        elif len(delete_candidates) == 1:
            self.unsorted_array = [studi for studi in self.unsorted_array if not key_to_delete == key(studi)]
            self.ll_by_matr.delete(key_to_delete, key=key)
            self.ll_by_name.delete(key_to_delete, key=key)
        else:  # multiple delete-candidates:
            print("Welchen: ")
            self._print(delete_candidates)
            inpt = self._input(">>> ", int)
            try:
                del_obj = delete_candidates[inpt-1].val
                self.unsorted_array.remove(del_obj)
                self.ll_by_matr.delete(id(del_obj), lambda x: id(x))
                self.ll_by_name.delete(id(del_obj), lambda x: id(x))
            except IndexError:
                return print("Falscher input, abbruch!")


    def __init__(self, filepath=None):
        if filepath is None:
            filepath = "studidaten.txt"

        self.filepath = filepath
        self.options = {
            "L":  ("Alle daten löschen",
                   self._del_all),
            "Z":  ("Gib das Array aus",
                   lambda: self._print(self.unsorted_array)),
            "ZN": ("Liste nach Namen anzeigen (In PreOrder-Reihenfolge des Baums! Anscheinend so gewollt.)",
                   lambda: self._print(self.ll_by_name.preorder_node())),
            "ZM": ("Liste nach Matrikelnummer anzeigen (In PreOrder-Reihenfolge des Baums! Anscheinend so gewollt.)",
                   lambda: self._print(self.ll_by_matr.preorder_node())),
            "SN": ("Studi mit bestimmtenm Namen suchen",
                   lambda: self._print(self._search(self.ll_by_name, _sort_name))),
            "SM": ("Studi mit bestimmter Matrikelnummer suchen",
                   lambda: self._print(self._search(self.ll_by_matr, _sort_matr, int))),
            "N":  ("Neuen Studi einfügen",
                   self._add_new_studi),
            "LN": ("Studi nach Namen löschen",
                   lambda: self._del_search(_sort_name)),
            "LM": ("Studi nache Matrikelnummer löschen",
                   lambda: self._del_search(_sort_matr, int)),
            "MN": ("Studinamen ändern",
                   self._modify_name),
            "MM": ("Matrikelnummer ändern",
                   self._modify_matr),
            "S":  ("Daten speichern", self._save),
            "E":  ("Programmende", exit)
        }
        self.unsorted_array = []
        self.ll_by_name = AvlTree(key=_sort_name)
        self.ll_by_matr = AvlTree(key=_sort_matr)

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
        self.ll_by_name = AvlTree(key=_sort_name)
        self.ll_by_matr = AvlTree(key=_sort_matr)


if __name__ == "__main__":
    tui = TUI()

    while True:
        tui.menu()
