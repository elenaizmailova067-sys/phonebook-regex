import csv
import re
from pprint import pprint

# чтение
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

header = contacts_list[0]
data = contacts_list[1:]

# разбор фио
for contact in data:
    fio_parts = " ".join(contact[:3]).split()
    fio_parts = (fio_parts + ["", "", ""])[:3]
    contact[:3] = fio_parts

# тел.
phone_pattern = re.compile(
    r"(?:\+7|8)?\s*\(?(?P<code>\d{3})\)?[\s-]*(?P<p1>\d{3})[\s-]*(?P<p2>\d{2})[\s-]*(?P<p3>\d{2})"
    r"(?:\s*(?:доб\.?|ext\.?|#)\s*(?P<ext>\d+))?"
)

def normalize_phone(phone: str) -> str:
    if not phone:
        return ""
    m = phone_pattern.search(phone)
    if not m:
        return phone
    base = f"+7({m['code']}){m['p1']}-{m['p2']}-{m['p3']}"
    if m["ext"]:
        base += f" доб.{m['ext']}"
    return base

for contact in data:
    contact[5] = normalize_phone(contact[5])

# дубли
def merge_contacts(contacts):
    merged = {}
    for contact in contacts:
        key = (contact[0], contact[1])  # Фамилия + Имя
        if key not in merged:
            merged[key] = contact[:]
        else:
            existing = merged[key]
            for i in range(2, 7):
                if not existing[i] and contact[i]:
                    existing[i] = contact[i]
    return list(merged.values())

data = merge_contacts(data)

# запись
result = [header] + data

with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    datawriter = csv.writer(f, delimiter=",")
    datawriter.writerows(result)

pprint(result)