import discord
from discord.ext import commands
from discord import Interaction, app_commands
import random
from discord.ext import commands
import json
import os
from discord import app_commands
import datetime

#Bot set up ---------------------------------------------------------------------------------------------------------------------------------------------

class Client(commands.Bot):
    async def on_ready(self):
        print(f'{self.user} logged in successfully')

        try:
            guild = discord.Object(id=1398401093809213504)
            synced = await self.tree.sync()
            print(f'Synced {len(synced)} global command(s).')

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

#bot set up ends here ---------------------------------------------------------------------------------------------------------------------------------------------




#Simple commands---------------------------------------------------------------------------------------------------------------------------------------------

@client.tree.command(name="hello", description="Ill say hello!",  )
async def sayhello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello!")

@client.tree.command(name="printer", description="I will say whatever you tell me!",  )
async def printer(interaction: discord.Interaction, printer: str):
    await interaction.response.send_message(printer)

@client.tree.command(name="cute-doggy", description="This is a rickroll",  )
async def printer(interaction: discord.Interaction):
    embed = discord.Embed(title="Cute Dog", url="https://www.youtube.com/watch?v=j5a0jTc9S10", description="Just a very cute dog", color=discord.Color.blue())
    embed.set_thumbnail(url="https://www.pawlovetreats.com/cdn/shop/articles/pembroke-welsh-corgi-puppy_600x.jpg?v=1628638716")
    embed.add_field(name="Info", value="Awww", inline=True)
    embed.add_field(name="More Info", value="So cute")
    embed.set_footer(text="Dog")
    embed.set_author(name=interaction.user.name, url="", icon_url="")
    await interaction.response.send_message(embed=embed)

#Simple commands end here---------------------------------------------------------------------------------------------------------------------------------------------


#All role commands---------------------------------------------------------------------------------------------------------------------------------------------

@client.tree.command(name="give_role", description="Type the role you would like to give and to which user",  )
async def assign_role(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    try:
        await member.add_roles(role)
        await interaction.response.send_message(f'Successfully assigned {role.name} to {member.name}')
    except discord.Forbidden:
        await interaction.response.send_message("I don't have the necessary permissions to assign roles.")
    except discord.HTTPException:
        await interaction.response.send_message('An error occurred while assigning the role. Please try again later.')

@client.tree.command(name="remove_role", description="Type the role you would like remove from a user and which user you would like to remove it from",  )
async def assign_role(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    try:
        await member.remove_roles(role)
        await interaction.response.send_message(f'Successfully removed {role.name} to {member.name}')
    except discord.Forbidden:
        await interaction.response.send_message("I don't have the necessary permissions to assign roles.")
    except discord.HTTPException:
        await interaction.response.send_message('An error occurred while assigning the role. Please try again later.')

@client.tree.command(name="role_info", description="Get information about a specific role in the server")
async def role_info(interaction: discord.Interaction, role: discord.Role):
    role_member_count = len(role.members)
    perms = [perm.replace('_', ' ').capitalize() for perm, value in role.permissions if value]
    perms_str = ", ".join(perms) if perms else "None"
    
    embed = discord.Embed(title=f"Role Information: {role.name}", color=role.color)
    embed.add_field(name="Role ID", value=role.id, inline=False)
    embed.add_field(name="Hoist", value=role.hoist, inline=False)
    embed.add_field(name="Position", value=role.position, inline=False)
    embed.add_field(name="Member Count", value=role_member_count, inline=False)
    embed.add_field(name="Permissions", value=perms_str, inline=False)
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

#Role commands end here ------------------------------------------------------------------------------------------------------------------------------


#All ban commands---------------------------------------------------------------------------------------------------------------------------------------------

@client.tree.command(name="ban_user", description="Select the user you would like to ban and the reason",  )
@app_commands.choices(clear_there_messages=[
    app_commands.Choice(name="Yes", value="yes"),
    app_commands.Choice(name="No", value="no")])
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "", clear_there_messages: str= ""):
    try:
        await member.ban(reason=reason)
        if clear_there_messages == "no":
            await interaction.response.send_message(f'Successfully banned {member.name} and did not clear their messages for: {reason} ')
        if clear_there_messages == "yes":
            for channel in interaction.guild.text_channels:
                try:
                    await channel.purge(limit=1000, check=lambda m: m.author == member)
                except Exception:
                    pass
            await interaction.response.send_message(f'Successfully banned {member.name} and cleared their messages for: {reason} ')
    except discord.Forbidden:
        await interaction.response.send_message("I don't have the necessary permissions to ban users.")
    except discord.HTTPException:
        await interaction.response.send_message('An error occurred while banning the user. Please try again later.')


@client.tree.command(name="unban_user", description="Unban a user by their user ID and provide a reason",  )
async def unban_user(interaction: discord.Interaction, user: discord.User, reason: str = ""):
    try:
        await interaction.guild.unban(user, reason=reason)
        await interaction.response.send_message(f'Successfully unbanned {user.name} for: {reason}')
    except discord.Forbidden:
        await interaction.response.send_message("I don't have the necessary permissions to unban users.")
    except discord.HTTPException:
        await interaction.response.send_message('An error occurred while unbanning the user. Please try again later.')



banned_words_file = "banned_words.json"

try:
    with open(banned_words_file, "r") as f:
        data = json.load(f)
        if isinstance(data, dict):
            banned_words = data
        else:
            banned_words = {}
except FileNotFoundError:
    banned_words = {}

def save_banned_words():
    with open(banned_words_file, "w") as f:
        json.dump(banned_words, f)

@client.tree.command(name="ban-words", description="Add a word to the banned words list")
@app_commands.choices(should_it_ban_user=[
    app_commands.Choice(name="Yes", value="yes"),
    app_commands.Choice(name="No", value="no")])

async def ban_words(interaction: discord.Interaction, word: str, should_it_ban_user: str):
    banned_words[word.lower()] = (should_it_ban_user.lower() == "yes")
    save_banned_words()
    await interaction.response.send_message(f'Added "{word}" to the banned words list with ban set to {should_it_ban_user}.')

@client.tree.command(name="unban-words", description="Remove a word from the banned words list")
async def unban_words(interaction: discord.Interaction, word: str):
    if word.lower() in banned_words:
        del banned_words[word.lower()]
        save_banned_words()
        await interaction.response.send_message(f'Removed "{word}" from the banned words list.')
    else:
        await interaction.response.send_message(f'"{word}" is not in the banned words list.')

@client.tree.command(name="list-banned-words", description="List all banned words")
async def list_banned_words(interaction: discord.Interaction):
    if banned_words:
        response = "Banned words: " + ", ".join(
            f"{w} (ban)" if banned_words[w] else f"{w}" for w in banned_words
        )
        await interaction.response.send_message(response)
    else:
        await interaction.response.send_message("No banned words set.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == 'hello kyro':
        await message.channel.send(f'Hi {message.author}')

    for banned_word, should_ban in banned_words.items():
        if banned_word in message.content.lower():
            await message.delete()
            if should_ban:
                try:
                    await message.author.ban(reason=f"Used banned word '{banned_word}'")
                except Exception:
                    pass
            else:
                await message.channel.send(
                    f"{message.author.mention}, your message contained a banned word.", delete_after=5
                )
            return

    await client.process_commands(message)

#All ban commands end here---------------------------------------------------------------------------------------------------------------------------------------------


#All game commands ---------------------------------------------------------------------------------------------------------------------------------------------

@client.tree.command(name="dice-roll", description="Rolls as many dice as you want (1–6)")
async def roll_dice(interaction: discord.Interaction, amountofdice: str = ""):
    amount = amountofdice.lower()

    if amount in ("1", "one"):
        roll = random.randint(1, 6)
    elif amount in ("2", "two"):
        roll = random.randint(2, 12)
    elif amount in ("3", "three"):
        roll = random.randint(3, 18)
    elif amount in ("4", "four"):
        roll = random.randint(4, 24)
    elif amount in ("5", "five"):
        roll = random.randint(5, 30)
    elif amount in ("6", "six"):
        roll = random.randint(6, 36)
    else:
        await interaction.response.send_message(
            "Please input a number from 1 to 6 — I don't own that many dice!")
        return

    await interaction.response.send_message(f"{roll} was rolled")
        

    
@client.tree.command(name="normal-dice-roll", description="Rigged Dice Roll")
async def rigged_dice(interaction: discord.Interaction, numberrolled: int= None):
    if numberrolled is None:
         await interaction.response.send_message("Please provide how many dice you want to roll (>ᴗ•)")
         return
    rigged_roll = random.randint(1, 100)

    if rigged_roll == 69:
        await interaction.response.send_message(f"Cheater you rigged it to roll {numberrolled}! 1% chance")
    else:
        await interaction.response.send_message(f"{numberrolled} was rolled.")
    



@client.tree.command(name="coin-flip", description="Flip a Coin",)
async def flip_coin(interaction: discord.Interaction, amountofcoins: str= ""):
    heads="Heads"
    tails="Tails"
    sides = [heads, tails]
    pick_side= random.choice(sides)
    await interaction.response.send_message(f"{pick_side}")




@client.tree.command(name="normal-coin-flip", description="Rigged Coin Flip")
@app_commands.choices(whichside=[
    app_commands.Choice(name="Heads", value="heads"),
    app_commands.Choice(name="Tails", value="tails")
])
async def choose(interaction: discord.Interaction, whichside: str):
    if whichside == "heads":
        rigged_flip = random.randint(1, 200)
        if rigged_flip == 42:
            await interaction.response.send_message("Cheater you rigged it to flip Heads 0.5% chance")
        else: 
            await interaction.response.send_message("Heads.")
    elif whichside == "tails":
        rigged_flip = random.randint(1, 200)
        if rigged_flip == 42:
            await interaction.response.send_message("Cheater you rigged it to flip Tails 0.5% chance")
        else: 
            await interaction.response.send_message("Tails.")

@client.tree.command(name="8ball", description="Type a question to ask the 8ball")
async def ask_8ball(interaction: discord.Interaction, question: str):
    responses = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful."
    ]
    await interaction.response.send_message(random.choice(responses), ephemeral=True)
    
#Game commands end here ---------------------------------------------------------------------------------------------------------------------------------------------




@client.tree.command(name="ultimate_timeout", description="They can't chat or join voice channels for 28 days",  )
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


#server owner commands start here ---------------------------------------------------------------------------------------------------------------------------------------------

welcome_message_global = None
@client.tree.command(name="welcome", description="Type a welcome message that will be privately sent when a new user joins",  )
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



@client.tree.command(name="clear_messages", description="Pick a number of the past messages to delete and the channel to delete them from")
async def delete_messages(interaction: discord.Interaction, number: int, channel: discord.TextChannel = None):
    target_channel = channel if channel else interaction.channel
    await interaction.response.defer(ephemeral=True)
    if number <= 0:
        await interaction.followup.send("Please provide a positive number of messages to delete.")
        return
    else:
        deleted = await target_channel.purge(limit=number + 1)  # +1 to include the command message itself
        await interaction.followup.send(f"Deleted {len(deleted)-1} messages.")


private_message_global = None
@client.tree.command(name="private_message", description="Private message a user, example: to warn them without using your account")
async def private_message(interaction: discord.integrations, user: discord.User, private_message: str):
    global private_message_global
    if not private_message:
        await interaction.response.send_message("Please provide a welcome message.", ephemeral=True)
        return
    else:
        await user.send(private_message)
        await interaction.response.send_message("Private message sent successfully.", ephemeral=True)
        

@client.tree.command(name="clear_bot", description="Clear all bot messages and pick from which channel only works on messages younger than 14 days")
async def clear_bot(interaction: discord.Interaction, channel: discord.TextChannel = None):
    target_channel = channel if channel else interaction.channel
    await interaction.response.defer(ephemeral=True)
    await target_channel.purge(limit=1000, check=lambda m: m.author == client.user)
    await interaction.followup.send("Bot messages cleared successfully.")
    

@client.tree.command(name="user_info", description="Get information about a specific user in the server")
async def user_info(interaction: discord.Interaction, user: discord.Member):
    user_member_count = len(user.roles)
    perms = [perm.replace('_', ' ').capitalize() for perm, value in user.guild_permissions if value]
    perms_str = ", ".join(perms) if perms else "None"
    
    embed = discord.Embed(title=f"User Information: {user.name}", color=user.color)
    embed.add_field(name="User ID", value=user.id, inline=False)
    embed.add_field(name="Member Count", value=user_member_count, inline=False)
    embed.add_field(name="Permissions", value=perms_str)
    embed.add_field(name="Joined At", value=user.joined_at, inline=False)
    embed.add_field(name="Created At", value=user.created_at, inline=False)
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

#All owner commands end here---------------------------------------------------------------------------------------------------------------------------------------------

client.run('DISCORD_TOKEN')
































































