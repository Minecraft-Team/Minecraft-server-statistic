import os
import datetime
import random

import vk_api as vk
import requests
from PIL import Image, ImageDraw, ImageFont

from app.constants import Constants


class PastebinService:
    def __init__(self):
        self.pastebin_dev_key = Constants.PASTEBIN_DEV_KEY

    def create_new_paste(self, text):
        now = datetime.datetime.now()
        post = requests.post('https://pastebin.com/api/api_post.php',
                             data={'api_dev_key': self.pastebin_dev_key,
                                   'api_option': 'paste',
                                   'api_paste_name': f'Server statistics: {now.strftime("%Y-%m-%d %H.%M.%S")}',
                                   'api_paste_code': text})
        return post.text[8:]


class TextToImageService:
    def __init__(self):
        self.background_color = Constants.BACKGROUND_COLOR
        self.text_color = Constants.TEXT_COLOR
        self.text_padding = Constants.TEXT_PADDING
        self.text_font = Constants.TEXT_FONT
        self.font_size = Constants.FONT_SIZE

    def draw_text(self, text):
        font = ImageFont.truetype(self.text_font, self.font_size)

        # get size of text in image
        img = Image.new('RGB', (0, 0))
        draw = ImageDraw.Draw(img)
        text_size = list(draw.textsize(text, font))

        # fit text
        final_text_size = tuple(map(lambda size: size + self.text_padding, text_size))
        final_text_position = tuple([int(self.text_padding / 2)] * 2)

        # convert text to image
        img = Image.new('RGB', final_text_size, color=self.background_color)
        draw = ImageDraw.Draw(img)
        draw.text(final_text_position, text, fill=self.text_color, font=font)

        img_tmp_filename = f'statistics_tmp_png_{random.randint(0, 1 << 31)}.png'
        img.save(img_tmp_filename)

        return img_tmp_filename


class VkBotServerStatistics:
    def __init__(self):
        vk_session = vk.VkApi(token=Constants.VK_BOT_ACCESS_TOKEN)
        self.vk_api = vk_session.get_api()
        self.target_chat_id = Constants.VK_CHAT_ID

    def send_statistics(self, statistics):
        pastebin_service = PastebinService()
        link_to_raw_text_statistics = pastebin_service.create_new_paste(statistics)

        text_to_image_service = TextToImageService()
        img_filename = text_to_image_service.draw_text(statistics)
        image_descriptor = open(img_filename, 'rb')

        msg_upload_server = self.vk_api.photos.getMessagesUploadServer(peer_id=0)
        response = requests.post(msg_upload_server['upload_url'], files={'photo': image_descriptor})
        response = response.json()

        image_descriptor.close()
        os.remove(img_filename)

        vk_image_info = self.vk_api.photos.saveMessagesPhoto(photo=response['photo'],
                                                             server=response['server'],
                                                             hash=response['hash'])[0]

        self.vk_api.messages.send(peer_id=self.target_chat_id,
                                  message=(f'Link to the text statistics: {link_to_raw_text_statistics}\n'
                                           f'{Constants.SERVER_TAG} '
                                           f'{Constants.STATISTICS_TAG}'),
                                  random_id=random.randint(0, 1 << 31),
                                  attachment=f'photo{vk_image_info["owner_id"]}_{vk_image_info["id"]}')
