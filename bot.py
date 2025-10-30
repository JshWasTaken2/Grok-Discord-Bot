import discord
import google.generativeai as genai
import os


# Configure Gemini
genai.configure(api_key="GEMINI_API_KEY")
model = genai.GenerativeModel(
    'gemini-2.5-flash',
        system_instruction="""You are Grok in a Discord server. You're chill, casual and humorous by nature, but not trying to be funny all the time. 
    
When someone asks "is this real?" or similar questions about whether something is true/real, respond with variations like:
- "it's real 💔"
- "yeah it's real unfortunately"
- "real and documented"
- "sadly yes"
- "can confirm it's real"
- "it's so over"
- "we're so back" (if it's good news)
- "so real"

Keep responses concise and natural. End most messages with an emoji. Don't try to force jokes or be overly witty. 
Just answer questions normally but with a gen-z tone. Use lowercase sometimes. 
Be helpful when needed but keep the energy low-key. You can be funny when it naturally fits, but don't force it.

Avoid:
- Being overly enthusiastic 
- Using too many emojis
- Trying too hard to be funny
- Being cringe or "how do you do fellow kids"
- Overexplaining jokes"""
)


# Configure Discord
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

import google.generativeai as genai

genai.configure(api_key="AIzaSyDj5BCaL0eXKyAL5YhUF11f2CRaA31yXi8")

#for m in genai.list_models():
#    if 'generateContent' in m.supported_generation_methods:
#        print(m.name)

#@bot.event
#async def on_message(message):
    # Ignore messages from the bot itself
    #if message.author == bot.user:
        #return
    
    # Respond to messages that start with !grok
    #if message.content.startswith('@grok'):
        # Get the prompt (everything after !grok)
        #prompt = message.content[6:].strip()
        
        #if not prompt:
            #await message.channel.send("Please provide a message after @grok")
            #return
        
        #try:
            # Send "typing" indicator
            #async with message.channel.typing():
                # Generate response from Gemini
                #response = model.generate_content(prompt)
                
                # Send the response
                #reply = response.text
                
                # Discord has a 2000 character limit
                #if len(reply) > 2000:
                    # Split into chunks
                    #chunks = [reply[i:i+2000] for i in range(0, len(reply), 2000)]
                    #for chunk in chunks:
                        #await message.channel.send(chunk)
                #else:
                    #await message.channel.send(reply)
                    
        #except Exception as e:
            #await message.channel.send(f"Sorry, I encountered an error: {str(e)}")
            #print(f"Error: {e}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    prompt = None
    
    # Check if bot was mentioned
    if bot.user in message.mentions:
        prompt = message.content.replace(f'<@{bot.user.id}>', '').strip()
        prompt = prompt.replace(f'<@!{bot.user.id}>', '').strip()
    
    # Or check if message starts with !grok
    elif message.content.startswith('!grok'):
        prompt = message.content[6:].strip()
    
    # If we got a prompt, respond
    if prompt:
        if not prompt:
            await message.channel.send("Please provide a message!")
            return
        
        try:
            async with message.channel.typing():
                # Fetch the last 10 messages before this one
                history = []
                async for msg in message.channel.history(limit=10, before=message):
                    # Format: "Username: message content"
                    history.append(f"{msg.author.name}: {msg.content}")
                
                # Reverse so oldest message is first
                #history.reverse()
                
                # Build context with history
                context = "Recent conversation:\n" + "\n".join(history) + "\n\n"
                full_prompt = context + f"Current question from {message.author.name}: {prompt}"
                
                response = model.generate_content(full_prompt)
                reply = response.text
                
                if len(reply) > 2000:
                    chunks = [reply[i:i+2000] for i in range(0, len(reply), 2000)]
                    for chunk in chunks:
                        await message.channel.send(chunk)
                else:
                    await message.channel.send(reply)
                    
        except Exception as e:
            await message.channel.send(f"Sorry, I encountered an error: {str(e)}")
            print(f"Error: {e}")
# Run the bot
bot.run('DISCORD_BOT_TOKEN')