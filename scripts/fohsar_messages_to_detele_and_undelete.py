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
        "martengf": ["kc6ge5uhj78d5n8ktum6o6zkpa", "17354enyrtfc9gwzwdag86sn8o", "mazw6iffdb8mjf67gzigw1jaia", "k6px4en5qb8mmnm37gn9hi873c", "eehnbq1tmprdxkiba8yhqbpymh", "mz5jdwstejfgmgfhctpfbcpw4h", "7dcz5jhegbgajr3ntd4yr57y5o", "kd6puhe3jffjtqksnzcfmdk6aw"],
        "hlennman": ["89npfaxb6jfpumrj7sandg1e7r"],
        "mollyw": ["ofr36mkh5tr7pk88d6965h7k1o", "1r15neoeh3dt3rh46ow58xm4pa"],
        "signesv": ["rkhx9wghtid6iccgukux9rtt3y", "7gchxbrq6jnsbdm7qpyw4ykf7a", "jz7f9m11fbr8jrfcgrztk8qkkh", "njkh7hbfpbycidy6cei477jatc", "qi76o8kcitdr3ywzs1aq4oookh", "erjp4j1ttin63xkt9pcjeb9joy"],
        "sernlund": ["be8mjm9jji8pmjbt3ss69pkqah"],
        "ntiemer": ["jtejg9fedj8xuerkyb11t31w5r", "aqjgbafyiire7e8yupuhho59pr", "us9j9aks3tde8gdmt9tqmig9ma"],
        "m25": ["adb5qhawy7rz9eetuo8gm1sepa", "bjy4ush8nbdtzydx6cu3pyhp6r", "jaanyrzxo7dn9ksy1cizf5psua", "un85pdmbjincdbox8njph76wta", "n4etuspw9injfm8xgy5yith5ky", "1oxyebttebgypmg1ord4fzie8w", "cxzjusbfjidoifeeiscy3em9fo", "8n6jhh6zgfnhzn7ycjxnkd5h4a", "r49jtxxq1pnxfn7qxocjmubitc", "9syd9fw1ztdupg84b5k5tcyjiy", "gwfbttf1g3bnzmwmfwqu4bz9oh", "awb8ix4p93y68fsr5wu5r83a4a", "tr8rqukynfyzjx4od3mc9m9ary", "repou6549jgifdh69dwmwz78tw", "9h7hxfjxq78a9xoarmnz4yxufe", "53yeemnkgbnf8gr9riiirxnguh", "paexm3yxx38yirg8s9isus8o5y", "g66p8zkxw78cdfhuramo3oykxo", "ynh8s1smzir1texpfkx55eqtqw", "86ucz4nbrfrgjybktqzhd3c9hh", "r4yn8gzenjf8dnwssnwbazjg5y", "m5hphb7z5byddy5wb77zfwsfyy", "y4pchh3mm7ybtyhc976jt5usia", "owbufgibnind7yuxn7az6qd4kr", "tj3kcak9pp83zk5k9atjf7kxmw", "ujuzmo7b8fd85nan4wmn3gbmey"],
        "sjsak": ["nfhra1s5sibgxk836r7867n1rc"],
        "ltrolin": ["ycphyuxsj3d6d8xo5uz7xuwyhe"],
        "ebbalo": ["ybqwcspu7t89bfffy99fg3mqzy"],
        "juliasve": ["irbhdrmn8ffyur18rjco96y51o", "9uyyceuuyinojpyggzfxmhopse", "9kyj5d6zb3b48nwwh3bwss4nde", "11cd83nentyp3kor9hh74ekmir", "ko53of6w1pypjka8bryeziztky"],
        "haggbr": ["c33ipzoebtrcmesu6unf1f6qnc"],
        "alvaah": ["pefh44t3gfncbnksm18wjkxnco", "itbe97pjs7fixku1d68hdqou4a"],
        "lukasgra": ["mookuy4unjncdf3uizq89jp43h", "8xaeukt1kjgitpchykoe4u5z6c"],
        "strende": ["xgcib99bmidr9yf9ksd3ghp9yh", "ryns9xr3m7diieogsjhqhps34o"],
        "aleung": ["o18eh6owdfgf5bsstxqg8q7bqe"],
        "emmiez": ["o8tq664egb83zr4b839th7sb1w", "5sydck8a4jrwdnw8ux3tzhcexo"],
        "chen9": ["sh9oktec8tb55yi4qkfh4c5cna", "7bdxahj38iyw5f9jzuc7dnpmza"],
        "albinwl": ["nowkmong8jny7eqzgqbi84yqzy", "8pym7p6pztfdjr7ss6681kmfpw", "jj1qwkim4bn7dkppc654f5anzy"],
        "armanas": ["7rm8dz5qbp8k3fge9msh3ta3xo"],
        "magdb": ["xpmqb8ox53byznu9ked9higefh"],
        "elbergst": ["meisaho9yin3zfo3nt3mfp6kxo", "i8tt7qo8g7n88bgoqtfxtgtnrh", "zntz86ne3fdzik498spudzcete"],
        "lwhalund": ["3smrsnrqoif6pmakg86gq5q1dy"],
        "hoti": ["nnot4xjexbft3gwobk6mi66u8r", "sut1i3arwirm9j9fryzb6j5s1h"],
        "jjl": ["p66ip4yo8b8afn6fyaj716jama"],
        "wbergst": ["635frd9kbp8wfk7k4gbgpqe86r"],
        "davpette": ["n533bbemb3np9p194k4er8xk8e"],
        "katjabo": ["qcjkc9fkwire9rqsxazuxhaqew", "dpqdpu3p5ty8jfjrxyw7y6h4xe"],
        "hugowr": ["r5e6d3m4o7na8xh5xqsyhmdpuc"],
        "samho": ["53wf9pdpbjyq3mkareu8ak4gxh", "o9an7rixmj8m9mdg4h97driwce"],
        "elliotc": ["i71asgrw13gtjjh644xr4rchmo"],
        "vmel": ["131r549ap3r5xybtxjiyzqpkwc"],
        "svastr": ["8jqrmtgxjfnkxrgg9zmib5s46r"],
        "casperbe": ["bm7uoop71frgzq4af5461jjktc"],
        "glek": ["qugmkdfncpgx7fm4bytoyf31ey"],
        "feeric": ["xqb8mgyy13y5mphxtpy9h9o1ar"],
        "jubr": ["tzk5tnq5p3r7f8u1kign4bidzy"]
        }

blacklisted_messages_2026 = {
        "m26": ["endiesjrw7fdj819z79fagiz8y", "cnd8ndyb1fdp9jfginmc5ywxgy", "93tudhtqsbg65nu86udcfgt3be", "nd63sj9ak38itrydtdhyu51fih", "mxajwum1opyrpx1is87atgd3wo", "3isdyftnci87dyjr5ptj6sfr1e", "m5hphb7z5byddy5wb77zfwsfyy", "y4pchh3mm7ybtyhc976jt5usia", "jgxkzsm5s3gpzqq5joor79f5oh", "bjy4ush8nbdtzydx6cu3pyhp6r", "un85pdmbjincdbox8njph76wta", "cdnj3gwuz7rqzc1pjop65dnokr", "peofb4wmxjr9xr9ix778jzns8y", "oj3qt6dfsjge5c8k4s18kkcj9a", "5zy8cfbdmifyd8w4xwaiiqc6hr", "sjuz89jioiny9n7is9znawgx1c", "k9p43bryhpfo3ptmx8cpdbfmxe", "1oxyebttebgypmg1ord4fzie8w", "fphrq68na3y87mq6dmxuugudzo", "8n6jhh6zgfnhzn7ycjxnkd5h4a", "jq3ggpudef8hfkh5a3xmoanqah", "rbefyjfmkpft7q7xq99uo6xbzr", "etf6cg1r7fbptfcnb1kb891o3y", "7g57q7wjipbpzfj5mt15rmxrxw", "55qisg8eyjbopnojjinudyfz6e", "9riiyhfzipbodep9ztfg8o98ky", "u17o9mc3uj8rxfcf5zqrse41hw", "pr6stppgt7g6mbm1gui7pz9ehy", "eawwpk3cjfnrdpbosgatkrh55r", "zp6wtadxyb8gbd3r4dqkog8dfo", "bjw7app14f8xdngzk1ckaa5xjh", "br5k7684zigr8kwes5o7r8im7a", "1f5xfibtyjy7z8c8as3huxbj3r", "adb5qhawy7rz9eetuo8gm1sepa", "jaanyrzxo7dn9ksy1cizf5psua", "r49jtxxq1pnxfn7qxocjmubitc", "9syd9fw1ztdupg84b5k5tcyjiy", "n4etuspw9injfm8xgy5yith5ky", "cxzjusbfjidoifeeiscy3em9fo", "gwfbttf1g3bnzmwmfwqu4bz9oh", "awb8ix4p93y68fsr5wu5r83a4a", "jsfdzkmbhf897ehaf7oprkjndw", "3isdyftnci87dyjr5ptj6sfr1e", "f9q3genb8i8y7gu4gzsr18ti9h", "5u5ztfnnrjgh5bt435rxxwtznc", "spgb79oaajg6jmmwu3ppe4g73e", "4ndd6eoqcff49fk6w6m1od1rha", "mxajwum1opyrpx1is87atgd3wo", "nd63sj9ak38itrydtdhyu51fih", "873d6b1ju3g3zmo64kfrf85gcc", "tmub1o6fwfbuxd1o6jy4wnyodh", "wk1maijer7r5tc5izxfjorxr8y", "ujuzmo7b8fd85nan4wmn3gbmey", "y4pchh3mm7ybtyhc976jt5usia", "8wfmk11idtge8rgstdb7dh9j4a", "owbufgibnind7yuxn7az6qd4kr", "m5hphb7z5byddy5wb77zfwsfyy", "tj3kcak9pp83zk5k9atjf7kxmw", "jgxkzsm5s3gpzqq5joor79f5oh", "93tudhtqsbg65nu86udcfgt3be", "cnd8ndyb1fdp9jfginmc5ywxgy", "adbdrnfsiidgtrcyie8baykgny", "r4yn8gzenjf8dnwssnwbazjg5y", "9h7hxfjxq78a9xoarmnz4yxufe", "dmhqqsamkfgifpgta444ixk9na", "abfibbotq3btbgsnpm5h9jhfuh", "repou6549jgifdh69dwmwz78tw", "86ucz4nbrfrgjybktqzhd3c9hh", "g66p8zkxw78cdfhuramo3oykxo", "tr8rqukynfyzjx4od3mc9m9ary", "paexm3yxx38yirg8s9isus8o5y", "ynh8s1smzir1texpfkx55eqtqw", "53yeemnkgbnf8gr9riiirxnguh", "endiesjrw7fdj819z79fagiz8y", "zt7i1914dbn1jd6f1zd51yhigw"],
        "zofialu": ["4n9iacng1bfkbms1b3dt4nox5c"],
        "wkraft": ["wbujesucjbrkdez41zumk8es5o", "55dnsedrjifftes7pogctxbgyy", "go4hkroiubfn8eraq91gz5u1fe", "bhme4znpzt8epkpj5tbkcx3umy", "ztxtaf43pjr77dan79kda9fyfa", "a4gawqensfnpmcyx1cce85u76h", "ihwcbx4z3bnr3cytjxn5rmqsgh", "wb8cge8qepfmbyuwcejy3gcuny", "dq5bamio57nkdbi9r4u4b4ujbc", "nsskh9gdq7fhpf5gbyszepqahr", "k193kfcdrff8dq97wbbh8iypiy", "5cpqieeimjgj9j4sftifztiq5e", "a9iwok7dofbspqcsctbpuqhxoa", "hug8nawrgbyffgs7rg64jff1ar", "q4wn99cymi8qzg5cs3wyh7pf9e", "7pgkkcxcmpgr5kuh3basci7fso", "x4o4yt1f9bgn7xcisbxgrqucuy"],
        "la5": ["3ttrbrzp8fd5pn689rdgwki4be"],
        "ojenner": ["iit6tjrputbpjgsrcb3y1wef1y", "8dad6t8nktdz8qrpnzkju7dn5y"],
        "ada.nobel": ["a33r3jn3mpg93dtytqy4xx1qmh", "9b9zbktagfrrikx7ordu3i5upy", "cjucg6grp3brxm6ybrwmybzhzw", "pdupejw6wfrs9grq9cjyxrdkty"],
        "ltrolin": ["czzrnqdumtbn3nwes7m44dawdy", "8d6gfhzpfjrp9jhm3fooyabyar", "krh3ycrb5bgiubj4hhscde7oqa"], "jubr": ["xa8gu7kgc7g5my3mqxjspjgwpc", "weepcwrqg7ns7rc99chb8tto6c", "sq5dprtxtjyaxd9taxgmqme3xr", "zkpuubk7qpf48mk33rksna8n3c", "iyrppsh4aigf8pfkfj5nmcsogy"],
        "mjoyce": ["hedkozar33dufm8sb3twzajt1r", "ukpixk5bj3b5ibs7q8eis11z7o", "xo77dqcfpjra9f49soo6t999mo", "g6roqyx9njrtifqh5ep1sgebhe", "3gujyzhwgpy19jx1e7fiynscwe", "xor3w663o78e88i6jx8ge4df5r"],
        "albinwl": ["7twexny6p78czdof6pi1eikg1r", "1sepmhce8jrn9y78utdg5zs3ta", "m4gzgbtbk7d9ig6ozwxdu6ztiw", "51jp4jwecfnpdppyaakhemii1y"],
        "akomarov": ["ewogn9os4pde388fb838fn6dkr", "f1oqbm3m13baipcy35g9ks9znw"],
        "mchristi": ["dp6dr98eitnfxbr75cs4q7fn7y"],
        "hchow": ["wcycc6wdhfrhikgw9ozdgj1y5w", "dwf9i4bodtfamqt7zi75ax7fow"],
        "juliasve": ["i6efdcrn4jy87q5uexkmg6s5ky", "11cd83nentyp3kor9hh74ekmir", "8yopk5nu9iye5mnh7tj71dtnty"],
        "alan.pascal": ["y5w87fr3dpf6mc577go5yyfq5h", "757861ax8tg8pgbffj9k4iq3da"],
        "kajsaeng": ["zndtna94jirqfnrtgjyia7hiwr", "oimgwi738fn5zmauis76irzwdr"],
        "fiek": ["c5xhs1a1w7nb5n81ejxiofcxbc"],
        "magdb": ["wq4nyzrbotn4ujn5omsbpbar4e"],
        "torlenn": ["e1y1jto5jb8t8x91o77ccugt1y"],
        "marie.lovelace": ["31oe5razkfyjde8o8f5bixip7o"],
        "martengf": ["ods79qpuxfghdxgcnc5ytnoiuw", "kc6ge5uhj78d5n8ktum6o6zkpa", "kii3nzucb3gjdypfpdmdsx5i7r"],
        "nkall": ["3qjka1oti3b5pemhtiodg5ayoh"],
        "nessimk": ["qeb8awamsjym5eks1ymzp4i6ac", "heuczcwdg3ro8k8pdy8kuuxsoc"],
        "repetto": ["saenrcaxofdhmdcp33mjteyz7h"],
        "lstal": ["numsetyp5j8iujuo8k7j8ghsxc"],
        "alainsw": ["kmmqcb1qopy1d8hbm7bcyih8ao"],
        "emmiez": ["o8tq664egb83zr4b839th7sb1w"],
        "ntiemer": ["okc9r43557f97dmo1e4oxtnyfr", "kx54fdjyztb3tczg7jtzn45sqr"],
        "jonng": ["koa6oghzdbnptj49n9pes6cxfe"],
        "elbergst": ["meisaho9yin3zfo3nt3mfp6kxo"],
        "damagnus": ["ouo9y37mw7y8td7geot6so4wby"],
        "adrkro": ["qugkjx48xidrzk69ruf5zi3xch"],
        "sernlund": ["7xob78chipbt8rfq6yo87bzz5w"]
        }

blacklisted_messages = {}

for year in [blacklisted_messages_2023_2024, blacklisted_messages_2025, blacklisted_messages_2026]:
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

