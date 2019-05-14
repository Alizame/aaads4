from LinkedList import LinkedList
from StudiObject import StudiObject


def get_user_input(prompt=""):
    return input(prompt)


def read_file():
    try:
        with open(filepath, "r") as file:
            for line in file:
                name, matr = line.strip("\n").split(",")
                unsorted_array.append(StudiObject(name, int(matr)))
    except Exception as e:
        print("Error while reading file")
        print(e)


# L
def delete_all_data():
    unsorted_array.clear()
    ll_by_name.clear()
    ll_by_matr.clear()


# SN
def search_by_name():
    try:
        inp = get_user_input("Please enter the name to be searched: ")
        ll_by_name.search(inp, lambda studi: studi.get_name())
    except AttributeError as _:
        print("No Student with that name was found")


# SM
def search_by_matr(matr):
    raise NotImplementedError


# N
def add_new_studiobject(name, matr):
    raise NotImplementedError


# LN
def delete_by_name(name):
    raise NotImplementedError


# LM
def delete_by_matr(matr):
    raise NotImplementedError


# MN
def change_name(new_name, former_name=None, matr=None):
    if former_name is None and matr is None:
        print("Too little information given, cancelling the name change")
        return None
    else:
        raise NotImplementedError


# MM
def change_matr(new_matr, old_matr=None, name=None):
    if old_matr is None and name is None:
        print("Too little information given, cancelling the change of matrikelnumber")
        return None
    else:
        raise NotImplementedError


# S
def save():
    with open(filepath, "w") as file:
        for obj in unsorted_array:
            name, matr = obj.get_name(), obj.get_matr()
            file.write(str(name) + ", " + str(matr) + "\n")


def invalid_input():
    print("Invalid input!")


def print_ll_by_matr():
    print("print_ll_by_matr:")
    for studi in ll_by_matr:
        print(studi)


def print_ll_by_name():
    print("print_ll_by_name:")
    for studi in ll_by_name:
        print(studi)


def tui():
    options = {
        "L":  delete_all_data,
        "Z": lambda: print("Studenten: \n- " + str(unsorted_array).strip("[").strip("]").replace(", ", "\n- ")),
        "ZN": print_ll_by_name,
        "ZM": print_ll_by_matr,
        "SN": search_by_name,
        "SM": search_by_matr,
        "N":  add_new_studiobject,
        "LN": delete_by_name,
        "LM": delete_by_matr,
        "MN": change_name,
        "MM": change_matr,
        "S": save,
        "E": exit
    }

    print("\n" + menu)

    inp = get_user_input("Please choose one of the options above: ").upper()
    options.get(inp, invalid_input)()


def fill_lists():
    for study_object in unsorted_array:
        ll_by_name.attach_sorted(study_object, key=lambda studi: studi.get_name())
        ll_by_matr.attach_sorted(study_object, key=lambda studi: studi.get_matr())


if __name__ == "__main__":

    filepath = "studidaten.txt"
    menu = "L = Alle Daten löschen\n" + \
           "Z = Gib den Array aus\n" + \
           "ZN = Liste nach Namen anzeigen \n" + \
           "ZM = Liste nach Matrikelnummer anzeigen \n" + \
           "SN = Studi mit bestimmtenm Namen suhen\n" + \
           "SM = Studi mit bestimmter Matrikelnummer suchen\n" + \
           "N = Neuen Studi einfügen\n" + \
           "LN = Studi nach Namen löschen\n" + \
           "LM = Studi nache Matrikelnummer löschen\n" + \
           "MN = Studinamen ändern\n" + \
           "MM = Matrikelnummer ändern\n" + \
           "S = Daten speichern\n" + \
           "E = Programmende\n"

    unsorted_array = []
    ll_by_name = LinkedList()
    ll_by_matr = LinkedList()

    read_file()
    fill_lists()

    while True:
        tui()
