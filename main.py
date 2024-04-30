import bitarray
import random
import math


def encoder(file_path: str):
    b_arr = bitarray.bitarray()
    with open('text.txt', 'r') as f:
        lines = f.read()
        b_arr.frombytes(lines.encode('utf-8'))
    l = len(b_arr)
    print(b_arr, '- bare')
    for i in range(l):
        if (2 ** i >= l + i + 1):
            num_cont_bits = i
            break

    # insert control bits filled with 0
    for i in range(num_cont_bits):
        b_arr.insert(pow(2, i) - 1, 0)

    cont_bits = [0]*num_cont_bits
    for i, bit in enumerate(b_arr):
        if bit:
            pos = i + 1
            for j in range(num_cont_bits):
                if pos % pow(2, j+1) != 0:
                    cont_bits[j] += 1
                    pos -= pos % pow(2, j+1)

    for i in range(num_cont_bits):
        b_arr[pow(2, i) - 1] = cont_bits[i] % 2

    return b_arr


def erorr_generator(bites: bitarray, n: int):
    error_pos = []
    for i in range(n):
        rand_pos = random.randint(0, len(bites))
        while rand_pos in error_pos:
            rand_pos = random.randint(0, len(bites))
        error_pos.append(rand_pos)
        bites[rand_pos] = (bites[rand_pos] + 1) % 2
        print("Ошибка на позиции:", rand_pos)
    return bites


def decode (bites: bitarray):
    l = len(bites)
    num_cont_bits = math.floor(math.log(l, 2)) + 1

    cont_bits = [0] * num_cont_bits
    for i, bit in enumerate(bites):
        if bit:
            pos = i + 1
            for j in range(num_cont_bits):
                if pos % pow(2, j + 1) != 0:
                    cont_bits[j] += 1
                    pos -= pos % pow(2, j + 1)

    error_pos = 0
    for i in range(num_cont_bits):
        cont_bits[i] = cont_bits[i] % 2
        error_pos += cont_bits[i] * pow(2, i)

    print("Найдена ошибка на позиции:", error_pos - 1)
    bites[error_pos-1] = (bites[error_pos-1] + 1) % 2
    return bites



rslt = encoder('text.txt')
print(rslt, " - encoded")
rslt = erorr_generator(rslt, 1)
print(rslt, " - bag")
print(decode(rslt), " - fixed")
