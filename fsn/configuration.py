TEAM_ID = "419spm3ugf8axc8chupqw9e5bo"
REACTION_POST_ID = "1yhfpko63tdbdpn4uuq6149ger"

COURSE_CHANNELS = {
        "dd1301-datorintroduktion": "hbm5srxnetyruf7ai47ek4mcee",
        "dd1327-grundlaggande-datalogi": "7jmo6p41highuct9x5g78e5s8w",
        "dd1328-grundlaggande-datalogi-for-tekniska-berakningar": "y49dgxa1zj898e3k3sm6t1zj5o",
        "dd1331-grundlaggande-programmering-ctfys": "3u7pyhnoit8nmfyfi8547h7gyr",
        "dd1331-grundlaggande-programmering-ctmat": "apd8b38pqfghibkjybmaw5dtgo",
        "dd1380-javaprogrammering-for-pythonprogrammerare": "5tguoe57j78ezbmwdocpdfbb5r",
        "dd1385-programutvecklingsteknik": "zt537fhzhff6upoyu7z34zkjmy",
        "ei1320-teoretisk-elektroteknik": "dw1cp3w74i8rzqctqz13kmr3oe",
        "el1000-reglerteknik-allman-kurs": "rorgkxc7opynuj69drcizbyxya",
        "sa1006-ingenjorsfardigheter-i-teknisk-matematik": "xcnpi31kcbym7bz16aykin8hco",
        "se1055-hallfasthetslara-grundkurs-med-energimetoder": "ozj8agkb7ibgxgg8z8dbexm67h",
        "sf0003-introduktion-till-matematik": "yki8m7iaabgqid7uhzm31tkadh",
        "sf1544-numeriska-metoder-grundkurs-iv": "7k6pi7pegfyqjrdi6ss9fhe4hy",
        "sf1550-numeriska-metoder-grundkurs": "7j5sqceikbgbd8ehamqf4ah9sc",
        "sf1672-linjar-algebra": "n6ku3cousfrp7ktf98g41xfkre",
        "sf1673-analys-i-en-variabel": "d4mpop743pyz5pz1xjufsoh5uo",
        "sf1674-flervariabelanalys": "x6514n3atty8xyb4qfab6qaoih",
        "sf1679-diskret-matematik": "e1tah7yggpgc9cr9m7gebkb4ic",
        "sf1680-seminariekurs-i-grundlaggande-matematik": "gtiw4qhnd7bmdjbqjunn157y8a",
        "sf1681-linjar-algebra-fortsattningskurs": "jkm8ceomgtr8zr9xrsg1jwoc4a",
        "sf1683-differentialekvationer-och-transformmetoder": "uk4ijk763bffdg1zdor5sfd4uo",
        "sf1692-analytiska-och-numeriska-metoder-for-ode": "f6uhh8qnufrujqsrfxq9zrymca",
        "sf1693-analytiska-och-numeriska-metoder-for-pde-och-transformer": "ujagpxc69tdcdr6pm9ecx5tgzo",
        "sf1811-optimeringslara": "uswwmh51o7btpjhaak8epyb33y",
        "sf1918-sannolikhetsteori-och-statistik": "t9gyr98sb3nsifz8si8q1t1pyc",
        "sf1922-sannolikhetsteori-och-statistik": "ogkcefx6bibs9p18gxwyuryfke",
        "sf1930-statistisk-inlarning-och-dataanalys": "8gmt3jcwsbynffbak6nd6zn9mc",
        "sg1112-mekanik-i": "5k7nduixdtg8jrojw695d46sda",
        "sg1113-mekanik-fortsattningskurs": "hhngowhfkfy53nwieuecy7t3oa",
        "sg1115-partikeldynamik-med-projekt": "7gxgpuawjig1ux7j4dbp3ikacy",
        "sg1218-stromningsmekanik": "dufn4qok5bg35rjgewsp6ytzba",
        "sh1014-modern-fysik": "ddbjd3j1xb88fdx7ohznt65d9r",
        "sh1015-tillampad-modern-fysik": "z5egajm4g7ndmd1kr5qbb9io8h",
        "sh1017-fysik-for-teknisk-matematik": "7c139c8tki857rypan9hd4gj5c",
        "si1121-termodynamik": "3zriggjketf7pxstwtkh86jbwy",
        "si1146-vektoranalys": "en95t8wpff8f7y5xadwd5rt6nw",
        "si1155-teoretisk-fysik": "98gam63hcbgbfj45f6urozmppe",
        "si1200-fysikens-matematiska-metoder": "wyxjpsa99tnojn5bpbjskgjqze",
        "si1336-simulering-och-modellering": "rxsw8mcueirimxfeoitbpexhxe",
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
            "sf1918-sannolikhetsteori-och-statistik",
            "sf1672-linjar-algebra",
            "sa1006-ingenjorsfardigheter-i-teknisk-matematik"
            },
        "CTFYS-f0": {
            "sf1672-linjar-algebra",
            "sk1104-klassik-fysik",
            "dd1331-grundlaggande-programmering-ctfys"
            },
        "CTMAT-f22": {
            "sf1693-analytiska-och-numeriska-metoder-for-pde-och-transformer",
            "dd1385-programutvecklingsteknik",
            "sf1681-linjar-algebra-fortsattningskurs"
            },
        "CTFYS-f22": {
            "sf1681-linjar-algebra-fortsattningskurs",
            "sf1683-differentialekvationer-och-transformmetoder",
            "sh1014-modern-fysik",
            "sf1544-numeriska-metoder-grundkurs-iv"
            }
        }
