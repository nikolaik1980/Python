from smartphone import Smartphone

catalog = [
    Smartphone("Apple", "iPhone 17", "+79123456789"),
    Smartphone("Samsung", "Galaxy S24", "+79234567890"),
    Smartphone("Xiaomi", "Redmi Note 13", "+79345678901"),
    Smartphone("Honor", "Magic 7 Pro", "+79456789012"),
    Smartphone("Lenovo", "Moto G4", "+79567890123")
]

print("Каталог смартфонов:")

for smartphone in catalog:
    print(f"{smartphone.brand} - {smartphone.model}. {smartphone.phone_number}")