import dataclasses
import typing
from statistics import quantiles

import form


class Prodotto:
    aliquota_iva = 0.22  # variabile di classe -- ovvero è la stessa per tutte le istanza che verranno create

    def __init__(self, name: str, price: float, quantity: int, supplier=None):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.supplier = supplier

    def valore_netto(self):
        return self.price * self.quantity

    def valore_lordo(self):
        netto = self.valore_netto()
        lordo = netto * (1 + self.aliquota_iva)
        return lordo

    def prezzo_finale(self) -> float:
        return self.price * (1 + self.aliquota_iva)

    # decoratore
    @classmethod
    def costruttore_con_quantità_uno(cls, name: str, price: float, supplier: str):
        return cls(name, price, quantity=1, supplier=supplier)

    @classmethod
    def applica_sconto(cls, prezzo, percentuale):
        return prezzo * (1 - percentuale)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price must be positive")
        self._price = value

    def __str__(self):
        return f"{self.name} - disponibili {self.quantity} pezzi a {self.price} $ "

    def __repr__(self):
        return f"Prodotto(name = {self.name}, price = {self.price}, quantity = {self.quantity}, supplier = {self.supplier})"

    def __eq__(self, other: object):
        if not isinstance(other, Prodotto):
            return NotImplemented
        return {self.name == other.name
                and self.price == other.price
                and self.quantity == other.quantity
                and self.supplier == other.supplier}

    def __lt__(self, other: "Prodotto") -> bool:
        return self.price < other.price


# classe totalmente specificata con tutti glio attributi della classe prodotto
class ProdottoScontato(Prodotto):
    def __init__(self, name: str, price: float, quantity: int, supplier: str, sconto_percento: float):
        # Prodotto:__init__()
        super().__init__(name, price, quantity, supplier)
        self.sconto_percento = sconto_percento

    def prezzo_finale(self) -> float:
        return self.valore_lordo() * (1 - self.sconto_percento / 100)


class Servizio(Prodotto):
    def __init__(self, name: str, tariffa_oraria: float, ore: int):
        super().__init__(name=name, price=tariffa_oraria, quantity=1, supplier=None)
        self.ore = ore

    def prezzo_finale(self) -> float:
        return self.price * self.ore


myproduct1 = Prodotto("Laptop", 1200.0, 12, "ABC")

myproduct1 = Prodotto(name="Laptop", price=1200.0, quantity=12, supplier="ABC")
print(f"Nome prodotto: {myproduct1.name}")
print(f"Prezzo prodotto: {myproduct1.price}")

print(f"Nome prodotto: {myproduct1.name}- prezzo : {myproduct1.price}")

p3 = Prodotto.costruttore_con_quantità_uno(name="Auricolari ", price=200., supplier="ABC")
print(f"prezzo scontato di myproduct 1  {Prodotto.applica_sconto(myproduct1.price, percentuale=0.15)}")

myproduct2 = Prodotto(name="Mouse", price=10, quantity=25, supplier="CDE")
print(f"Nome prodotto: {myproduct2.name}- prezzo : {myproduct2.price}")

print(p3)

p_a = Prodotto(name="Laptop", price=1200.0, quantity=12, supplier="ABC")
p_b = Prodotto(name="Mouse", price=10, quantity=25, supplier="CDE")

print("myproduct1 == p_a?", myproduct1 == p_a)  # va a chiamare il metodo  __eq__ appena implementanto mi aspetto True

print("myproduct1 == p_b?", myproduct1 == p_b)  # va a chiamare il metodo  __eq__ appena implementanto mi aspetto False

myList = [p_a, p_b, myproduct1]

myList.sort()

print("lista prodotti ordinata")
for p in myList:
    print(f"- {p}")

my_product_scontato = ProdottoScontato(name="Auricolari", price=320, quantity=1, supplier="ABC", sconto_percento=10)
my_service = Servizio(name="Consulenza", tariffa_oraria=100, ore=3)

myList.append(my_product_scontato)
myList.append(my_service)

myList.sort(reverse=True)
for elem in myList:
    print(elem.name, "->", elem.prezzo_finale())

print("-----------------------------------------------------------")
# Definire una classe Abbonamento che abbia come attributi: "nome, prezzo_mensile, mesi"
# Abbonamento dovrà avere un metodo per calcolare il prezzo finale, ottenuto come prezzo_mensile*mesi

class Abbonamento:
    def __init__(self, name: str, prezzo_mensile: float, mesi: int):
        self.name = name
        self.prezzo_mensile = prezzo_mensile
        self.mesi = mesi

    def prezzo_finale(self) -> float:
        return self.prezzo_mensile * self.mesi


abb = Abbonamento(name="Software gestionale", prezzo_mensile=30.0, mesi=24)

myList.append(abb)
for elem in myList:
    print(elem.name, "->", elem.prezzo_finale())


def clacola_totale(elementi):
    tot = 0
    for e in elementi:
        tot += e.prezzo_finale()
    return tot

print(f"Il totale è: {clacola_totale(myList)}")
print("-----------------------------------------------------------")
from typing import Protocol

class HaPrezzoFinale(Protocol):
    def prezzo_finale(self) -> float:
        ...

def calcola_totale(elementi:list[HaPrezzoFinale]) ->float:
    return sum(e.prezzo_finale() for e in elementi)
print(f"Il totale è: {clacola_totale(myList)}")

print("-----------------------------------------------------------")


from dataclasses import dataclass
@dataclass
class ProdottoRecord:
    nome:str
    prezzo_unitario: float

@dataclass
class ClienteRecord :
    name: str
    email: str
    categoria: str


@dataclass
class RigaOrdine:
    prodotto:ProdottoRecord
    quantita:int

    def totale_riga(self):
        return self.prodotto.prezzo_unitario * self.quantita


@dataclass
class  Ordine:
    righe : list[RigaOrdine]
    cliente : ClienteRecord

    def totale_netto(self):
        return sum(r.totale_riga() for r in self.righe)

    def totale_lordo (self, aliquota_iva):
        return self.totale_netto()*(1+aliquota_iva)

    def numero_righe(self):
        return len(self.righe)

@dataclass
class OrdineConSconto(Ordine):
    sconto_percentuale: float

    def totale_scontato(self):
        self.totale_lordo()*(1-self.sconto_percentuale)

    def totale_netto(self):
        netto_base = super().totale_netto()
        return netto_base*(1-self.sconto_percentuale)


cliente1 = ClienteRecord("Mario Rossi","mariorossi@example.com", "Gold")
p1 = ProdottoRecord("Laptop", 1200.0)
p2 = ProdottoRecord("Mouse", 20)

ordine = Ordine([RigaOrdine(p1, 2), RigaOrdine(p2,10)], cliente1)
ordine_scontato = OrdineConSconto([RigaOrdine(p1, 2), RigaOrdine(p2,10)], cliente1,0.1)


print(ordine)
print("Numero di righe nell'ordine: ", ordine.numero_righe())
print("Totale netto: ", ordine.totale_netto())
print("Total lordo( IVA 22%): ", ordine.totale_lordo(0.22))

print(ordine_scontato)
print("Totale netto sconto: ", ordine_scontato.totale_netto())
print( "Totale lordo scontato: ", ordine_scontato.totale_lordo(0.22))

print("-----------------------------------------------------------")






print("-----------------------------------------------------------")
# Scrivere una classe Cliente che abbia i campi "nome","email","categoria"("Gold","Silver","Bronze")
# vorremmo che questa calsse avesse un metodo che chiamiamo "descrizione"
# che deve restituriee una stringa formattata ad esempio
# Cliente Fulvio Bianchi (Gold) - email"

class Cliente:

    def __init__(self, name: str, email: str, categoria: str):
        self.name = name
        self.email = email
        self.categoria = categoria

    def descrizione(self):
        return (f"Cliente {self.name} ({self.categoria}) - {self.email}")


c1 = Cliente(name="Mario Bianchi", email="mario.bianchi@gmail.com", categoria="Gold")
print(c1.descrizione())
