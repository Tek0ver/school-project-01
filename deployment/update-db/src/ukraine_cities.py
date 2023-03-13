import re


ukraine_cities = """Almazna (oblast de Louhansk)  
    Alouchta (Crimée)  
    Aloupka (Crimée)  
    Altchevsk (oblast de Louhansk)  
    Amvrossiïvka (oblast de Donetsk)  
    Ananiv (oblast d'Odessa)  
    Androuchivka (oblast de Jytomyr)  
    Antratsyt (oblast de Louhansk)  
    Apostolove (oblast de Dnipropetrovsk)  
    Armiansk (Crimée)  
    Artsyz (oblast d'Odessa)  
    Avdiïvka (oblast de Donetsk)  
    Bachtanka (oblast de Mykolaïv)  
    Bakhmatch (oblast de Tchernihiv)  
    Bakhmout (oblast de Donetsk)  
    Bakhtchyssaraï (Crimée)  
    Balakliia (oblast de Kharkiv)  
    Balta (oblast d'Odessa)  
    Bar (oblast de Vinnytsia)  
    Baranivka (oblast de Jytomyr)  
    Barvinkove (oblast de Kharkiv)  
    Batouryn (oblast de Tchernihiv)  
    Belz (oblast de Lviv)  
    Berchad (oblast de Vinnytsia)  
    Berdiansk (oblast de Zaporijjia)  
    Berdytchiv (oblast de Jytomyr)  
    Berehove (oblast de Transcarpatie)  
    Berejany (oblast de Ternopil)  
    Berestetchko (oblast de Volhynie)  
    Berezan (oblast de Kiev)  
    Berezivka (oblast d'Odessa)  
    Berezne (oblast de Rivne)  
    Beryslav (oblast de Kherson)  
    Bibrka (oblast de Lviv)  
    Bila Tserkva (oblast de Kiev)  
    Bilhorod-Dnistrovskyï (oblast d'Odessa)  
    Biliaïvka (oblast d'Odessa)  
    Bilohirsk (Crimée)  
    Bilopillia (oblast de Soumy)  
    Bilozerske (oblast de Donetsk)  
    Bilytske (oblast de Donetsk)  
    Blahovichtchenske (oblast de Kirovohrad)  
    Bobrovytsia (oblast de Tchernihiv)  
    Bobrynets (oblast de Kirovohrad)  
    Bohodoukhiv (oblast de Kharkiv)  
    Bohouslav (oblast de Kiev)  
    Boïarka (oblast de Kiev)  
    Bokovo Khroustalne (oblast de Louhansk)  
    Bolekhiv (oblast d'Ivano-Frankivsk)  
    Bolhrad (oblast d'Odessa)  
    Borchtchiv (oblast de Ternopil)  
    Boryslav (oblast de Lviv)  
    Boryspil (oblast de Kiev)  
    Borzna (oblast de Tchernihiv)  
    Bounhe (oblast de Donetsk)  
    Bourchtyn (oblast d'Ivano-Frankivsk)  
    Bouryn (oblast de Soumy)  
    Bousk (oblast de Lviv)  
    Boutcha (oblast de Kiev)  
    Boutchatch (oblast de Ternopil)  
    Brianka (oblast de Louhansk)  
    Brody (oblast de Lviv)  
    Brovary (oblast de Kiev)  
    Chakhtarsk (oblast de Donetsk)  
    Charhorod (oblast de Vinnytsia)  
    Chepetivka (oblast de Khmelnytskyï)  
    Chostka (oblast de Soumy)  
    Choumsk (oblast de Ternopil)  
    Chpola (oblast de Tcherkassy)  
    Chtchastia (oblast de Louhansk)  
    Chtcholkine (Crimée)  
    Debaltseve (oblast de Donetsk)  
    Derajnia (oblast de Khmelnytskyï)  
    Derhatchi (oblast de Kharkiv)  
    Djankoï (Crimée)  
    Dnipro (oblast de Dnipropetrovsk)  
    Dniproroudne (oblast de Zaporijjia)  
    Dobromyl (oblast de Lviv)  
    Dobropillia (oblast de Donetsk)  
    Dokoutchaïevsk (oblast de Donetsk)  
    Dolyna (oblast d'Ivano-Frankivsk)  
    Dolynska (oblast de Kirovohrad)  
    Donetsk (oblast de Donetsk)  
    Doubliany (oblast de Lviv)  
    Doubno (oblast de Rivne)  
    Doubrovytsia (oblast de Rivne)  
    Dounaïvtsi (oblast de Khmelnytskyï)  
    Dovjansk (oblast de Louhansk)  
    Drohobytch (oblast de Lviv)  
    Droujba (oblast de Soumy)  
    Droujkivka (oblast de Donetsk)  
    Enerhodar (oblast de Zaporijjia)  
    Eupatoria (Crimée)  
    Fastiv (oblast de Kiev)  
    Feodossia (Crimée)  
    Hadiatch (oblast de Poltava)  
    Haïssyn (oblast de Vinnytsia)  
    Haïvoron (oblast de Kirovohrad)  
    Halytch (oblast d'Ivano-Frankivsk)  
    Henitchesk (oblast de Kherson)  
    Hertsa (oblast de Tchernivtsi)  
    Hirnyk (oblast de Donetsk)  
    Hirske (oblast de Louhansk)  
    Hlobyne (oblast de Poltava)  
    Hloukhiv (oblast de Soumy)  
    Hlyniany (oblast de Lviv)  
    Hnivan (oblast de Vinnytsia)  
    Hola Prystan (oblast de Kherson)  
    Holoubivka (oblast de Louhansk)  
    Holovanivsk (oblast de Kirovohrad)  
    Horichni Plavni (oblast de Poltava)  
    Horlivka (oblast de Donetsk)  
    Horodenka (oblast d'Ivano-Frankivsk)  
    Horodnia (oblast de Tchernihiv)  
    Horodok (oblast de Khmelnytskyï)  
    Horodok (oblast de Lviv)  
    Horodychtche (oblast de Tcherkassy)  
    Horokhiv (oblast de Volhynie)  
    Houliaïpole (oblast de Zaporijjia)  
    Hrebinka (oblast de Poltava)  
    Ienakiieve (oblast de Donetsk)  
    Illintsi (oblast de Vinnytsia)  
    Ilovaïsk (oblast de Donetsk)  
    Inkerman (Sébastopol)  
    Irchava (oblast de Transcarpatie)  
    Irmino (oblast de Louhansk)  
    Irpin (oblast de Kiev)  
    Itchnia (oblast de Tchernihiv)  
    Ivano-Frankivsk (oblast d'Ivano-Frankivsk)  
    Iziaslav (oblast de Khmelnytskyï)  
    Izioum (oblast de Kharkiv)  
    Izmaïl (oblast d'Odessa)  
    Jachkiv (oblast de Tcherkassy)  
    Jdanivka (oblast de Donetsk)  
    Jmerynka (oblast de Vinnytsia)  
    Jovkva (oblast de Lviv)  
    Jovti Vody (oblast de Dnipropetrovsk)  
    Jydatchiv (oblast de Lviv)  
    Jytomyr (oblast de Jytomyr)  
    Kadiïvka (oblast de Louhansk)  
    Kaharlyk (oblast de Kiev)  
    Kakhovka (oblast de Kherson)  
    Kalmiouske (oblast de Donetsk)  
    Kalouch (oblast d'Ivano-Frankivsk)  
    Kalynivka (oblast de Vinnytsia)  
    Kamianets-Podilskyï (oblast de Khmelnytskyï)  
    Kamianka (oblast de Tcherkassy)  
    Kamianka-Bouzka (oblast de Lviv)  
    Kamianka-Dniprovska (oblast de Zaporijjia)  
    Kamianske (oblast de Dnipropetrovsk)  
    Kamin-Kachyrskyï (oblast de Volhynie)  
    Kaniv (oblast de Tcherkassy)  
    Karlivka (oblast de Poltava)  
    Kertch (Crimée)  
    Kharkiv (oblast de Kharkiv)  
    Khartsyzk (oblast de Donetsk)  
    Kherson (oblast de Kherson)  
    Khmelnytskyï (oblast de Khmelnytskyï)  
    Khmilnyk (oblast de Vinnytsia)  
    Khodoriv (oblast de Lviv)  
    Khorol (oblast de Poltava)  
    Khorostkiv (oblast de Ternopil)  
    Khotyn (oblast de Tchernivtsi)  
    Khoust (oblast de Transcarpatie)  
    Khrestivka (oblast de Donetsk)  
    Khroustalny (oblast de Louhansk)  
    Khrystynivka (oblast de Tcherkassy)  
    Khyriv (oblast de Lviv)  
    Kiev (Kiev)  
    Kilia (oblast d'Odessa)  
    Kitsman (oblast de Tchernivtsi)  
    Kivertsi (oblast de Volhynie)  
    Kobeliaky (oblast de Poltava)  
    Kodyma (oblast d'Odessa)  
    Kolomya (oblast d'Ivano-Frankivsk)  
    Komarno (oblast de Lviv)  
    Konotop (oblast de Soumy)  
    Kopytchyntsi (oblast de Ternopil)  
    Korets (oblast de Rivne)  
    Korioukivka (oblast de Tchernihiv)  
    Korosten (oblast de Jytomyr)  
    Korostychiv (oblast de Jytomyr)  
    Korsoun-Chevtchenkivskyï (oblast de Tcherkassy)  
    Kossiv (oblast d'Ivano-Frankivsk)  
    Kostiantynivka (oblast de Donetsk)  
    Kostopil (oblast de Rivne)  
    Koupiansk (oblast de Kharkiv)  
    Kourakhove (oblast de Donetsk)  
    Kovel (oblast de Volhynie)  
    Koziatyn (oblast de Vinnytsia)  
    Kramatorsk (oblast de Donetsk)  
    Krasnohorivka (oblast de Donetsk)  
    Krasnohrad (oblast de Kharkiv)  
    Krasnoperekopsk (Crimée)  
    Krassyliv (oblast de Khmelnytskyï)  
    Krementchouk (oblast de Poltava)  
    Kremenets (oblast de Ternopil)  
    Kreminna (oblast de Louhansk)  
    Krolevets (oblast de Soumy)  
    Kropyvnytskyï (oblast de Kirovohrad)  
    Kryvy Rih (oblast de Dnipropetrovsk)  
    Kypoutche (oblast de Louhansk)  
    Ladyjyn (oblast de Vinnytsia)  
    Lanivtsi (oblast de Ternopil)  
    Lebedyn (oblast de Soumy)  
    Liouboml (oblast de Volhynie)  
    Lioubotyn (oblast de Kharkiv)  
    Lokhvytsia (oblast de Poltava)  
    Loubny (oblast de Poltava)  
    Louhansk (oblast de Louhansk)  
    Loutouhyne (oblast de Louhansk)  
    Loutsk (oblast de Volhynie)  
    Lozova (oblast de Kharkiv)  
    Lviv (oblast de Lviv)  
    Lyman (oblast de Donetsk)  
    Lypovets (oblast de Vinnytsia)  
    Lyssytchansk (oblast de Louhansk)  
    Makiïvka (oblast de Donetsk)  
    Mala Vyska (oblast de Kirovohrad)  
    Malyn (oblast de Jytomyr)  
    Marhanets (oblast de Dnipropetrovsk)  
    Marïnka (oblast de Donetsk)  
    Marioupol (oblast de Donetsk)  
    Melitopol (oblast de Zaporijjia)  
    Milove (oblast de Louhansk)  
    Mena (oblast de Tchernihiv)  
    Merefa (oblast de Kharkiv)  
    Mioussynsk (oblast de Louhansk)  
    Mochtchena (oblast de Volhynie)  
    Mohyliv-Podilskyï (oblast de Vinnytsia)  
    Molodohvardiisk (oblast de Louhansk)  
    Molotchansk (oblast de Zaporijjia)  
    Monastyrychtche (oblast de Tcherkassy)  
    Monastyryska (oblast de Ternopil)  
    Morchyn (oblast de Lviv)  
    Mospyne (oblast de Donetsk)  
    Mostyska (oblast de Lviv)  
    Moukatcheve (oblast de Transcarpatie)  
    Mykhaïlivka  (oblast de Louhansk)  
    Mykhaïlivka  (oblast de Zaporijjia)  
    Mykolaïv (oblast de Lviv)  
    Mykolaïv (oblast de Mykolaïv)  
    Mykolaïvka (oblast de Donetsk)  
    Myrhorod (oblast de Poltava)  
    Myrnohrad (oblast de Donetsk)  
    Myronivka (oblast de Kiev)  
    Nadvirna (oblast d'Ivano-Frankivsk)  
    Nemyriv (oblast de Vinnytsia)  
    Netichyn (oblast de Khmelnytskyï)  
    Nijyn (oblast de Tchernihiv)  
    Nikopol (oblast de Dnipropetrovsk)  
    Nossivka (oblast de Tchernihiv)  
    Nova Kakhovka (oblast de Kherson)  
    Nova Odessa (oblast de Mykolaïv)  
    Novhorod-Siverskyï (oblast de Tchernihiv)  
    Novoaïdar (oblast de Louhansk)  
    Novoazovsk (oblast de Donetsk)  
    Novodnistrovsk (oblast de Tchernivtsi)  
    Novodroujesk (oblast de Louhansk)  
    Novohrad-Volynskyï (oblast de Jytomyr)  
    Novohrodivka (oblast de Donetsk)  
    Novoïavorivsk (oblast de Lviv)  
    Novomoskovsk (oblast de Dnipropetrovsk)  
    Novomyrhorod (oblast de Kirovohrad)  
    Novooukraïnka (oblast de Kirovohrad)  
    Novosselytsia (oblast de Tchernivtsi)  
    Novovolynsk (oblast de Volhynie)  
    Novyï Bouh (oblast de Mykolaïv)  
    Novyï Kalyniv (oblast de Lviv)  
    Novyï Rozdil (oblast de Lviv)  
    Oboukhiv (oblast de Kiev)  
    Odessa (oblast d'Odessa)  
    Okhtyrka (oblast de Soumy)  
    Olechky (oblast de Kherson)  
    Oleksandria (oblast de Kirovohrad)  
    Oleksandrivsk (oblast de Louhansk)  
    Olevsk (oblast de Jytomyr)  
    Orikhiv (oblast de Zaporijjia)  
    Oster (oblast de Tchernihiv)  
    Ostroh (oblast de Rivne)  
    Otchakiv (oblast de Mykolaïv)  
    Ouhniv (oblast de Lviv)  
    Oujhorod (oblast de Transcarpatie)  
    Oukraïnka (oblast de Kiev)  
    Oukraïnsk (oblast de Donetsk)  
    Ouman (oblast de Tcherkassy)  
    Oustylouh (oblast de Volhynie)  
    Ouzyn (oblast de Kiev)  
    Ovidiopol (oblast d'Odessa)  
    Ovroutch (oblast de Jytomyr)  
    Pavlohrad (oblast de Dnipropetrovsk)  
    Perchotravensk (oblast de Dnipropetrovsk)  
    Perechtchepyne (oblast de Dnipropetrovsk)  
    Pereiaslav (oblast de Kiev)  
    Peremychliany (oblast de Lviv)  
    Peretchyn (oblast de Transcarpatie)  
    Perevalsk (oblast de Louhansk)  
    Pervomaïsk (oblast de Louhansk)  
    Pervomaïsk (oblast de Mykolaïv)  
    Pervomaïskyï (oblast de Kharkiv)  
    Petrovo Krasnosillia (oblast de Louhansk)  
    Piatykhatky (oblast de Dnipropetrovsk)  
    Pidhaïtsi (oblast de Ternopil)  
    Pidhorodne (oblast de Dnipropetrovsk)  
    Pivdenne (oblast de Kharkiv)  
    Podilsk (oblast d'Odessa)  
    Pohrebychtche (oblast de Vinnytsia)  
    Pokrov (oblast de Dnipropetrovsk)  
    Pokrovsk (oblast de Donetsk)  
    Polohy (oblast de Zaporijjia)  
    Polonne (oblast de Khmelnytskyï)  
    Poltava (oblast de Poltava)  
    Pomitchna (oblast de Kirovohrad)  
    Popasna (oblast de Louhansk)  
    Potchaïv (oblast de Ternopil)  
    Poustomyty (oblast de Lviv)  
    Poutyvl (oblast de Soumy)  
    Prylouky (oblast de Tchernihiv)  
    Prymorsk (oblast de Zaporijjia)  
    Prypiat (oblast de Kiev)  
    Pryvillia (oblast de Louhansk)  
    Pyriatyn (oblast de Poltava)  
    Radekhiv (oblast de Lviv)  
    Radomychl (oblast de Jytomyr)  
    Radyvyliv (oblast de Rivne)  
    Rakhiv (oblast de Transcarpatie)  
    Rava-Rouska (oblast de Lviv)  
    Reni (oblast d'Odessa)  
    Rivne (oblast de Rivne)  
    Rjychtchiv (oblast de Kiev)  
    Rodynske (oblast de Donetsk)  
    Rohatyn (oblast d'Ivano-Frankivsk)  
    Rojychtche (oblast de Volhynie)  
    Romny (oblast de Soumy)  
    Roubijne (oblast de Louhansk)  
    Roudky (oblast de Lviv)  
    Rovenky (oblast de Louhansk)  
    Rozdilna (oblast d'Odessa)  
    Saky (Crimée)  
    Sambir (oblast de Lviv)  
    Sarny (oblast de Rivne)  
    Sébastopol (Sébastopol)  
    Selydove (oblast de Donetsk)  
    Semenivka (oblast de Tchernihiv)  
    Seredyna-Bouda (oblast de Soumy)  
    Sievierodonetsk (oblast de Louhansk)  
    Simferopol (Crimée)  
    Siversk (oblast de Donetsk)  
    Skadovsk (oblast de Kherson)  
    Skalat (oblast de Ternopil)  
    Skole (oblast de Lviv)  
    Skvyra (oblast de Kiev)  
    Slavouta (oblast de Khmelnytskyï)  
    Slavoutytch (oblast de Kiev)  
    Slovianoserbsk (oblast de Louhansk)  
    Sloviansk (oblast de Donetsk)  
    Smila (oblast de Tcherkassy)  
    Sniatyn (oblast d'Ivano-Frankivsk)  
    Snihourivka (oblast de Mykolaïv)  
    Snijne (oblast de Donetsk)  
    Snovsk (oblast de Tchernihiv)  
    Sokal (oblast de Lviv)  
    Sokyriany (oblast de Tchernivtsi)  
    Soledar (oblast de Donetsk)  
    Sorokyne (oblast de Louhansk)  
    Sosnivka (oblast de Lviv)  
    Soudak (Crimée)  
    Soudova Vychnia (oblast de Lviv)  
    Soukhodilsk (oblast de Louhansk)  
    Soumy (oblast de Soumy)  
    Starobilsk (oblast de Louhansk)  
    Starokostiantyniv (oblast de Khmelnytskyï)  
    Staryï Krym (Crimée)  
    Staryï Sambir (oblast de Lviv)  
    Stebnyk (oblast de Lviv)  
    Storojynets (oblast de Tchernivtsi)  
    Stry (oblast de Lviv)  
    Svaliava (oblast de Transcarpatie)  
    Svatove (oblast de Louhansk)  
    Sviatohirsk (oblast de Donetsk)  
    Svitlodarsk (oblast de Donetsk)  
    Svitlovodsk (oblast de Kirovohrad)  
    Synelnykove (oblast de Dnipropetrovsk)  
    Talne (oblast de Tcherkassy)  
    Tarachtcha (oblast de Kiev)  
    Tatarbounary (oblast d'Odessa)  
    Tavriisk (oblast de Kherson)  
    Tchassiv Yar (oblast de Donetsk)  
    Tcherkassy (oblast de Tcherkassy)  
    Tchernihiv (oblast de Tchernihiv)  
    Tchernivtsi (oblast de Tchernivtsi)  
    Tchervonohrad (oblast de Lviv)  
    Tchop (oblast de Transcarpatie)  
    Tchornobyl (oblast de Kiev)  
    Tchornomorsk (oblast d'Odessa)  
    Tchortkiv (oblast de Ternopil)  
    Tchouhouïv (oblast de Kharkiv)  
    Tchyhyryne (oblast de Tcherkassy)  
    Tchystiakove (oblast de Donetsk)  
    Teplodar (oblast d'Odessa)  
    Terebovlia (oblast de Ternopil)  
    Ternivka (oblast de Dnipropetrovsk)  
    Ternopil (oblast de Ternopil)  
    Tetiïv (oblast de Kiev)  
    Tiatchiv (oblast de Transcarpatie)  
    Tloumatch (oblast d'Ivano-Frankivsk)  
    Tokmak (oblast de Zaporijjia)  
    Toretsk (oblast de Donetsk)  
    Toultchyn (oblast de Vinnytsia)  
    Tourka (oblast de Lviv)  
    Trostianets (oblast de Soumy)  
    Trouskavets (oblast de Lviv)  
    Tysmenytsia (oblast d'Ivano-Frankivsk)  
    Vachkivtsi (oblast de Tchernivtsi)  
    Valky (oblast de Kharkiv)  
    Varach (oblast de Rivne)  
    Vassylivka (oblast de Zaporijjia)  
    Vassylkiv (oblast de Kiev)  
    Vatoutine (oblast de Tcherkassy)  
    Velyki Mosty (oblast de Lviv)  
    Verkhivtseve (oblast de Dnipropetrovsk)  
    Verkhnodniprovsk (oblast de Dnipropetrovsk)  
    Vilniansk (oblast de Zaporijjia)  
    Vilnohirsk (oblast de Dnipropetrovsk)  
    Vinnytsia (oblast de Vinnytsia)  
    Volnovakha (oblast de Donetsk)  
    Volodymyr-Volynskyï (oblast de Volhynie)  
    Volotchysk (oblast de Khmelnytskyï)  
    Vorojba (oblast de Soumy)  
    Vouhledar (oblast de Donetsk)  
    Vouhlehirsk (oblast de Donetsk)  
    Vovtchansk (oblast de Kharkiv)  
    Voznesenivka (oblast de Louhansk)  
    Voznessensk (oblast de Mykolaïv)  
    Vychhorod (oblast de Kiev)  
    Vychneve (oblast de Kiev)  
    Vyjnytsia (oblast de Tchernivtsi)  
    Vylkove (oblast d'Odessa)  
    Vynnyky (oblast de Lviv)  
    Vynohradiv (oblast de Transcarpatie)  
    Yahotyn (oblast de Kiev)  
    Yalta (Crimée)  
    Yampil (oblast de Vinnytsia)  
    Yaremtche (oblast d'Ivano-Frankivsk)  
    Yassynouvata (oblast de Donetsk)  
    Yavoriv (oblast de Lviv)  
    Youjne (oblast d'Odessa)  
    Youjnooukraïnsk (oblast de Mykolaïv)  
    Zalichtchyky (oblast de Ternopil)  
    Zalizne (oblast de Donetsk)  
    Zaporijjia (oblast de Zaporijjia)  
    Zastavna (oblast de Tchernivtsi)  
    Zavodske (oblast de Poltava)  
    Zbaraj (oblast de Ternopil)  
    Zboriv (oblast de Ternopil)  
    Zdolbouniv (oblast de Rivne)  
    Zelenodolsk (oblast de Dnipropetrovsk)  
    Zinkiv (oblast de Poltava)  
    Zmiïv (oblast de Kharkiv)  
    Znamianka (oblast de Kirovohrad)  
    Zolotchiv (oblast de Lviv)  
    Zolote (oblast de Louhansk)  
    Zolotonocha (oblast de Tcherkassy)  
    Zorynsk (oblast de Louhansk)  
    Zouhres (oblast de Donetsk)  
    Zvenyhorodka (oblast de Tcherkassy)  
    Zymohiria (oblast de Louhansk)
    Abazivka
    Abrykosivka
    Adamivka
    Aeroflotskyi
    Ahrarne
    Alchevsk
    Almazna
    Alushta
    Amvrosiivka
    Ananiv
    Andriievo-Ivanivka
    Andriivka
    Andriivka
    Andriivka
    Andrushivka
    Andrushivka
    Andrushky
    Antonivka
    Antratsyt
    Anysiv
    Apostolove
    Arbuzynka
    Arkhanhelska Sloboda
    Artemivsk
    Artsyz
    Askaniia-Nova
    Auly
    Avdiivka
    Aviatorske
    Babche
    Babyn
    Babyn
    Babyntsi
    Baibuzy
    Bairachky
    Bakhchysarai
    Bakhmut
    Balabyne
    Balakliia
    Balta
    Bandurove
    Bar
    Baranivka
    Baranykivka
    Barashi
    Barashivka
    Barturyn
    Barvynkove
    Baryshivka
    Bashmachka
    Bashtanka
    Basyuvka
    Batovo
    Baykovtsy
    Bazaliia
    Beleluia
    Belobozhnitsa
    Belogorodka
    Belz
    Bendzary
    Bene
    Berdiansk
    Berdychiv
    Berehove
    Berestechko
    Berezan
    Berezanka
    Berezhany
    Berezhany
    Berezhynka
    Berezivka
    Bereznehuvate
    Berezova Rudka
    Berezovo
    Berezyna
    Bernove
    Bershad
    Beryslav
    Bezborodky
    Bezliudivka
    Bibrka
    Bila Tserkva
    Bila Tserkva
    Bilche
    Bile
    Bilenke
    Bilenke
    Bilhorod-Dnistrovskyi
    Biliaivka
    Bilkivtsi
    Bilmak
    Biloberizka
    Bilohirsk
    Bilohorodka
    Bilokorovychi
    Bilokrynnytsia
    Bilokurakyne
    Bilopillya
    Bilousivka
    Bilovodsk
    Bilozerka
    Bilozirka
    Bilshivtsi
    Bilyne
    Birky
    Birky
    Blahodatne
    Blahovishchenske
    Blystavytsya
    Blyzhnie
    Bobrivnyk
    Bobrovytsia
    Bobrynets
    Bochanytsya
    Bochechky
    Bodaki
    Bodakva
    Bohdanivka
    Bohdanivka
    Bohdanivka
    Bohodukhiv
    Bohorodchany
    Bohuslav
    Bohuslav
    Bohynivka
    Boikivske
    Bokhonyky
    Bolekhiv
    Bolhrad
    Borisov
    Borivtsi
    Borki
    Borodyanka
    Borokhiv
    Boromlya
    Borova
    Borovytsia
    Borozenske
    Borshchivka
    Borynia
    Boryslav
    Boryspil
    Borzhava
    Borzna
    Boyarka
    Bozhkivs’ke
    Brailiv
    Bratske
    Bratslav
    Brianka
    Brody
    Brody
    Broshniv-Osada
    Brovary
    Brusyliv
    Brylivka
    Bryukhovychi
    Bucha
    Buchach
    Budy
    Buhas
    Bukachivtsi
    Bulakhivka
    Burshtyn
    Bushtyno
    Busk
    Buzovytsia
    Buzynove
    Bykivka
    Byrlivka
    Bystryk
    Bytkiv
    Chabany
    Chaplyne
    Chaplynka
    Chaplynka
    Chechelnyk
    Chemer
    Chemerivtsi
    Cherepashyntsi
    Cherkaske
    Cherkasy
    Chernechchyna
    Chernelytsya
    Chernihiv
    Chernihivka
    Chernivtsi
    Chernivtsi
    Chernyatin
    Chervone
    Chervone
    Chervonohrad
    Chervonohryhorivka
    Chervonyy Oskil
    Chkalove
    Chkalove
    Chop
    Chopovychi
    Chornivka
    Chornoholova
    Chornomorsk
    Chornomorske
    Chornotysiv
    Chornukhy
    Chornyy Potik
    Chortkiv
    Chortomlyk
    Chudniv
    Chuhuiv
    Chukaluvka
    Chumaky
    Chyhyryn
    Chynadiyovo
    Chyshky
    Dashiv
    Delen
    Deleva
    Deliatyn
    Demuryne
    Denyshi
    Derno
    Dertsen
    Dihtiari
    Dmukhailivka
    Dmytrivka
    Dmytrivka
    Dnipro
    Dniprorudne
    Dniprovske
    Dnistrivka
    Dobra
    Dobrik
    Dobromyl
    Dobroslav
    Dobrotvir
    Dobrovelychkivka
    Dobrovlyany
    Dolyna
    Dolynska
    Domanivka
    Donetsk
    Doroshivtsi
    Doslidnytske
    Dovbysh
    Dovhe
    Dovzhansk
    Dovzhok
    Drabiv
    Drachyntsi
    Drohobych
    Druzhkivka
    Duba
    Dubivskyi
    Dubivtsi
    Dubno
    Dubove
    Dubrovytsya
    Dubyshche
    Dykanka
    Dymer
    Dyrdyn
    Dzhankoi
    Dzhulynka
    Enerhodar
    Fastiv
    Fastovets
    Fedorivka
    Fedorivka
    Fertesholmash
    Fontanka
    Gorishnyaya Vygnanka
    Haisyn
    Haivoron
    Halych
    Harasymiv
    Havrylivka
    Havryshivka
    Henichesk
    Hertsa
    Hirne
    Hirnyk
    Hirsivka
    Hleiuvatka
    Hlobyne
    Hlodosy
    Hlukhiv
    Hlukhivtsi
    Hlushkiv
    Hlyboka
    Hlyboke
    Hlyniany
    Hlynsk
    Hnivan
    Hola Prystan
    Holma
    Holoskiv
    Holovanivsk
    Holovetsko
    Holovkivka
    Holovne
    Holovy
    Holovyne
    Holubivka
    Holubivske
    Holubyne
    Holubynka
    Honcharivka
    Hora
    Hordiivka
    Horenka
    Horianivske
    Horinchovo
    Horishni Plavni
    Horlivka
    Hornostaivka
    Horodenka
    Horodnia
    Horodnytsia
    Horodok
    Horodok
    Horodok
    Horodyshche
    Horodyshche
    Horodyshche
    Horokhiv
    Horonda
    Horoshova
    Horyhliady
    Hoshcha
    Hostomel
    Hozhuly
    Hołoby
    Hrabiv
    Hranitne
    Hrebinka
    Hrebinky
    Hreblya
    Hrechane
    Hrechyshkyne
    Hrunyky
    Hrushivtsi
    Hryshkivtsi
    Hubnyk
    Hubynykha
    Huiva
    Huliaipole
    Hulsk
    Hulyaypole
    Hupalivka
    Hurzuf
    Huta
    Hvardiys’ke
    Hvizdets
    Hyryavi Iskivtsi
    Ichki
    Ichnia
    Ilarionove
    Illintsi
    Iltsi
    Imeni Shevchenko
    Imstychovo
    Inkerman
    Irpin
    Irshansk
    Irshava
    Isaiky
    Isliam-Terek
    Ivana Franka
    Ivanivka
    Ivanivka
    Ivanivka
    Ivanivka
    Ivanivka
    Ivanivka
    Ivanivske
    Ivanivtsi
    Ivankiv
    Ivankov
    Ivano-Frankivsk
    Ivanopil
    Ivanopillia
    Ivanychi
    Ivashkivtsi
    Iverske
    Iziaslav
    Izium
    Izmail
    Izobilne
    Kachanivka
    Kaharlyk
    Kaihador
    Kakhovka
    Kalanchak
    Kalmiuske
    Kalush
    Kalynivka
    Kalynivka
    Kalynivka
    Kalynivske
    Kalyta
    Kamianets-Podilskyi
    Kamiani Potoky
    Kamianka-Dniprovska
    Kamianske
    Kamianske
    Kamin-Kashyrskyi
    Kam”yane
    Kaniv
    Kapulivka
    Kapytolivka
    Kariv
    Karnaukhivka
    Karpylivka
    Kashperivka
    Kashperivka
    Katerynivka
    Kaydanovo
    Kazanka
    Kaznacheyivka
    Kehychivka
    Keleberda
    Kelmentsi
    Kernitsa
    Kharkiv
    Khartsyzk
    Kherson
    Khmelnytskyi
    Khmilnyk
    Khodoriv
    Khodorkiv
    Khomenky
    Khomutets
    Khorol
    Khoroshe
    Khoroshiv
    Khotiv
    Khotyn
    Khreshchatytske
    Khrestivka
    Khroly
    Khrustalnyi
    Khrystoforivka
    Khrystynivka
    Khust
    Khymchyn
    Kiliia
    Kitsman
    Kivertsi
    Klavdiyevo-Tarasove
    Klembivka
    Klenovyi
    Kniazhdvir
    Kobeliaky
    Kobyletska Poliana
    Kocherezhky
    Kochubeyev
    Kodra
    Kodyma
    Koktebel
    Kolchyno
    Kolky
    Kolochava
    Kolodribka
    Kolomyia
    Kolybaivka
    Kolychivka
    Komariv
    Komariv
    Komarno
    Kompaniivka
    Komysh-Zoria
    Komyshuvakha
    Konotop
    Kopachivka
    Kopaihorod
    Kopashnovo
    Korchyn
    Koreiz
    Koriukivka
    Korniyivka
    Kornyn
    Korolevo
    Korop
    Koropets
    Korosten
    Korostyshiv
    Korsun-Shevchenkivskyi
    Korytne
    Kosari
    Kosiv
    Kosmach
    Kostiantynivka
    Kostopil
    Kosyno
    Kotovka
    Kotsyubyns’ke
    Kovalivka
    Kovalivka
    Kovel
    Koviahy
    Kozelets
    Kozelshchyna
    Kozhanka
    Kozhukhivka
    Koziatyn
    Kozova
    Kozyn
    Kozyriany
    Kramatorsk
    Krasnodon
    Krasnohrad
    Krasnoillia
    Krasnoilsk
    Krasnokamianka
    Krasnokutsk
    Krasnopilka
    Krasnopillya
    Krasnosilka
    Krasnostavtsi
    Krasnostavtsy
    Krasnyi Kut
    Krasnyk
    Kremenchuk
    Kremenets
    Kropyvnytskyi
    Kruhlyakivka
    Krupske
    Kryklyvets
    Krylos
    Krynychky
    Krynychky
    Krynychne
    Krynychne
    Kryukivshchyna
    Kryve Ozero
    Kryvorivnia
    Kryvyi Rih
    Kryzhopil
    Kubei
    Kuchakiv
    Kuchurhan
    Kukavka
    Kumachove
    Kupiansk
    Kurman
    Kurylivka
    Kushnytsia
    Kushuhum
    Kuty
    Kutyshche
    Kvasyliv
    Kvitky
    Kvitneve
    Kyinka
    Kyiv
    Kyrnasivka
    Kyrylivka
    Kyslychuvata
    Kytaihorod
    Ladychin
    Ladyzhyn
    Lanchyn
    Lanivtsi
    Lany
    Lativka
    Lavky
    Lazeshchyna
    Lazurne
    Lazy
    Lebedyn
    Lemeshivka
    Lenkivtsi
    Lepetykha
    Letychiv
    Lisnyky
    Lisohirka
    Lisova Lysiivka
    Lisovi Hrynivtsi
    Lisovychi
    Lityn
    Liubar
    Liubashivka
    Liubech
    Liubotyn
    Livadiia
    Livyntsi
    Lokachi
    Lokhvytsya
    Loshkarivka
    Losynivka
    Lozova
    Lozova
    Lozuvatka
    Lozuvatka
    Lubny
    Luchyste
    Luhansk
    Luhy
    Luhyny
    Luka
    Lukiv
    Lukovo
    Lupareve
    Lutsk
    Lviv
    Lychkove
    Lykhivka
    Lyman
    Lyman
    Lymanske
    Lypcha
    Lypetska Poliana
    Lypne
    Lypovets
    Lysets
    Lysianka
    Lysychansk
    Lysychovo
    Lytvynivka
    Lyubeshiv
    Lyublynets’
    Lyuboml’
    Lyubymivka
    Lyutens’ki Budyshcha
    Machukhy
    Mahdalynivka
    Maidan
    Maidan
    Maidanetske
    Makariv
    Makariv Yar
    Makhnivka
    Makiivka
    Mala Danylivka
    Mala Petrykivka
    Mala Uhol’ka
    Mala Vyska
    Mali Kopani
    Malokaterynivka
    Malomykolaivka
    Malyi Kobeliachok
    Malyn
    Malyy Khodachkov
    Malyy Rakovets’
    Manevychi
    Manhush
    Mankivka
    Mardarivka
    Marhanets
    Marianivka
    Mariiampil
    Mariupol
    Masandra
    Mashivka
    Matroska
    Matviyivka
    Mazurivka
    Medenychi
    Medvyn
    Medynia
    Medzhybizh
    Melekyne
    Melioratyvne
    Melitopol
    Melnyky
    Mel’nyky
    Mena
    Menchykury
    Mezhova
    Mezhyrich
    Mikhailivka
    Milove
    Miusynsk
    Mizhhiria
    Mliiv
    Mohyliv-Podilskyi
    Molochansk
    Molodkiv
    Molodohvardiisk
    Monastyrets
    Monastyryshche
    Monastyryska
    Morshyn
    Morske
    Moshanets
    Moshny
    Moshoryne
    Mostove
    Mukacheve
    Murovani Kurylivtsi
    Myhove
    Mykhailivka
    Mykhailivka
    Mykhailivka
    Mykhailivka
    Mykhailivka
    Mykhailivtsi
    Mykhailo-Kotsiubynske
    Mykhaylivka
    Mykolaiv
    Mykolaiv
    Mykolaivka
    Mykolaivka
    Mykolaivka
    Mykolaivka
    Mykolaivka
    Mykolaivka
    Mykolayiv
    Mykolayivka
    Mykolayivka
    Myrhorod
    Myrne
    Myrne
    Myrnohrad
    Myroliubivka
    Myronivka
    Myropil
    Myropillya
    Mytchenky
    Mytlashivka
    Nadezhdivka
    Nadvirna
    Nahirne
    Nahiryanka
    Napadovka
    Naraivka
    Narodychi
    Nasypne
    Nedaivoda
    Nedryhayliv
    Nehrovets
    Nehrovo
    Nekhvoroshch
    Nelypivtsi
    Nemishayeve
    Nemyriv
    Nemyriv
    Nerubaiske
    Netishyn
    Nikita
    Nikolske
    Nikopol
    Nizhyn
    Nosivka
    Nova Borova
    Nova Dacha
    Nova Haleshchyna
    Nova Hreblia
    Nova Kakhovka
    Nova Maiachka
    Nova Odesa
    Nova Ushytsia
    Novgorodskoye
    Novhorod-Siverskyi
    Novhorodka
    Novi Bilokorovychi
    Novi Kryvotuly
    Novi Sanzhary
    Novoaidar
    Novoarkhanhelsk
    Novoazovsk
    Novoderkul
    Novoekonomichne
    Novohrad-Volynskyi
    Novohuivynske
    Novohupalivka
    Novokrasnyanka
    Novomoskovsk
    Novomykolaivka
    Novomykolaivka
    Novomykolayivka
    Novomyrhorod
    Novooleksandrivka
    Novooleksandrivka
    Novoozerne
    Novopavlivka
    Novopetrivka
    Novopidhorodne
    Novopillia
    Novopokrovka
    Novopoltavka
    Novosamarka
    Novoselytsia
    Novoselytsia
    Novosilky
    Novotaromske
    Novotroitske
    Novoukrainka
    Novovasylivka
    Novovolynsk
    Novovorontsovka
    Novoyavorovskoye
    Novozarivka
    Novyi Bilous
    Novyi Buh
    Novyi Kalyniv
    Novyi Kropyvnyk
    Novyi Rozdil
    Novyi Yarychiv
    Novyy Svit
    Nyzhni Sirohozy
    Nyzhnia Krynka
    Nyzhnie Selyshche
    Nyzhnii Bystryi
    Nyzhniy Dubovets’
    Nyzhnohirskyi
    Nyzhnya Syrovatka
    Obertyn
    Obolon
    Obroshino
    Obukhiv
    Obukhivka
    Ochakiv
    Odesa
    Okhtyrka
    Oleksandriia
    Oleksandriiske
    Oleksandrivka
    Oleksandrivka
    Oleksandrivka
    Oleksandrivka
    Oleksandrivka
    Oleksandrivsk
    Oleksiivka
    Oleksiivka
    Olenivka
    Olenivka
    Olenivka
    Oleshky
    Olevsk
    Oleyëvo-Korolëvka
    Olyka
    Onufriivka
    Opishnya
    Opytne
    Orativ
    Orikhiv
    Orilka
    Orzhytsia
    Osiy
    Ostapovo
    Oster
    Ostriv
    Ostroh
    Osynove
    Otyniia
    Ovidiopol
    Ovruch
    Ozaryntsi
    Ozeriany
    Ozerne
    Palahychi
    Palanka
    Parafiivka
    Partenit
    Partyzanske
    Pashkivtsi
    Pasika
    Pasytsely
    Pavlivka
    Pavlohrad
    Pechenihy
    Pechenizhyn
    Perebykivtsi
    Perechyn
    Peredilske
    Perehinske
    Peremoha
    Peremyl
    Peremyshliany
    Pereshchepyne
    Perevalsk
    Pereyaslav-Khmel’nyts’kyy
    Perkivtsi
    Pershotravensk
    Pershotravensk
    Pershotravneve
    Pervomaisk
    Pervomaisk
    Pervomaiske
    Pervomaiskyi
    Pervomaiskyi
    Petropavlivka
    Petropavlivka
    Petropavlivs’ka Borshchahivka
    Petrove
    Petrushiv
    Petrykivka
    Piatkivka
    Piatyhory
    Piatykhatky
    Pidhaitsi
    Pidhorodna
    Pidhorodne
    Pidlisne
    Pidplesha
    Pidvolochysk
    Piilo
    Pishcha
    Pishchane
    Pishchanka
    Piskivka
    Pivdenne
    Pivdenne
    Plodorodne
    Ploske
    Pluzhnoye
    Pnikut
    Poberezhzhia
    Podilsk
    Podishor
    Podove
    Pohreby
    Pohrebyshche
    Pokrov
    Pokrovsk
    Pokrovske
    Poliana
    Polianka
    Polohy
    Polohy
    Polovynkyne
    Poltava
    Poltavka
    Pomichna
    Pomynyk
    Poninka
    Popasne
    Popeli
    Popelnaste
    Popilnia
    Popivtsi
    Potashnia
    Potik
    Potoky
    Preobrazhenka
    Preobrazhenka
    Preslav
    Priadivka
    Pridberezzia
    Pristromy
    Prosyana
    Pryazovske
    Prybuzhzhia
    Prydniprovske
    Prykolotne
    Pryluky
    Prymorsk
    Prymorske
    Prymorske
    Pryshyb
    Pryshyb
    Pryvillya
    Pryvilne
    Pryvitne
    Pryvitne
    Puhachivka
    Pulyny
    Pustomyty
    Putyla
    Putyvl
    Pysarivka
    Pysarivka
    Pysarivka
    Pysmenne
    Rachky
    Radisne
    Radomyshl
    Radovel
    Radushne
    Radyvyliv
    Rakhiv
    Rashkiv
    Ratne
    Rava-Rus’ka
    Razdory
    Reia
    Reni
    Repuzhyntsi
    Reshetylivka
    Richytsya
    Rivne
    Rivne
    Rivne
    Rogozno
    Rohatyn
    Roishche
    Rokyni
    Rokytne
    Romaniv
    Romny
    Ropcha
    Rosishka
    Rososhany
    Rotmistrivka
    Rovenky
    Rozdilna
    Rozdolne
    Rozhniativ
    Rozhyshche"""

ukraine_cities = (
    re.sub("[\(\[].*?[\)\]]", "", ukraine_cities)
    .replace("\n", ",")
    .replace(" ", "")
    .replace("’", "'")
)
ukraine_cities = ukraine_cities.split(",")

# print(ukraine_cities[-1])
