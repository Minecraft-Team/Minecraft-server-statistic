import os


class Constants:
    LOGS_DIR = 'logs'
    DATA = '.data'

    NORMAL_PLAYERS = []

    DATE_FORMAT = '%Y-%m-%d'
    DAY_FORMAT = '%H:%M:%S'

    # VK bot
    VK_BOT_ACCESS_TOKEN = os.getenv('VK_BOT_ACCESS_TOKEN')
    CHAT_ID = os.getenv('VK_BOT_CHAT_ID')

    # VK tags
    SERVER_TAG = '#server'
    STATISTICS_TAG = '#statistics'

    # Pastebin service
    PASTEBIN_DEV_KEY = os.getenv('PASTEBIN_DEV_KEY')

    # Text to image service
    BACKGROUND_COLOR = (0, 0, 0)
    TEXT_COLOR = (255, 255, 0)
    TEXT_PADDING = 50
    TEXT_FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'   # linux monospace font
    FONT_SIZE = 30
