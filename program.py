from PIL import Image
import random

def text_to_decimals(text): 
    return [int(ord(element)) for element in text]

def decimals_to_binaries(decimals): 
    return [int(format(element,'b')) for element in decimals] 

def binaries_to_decimals(binaries): 
    return [int(str(element),2) for element in binaries]

def decimals_to_text(decimals):
    return[chr(int(element)) for element in decimals]

def binary_to_decimal(element):
    return int(str(element),2)

def length_reduction(text, length):
    if len(text)<length:
            num=length-len(text)
            reducted_str=''
            for i in range(num):
                reducted_str='0'+reducted_str
            text=reducted_str+text
    return text

def get_parametrs(column_number, row_number, width, pixel, next_key):
    column_number=(column_number)+1+(next_key//24)
    row_number=row_number+((column_number)//width)
    column_number=(column_number)%width
    color=next_key%24//8
    bit_number=next_key%24%8
    next_key=pixel[column_number,row_number][(color+1)%3]
    pix=int(format(pixel[column_number,row_number][color], 'b'))
    pix_str=length_reduction(str(pix), 8)
    return(column_number,row_number,color,next_key,pix,pix_str,bit_number)

def start():
    print("Введите имя файла: ")
    file_name=input()
    image = Image.open(file_name) 
    pixel = image.load()
    width, height = image.size
    return(pixel,width,height,image)
def encryption_decryption(key, numbers):
    random.seed(key)
    gamming_numbers=[]
    for element in numbers:
        gamma=random.randint(0,65535)
        gamming_numbers.append(element^gamma)
    return gamming_numbers
def encode():
    pixel,width,height,image=start()
    print("Введите информацию:")
    s=input()
    key=random.randint(0,255)
    print("Ключ:", key)
    message_length=len(s)
    print("Длина сообщения:", message_length)
    column_number=0
    row_number=0
    decimals_text=text_to_decimals(s)
    decimals_text=encryption_decryption(key, decimals_text)
    bin_text=decimals_to_binaries(decimals_text)
    next_key=key
    for letter in bin_text:
        letter=length_reduction(str(letter), 16)
        for changed_bit in letter:
            column_number,row_number,color,next_key,changed_pixel,changed_pixel_str,bit_number=get_parametrs(column_number, row_number, width, pixel, next_key)
            if (int(changed_pixel_str[7-bit_number])<int(changed_bit)):
                changed_pixel=changed_pixel+10**bit_number
            elif (int(changed_pixel_str[7-bit_number])>int(changed_bit)):
                changed_pixel=changed_pixel-10**bit_number
            changed_pixel=binary_to_decimal(changed_pixel)
            old_pix=list(pixel[column_number,row_number])
            old_pix[color]=changed_pixel
            pixel[column_number,row_number]=tuple(old_pix)
    print("Введите имя файла для сохранения: ")
    file_save=input()
    image.save(file_save)

def decode():
    pixel,width,height,image=start()
    key=int(input("Введите ключ:"))
    length=int(input("Введите длину сообщения:"))
    column_number=0
    row_number=0
    info=[]
    next_key=key
    for n in range(length):
        dec_info=''
        for m in range(16):
            column_number,row_number,color,next_key,taken_pixel,taken_pixel_str,bit_number=get_parametrs(column_number, row_number, width, pixel, next_key)
            dec_info=dec_info+taken_pixel_str[7-bit_number]
        info.append(dec_info)
    decimals_text=binaries_to_decimals(info)
    decimals_text=encryption_decryption(key, decimals_text)
    letters=decimals_to_text(decimals_text)
    information=''
    for i in letters:
        information=information+i
    print("Расшифрованное сообщение: ", information)

def menu():
    while True:
        a = int(input(" 1. Зашифровать\n 2. Расшифровать\n 3. Выход\n"))
        if (a==1):
            encode()
        elif (a==2):
            decode()
        elif (a==3):
            break
        else:
            print("Введите корректную информацию")
menu()
