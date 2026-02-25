class Prodotto:
    aliquota_iva = 0.22  # variabile di classe -- ovvero è la stessa per tutte le istanza che verranno create

    def __init__(self, name: str, price: float, quantity: int, supplier = None):

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

    # decoratore
    @classmethod
    def costruttore_con_quantità_uno(cls, name: str, price: float, supplier: str):
        return cls(name, price,quantity=1, supplier= supplier)

    @classmethod
    def applica_sconto(cls, prezzo, percentuale):
        return prezzo*(1-percentuale)



myproduct1 = Prodotto("Laptop", 1200.0, 12, "ABC")

myproduct1 = Prodotto(name="Laptop", price=1200.0, quantity=12, supplier="ABC")
print(f"Nome prodotto: {myproduct1.name}")
print(f"Prezzo prodotto: {myproduct1.price}")

print(f"Nome prodotto: {myproduct1.name}- prezzo : {myproduct1.price}")

p3 = Prodotto.costruttore_con_quantità_uno(name = "Auricolari ", price= 200., supplier="ABC")
print( f"prezzo scontato di myproduct 1  {Prodotto.applica_sconto(myproduct1.price, percentuale=0.15)}")

myproduct2 = Prodotto(name="Mouse", price=10, quantity=25, supplier="CDE")
print(f"Nome prodotto: {myproduct2.name}- prezzo : {myproduct2.price}")


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
