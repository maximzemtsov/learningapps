import os
import time
import random
from vk_messages import MessagesAPI
from vk_messages.utils import (cleanhtml, get_random, get_creators,
                               fast_parser, get_attachments)
import requests
from pprint import pprint


def SendMessage(vk, name, filename, login, password, peer_id):
    # filename = 'rose.jpeg'
    # login, password = '+79536716200', 'QAzse$123'
    # peer_id = '-198672265'  # elementobot dialog

    # Авторизовались
    # vk = MessagesAPI(login=login, password=password, two_factor=False)  # two_factor auth parametr

    # Получили ссылку на изображение
    upload_url = vk.method('photos.getMessagesUploadServer', peer_id=peer_id)

    print('Получена ссылка для загрузки изображения {}'.format(upload_url['upload_url']))

    # Отправили изображение на сервер
    request = requests.post(upload_url['upload_url'], files={'photo': open(filename, "rb")})
    params = {'photo': request.json()['photo'],
              'server': request.json()['server'],
              'hash': request.json()['hash']}
    # Сохранили изображение
    save = vk.method('photos.saveMessagesPhoto',
                     photo=request.json()['photo'],
                     server=request.json()['server'],
                     hash=request.json()['hash'])
    # Отправляем изображение
    att = 'photo{}_{}'.format(save[0]['owner_id'], save[0]['id'])
    send = vk.method('messages.send',
                     user_id=peer_id,
                     random_id=get_random(),
                     message='Я немного пофлужу',
                     attachment=att)  # vk_api library on github

    pprint(send)
    # Можно получить ответ на изображение и обработать его.

    print('Файл {} обработан.'.format(filename))


def Sender(login, password, peer_id, start=None, count=1000):
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

    pprint('Найдено {} изображений'.format(len(imageList)))

    index = 0
    isStart = False

    if start == None:
        isStart = True

    API = MessagesAPI(login=login, password=password, two_factor=False)  # two_factor auth parametr

    for name in sorted(imageList.keys()):
        fullPath = imageList[name]
        if name[:-4] == start:
            isStart = True
        if isStart == True:
            pprint('{}-{}'.format(name[:-4], fullPath))
            SendMessage(vk=API,
                        name=name,
                        filename=fullPath,
                        login=login,
                        password=password,
                        peer_id=peer_id)
            delay = random.randint(1, 7)
            print('Задержка постинга следующего изображения - {}секунд'.format(delay))
            time.sleep(delay)
            index = index + 1
        if index >= count:
            break
    print('Конец обработки программы')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Sender('+79536716200', 'QAzse$123', '-198672265')
