import random
import openai
import praw
import os
import time

max_comments = 10
subreddit_name = 'askreddit'
min_seconds = 600
max_seconds = 900
chatgpt_model = "text-davinci-003"
# Enable sleep if you get api throttled when posting comments
enable_sleep = False

openai.api_key = os.environ["CHATGPT_TOKEN"]


def get_chatgpt_answer(prompt):
    response = openai.Completion.create(
        model=chatgpt_model,
        prompt=prompt,
        max_tokens=50,
        temperature=0
    )
    return response.choices[0].text


def get_reddit_posts():
    reddit = praw.Reddit(client_id=os.environ["CLIENT_ID"],
                         client_secret=os.environ["CLIENT_SECRET"],
                         password=os.environ["PASSWORD"],
                         user_agent=os.environ["USER_AGENT"],
                         username=os.environ["USERNAME"])
    subreddit = reddit.subreddit(subreddit_name)
    return subreddit.top(limit=10, time_filter='hour')


def main():
    reddit_posts = get_reddit_posts()
    successful_posts = 0

    while successful_posts <= max_comments:
        for post in reddit_posts:
            if successful_posts > max_comments:
                break
            if not post.over_18:
                reddit_post_title = post.title
                print(f"Title: {reddit_post_title}")

                chatgpt_response = get_chatgpt_answer(reddit_post_title)
                print(f"ChatGPT Answer: {chatgpt_response}")
                post.reply(body=chatgpt_response)

                successful_posts += 1

                if enable_sleep:
                    random_seconds = random.randint(min_seconds, max_seconds)
                    time.sleep(random_seconds)

    print(f"Max comments reached! : {successful_posts}")


if __name__ == "__main__":
    main()
