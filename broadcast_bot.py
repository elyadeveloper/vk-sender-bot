import asyncio
import threading
import time
from typing import List, Optional, Dict
from vk_sender import VKSender
from config import Config

class BroadcastBot:
    def __init__(self):
        self.vk_sender = None
        self._init_senders()
    
    def _init_senders(self):
        try:
            if Config.VK_TOKEN:
                self.vk_sender = VKSender()
                print("VK отправитель инициализирован")
            else:
                print("VK_TOKEN не настроен, VK рассылка недоступна")
        except Exception as e:
            print(f"Ошибка инициализации отправителей: {e}")
            raise
    
    def start(self):
        print("Запуск бота для рассылки VK...")
        print("Бот успешно запущен!")
    
    def send_to_vk(self, message: str, chat_ids: Optional[List[int]] = None) -> Dict:
        if not self.vk_sender:
            print("VK отправитель не инициализирован")
            return {"success": 0, "failed": 0, "total": 0}
        return self.vk_sender.send_broadcast(message, chat_ids)
    
    async def send_broadcast(self, message: str, vk_chat_ids: Optional[List[int]] = None) -> Dict:
        print(f"Начинаю рассылку сообщения: {message[:50]}...")
        results = {
            "vk": {"success": 0, "failed": 0, "total": 0},
            "total_success": 0,
            "total_failed": 0,
            "total_sent": 0
        }
        if self.vk_sender:
            vk_result = self.send_to_vk(message, vk_chat_ids)
            results["vk"] = vk_result
            results["total_success"] += vk_result["success"]
            results["total_failed"] += vk_result["failed"]
            results["total_sent"] += vk_result["total"]
        print(f"Итоговый результат рассылки:")
        print(f"   VK: {results['vk']['success']}/{results['vk']['total']} успешно")
        print(f"   Общий итог: {results['total_success']}/{results['total_sent']} успешно")
        return results
    
    def add_vk_chat(self, chat_id: int):
        if chat_id not in Config.VK_CHAT_IDS:
            Config.VK_CHAT_IDS.append(chat_id)
            print(f"Добавлена VK беседа {chat_id} в список рассылки")
        else:
            print(f"VK беседа {chat_id} уже в списке рассылки")
    
    def remove_vk_chat(self, chat_id: int):
        if chat_id in Config.VK_CHAT_IDS:
            Config.VK_CHAT_IDS.remove(chat_id)
            print(f"Удалена VK беседа {chat_id} из списка рассылки")
        else:
            print(f"VK беседа {chat_id} не найдена в списке рассылки")
    
    def get_status(self) -> Dict:
        return {
            "vk_initialized": self.vk_sender is not None,
            "vk_chat_count": len(Config.VK_CHAT_IDS),
            "vk_chats": Config.VK_CHAT_IDS
        } 