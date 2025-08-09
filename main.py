import discord
from discord.ext import commands
from discord import Interaction, app_commands
import random
from discord.ext import commands
from discord import app_commands
import json
import os

class Client(commands.Bot):
    async def on_ready(self):
        print(f'{self.user} logged in successfully')

        try:
            guild = discord.Object(id=1398401093809213504)
            synced = await self.tree.sync()
            print(f'Synced {len(synced)} command to guild {guild.id}')

        except Exception as e:
            print(f'error with syncing commands: {e}')



    async def on_message(self, message):
        if message.author == self.user:
            return
        
        
        
    #async def on_reaction_add(self, reaction, user):
        #await reaction.message.channel.send('you reacted')



intents = discord.Intents.default()
intents.message_content = True
intents.members = True  
client = Client(command_prefix="!", intents=intents)




GUILD_ID = discord.Object(id=1398401093809213504)


#SLASH NO INPUT
@client.tree.command(name="hello", description="Ill say hello!", guild=GUILD_ID)
async def sayhello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello!")


#SLASH WITH INPUT
@client.tree.command(name="printer", description="I will say whatever you tell me!", guild=GUILD_ID)
async def printer(interaction: discord.Interaction, printer: str):
    await interaction.response.send_message(printer)

#EMBED
@client.tree.command(name="cute-doggy", description="This is a rickroll", guild=GUILD_ID)
async def printer(interaction: discord.Interaction):
    embed = discord.Embed(title="Cute Dog", url="https://www.youtube.com/watch?v=j5a0jTc9S10", description="Just a very cute dog", color=discord.Color.blue())
    embed.set_thumbnail(url="https://www.pawlovetreats.com/cdn/shop/articles/pembroke-welsh-corgi-puppy_600x.jpg?v=1628638716")
    embed.add_field(name="Info", value="Awww", inline=True)
    embed.add_field(name="More Info", value="So cute")
    embed.set_footer(text="Dog")
    embed.set_author(name=interaction.user.name, url="", icon_url="")
    await interaction.response.send_message(embed=embed)


#BUTTON (you can make more than one in each view but must change label and diffrent think before button https://www.youtube.com/watch?v=RCPPqPdlvE8)
#class View(discord.ui.View):
#    @discord.ui.button(label="hehehe", style=discord.ButtonStyle.blurple, emoji="💀")
#    async def button_callback(self, button, interaction):
#       await button.response.send_message("Button clicked!")


#@client.tree.command(name="button", description="displays a button", guild=GUILD_ID)
#async def myButton(interaction: discord.Interaction):
#    await interaction.response.send_message(view=View())


#Gives a role to a member
@client.tree.command(name="give_role", description="Type the role you would like to give and to which user", guild=GUILD_ID)
async def assign_role(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    try:
        await member.add_roles(role)
        await interaction.response.send_message(f'Successfully assigned {role.name} to {member.name}')
    except discord.Forbidden:
        await interaction.response.send_message("I don't have the necessary permissions to assign roles.")
    except discord.HTTPException:
        await interaction.response.send_message('An error occurred while assigning the role. Please try again later.')

@client.tree.command(name="remove_role", description="Type the role you would like remove from a user and which user you would like to remove it from", guild=GUILD_ID)
async def assign_role(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    try:
        await member.remove_roles(role)
        await interaction.response.send_message(f'Successfully removed {role.name} to {member.name}')
    except discord.Forbidden:
        await interaction.response.send_message("I don't have the necessary permissions to assign roles.")
    except discord.HTTPException:
        await interaction.response.send_message('An error occurred while assigning the role. Please try again later.')



@client.tree.command(name="ban_user", description="Select the user you would like to ban and the reason", guild=GUILD_ID)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = ""):
    try:
        await member.ban(reason=reason)
        await interaction.response.send_message(f'Successfully banned {member.name} for: {reason}')
    except discord.Forbidden:
        await interaction.response.send_message("I don't have the necessary permissions to ban users.")
    except discord.HTTPException:
        await interaction.response.send_message('An error occurred while banning the user. Please try again later.')


@client.tree.command(name="unban_user", description="Unban a user by their user ID and provide a reason", guild=GUILD_ID)
async def unban_user(interaction: discord.Interaction, user: discord.User, reason: str = ""):
    try:
        await interaction.guild.unban(user, reason=reason)
        await interaction.response.send_message(f'Successfully unbanned {user.name} for: {reason}')
    except discord.Forbidden:
        await interaction.response.send_message("I don't have the necessary permissions to unban users.")
    except discord.HTTPException:
        await interaction.response.send_message('An error occurred while unbanning the user. Please try again later.')


banned_words = set()

@client.tree.command(name="ban-words", description="Add a word to the banned words list", guild=GUILD_ID)
async def ban_words(interaction: discord.Interaction, word: str):
    banned_words.add(word.lower())
    await interaction.response.send_message(f'Added "{word}" to the banned words list.')

@client.tree.command(name="unban-words", description="Remove a word from the banned words list", guild=GUILD_ID)
async def unban_words(interaction: discord.Interaction, word: str):
    if word.lower() in banned_words:
        banned_words.remove(word.lower())
        await interaction.response.send_message(f'Removed "{word}" from the banned words list.')
    else:
        await interaction.response.send_message(f'"{word}" is not in the banned words list.')

@client.tree.command(name="list-banned-words", description="List all banned words", guild=GUILD_ID)
async def list_banned_words(interaction: discord.Interaction):
    if banned_words:
        await interaction.response.send_message("Banned words: " + ", ".join(banned_words))
    else:
        await interaction.response.send_message("No banned words set.")

# Check messages for banned words
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.lower() == 'hello kyro':
            await message.channel.send(f'Hi {message.author}')

    if any(word in message.content.lower() for word in banned_words):
        await message.delete()
        await message.channel.send(f"{message.author.mention}, your message contained a banned word.", delete_after=5)
        return
    await client.process_commands(message)



@client.tree.command(name="dice-roll", description="Rolls a Dice", guild=GUILD_ID)
async def roll_dice(interaction: discord.Interaction):
    roll=random.randint(1, 6)
    await interaction.response.send_message(f"{roll} was rolled")



@client.tree.command(name="coin-flip", description="Flip a coin", guild=GUILD_ID)
async def flip_coin(interaction: discord.Interaction):
    heads="Heads"
    tails="Tails"
    sides = [heads, tails]
    pick_side= random.choice(sides)
    await interaction.response.send_message(f"{pick_side}")


@client.tree.command(name="ultimate_timeout", description="They can't chat or join voice channels for 28 days", guild=GUILD_ID)
async def ultimate_timeout(interaction: discord.Interaction, member: discord.Member, reason: str = ""):
    from datetime import datetime, timedelta, timezone
    try:
        max_duration = 40320  
        duration = max_duration
        until = datetime.now(timezone.utc) + timedelta(minutes=duration)
        await member.timeout(until, reason=reason)
        if reason == "":
            await interaction.response.send_message(f'Successfully sent {member.name} to timeout for {duration} minutes (28 days). Reason: No reason given')
        else:
            await interaction.response.send_message(f'Successfully sent {member.name} to timeout for {duration} minutes (28 days). Reason: {reason}')
    except discord.Forbidden:
        await interaction.response.send_message("I don't have the necessary permissions to send users to timeout.")
    except discord.HTTPException as e:
        await interaction.response.send_message(f'An error occurred while sending the user to timeout: {e}')
    except Exception as e:
        await interaction.response.send_message(f'Unexpected error: {e}')


welcome_message_global = None
@client.tree.command(name="welcome", description="Type a welcome message that will be privately sent when a new user joins", guild=GUILD_ID)
async def welcome(interaction: discord.Interaction, welcome_message: str = ""):
    global welcome_message_global
    if not welcome_message:
        await interaction.response.send_message("Please provide a welcome message.", ephemeral=True)
        return

    welcome_message_global = welcome_message
    await interaction.response.send_message("Welcome message has been set and will be sent to new members.", ephemeral=True)

@client.event
async def on_member_join(member):
    if welcome_message_global:
        try:
            await member.send(welcome_message_global)
        except Exception:
            pass

   
@client.event
async def on_guild_join(guild: discord.Guild):
    try:
        await client.tree.sync(guild=guild)  # Sync slash commands to the new guild
        print(f"Commands synced to new guild: {guild.name} ({guild.id})")
    except Exception as e:
        print(f"Failed to sync commands to {guild.name} ({guild.id}): {e}")



client.run('')






























































