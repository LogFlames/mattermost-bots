from eliasmamo_import import *
from secret import TOKEN
import os
import datetime
from mattermostdriver.exceptions import ResourceNotFound
import time

blacklisted_messages_2023_2024 = {
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
        "m24": ['55qisg8eyjbopnojjinudyfz6e', '5zy8cfbdmifyd8w4xwaiiqc6hr', 'sjuz89jioiny9n7is9znawgx1c', 'pr6stppgt7g6mbm1gui7pz9ehy', 'k9p43bryhpfo3ptmx8cpdbfmxe', 'eawwpk3cjfnrdpbosgatkrh55r', '9riiyhfzipbodep9ztfg8o98ky', 'br5k7684zigr8kwes5o7r8im7a', 'rbefyjfmkpft7q7xq99uo6xbzr', 'zp6wtadxyb8gbd3r4dqkog8dfo', 'peofb4wmxjr9xr9ix778jzns8y', 'bjw7app14f8xdngzk1ckaa5xjh', 'jq3ggpudef8hfkh5a3xmoanqah', 'cdnj3gwuz7rqzc1pjop65dnokr', 'ht1yzxk5yfb5jr66tamg93xkzy', 'u17o9mc3uj8rxfcf5zqrse41hw', 'oj3qt6dfsjge5c8k4s18kkcj9a', 'etf6cg1r7fbptfcnb1kb891o3y', 'bdfbzgegp3ykmmqquo7dxwt4cc', '1f5xfibtyjy7z8c8as3huxbj3r', 'jgxkzsm5s3gpzqq5joor79f5oh', 'dmhqqsamkfgifpgta444ixk9na', 'abfibbotq3btbgsnpm5h9jhfuh', '8wfmk11idtge8rgstdb7dh9j4a', 'adbdrnfsiidgtrcyie8baykgny'],
        "lukasgra": ['jeh8jpors7ysde1u3ymkba4fta', 'fphrq68na3y87mq6dmxuugudzo', 'baiq5kz94bd4myubkzcip5rx5a', 'cgnp933eqbdi7rawac9e6twg4o'],
        "edwinost": ['ntbgtqi87jdspp6wfw87ghjxqr'],
        "juliasv": ['pi61m6dp9jgxjpwju7gsygoqrh'],
        "antmatt": ['kgnwcj8roj8x9bk6awxs3eb7ee'],
        "magdb": ['d34orrdqc7r1txahhp8gr768dc', '9p3s6ox43p8xxbzmqj1ijhze1a', '8418biktu7byimwnpw55zn3f6r', 'hkkscjmubig7dew9i133frkbby', 'qkqkj5q5afribfbkzckp5egnpw', '3x5m16z347buibpihyjrdxww3a', 'hedoc9oj5fri8y5o5n5a5bxjwo', 'r7wgt9j3k7ymir3u6ds4h6b73e', 's9wp41ozn7rjiyr4ghnfh8c4go', 'fjqku113z3gqze6u3qfatyckfr', '3do99qfk7jb4de8d35qcdbek5e', 'tco1hcer5t85tq4xgq1h71aide', 'neitx5ukzpytb8jxnus3c7aioa', 'hnpc7ymb7iyixxz1ef949nn3dw'],
        "rylla": ['jix9eywmnbnkx86a73r6ycgwyr', '13e7i34fhtg7xqmdsj1y4mwn7o', 'mm7jhnhjhfr4xn4s9c6exfj3de', 'adpbccgkcpdbzgkyny7gpt66zy', '6om8jexwnfntiqphrtbnp3z6dr', '5me4u9ziujb3fc9nkrxt1sww8o', 'i5e7qithm7yqix943a3t3z9n4a', 'zy9nzig4mtbn8et374kmitjsiw', 'mp4aqddwridy5ennhttsz7fo3o', 'or3jpyh8q7dq7gdmh5bkborsqh', 'gtgn57ukdf8epe9wtapa7e3bah', 's9jj7q89xbgquyosrpqf8yb3wc']
        }

blacklisted_messages_2025 = {
        "martengf": ["kc6ge5uhj78d5n8ktum6o6zkpa", "17354enyrtfc9gwzwdag86sn8o", "mazw6iffdb8mjf67gzigw1jaia", "k6px4en5qb8mmnm37gn9hi873c", "eehnbq1tmprdxkiba8yhqbpymh"],
        "hlennman": ["89npfaxb6jfpumrj7sandg1e7r"],
        "mollyw": ["ofr36mkh5tr7pk88d6965h7k1o", "1r15neoeh3dt3rh46ow58xm4pa"],
        "signesv": ["rkhx9wghtid6iccgukux9rtt3y", "7gchxbrq6jnsbdm7qpyw4ykf7a", "jz7f9m11fbr8jrfcgrztk8qkkh"],
        "sernlund": ["be8mjm9jji8pmjbt3ss69pkqah"],
        "ntiemer": ["jtejg9fedj8xuerkyb11t31w5r", "aqjgbafyiire7e8yupuhho59pr", "us9j9aks3tde8gdmt9tqmig9ma"],
        "m25": ["adb5qhawy7rz9eetuo8gm1sepa", "bjy4ush8nbdtzydx6cu3pyhp6r", "jaanyrzxo7dn9ksy1cizf5psua", "un85pdmbjincdbox8njph76wta", "n4etuspw9injfm8xgy5yith5ky", "1oxyebttebgypmg1ord4fzie8w", "cxzjusbfjidoifeeiscy3em9fo", "8n6jhh6zgfnhzn7ycjxnkd5h4a", "r49jtxxq1pnxfn7qxocjmubitc", "9syd9fw1ztdupg84b5k5tcyjiy", "gwfbttf1g3bnzmwmfwqu4bz9oh", "awb8ix4p93y68fsr5wu5r83a4a", "tr8rqukynfyzjx4od3mc9m9ary", "repou6549jgifdh69dwmwz78tw", "9h7hxfjxq78a9xoarmnz4yxufe", "53yeemnkgbnf8gr9riiirxnguh", "paexm3yxx38yirg8s9isus8o5y", "g66p8zkxw78cdfhuramo3oykxo", "ynh8s1smzir1texpfkx55eqtqw", "86ucz4nbrfrgjybktqzhd3c9hh", "r4yn8gzenjf8dnwssnwbazjg5y", "m5hphb7z5byddy5wb77zfwsfyy", "y4pchh3mm7ybtyhc976jt5usia", "owbufgibnind7yuxn7az6qd4kr", "tj3kcak9pp83zk5k9atjf7kxmw", "ujuzmo7b8fd85nan4wmn3gbmey"],
        "sjsak": ["nfhra1s5sibgxk836r7867n1rc"],
        "ltrolin": ["ycphyuxsj3d6d8xo5uz7xuwyhe"],
        "ebbalo": ["ybqwcspu7t89bfffy99fg3mqzy"],
        "juliasve": ["irbhdrmn8ffyur18rjco96y51o", "9uyyceuuyinojpyggzfxmhopse", "9kyj5d6zb3b48nwwh3bwss4nde", "11cd83nentyp3kor9hh74ekmir"],
        "haggbr": ["c33ipzoebtrcmesu6unf1f6qnc"],
        "alvaah": ["pefh44t3gfncbnksm18wjkxnco", "itbe97pjs7fixku1d68hdqou4a"],
        "lukasgra": ["mookuy4unjncdf3uizq89jp43h", "8xaeukt1kjgitpchykoe4u5z6c"],
        "strende": ["xgcib99bmidr9yf9ksd3ghp9yh", "ryns9xr3m7diieogsjhqhps34o"],
        "aleung": ["o18eh6owdfgf5bsstxqg8q7bqe"],
        "emmiez": ["o8tq664egb83zr4b839th7sb1w", "5sydck8a4jrwdnw8ux3tzhcexo"],
        "chen9": ["sh9oktec8tb55yi4qkfh4c5cna", "7bdxahj38iyw5f9jzuc7dnpmza"],
        "albinwl": ["nowkmong8jny7eqzgqbi84yqzy"],
        "armanas": ["7rm8dz5qbp8k3fge9msh3ta3xo"],
        "magdb": ["xpmqb8ox53byznu9ked9higefh"],
        "elbergst": ["meisaho9yin3zfo3nt3mfp6kxo", "i8tt7qo8g7n88bgoqtfxtgtnrh", "zntz86ne3fdzik498spudzcete"]
        }

blacklisted_messages = {}

for year in [blacklisted_messages_2023_2024, blacklisted_messages_2025]:
    for name in year:
        if name not in blacklisted_messages:
            blacklisted_messages[name] = []

        for message in year[name]:
            if message not in blacklisted_messages[name]:
                blacklisted_messages[name].append(message)

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
                time.sleep(0.1)
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

