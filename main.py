import discord
from discord.ext import commands, tasks
#from discord.commands import Option
#from discord.ext import tasks
import os
import ast
from web import site
from replit import db


intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

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



gpuroledic = {"RTX 30XX" : 951494273658945566, "RTX 20XX" : 951494361256972308, "GTX 16XX" : 951494366592131223, "GTX 10XX" : 951494365392560149, "Radeon 6XXX" : 951494367640682556, "Radeon 5XXX" : 951494368601202778}



class gpuroles(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(custom_id = "gpuroleselect", placeholder='Pick your GPU', min_values=1, max_values=1, options=[
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
    if ctx.author.id not in [602569683543130113,743672901680627764,617021192011776000]:
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









site()
client.run(os.getenv("token"))
