import json

base_dict = {"type": "", "amount": "", "comment": "", "safety": ""}

food_list_PL = ["""ZAKAZANE
Jabł, red
śliw, red
wiśni, red
wiśn, red
grusz, red
brzoskwi, red
morel, red
nektaryn, red
mang, red
arbuz, red
grejpfrut, red
daktyl, red
jeżyn, red
porzecz, red
rodzyn, red
w syropi, red
Suszon fasol, red
groch, red
soczewic, red
soj, red
sojow, red
izolat białk sojow, red
cebul, red
szalot, red
czosn, red
kapust, red
karczoch, red
kalafior, red
kukurydz, red
szparag, red
bób, red
bob, red
czerwo fasol, red
czar fasol, red
fasol, red
fasolnik, red
groch, red
soczewic, red
maślan, red
lod, red
pudding, red
Pszeniczn, red
mą, red
jęczmień, red
żyt, red
żytn, red
żytni, red
otręb, red
pistacj, red
grzyb, red
kur, red
kurk, red
maślak, red
borowik, red
koźlarz, red
rydz, red
miód, red
miod, red
syrop agaw, red
gum do żuci, red
rum, red
diet cok, red
inulin, red
salam, red
sos tysiąc wysp, red
kukurydz konserwo, red
ser koz, red
ser kozi, red""",
                """PRODUKTY MLECZNE
                Bit śmietan
                Masł
                margary, sprawdź dokładnie skład (węglodowany), yellow
                ol
                Mozzarell
                Fet
                bri
                camembert
                cheddar
                parmezan
                pecorin
                szwajcars
                gran padan
                padan
                koz pleśni
                ser pleśni
                ementaler
                gruyer
                cheddar
                radamer
                ser królews
                goud
                edams
                salam
                tylżyc
                mors
                podlas
                zamojs
                ser żółt
                żółt ser
                Ricott (do 40 g), orange
                haloum (max. 50 g), orange
                Twaróg (max. 30 g), orange
                twarog (max. 30 g), orange""",
                """SZTUCZNE
                Knorr, sprawdź dokładnie skład, orange
                Winiar, sprawdź dokładnie skład, orange
                Kamis, sprawdź dokładnie skład, orange
                Ram, sprawdź dokładnie skład, orange
                Ketchup, sprawdź dokładnie skład, orange
                keczup, sprawdź dokładnie skład, orange""",
                """ZASTĘPUJĄCE PRODUKTY MLECZNE
                Jogurt kokos
                Mle migdał
                Mle z orzech makadam
                Mle z quino
                Mle kokos (max. 120 g), yellow
                Mle owsia (125 g), yellow
                Mle ryżow (max. 250 ml), yellow
                Mle z konopi (max. 300 ml), yellow
                Wod kokos (100 g), orange""",
                """OWOCE
                Ananas
                Cytry
                Karambol
                Kiw
                Klementyn
                Limon
                Mandaryn
                Papaj
                Pomarańcz
                Rabarbar
                Smocz owoc
                Truskaw
                Winogro
                Winogron
                Banan, < 125g niedojrzałe | < 33g dojrzałe 33 g| suszone (<20 chips), orange
                Borów (< 60 g), yellow
                Jagod (< 60 g), yellow
                Jagód (< 60 g), yellow
                Melon honeydew (<135 g), yellow
                Melon kantalup (<160 g), yellow
                Malin (< 90 g), yellow
                Granat (max. 38 g), orange""",
                """NAPOJE
                Herbat czarn, słaba
                Herbat zielon
                Herbat biał
                Herbat miętow
                Sok pomidorow
                koncenrtat pomidor
                Sok warzywn, bez warzyw zabronionych
                Sok żurawinow
                Gin, yellow
                Piw, yellow
                Wódk, yellow
                Whisk, yellow
                Wi, yellow
                Kaw, yellow""",
                """ZIARNA i przetwory
                schär
                mą schär
                schaer
                mą schaer
                Kasz kukurydzia
                Kasz jagla
                kasz pęczak
                Kasz grycza niepalo (max. 27 g), ugotowana, orange
                Kasz bulgur (max. 44 g), ugotowana, orange
                Kasz owsia (< 120 g), yellow
                Mą jagla
                Mą ryżo
                Mą z quino
                Mą z komos ryżo
                Mą z sorgo
                Mą kukurydzia
                Mą orkiszow, przesiana
                Mą ziemniacza
                Mą grycza
                Mą owsia (< 60 g)
                Skrob z tapioki
                Skrob kukurydzia
                skrob ziemniacza
                skrob
                Quino
                komos ryżo
                Płat ryż
                Płat ryżow
                Płat quino
                Płat kukurydzia bezglutenow
                Płat kukurydzia (max 15g), orange
                Płat owsia błyskawicz (max 25g), orange
                Płat owsia górski (max. 50 g), yellow
                Płat owsia zwykł (max. 50 g), yellow
                płat owsia, bezglutenowe | górskie (max. 50 g) | zwykłe (max. 50 g), yellow
                Otręb owsia (<5 łyżek), yellow
                Otręb ryżow (< 60 g), yellow
                Otręb pszen (max. 5 g), orange
                Makaron vermicell
                Makaron orkiszow (max. 85 g), orange
                Makaron pszen (max. 74 g), orange
                Makaron jajecz (max. 40 g), orange
                Makaron pszen ugotowan (74 g), orange
                Makaron orkiszow ugotowan (74 g), orange
                Ryż
                Ryż ekspandowa (15 g), orange
                Wafl ryżow (max. 4), yellow
                Skiełkowa jęczmie
                Amarantus ekspandowa (10 g), orange
                Polent
                bagiet, red
                buł, red
                Pszen chleb pełnoziarnist, na zakwasie
                chleb pszen pełnoziarnist, na zakwasie
                chleb pełnoziarnist, pszenny na zakwasie
                Chleb 100% orkiszow zakwasi (<3 kromki), yellow
                Chleb orkiszow zakwasi (< 3 kromki), yellow
                Chleb orkiszow (< 3 kromki), na zakwasie, yellow
                Chleb bezglutenow bez skrobi pszennej (<3 kromki), yellow
                Chleb bezglutenow (<3 kromki), bez skrobi pszennej, yellow
                Chleb pszen biał zakwasi (2 kromki), yellow
                Chleb pszen biał (2 kromki), na zakwasie, yellow
                Chleb pszen (2 kromki), biały na zakwasie, yellow
                Tortill kukurydzia (< 6 tortilli), yellow
                Skiełkowa pszenic (max. 50 g), orange""",
                """WARZYWA
                Boćwin
                Cykori
                Chill, zielone | Chilli czerwone (< 50g)
                Chil, zielone | Chilli czerwone (< 50g)
                Dyni, zwykła
                Dyn, zwykła
                Dym, zielona część
                cebul dym, zielona część
                dym cebul, zielona część
                jarmuż
                jarmuz
                Kabacz
                Kalarep
                Kieł lucer
                Marchew
                marchw
                Ogór
                papry, czerwona
                Papry czerwo
                czerwo papry
                papryka, czerwona ok | zielona < 54g
                Pasternak
                Pietrusz
                Pomidor, zwykłe
                Rzodkiew
                Rukol
                Sałat radicchi
                Sałat masłow
                Sałat lodow
                Sałat
                Seler korzeniow
                Szczypior
                Wodorost, nori
                Nori, wodorosty
                Ziemnia
                Okr (< 100 g), yellow
                Piżmian jadalny (< 100 g), yellow
                Bakłażan (< 182 g), yellow
                Bok choy (< 160 g), yellow
                Brokuł (<270 g), kwiaty | łodyga < 45g | cały < 90g, yellow
                Bruk (<280 g), yellow
                Bruksel (<74 g), yellow
                Cukin (< 70 g), yellow
                Chill czerwon (< 50g), zielone ok
                Chil czerwon (< 50g), zielone ok
                Fasol szparagow zielo (< 125 g), yellow
                Fenkuł (<100 g), korzeń, yellow
                Kapust czerwo (<142 g), yellow
                Papry zielo (< 54 g)
                Pomidor z pusz (< 100 g), yellow
                Pomidor w puszce (< 100 g), yellow
                Pomidork koktajlow (<222 g), yellow
                Pomidor rzymsk (<250 g), yellow
                Rzep (< 100 g), yellow
                Rzodkiew daikon (<350 g), yellow
                Szpina (< 143 g), yellow
                Szpinak (< 143 g), yellow
                Kapust pekińs (<600 g), yellow
                Kapust biał (< 96 g), yellow
                Kapust bok choy (< 150 g), yellow
                Awokad (max. 20 g), orange
                Batat (max. 70 g), orange
                Burak (max. 20 g), orange
                Dyni piżmow (max. 30 g), orange
                Grosz cukr (max. 17 g), orange
                Kapust włos (max. 35 g), orange
                Kukurydz cukr (max. 43 g– 1⁄2 kolby), świeża, orange
                Kukurydz (max. 43 g– 1⁄2 kolby), świeża, orange
                Serc karczoch (max. 28 g), orange
                Seler naciow (max. 12 g), orange
                """,
                # Orzech, makadami: ok | arachidowe: ok | włoskie < 135 g | pekan < 100g | brazylijskie < 52 g | laskowe < 15 g | nerkowca: zakazane
                """ORZECHY I NASIONA
                Masł orzechow, z orzeszków ziemnych
                Mak
                Orzech makadam
                Orzech arachidow
                Orzech nerkowc, red
                Orzech brazylijsk (< 52 g), yellow
                Orzech laskow (max. 15 g), orange
                Orzech włoskich (< 135 g), yellow
                Orzech włosk (< 135 g), yellow
                Ch (< 48 g), yellow
                piniow (< 100g), yellow
                Kasztan jadaln (< 295 g), yellow
                Nasio dyn (< 100g), yellow
                Sezam (< 66 g), yellow
                Nasio słoneczni (< 70g), yellow
                ziar słoneczni (< 70g), yellow
                Masł migdałow (< 35 g), yellow
                Migdał (max 10), orange
                Mąk migdałow (max. 24 g), orange
                Siemi lnian (max. 30 g), orange
                Siemienia lnian (max. 30 g), orange
                Nasio kmin (max. 10 g), orange""",
                """ROśLINY STRĄCZKOWE
                Chan dal (46 g), ugotowana, yellow
                Uri dal (46 g), ugotowana, yellow
                Kieł fasol mung (< 200 g), yellow
                Ciecior z pusz (max. 42 g), dobrze wypłukana, orange
                Ciecior pusz (max. 42 g), dobrze wypłukana, orange
                Ciecior w puszce (max. 42 g), dobrze wypłukana, orange
                Soczewic z pusz (max. 46 g), dobrze wypłukana, orange
                Soczewic pusz (max. 46 g), dobrze wypłukana, orange
                Soczewic w puszc (max. 46 g), dobrze wypłukana, orange
                Soczewic gotowan (max. 23 g), orange""",
                """DO SŁODZENIA i SŁODYCZE
                Aspartam
                Sachary
                Syrop klon, bez syropu fruktozowo- kukurydzianego
                Syrop klonow, bez syropu fruktozowo- kukurydzianego
                Cukier
                erytrol
                erytrytol
                Cukr
                lukier
                lukr
                Stewi w prosz
                Galaretk malinow
                Galaretk truskawkow
                Galaretk limonkow
                Gorzk czekolad (<90 g), yellow
                Cukier kokos (max. 4 g), orange
                Czekolad mlecz (max. 15 g), orange
                Czekolad deser (max. 15 g), orange
                Czekolad desero (max. 15 g), orange
                deser czekolad (max. 15 g), orange
                mlecz Czekolad (max. 15 g), orange
                Czekolad biał (max. 15 g), orange
                biał Czekolad (max. 15 g), orange
                Melas (max. 5 g), orange""",
                """białko
                Indy
                bocz
                Jaj
                jajk
                Jagnięci
                Kurczak
                kurcza
                mięs drobiow
                Barani
                Ryb
                Łoso
                tuńczyk
                tuńczy
                dorsz
                łupacz
                pstrą̨g
                mintaj
                sol
                miru
                tołpyg
                krewet
                Małż
                ostryg
                omuł
                przegrzeb
                serców
                ślimak
                uchow
                trąbik
                pobrzeż
                Tof, twarde
                Wołowi
                st
                Wieprzowi
                szyn, sprawdź składniki, orange
                Tempeh (< 220 g), yellow
                mięs mielo
                mielon mięs
                mięs mielon
                mielo mięs
                mięso
                mieso
                mamalyga""",
                """PRZETWORY
                Buracz marynowa
                Kapar
                Ogór marynowa, w occie
                Korniszo
                Oliw
                oliwek, czarne | zielone
                oliwki, czarne | zielone
                Min kukurydz, w puszce
                Pę̨d bambus, z puszki
                Dżem truskawkow
                Past vegemite
                Pieczar w puszce (< 200 g), yellow
                Pieczar (< 200 g), w puszce, yellow
                Pieczar z pusz (< 200 g), yellow
                Zielo grosz w puszc (max. 42 g), orange
                Zielo grosz (max. 42 g), puszka, orange
                Suszo borowik (max. 10 g), orange
                suszo grzyby shiitake (max. 7 g), orange
                grzyb shiitake (max. 7 g), suszone, orange
                Dżem z pigw (max. 13 g), orange
                past z pigw (max. 13 g), orange""",
                """ZIOŁA I PRZYPRAWY.
                Anyż gwiaździsty
                Kurkum
                Curr
                Pieprz czar
                Pieprz
                liść laur
                liśc laur
                sól
                sol
                Wanili esencj
                Esencj wanili
                Wanilia strącz
                strączk wanili
                Asafetyd
                Nasion gorczyc
                Szafran
                Chill w prosz
                Kardamon
                Cynamon
                Goździk
                Kmin rzyms
                Nasion kopr włoski
                Koper włos
                Nasion kozieradk
                Kozierad
                Papry w prosz
                Słodk papry
                ostr papry
                Przypraw pięć smaków
                Kolendr nasio
                Gał muszkatołow
                Bazyli śwież
                śwież bazyli
                Estragon świeży
                Imbir korzeń
                korzeń imbir
                Kolendr śwież
                śwież kolendr
                Liśc curr, świeże
                Liśc kozieradk świeże
                Liśc limonk 
                Mięt śwież
                śwież Mięt
                Nać pietrusz świeża
                nat pietrusz
                Pandan liści
                Rozmaryn śwież
                śwież Rozmaryn
                Rukiew wodn
                Szałwi śwież
                Traw cytrynow
                Tymian śwież
                śwież Tymian
                koper
                tymian
                orega
                bazyl""",
                """INNE
                bezglutenow
                low fodmap
                bulion, zależnie od składu, orange
                przypraw korzen
                przypraw d pierni
                sod oczyszczo
                wod
                Ocet czerwon
                Ocet biał
                Ocet jabłkow
                Ocet ryżow
                Ocet słodow
                oct
                Ocet Balsamicz (< 21 g), yellow
                Oct Balsamicz (< 21 g), yellow
                Agar agar
                Olej
                Past mis
                Past krewetkow
                wasab
                Wasab prosz
                Wasab past
                past wasab
                Sos rybn
                Imbir, świeży
                Past z tamaryndowc
                Wodorost nor
                Musztard
                Majonez
                Sos Worcestershire
                Sos sojow
                Esencj waniliow
                Drożdż nieaktywn, płatki
                Drożdż, suche
                Sos ostrygow (< 20 g), yellow
                Past z tamaryndowc (< 3 łyżki), yellow
                Kaka (< 20g), yellow
                Chrzan (< 90 g), yellow
                Glon wakam (max. 5 g), płatki, orange
                Past tahin (max. 20 g), orange
                wiór kokos (max. 18 g), orange
                Suszo żurawi (max. 13 g), orange
                żurawi (max. 13 g), suszona, orange
                Suszo pomidor (2 sztuki), orange
                Pest (10 g), orange
                Kost bulionow (max. 2 g), orange
                bulionet (max. 2 g), orange""",
                """ZAMIENNIKI
                makaron, bez glutenu, blue
                chleb, bez glutenu, blue
                buł, bez glutenu, blue
                ciabatt, bez glutentu, blue
                chleb tost, bez glutenu, blue
                buł tart, bez glutenu, blue
                tost, bez glutenu, blue
                mle, bez laktozy, blue
                jogurt, bez laktozy | z koziego mleka, blue
                śmieta, bez laktozy, blue
                Ser wiejs, bez laktozy
                tortill (< 6 placków), kukurydziana,
                prosz d pieczen, bezglutenowy, blue
                cukier wanilinow, bezglutenowy, blue
                croissant, bez glutenu, blue""",
                ]


food_list_ENG = ["""FORBIDDEN
apple, red
plum, red
cheer, red
pear, red
peach, red
apricot, red
nectarine, red
mango, red
watermelon, red
grapefruit, red
dactyl, red
blackberr, red
currant, red
raisin, red
sultana, red
in syrup, red
Dried Beans, red
pea, red
lentil, red
so, red
protein isolate, red
onion, red
shallot, red
garlic, red
cabbage, red
artichoke, red
cauliflower, red
corn, red
asparagus, red
broad bean, red
Red bean, red
black bean, red
bean, red
black eyed peas, red
buttermilk, red
ice cream, red
pudding, red
wheat, red
flour, red
barle, red
rye, red
bran, red
pistachio, red
mushroom, red
hone, red
agave syrup, red
chewing gum, red
rum, red
diet coke, red
inulin, red
salami, red
Thousand Island dressing, red
canned corn, red
goat cheese, red""",
                 """DIARY
                 Whipped cream
                 butter
                 margarine, sprawdź dokładnie skład (węglodowany), yellow
                 oil
                 Mozzarella
                 feta
                 brie
                 camembert
                 cheddar
                 parmezan
                 pecorin
                 Swis cheese
                 grana padano
                 blue goat cheese
                 blue cheese
                 ementaler
                 gruyer
                 cheddar
                 radamer
                 royal cheese
                 gouda
                 edam
                 cheese
                 Ricotta (do 40 g), orange
                 haloumi (max. 50 g), orange
                 Cottage cheese (max. 30 g), orange""",
                 """ARTIFICIAL
                 Knorr, check ingredients, orange""",
                 """ DIARY SUBSTITUTES
                 Coconut Yogurt
                 Almond milk
                 Macadam nut milk
                 quinoa milk
                 cocomut milk (max. 120 g), yellow
                 Oat milk (125 g), yellow
                 rice milk (max. 250 ml), yellow
                 Hemp milk (max. 300 ml), yellow
                 coconut water (100 g), orange""",
                 """FRUITS
                 pineapple
                 lemon
                 Kiw
                 clementine
                 lime
                 Mandarin
                 tangerine
                 Papaya
                 orange
                 Rhubarb
                 Dragon fruit
                 strawberr
                 grape
                 Banana, < 125g green | < 33g mature 33 g| dried (<20 chips), orange
                 bilberr (< 60 g), yellow
                 blueberr (< 60 g), yellow
                 honeydew Melon (<135 g), yellow
                 Cantaloupe melon (<160 g), yellow
                 Raspberr (< 90 g), yellow
                 pomegranate (max. 38 g), orange""",
                 """NAPOJE
                 black tea, week
                 green tea
                 white tea
                 mint tea
                 Tomato Juice
                 Vegetable juice, bez warzyw zabronionych
                 Cranberr Juice
                 Gin, yellow
                 Beer, yellow
                 Vodka, yellow
                 Whisk, yellow
                 Wine, yellow
                 Coffee, yellow""",
                 """ZIARNA i przetwory
                 schär
                 schaer
                 Corn groats
                 millet
                 pearl barle
                 Buckwheat not roasted (max. 27 g), ugotowana, orange
                 Buckwheat  (max. 27 g),, not roasted, orange
                 Bulgur (max. 44 g), ugotowana, orange
                 Porridge (< 120 g), yellow
                 Millet flour
                 rice flour
                 quinoa flour
                 sorghum flour
                 corn flour
                 Spelt flour, sifted
                 Potato flour
                 buckwheat flour
                 oat flour (< 60 g)
                 gluten-free flour
                 gluten free flour
                 glutenfree flour
                 gluten free
                 gluten-free
                 glutenfree
                 low fodmap
                 Tapioca starch
                 corn starch
                 potato starch
                 starch
                 Quinoa
                 Rice Flake
                 quinoa flake
                 Gluten-free cornflake
                 corn flake (max 15g), orange
                 Instant oat flake (max 25g), orange
                 oat flake (max. 50 g), yellow
                 Oat bran (<5 łyżek), yellow
                 oat, instant oat flakes (max 25g) | oat flakes (max. 50 g), orange
                 Rice bran (< 60 g), yellow
                 wheat bran (max. 5 g), orange
                 Vermicelli pasta
                 Spelled pasta (max. 85 g), orange
                 wheat pasta (max. 74 g), orange
                 Egg noodl (max. 40 g), orange
                 pasta cooked (74 g), orange
                 rice
                 Expanded rice (15 g), orange
                 Rice waffle (max. 4), yellow
                 Sprouted barley
                 Expanded Amaranth (10 g), orange
                 Polenta
                 baguet, red
                 bun, red
                 roll, red
                 Whole grain wheat bread sourdough
                 Whole grain wheat bread, sourdough
                 sourdough spelt bread, <3 slices, yellow
                 white bread (2 slices), sourdough, yellow
                 corn tortilla (< 6 tortillas), yellow
                 Sprouted wheat (max. 50 g), orange""",
                 """WARZYWA
                 chard
                 Chicor
                 Chilli, green | Chilli red (< 50g)
                 pumpkin
                 spring onion
                 kale
                 Cucurbit
                 Kohlrabi
                 Alfalfa sprout
                 carrot
                 cucumber
                 red paprika
                 red pepper
                 paprika, red ok | green < 54g | powder ok, yellow
                 Parsnip
                 Parsle
                 tomato
                 Radish
                 Rocket
                 Radicchio Lettuce
                 Butterhead lettuce
                 Iceberg Lettuce
                 lettuce
                 Root celer
                 celer root
                 Chive
                 Seaweed, nori
                 Nori, Seaweed
                 Potato
                 Okra (< 100 g), yellow
                 Eggplant (< 182 g), yellow
                 Bok cho (< 160 g), yellow
                 Broccoli (<270 g), kwiaty | łodyga < 45g | cały < 90g, yellow
                 Brussel sprout (<74 g), yellow
                 Courgette (< 70 g), yellow
                 zucchini (< 70 g), yellow
                 Chill red (< 50g), green ok
                 Green bean (< 125 g), yellow
                 fennel (<100 g), root, yellow
                 Red cabbage (<142 g), yellow
                 Green pepper (< 54 g)
                 Green paprika (< 54 g)
                 Canned tomato (< 100 g), yellow
                 Roman tomato (<250 g), yellow
                 turnip (< 100 g), yellow
                 Daikon radish (<350 g), yellow
                 spinach (< 143 g), yellow
                 Chinese cabbage (<600 g), yellow
                 white cabbage (< 96 g), yellow
                 bok choy cabbage (< 150 g), yellow
                 avocado (max. 20 g), orange
                 Sweet potato (max. 70 g), orange
                 Beetroot (max. 20 g), orange
                 Butternut squash (max. 30 g), orange
                 Sugar pea (max. 17 g), orange
                 Sweetcorn (max. 43 g– 1⁄2 kolby), świeża, orange
                 Corn (max. 43 g– 1⁄2 kolby), świeża, orange
                 Artichoke heart (max. 28 g), orange
                 celer (max. 12 g), orange""",
                 """NUTS AND SEEDS
                 Peanut butter
                 popp seed
                 Macadamia nut
                 Peanut
                 Cashew nut, red
                 Brazil Walnut (< 52 g), yellow
                 Brazilian Walnut (< 52 g), yellow
                 Hazelnut (max. 15 g), orange
                 Walnut (< 135 g), yellow
                 Chia (< 48 g), yellow
                 Pine nut (< 100g), yellow
                 Chestnut (< 295 g), yellow
                 Pumpkin seed (< 100g), yellow
                 Sesame (< 66 g), yellow
                 Sunflower seed (< 70g), yellow
                 Almond Butter (< 35 g), yellow
                 Almond (max 10), orange
                 Almond flour (max. 24 g), orange
                 Linseed (max. 30 g), orange
                 Cumin Seed (max. 10 g), orange""",
                 """LEGUMES
                 Chana dal (46 g), ugotowana, yellow
                 Uri dal (46 g), ugotowana, yellow
                 Mung bean sprout (< 200 g), yellow
                 Canned chickpea (max. 42 g), dobrze wypłukana, orange
                 canned lentil (max. 46 g), dobrze wypłukana, orange
                 cooked lentil (max. 23 g), orange
                 lentil (max. 23 g), cooked, orange""",
                 """SWEETS
                 Aspartame
                 Saccharin
                 Maple Syrup, without corn fructose syrup
                 sugar
                 erytrol
                 erytrytol
                 frosting
                 Stevia powder
                 stevia
                 Raspberr jell
                 Strawberr jell
                 Lime jell
                 coconut sugar (max. 4 g), orange
                 dark chocolate (<90 g), yellow
                 milk chocolate (max. 15 g), orange
                 white chocolate (max. 15 g), orange
                 Molass (max. 5 g), orange""",
                 """PROTEIN
                 Turkey
                 bacon
                 egg
                 Lamb
                 Chicken
                 poultry meat
                 Mutton
                 fish
                 salmon
                 tuna
                 cod
                 haddock
                 trout
                 pollock
                 sole
                 hoki
                 silver carp
                 prawn
                 Clam
                 oyster
                 mussel
                 scallop
                 cockle
                 snail
                 conch
                 Tofu, hard
                 Beef
                 steak
                 Pork
                 ham, check the ingredients, orange
                 Tempeh (<220 g), yellow """,
                 """PROCESSED
                 Marinated beetroot
                 Caper
                 Pickled cucumber, in vinegar
                 Pickle, in vinegar
                 Gherkin
                 Olive
                 olive, black green
                 olive, black green
                 Mini corn, canned
                 Bamboo shoot, canned
                 Strawberr jam
                 Vegemite paste
                 Canned mushroom (<200 g), yellow
                 Green canned pea (max. 42 g), orange
                 Dried boletu  (max. 10 g), orange
                 dried shiitake mushroom (max. 7 g), orange
                 Shiitake Mushroom (max. 7 g), dried, orange
                 Quince jam (max. 13 g), orange
                 quince paste (max. 13 g), orange """,
                 """ HERBS AND SPICES.
                 Star Anise
                 Turmeric
                 Curr
                 Black pepper
                 Pepper
                 Ba leaf
                 salt
                 Vanilla essence
                 Vanilla pods
                 asafoetida
                 Mustard Seeds
                 Saffron
                 Chilli in powder
                 Cardamom
                 Cinnamon
                 Carnation
                 Roman cumin
                 Fennel seeds
                 Fennel
                 Fenugreek seeds
                 Fenugreek
                 Pepper in powder
                 Sweet pepper
                 Sweet paprika
                 hot pepper
                 hot paprika
                 Five flavor spice
                 Coriander Seeds
                 Nutmeg
                 Fresh basil
                 Tarragon fresh
                 Ginger root
                 Fresh coriander
                 Fresh curr leaves
                 Fresh fenugreek leaves
                 Lime leaf
                 Lime leaves
                 Fresh mint
                 Fresh parsley
                 Pandan leaves
                 Fresh rosemary
                 Watercress
                 Fresh sage
                 Lemongrass
                 Fresh thyme
                 dill
                 thyme
                 oregano
                 basil
                 marjoram""",
                 """OTHER
                 coleslaw, depending on ingredients, orange
                 broth, depending on ingredients, orange
                 root spice
                 spice to the breast
                 baking soda
                 water
                 Red vinegar
                 White vinegar
                 Apple vinegar
                 Rice vinegar
                 Malt vinegar
                 cider vinegar
                 Balsamic vinegar (<21 g), yellow
                 Oct Balsamic (<21 g), yellow
                 Agar agar
                 Oil
                 Love paste
                 Shrimp paste
                 wasabi
                 Wasabi please
                 Wasabi past
                 wasabi paste
                 Fish sauce
                 Ginger, fresh
                 Tamarind paste
                 Seaweed
                 Mustard
                 Mayonnaise
                 Worcestershire sauce
                 So sauce
                 Vanilla essence
                 Inactive yeast, flakes
                 Yeast, dry
                 Oyster sauce (<20 g), yellow
                 Tamarind paste (<3 tablespoons), yellow
                 Cocoa (<20g), yellow
                 Horseradish (<90 g), yellow
                 Tahini paste (max. 20 g), orange
                 Coconut flake (max. 18 g), Orange
                 Dried cranberr (max. 13 g), orange
                 Cranberr (max. 13 g), dried, orange
                 Dried tomato (2 pieces), orange
                 Pesto (10 g), orange
                 Bouillon cube (max. 2 g), orange""",
                 """SUBSTITUTES
                 flour, gluten free, blue
                 pasta, gluten free, blue
                 bread, gluten free, blue
                 roll, gluten free, blue
                 ciabatta, gluten free, blue
                 toast bread, gluten free, blue
                 Bread crumbs, gluten free, blue
                 toast, gluten free, blue
                 milk, lactose free, blue
                 yogurt, lactose free made of goat's milk, blue
                 cream, lactose free, blue
                 Cottage cheese, lactose free
                 tortilla (<6 slices), corn,
                 baking powder, gluten-free, blue
                 vanilla, gluten-free, blue sugar
                 Croissant, gluten free, blue""",
                 ]


def prepare_food_dict_list(food_list):
    food_dict = {}
    for group in food_list:
        lines_list = group.split('\n')
        type = lines_list[0]
        lines_list = lines_list[1:]
        for line in lines_list:
            safety = 'green'
            comment = ''
            if ',' in line:
                # check if there's both safety and a comment
                try:
                    safety, comment, line = line.split(', ')[2],line.split(', ')[1],line.split(', ')[0]
                except IndexError:
                    # if only safety
                    if 'yellow' in line.split(', ')[1] or 'orange' in line.split(', ')[1] or  'red' in line.split(', ')[1] or  'blue' in line.split(', ')[1]:
                        safety, comment, line = line.split(', ')[1], comment,line.split(', ')[0]
                    else:
                        # if only comment
                        safety, comment, line = safety, line.split(', ')[1], line.split(', ')[0]
            # if max safe amount is given
            if '(' in line:
                name = line.split('(')[0].lower().strip()
                item_dict = dict(zip(base_dict.keys(), [type.lower(), line.split(' (')[1].split(')')[0].lower(), comment.lower(), safety.lower()]))
            else:
                name = line.lower().strip()
                item_dict = dict(zip(base_dict.keys(), [type.lower(), '', comment.lower(), safety.lower()]))
            food_dict[name] = item_dict
    return food_dict

food_dict_PL = prepare_food_dict_list(food_list_PL)
food_dict_ENG = prepare_food_dict_list(food_list_ENG)

with open('../../analyzer/static/json/lowfodmap_foods_PL.json', 'w') as file:
    json.dump(food_dict_PL, file)

with open('../../analyzer/static/json/lowfodmap_foods_ENG.json', 'w') as file:
    json.dump(food_dict_ENG, file)
