TEAM_ID = "419spm3ugf8axc8chupqw9e5bo"
REACTION_POST_ID = "1yhfpko63tdbdpn4uuq6149ger"

COURSE_CHANNELS = {
        "dd1301_datorintroduktion": "hbm5srxnetyruf7ai47ek4mcee",
        "dd1327_grundlaggande_datalogi": "7jmo6p41highuct9x5g78e5s8w",
        "dd1328_grundlaggande_datalogi_for_tekniska_berakningar": "y49dgxa1zj898e3k3sm6t1zj5o",
        "dd1331_grundlaggande_programmering_ctfys": "3u7pyhnoit8nmfyfi8547h7gyr",
        "dd1331_grundlaggande_programmering_ctmat": "apd8b38pqfghibkjybmaw5dtgo",
        "dd1380_javaprogrammering_for_pythonprogrammerare": "5tguoe57j78ezbmwdocpdfbb5r",
        "dd1385_programutvecklingsteknik": "zt537fhzhff6upoyu7z34zkjmy",
        "ei1320_teoretisk_elektroteknik": "dw1cp3w74i8rzqctqz13kmr3oe",
        "el1000_reglerteknik_allman_kurs": "rorgkxc7opynuj69drcizbyxya",
        "sa1006_ingenjorsfardigheter_i_teknisk_matematik": "xcnpi31kcbym7bz16aykin8hco",
        "se1055_hallfasthetslara_grundkurs_med_energimetoder": "ozj8agkb7ibgxgg8z8dbexm67h",
        "sf0003_introduktion_till_matematik": "yki8m7iaabgqid7uhzm31tkadh",
        "sf1544_numeriska_metoder_grundkurs_iv": "7k6pi7pegfyqjrdi6ss9fhe4hy",
        "sf1550_numeriska_metoder_grundkurs": "7j5sqceikbgbd8ehamqf4ah9sc",
        "sf1672_linjar_algebra": "n6ku3cousfrp7ktf98g41xfkre",
        "sf1673_analys_i_en_variabel": "d4mpop743pyz5pz1xjufsoh5uo",
        "sf1674_flervariabelanalys": "x6514n3atty8xyb4qfab6qaoih",
        "sf1679_diskret_matematik": "e1tah7yggpgc9cr9m7gebkb4ic",
        "sf1680_seminariekurs_i_grundlaggande_matematik": "gtiw4qhnd7bmdjbqjunn157y8a",
        "sf1681_linjar_algebra_fortsattningskurs": "jkm8ceomgtr8zr9xrsg1jwoc4a",
        "sf1683_differentialekvationer_och_transformmetoder": "uk4ijk763bffdg1zdor5sfd4uo",
        "sf1692_analytiska_och_numeriska_metoder_for_ode": "f6uhh8qnufrujqsrfxq9zrymca",
        "sf1693_analytiska_och_numeriska_metoder_for_pde_och_transformer": "ujagpxc69tdcdr6pm9ecx5tgzo",
        "sf1811_optimeringslara": "uswwmh51o7btpjhaak8epyb33y",
        "sf1918_sannolikhetsteori_och_statistik": "t9gyr98sb3nsifz8si8q1t1pyc",
        "sf1922_sannolikhetsteori_och_statistik": "ogkcefx6bibs9p18gxwyuryfke",
        "sf1930_statistisk_inlarning_och_dataanalys": "8gmt3jcwsbynffbak6nd6zn9mc",
        "sg1112_mekanik_i": "5k7nduixdtg8jrojw695d46sda",
        "sg1113_mekanik_fortsattningskurs": "hhngowhfkfy53nwieuecy7t3oa",
        "sg1115_partikeldynamik_med_projekt": "7gxgpuawjig1ux7j4dbp3ikacy",
        "sg1218_stromningsmekanik": "dufn4qok5bg35rjgewsp6ytzba",
        "sh1014_modern_fysik": "ddbjd3j1xb88fdx7ohznt65d9r",
        "sh1015_tillampad_modern_fysik": "z5egajm4g7ndmd1kr5qbb9io8h",
        "sh1017_fysik_for_teknisk_matematik": "7c139c8tki857rypan9hd4gj5c",
        "si1121_termodynamik": "3zriggjketf7pxstwtkh86jbwy",
        "si1146_vektoranalys": "en95t8wpff8f7y5xadwd5rt6nw",
        "si1155_teoretisk_fysik": "98gam63hcbgbfj45f6urozmppe",
        "si1200_fysikens_matematiska_metoder": "wyxjpsa99tnojn5bpbjskgjqze",
        "si1336_simulering_och_modellering": "rxsw8mcueirimxfeoitbpexhxe",
        "sk1104_klassik_fysik": "fjet8pqxw7dr3fo537npy5urke",
        "sk1105_experimentell_fysik": "6xzhjat9pfg8my67nxu7ccfb7o"
        }

CHANNELS = {
        "välkommen_till_fsn": "8tyspqdmyifsmg9wj9zitfeb4c",
        "random": "q77s98iqkjbsfknafm8zcoft6r",
        "general": "wuuw5rnkpjykfedsbk99hghjpe",
        **COURSE_CHANNELS
        }

DEFAULT_CHANNELS = {
        "välkommen_till_fsn": "8tyspqdmyifsmg9wj9zitfeb4c",
        "random": "q77s98iqkjbsfknafm8zcoft6r",
        "general": "wuuw5rnkpjykfedsbk99hghjpe"
        }

CATEGORIES = {
        "Kurser": [*COURSE_CHANNELS],
        "Channels": ["välkommen_till_fsn", "random", "general"]
        }

CHANNEL_GROUPS = {
        "CTMAT-f23": {
            "sf1674_flervariabelanalys",
            "dd1328_grundlaggande_datalogi_for_tekniska_berakningar",
            "sf1550_numeriska_metoder_grundkurs"
            },
        "CTFYS-f23": {
            "sk1104_klassik_fysik",
            "sf1674_flervariabelanalys",
            "sg1112_mekanik_i"
            },
        "CTMAT-f22": {
            "sf1693_analytiska_och_numeriska_metoder_for_pde_och_transformer",
            "sf1679_diskret_matematik"
            },
        "CTFYS-f22": {
            "sf1544_numeriska_metoder_grundkurs_iv",
            "si1200_fysikens_matematiska_metoder",
            "se1055_hallfasthetslara_grundkurs_med_energimetoder"
            }
        }
