import telebot
import os
from dotenv import load_dotenv 

load_dotenv()
# Definir o token do seu bot do Telegram
CHAT_ID = os.getenv("CHAT_ID")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Criar uma instância do bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Função para enviar mensagem com imagem
def enviar_mensagem_com_imagem(mensagem, imagem_url):
    try:
        # Enviar a imagem com a mensagem como legenda
        bot.send_photo(chat_id=CHAT_ID, photo=imagem_url, caption=mensagem)
    except Exception as e:
        print(f"Erro ao enviar mensagem com imagem para o Telegram: {e}")

