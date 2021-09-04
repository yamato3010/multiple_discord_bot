import discord

token = 'Nzg3Mjc1MzgwOTUxNzQ0NTIy.X9SlVQ.rqaB42Z-W1Xwe1dc4TDAMHVS8lM'

client = discord.Client()

# 以下投票コマンド selectはリストだ！！！
async def vote(message, title, select):
	emoji_list = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣"]
	if len(select) > 5:
		await message.channel.send("選択肢は5以下にしてください！")
	emb = discord.Embed(title = title)
	for i in select:
		emb.add_field(name=str(len(i)) , value=i)

	print(emb)
	await message.channel.send(embed=emb)
	

@client.event
async def on_ready():
	
	print("ログインしました。")
	

@client.event
async def on_message(message):
	sentakusi = ["1","2","3","4"]
	if message.author.bot:
		return
		
	if message.content == "/neko":
		await message.channel.send("にゃーん")

	if message.content == "/test":
		await vote(message,"テスト", sentakusi)
		
		
client.run(token)