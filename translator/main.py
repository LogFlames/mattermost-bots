from eliasmamo_import import *
from secret import TOKEN, OPENAI_API_KEY
from dictionary import DICTIONARY
import openai
import json

ADMIN_TRANSLATION_TEST_CHANNEL_ID = "8u5crz5fjid15nphaecbxb84er"
EVENTS_CHANNEL_ID = "it7zah8m5jrw9dm8bkjm14eyaw"
SEKTIONSNYTT_CHANNEL_ID = "pda7c6r7zbbtmc17x4ehczc8gc"
EVENEMANG_CHANNEL_ID = "wkgnsmmbqpgpj8ptdiyx8os16c"

def translate(openai_client: openai.OpenAI, message):
    try:
        completion = openai_client.chat.completions.create(
          model="gpt-3.5-turbo",
          messages=[
              {"role": "system", "content": "You are a skilled professional translator assistant that translates messages from swedish to english on demand with high accuracy. To your help you have the following dictionary that directs you how to translate specific phrases. In the dictionary commas are used to indicate there are multiple phrases with the same meaning:" + 
               DICTIONARY},
              {"role": "user", "content": "Translate the following swedish text in the markdown code while preserving markdown syntax and whitespaces:\n" + message}
          ]
        )

        return completion.choices[0].message.content
    except Exception as e:
        print(f"OpenAI threw an error: {e}")
        return None

def handle_event(driver: Driver, openai_client: openai.OpenAI, data):
    post = json.loads(data["post"])
    if post["channel_id"] not in (SEKTIONSNYTT_CHANNEL_ID, EVENEMANG_CHANNEL_ID, ADMIN_TRANSLATION_TEST_CHANNEL_ID):
        return

    if post["user_id"] == driver.client.userid:
        return

    if post["type"].startswith("system"):
        return

    if post["root_id"]:
        return

    driver.channels.add_user(EVENTS_CHANNEL_ID, {"user_id": post["user_id"]})

    delete_new_posts_in_clean_channels(driver, {"events": EVENTS_CHANNEL_ID})

    message_eng = translate(openai_client, post["message"])

    if message_eng is None:
        driver.posts.create_post({"channel_id": ADMIN_TRANSLATION_TEST_CHANNEL_ID, "message": "Error occured while translating a message with openai. Check journal."})
        return

    dm_channel = driver.channels.create_direct_message_channel([post["user_id"], driver.client.userid])

    driver.posts.create_post({
        "channel_id": dm_channel["id"], 
        "message": """Vi vill gärna att internationella studenter får möjlighet att gå på evenemang som kan ges på engelska. Vänligen lägg upp ditt evenemang i den engelska kanalen [info-eng](https://mattermost.fysiksektionen.se/fysiksektionen/channels/events) i Fysiksektionen-teamet ifall det är relevant att internationella studenter får informationen. Här är ett förslag på en översättning att utgå ifrån:"""})

    driver.posts.create_post({
        "channel_id": dm_channel["id"], 
        "message": message_eng})

def main():
    driver = Driver(
            {
                'url': 'mattermost.fysiksektionen.se',
                'basepath': '/api/v4',
                'verify': True,
                'scheme': 'https',
                'port': 443,
                'auth': None,
                'token': TOKEN,
                'keepalive': True,
                'keepalive_delay': 5,
                }
            )

    driver.login()

    openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

    ws = WebSocket(TOKEN)

    ws.subscribe("posted", lambda data: handle_event(driver, openai_client, data))

    ws.join()

if __name__ == "__main__":
    main()
