import nltk 
import json 
import random 
from telegram import Update 
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler 

BOT_KEY = "5339469291:AAEla00dWBHjD9rGuDxH4Vu4uABMeUKiKFc" 

config_file = open("/content/pizz2.json","r") 
BOT_CONFIG = json.load(config_file) 


def filter(text): 
  text = text.lower() 
  alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя -" 
  result = [c for c in text if c in alphabet] 
  return ''.join(result) 

def match(text, example): 
  text =filter(text) 
  example = example.lower() 
  distance = nltk.edit_distance(text, example)/len(example) 
  return distance < 0.4 

def get_intent(text): 
  for intent in BOT_CONFIG["intents"]: 
   for example in BOT_CONFIG["intents"][intent]["examples"]: 
    if match(text,example): 
      return intent 


def get_example(text): 
  for intent in BOT_CONFIG["intents"]: 
   for example in BOT_CONFIG["intents"][intent]["examples"]: 
    if match(text,example): 
      return example 


def bot(text): 
  intent = get_intent(text) 
  if intent: 
    return random.choice(BOT_CONFIG["intents"][intent]["responses"]) 

def start(update: Update, context): 
  global name 
  update.message.reply_text("Как вас зовут?") 
  return 1 


def vid(update: Update, context): 
  name=update.message.text 
  update.message.reply_text(f"Здравствуйте, {name}! Какую пиццу вы хотите? 'Сырная', 'Диабло', 'Песто' ,'Гавайская' , 'Овощи и грибы'")                    
  return 2   
 
def size(update: Update, context): 
  update.message.reply_text(f" Большую, среднюю или маленькую?") 
  return 3 
def pay(update: Update, context): 
  global siz 
  question_size=update.message.text 
  siz = get_example(question_size) 
  update.message.reply_text("Как вы будете платить?") 
  return 4 
def street(update: Update, context): 
  global pa 
  question_pay = update.message.text 
  pa = bot(question_pay) 
  update.message.reply_text("Какой у вас адрес доставки?") 
  return 5
def correction(update: Update, context): 
  question_street = update.message.text 
  update.message.reply_text(f"Вы хотите {siz} пиццу, Способ оплаты – {pa}, доставить по адресу: {question_street}?") 
  return 6
def finish(update: Update, context): 
  question_correction = update.message.text 
  correct = bot(question_correction) 
  update.message.reply_text(correct) 
  return 6 
def stop(bot, update): 
  update.message.reply_text("До свидания! Жаль что вы не хотите пиццы :(") 
  return ConversationHandler.END 


conv_handler = ConversationHandler( 
entry_points=[CommandHandler('start', start)], 
states={ 
2: [MessageHandler(Filters.text, size, pass_user_data=True)], 
3: [MessageHandler(Filters.text, pay, pass_user_data=True)], 
4: [MessageHandler(Filters.text, street, pass_user_data=True)], 
5: [MessageHandler(Filters.text, correction, pass_user_data=True)], 
6: [MessageHandler(Filters.text, finish, pass_user_data=True)], 
1: [MessageHandler(Filters.text, vid, pass_user_data=True)] 
}, 
fallbacks=[CommandHandler('stop', stop)] 
) 

upd = Updater(BOT_KEY) 
upd.dispatcher.add_handler(conv_handler) 
upd.dispatcher.add_handler(CommandHandler('start', start)) 
upd.dispatcher.add_handler(CommandHandler('stop', stop)) 
upd.start_polling() 
upd.idle()
