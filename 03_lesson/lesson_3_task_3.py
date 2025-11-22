from address import Address
from mailing import Mailing

to_address = Address("123456", "Москва", "Ленина", "15", "25")
from_address = Address("654321", "Санкт-Петербург", "Пушкина", "42", "17")

mailing = Mailing(
    to_address=to_address,
    from_address=from_address,
    cost=500,
    track="TRACK123456789"
)

print(f"Отправление {mailing.track} из {mailing.from_address.index}, {mailing.from_address.city}, {mailing.from_address.street}, {mailing.from_address.house} - {mailing.from_address.apartment} в {mailing.to_address.index}, {mailing.to_address.city}, {mailing.to_address.street}, {mailing.to_address.house} - {mailing.to_address.apartment}. Стоимость {mailing.cost} рублей.")