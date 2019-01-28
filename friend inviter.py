###Creator: Keo Tom-Shaw
###Date: 25/01/2019
###Version: 1.0
###License: MIT
###
###This is a Discord bot made for the purpose of easily inviting certain friends to play games
###
###Future features: -Don't notify users in the same call as the inviter

import discord
import asyncio

client = discord.Client()

def get_bot_token():
	line = None
	try:
		bot_file = open("bot.txt", 'r')
		line = bot_file.readline() #should only be one line
	except(Exception):
		print("Problem reading bot token")
	finally:
		bot_file.close()
		
	return line.replace('\n','')

def populate_games():
	game_names = {}
	
	try:
		game_file = open("commands.txt", 'r')
		lines = game_file.readlines()
		
		for line in lines:
			parsed = line.split(',')
			game_names[ parsed[0].replace('\n','') ] = parsed[1].replace('\n','')
		
	except(Exception):
		print("Problem reading commands.txt")
	finally:
		game_file.close()
	
	return game_names
	
def populate_friends():
	friend_list = {}
	
	try:
		friend_file = open("friends.txt", 'r')
		read_lines = friend_file.readlines()
		
		for line in read_lines:
			parsed = line.split(',')
			games = []
			for i in range(1,len(parsed)):
				games.append( parsed[i].replace('\n','') )
			
			friend_list[ parsed[0].replace('\n','') ] = games
		
	except(Exception):
		print("Problem reading friends info")
	finally:
		friend_file.close()
	
	return friend_list
	
def get_owner():
	lines = []
	try:
		owner_file = open("owner.txt", 'r')
		read_lines = owner_file.readlines()
		
		for line in read_lines:
			lines.append( line.replace('\n','') )
		
	except(Exception):
		print("Problem reading owner name")
	finally:
		owner_file.close()
		
	return lines
	
def get_server_name():
	line = None
	try:
		server_file = open("server.txt", 'r')
		line = server_file.readline() #should only be one line
	except(Exception):
		print("Problem reading server name")
	finally:
		server_file.close()
		
	return line.replace('\n','')
	
async def game_invite(message):
	for friend in friends:
		#Only send message if user plays that game, is online, and is not in the same voice channel as the sender (unless they're deafened)
		if message.content in friend_ids[friend.id] and not friend.status == discord.Status.offline and (friend.voice.voice_channel != message.author.voice.voice_channel or friend.voice.voice_channel == None or friend.voice.self_deaf or friend.voice.deaf):
			await client.send_message(friend, "Your friends would like to know if you're willing to play %s" % game_list[message.content])

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	print("fetching user list")
	for server in client.servers:
		if server.id == server_name:
			main_server = server
	if main_server != None:
		for member in main_server.members:
			key = member.id
			if key in friend_ids:
				friends.append(member)
			if key in owner_id:
				owner.append(member)
	print("list succesfully fetched\n------")

@client.event
async def on_message(message):
	key = message.content
	#potential data race due to async?
	if key in command_switch and message.author.id in owner_id:
		await switch[message.content](message)
	if key in game_list and message.author.id in owner_id:
		await game_invite(message)
	if message.channel.is_private and not message.author.bot:
		await client.send_message(owner[0], "%s said: %s" % (message.author.name, message.content))

game_list = populate_games() #List of commands for games, and their names, in commands.txt
command_switch = {} #hard-coded commands

server_name = get_server_name() #ID of the server to be checked, specified in server.txt. string
main_server = None #server object

friend_ids = populate_friends() #friends specified in friends.txt. In the format: ID(numeric): [game commands, e.g. +rs2]. Can have all or no commands, or anywhere in between strings
friends = [] #objects
owner_id = get_owner() #owner(s) specified in owner.txt. Only the ID is needed (can have multiple on new lines). strings
owner = [] #user objects

bot_token = get_bot_token() #Token for the bot (find on Discord's bot website)

client.run(bot_token)