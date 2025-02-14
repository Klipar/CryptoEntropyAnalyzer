import struct

# Відкриваємо файл у бінарному режимі
with open('1', 'rb') as file:
    # Читаємо байт
    byte = file.read(1)
    while byte:
        # Перетворюємо байт у ціле число
        value = struct.unpack('B', byte)[0]
        print(f'Байт: {value} \t(бінарний: {value:08b})')
        byte = file.read(1)