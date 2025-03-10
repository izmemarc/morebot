import logging
import json
import sys
from datetime import datetime
from pathlib import Path

class MessageLogger:
    def __init__(self, log_file="logs/messages.json"):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(exist_ok=True)
        
        # Create log file if it doesn't exist
        if not self.log_file.exists():
            self.log_file.write_text("[]")
        
        # Configure logging to both file and console
        self.logger = logging.getLogger('discord_bot')
        self.logger.setLevel(logging.INFO)
        
        # File handler
        file_handler = logging.FileHandler('logs/discord_bot.log')
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        
        # Add both handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def log_message(self, message):
        """Log a Discord message with timestamp and relevant information"""
        # Create message data
        message_data = {
            'timestamp': datetime.now().isoformat(),
            'author': str(message.author),
            'content': message.content or '[empty]',  # Handle empty messages
            'channel': str(message.channel),
            'guild': str(message.guild),
            'is_mention': self.bot.user.mentioned_in(message) if hasattr(self, 'bot') else False
        }

        try:
            # Load existing messages
            try:
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    messages = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                messages = []

            # Add new message
            messages.append(message_data)

            # Save updated messages
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(messages, f, indent=2, ensure_ascii=False)

            self.logger.info(f"Message from {message.author}: {message.content or '[empty]'}")

        except Exception as e:
            self.logger.error(f"Error logging message: {e}") 