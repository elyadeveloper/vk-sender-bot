import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # VK настройки
    VK_TOKEN = ''
    
    # Список ID бесед ВКонтакте для рассылки
    VK_CHAT_IDS = []
    
    # Настройки рассылки
    MESSAGE_DELAY = 1  # Задержка между отправкой сообщений в секундах
    MAX_RETRIES = 3    # Максимальное количество попыток отправки 