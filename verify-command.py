import disnake
from disnake import Button, ButtonStyle
from disnake.ext import commands
from disnake.utils import get
import asyncio

# ALSO YOU CAN USE / COMMANDS IT SO EASY, can swap @bot.command() -> @bot.slash_command()


intents = disnake.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", help_command=None, intents=intents, test_guilds=[" Your Guidlds ID "])
bot.remove_command('help')


@bot.event
async def on_ready():
    print('BOT CONNECTED')

    await bot.change_presence(status=disnake.Status.online, activity=disnake.Game('!help'))


@bot.event
async def on_member_join(member):
    role = disnake.utils.get(member.guild.roles,
                             id=
                             "#Guild ID")  # ID вашей роли
    await member.add_roles(role)


@bot.command()  # / you can use @bot.slash_command(name = " ", description = " ")
@commands.has_any_role("Your roles or ID roles")
async def verify(ctx,
                 member: disnake.Member):  # if you use @bot.slash_command replace ctx -> interaction and all methods interaction such as: 52) unverify_role = interaction.guild.get_role(unverify_role_id)
    channel_id = 1132286840901206138  # Замените на ID вашего канала
    channel = bot.get_channel(channel_id)
    embed = disnake.Embed(title="Выберите ваш пол", description="Нажмите на кнопку, чтобы выбрать свой пол.")
    male_button = disnake.ui.Button(style=disnake.ButtonStyle.primary, label="Мужчина", custom_id="male")
    female_button = disnake.ui.Button(style=disnake.ButtonStyle.primary, label="Женщина", custom_id="female")
    cancel_button = disnake.ui.Button(style=disnake.ButtonStyle.primary.red, label="Недопуск", custom_id="dodge")
    embed.set_footer(text="Кликните на кнопку, чтобы выбрать пол.")
    embed.set_thumbnail(url=bot.user.avatar.url)
    embed.set_author(name="diperoqq", icon_url=bot.user.avatar.url)
    message = await channel.send(embed=embed, components=[[male_button, female_button]])

    def check(interaction):
        return interaction.message.id == message.id

    async def handle_interaction(interaction):
        unverify_role_id = 1131991046419660931  # Замените на ID роли "unverify"
        unverify_role = ctx.guild.get_role(unverify_role_id)
        await member.remove_roles(unverify_role)

        if interaction.component.custom_id == "male":
            role_id = 1132283864123985940  # Замените на ID роли "Мужчина"
            role = ctx.guild.get_role(role_id)
            await member.add_roles(role)
            await interaction.response.send_message("Вы выбрали роль Мужчина.", ephemeral=True)
        elif interaction.component.custom_id == "female":
            role_id = 1132284015907446884  # Замените на ID роли "Женщина"
            role = ctx.guild.get_role(role_id)
            await member.add_roles(role)
            await interaction.response.send_message("Вы выбрали роль Женщина.", ephemeral=True)
        elif interaction.component.custom_id == "dodge":
            role_id = 1155227536188522681
            role = ctx.guild.get_role(role_id)
            await member.add_roles(role)
            await interaction.response.send_message("Вы выбрали недопуск", ephemeral=True)

        # Удаляем все кнопки после выбора роли
        await message.edit(components=[])

    try:
        interaction = await bot.wait_for("button_click", check=check, timeout=30)
        await asyncio.gather(handle_interaction(interaction))
    except disnake.NotFound:
        pass
    except disnake.TimeoutError:
        await message.edit(components=[])


@bot.command()
@commands.has_any_role("Your roles or ID roles")
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print('Бот присоединился')


# Отключение бота
@bot.command()
@commands.has_any_role("Your roles or ID roles")
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        voice = await channel.connect()
        print('Бот вышел')


bot.run('Your Token')
