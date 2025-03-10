import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from message_logger import MessageLogger
from response_generator import ResponseGenerator
from config import TARGET_GUILD_ID, TARGET_CHANNEL_ID
import logging

# Configure logging to output to the terminal
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Example of logging a message
logger.info("Bot is starting...")

# Load environment variables
load_dotenv()

class MoreBot:
    def __init__(self):
        # Set up Discord bot with ALL intents
        intents = discord.Intents.all()  # Enable all intents
        self.bot = commands.Bot(command_prefix='!', intents=intents)
        
        self.logger = MessageLogger()
        self.response_generator = ResponseGenerator()
        
        self.setup_events()
    
    def setup_events(self):
        @self.bot.event
        async def on_ready():
            print(f'{self.bot.user} has connected to Discord!')

        @self.bot.event
        async def on_message(message):
            # Only respond in the target server and channel
            if message.guild.id != TARGET_GUILD_ID or message.channel.id != TARGET_CHANNEL_ID:
                return

            # Ignore messages from the bot itself
            if message.author == self.bot.user:
                return

            # Log the message
            self.logger.log_message(message)
            
            # Generate and send response
            should_respond = await self.should_respond_to_more(message)
            
            if should_respond:
                response = await self.response_generator.generate_response(message)
                if response:
                    await message.channel.send(response)

            await self.bot.process_commands(message)

    async def should_respond_to_more(self, message):
        logger.info(f"Evaluating message: '{message.content}' from {message.author}")
        # Your logic to determine if the bot should respond
        return True  # or False based on your conditions

    def run(self):
        self.bot.run(os.getenv('DISCORD_TOKEN'))

if __name__ == "__main__":
    bot = MoreBot()
    bot.run()   