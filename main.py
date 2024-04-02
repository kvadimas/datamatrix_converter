import os
import time
from pylibdmtx.pylibdmtx import decode, encode
from PIL import Image


def time_of_function(function):
    """Декоратор замера времени"""
    def wrapped(*args):
        start_time = time.time()
        res = function(*args)
        print(time.time() - start_time)
        return res
    return wrapped

# Указываем путь к директории
directory = "./datamatrix/"

dm_codes = [
    "datamatrix_test_1",
    "datamatrix_test_2",
    "datamatrix_test_3",
    "datamatrix_test_4",
    "datamatrix_test_5",
    "datamatrix_test_6",
    "datamatrix_test_7"
]


def dm_decode(file_path: str):
    """Читает коды"""
    if os.path.exists(file_path):
        img = Image.open(file_path)
        res = decode(img)[0].data.decode('utf-8')
    else:
        res = f"Файл {file_path} не найден."
    return res


def dm_encode(code: str, name: str, save_path: str):
    """Генерирует коды"""
    encoded = encode(code.encode('utf8'))
    img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
    img.save(save_path + name + '.png')


def read_path(directory: str):
    """Получаем список файлов"""
    return sorted(os.listdir(directory))


def save_list(row: list, save_path: str):
    with open(save_path + "res.txt", "w") as file:
        print(*row, file=file, sep="\n")


@time_of_function
def main():
    #for i in range(len(dm_codes)):
    #    dm_encode(dm_codes[i], f"code{i}", directory)
    codes = []
    for j in read_path(directory):
        codes.append(dm_decode(directory + j))
        save_list(codes, directory)


if __name__ == "__main__":
    main()
