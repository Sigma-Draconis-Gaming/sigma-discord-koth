import datetime
import time

import requests
from discord_webhooks import DiscordWebhooks

web_hook_url = ""
bot_token = ""
base_discord_url = "https://discordapp.com/api/v6"
messages_endpoint = "/channels/689704387064496173/messages"
delete_endpoint = "/channels/689704387064496173/messages/{}"
discord_auth = {"Authorization": f"Bot {bot_token}"}


def delete_messages():
    r = requests.get(url=base_discord_url + messages_endpoint, headers=discord_auth)
    raw = r.json()
    ids = []
    if len(raw) > 1:
        for m in raw:
            ids.append(m["id"])
    requests.post(url=base_discord_url + delete_endpoint.format("bulk-delete"), headers=discord_auth,
                  json={"messages": ids})
    if len(raw) == 1:
        requests.delete(url=base_discord_url + delete_endpoint.format(raw[0]["id"]), headers=discord_auth)


def score():
    webhook = DiscordWebhooks(web_hook_url)
    r = requests.get("https://api.sigmadraconis.games/scores")
    servers = r.json()["scores"]
    s = set([s["Server"] for s in servers])
    print(s)
    for s in s:
        ss = [x for x in servers if x["Server"] == s]
        print(ss)
        p = set([s["PlanetId"] for s in ss])
        print(p)
        d = ""
        webhook.set_content(
            content="\n",
            title=f"Scores for {s}")
        for p in p:
            sss = [x for x in ss if x["PlanetId"] == p]
            d += f"\n**Planet**: ***{p}***\n"
            for sss in sss:
                d += f"\n**Faction**: {sss['FactionName']}\n"
                d += f"**Score**: {sss['Points']}\n"
        print(d)
        webhook.set_content(
            content="",
            title=f"Scores for **{s}**",
            url="https://sigmadraconis.games/koth.html",
            description=d,
            timestamp=str(datetime.datetime.now()),
            color=0xF58CBA)
        webhook.set_author(
            name="KOTH",
            icon_url="https://cdn.discordapp.com/attachments/657771421564534807/689958406194200666/draconis_logo.png",
            url="https://sigmadraconis.games/koth.html"
        )
        webhook.set_footer(text="https://sigmadraconis.games/koth.html", icon_url="https://cdn.discordapp.com/attachments/657771421564534807/689958406194200666/draconis_logo.png")
        webhook.set_thumbnail(url="https://cdn.discordapp.com/attachments/657771421564534807/689958406194200666/draconis_logo.png")
        webhook.send()
        time.sleep(5)


if __name__ == "__main__":
    while True:
        try:
            delete_messages()
            score()
            time.sleep(300)
        except Exception as e:
            print(e)
            continue
