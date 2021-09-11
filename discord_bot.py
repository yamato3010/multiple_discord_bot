import discord
from discord.embeds import Embed
from discord.flags import Intents
import env
import math
import datetime
import time
import mylist
import lang
from discord import reaction
from discord.utils import get

intents = discord.Intents.all()

# env.pyというファイルを作ってなかにtoken = "YOUR TOKEN"としてください
message_id = None
voteMax = 5
text = lang.ja

client = discord.Client(intents = intents)

# 以下投票コマンド selectはリストだ！！！
async def vote(message, select):

	global finalCount
	global reactionContent
	global voteMax

	finalCount = {}
	reactionContent = {}

	await message.delete(delay = 3)
	


	if len(select) > voteMax + 3:
		await message.channel.send(text["attention_choices"] % voteMax)
		return False


	emb = discord.Embed(title = select[1])
	vote_time = int(select[2])
	
	dt = datetime.datetime.now() # 投票時間をフッターに表示
	if vote_time < 60:
		dt1 = dt + datetime.timedelta(minutes=vote_time)
		dt1 = dt.replace(microsecond = 0)
		emb.set_footer(text = text["this_vote"] + str(dt1) + text["is_end"] + str(vote_time) + text["after_min"])

	elif vote_time >= 60:
		h = math.floor(vote_time / 60)
		m = vote_time % 60
		dt1 = dt + datetime.timedelta(hours=h, minutes=m)
		dt1 = dt.replace(microsecond = 0)
		emb.set_footer(text = text["this_vote"] + str(dt1) + text["is_end"] + str(h) + text["after_hr"] + str(m) + text["after_min"])

	for i in range(3):

		select.pop(0) # リストの先頭を3回削除

	for i, item in enumerate(select):
		emb.add_field(name=str(i + 1) , value=item)

	vote_message = await message.channel.send(embed=emb) # embメッセージ送信

	global message_id
	message_id = vote_message.id
	
	# もし選択肢が一つ以下だったらyes or no ここから
	if len(select) <= 1:
		for i in range(2):
			await vote_message.add_reaction(mylist.yon[i])
		time.sleep(vote_time) # 一時停止
		await vote_message.delete()
		print("投票タイム終了") # 終了
		return await vote_result_yon(message)
	# ここまで

	for i ,item in enumerate(select):
		await vote_message.add_reaction(mylist.count[i])
	
	time.sleep(vote_time) # 一時停止
	await vote_message.delete()
	print("投票タイム終了") # 終了
	return await vote_result(message)
	

async def vote_result(message):
	select = message.content.split()
	title = select[1]
	emb = discord.Embed(title = text["result"] + str(title))
	for i in finalCount:
		emb.add_field(name = select[i + 3] , value = int(finalCount[i]) - 1)
	
	await message.channel.send(embed = emb)

async def vote_result_yon(message): # 選択肢が一つ股はない時の結果表示
	select = message.content.split()
	title = select[1]
	txt = [text["agree"], text["disagree"]]
	
	if len(select) == 4: # もし選択肢が一つあったら
		subTitle = select[3]
		emb = discord.Embed(title = text["result"] + str(title), description=str(subTitle))

	else:
		emb = discord.Embed(title = text["result"] + str(title))

	for i in finalCount_yor:
		emb.add_field(name = txt[i] , value = int(finalCount_yor[i]) - 1)
	
	await message.channel.send(embed = emb)


async def whichVote(message):

	global reactionContent

	emb = discord.Embed(title = text["vote_to"])
	for user in reactionContent.keys():

		reactionContent[user] = list(set(reactionContent[user]))

		emb.add_field(name = user, value = sorted(reactionContent[user], key= lambda i: mylist.countOrder.get(i, float("inf"))))


	await message.channel.send(embed = emb)


emojiCount = {}
finalCount = {}
emojiCount_yon = {}
finalCount_yor = {}

for i, countEmoji in enumerate(mylist.count):

	emojiCount[i] = countEmoji
	
for i, countEmoji_yon in enumerate(mylist.yon):

	emojiCount_yon[i] = countEmoji_yon

reactionContent = {}




@client.event
async def on_reaction_add(reaction, user):
	global message_id
	global emojiCount
	global emojiCount_yon
	global finalCount
	global finalCount_yor
	global reactionContent

	if reaction.message.id == message_id:

		if reaction.emoji == "✅" or reaction.emoji == "❎": # 選択肢が一つの時の場合
			
			for i in emojiCount_yon:

				if reaction.emoji == emojiCount_yon[i]:

					finalCount_yor[i] = reaction.count
					
					if not user.bot:

						reactionContent.setdefault(user.name, []).append(reaction.emoji)


		for i in emojiCount:

			if reaction.emoji == emojiCount[i]:

				finalCount[i] = reaction.count
				
				if not user.bot:

					reactionContent.setdefault(user.name, []).append(reaction.emoji)




@client.event
async def on_reaction_remove(reaction, user):
	if reaction.message.id == message_id:

		if not user.bot:

			for i in emojiCount:

				if reaction.emoji == emojiCount[i]:

					finalCount[i] = reaction.count
					print(finalCount)
					
					reactionContent[user.name].remove(reaction.emoji)
			
			
		


@client.event
async def on_ready():
	
	print("ログインしました。")
	

@client.event
async def on_message(message):
	global reactionContent
	global text

	if message.author.bot:
		return

	command = mylist.command

	if message.content.split()[0] == command[0] or message.content.split()[0] == command[1]:
		l = message.content.split()
		vote_error = await vote(message, l)
		if vote_error == False:
			return
		await whichVote(message)
	
	if message.content.startswith(command[2]):
		vmax = message.content.split()[1]
		if not str.isdecimal(vmax):
			await message.channel.send(text["attention_int"] % vmax)
			return

		if int(vmax) > 11:
			await message.channel.send(text["attention_max"])
			return

		global voteMax

		l = message.content.split()

		voteMax = int(l[1])
		await message.channel.send(text["change_max"] % voteMax)


	if message.content.startswith(command[3]):

		await whichVote(message)
	
	if message.content.startswith(command[4]):
		language = message.content.split()[1]

		if language == "ja":
			text = lang.ja
			await message.channel.send(text["change_lang"] % language)
		elif language == "en":
			text = lang.en
			await message.channel.send(text["change_lang"] % language)
		else:
			await message.channel.send(text["error_lang"])

		
client.run(env.token)