from Easy.massage import *

def hello ():
    print(colors.BEIGE + """
 _____      _                           _____                                 
|  ___|    | |                         /  ___|                                
| |__ _ __ | |_ _ __ ___  _ __  _   _  \\ `--.  ___ __ _ _ __  _ __   ___ _ __ 
|  __| '_ \\| __| '__/ _ \\| '_ \\| | | |  `--. \\/ __/ _` | '_ \\| '_ \\ / _ \\ '__|
| |__| | | | |_| | | (_) | |_) | |_| | /\\__/ / (_| (_| | | | | | | |  __/ |   
\\____/_| |_|\\__|_|  \\___/| .__/ \\__, | \\____/ \\___\\__,_|_| |_|_| |_|\\___|_|   
                         | |     __/ |                                        
                         |_|    |___/                                         
    
"""+ colors.END)

def get_numbers_tuple():
    while 1:
        inform ("Enter your size (x, y):", end = "")
        input_string = input("")
        try:
            numbers = tuple(map(int, input_string.split(',')))
            if numbers[0] < 0 or numbers[1] < 0:
                raise ("Value erro. Some of the entered data is less than 0!")
            return numbers
        except:
            failed ("Data entered incorrectly!\nThese must be 2 numbers greater than 0.")