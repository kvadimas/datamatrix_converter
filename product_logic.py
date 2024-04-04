from pylibdmtx.pylibdmtx import decode, encode
from PIL import Image


def dm_decode(file, name: str):
    """Читает коды"""
    try:
        img = Image.open(file)
        res = decode(img)[0].data.decode('utf-8')
    except:
        res = f"Файл {name} поврежден."
    return res


def dm_encode(code: str, name: str, save_path: str):
    """Генерирует коды"""
    encoded = encode(code.encode('utf8'))
    img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
    img.save(save_path + name + '.png')
