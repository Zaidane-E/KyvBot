import discord, pytz, config
from datetime import datetime, timezone, timedelta
from varname import varname, nameof

client = discord.Client()

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))
	return

async def invalid(message):
	return

async def print_help(message):
	await message.channel.send('`Basic commands:\n\nprefix: .\nhelp : Help\ntimefrance : Local time in Paris, France\ntimecanada: Local time in Toronto, Canada\ntime : Local time\nschedule: Schedule`')

async def print_schedule(message):
	await message.channel.send(file=discord.File('schedule_zaidane.png'))
	
async def print_time(message):
	if message.author.id == 211840395141840897:
		tz = pytz.timezone('America/Toronto')
		time = datetime.now(tz).strftime('%A %d/%m/%Y\n%H:%M %p Toronto Time')
	else:
		tz = pytz.timezone('Europe/Paris')
		time = datetime.now(tz).strftime('%A %d/%m/%Y\n%H:%M %p Paris Time')	
	await message.channel.send(time)

async def print_timeParis(message):
	tz = pytz.timezone('Europe/Paris')
	time = datetime.now(tz).strftime('%A %d/%m/%Y\n%H:%M %p Paris Time')
	await message.channel.send(time)

async def print_timeToronto(message):
	tz = pytz.timezone('America/Toronto')
	time = datetime.now(tz, ).strftime('%A %d/%m/%Y\n%H:%M %p Toronto Time')
	await message.channel.send(time)

def getCurrentTime():
	"""
	docstring
	"""
	return datetime.now()

def addThirtyMinutes(t):
	thirtyMinutes = timedelta(minutes = 30)
	t += thirtyMinutes
	return t


GNG = ((1,2,3),(),(13,15,16,17,18),(4,5,6),(),(),())
CSI = ((),(4,5,6,10,11,12),(),(7,8,9),(),(),())
CEG = ((13,14,15,16,17,18),(),(),(),(),(),())
JPN = ((),(21,22,23),(),(20,21,22,23,24,25,26,27),(),(),())

schedule = [[None]*31,[None]*31,[None]*31,[None]*31,[None]*31,[None]*31,[None]*31]

courses = [GNG, CSI, CEG, JPN]

for course in courses:	
	for day in range(7):
		for period in range(len(course[day])):
			schedule[day][course[day][period]] = course


async def currentClass(message):
	currentDay = datetime.now().weekday()
	currentTime = getCurrentTime()
	t = currentTime.replace(hour=7, minute=30)
	blocks = [None]*31
	block = 0
	saved = 0
	nextClass = None
	for i in range(31):
		blocks[i] = addThirtyMinutes(t)
		t = addThirtyMinutes(t)
	
	for i in range(31):
		if blocks[i] <= currentTime < blocks[i+1]:
			block = i
			saved = i
			break
	
	while schedule[currentDay][saved] == None:
		saved += 1
	nextClass = blocks[saved]

	currentPeriod = schedule[currentDay][block]

	switcher = {
		GNG: 'GNG',
		CSI: 'CSI',
		CEG: 'CEG',
		JPN: 'JPN',
		None: 'no class',
	}
	currentClass = switcher.get(currentPeriod, 'Error')

	if schedule[currentDay][block] == None:
		await message.channel.send(config.bot['user'] + ' has ' + currentClass + ' right now. Their next class is at ' + nextClass.strftime('%A %d/%m/%Y %H:%M %p Toronto Time (%H:%M %p Paris Time)'))
	else:
		await message.channel.send(config.bot['user'] + ' has ' + currentClass + ' right now.')

#	currentDay = datetime.weekday()
#	time, t1, t2 = getCurrentTime()
#	m = 30
#	turn = 0
#	for i in range(8, 23):
#		if turn == 0:
#			t1 = getTodayTimeAt(t1, i, m)
#			t2 = getTodayTimeAt(t2, )
#			schedule.update(dict.fromkeys([]))
#			turn = 1
#		else:
#			t1 = getTodayTimeAt(t1, i)
#			turn = 0
#	

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	
	switcher = {
		'.invalid' : invalid
	}

	switcher.update(dict.fromkeys(['.help', '.h'], print_help))
	switcher.update(dict.fromkeys(['.time france', '.time f', '.timef', '.tf'], print_timeParis))
	switcher.update(dict.fromkeys(['.time canada', '.time c', '.timec', '.tt'], print_timeToronto))
	switcher.update(dict.fromkeys(['.time', '.t'], print_time))
	switcher.update(dict.fromkeys(['.schedule', '.s'], print_schedule))
	switcher.update(dict.fromkeys(['.current'], currentClass))
	
	if message.content in switcher:
		msg = message.content
	else:
		msg = '.invalid'

	func = switcher.get(msg, ".invalid")
	await func(message)

client.run(config.bot['token'])
