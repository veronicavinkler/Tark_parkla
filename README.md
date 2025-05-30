SISSEJUHATUS
Projekti tulemusel peaks parkimisvajadusega lõppkasutajale muutuma parkimiskohtade leidmine lihtsamaks, et ei peaks parklat tühjalt ringi sõitma lootes, et  on kusagil on vaba koht olemas.
Hetkeseseisuga parkla, juhul kui parkimiskohal on  auto pargitud, lülitab sisse punase tule ja kui parkimiskoht on vaba, siis lülitab punase tule välja ning rohelise sisse. Kui tekib rikke või auto on liiga lähedal ultraheli andurile, hakkavad roheline ja punane tuli vilkuma samal ajal.
Projekti eesmärk on ühendada ja programmeerida ultraheli andurid tuvastama kas auto on ees olevas parkimiskohas või mitte ja vastavalt sellele panna kas rohelise või punase led-lambi tööle ning kuvada kasutajale led-ekraanil mitu parkimiskohta on vaba.

TARKVARA
Tarkvara, mida projektis kasutatakse, on Thonny.

Koodi ülesanne on täita järgmiseid ülesandeid: 
Anda parkla LED lampide järgi infot parkimiskoha seisundi kohta- „Vaba“, „Hõivatud“ või „Vigane“;
Anda kasutajale infot I2C ekraani abil, kus esimene rida annab teada, mitu parkimiskohta on vaba ja teine rida, millised parkimiskohad on vigased;
Anda infot aplikatsiooni kaudu-millised parkimise kohad on vabad, hõivatud ja vigased;
Aplikatsiooni logi annab ülevaate viimastest parkla muutustest;
Aplikatsioon annab teada mitu parkimiskohta on vaba ja millised ning mitu ja millised parkimiskohad on vigased.

Targa Parkla Kood on üles ehitatud funktsioonide peal. Funktsioonid on jagatud kahte gruppi: funktsioonid informatsiooni saamiseks ja funktsioonid informatsiooni edastamiseks. 

Ülesanded mida on vaja taita informatsiooni saamiseks:
Kui kaugel on auto parkimise kohast
Mitu parkimiskohta on vaba
Millised parkimise kohad on vabad
mitu parkimiskohta on vigased
millised parkimiskohad on vigased

Ülesanded mida tuleb täita informatsiooni edastamiseks
LED lampidele- kas parkimiskoht on vaba, kinni või vigane
I2C ekraan- mitu parkimiskohta on vaba, millised parkimiskohad on vigased
App- Millised parkimise kohad on vabad, kinni, vigased.
App- Mitu parkimiskohta on vabad, vigased ja millised

Tähtsad väärtused:
free_num- annab infot, mitu parkimiskohta on vaba
error_num- annab teada, mitu parkimiskohta on vigased
parking spaces- näitab iga parkimise koha staatust, kas need on vabad või hõivatud
error spaces-näitab kas iga parkimiskoht on vigane või mitte
ledred- punase LED lambi ühendused
ledgreen- rohelise LED lambi ühendused
TRIG- trigger ühendus
ECHO- echo ühendus
speed_of_sound- heli kiirus

Funktsioonid ja ülesandeid need täidavad:
distance- auto distantsi arvutamine
add_free_and_error- lisab vabad parkimiskohad ja arvutab vabade kohtade summa ja vea
p_checking- parkimise koha staatuse määramine
Edastamine appile
build- Ehitatakse üles appi välimus ja antakse esimesed ülesanded
add_to_log- info logisse lisamine
Edastamine I2C ekraanile
add_to_screen
Edastamine LED lampidele
Initializing-  LED lampide ülesseadmine
add_to_led- LED lampide värvuse määramine

Algselt pannakse TRIG1 väära, tõese ja väära peale ning mõõdetakse ECHO1 algus ja lõppaega, misjärel arvutatakse pulsi kestus aeg.
Seejärel arvutatakse objekti distants ultraheli andurist kasutades valemit: distants=(pulsi kestus aeg*valgus kiirus)/2. Vastus antakse sentimeetrites ja saadud tulemus ümardatakse.

Arvutuste põhjal saadud tulemust kasutatakse edasi if lausetes:
Kui distants on väiksem kui 0 cm või suurem kui 25 cm kirjutab konsool ““error or car too close, car distance:”,distance “cm”” mis tähendab viga või auto on liikunud ultraheli andurile liiga lähedale. Tulemusena pannakse teatud ajavahemikega tööle punane ja roheline andur koos s.o tuled vilguvad vaheldumisi.
Kui distants on suurem kui 15 cm ja väiksem kui 25 cm siis süttib parkimis koha üleval olev roheline LED-tuli ja konsool kirjutab, et parkimise koht on vaba.
Kui distants on suurem kui 0 cm ja väiksem kui 15 cm siis süttib punane LED-lamp ja konsool kirjutab parkimiskoht 1 on hõivatud. 
Kui distants jääb 15 cm ja 25 cm vahele kirjutatakse konsooli kui lähedal on auto ultraheli andurist.

Parkimisaluse äär asub ultraheliandurist umbes 25 cm kaugusel, mistõttu loetakse kõik mõõtmised sellest kaugemal ebatäpseteks ehk vigaseks. Põhjuseks on see, et andur tuvastab parkimisaluse äärt peaaegu alati, mis mõjutab anduri võimet anda usaldusväärseid mõõtetulemusi kaugemal asuvate objektide kohta. Roheline tuli süttib ka pärast 15cm, kuna kui auto sõidab parkimise kohast mööda täiesti seina ääres, ei loeta seda parkimiskoha okupeerimiseks.
Raspberry Pi saab peale laadida minnes Raspberry Pi kodulehele, ühendada mälupulk või mälukaart arvutiga ning laadida mälupulgale või kaardile Imager-i windowsi jaoks. Pärast laadimist saab seadistada Raspberry Pi tarkvara vastavalt enda vajadustele ning ühendada Raspberry pi mälukaardi või pulgaga ja ülejäänud tarkvaraga.
Targale parklale oli ka lisatud LCD ekraan I2C, et seda kasutada Thonny koodis oli kõigepealt vaja loa anda I2C moodulile [1] selleks jooksime cmd-s käsu sudo apt-get update kui uuendus oli tehtud laadisime alla vajalikud tööriistad kasutades käsku sudo apt-get install i2c-tools [2] ja sudo apt-get install python-smbus [3]. Pärast laadimist oli vaja teha restart.
Kui vajalik on installitud peame eemaldama I2C mustast nimekirjast, selleks läksime /etc/modprobe.d/raspi-blacklist.conf kasutasdes käsklust sudo nano /etc/modprobe.d/raspi-blacklist.conf. Antud kohas oli vaja kommenteerida välja rida blacklist i2c-bcm2708 (#blacklist i2c-bcm2708). Kui i2c oli mustast nimekirjast välja võetud oli vaja lisada moodul kernel-sse kasutades käsku sudo nano /etc/modules, sinna oli vaja lisada i2c-dev. Pärast seda anname ka kasutajale õiguse pääseda ligi I2C moodulile joostes käsklust sudo adduser pi i2c. [3]
Kui I2C moodulile oli luba antud tuli veebist alla laadida Python-i fail, mis aitas teha I2C-ga töötamise kergemaks ja leida I2C aadressi mille hiljem tuli lisada mainitud Pythoni faili. Et leida aadress tuli joosta cmd-s käsu i2cdetect -y 0 [3]. Vajaliku Pythoni faili laadisime alla Circuit Basics veebilehelt ja salvestasime nimega I2C_LCD_driver.py nimega, seejärel muutsime real kirjutatu I2CBUS = 0 pordi ja ADDRESS=0x21 cmd väljastatud aadressiks. Pärast seda salvestasime ja importime targa parkla faili [1] (vt koodi Lisa 2).
