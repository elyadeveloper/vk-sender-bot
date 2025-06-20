import asyncio
import sys
from broadcast_bot import BroadcastBot

class BroadcastBotCLI:
    def __init__(self):
        self.bot = None
    
    def print_banner(self):
        print("=" * 60)
        print("Бот для рассылки сообщений в VK")
        print("=" * 60)
    
    def print_help(self):
        print("\nДоступные команды:")
        print("  start                    - Запустить бота")
        print("  status                   - Показать статус бота")
        print("  send <сообщение>         - Отправить сообщение во все VK беседы")
        print("  add_vk <chat_id>         - Добавить VK беседу в список рассылки")
        print("  remove_vk <chat_id>      - Удалить VK беседу из списка рассылки")
        print("  list                     - Показать все ID бесед")
        print("  chats                    - Показать доступные беседы пользователя")
        print("  help                     - Показать эту справку")
        print("  exit                     - Выйти из программы")
    
    async def start_bot(self):
        try:
            self.bot = BroadcastBot()
            self.bot.start()
            print("Бот успешно запущен и готов к работе.")
        except Exception as e:
            print(f"Ошибка запуска бота: {e}")
            return False
        return True
    
    def show_status(self):
        if not self.bot:
            print("Бот не запущен. Используйте команду 'start'")
            return
        status = self.bot.get_status()
        print("\nСтатус бота:")
        print(f"  VK отправитель: {'Активен' if status['vk_initialized'] else 'Неактивен'}")
        print(f"  VK бесед в списке: {status['vk_chat_count']}")
        if status['vk_chats']:
            print(f"  VK беседы: {', '.join(map(str, status['vk_chats']))}")
    
    def show_available_chats(self):
        if not self.bot:
            print("Бот не запущен. Используйте команду 'start'")
            return
        try:
            chats = self.bot.vk_sender.get_user_chats()
            if chats:
                print("\nДоступные беседы:")
                for chat in chats:
                    print(f"  ID: {chat['id']} - {chat['title']}")
                print(f"\nВсего бесед: {len(chats)}")
            else:
                print("Не удалось получить список бесед или бесед нет.")
        except Exception as e:
            print(f"Ошибка получения списка бесед: {e}")
    
    async def send_message(self, message: str):
        if not self.bot:
            print("Бот не запущен. Используйте команду 'start'")
            return
        try:
            result = await self.bot.send_broadcast(message)
            print(f"Результат: {result}")
        except Exception as e:
            print(f"Ошибка отправки сообщения: {e}")
    
    def add_channel(self, channel_id: str):
        if not self.bot:
            print("Бот не запущен. Используйте команду 'start'")
            return
        try:
            channel_id_int = int(channel_id)
            self.bot.add_vk_chat(channel_id_int)
        except ValueError:
            print("ID беседы должен быть числом.")
        except Exception as e:
            print(f"Ошибка добавления беседы: {e}")
    
    def remove_channel(self, channel_id: str):
        if not self.bot:
            print("Бот не запущен. Используйте команду 'start'")
            return
        try:
            channel_id_int = int(channel_id)
            self.bot.remove_vk_chat(channel_id_int)
        except ValueError:
            print("ID беседы должен быть числом.")
        except Exception as e:
            print(f"Ошибка удаления беседы: {e}")
    
    def list_channels(self):
        if not self.bot:
            print("Бот не запущен. Используйте команду 'start'")
            return
        status = self.bot.get_status()
        print("\nСписок бесед для рассылки:")
        if status['vk_chats']:
            print("  VK беседы:")
            for chat_id in status['vk_chats']:
                print(f"    - {chat_id}")
        else:
            print("  VK беседы: нет")
    
    async def run(self):
        self.print_banner()
        self.print_help()
        while True:
            try:
                command = input("\nВведите команду: ").strip()
                if not command:
                    continue
                parts = command.split(' ', 1)
                cmd = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""
                if cmd == "exit":
                    print("Выход.")
                    break
                elif cmd == "help":
                    self.print_help()
                elif cmd == "start":
                    await self.start_bot()
                elif cmd == "status":
                    self.show_status()
                elif cmd == "send":
                    if not args:
                        print("Укажите сообщение для отправки.")
                        continue
                    await self.send_message(args)
                elif cmd == "add_vk":
                    if not args:
                        print("Укажите ID беседы VK.")
                        continue
                    self.add_channel(args)
                elif cmd == "remove_vk":
                    if not args:
                        print("Укажите ID беседы VK.")
                        continue
                    self.remove_channel(args)
                elif cmd == "list":
                    self.list_channels()
                elif cmd == "chats":
                    self.show_available_chats()
                else:
                    print("Неизвестная команда. Используйте 'help' для справки.")
            except KeyboardInterrupt:
                print("\nВыход.")
                break
            except Exception as e:
                print(f"Ошибка: {e}")

async def main():
    cli = BroadcastBotCLI()
    await cli.run()

if __name__ == "__main__":
    asyncio.run(main()) 