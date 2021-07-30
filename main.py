from aiogram import Bot, types, Dispatcher, executor
from os import chdir
import numpy as np
import cv2
from time import sleep
BLACK = '⬛️' 
WHITE = '⬜️'
FRAME_SIZE = (20,16)
def get_color(color_key):
    return WHITE if color_key > 127.5 else BLACK
def calc_average_color(color_stream):
        return  [[get_color(sum(i) / len(i)) for i in row ] for row in cv2.resize(color_stream, FRAME_SIZE)]
bot = Bot('BOT:TOKEN')
dp = Dispatcher(bot)
chdir('/path/to/video')
stop_timer = False
@dp.message_handler(commands=['start'])
async def Start(message: types.Message):
    if message.from_user.id != 1026133582:
        return
    cap = cv2.VideoCapture('bad apple.mp4')
    m_id = message.message_id + 1
    await bot.send_message(message.chat.id, BLACK * FRAME_SIZE[1] * FRAME_SIZE[0])
    i = 0 
    f = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            if not f % 5 == 0: # 30 fps to 24 fps
                colors = '\n'.join([''.join(i) for i in calc_average_color(frame)])
                await bot.edit_message_text(colors + f'\n{i}', message.chat.id, m_id)
                i+= 1
        else:
            print('error or eof')
            break
        f += 1
        sleep(4) # so as not to flood
if __name__ == '__main__':
    executor.start_polling(dp)