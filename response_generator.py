import openai
import random
import os
from response_conditions import ResponseConditions
from dotenv import load_dotenv

class ResponseGenerator:
    def __init__(self):
        # Set up OpenAI
        load_dotenv()
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.conditions = ResponseConditions()

    async def generate_response(self, message):
        content = message.content.strip()

        # Check if the bot should respond based on conditions
        should_respond = await self.conditions.should_respond_to_more(message)
        if not should_respond:
            return None  # Do not generate a response if conditions are not met

        # Check if the response condition indicates "heard_more"
        if "heard_more" in content:
            return "i heard more!"

        # Generate a silly response related to "more" based on the user's message
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a dumb annoying sarcastic character who loves saying 'more' and responds in lower case and no emojis." +
                        "You very short sentences but make it make sense, and your sole purpose is to mock the user." +
                        "If the user says good morning, you will reply good morening and don't say more after that." +
                        "make sure 'more' sounds natural in the sentence dont put it at the end only"
                    },
                    {"role": "user", "content": content}
                ],
                max_tokens=15,
                temperature=0.9
            )
            
            ai_response = response.choices[0].message.content.strip().lower()
            
            # Ensure the response contains 'more'
            if 'more' not in ai_response:
                return None  # Do not respond if 'more' is not included
            
            return ai_response  # Return only the AI response

        except Exception as e:
            print(f"Error with OpenAI API (generate_response): {e}")
            return "more!"  # Fallback response

    async def should_respond_to_more(self, message):
        # Implementation of should_respond_to_more method
        pass

    async def get_ai_response(self, message):
        # Implementation of get_ai_response method
        pass
