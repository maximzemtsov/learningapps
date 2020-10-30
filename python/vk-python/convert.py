import math
import os
from pprint import pprint
# Для работы с изображениями используем эту либу
# https://pillow.readthedocs.io/en/stable/
import PIL as pl;
import PIL.Image as Image


def converter_():
    currentPath = os.getcwd()

    imageList = dict()
    if os.path.exists(currentPath):
        print(currentPath)
    else:
        print("Путь не найден. Завершаю работу")
        exit

    currentImageSourcePath = currentPath + "/images/"

    # r=root, d=directories, f = files
    for r, d, f in os.walk(currentImageSourcePath):
        for file in f:
            if ('.png' in file) or ('jpg' in file):
                imageList.update({file: os.path.join(r, file)})

    if len(imageList) == 0:
        pprint('Файлы не найдены')
    else:
        pprint(imageList)

    # ресайзим по центру в соотношение 2:1
    # сохраняем их в директорию out_image
    outAddBarPath = currentPath + "/add_white_bar/"
    if not os.path.exists(outAddBarPath):
        pprint('Создаем директорию out_image')
        os.mkdir(outAddBarPath)
    else:
        pprint("Найдена директория сохранения результатов обработки")

    outCropPath = currentPath + "/crop_height/"
    if not os.path.exists(outCropPath):
        pprint('Создаем директорию out_image')
        os.mkdir(outCropPath)
    else:
        pprint("Найдена директория сохранения результатов обработки")

    """
    У МилаМи все фото вертикальные, как эта
    для карусели нужен размер 
    884x544 пикселей, 
    это уже правильное соотношение
    то есть нужно белые поля по бокам добавить
    """

    deltaPixels = 8 / 13  # 544.0 / 884  # Соотношение высоты и ширины нужное.
    targetWidth = 442
    targetHeight = 272

    for name, fullPath in imageList.items():
        convert_image_width_add(name, fullPath, outAddBarPath, deltaPixels, targetWidth, targetHeight)
        convert_image_crop(name, fullPath, outCropPath, deltaPixels, targetWidth, targetHeight)


'''
Метод конвертации изображения путем добавления по ширине
'''


def convert_image_width_add(name, fullPath, outPath, deltaPixels, targetWidth, targetHeight):
    im = Image.open(fullPath)  # Открыли изображение
    if im.height / im.width != deltaPixels:
        # Для начала проверим и установим нужную нам высоту картинки
        # для этого ресайзим пропорционально ширину и высоту,
        # подгоняя высоту под заданное значение
        if im.height != targetHeight:
            dy = targetHeight / im.height
            im = im.resize((int(im.width * dy), targetHeight))

        # Далее зададим канвас с заданными значениями ширины и длины
        old_width, old_height = im.size
        # зададим центр
        x1 = int(math.floor((targetWidth - old_width) / 2))
        y1 = int(math.floor((targetHeight - old_height) / 2))
        # Скопируем режим изображения
        mode = im.mode
        if len(mode) == 1:  # L, 1
            new_background = (255)
        if len(mode) == 3:  # RGB
            new_background = (255, 255, 255)
        if len(mode) == 4:  # RGBA, CMYK
            new_background = (255, 255, 255, 255)
        # Создадим новый холст
        newImage = Image.new(mode, (targetWidth, targetHeight), new_background)
        newImage.paste(im, (x1, y1, x1 + old_width, y1 + old_height))
        im = newImage
    im.save(outPath + name, dpi=(300, 300), quality=95)
    pprint('Файл ' + name + " обработан успешно")


'''
Метод конвертации изображения путем обрезания по высоте
'''


def convert_image_crop(name, fullPath, outPath, deltaPixels, targetWidth, targetHeight):
    im = Image.open(fullPath)  # Открыли изображение

    # будем проверять если ширина меньше targetWidth пикселей, то ставим ширину targetWidth
    if im.width != targetWidth:
        dx = targetWidth / im.width
        im = im.resize((targetWidth, int(im.height * dx)))

    old_width, old_height = im.size
    # зададим центр
    x1 = int(math.floor((targetWidth - old_width) / 2))
    y1 = int(math.floor((targetHeight - old_height) / 2))
    # Скопируем режим изображения
    mode = im.mode
    if len(mode) == 1:  # L, 1
        new_background = (255)
    if len(mode) == 3:  # RGB
        new_background = (255, 255, 255)
    if len(mode) == 4:  # RGBA, CMYK
        new_background = (255, 255, 255, 255)
    # Создадим новый холст
    newImage = Image.new(mode, (targetWidth, targetHeight), new_background)
    # Вставим в новый холст текущее изображение по центру
    newImage.paste(im, (x1, y1, x1 + old_width, y1 + old_height))
    im = newImage
    im.save(outPath + name, dpi=(300, 300), quality=95)
    pprint('Файл ' + name + " обработан успешно")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    converter_()
