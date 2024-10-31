import discord
from discord.ext import commands, tasks
#from discord.commands import Option
#from discord.ext import tasks
import os
import ast
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)
prev_message_ids = [1233700897759035403, 1233700899587620874]
mongoclient = MongoClient(os.getenv("URI"))
db = mongoclient["Omen"]
thanks_collection = db["Thanks"]


async def insert_returns(body):
	if isinstance(body[-1], ast.Expr):
		body[-1] = ast.Return(body[-1].value)
		ast.fix_missing_locations(body[-1])
	if isinstance(body[-1], ast.If):
		insert_returns(body[-1].body)
		insert_returns(body[-1].orelse)
	if isinstance(body[-1], ast.With):
		insert_returns(body[-1].body)
	if isinstance(body[-1], ast.AsyncWith):
		insert_returns(body[-1].body)


@client.event
async def on_ready():
    print("we have logged in as {0.user}".format(client))
    await client.change_presence(activity = discord.Game(name="Watching over omencord"))
    client.add_view(cpuroles())
    client.add_view(gpuroles())
    client.add_view(typeroles())
    sticky.start()

@client.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("This command is currently on cooldown.")
    else:
        raise error


roledic = {"Ryzen 5" : 951474373049606245, "Ryzen 7" : 951474289708765214, "Ryzen 9" : 951474453957738496, "Intel i5" : 951474497532354623, "Intel i7" : 951474535931183104, "Intel i9" : 951474585860210728}

class cpuroles(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(custom_id = "roleselect", placeholder='Pick your CPU', min_values=1, max_values=1, options=[
        discord.SelectOption(label='Ryzen 5', description='ex: 3550h/4600h/5600x', emoji='<:R5:940244878611329074>'),
        discord.SelectOption(label='Ryzen 7', description='ex: 3750h/3700x/4800h/5800h', emoji='<:R7:940244878691012629>'),
        discord.SelectOption(label='Ryzen 9', description='ex: 3950x/4900h/5900h/5980h', emoji='<:R9:940244878951063593>'),
        discord.SelectOption(label='Intel i5', description='ex: 8600k/9300h/10300h', emoji='<:i5:940244878581964800>'),
        discord.SelectOption(label='Intel i7', description='ex: 9750h/10700k/11375h', emoji='<:i7:940244878619713629>'),
        discord.SelectOption(label='Intel i9', description='ex: 10900/10950h/11950h', emoji='<:i9:940244879085301760>'),        
        discord.SelectOption(label='Clear roles', description='Remove any role you may have selected', emoji='❌')

    ])
    async def select_callback(self, select, interaction):
        if select.values[0] == "Clear roles":
            for roleid in roledic.values():
                role = discord.utils.get(interaction.guild.roles, id = roleid)
                if role in interaction.user.roles:
                    await interaction.user.remove_roles(role)
                    await interaction.response.send_message(f'Removed <@&{roleid}> from your roles.',ephemeral=True)
                    break
                else:
                    continue
                await interaction.response.send_message(f"You need to select a role first.",ephemeral=True)
        else:                
            for role in interaction.user.roles:
                if role.id in roledic.values():
                    await interaction.response.send_message(f'You can only choose 1 role of this type.', ephemeral=True)
                    return

            role = discord.utils.get(interaction.guild.roles, id = roledic[select.values[0]])
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f'Added <@&{roledic[select.values[0]]}> to your roles.', ephemeral=True)



gpuroledic = {"RTX 40XX": 1060192351110320270, "RTX 30XX" : 951494273658945566, "RTX 20XX" : 951494361256972308, "GTX 16XX" : 951494366592131223, "GTX 10XX" : 951494365392560149, "Radeon 6XXX" : 951494367640682556, "Radeon 5XXX" : 951494368601202778}



class gpuroles(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(custom_id = "gpuroleselect", placeholder='Pick your GPU', min_values=1, max_values=1, options=[
        discord.SelectOption(label = "RTX 40XX", description = 'ex:4060/4070/4090 (🤑)', emoji = '<:RTX:951493702784811018>'),
        discord.SelectOption(label='RTX 30XX', description='ex: 3060/3070ti/3080', emoji='<:RTX:951493702784811018>'),
        discord.SelectOption(label='RTX 20XX', description='ex: 2060/2070s/2080', emoji='<:RTX:951493702784811018>'),
        discord.SelectOption(label='GTX 16XX', description='ex: 1650/1660ti', emoji='<:GTX:951493807063584829>'),
        discord.SelectOption(label='GTX 10XX', description='ex: 1050/1070/1080ti', emoji='<:GTX:951493807063584829>'),
        discord.SelectOption(label='Radeon 6XXX', description='ex: 6600M/6900XT', emoji='<:amd:951467046535831562>'),
        discord.SelectOption(label='Radeon 5XXX', description='ex: 5600M/5700XT', emoji='<:amd:951467046535831562>'),        
        discord.SelectOption(label='Clear roles', description='Remove any role you may have selected', emoji='❌')

    ])
    async def select_callback(self, select, interaction):
        if select.values[0] == "Clear roles":
            for roleid in gpuroledic.values():
                role = discord.utils.get(interaction.guild.roles, id = roleid)
                if role in interaction.user.roles:
                    await interaction.user.remove_roles(role)
                    await interaction.response.send_message(f'Removed <@&{roleid}> from your roles.',ephemeral=True)
                    break
                else:
                    continue
                await interaction.response.send_message(f"You need to select a role first.",ephemeral=True)
        else:                
            for role in interaction.user.roles:
                if role.id in gpuroledic.values():
                    await interaction.response.send_message(f'You can only choose 1 role of this type.', ephemeral=True)
                    return

            role = discord.utils.get(interaction.guild.roles, id = gpuroledic[select.values[0]])
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f'Added <@&{gpuroledic[select.values[0]]}> to your roles.', ephemeral=True)



typeroledic = {"Omen laptop" : 800740416118325248, "Omen desktop" : 797059506730696727, "Victus laptop" : 951500157495672923, "Pavilion laptop" : 951500154207338539, "Pavilion desktop" : 951500155809591346}


class typeroles(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(custom_id = "typeroleselect", placeholder='Pick your device', min_values=1, max_values=1, options=[
        discord.SelectOption(label='Omen laptop', description= 'ie: Omen 15/Omen 16', emoji='<:omen:951499552702201866>'),
        discord.SelectOption(label='Omen desktop', description='Omen prebuilt desktops', emoji='<:omen:951499552702201866>'),
        discord.SelectOption(label='Victus laptop', description='ie: Victus 16', emoji='<:victus:951499691621761044>'),
        discord.SelectOption(label='Pavilion laptop', description='ie: Pavilion 15', emoji='<:pavilion:951501972324884561>'),
        discord.SelectOption(label='Pavilion desktop', description='Pavilion prebuilt desktops', emoji='<:pavilion:951501972324884561>'),
        discord.SelectOption(label='Clear roles', description='Remove any role you may have selected', emoji='❌')

    ])
    async def select_callback(self, select, interaction):
        if select.values[0] == "Clear roles":
            for roleid in typeroledic.values():
                role = discord.utils.get(interaction.guild.roles, id = roleid)
                if role in interaction.user.roles:
                    await interaction.user.remove_roles(role)
                    await interaction.response.send_message(f'Removed <@&{roleid}> from your roles.',ephemeral=True)
                    break
                else:
                    continue
                await interaction.response.send_message(f"You need to select a role first.",ephemeral=True)
        else:                
            for role in interaction.user.roles:
                if role.id in typeroledic.values():
                    await interaction.response.send_message(f'You can only choose 1 role of this type.', ephemeral=True)
                    return

            role = discord.utils.get(interaction.guild.roles, id = typeroledic[select.values[0]])
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f'Added <@&{typeroledic[select.values[0]]}> to your roles.', ephemeral=True)

@client.command(aliases= ['eval'])
async def _eval(ctx, * , cmd):
    try:
        if ctx.author.id not in [539122128893509673,602569683543130113,743672901680627764,617021192011776000]:
            return
        fn_name = "_eval_expr"
        cmd = cmd.strip("`py ")
        cmd = cmd.strip("` ")
        cmd = "\n".join(f"	{i}" for i in cmd.splitlines())
        body = f"async def {fn_name}():\n{cmd}"
        parsed = ast.parse(body)
        body = parsed.body[0].body	
        await insert_returns(body)
        env = {
            'client': ctx.bot,
            'commands': commands,
            'ctx': ctx,
            '__import__': __import__
        }
        try:
            exec(compile(parsed, filename="<ast>", mode="exec"), env)
            await eval(f"{fn_name}()", env)
            await ctx.message.add_reaction("✅")
        except Exception as e:
            await ctx.message.add_reaction("❌")
            return await ctx.send(f"```{e.__class__.__name__}: {e}```")
    except Exception as e2:
        await ctx.message.add_reaction("❌")
        return await ctx.send(f"```{e.__class__.__name__}: {e2}```")





@client.command()
async def setup(ctx):
    em = discord.Embed(title = "Select CPU roles", color = discord.Color(0xf5791f))
    em.set_image(url = "https://cdn.discordapp.com/attachments/936909342744141824/951488202550702080/unknown.png")
    view = cpuroles()
    await ctx.channel.send(embed = em, view = view)

@client.command()
async def setup2(ctx):
    em = discord.Embed(title = "Select GPU roles", color = discord.Color(0xf5791f))
    em.set_image(url = "https://cdn.discordapp.com/attachments/936909342744141824/951495090956795924/unknown.png")
    view = gpuroles()
    await ctx.channel.send(embed = em, view = view)

@client.command()
async def setup3(ctx):
    em = discord.Embed(title = "Select device roles", color = discord.Color(0xf5791f))
    em.set_image(url = "https://cdn.discordapp.com/attachments/936909342744141824/951501220441358437/unknown.png")
    view = typeroles()
    await ctx.channel.send(embed = em, view = view)



#Thank & Leaderboard

@client.slash_command(name="thank", guild_ids=[750760232954888363], description="Thank someone for helping you!")
@commands.cooldown(1, 30, commands.BucketType.user)
async def thank(ctx: discord.ApplicationContext, member: discord.Member):
    if member.id == ctx.author.id:
        await ctx.respond("Let's not give ourselves a pat on our own back.", ephemeral=True)
        return

    thanks_collection.update_one({"user_id": member.id}, {"$inc": {"thank_count": 1}}, upsert=True)
    await ctx.respond(f"{member.mention} has been thanked!")

@client.slash_command(name="leaderboard", guild_ids=[750760232954888363], description="View the most helpful people in the server.")
async def leaderboard(ctx: discord.ApplicationContext):
    top_users = thanks_collection.find().sort("thank_count", -1).limit(10)
    
    # Emojis for top 3 positions
    rank_emojis = ["🥇", "🥈", "🥉"]
    
    # Prepare embed
    embed = discord.Embed(title="Community Pillars 🏛️", description="", color=discord.Color.gold())
    
    leaderboard_lines = []

    for i, user in enumerate(top_users, start=1):
        user_id = user["user_id"]
        thank_count = user["thank_count"]
        member = ctx.guild.get_member(user_id)
        username = f"<@{user_id}>" if member else f"User {user_id}"
        
        rank_display = rank_emojis[i - 1] if i <= 3 else f"{i}."
        line = f"{rank_display} **{username}** - {thank_count} thanks"
        leaderboard_lines.append(line)

    # Check if the user is in the leaderboard and find their rank
    user_data = thanks_collection.find_one({"user_id": ctx.author.id})
    if user_data:
        user_rank = thanks_collection.count_documents({"thank_count": {"$gt": user_data["thank_count"]}}) + 1
        if user_rank > 10:
            # Add ellipsis and show user's rank if outside top 10
            leaderboard_lines.append("...\n")
            leaderboard_lines.append(f"**{user_rank}. <@{ctx.author.id}>** - {user_data['thank_count']} thanks")
        else:
            # Bold the user's position if in the top 10
            leaderboard_lines[user_rank] = f"**{leaderboard_lines[user_rank]}**"
    else:
        embed.set_footer(text="You haven't received any thanks yet.")

    # Set the description with the collected lines
    embed.description = "\n".join(leaderboard_lines)

    await ctx.respond(embed=embed)





#LOOPs

@tasks.loop(hours=1)
async def sticky():
    global prev_message_ids
    await client.wait_until_ready()
    
    ogh = client.get_channel(933772572565319751)
    desk = client.get_channel(1100791424187908229)    

    # Fetch messages in the channel
    ogh_messages = await ogh.history(limit=100).flatten()
    desk_messages = await desk.history(limit=100).flatten()

    # Check if the first message is a sticky by the bot
    ogh_sticky_exists = len(ogh_messages) > 0 and ogh_messages[0].author.id == 936903746145898536
    desk_sticky_exists = len(desk_messages) > 0 and desk_messages[0].author.id == 936903746145898536

    if not ogh_sticky_exists:
        embed = discord.Embed(title="This is a feedback channel 😄", description="This channel is for discussions with HP about any suggestions/feedback/bugs you might have with **OMEN Gaming Hub**.\n\nFor troubleshooting, please visit <#810839857940660236>.", color=0xf5791f)
        new_message1 = await ogh.send(embed=embed)
        if prev_message_ids:
            try:
                old_message = await ogh.fetch_message(prev_message_ids[0])
                await old_message.delete()
            except discord.NotFound:
                pass
            prev_message_ids[0] = new_message1.id
        else:
            prev_message_ids.append(new_message1.id)

    if not desk_sticky_exists:
        embed2 = discord.Embed(title="This is a feedback channel 😄", description="This channel is for discussions with HP about any suggestions/feedback/bugs you might have with **OMEN Desktops**.\n\nFor troubleshooting, please visit <#810839857940660236>.", color=0xf5791f)
        new_message2 = await desk.send(embed=embed2)
        if prev_message_ids:
            try:
                old_message = await desk.fetch_message(prev_message_ids[1])
                await old_message.delete()
            except discord.NotFound:
                pass
            prev_message_ids[1] = new_message2.id
        else:
            prev_message_ids.append(new_message2.id)



@client.command()
async def embed(ctx):
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel
    
    await ctx.send('Waiting for a channel')
    channel = await client.wait_for('message', check=check)
    channel = channel.content.strip("<#")
    channel = channel.strip(">")
    channel = int(channel)
    channel = client.get_channel(channel)
    await ctx.send("waiting for title")
    title = await client.wait_for('message', check=check)

    await ctx.send('Waiting for a description')
    desc = await client.wait_for('message', check=check)

    await ctx.send('waiting for thumbnail')
    thumb = await client.wait_for('message', check=check)

    if title.content and desc.content == "none":
        embed = discord.Embed(color=0xf5791f)
    elif title.content == "none":
        embed = discord.Embed(description = desc.content,color=0xf5791f)
    elif desc.content == "none":
        embed = discord.Embed(title = title.content,color=0xf5791f)
    else:
        embed = discord.Embed(title = title.content, description = desc.content,color=0xf5791f)



    await ctx.send('waiting for image')
    image = await client.wait_for('message', check=check)

    if thumb.content != "none":
        embed.set_thumbnail(url = thumb.content)

    if image.content != "none":
        embed.set_image(url = image.content)

    await channel.send(embed=embed)







client.run(os.getenv("token"))

