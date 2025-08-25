namnd_teams = [
    "funktionarer",
    "fkm",
    "fcap",
    "jamn",
    "fan",
    "fsn",
    "fysikalen",
    "fysiksektionen",
    "fcom",
    "fint",
    "frum",
    "fn",
    "fusion"
]

fohsare = [
    {
        "from": "cwewz5kw1jdkzxi7z1cqfhof5e", # Överföhs
        "to": "eir39sx3ijftirjh3dwt9zhixa" # Marie Lovelace
    },
    {
        "from": "fixxox8xyjb9dm8cffikeitgew", # Stilföhs
        "to": "bb3w4jeg3jfe9k7fwg16k3tesr" # Ada Nobel
    },
    {
        "from": "adt5q1g55i8dbnorfmdmp367dy", # Taktikföhs
        "to": "yosrf6oys7nnupwcgeuzixatnw" # Alan Pascal
    }
]

teams_str = ", ".join(f"'{team}'" for team in namnd_teams)

print("---- TRANSFORM FROM FÖHS TO FAKE ACCOUNTS ----")
for fohs in fohsare:
    SQL_QUERY = f"""
    UPDATE posts
    SET userid = '{fohs['to']}'
    WHERE id IN (
        SELECT p.id
        FROM posts p
        JOIN channels c ON p.channelid = c.id
        JOIN teams t ON c.teamid = t.id
        WHERE
            p.userid = '{fohs['from']}' AND
            c.type = 'O' AND
            p.deleteat = 0 AND
            t.deleteat = 0 AND
            t.name IN ({teams_str})
    );
    """
    print(SQL_QUERY)

print("---- TRANSFORM BACK ----")
for fohs in fohsare:
    SQL_QUERY = f"""
    UPDATE posts
    SET userid='{fohs['from']}'
    WHERE userid='{fohs['to']}';
    """

"""
Överföhs
             id
----------------------------
 1r15neoeh3dt3rh46ow58xm4pa
 9d13dgugftn1mc31k33nxxyowy
 f655jscemidzxq6qjofirjb78h
 4y7iiq1qm7gyfx3srnpyjpikfc
 p1u3mpp5eb88ic5o14ynsimush
 z84gcqbeppnbfme5q5u9d7aahy
 fmjzkwop73nujnzgxph7ijckhc
 ofr36mkh5tr7pk88d6965h7k1o
 sqt1bwhcridmfyhdqtynyr1ddc
 r36kb4uxafnzzf4chypg396dbh
 qfxqxiiw938gmxssn7q5ifryxh
 q457geb8gjf59piem3pr9f4t8y
 mxb77dqpg3dy9pgqkhekfqkitr
 dtt8fe58k78e5qdcrsawjspx4o
 y978ket7dfg97ehcmeqbpxhf8o
 xornfc6fyfbg3p73fumhhu4s5h
 sqc3ff1o6f8jfre3os83wrq98e
 ctcymhxwu3fbbxz6rwjestg17y
 uo9sygcj67frbqm9smh73zr8wo
 jpkj6uxg7pg9ff6q4spqmhtabc
 sr5aba99tiyepjm5q98ropndfc


Stilföhs
            id
----------------------------
 oojy3hcgkpbf5e73moqa35z9mw
 zrtkkohm5bnrmpkou4foz4te4h
 sg58pwaqyirwdmbt8mfaqbmn1h
 3cj1fuqitbn15dhspkdzggr3oo
 qff6oe8d1bdkbkq4ana4f1ng4o
 184jgfhhupdapcsf6iiytncqcr
 s4gfqnoiwty15nfs9zkmmhes4o
 689z5mhwbjbhbf41aoq1487mxr
 m8byzqxyiprs38ie8ssa19ttxr
 aigaebinq3r5jjehs4jk7dhgie
 q5pyrjkscpfd5fn11snhjo5pth
 rqiynmqfqtr55bkbgyzpqi7cje
 kp8kc6s1f7g43bq94pom6bn6pc
 o3k5pb9fpi85udxjtd7chre8ca
 rutnzhf7pf8ez8totdbtw5nfkw
 r5pfx3yfr7fatb1ipbq8cwpkee
 xyrqihoaubbfzeqmd9dfp9yw5r
 4o7haqeba3gg3kxogf96x67zuc
 ihjqe48j57n8zmmg5cmmorhnac
 jicdi45j3jn9fm6nycfc9dbnnc
 4fr5ah9z73b4tkgq5xa7spssbr
 me38agaumjf68g3uyf7dquem6y
 caji44imgfyc9njeqchyy9thpc
 9fmdqiu15idt98iwsqj6yuwdqh
 jw7ebwk9ki85iyo5naokprg9go
 tw1d7zdq53dsfymgxicjapi6py
 4guhhbdfgbfx7puc4wkhcg7wdr
 ofn57brgbfnyznj1kfzjqwtrho
 mfs4g5nnwbfixyu41utycd3p7a
 4u7cajj7atdytr3kp3uztyzgmh
 9aqt994683n19jh3i47da7983h
 zhqcsn8q7pyaunduefftmtwxch
 stehu9brq7yu78pubxg7ojxqer
 9j5rbuu38pg13f6rfd5xiibxca
 g9uxmoibdjf1unysnxfskiq41e
 wi986uhd67ybin8qtpeag7jg6y
 negz8dza6385fq15epitn9a7ac
 hyi5zgr94pbaze5uef6tgy31yy
 k9iwtsiari8ubxidfbcn69n1zr
 zzyx6h88pjn35p5fq96r6t3wjr
 xf56uizd9frumkf5zzg6p44bqh
 tehxhnfom3dcum8sufgj51w1sc
 amxjtsw6478f9cd8rgue8g4kch
 th6eejkncinktp4ae3ne76kz1e
 o6aprcqb3tg1de8uarf9bnj48o
 4zn4pq61k7f858pxa4dqtbw94y
 kyyfbdobg3ngzg86i1c36hi9mh
 imikoqzdkfrtbp5j8dk9fquuyr
 ba58b7ayi7ntuy1w3bwowoojnh
 qyhy6uoeqjr1jd6rtskfshjonh
 hm9w7fq5dfyk7me646gzb5dnse
 eb4kei5twtbobf7kazipgizgqr
 r756h3hn87gf8cc44pbj6grhfc
 764bg6qjxibiddznbrg81cc1ia
 kmmico1yb78tfcy6gfa1pz4iky
 fthjon6tzfnrbdpadc7ird5g1h
 am9rjg13f7gcbqiyw5g4j658jc
 g3bbt1s9sinc8nz8c5tj18xrmc
 7rj8iddhipf8ffajmskdc5qhkh
 dngunb3e87yf3rdfsfbfud6mmh
 uenzi59tjbg7pp3d1qjzhh7mmh
 edaaxhwzjfr7urd9ugugg1t95r
 dgja861xc3ncmda9st4jw5tguo
 jj59gtwkh7nou89poph93esaew
 kqternaoqjfc9eyzcfzcf8s86a
 bzc4m7ggipyx5kngxqqhq45z7o
 sp7n8u9pi3bd3m499e6a1bthda
 ietgh7xczpdj5n8pwo5yh8jukr
 hmuq5gxccpy7brkgu4nd6gi1ec
 tjrcg5gej3n79byfqbg13qnrsa
 qmonzzfqz7rcukbsauy957re6y
 1k7zjjw6mpf1u8un3sqicyyk4a
 7cpbbndgqjgn9cs97193sc39na
 xgctffrhf7gxmrospy43ahkd7o
 rgc4ja7csbbixpihso1am4gkah
 px35wefdw7biudtoqs8834wp4o
 sacainjd4ifqmmnf11txrghujy
 s4me9883opniddq8zpps1ij5cr
 qznu8hw9qty1zydm5npxft4qda
 bsmgiq83wpg43e77iupjoppopy
 1qwk4k9oajr9fnn9kb6pxwmzgr
 obeotj5q4tycm89ot9aynthtge
 f75i4j146jyuxea5xiyxboa1so
 6kgcskbw7brwbebngu4if5pxgw
 x8cswawmkp8hfd5xkczxo7zpoc
 y6z755z7t7d7xru3dnwop6fo9r
 qz6pwbx6nbr6dg6meuu6cmaxay
 ft1buka47tf8pm3yzmsn8ad4ka
 m1k1njz1kibdtbskncqyb73o1r
 456yzzwwh3gt78a1f37ek8uhra
 u6timzkj7jypudufp4cwxftzee
 du8f5mqx1tgqteh4qu9rfscsre
 59xbd7eqqjff8rcay9wfd5s8cy
 igz4cz4ksbrwtk6sdedmc8cd7h
 h1ywtk5g8frk7nzxdnjpoufetc

Taktikföhs
             id
----------------------------
 sfq6qmn4cfbx5q57wck6xjspia
 dqc8gamartf6byx9rcf7grw5wc
 7ofdf7wsrifm8x9n39jcerenge
 jpg8o96r9ibr8ntnc77ugkemzo
 xkwhj7ks1frfdqf3r3zy66faqa
 7f6dhdqn5pfajk7nmzgrfb6phr
 kazoq4xz5jraxq7ifw1o91qupw
 xs8qdqi54jf4d8bhyn8jpe3g9c
 cuanidb95pdnpjjxpfpn6di8na
 n9yn8paciifwpgjfrgb6pjn7ka
 c3y8jrehojrt8fhb18t6g9kjbw
 hz77e44eubnx7khe9qpwmogx6a
 ybqwcspu7t89bfffy99fg3mqzy
 7ks914ok6tnb7dwd85ro8rwaqw
 5gd6cf7at7bnubo56aybenyddo
 8qaoypq89jrp5exde8wf73ghay
 gsw1bsz3dfye8pib977afnjhre
"""