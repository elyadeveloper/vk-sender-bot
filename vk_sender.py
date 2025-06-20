import vk_api
import asyncio
import time
from typing import List, Optional
from config import Config

class VKSender:
    def __init__(self):
        self.vk_session = None
        self.vk = None
        self._init_vk()
    
    def _init_vk(self):
        try:
            if not Config.VK_TOKEN:
                raise ValueError("VK_TOKEN не найден в конфигурации")
            
            self.vk_session = vk_api.VkApi(token=Config.VK_TOKEN)
            self.vk = self.vk_session.get_api()
    
            try:
                user_info = self.vk.users.get()[0]
                print(f"✅ VK API успешно инициализирован (пользователь: {user_info['first_name']} {user_info['last_name']})")
            except:
                try:
                    group_info = self.vk.groups.getById()[0]
                    print(f"✅ VK API успешно инициализирован (группа: {group_info['name']})")
                except:
                    print("✅ VK API успешно инициализирован (тип токена не определен)")
                    
        except Exception as e:
            print(f"❌ Ошибка инициализации VK API: {e}")
            raise
    
    def get_user_chats(self):
        try:
            dialogs = self.vk.messages.getDialogs(count=200)
            chats = []
            
            for item in dialogs['items']:
                if 'chat_id' in item['message']:
                    chat_id = item['message']['chat_id']
                    chat_title = item['message']['title'] if 'title' in item['message'] else f"Беседа {chat_id}"
                    chats.append({
                        'id': chat_id,
                        'title': chat_title
                    })
            
            return chats
        except Exception as e:
            print(f"❌ Ошибка получения списка бесед: {e}")
            return []
    
    def send_message_to_chat(self, chat_id: int, message: str, retries: int = 0) -> bool:
        try:
            try:
                result = self.vk.messages.send(
                    chat_id=chat_id,
                    message=message,
                    random_id=0
                )
                print(f"✅ Сообщение отправлено в VK беседу {chat_id} (способ 1)")
                return True
            except Exception as e1:
                print(f"⚠️ Способ 1 не сработал: {e1}")
                
                peer_id = 2000000000 + chat_id
                result = self.vk.messages.send(
                    peer_id=peer_id,
                    message=message,
                    random_id=0
                )
                print(f"✅ Сообщение отправлено в VK беседу {chat_id} (способ 2, peer_id: {peer_id})")
                return True
                
        except Exception as e:
            if retries < Config.MAX_RETRIES:
                print(f"⚠️ Попытка {retries + 1} не удалась для VK беседы {chat_id}: {e}")
                time.sleep(2)
                return self.send_message_to_chat(chat_id, message, retries + 1)
            else:
                print(f"❌ Не удалось отправить сообщение в VK беседу {chat_id}: {e}")
                return False
    
    def send_message_to_user(self, user_id: int, message: str, retries: int = 0) -> bool:
        try:
            result = self.vk.messages.send(
                user_id=user_id,
                message=message,
                random_id=0
            )
            print(f"✅ Сообщение отправлено пользователю VK {user_id}")
            return True
        except Exception as e:
            if retries < Config.MAX_RETRIES:
                print(f"⚠️ Попытка {retries + 1} не удалась для пользователя VK {user_id}: {e}")
                time.sleep(2)
                return self.send_message_to_user(user_id, message, retries + 1)
            else:
                print(f"❌ Не удалось отправить сообщение пользователю VK {user_id}: {e}")
                return False
    
    def send_broadcast(self, message: str, chat_ids: Optional[List[int]] = None) -> dict:
        if chat_ids is None:
            chat_ids = Config.VK_CHAT_IDS
        
        if not chat_ids:
            print("⚠️ Список ID бесед ВКонтакте пуст")
            return {"success": 0, "failed": 0, "total": 0}
        
        success_count = 0
        failed_count = 0
        
        print(f"📤 Начинаю рассылку в {len(chat_ids)} бесед ВКонтакте...")
        
        for chat_id in chat_ids:
            if self.send_message_to_chat(chat_id, message):
                success_count += 1
            else:
                failed_count += 1
            time.sleep(Config.MESSAGE_DELAY)
        
        result = {
            "success": success_count,
            "failed": failed_count,
            "total": len(chat_ids)
        }
        
        print(f"📊 Результат рассылки VK: {success_count} успешно, {failed_count} неудачно")
        return result 