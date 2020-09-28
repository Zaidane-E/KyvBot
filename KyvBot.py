import discord
import pytz
import config as cfg
from datetime import datetime, timezone, timedelta

client = discord.Client()

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))
	return

async def invalid(message):
	return

async def print_help(message):
	await message.channel.send('Commands:\n.help : helps...?\ntimefrance : time in france\ntimecanada: time in canada\ntime : time wherever u are\nschedule: stalk schedule')

async def print_schedule(message):
	await message.channel.send(file=discord.File('schedule_zaidane.png'))
	
async def print_time(message):
	if message.author.id == 211840395141840897:
		tz = pytz.timezone('America/Toronto')
		time = datetime.now(tz, ).strftime('%A %d/%m/%Y\n%H:%M %p Toronto Time')
	else:
		tz = pytz.timezone('Europe/Paris')
		time = datetime.now(tz, ).strftime('%A %d/%m/%Y\n%H:%M %p Paris Time')	
	await message.channel.send(time)

async def print_timeParis(message):
	tz = pytz.timezone('Europe/Paris')
	time = datetime.now(tz, ).strftime('%A %d/%m/%Y\n%H:%M %p Paris Time')
	await message.channel.send(time)

async def print_timeToronto(message):
	tz = pytz.timezone('America/Toronto')
	time = datetime.now(tz, ).strftime('%A %d/%m/%Y\n%H:%M %p Toronto Time')
	await message.channel.send(time)

#async def class(message):

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	
	switcher = {
		'.help' : print_help,
		'.timefrance' : print_timeParis,
		'.timecanada' : print_timeToronto,
		'.time' : print_time,
		'.schedule': print_schedule,
		'.invalid' : invalid
	}
	
	if message.content in switcher:
		msg = message.content
	else:
		msg = '.invalid'

	func = switcher.get(msg, ".invalid")
	await func(message)

client.login(cfg.token)
