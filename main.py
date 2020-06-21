import tkinter as tk
from typing import Optional
from tkinter import messagebox


# klasa- pojedyncza lista zakupów
class ShoppingList:
    def __init__(self, name):
        self.name_ = name  # nazwa tej konkretnej listy
        self.list_ = []  # zawartość tej listy (str)
        self.entryFields_ = []  # lista z polami Entry Field wyświetlanymi po prawej stronie
        self.newButton = None  # zmienna w której zapisany jest przycisk dodającegy nowe pole do tej listy
        self.newEntry = None  # zmienna w której zapisane jest pole tekstowe Entry Field do którego należy podać nazwę nowego pola
        self.maxNameLen = 25  # zmienna dodana, aby w łatwy sposób umożliwić późniejsze zmienianie limitu długości nazw

        # sprawdzenie, czy nazwa nie jest za długa
        if len(name) > self.maxNameLen:
            raise ListNameLengthError(self)

        # sprawdzenie, czy nazwa listy jest zajęta
        for i in listsList:
            if name in i.name_:
                raise ListNameAlreadyTakenError(self)

    # metoda wypisująca zawartość zmiennej list_
    def printList(self):
        global currentlyOpenedList  # aby była używana globalna wersja zmiennej
        if currentlyOpenedList is not None: currentlyOpenedList.closeList()  # zamyka obecnie otwartą listę zanim otworzy nową
        if currentlyOpenedList is None:  # może coś wyświetlić tylko jeżeli nic nie jest wyświetlone
            currentlyOpenedList = self  # przypisuje siebie jako otawrta liste
            while "" in self.list_: self.list_.remove("")  # czyszczenie listy z pustych elementów
            # pętla wypisująca wszystkie wartości z list_ do poszczególnych pól entry
            for j in self.list_:
                w = tk.Entry(  # tworzy pola typu entry w których są nazwy produktów
                    f2,
                    width=25
                )
                w.insert(0, j)
                w.pack(side=tk.TOP)
                self.entryFields_.append(w)  # dodaje te pola do listy aby potem dało się je usunac
            ##############

            # pole tekstowe odpowiedzialne za zebranie nazwy nowego porduktu
            self.newEntry = tk.Entry(
                f2,
                width=25
            )
            self.newEntry.insert(0, "Podaj nazwę nowego produktu")
            self.newEntry.pack(side=tk.BOTTOM)
            ############

            # przycisk odpowiedzialny za dodawnia nowego produktu
            self.newButton = tk.Button(
                f2,
                width=25,
                height=1,
                text="dodaj produkt",
                command=lambda: self.addProduct(self.newEntry.get())
            )
            self.newButton.pack(side=tk.BOTTOM)
            ##########

    # metoda dodająca nowy produkt do listy
    def addProduct(self, productName):
        
        # sprawdzenie czy ilość produktów nie przekracza maksymalnej
        if len(self.list_) > 20:
            raise ListElementsAmountError(self)
            
        self.list_.append(productName)
        if self == currentlyOpenedList:
            self.printList()

    # metoda zamykająca obecnie otwartą listę
    def closeList(self):
        global currentlyOpenedList
        isShowed = False
        self.saveList()
        for i in self.entryFields_:
            i.destroy()
        self.newButton.destroy()
        self.newEntry.destroy()
        self.entryFields_.clear()
        currentlyOpenedList = None

    # metoda zapisująca obecnie otwartą listę do listy list
    def saveList(self):
        global currentlyOpenedList
        for i in range(len(self.entryFields_)):
            self.list_[i] = (self.entryFields_[i]).get()


# zmienne gloablne używane WSZĘDZIE
listsList = []  # lista list - lista zawierająca listy zakupów

currentlyOpenedList: Optional[ShoppingList] = None  # obecnie otwarta lista

# testowa lista zakupów
listsList.append(ShoppingList("testowaLista"))
listsList[0].list_.append("zakup 1")
listsList[0].list_.append("zakup 2")
listsList[0].list_.append("zakup 3")
listsList[0].list_.append("zakup 4")

listsNum = len(listsList)  # obecna ilosc list


###########
# FUNCTIONS
# Funkcje operujące na liście wszystkich list zakupów (działające na lewej połówce ekranu, przypsiane do f1)

# funkcja tworząca przycisk służący do tworzenia nowych list i pole tekstowe typu entry gdzie trzeba podać nazwę nowej listy
def createNewListButton():
    global newListButton  # aby do obu pól można było się odwoływać gdzie indziej muyszą byc globalne
    global entry

    # pole do wpisania tytułu nowej listy
    entry = tk.Entry(
        f1,  # f1 przypisuje ten przycisk do ramki1
        width=25
    )
    entry.insert(0, "Podaj nazwę nowej listy")  # insert "wkłada" bazowy tekst do pola entry
    entry.pack()  # "pakuje" pole aby było odpowiednio wyświetlane w ramce

    # przycisk, po kliknięciu którego dodaje się lista o tytule wpisanym w entry
    newListButton = tk.Button(
        f1,
        text="utworz liste",
        width=25,
        height=3,
        command=newList
        # command to funkcja która ma być wywołana po kliknięciu przycisku. MUSI być bez (), inaczej funkcja wykona się przy interpretacji kodu, a nie przy klinkięciu.
    )
    newListButton.pack()


# funkcja tworząca przycisk służący do wyszukiwania list z listy i pole tekstowe typu entry gdzie trzeba podać nazwę wyszukiwanej listy
def createSearchBarButton():
    global searchButton
    global searchEntry

    searchEntry = tk.Entry(
        f1,
        width=25
    )
    searchEntry.insert(0, "podaj szukaną frazę")
    searchEntry.pack()

    searchButton = tk.Button(
        f1,
        text="wyszukaj",
        width=25,
        height=3,
        command=openSearchedList
    )
    searchButton.pack()


def openSearchedList():
    found = False
    for i in listsList:
        if i.name_ == searchEntry.get():
            found = True
            i.printList()
    if not found:
        searchEntry.delete(0, tk.END)
        searchEntry.insert(0, "brak takiej listy")


# tworzenie nowej listy, wraz z przyciskiem, dodaniem przycisku do tablicy przycisków itp
def newList():
    global listsNum
    
    # sprawdzenie czy ilosc list nie przekracza maksymalnej
    if listsNum >= 20:
        raise ListAmountError(listsNum)
        
    newListInstance = ShoppingList(
        entry.get())  # zbieram z pola entry (funkcja createNewListButton() odpowiada za tworzenie tego pola) nazwę nowej listy

    # przycisk do wyświetlania nowo utworzonej listy
    listButton = tk.Button(
        f1,
        text=newListInstance.name_,
        width=25,
        height=2,
        command=newListInstance.printList
    )
    listButton.pack()

    listsList.append(newListInstance)  # dodaje do tablicy z listami zakupów nową listę
    listsNum = len(listsList)  # zwiększa ilość zapisanych list


# funkcja używana w opcji menu górnego poziomego "Zapisz", służąca zapisowi do pliku
def saveToFile():
    pass


# funkcja używana w opcji menu górnego poziomego "Wczytaj", służąca wczytywaniu z pliku
def readFromFile():
    pass


#############

# EXCEPTIONS

class ListError(Exception):
    """Podstawowa klasa wyjątku rzucana przez listy"""

    def __init__(self, msg=None):
        if msg is None:
            msg = "Wystąpił problem z listą zakupów"
        super().__init__(msg)


class ListAmountError(ListError):
    """Zbyt wiele list"""

    def __init__(self, listsNum):
        super().__init__(
            msg=f"Ilość list: {listsNum} przekracza maksymalną")

        tk.messagebox.showerror(
            title="ListAmountError",
            message=f"Ilość list: {listsNum} przekracza maksymalną")


class ListElementsAmountError(ListError, ShoppingList):
    """Zbyt wiele pozycji na liście"""

    def __init__(self, currentList: ShoppingList):
        super().__init__(
            msg=f"Ilość produktów: {len(currentList.list_)} przekracza maskymalną")

        tk.messagebox.showerror(
            title="ListElementsAmountError",
            message=f"Ilość produktów: {len(currentList.list_)} przekracza maksymalną")


class ListNameLengthError(ListError, ShoppingList):
    """Nazwa listy zbyt długa"""

    def __init__(self, currentList: ShoppingList):
        super().__init__(
            msg=f"Ilość znaków w nazwie: {len(currentList.name_)} przekracza maksymalną: {currentList.maxNameLen}")

        tk.messagebox.showerror(
            title="ListNameLengthError",
            message=f"Ilość znaków w nazwie: {len(currentList.name_)} przekracza maksymalną: {currentList.maxNameLen}")


class ListNameAlreadyTakenError(ListError, ShoppingList):
    """Nazwa listy zajęta"""

    def __init__(self, currentList: ShoppingList):
        super().__init__(
            msg=f"Nazwa \"{currentList.name_}\" jest już zajęta")

        tk.messagebox.showerror(
            title="ListNameAlreadyTakenError",
            message=f"Nazwa \"{currentList.name_}\" jest już zajęta")


#############


# tworzy okno, chyba, wiem że musi być
root = tk.Tk()

# tworzę framey. w lewej (1) ramce zamieszczam kolejno przyciski z listami. W prawej po kliknięciu pojawia się konkretna lista
f1 = tk.Frame(
    width=25,
    height=100,
    bd=1
)
f1.pack(side=tk.LEFT)
f2 = tk.Frame(
    width=25,
    height=100,
    bd=5
)
f2.pack(side=tk.LEFT)

# tworzenie przycisku zamykającego otwartą listę
closeListButton = tk.Button(
    f2,  # przypisanie do prawego framea
    text="zamknij obecną listę",
    width=25,
    height=1,
    command=lambda: currentlyOpenedList.closeList() if currentlyOpenedList is not None else None
)
closeListButton.pack(side=tk.TOP, anchor=tk.N)

tk.Label(
    f1,
    text="Tworzenie nowej listy:"
).pack()
# funkcja tworząca przycisk tworzący nową listę i pole do wpisania jej nazwy - możnaby całą funckjonalność tej funkcji umieścić tutaj, nie musi być funkcji
createNewListButton()
tk.Label(
    f1,
    text="Wyszukiwarka:"
).pack()
createSearchBarButton()  # pole do wyszukiwania list - same as above
tk.Label(
    f1,
    text="lista list zakupów:"
).pack()

# pętla zbierająca istniejace listy z talicy listsList i tworząca przyciski do nich stworzona w celach testowych - trzeba będzie to przenieść do funkcji wczytującej z pliku
for i in listsList:
    listButton = tk.Button(
        f1,
        text=i.name_,
        width=25,
        height=2,
        command=i.printList
    )
    listButton.pack()

# Menu górne poziome
menu = tk.Menu(root)
root.config(menu=menu)
menu.add_command(label="Zapisz", command=saveToFile)
menu.add_command(label="Wczytaj", command=readFromFile)

root.mainloop()
