from operator import contains
from datetime import datetime, timedelta
from tbot import tbot_config
from bot import models
import os
from dotenv import load_dotenv
import telebot
from telebot import types



dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
	
	load_dotenv(dotenv_path)

bot = telebot.TeleBot(os.getenv('TOKEN'))

data:dict = {}
book_data:dict = {}
#-------------------------********------------------------------------#
#-------------------------COMMANDS------------------------------------#
#-------------------------********------------------------------------#
@bot.message_handler(commands=['start'])
def start(message):
	global data, book_data
	chat_id = message.json['from']['id']
	# if chat_id in data:
	# 	del_message(chat_id, data[chat_id][2])
	# if chat_id in book_data:
	# 	del_message(chat_id, book_data[chat_id][2])	
	check_reg(message)

@bot.message_handler(commands=['url'])
def get_all_booking(message):
	chat_id = message.json['from']['id']
	markup = types.InlineKeyboardMarkup()
	button = types.InlineKeyboardButton("Ссылка", url='http://mu.com.ru:8000')
	markup.add(button)
	bot.send_message(message.chat.id, "Посмотреть все бронирования", reply_markup=markup)


@bot.message_handler(commands=['delete'])
def delete(message):
	chat_id = message.json['from']['id']
	try:
		models.User.objects.get(bot_id = chat_id)
		markup = types.InlineKeyboardMarkup()
		btn_yes = types.InlineKeyboardButton('Да', callback_data = 'del-yes')
		btn_no = types.InlineKeyboardButton('Нет', callback_data = 'del-no')
		markup.add(btn_yes, btn_no)
		bot.send_message(message.chat.id, "Удалить данные о Вас?", reply_markup=markup)
	except models.User.DoesNotExist as e:
		print('delete', str(e))
		check_reg(message)

@bot.message_handler(commands=['self'])
def get_user_info(message):
	global book_data
	chat_id = message.json['from']['id']
	try:
		user = models.User.objects.get(bot_id=message.json['from']['id'])
		bot.send_message(message.json['from']['id'], f"Имя - {user.firstname}\nЛогин - {user.login}\nКампус - {user.campus.name}\n Роль - {user.role.name}"  )
	except models.User.DoesNotExist as e:
		print('SELF' ,e)
		bot.send_message(message.json['from']['id'], 'В системе нет данных о вас! Пожалуйста зарегистрируйтесь')

@bot.message_handler(commands=['my_booking'])
def get_user_booking(message):
	chat_id = message.json['from']['id']
	try:
		user = models.User.objects.get(bot_id=chat_id)
		count = len(models.Booking.objects.filter(user__bot_id=chat_id, end__gte=datetime.now()))
		print(f'count {count}')
		if count > 0:
			book_data[chat_id][2] = bot.send_message(chat_id, "Ваши бронирования", reply_markup=get_buttons(models.Booking, 'booking', 'id', booking=chat_id))
		else:
			book_data[chat_id][2] = bot.send_message(chat_id, "Нет бронирований")
	except (models.User.DoesNotExist, KeyError) as e:
		print('SELF' ,e)
		start(message)
		# bot.send_message(message.json['from']['id'], 'В системе нет данных о вас! Пожалуйста зарегистрируйтесь')


#-------------------------****************------------------------------------#
#-------------------------SHARE__FUNCTIONS------------------------------------#
#-------------------------****************------------------------------------#


def del_message(chat_id, *args):
	for message_id in args:
		if message_id:
			bot.delete_message(chat_id, message_id.json['message_id'])
			if chat_id in data:
				data[chat_id][2] = None


def get_buttons(model, key, *args, **kwargs):
	markup = types.InlineKeyboardMarkup()
	btns = []
	
	if 'req' in kwargs:
		keys = model.objects.filter(is_admin = False).values_list(*args)
	elif 'obj_types' in kwargs:
		markup = types.InlineKeyboardMarkup(row_width=2)
		user = models.User.objects.get(bot_id = kwargs['obj_types'])
		role_id = user.role.id
		user_campus = user.campus.id
		user_obj = models.Role.objects.get(id = role_id).school_objects.filter(object_campus_id=user_campus).values_list('object_type_id', 'object_type_id__name')
		keys = set(user_obj)
	elif 'type_id' in kwargs:
		# models.Role.objects.get(id = kwargs['type_id']).school_objects.all()
		# keys = models.Role.objects.get(id = kwargs['type_id']).school_objects.all().values_list(*args)
		user = models.User.objects.get(bot_id = kwargs['user_bot_id'])
		user_campus = user.campus.id
		role_id = user.role.id
		# models.Role.objects.get(id = role_id).school_objects.all().filter(object_type_id = kwargs['type_id'])
		markup = types.InlineKeyboardMarkup(row_width=1)
		keys = models.Role.objects.get(id = role_id).school_objects.filter(object_campus_id=user_campus).filter(object_type_id = kwargs['type_id']).values_list(*args)
	elif 'days' in kwargs:
		date_now = datetime.now().date()
		keys = []
		for i in range(30):
			keys.append([str(date_now) ,str(date_now)])
			date_now += timedelta(days=1)
	elif 'hours' in kwargs:
		time = models.Booking.objects.filter(school_object=kwargs['school_object'], start__date=kwargs['hours']).values_list('start__time')
		print(time)
		print(datetime.strptime(f'1:00:00', '%H:%M:%S').time())
		keys = []
		markup = types.InlineKeyboardMarkup(row_width=5)
		for i in range(24):
			if (datetime.strptime(f'{i}:00:00', '%H:%M:%S').time(),) not in time:
				keys.append([f'{i}:00:00', f'{i}:00'])
	elif 'booking' in kwargs:
		keys = []
		markup = types.InlineKeyboardMarkup(row_width=1)
		booking = model.objects.filter(user__bot_id=kwargs['booking'], end__gte=datetime.now())
		for i in booking:
			print(i)
			keys.append([i.id, str(i)])
	else:
		keys = model.objects.all().values_list(*args)
	for i in keys:
		btns.append(types.InlineKeyboardButton(i[1], callback_data = str(i[0])+'_' +key))
	markup.add(*btns)
	return markup


#-------------------------****************------------------------------------#
#-------------------------CALLBACK_BUTTONS------------------------------------#
#-------------------------****************------------------------------------#

@bot.callback_query_handler(func=lambda call: True) #вешаем обработчик событий на нажатие всех inline-кнопок
def callback_inline(call):
	print(call.data)
	spl = str(call.data).split('_')
	chat_id = call.from_user.id

	if chat_id in data:
		del_message(chat_id, data[chat_id][2])		
		if "campus" in spl:
			print(call.data)
			data[chat_id][0].campus = models.Campus.objects.get(pk = int(spl[0]))
			data[chat_id][2] = bot.send_message(chat_id, "Кто ты?", reply_markup=get_buttons(models.Role, 'roles', 'id', 'name', req='roles'))

		if "roles" in spl:
			print(call.data)
			data[chat_id][0].role = models.Role.objects.get(pk = int(spl[0]))
			markup = types.InlineKeyboardMarkup()
			btn_yes = types.InlineKeyboardButton('Да', callback_data = 'reg-yes')
			btn_no = types.InlineKeyboardButton('Нет', callback_data = 'reg-no')
			markup.add(btn_yes, btn_no)
			data[chat_id][2] = bot.send_message(chat_id, f'Твой логин - {str(data[chat_id][0].login)}\nТвое имя - {str(data[chat_id][0].firstname)}\nКампус -  {str(data[chat_id][0].campus)}\nТы - {str(data[chat_id][0].role)}\nВсе Верно?', reply_markup=markup)
			
		# print('1 ' + str(data[chat_id][0].login))
		# print('2 ' + str(data[chat_id][0].firstname))
		# print('3 ' + str(data[chat_id][0].campus))
		# print('4 ' + str(data[chat_id][0].role))

		if "reg-yes" in spl:
			#go to main menu
			data[chat_id][0].bot_id = chat_id
			data[chat_id][0].save()
			# bot.edit_message_reply_markup(call.message.chat.id, call.message.id, types.ReplyKeyboardRemove())
			del data[chat_id]
			bot.send_message(call.message.chat.id, 'Регистрация завершена')
		
		if "reg-no" in spl:
			del data[chat_id]



	if "del-yes" in spl:
		#go to main menu
		models.User.objects.get(bot_id = chat_id).delete()
		bot.edit_message_reply_markup(call.message.chat.id, call.message.id, types.ReplyKeyboardRemove())
		bot.send_message(call.message.chat.id, 'User deleted')

	if "del-no" in spl:
		bot.edit_message_reply_markup(call.message.chat.id, call.message.id, types.ReplyKeyboardRemove())
	

	if chat_id in book_data:
		del_message(chat_id, book_data[chat_id][2])
		if "types" in spl:
			print(int(spl[0]))
			
			
			book_data[chat_id][2] = bot.send_message(chat_id, 'Выберите объект', reply_markup=get_buttons(models.SchoolObject, 'objects', 'id', 'object_name', type_id = int(spl[0]), user_bot_id = chat_id))

		if "objects" in spl:
			print(int(spl[0]))
			book_data[chat_id][0].school_object_id = int(spl[0])
			book_data[chat_id][2] = bot.send_message(chat_id, 'Выберите дату', reply_markup=get_buttons(None, 'days', days = None))	
		
		if "days" in spl:
			book_data[chat_id][0].start = datetime.strptime(spl[0],'%Y-%m-%d')
			print(book_data[chat_id][0].start)
			book_data[chat_id][2] = bot.send_message(chat_id, 'Выберите время', reply_markup=get_buttons(None, 'hours', hours = book_data[chat_id][0].start, school_object=book_data[chat_id][0].school_object_id))

		if "hours" in spl:
			# print(type(book_data[chat_id][0].start.date))
			# print(datetime.strptime(spl[0], '%H:%M').time())
			book_data[chat_id][0].start = datetime.combine(book_data[chat_id][0].start.date(), datetime.strptime(spl[0], '%H:%M:%S').time())
			book_data[chat_id][0].end = book_data[chat_id][0].start + timedelta(hours=1)
			print(book_data[chat_id][0].start)
			markup = types.InlineKeyboardMarkup()
			btn_yes = types.InlineKeyboardButton('Да', callback_data = 'book-yes')
			btn_no = types.InlineKeyboardButton('Нет', callback_data = 'book-no')
			markup.add(btn_yes, btn_no)
			book_data[chat_id][2] = bot.send_message(chat_id, f'{book_data[chat_id][0].school_object}\n{book_data[chat_id][0].start}\n{book_data[chat_id][0].end}\n', reply_markup=markup)

		if "book-yes" in spl:
			#go to main menu
			book_data[chat_id][0].user = models.User.objects.get(bot_id=chat_id)
			book_data[chat_id][0].status = models.Status.objects.filter(name__contains='брон')[0]
			book_data[chat_id][0].save()
			# bot.edit_message_reply_markup(call.message.chat.id, call.message.id, types.ReplyKeyboardRemove())
			book_data[chat_id] = [models.Booking(), False, None]
			bot.send_message(call.message.chat.id, 'Бронирование завершено')
			
		if "book-no" in spl:
			del book_data[chat_id]

		if "booking" in spl:
			print('del?')
			markup = types.InlineKeyboardMarkup()
			btn_yes = types.InlineKeyboardButton('Да', callback_data = str(spl[0])+'_del-book-yes')
			btn_no = types.InlineKeyboardButton('Нет', callback_data = 'del-book-no')
			markup.add(btn_yes, btn_no)
			book_data[chat_id][2] = bot.send_message(chat_id, 'Удалить бронирование?', reply_markup=markup)
			# bot.edit_message_reply_markup(call.message.chat.id, call.message.id, types.ReplyKeyboardRemove())
		
		if "del-book-yes" in spl:
			models.Booking.objects.get(id = int(spl[0]), user__bot_id = chat_id).delete()
		


	

#-------------------------*****************------------------------------------#
#-------------------------TEXT_INSTRUCTIONS------------------------------------#
#-------------------------*****************------------------------------------#


@bot.message_handler(content_types='text')
def check_reg(message):
	global data
	print(message.json)
	
	chat_id = message.json['from']['id']
	try:
		models.User.objects.get(bot_id = chat_id)
		start_booking(message) # go to main menu
		return
	except models.User.DoesNotExist as e:
		print('EXEPTION', e)
		if chat_id not in data:
			data[chat_id] = [models.User(), False, 0]
			
	if data[chat_id][0].campus == None:
		del_message(chat_id, data[chat_id][2], message)
	else:
		del_message(chat_id, message)
	
	if data[chat_id][0].login == None:
		if data[chat_id][1] == False:
			data[chat_id][2] = bot.send_message(chat_id,'В системе нет данных о вас! Пожалуйста зарегистрируйтесь')
			data[chat_id][2] = bot.send_message(chat_id,'Введи логин интры или платформы')
			data[chat_id][1] = True
		else:
			data[chat_id][0].login = message.json['text']
			# print(data[chat_id][0].login)
			data[chat_id][1] = False
	if data[chat_id][0].firstname == None and data[chat_id][0].login != None:
		if data[chat_id][1] == False:
			data[chat_id][2] = bot.send_message(chat_id,'Введи имя')
			data[chat_id][1] = True
		else:
			data[chat_id][0].firstname = message.json['text']
			# print(data[chat_id][0].firstname)
			data[chat_id][1] = False
	if data[chat_id][0].campus == None and data[chat_id][0].firstname != None:
		if data[chat_id][1] == False:
			data[chat_id][2] = bot.send_message(chat_id, "Выбери кампус", reply_markup=get_buttons(models.Campus, 'campus', 'id', 'name'))
			data[chat_id][1] == True
		else:
			data[chat_id][1] = False


	# print('1 '+str(data[chat_id][0].login))
	# print('2 '+str(data[chat_id][0].firstname))
	# print('3 '+str(data[chat_id][0].campus))

#////////////////////////////////////////////////////////////////////////////////////////////////////

def start_booking(message):
	
	# ObjectType
	global book_data
	print(message.json)
	
	chat_id = message.json['from']['id']
	if chat_id not in book_data:
		book_data[chat_id] = [models.Booking(), False, None]

	book_data[chat_id][2] = bot.send_message(chat_id, 'Выберите типы объектов', reply_markup=get_buttons(models.ObjectType, 'types', 'id', 'name', obj_types = chat_id))
	
	return	



	# if book_data[chat_id][0].firstname == None and book_data[chat_id][0].login != None:
	# 	if book_data[chat_id][1] == False:
	# 		book_data[chat_id][2] = bot.send_message(chat_id,'Введи имя')
	# 		book_data[chat_id][1] = True
	# 	else:
	# 		book_data[chat_id][0].firstname = message.json['text']
	# 		# print(book_data[chat_id][0].firstname)
	# 		book_data[chat_id][1] = False
	# if book_data[chat_id][0].campus == None and book_data[chat_id][0].firstname != None:
	# 	if book_data[chat_id][1] == False:
	# 		book_data[chat_id][2] = bot.send_message(chat_id, "Выбери кампус", reply_markup=get_buttons(models.Campus, 'campus', 'id', 'name'))
	# 		book_data[chat_id][1] == True
	# 	else:
	# 		book_data[chat_id][1] = False

	# print('1 '+str(book_data[chat_id][0].login))
	# print('2 '+str(book_data[chat_id][0].firstname))
	# print('3 '+str(book_data[chat_id][0].campus))








bot.polling(none_stop=True, interval=0)
# print(models.User.objects.get(login = 'sdarr'))
