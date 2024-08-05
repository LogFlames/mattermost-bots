from eliasmamo_import import *
from secret import TOKEN
import os
import datetime
from mattermostdriver.exceptions import ResourceNotFound

blacklisted_messages = {
        "matwan": ['i3mimqq3djd4iy95o77wbdcd8a', 'mbd43kbx4pfmzc1w3w1p36yaye', 'ezmpb5jdw78ax8cdjxyoii5nuo'],
        "sael": ['xj3hucrrdtb87e3jdbjx74ndha', '4j8fkgg6ff8ujmk1qjcscn8q7h', 'zhcxtbu44f8sbnz8wpzt1u9uta', '58s7xrcgp3gnin75aor6gf98po', 'da99n6pgdfypmd7eypdqk7j1sa'],
        "emmakt": [],
        "lagehl": ['mrne9w9ur7fqjbiqyfjkn7nh9o'],
        "fiek": ['gdjwfnhjjfn7fpz9x13z68xd4w'],
        "kajsaeng": ['t8zgua7g33gjmy7jpniwhby35e'],
        "ljanes": ['jmigo3ngi3rdmpbzjb9higydkw'],
        "chrieh": ['9zqw5971qp8h5mpi81yb6g9zha'],
        "martengf": ['hxaqro8a5tnw9jinoz6gamnqrw'],
        "jjl": ['ce55eda867dotbc383moqeu1ae'],
        "tufva": ['zjuk3dh8d3n8uxgocr1e38pyfe', 'gebnz5tg9tntpeetxup9n58s5o'],
        "fysikalen_team": ['3kyyh5tscinexd7yjjiwoeyn6h', 'yipjz849z3brdrfag9ty417rgo'],
        "eskilny": ['yocdihjb3igfdmtdg694ifoe7a'],
        "mollyw": ['uo9sygcj67frbqm9smh73zr8wo'],
        "lstal": ['ep5wmummtpbpxk7qiz8o37wzxy', 'u4jihq3brp8o7jojig7mqu3zoy'],
        "halinda": ['aj8mcxae3b85pyh4ohp94roqoa'],
        "m24": ['55qisg8eyjbopnojjinudyfz6e', '5zy8cfbdmifyd8w4xwaiiqc6hr', 'sjuz89jioiny9n7is9znawgx1c', 'pr6stppgt7g6mbm1gui7pz9ehy', 'k9p43bryhpfo3ptmx8cpdbfmxe', 'eawwpk3cjfnrdpbosgatkrh55r', '9riiyhfzipbodep9ztfg8o98ky', 'br5k7684zigr8kwes5o7r8im7a', 'rbefyjfmkpft7q7xq99uo6xbzr', 'zp6wtadxyb8gbd3r4dqkog8dfo', 'peofb4wmxjr9xr9ix778jzns8y', 'bjw7app14f8xdngzk1ckaa5xjh', 'jq3ggpudef8hfkh5a3xmoanqah', 'cdnj3gwuz7rqzc1pjop65dnokr', 'ht1yzxk5yfb5jr66tamg93xkzy', 'u17o9mc3uj8rxfcf5zqrse41hw', 'oj3qt6dfsjge5c8k4s18kkcj9a', 'etf6cg1r7fbptfcnb1kb891o3y', 'bdfbzgegp3ykmmqquo7dxwt4cc'],
        "lukasgra": ['jeh8jpors7ysde1u3ymkba4fta', 'fphrq68na3y87mq6dmxuugudzo', 'baiq5kz94bd4myubkzcip5rx5a', 'cgnp933eqbdi7rawac9e6twg4o'],
        "edwinost": ['ntbgtqi87jdspp6wfw87ghjxqr'],
        "juliasv": ['pi61m6dp9jgxjpwju7gsygoqrh'],
        "antmatt": ['kgnwcj8roj8x9bk6awxs3eb7ee'],
        "magdb": ['d34orrdqc7r1txahhp8gr768dc', '9p3s6ox43p8xxbzmqj1ijhze1a', '8418biktu7byimwnpw55zn3f6r', 'hkkscjmubig7dew9i133frkbby', 'qkqkj5q5afribfbkzckp5egnpw', '3x5m16z347buibpihyjrdxww3a', 'hedoc9oj5fri8y5o5n5a5bxjwo', 'r7wgt9j3k7ymir3u6ds4h6b73e', 's9wp41ozn7rjiyr4ghnfh8c4go', 'fjqku113z3gqze6u3qfatyckfr', '3do99qfk7jb4de8d35qcdbek5e', 'tco1hcer5t85tq4xgq1h71aide', 'neitx5ukzpytb8jxnus3c7aioa', 'hnpc7ymb7iyixxz1ef949nn3dw', 'zqk54kf1bpdnjrkezxkqgm316a'],
        "rylla": ['jix9eywmnbnkx86a73r6ycgwyr', '13e7i34fhtg7xqmdsj1y4mwn7o', 'mm7jhnhjhfr4xn4s9c6exfj3de', 'adpbccgkcpdbzgkyny7gpt66zy', '6om8jexwnfntiqphrtbnp3z6dr', '5me4u9ziujb3fc9nkrxt1sww8o', 'i5e7qithm7yqix943a3t3z9n4a', 'zy9nzig4mtbn8et374kmitjsiw', 'mp4aqddwridy5ennhttsz7fo3o', 'or3jpyh8q7dq7gdmh5bkborsqh', 'gtgn57ukdf8epe9wtapa7e3bah', 's9jj7q89xbgquyosrpqf8yb3wc']
        }

messages_to_delete = []
for person in blacklisted_messages:
    messages_to_delete.extend(blacklisted_messages[person])

def main():
    while (ans := input("(D). Delete messages\n(U). Generate Update Query \n(q). Quit\nWhat do you want to do?: ")) not in ("D", "U", "q"): pass
    if ans == "D":
        if not os.path.exists("deleted_messages/"):
            os.mkdir("deleted_messages/")

        name = f"deleted_messages/deleted_messages_at-{datetime.datetime.now()}.log"
        print(f"Writing messages to file: {name}")
        with open(name, "w+") as log:
            deleted_messages = set()
            driver: Driver = Driver(
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

            for message in messages_to_delete:
                try:
                    post = driver.posts.get_post(message)
                except ResourceNotFound:
                    print(f"Could not find message: {message}")
                    continue
                for reply in driver.posts.get_thread(message)['posts'].keys():
                    print(f"Saving reply id: {reply}")
                    deleted_messages.add(reply)
                    log.write(f"{reply}\n")
                channel = driver.channels.get_channel(post["channel_id"])
                if channel["delete_at"] > 0:
                    print(f"Restoring channel {post['channel_id']}")
                    driver.channels.restore_channel(post["channel_id"])

                print(f"Deleting message: {message}")
                driver.posts.delete_post(message)

                if channel["delete_at"] > 0:
                    print(f"Archiving channel {post['channel_id']}")
                    driver.channels.delete_channel(post["channel_id"])

        if len(deleted_messages) == 0:
            print("Did not delete any messages")
            exit(1)

    elif ans == "U":
        p = input("Path to file with messages (excluding 'deleted_messages/'): ")
        pp = os.path.join(os.path.dirname(__file__), "deleted_messages/", p)
        if not os.path.exists(pp):
            print(f"Could not find file: {pp}")
            exit(1)

        with open(pp, "r") as f:
            messages = f.read().split()
        posts = "', '".join(messages)
        print(f"UPDATE posts SET deleteat = 0 WHERE id IN ('{posts}');")
        print(f"UPDATE fileinfo SET deleteat = 0 WHERE postid IN ('{posts}');")

if __name__ == "__main__":
    main()

