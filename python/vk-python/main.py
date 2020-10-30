import math
import os
import pandas as pd
from pprint import pprint
import operator
import vk_api

import requests  # to get image from the web
import shutil  # to save it locally


def DownloadImage(image_url, filename, is_in):
    if is_in == True:
        filename = image_url.split("/")[-1]

    r = requests.get(image_url, stream=True)

    if r.status_code == 200:
        r.raw.decode_content = True
        with open(filename + '.jpg', 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        print('Изображение {} скопировано верно {}'.format(image_url.split("/")[-1], filename))
    else:
        print('Проблемы с загрузкой картинки'.format(image_url.split("/")[-1]))


##
#   Номер группы в VK.
#   положительное число после club- в адресе группы)
##
def Parser(login, password, groupID):
    # Настраиваем пути
    currentPath = os.getcwd()

    if os.path.exists(currentPath):
        print(currentPath)
    else:
        print("Путь не найден. Завершаю работу")
        exit

    imageSource = currentPath + "/images/"

    if not os.path.exists(imageSource):
        pprint('Создаем директорию out_image')
        os.mkdir(imageSource)
    else:
        pprint("Найдена директория сохранения результатов обработки")

    # авторизуемся
    vk_session = vk_api.VkApi(login, password, api_version='5.131')
    vk_session.auth()
    vk = vk_session.get_api()
    group = vk.market.get(owner_id=-1 * groupID,
                          album_id=0,  # идентификатор подборки, товары из которой нужно вернуть
                          count=1,  # максимальное значение 200, по умолчанию 100
                          offset=0,  # положительное число
                          extended=1, )
    pprint(len(group))
    productTable = pd.DataFrame(columns=['id', 'description', 'photo', 'article'])
    index = 0
    step = 100
    while index < group['count']:
        group = vk.market.get(owner_id=-1 * groupID,
                              album_id=0,  # идентификатор подборки, товары из которой нужно вернуть
                              count=100,  # максимальное значение 200, по умолчанию 100
                              offset=index,  # положительное число
                              extended=1, )
        for item in group['items']:
            urlImage = ''
            if len(item['photos']) > 0:
                imgs = item['photos']
                img = imgs[0]
                # Вот блин как бы не забыть
                # max(d['price'] for d in myList)
                # max(lst, key=lambda x: x['price'])
                max_img0 = max(img['sizes'], key=lambda x: x['height'])  # max(d['height'] for d in img['sizes'])
                urlImage = max_img0['url']
                index += 1

            else:
                urlImage = ''

            sku = ''
            if 'sku' in item:
                sku = item['sku']

            productTable = productTable.append({'id': item['id'],
                                                'name': item['title'],
                                                'description': item['description'],
                                                # И вот права ты что делить придется
                                                'price': int(item['price']['amount']) / 100,
                                                'article': "",
                                                'photo': urlImage,
                                                'sku': sku},
                                               ignore_index=True)
            #DownloadImage(urlImage, imageSource + str(item['id']), False)

    productTable.to_csv(currentPath + '/Parsing_{}.csv'.format(groupID))
    # upload photo
    # https://github.com/python273/vk_api/blob/master/examples/upload_photo.py


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Parser('+79536716200', 'QAzse$123', 165036111)
