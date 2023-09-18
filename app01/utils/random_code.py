from PIL import Image, ImageDraw, ImageFont
import string
import random
from io import BytesIO


def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def random_code(size=(184, 44), length=4, point_num=100, line_num=15):
    width, height = size

    img = Image.new('RGB', (width, height), color=(255, 255, 255))  # 生成200*40的白色背景图
    draw = ImageDraw.Draw(img)  # 创建画布
    font = ImageFont.truetype(font='static/my/font/MexicanTequila.ttf', size=40)  # 字体

    str_all = string.digits + string.ascii_letters
    valid_code = ''
    for i in range(length):
        random_char = random.choice(str_all)
        draw.text((40 * i + 20, 5), random_char, (0, 0, 0), font=font)
        valid_code += random_char
    print(valid_code)

    # 随级生成点
    for i in range(point_num):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.point((x, y), random_color())

    # 随级划线
    for i in range(line_num):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), random_color())

    f = BytesIO()  # 创建内存句柄
    img.save(f, 'PNG')  # 将图片保存到内存句柄中
    data = f.getvalue()  # 读取内存句柄
    return data, valid_code


if __name__ == '__main__':
    random_code()
