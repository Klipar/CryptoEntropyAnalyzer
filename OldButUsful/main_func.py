import struct

def read_bytes_from_file(filename, num_bytes):
    if num_bytes < 1:
        raise ValueError("Кількість байтів повинна бути не менше 1.")
    
    # Визначаємо формат на основі кількості байтів
    if num_bytes == 1:
        format_char = 'B'  # 8-бітне беззнакове ціле
    elif num_bytes == 2:
        format_char = 'H'  # 16-бітне беззнакове ціле
    elif num_bytes == 4:
        format_char = 'I'  # 32-бітне беззнакове ціле
    elif num_bytes == 8:
        format_char = 'Q'  # 64-бітне беззнакове ціле
    elif num_bytes == 16:
        format_char = '16s'  # 16 байтів (рядок)
    elif num_bytes == 32:
        format_char = '32s'  # 32 байти (рядок)
    elif num_bytes == 64:
        format_char = '64s'  # 64 байти (рядок)
    elif num_bytes == 128:
        format_char = '128s'  # 128 байтів (рядок)
    else:
        raise ValueError("Підтримуються лише 1, 2, 4, 8, 16, 32, 64 або 128 байтів.")

    bytes_per_value = struct.calcsize(format_char)  # Кількість байтів, необхідна для формату
    with open(filename, 'rb') as file:
        while True:
            # Читаємо задану кількість байтів
            bytes_data = file.read(bytes_per_value)
            if len(bytes_data) < bytes_per_value:
                # Якщо прочитано менше, ніж потрібно, виходимо з циклу
                break
            
            # Перетворюємо байти у значення
            if num_bytes in [1, 2, 4, 8]:
                value = struct.unpack(format_char, bytes_data)[0]
                print(f'{bytes_per_value}\tбайтів: {value}\t\t(бінарний: {value:0{bytes_per_value * 8}b})', end="\r")
            else:
                # Для рядків просто виводимо байти
                print(f'{bytes_per_value}\tбайтів: {bytes_data}\t\t(рядок)', end="\r")

# Виклик функції з файлом і кількістю байтів


filename = 'cont_small'  # Задайте назву вашого файлу
num_bytes = int(input("Введіть кількість байтів (1, 2, 4, 8, 16, 32, 64 або 128): "))
read_bytes_from_file(filename, num_bytes)

