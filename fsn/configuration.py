TEAM_ID = "419spm3ugf8axc8chupqw9e5bo"
REACTION_POST_ID = "1yhfpko63tdbdpn4uuq6149ger"

COURSE_CHANNELS = {
        "dd1301-datorintroduktion": "hbm5srxnetyruf7ai47ek4mcee",
        "dd1328-grundlaggande-datalogi-for-tekniska-berakningar": "y49dgxa1zj898e3k3sm6t1zj5o",
        "dd1331-grundlaggande-programmering-ctfys": "3u7pyhnoit8nmfyfi8547h7gyr",
        "dd1331-grundlaggande-programmering-ctmat": "apd8b38pqfghibkjybmaw5dtgo",
        "sa1006-ingenjorsfardigheter-i-teknisk-matematik": "xcnpi31kcbym7bz16aykin8hco",
        "sf0003-introduktion-till-matematik": "yki8m7iaabgqid7uhzm31tkadh",
        "sf1550-numeriska-metoder-grundkurs": "7j5sqceikbgbd8ehamqf4ah9sc",
        "sf1672-linjar-algebra": "n6ku3cousfrp7ktf98g41xfkre",
        "sf1673-analys-i-en-variabel": "d4mpop743pyz5pz1xjufsoh5uo",
        "sf1674-flervariabelanalys": "x6514n3atty8xyb4qfab6qaoih",
        "sf1918-sannolikhetsteori-och-statistik": "t9gyr98sb3nsifz8si8q1t1pyc",
        "sf1922-sannolikhetsteori-och-statistik": "ogkcefx6bibs9p18gxwyuryfke",
        "sg1112-mekanik-i": "5k7nduixdtg8jrojw695d46sda",
        "sg1115-partikeldynamik-med-projekt": "7gxgpuawjig1ux7j4dbp3ikacy",
        "si1121-termodynamik": "3zriggjketf7pxstwtkh86jbwy",
        "sk1104-klassik-fysik": "fjet8pqxw7dr3fo537npy5urke",
        "sk1105-experimentell-fysik": "6xzhjat9pfg8my67nxu7ccfb7o"
        }

CHANNELS = {
        "välkommen-till-fsn": "8tyspqdmyifsmg9wj9zitfeb4c",
        "random": "q77s98iqkjbsfknafm8zcoft6r",
        "general": "wuuw5rnkpjykfedsbk99hghjpe",
        **COURSE_CHANNELS
        }

CATEGORIES = {
        "Kurser": [*COURSE_CHANNELS],
        "Channels": ["välkommen-till-fsn", "random", "general"]
        }

CHANNEL_GROUPS = {
        "CTMAT-f0": {
            "dd1301-datorintroduktion",
            "dd1331-grundlaggande-programmering-ctmat",
            "sf1673-analys-i-en-variabel",
            "sa1006-ingenjorsfardigheter-i-teknisk-matematik"
            },
        "CTFYS-f0": {
            "dd1301-datorintroduktion",
            "sf1673-analys-i-en-variabel",
            "dd1331-grundlaggande-programmering-ctfys",
            "si1121-termodynamik"
            }
        }
