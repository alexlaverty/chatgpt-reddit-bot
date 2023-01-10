import openai
import praw
import os

max_comments = 5
subreddit_name = 'askreddit'

# Assign API key before function call
openai.api_key = os.environ["CHATGPT_TOKEN"]


def get_chatgpt_answer(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        temperature=0
    )
    return response.choices[0].text


def main():

    # Create a Reddit instance and authenticate
    reddit = praw.Reddit(client_id=os.environ["CLIENT_ID"],
                         client_secret=os.environ["CLIENT_SECRET"],
                         password=os.environ["PASSWORD"],
                         user_agent=os.environ["USER_AGENT"],
                         username=os.environ["USERNAME"])

    # Loop through the latest Reddit posts in the r/AskReddit subreddit
    subreddit = reddit.subreddit(subreddit_name)
    latest_post = subreddit.hot(limit=10)
    successful_posts = 0

    while successful_posts <= max_comments:
        for post in latest_post:
            if successful_posts > max_comments:
                break

            if not post.over_18 and post.score > 10:
                reddit_post_title = post.title
                print(f"Title: {reddit_post_title}")

                chatgpt_response = get_chatgpt_answer(reddit_post_title)
                print(f"ChatGPT Answer: {chatgpt_response}")
                post.reply(body=chatgpt_response)

                successful_posts += 1

    print(f"Max comments reached! : {successful_posts}")


if __name__ == "__main__":
    main()
