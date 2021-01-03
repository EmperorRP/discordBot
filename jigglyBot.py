import discord
import random
import os
from discord.ext import commands, tasks
import time
from itertools import cycle

client = commands.Bot(command_prefix = '*')
status = cycle(['I am cute'])



#Reaction Roles
reaction_title=""
reactions={}
reaction_message_id=""
@client.command(name="reaction_create_post")
async def reaction_create_post(ctx):
    embed=discord.Embed(title="Create Reaction Post",color=0x8cc542)
    embed.set_author(name="JigglyMod Bot")
    embed.add_field(name="Set Title", value="*reaction_set_title \"New Title\"",inline=False)
    embed.add_field(name="Add Role", value="*reaction_add_role @Role EMOJI",inline=False)
    embed.add_field(name="Remove Role", value="*reaction_remove_role @Role",inline=False)
    embed.add_field(name="Send Creation Post", value="*reaction_send_post",inline=False)
    await ctx.send(embed=embed)
    await ctx.message.delete()

@client.command(name="reaction_set_title")
async def reaction_set_title(ctx,new_title):
    global reaction_title
    reaction_title = new_title
    await ctx.send("The title for the message is now '"+reaction_title+"'!")
    await ctx.message.delete()

@client.command(name="reaction_add_role")
async def reaction_add_role(ctx, role: discord.Role, reaction):
    if role != None:
        reactions[role.name]=reaction
        await ctx.send("Role '"+ role.name +"' has been added with emoji"+ reaction)
        await ctx.message.delete()
    else:
        await ctx.send("Please try again")

    print(reactions)
    
@client.command(name="reaction_remove_role")
async def reaction_remove_role(ctx, role: discord.Role, reaction):
    if role.name in reactions:
        del reactions[role.name]
        await ctx.send("Role '"+ role.name +"' has been removed")
        await ctx.message,delete()
    else:
        await ctx.send("That role was not added")
    print(reactions)

@client.command(name="reaction_send_post")
async def reaction_send_post(ctx):
    description = "React to add the Roles!\n"
    
    for role in reactions:
        description +="'"+role+"' -" + reactions[role]+"\n"

    embed = discord.Embed(title=reaction_title, description = description, color=0x8cc542)
    embed.set_author(name="JigglyMod Bot")

    message = await ctx.send(embed=embed)

    global reaction_message_id
    reaction_message_id=str(message.id)

    for role in reactions:
        await message.add_reaction(reactions[role])
    await ctx.message.delete()

@client.event
async def on_reaction_add(reaction, user):
    if not user.bot:
        message=reaction.message
        if str(message.id)==reaction_message_id:
            #add roles to users
            role_to_give=""

            for role in reactions:
                if reactions[role]== reaction.emoji:
                    role_to_give = role
            role_for_reaction = discord.utils.get(user.guild.roles,name=role_to_give)
            await user.add_roles(role_for_reaction)

    
#Status + Online
#Status
@client.event
async def on_ready():
    change_status.start()
    #await client.change_presence(status=discord.Status.idle,activity=discord.Game('Simping Lina'))
    print("Bot is Online")
    
#Changing Status every 10s   
@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

    
#Error if command not found
@client.event
async def on_command_error(ctx,error):
    resp=["Not a valid command."]
    if isinstance(error,commands.CommandNotFound):
        await ctx.send(random.choice(resp))


#Only those with permissions can use the following
@commands.has_permissions(manage_messages=True)        

#Clears Texts
@client.command()
async def clear(ctx, amount:int):
    await ctx.send(f"Clearing {amount} message(s)")
    time.sleep(0.79)
    await ctx.channel.purge(limit=amount+2)
    
#Error message if incorrect clear command
@clear.error
async def clear_error(ctx,error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify number of texts')

#pin message

@client.event
async def on_message(message, channel="instagram-ids"):
    if "instagram.com" in message.content:
        await message.pin()
    await client.process_commands(message)


'''
@client.event
async def on_message(message):
    args = message.content.split(" ")[1:]
    print(args)
    msg = await message.channel.fetch_message(int(messageID))
    if ("instagram.com" in args):
        
 '''   
client.run('NzgwNDI0NTU1NTU4NzMxNzg2.X7u5AQ.Pxk4fUg7CMT5YQADcvGtrRsqqsA')

#Upvote downvote Reactions
'''
@client.event

async def on_message(message):
    if discord.File.endswith('jpg') in message.content:
        await message.add_reaction('\U0001F44D')
'''

