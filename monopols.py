
# visas vertibas ir *1tukst.
# speletajs=[laucins, nauda, [ipasumi], [kilas], jf, [merki], vards]
import random

def chance_community(speletaji, speletajs, krasa, chance, community_chest, ipasumi):
    k = 0
    if krasa == "chance":
        k = chance[0]
        nonem = chance.pop(0)
        if k != "jf":
            chance.append(nonem)
    elif krasa == "chest":
        k = community_chest[0]
        nonem = community_chest.pop(0)
        if k != "jf":
            community_chest.append(nonem)
    if k == "jf":
        speletajs[4] += 1
    
    elif k == "-3s":
        speletajs[0] -= 3
        laucins_info = next(
            (ip for ip in ipasumi if ip["nr"] == speletajs[0]), None)
        krasa = laucins_info["color"]
        if krasa == "chest" or krasa == "chance":
            speletaji, speletajs, chance, community_chest, ipasumi = chance_community(
                speletaji, speletajs, krasa, chance, community_chest, ipasumi)

    elif k == "l_25":
        if speletajs[0] > 25:
            speletajs[1] += 2000
        speletajs[0] = 25

    elif k == "l_12":
        if speletajs[0] > 12:
            speletajs[1] += 2000
        speletajs[0] = 12

    elif k == "l_1":
        speletajs[0] = 1
    elif k == "l_0":
        speletajs[0] = 0

    elif k == "l_6":
        if speletajs[0] > 6:
            speletajs[1] += 2000
        speletajs[0] = 6

    elif k == "l_40":
        speletajs[0] = 40

    elif k == "l_utility":
        if speletajs[0] > 30:
            speletajs[1] += 2000
            speletajs[0] = 13
        elif speletajs[0] > 13:
            speletajs[0] = 29
        else:
            speletajs[0] = 13


    elif k == "l_station":
        if speletajs[0] > 36 or speletajs[0] < 6:
            speletajs[0] = 6
            speletajs[1] += 2000
        elif speletajs[0] > 26:
            speletajs[0] = 36
        elif speletajs[0] > 16:
            speletajs[0] = 26
        else:
            speletajs[0] = 16

    elif k == "tax_ch":
        houses = 0
        hotel = 0
        for nr in speletajs[2]:
            property = atrod_pec_nr(nr, ipasumi)
            if property["houses"] < 5:
                houses += property["houses"]
            elif property["houses"] == 5:
                hotel += 1
        speletajs[1] -= 400*houses + 1500*hotel
    elif k == "tax_com":
        houses = 0
        hotel = 0
        for nr in speletajs[2]:
            property = atrod_pec_nr(nr, ipasumi)
            if property["houses"] < 5:
                houses += property["houses"]
            elif property["houses"] == 5:
                hotel += 1
        speletajs[1] -= 250*houses + 1000*hotel

    elif k == "pl+500":
        index = random.randint(0, len(speletaji)-1)
        while speletaji[index] == speletajs:
            index = random.randint(0, len(speletaji)-1)

        speletaji[index][1] += 500
        speletajs[1] += -500

    elif k == "pl-100":
        for pl in speletaji:
            pl[1] -= 100
            speletajs[1] += 100
    else:
        speletajs[1] += int(k)

    return speletaji, speletajs, chance, community_chest, ipasumi


def atrod_pec_nr(nr, ipasumi):
    return next((property for property in ipasumi if property["nr"] == nr), None)


def pardosana(seller, nr, buyer, cena, ipasumi):
    # parbauda, vai ir, ko pardot, ar ko pirkt
    if nr in (seller[2] + seller[3]) and buyer[1] >= cena:
        property = atrod_pec_nr(nr, ipasumi)

        # nonem majas
        seller_properties = {nr_visi: atrod_pec_nr(nr_visi, ipasumi) for nr_visi in seller[2]}
        for nr_visi, prop in seller_properties.items():
            if prop["color"] == property["color"] and prop["houses"] > 0:
                while prop["houses"] > 0:
                    prop["houses"] -= 1
                    seller[1] += 0.5 * prop["h_cost"]

        # saliek pa vietām - no pārdevēja uz pircēju
        if nr in seller[2]:
            seller[2].remove(nr)
            buyer[2].append(nr)
        elif nr in seller[3]:
            seller[3].remove(nr)
            buyer[3].append(nr)

        # maksaa
        buyer[1] -= cena
        seller[1] += cena

        # salabo same
        for speletajs in [seller, buyer]:
            same = 0
            color_properties = [atrod_pec_nr(nr, ipasumi) for nr in (speletajs[2] + speletajs[3]) if atrod_pec_nr(nr, ipasumi)["color"] == property["color"]]
            same = len(color_properties)
            for prop in color_properties:
                ipasumi[ipasumi.index(prop)]["same"] = same

    return seller, buyer, ipasumi


def izsole(speletaji, property_nr):
    buyers = [sp for sp in speletaji if sp[0] > 0 and sp[1] >= 100]
    if not buyers:
        return None, 0

    prasita_cena = 100  # Minimumala sakumcena
    buyers_var = buyers[:]

    while len(buyers_var) > 1:
        prasita_cena_new = prasita_cena + 100
        buyers_var = [bu for bu in buyers_var if 1 - prasita_cena/bu[1] > 0.7 and bu[1] >= prasita_cena]

        if not buyers_var:
            break

        prasita_cena = prasita_cena_new

    if len(buyers_var) == 1:
        buyer = buyers_var[0]
    elif buyers_var:
        buyer = random.choice(buyers_var)
    else:
        buyer = None

    return buyer, prasita_cena


def naudas_ieguve(speletajs, speletaji, ipasumi):
    privatipasums = speletajs[2]
    dargaka_v = None
    dargaka_m = None
    dargaka_k = None

    # viesnicu pardošana
    for property in ipasumi:
        if property["nr"] in privatipasums and property["houses"] == 5:
            if dargaka_v is None or property["hotel"] > dargaka_v["hotel"]:
                dargaka_v = property
    if dargaka_v is not None:
        dargaka_v["houses"] -= 1
        speletajs[1] += 0.5 * dargaka_v["hotel"]
    else:
        # majas pardosana
        for houses in range(4, 0, -1):
            for property in ipasumi:
                if property["nr"] in privatipasums and property["houses"] == houses:
                    if dargaka_m is None or property["h_cost"] > dargaka_m["h_cost"]:
                        dargaka_m = property
            if dargaka_m is not None:
                dargaka_m["houses"] -= 1
                speletajs[1] += 0.5 * dargaka_m["h_cost"]
                break

    # iekilasana
    if dargaka_v is None and dargaka_m is None:
        for property in ipasumi:
            if property["nr"] in privatipasums:
                if dargaka_k is None or property["mortgage"] > dargaka_k["mortgage"]:
                    dargaka_k = property
    
    if dargaka_k is not None:
        speletajs[2].remove(dargaka_k["nr"])
        speletajs[3].append(dargaka_k["nr"])
        speletajs[1] += dargaka_k["mortgage"]
    else:
        # pardosana citam
        for numurs in (privatipasums + speletajs[3]):
            buyer, cena = izsole(speletaji, numurs)
            if buyer is not None:
                for i, s in enumerate(speletaji):
                    if buyer == s:
                        speletajs, speletaji[i], ipasumi = pardosana(
                            speletajs, numurs, buyer, cena, ipasumi)
                        break

    return speletaji, speletajs, ipasumi


def nebankrotesana(speletajs, speletaji, ipasumi, chance, community_chest):
    while speletajs[1] < 0 and (len(speletajs[2]) > 0):
        speletaji, speletajs, ipasumi = naudas_ieguve(
            speletajs, speletaji, ipasumi)

    if speletajs[4] > 0 and speletajs[1] < 0:
        pirceji = speletaji[:]
        pirceji.remove(speletajs)
        jf_cena = 500
        velme_pirkt_vajag = 0.5
        for buyer in pirceji:
            velme_pirkt = random.random()
            if velme_pirkt >= velme_pirkt_vajag and buyer[1] >= jf_cena and speletajs[4] > 0:
                buyer[1] -= jf_cena
                speletajs[1] += jf_cena
                buyer[4] += 1
                speletajs[4] -= 1

    # bankrots
    # izsledz speletajuno speles
    if speletajs[1] < 0:
        if speletajs in speletaji:
            speletaji.remove(speletajs)
            seller = speletajs[:]

        # atliek atpakal jail free kartites
        while seller[4] > 0:
            if len(chance) < 16:
                chance.append("jf")
            elif len(community_chest) < 16:
                community_chest.append("jf")
            seller[4] -= 1

        # izsole
        for property_nr in (seller[2]+seller[3]):
            buyer, prasita_cena = izsole(speletaji, property_nr)

            if buyer is not None:
                index = speletaji.index(buyer)

                seller, speletaji[index], ipasumi = pardosana(
                    seller, property_nr, buyer, prasita_cena, ipasumi)
        speletajs = None

    return speletajs, speletaji, ipasumi, chance, community_chest


def gajiens(speletaji, speletajs, double, ipasumi, chance, community_chest):
    # met kaulinus
    d = 0
    pirmais = random.randint(1, 6)
    otrais = random.randint(1, 6)
    d = 1 if pirmais == otrais else 0
    if d == 0:
        double == 0
    else:
        double += 1
    rez = pirmais+otrais
    # triisreiz dubultais -> cietums un gaajiens beidzas
    if double == 3:
        speletajs[0] = 0
        return speletaji, speletajs, 0, ipasumi, chance, community_chest

    # cietums (?)
    if speletajs[0] < 1:
        speletajs[0] -= 1

        # velme izmantot jf
        if d == 1:
            speletajs[0] = 11 + rez
        elif speletajs[4] > 0:
            speletajs[4] -= 1
            speletajs[0] = 11 + rez
        # samaksa par izlaisanu
        elif speletajs[0] <= -3:
            speletajs[1] -= 500
            if speletajs[1] >= 0:
                speletajs[0] = 11 + rez
            else:
                # naudas nav, taapeec censas to ieguut, vai bankrots klaat
                speletajs, speletaji, ipasumi, chance, community_chest = nebankrotesana(speletajs, speletaji, ipasumi, chance, community_chest)
                if speletajs is None:
                    # ja bankrote - gaajiens beidzas
                    return speletaji, speletajs, double, ipasumi, chance, community_chest
                else:
                    speletajs[0] = 11 + rez
    else:
        jaunais_lauks = speletajs[0]+rez
        if jaunais_lauks > 40:
            jaunais_lauks -= 40

        # paarbauda starta naudu
        if jaunais_lauks < speletajs[0]:
            speletajs[1] += 2000
        speletajs[0] = jaunais_lauks
 
    # visiem, kuri veel ir cietumaa, gaajienam nav vairaak opciju
    if speletajs[0] <= 0:
        return speletaji, speletajs, double, ipasumi, chance, community_chest

    # ievaac zinas par laucinu, uz kura atrodas speeleetaajs
    laucins_info = next(
        (ip for ip in ipasumi if ip["nr"] == speletajs[0]), None)
    krasa = laucins_info["color"] if laucins_info else None

    if krasa in ["chance", "chest"]:
        speletaji, speletajs, chance, community_chest, ipasumi = chance_community(
            speletaji, speletajs, krasa, chance, community_chest, ipasumi)
        # nelauj staigaat apkaart ar paraadiem
        if speletajs[1] < 0:
            speletajs, speletaji, ipasumi, chance, community_chest = nebankrotesana(speletajs, speletaji, ipasumi, chance, community_chest)

        # paarbauda, vai nav bankroteejis
        if speletajs is None:
            return speletaji, speletajs, double, ipasumi, chance, community_chest

        # izveertee jauno laucinu
        laucins_info = next(
            (ip for ip in ipasumi if ip["nr"] == speletajs[0]), None)
        krasa = laucins_info["color"] if laucins_info else None

    # ar iesanu cietumaa gaajiens beidzas
    if krasa == "go_jail":
        speletajs[0] == 0
        return speletaji, speletajs, double, ipasumi, chance, community_chest

    elif krasa == "i_tax":
        speletajs[1] -= 2000
        # nelaujam staigat apkart ar paradiem
        if speletajs[1] < 0:
            speletajs, speletaji, ipasumi, chance, community_chest = nebankrotesana(speletajs, speletaji, ipasumi, chance, community_chest)

    elif krasa == "s_tax":
        speletajs[1] -= 1000
        # nelauj staigaat apkaart ar paraadiem
        if speletajs[1] < 0:
            speletajs, speletaji, ipasumi, chance, community_chest = nebankrotesana(speletajs, speletaji, ipasumi, chance, community_chest)

    elif krasa in ["free", "chance", "chest", "start", "go_jail", "i_tax", "s_tax"]:
        maksa = 0

    # uzkaapsana uz iipasumiem
    else:
        if speletajs[0] in (speletajs[2]+speletajs[3]):
            maksa = 0  # atrodas uz sava ipasuma

        else:
            property = atrod_pec_nr(speletajs[0], ipasumi)
            nav = 0
            # neatrodas uz sava ipasuma
            for sp in speletaji:
                # parbauda, vai ir iekilkats
                if speletajs[0] in sp[3]:
                    maksa = 0

                # paarbauda, vai ir nopirkts
                elif speletajs[0] in sp[2]:
                    # atrod ipasnieku, jaasamaksaa ire

                    if property["color"] == "station":
                        maksa = 250*property["same"]

                    elif property["color"] == "utility":
                        if property["same"] == 1:
                            k = 4
                        elif property["same"] == 2:
                            k = 10
                        maksa = k*rez*10

                    else:
                        kop_same = sum(
                            1 for ip in ipasumi if ip["color"] == property["color"])
                        # paarbauda, vai ir visi iipasumi
                        if kop_same == property["same"]:
                            if property["houses"] == 0:
                                maksa = property["rent"] * 2
                            elif property["houses"] == 5:
                                maksa = property["hotel"]
                            else:
                                houses = property["houses"]
                                maksa = property[f"{houses}h"]

                        # nav visu ipasumu
                        else:
                            maksa = property["rent"]

                    # samaksa
                    speletajs[1] -= maksa
                    sp[1] += maksa

                # nav iegadats
                else:
                    nav += 1

            # nevienam nepieder
            if speletajs[1] < 0:
                speletajs, speletaji, ipasumi, chance, community_chest = nebankrotesana(speletajs, speletaji, ipasumi, chance, community_chest)
            if speletajs is None:
                return speletaji, speletajs, double, ipasumi, chance, community_chest

            if len(speletaji) == nav and property is not None:
                if speletajs is None:
                    return speletaji, speletajs, double, ipasumi, chance, community_chest
                # var atlauties nopirkt

                property = atrod_pec_nr(speletajs[0], ipasumi)
                if speletajs[1] >= property["price"]:
                    # banka paardod
                    banka = [1, property["price"], [property["nr"]], [], 0, []]
                    seller, speletajs, ipasumi = pardosana(banka, property["nr"], speletajs, property["price"], ipasumi)

                # paarbauda, vai tas nav speeleetaaja meerkis
                elif speletajs[0] in speletajs[5]:
                    # parbauda, vai var iegadaties un nebankrotet
                    speletajs_tests = speletajs[:]
                    speletaji_tests = speletaji[:]
                    ipasumi_tests = ipasumi[:]
                    community_chest_tests = community_chest[:]
                    chance_tests = chance[:]

                    # atrod indeksu
                    index = speletaji_tests.index(speletajs_tests)

                    # banka "paardod"
                    banka = [1, property["price"], [property["nr"]], [], 0, []]
                    speletajs_tests[1] += property["price"]

                    seller, speletajs_tests, ipasumi_tests = pardosana(banka, property["nr"], speletajs_tests, property["price"], ipasumi_tests)
                    speletajs_tests[1] -= property["price"]
                    speletaji_tests[index] = speletajs_tests

                    # neaiztiek citus meerka ipasumus
                    neaizskaramie_2 = []
                    neaizskaramie_3 = []
                    for nr in speletajs_tests[5]:
                        if nr in speletajs_tests[2]:
                            speletajs_tests[2].remove(nr)
                            neaizskaramie_2.append(nr)
                        if nr in speletajs_tests[3]:
                            speletajs_tests[3].remove(nr)
                            neaizskaramie_3.append(nr)

                    # vai nav bankrots, ja nopirks?
                    speletajs_tests, speletaji_tests, ipasumi_tests, chance_tests, community_chest_tests = nebankrotesana(speletajs_tests, speletaji_tests, ipasumi_tests, chance_tests, community_chest_tests)

                    # ja nebankrotee, tad var pirkt
                    if speletajs_tests is not None:
                        speletajs = speletajs_tests
                        for ip in neaizskaramie_2:
                            speletajs[2].append(ip)
                        for ip in neaizskaramie_3:
                            speletajs[3].append(ip)
                        speletaji = speletaji_tests
                        ipasumi = ipasumi_tests
                        community_chest = community_chest_tests
                        chance = chance_tests
    
    if speletajs is None:
        return speletaji, speletajs, double, ipasumi, chance, community_chest
    # papildiespeejas, ja ir budzets un netiks veikti taalaaki metieni
    if speletajs[1] > 0 and d != 1:
        iespejas = ["atkilat", "majas", "iepirkumi"]
        aktivitate = random.choice(iespejas)

        if aktivitate == "atkilat":
            if len(speletajs[3]) > 0:
                kilas_nr = speletajs[3][:]  
                random.shuffle(kilas_nr)
                for kila_nr in kilas_nr:
                    kila = atrod_pec_nr(kila_nr, ipasumi)
                    if speletajs[1] >= kila["mortgage"] * 1.1 + 100:
                        speletajs[1] -= 1.1*kila["mortgage"]
                        speletajs[3].remove(kila_nr)
                        speletajs[2].append(kila_nr)

        elif aktivitate == "majas":
            # viesnicu un maju limiti
            kop_majas = sum(visi_ipasumi["houses"] for visi_ipasumi in ipasumi if visi_ipasumi["houses"] != 5)
            kop_viesnicas = sum(1 for visi_ipasumi in ipasumi if visi_ipasumi["houses"] == 5)
            
            kop_same_visi = {ip["color"]: sum(1 for i in ipasumi if i["color"] == ip["color"]) for ip in ipasumi}
            apbuvejami = [ip_nr for ip_nr in speletajs[2] if (atrod_pec_nr(ip_nr, ipasumi) is not None and
                atrod_pec_nr(ip_nr, ipasumi).get("1h") is not None and  
                atrod_pec_nr(ip_nr, ipasumi)["same"] == kop_same_visi[atrod_pec_nr(ip_nr, ipasumi)["color"]] and
                atrod_pec_nr(ip_nr, ipasumi)["houses"] != 5)]

            if len(apbuvejami) > 0:
                random.shuffle(apbuvejami)
                for apbuve_nr in apbuvejami:
                    apbuve = atrod_pec_nr(apbuve_nr, ipasumi)
                    if apbuve["color"] not in ["utilities", "station"]:
                        house_new = apbuve["houses"] + 1
                        if house_new == 5 and speletajs[1] >= 1.5*apbuve["h_cost"] and kop_viesnicas < 12:
                            speletajs[1] -= apbuve["h_cost"]
                            index = ipasumi.index(apbuve)
                            ipasumi[index]["houses"] += 1

                        elif house_new < 5 and speletajs[1] >= 1.5*apbuve["h_cost"] and kop_majas < 32:
                            speletajs[1] -= apbuve["h_cost"]
                            index = ipasumi.index(apbuve)
                            ipasumi[index]["houses"] += 1

        elif aktivitate == "iepirkumi":
            # no meerkiem
            done = 0
            for sp_nr in speletajs[5]:
                for cits in speletaji:
                    if cits != speletajs:
                        for cits_nr in (cits[2]+cits[3]):
                            # ir mekletajs
                            if cits_nr == sp_nr:
                                # noskaidro, kaada ir cena
                                k = 1
                                # vai vinam ir citi (godiigas cenas mekleejumi)
                                karotais_ipasums = atrod_pec_nr(sp_nr, ipasumi)
                                k *= karotais_ipasums["same"]
                                # vai vinam ir majas
                                k *= karotais_ipasums["houses"] + 1

                                cena = 2*k*karotais_ipasums["price"]

                                # vai var atlautiess?
                                if cena <= speletajs[1]:
                                    # peerk
                                    cits, speletajs, ipasumi = pardosana(
                                        cits, sp_nr, speletajs, cena, ipasumi)
                                    done = 1
                                    break
                    if done != 0:
                        break

            # no same
            if done == 0:
                for sp_nr in (speletajs[2]+speletajs[3]):
                    sp_ip = atrod_pec_nr(sp_nr, ipasumi)
                    for cits in speletaji:
                        if speletajs != cits:
                            for cits_nr in (cits[2]+cits[3]):
                                cits_ip = atrod_pec_nr(cits_nr, ipasumi)
                                if cits_ip["color"] == sp_ip["color"]:
                                    # ir vienaas same
                                    # meklee cenu
                                    k = 1
                                    # vai viÅam ir citi
                                    k *= cits_ip["same"]
                                    # vai vinamm ir majas
                                    k *= cits_ip["houses"] + 1

                                    cena = 2*k*cits_ip["price"]

                                    if cena <= speletajs[1]:
                                        # peerk
                                        cits, speletajs, ipasumi = pardosana(
                                            cits, cits_nr, speletajs, cena, ipasumi)
                                        done = 1
                                        break
                        if done != 0:
                            break

    # navar pabeigt ar paraadiem
    if speletajs[1] < 0:
        speletajs, speletaji, ipasumi, chance, community_chest = nebankrotesana(speletajs, speletaji, ipasumi, chance, community_chest)

    if double > 0:
        speletaji, speletajs, double, ipasumi, chance, community_chest = gajiens(
            speletaji, speletajs, double, ipasumi, chance, community_chest)

    return speletaji, speletajs, double, ipasumi, chance, community_chest


def spele(merki):
    chance_kartites = ["jf", "-150", "+1500", "+500", "-3s", "l_utility", "l_25", "l_station", "l_0", "l_12", "l_40", "l_6", "l_1", "l_station", "tax_ch", "pl+500"]
    community_chest_kartites = ["pl-100", "+100", "+100", "+200", "+250", "+1000", "+1000", "+500", "+2000", "l_1", "l_0", "jf", "tax_com", "-500", "-500", "-1000"]

    random.shuffle(chance_kartites)
    random.shuffle(community_chest_kartites)

    chance = chance_kartites
    community_chest = community_chest_kartites    
    #visi ipasumi
    ipasumi =  [
    {"nr": 2, "price": 600, "rent": 20, "1h": 100, "2h": 300, "3h": 900, "4h": 1600, "hotel": 2500, "h_cost": 500, "mortgage": 300, "color": "brown", "same": 0, "houses": 0},
    {"nr": 4, "price": 600, "rent": 40, "1h": 200, "2h": 600, "3h": 1800, "4h": 3200, "hotel": 4500, "h_cost": 500, "mortgage": 300, "color": "brown", "same": 0, "houses": 0},
    {"nr": 7, "price": 1000, "rent": 60, "1h": 300, "2h": 900, "3h": 2700, "4h": 4000, "hotel": 5500, "h_cost": 500, "mortgage": 500, "color": "l_blue", "same": 0, "houses": 0},
    {"nr": 9, "price": 1000, "rent": 60, "1h": 300, "2h": 900, "3h": 2700, "4h": 4000, "hotel": 5500, "h_cost": 500, "mortgage": 500, "color": "l_blue", "same": 0, "houses": 0},
    {"nr": 10, "price": 1200, "rent": 80, "1h": 400, "2h": 1000, "3h": 3000, "4h": 4500, "hotel": 6000, "h_cost": 500, "mortgage": 600, "color": "l_blue", "same": 0, "houses": 0},
    {"nr": 12, "price": 1400, "rent": 100, "1h": 500, "2h": 1500, "3h": 4500, "4h": 6250, "hotel": 7500, "h_cost": 1000, "mortgage": 700, "color": "pink", "same": 0, "houses": 0},
    {"nr": 14, "price": 1400, "rent": 100, "1h": 500, "2h": 1500, "3h": 4500, "4h": 6250, "hotel": 7500, "h_cost": 1000, "mortgage": 700, "color": "pink", "same": 0, "houses": 0},
    {"nr": 15, "price": 1600, "rent": 120, "1h": 600, "2h": 1800, "3h": 5000, "4h": 7000, "hotel": 9000, "h_cost": 1000, "mortgage": 800, "color": "pink", "same": 0, "houses": 0},
    {"nr": 17, "price": 1800, "rent": 140, "1h": 700, "2h": 2000, "3h": 5500, "4h": 7500, "hotel": 9500, "h_cost": 1000, "mortgage": 900, "color": "orange", "same": 0, "houses": 0},
    {"nr": 19, "price": 1800, "rent": 140, "1h": 700, "2h": 2000, "3h": 5500, "4h": 7500, "hotel": 9500, "h_cost": 1000, "mortgage": 900, "color": "orange", "same": 0, "houses": 0},
    {"nr": 20, "price": 2000, "rent": 160, "1h": 800, "2h": 2200, "3h": 6000, "4h": 8000, "hotel": 10000, "h_cost": 1000, "mortgage": 1000, "color": "orange", "same": 0, "houses": 0},
    {"nr": 22, "price": 2200, "rent": 180, "1h": 900, "2h": 2500, "3h": 7000, "4h": 8750, "hotel": 10500, "h_cost": 1500, "mortgage": 1100, "color": "red", "same": 0, "houses": 0},
    {"nr": 24, "price": 2200, "rent": 180, "1h": 900, "2h": 2500, "3h": 7000, "4h": 8750, "hotel": 10500, "h_cost": 1500, "mortgage": 1100, "color": "red", "same": 0, "houses": 0},
    {"nr": 25, "price": 2400, "rent": 200, "1h": 1000, "2h": 3000, "3h": 7500, "4h": 9250, "hotel": 11000, "h_cost": 1500, "mortgage": 1200, "color": "red", "same": 0, "houses": 0},
    {"nr": 27, "price": 2600, "rent": 220, "1h": 1100, "2h": 3300, "3h": 8000, "4h": 9750, "hotel": 11500, "h_cost": 1500, "mortgage": 1300, "color": "yellow", "same": 0, "houses": 0},
    {"nr": 28, "price": 2600, "rent": 220, "1h": 1100, "2h": 3300, "3h": 8000, "4h": 9750, "hotel": 11500, "h_cost": 1500, "mortgage": 1300, "color": "yellow", "same": 0, "houses": 0},
    {"nr": 30, "price": 2800, "rent": 240, "1h": 1200, "2h": 3600, "3h": 8500, "4h": 10250, "hotel": 12000, "h_cost": 1500, "mortgage": 1400, "color": "yellow", "same": 0, "houses": 0},
    {"nr": 32, "price": 3000, "rent": 260, "1h": 1300, "2h": 3900, "3h": 9000, "4h": 11000, "hotel": 12750, "h_cost": 2000, "mortgage": 1500, "color": "green", "same": 0, "houses": 0},
    {"nr": 33, "price": 3000, "rent": 260, "1h": 1300, "2h": 3900, "3h": 9000, "4h": 11000, "hotel": 12750, "h_cost": 2000, "mortgage": 1500, "color": "green", "same": 0, "houses": 0},
    {"nr": 35, "price": 3200, "rent": 280, "1h": 1500, "2h": 4500, "3h": 10000, "4h": 12000, "hotel": 14000, "h_cost": 2000, "mortgage": 1600, "color": "green", "same": 0, "houses": 0},
    {"nr": 38, "price": 3500, "rent": 350, "1h": 1750, "2h": 5000, "3h": 11000, "4h": 13000, "hotel": 15000, "h_cost": 2000, "mortgage": 1750, "color": "d_blue", "same": 0, "houses": 0},
    {"nr": 40, "price": 4000, "rent": 500, "1h": 2000, "2h": 6000, "3h": 14000, "4h": 17000, "hotel": 20000, "h_cost": 2000, "mortgage": 2000, "color": "d_blue", "same": 0, "houses": 0},
    {"nr": 13, "price": 1500, "mortgage": 750, "color": "utility", "same": 0, "houses": 0},
    {"nr": 29, "price": 1500, "mortgage": 750, "color": "utility", "same": 0, "houses": 0},
    {"nr": 6, "price": 2000, "mortgage": 1000, "color": "station", "same": 0, "houses": 0},
    {"nr": 16, "price": 2000, "mortgage": 1000, "color": "station", "same": 0, "houses": 0},
    {"nr": 26, "price": 2000, "mortgage": 1000, "color": "station", "same": 0, "houses": 0},
    {"nr": 36, "price": 2000, "mortgage": 1000, "color": "station", "same": 0, "houses": 0},
    {"nr": 8, "color": "chance","same": 0, "houses": 0},
    {"nr": 23, "color": "chance", "same": 0, "houses": 0},
    {"nr": 37, "color": "chance", "same": 0, "houses": 0},
    {"nr": 3, "color": "chest", "same": 0, "houses": 0},
    {"nr": 18, "color": "chest", "same": 0, "houses": 0},
    {"nr": 34, "color": "chest", "same": 0, "houses": 0},
    {"nr": 1, "color": "start", "same": 0, "houses": 0},
    {"nr": 11, "color": "free", "same": 0, "houses": 0},
    {"nr": 21, "color": "free", "same": 0, "houses": 0},
    {"nr": 5, "color": "i_tax", "same": 0, "houses": 0},
    {"nr": 39, "color": "s_tax", "same": 0, "houses": 0},
    {"nr": 31, "color": "go_jail", "same": 0, "houses": 0}]
    
    # rada speletajus
    vards = ["es", "Elis","tetis", "mamma"]
    speletaji = [[1, 15000, [], [], 0, m, id] for m in merki for id in vards]

    # izvelas secibu
    random.shuffle(speletaji)
    while len(speletaji) > 1:
        for speletajs in speletaji:
            speletaji, speletajs, double, ipasumi, chance, community_chest = gajiens(
                speletaji, speletajs, 0, ipasumi, chance, community_chest)
    # atgriez uzvareetaaju
    return speletaji[0][6]


def play_game(mans_merkis):
    merki = [mans_merkis, [38, 40], [13, 29], [22, 24, 25]]
    results = spele(merki)
    win = 1 if results == "es" else 0
    
    return {"mans_merkis": mans_merkis, "uzvaras": win}

rez_l = []

for i in range(5):
    for m in [[2, 4], [7, 9, 10], [12, 14, 15], [17, 19, 20], [22, 24, 25], [27, 28, 30], [32, 33, 35], [6, 16, 26, 36], [38, 40], [13, 29]]:
        rez = play_game(m)
        rez_l.append(rez)
    print(1)
print(rez_l)

uzvaras = {}

for entry in rez_l:
    merkis_tuple = tuple(entry['mans_merkis'])
    if merkis_tuple in uzvaras:
        uzvaras[merkis_tuple] += entry['uzvaras']
    else:
        uzvaras[merkis_tuple] = entry['uzvaras']

rez_l = [{'mans_merkis': list(merkis), 'uzvaras': victories} for merkis, victories in uzvaras.items()]
print(rez_l)

# atkārto,  cik dators lauj
