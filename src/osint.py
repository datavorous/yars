from yars.yars import YARS
from meta_ai_api import MetaAI
import json

class RedditUserAnalyzer:
    def __init__(self):
        self.miner = YARS()
        self.ai = MetaAI()
        self.data = []

    def scrape_user_data(self, username, limit=30):
        user_data = self.miner.scrape_user_data(username, limit)
        for item in user_data:
            if item['type'] == 'comment':
                self.data.append(f"{item['subreddit']} > {item['body'].replace('\n', ' <line gap> ')}")

    def generate_ai_prompt(self):
        prompt_template = {
            "prompt_template": """
You are an AI assistant specialized in analyzing Reddit user data. Your task is to analyze the given user's comment history and provide insights into their personality, interests, and behavior.

Given the user's comment history, please provide an analysis focusing on the following aspects:

1. Personality Traits: Identify key personality traits based on the user's comments.
2. Interests & Passions: Determine the user's main interests and passions from their subreddit choices and comment content.
3. Communication Style: Describe how the user typically engages with others on Reddit.
4. Social Behavior: Infer the user's social interaction tendencies on the platform.
5. Recurring Themes: Identify any patterns or repeated themes in the user's comments.

For each aspect, provide a concise analysis supported by specific examples from the user's comment history when possible. Limit your total response to approximately 500 words.

User's comment history:
"""
        }
        
        # Add the scraped data to the prompt
        prompt_template["prompt_template"] += "\n".join(self.data)
        
        return json.dumps(prompt_template)

    def analyze_user(self):
        prompt = self.generate_ai_prompt()
        return self.ai.prompt(message=prompt)

if __name__ == "__main__":
    analyzer = RedditUserAnalyzer()
    analyzer.scrape_user_data("Global_Test_3950")
    ai_response = analyzer.analyze_user()
    print(ai_response)