# 靡不有初，鲜克有终
# 开发时间：2022/3/4 20:12

'''
# 案例1 求Π
import random
# PI=概率*4
total = 1000  # 点数
in_count = 0
for i in range(total):
    x = random.random()  # 0-1
    y = random.random()
    distance = (x**2+y**2)**0.5
    if distance < 1:
        in_count += 1
print('PI=', (in_count/total)*4)'''

# 案例2 求不规则图形的面积(在python3.8base的环境下)
from PIL import Image
import random
img = Image.open('SEU_logo.png')
total = 100
black_count = 0
for i in range(total):
    x = random.randint(0, img.width - 1)  # randint随机数是包含边界的
    y = random.randint(0, img.height - 1)
    color = img.getpixel((x, y))
    if color == (1, 1, 1):
        black_count += 1
print(black_count/total)
print((black_count/total)*img.width*img.height)

total = 1000
black_count = 0
for i in range(total):
    x = random.randint(0, img.width - 1)  # randint随机数是包含边界的
    y = random.randint(0, img.height - 1)
    color = img.getpixel((x, y))
    if color == (1, 1, 1):
        black_count += 1
print(black_count/total)
print((black_count/total)*img.width*img.height)

total = 10000
black_count = 0
for i in range(total):
    x = random.randint(0, img.width - 1)  # randint随机数是包含边界的
    y = random.randint(0, img.height - 1)
    color = img.getpixel((x, y))
    if color == (1, 1, 1):
        black_count += 1
print(black_count/total)
print((black_count/total)*img.width*img.height)

total = 100000
black_count = 0
for i in range(total):
    x = random.randint(0, img.width - 1)  # randint随机数是包含边界的
    y = random.randint(0, img.height - 1)
    color = img.getpixel((x, y))
    if color == (1, 1, 1):
        black_count += 1
print(black_count/total)
print((black_count/total)*img.width*img.height)

total = 1000000
black_count = 0
for i in range(total):
    x = random.randint(0, img.width - 1)  # randint随机数是包含边界的
    y = random.randint(0, img.height - 1)
    color = img.getpixel((x, y))
    if color == (1, 1, 1):
        black_count += 1
print(black_count/total)
print((black_count/total)*img.width*img.height)

# 标准答案
other_count = 0
black_count_1 = 0
for x in range(0, img.width):
    for y in range(0, img.height):
        color = img.getpixel((x, y))
        if color == (1, 1, 1):
            black_count_1 += 1
        else:
            other_count += 1
print(black_count_1/other_count)
print((black_count_1/other_count)*img.width*img.height)



