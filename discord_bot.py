import discord
from discord.embeds import Embed
import env
import math
import datetime
import time
import mylist
from discord import reaction
from discord.utils import get

# env.pyというファイルを作ってなかにtoken = "YOUR TOKEN"としてください
message_id = None

voteMax = 5

client = discord.Client()

# 以下投票コマンド selectはリストだ！！！
async def vote(message, select):

	global finalCount
	global voteMax
	await message.delete(delay = 3)
	


	if len(select) > voteMax + 3:
		await message.channel.send("選択肢は%s以下にしてください！" % voteMax)
		return
	
	emb = discord.Embed(title = select[1])
	vote_time = int(select[2])
	
	dt = datetime.datetime.now() # 投票時間をフッターに表示
	if vote_time < 60:
		dt1 = dt + datetime.timedelta(minutes=vote_time)
		dt1 = dt.replace(microsecond = 0)
		emb.set_footer(text = "この投票は" + str(dt1) + "に終了します(" + str(vote_time) + "分後)")

	elif vote_time >= 60:
		h = math.floor(vote_time / 60)
		m = vote_time % 60
		dt1 = dt + datetime.timedelta(hours=h, minutes=m)
		dt1 = dt.replace(microsecond = 0)
		emb.set_footer(text = "この投票は" + str(dt1) + "に終了します(" + str(h) + "時間" + str(m) + "分後)")

	for i in range(3):

		select.pop(0) # リストの先頭を3回削除

	for i, item in enumerate(select):
		emb.add_field(name=str(i + 1) , value=item)

	vote_message = await message.channel.send(embed=emb) # embメッセージ送信

	global message_id
	message_id = vote_message.id
	
	for i ,item in enumerate(select):
		await vote_message.add_reaction(mylist.count[i])
	
	time.sleep(vote_time) # 一時停止
	await vote_message.delete()
	print("投票タイム終了") # 終了
	return await vote_result(message)
	

async def vote_result(message):
	select = message.content.split()
	title = select[1]
	emb = discord.Embed(title = "投票結果:" + str(title))
	
	for i in finalCount:
		emb.add_field(name = select[i + 3] , value = int(finalCount[i]) - 1)
	
	await message.channel.send(embed = emb)




emojiCount = {}
finalCount = {}

for i, countEmoji in enumerate(mylist.count):
	emojiCount[i] = countEmoji
	

reactionContent = {}




@client.event
async def on_reaction_add(reaction, user):
	global message_id
	global emojiCount
	global finalCount
	global reactionContent
	if reaction.message.id == message_id:
		for i in emojiCount:
			if reaction.emoji == emojiCount[i]:
				finalCount[i] = reaction.count
				if not user.bot:
					reactionContent.setdefault(user.name, []).append(reaction.emoji)

			
		


@client.event
async def on_ready():
	
	print("ログインしました。")
	

@client.event
async def on_message(message):

	global reactionContent

	if message.author.bot:
		return

	command = mylist.command

	if message.content.startswith(command[0]) or message.content.startswith(command[1]) and not message.content.startswith(command[2]) and not message.content.startswith(command[3]):
		l = message.content.split()
		await vote(message, l)
	
	if message.content.startswith(command[2]):
		vmax = message.content.split()[1]
		if not str.isdecimal(vmax):
			await message.channel.send("%sは数字ではありません\n10以下の自然数を入力してください！" % vmax)
			return

		if int(vmax) > 11:
			await message.channel.send("投票最大値は10以下にしてくださいｗ")
			return

		global voteMax

		l = message.content.split()

		voteMax = int(l[1])
		await message.channel.send("投票最大数を%sに変更しました" % voteMax)


	if message.content.startswith(command[3]):

		emb = discord.Embed(title = "前回の投票先")
		for user in reactionContent.keys():
				emb.add_field(name = user, value = reactionContent[user])
		await message.channel.send(embed = emb)






		
		
client.run(env.token)