import discord
from discord.ext import commands
import asyncio

bot = commands.Bot(command_prefix="$")

@bot.event
async def on_ready():
    await bot.get_channel(954723835679244418).send("Le bot est en ligne")
    print("Bot main online")

@commands.has_role('bot_mod')
@bot.command(name="clear")
async def delete(ctx, number: int):
    messages = await ctx.channel.history(limit=number + 1).flatten()

    for each_message in messages:
        await each_message.delete()


async def createMutedRole(ctx):
    mutedRole = await ctx.guild.create_role(name="Muted",
                                            permissions=discord.Permissions(
                                                send_messages=False,
                                                speak=False),
                                            reason="Creation du role Muted pour mute des gens.")
    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedRole, send_messages=False, speak=False)
    return mutedRole


async def getMutedRole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Muted":
            return role

    return await createMutedRole(ctx)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Mmmmmmh, j'ai bien l'impression que cette commande n'existe pas.")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Il manque un argument.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Vous n'avez pas les permissions pour faire cette commande.")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("Oups vous ne pouvez pas utilisez cette commande.")
    if isinstance(error.original, discord.Forbidden):
        await ctx.send("Oups, je n'ai pas les permissions nécéssaires pour faire cette commmande")

@commands.has_role('bot_mod')
@bot.command()
async def mute(ctx, member: discord.Member, *, reason="Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.add_roles(mutedRole, reason=reason)
    await ctx.send(f"{member.mention} a été mute pour la raison suivante : {reason}")

@commands.has_role('bot_mod')
@bot.command()
async def unmute(ctx, member: discord.Member, *, reason="Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.remove_roles(mutedRole, reason=reason)
    await ctx.send(f"{member.mention} a été unmute !")

@commands.has_role('bot_mod')
@bot.command()
async def ban(ctx, user : discord.User, *, reason="Aucune raison n'a été renseigné"):
    await ctx.guild.ban(user, reason=reason)
    em = discord.Embed(description=f"{user.mention} a été **banni** pour *{reason}* par {ctx.author} !", color=0x000000)
    em.set_thumbnail(url=user.avatar_url)

    await ctx.send(embed=em)

@commands.has_role('bot_mod')
@bot.command()
async def kick(ctx, user : discord.User, *, reason="Aucune raison n'a été renseigné"):
    await ctx.guild.kick(user, reason = reason)
    em = discord.Embed(description=f"{user.mention} a été **kick** pour *{reason}* par {ctx.author} !", color=0x000000)
    em.set_thumbnail(url=user.avatar_url)

    await ctx.send(embed=em)

bot.run("OTUxNTE0NTAyMTQ5NTk5MjYy.Yiok7w.Atebcr0QzX8bdM18WHeAVoP-nhw")