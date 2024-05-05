import requests
import os
import re
import time

def get_choice():
    choice = int(input("""
(1) get data about a player\n
(2) get data about a club\n
(3) get data about all brawler\n
(4) get the current game mode + map\n
(5) get the coins and powerpoints you spent\n
(6) get the percentage of how many brawler you have on lvl 11, lvl 10 ...\n
(7) Are you in the top 200 leaderboard of your country?
                       
your choice: """))
    return choice

def acc_data(headers, tag, url1, url2):
    try:
        os.mkdir("DATA Player")
    except:
        print("")
    url = url1+tag
    response = requests.get(url, headers=headers)
    data = response.json()
    response2 = requests.get(url2, headers=headers)
    data2 = response2.json()

    if response.status_code == 200 and response2.status_code == 200:
        brawler_existing = []
        brawler_collected = []
        for brawler in data2.get('items'):
            brawler_existing.append(brawler.get('name'))
        for brawler in data.get('brawlers'):
            brawler_collected.append(brawler.get('name'))
        brawler_not_collected = [element for element in brawler_existing if element not in brawler_collected]
        name = re.sub(r'[<>:"/\\|?*]', '_', data.get('name'))
        print(f"Name: {data.get('name')}")
        with open(f"DATA Player\\{name}.txt", "w", encoding="UTF-8") as f:
            f.write(f"tag: {data.get('tag')}\n")
            f.write(f"name: {data.get('name')}\n")
            f.write(f"trophies: {data.get('trophies')}\n")
            f.write(f"most trophies: {data.get('highestTrophies')}\n")
            f.write(f"club name: {data.get('club').get('name')}\n")
            f.write(f"club tag: {data.get('club').get('tag')}\n")
            f.write(f"3v3 victory: {data.get('3vs3Victories')}\n")
            f.write(f"Duo victory: {data.get('duoVictories')}\n")
            f.write(f"Solo victory: {data.get('soloVictories')}\n")
            f.write(f"collected brawler: {len(brawler_collected)}/{len(brawler_existing)}\n")
            f.write(f"not collected brawlers: {brawler_not_collected}\n")
            f.write("Brawler:")
            f.write("\n\n")
            for brawlers in data.get('brawlers'):
                f.write(f"name: {brawlers.get('name')}\n")
                f.write(f"\tbrawler ID: {brawlers.get('id')}\n")
                f.write(f"\tpower level: {brawlers.get('power')}\n")
                f.write(f"\trank: {brawlers.get('rank')}\n")
                f.write(f"\ttrophies: {brawlers.get('trophies')}\n")
                f.write(f"\thighest trophies: {brawlers.get('highestTrophies')}\n")
                f.write(f"\tgears:\n")
                for gears in brawlers.get('gears'):
                    f.write(f"\t\tgear ID: {gears.get('id')}\n")
                    f.write(f"\t\tname: {gears.get('name')}\n")
                    f.write("\n")
                f.write("\tstarpower:\n")
                for starpower in brawlers.get('starPowers'):
                    f.write(f"\t\tstarpower ID: {starpower.get('id')}\n")
                    f.write(f"\t\tname: {starpower.get('name')}\n")
                    f.write("\n")
                f.write("\tGadgets:\n")
                for gadgets in brawlers.get('gadgets'):
                    f.write(f"\t\tgadget ID: {gadgets.get('id')}\n")
                    f.write(f"\t\tname: {gadgets.get('name')}\n")
                    f.write("\n")
                f.write("\n")
    else:
        print("Error (maybe too much requests):", response.status_code)

def club_data(headers, tag, url1):
    url = url1 + tag
    url2= url + "/members"
    try:
        os.mkdir("DATA Club")
    except:
        print("")
    response = requests.get(url, headers=headers)
    data = response.json()
    response2 = requests.get(url2, headers=headers)
    data2 = response2.json()
    if response.status_code == 200:
        with open(f"DATA Club\\{data.get('name')}.txt", "w", encoding="UTF-8") as f:
            f.write(f"name: {data.get('name')}\n")
            f.write(f"tag: {data.get('tag')}\n")
            f.write(f"description: {data.get('description')}\n")
            f.write(f"type (open, closed...): {data.get('type')}\n")
            f.write(f"badge ID: {data.get('badgeId')}\n")
            f.write(f"total trophies: {data.get('trophies')}\n")
            f.write(f"required trophies: {data.get('requiredTrophies')}\n\n")
    else:
        print("Error")
    if response2.status_code == 200:
        with open(f"DATA Club\\{data.get('name')}.txt", "a", encoding="UTF-8") as f:
            for item in data2.get('items'):
                f.write(f"name: {item.get('name')}\n")
                f.write(f"player tag: {item.get('tag')}\n")
                f.write(f"name color: {item.get('nameColor')}\n")
                f.write(f"Clubrole: {item.get('role')}\n")
                f.write(f"trophies: {item.get('trophies')}\n")
                f.write(f"icon ID: {item.get('icon').get('id')}\n\n")    
    else:
        print("Error")

def brawler_data(headers, url):
    try:
        os.mkdir("DATA Brawler")
    except:
        print("")
    response = requests.get(url, headers=headers)
    data = response.json()
    with open("DATA Brawler\\Brawler.txt", 'w') as f:
        for brawler in data.get('items'):
            f.write(f"brawler ID: {brawler.get('id')}\n")
            f.write(f"name: {brawler.get('name')}\n")
            f.write(f"starpowers:\n")
            for starpower in brawler.get('starPowers'):
                f.write(f"\tstarpower ID: {starpower.get('id')}\n")
                f.write(f"\tname: {starpower.get('name')}\n\n")
            f.write("gadgets:\n")
            for gadget in brawler.get('gadgets'):
                f.write(f"\tgadget ID: {gadget.get('id')}\n")      
                f.write(f"\tname: {gadget.get('name')}\n\n")

def gamemode_map_data(headers, url):
    response = requests.get(url, headers=headers)
    data = response.json()
    if response.status_code == 200:
        for event in data:
            event_details = event.get('event')
            mode = event_details.get('mode') if event_details else None
            map_name = event_details.get('map') if event_details else None
            print(f"Mode: {mode}, Map: {map_name}")
    else:
        print("Error")

def progress_one(headers, url1, url2, tag):
    hypercharge_unlocked = int(input("How many Hypercharges unlocked?: "))
    normal_brawler = [16000000, 16000006, 16000007, 16000009, 16000013, 16000015, 16000018, 16000020, 16000024, 16000025, 16000026, 16000029, 16000030, 16000032, 16000035, 16000038, 16000039, 16000042, 16000044, 16000045, 16000047, 16000048, 16000049, 16000052, 16000054, 16000057, 16000060, 16000061, 16000062, 16000063, 16000064, 16000065, 16000066, 16000067, 16000068, 16000069, 16000070, 16000071, 16000072, 16000073, 16000074, 16000075, 16000076, 16000077, 16000078, 16000079, 16000080, 16000081]
    reaload_brawler = [16000027, 16000040, 16000046, 16000014, 16000003, 16000001, 16000004, 16000056, 16000050, 16000053]
    super_charge_brawler = [16000051, 16000058, 16000002, 16000043, 16000010, 16000034, 16000041, 16000036, 16000059, 16000037]
    pet_power_brawler = [16000007, 16000031, 16000008, 16000019, 16000017]
    mythic_gear_brawler = [16000022, 16000021, 16000012, 16000005, 16000023, 16000028, 16000040, 16000056, 16000016, 16000011]
    normal_gear_id = [62000000, 62000001, 62000002, 62000003, 62000004, 62000017]
    epic_gear_id = [62000006, 62000014, 62000005]
    mythic_gear_id = [62000007, 62000008, 62000009, 62000010, 62000011, 62000012, 62000013, 62000015, 62000016, 62000018]
    hyperchargecount = 30
    hypercharge_cost = 5000
    hypercharge_cost_overall = hyperchargecount * hypercharge_cost
    brawler_exist = []
    epic_gear_brawler = reaload_brawler + super_charge_brawler + pet_power_brawler
    gadget_count = 0
    starpower_count = 0
    gear_normal = 0
    gear_epic = 0
    gear_mythic = 0
    cost_overall = 0
    cost = 0
    powerpoints = 0
    upgrade_per_lvl = [[20, 20], [50, 55], [100, 130], [180, 270], [310, 560], [520, 1040], [860, 1840], [1410, 3090], [2300, 4965], [3740, 7765]]
    cost_overall_gold = 0
    cost_overall_power = 0
    url = url1+tag
    data = requests.get(url, headers=headers).json()
    data2 = requests.get(url2, headers=headers).json()
    for brawler in data2.get('items'):
        brawler_exist.append(brawler.get('id'))
    for brawler in brawler_exist:
        if brawler in normal_brawler and brawler not in epic_gear_brawler and brawler not in mythic_gear_brawler:
            cost=2*1000+2*2000+6*1000
        if brawler in epic_gear_brawler and brawler not in normal_brawler and brawler not in mythic_gear_brawler:
            cost=2*1000+2*2000+6*1000+1500
        if brawler in mythic_gear_brawler and brawler not in normal_brawler and brawler not in epic_gear_brawler:
            cost=2*1000+2*2000+6*1000+2000
        if brawler in mythic_gear_brawler and brawler in epic_gear_brawler and brawler not in normal_brawler:
            cost=2*1000+2*2000+6*1000+2000+1500 
        cost_overall+=cost
        cost_overall+=7765
        powerpoints+=3740
    cost_overall=cost_overall+hypercharge_cost_overall
    for brawler in data.get('brawlers'):
        for gadget in brawler.get('gadgets'):
            gadget_count+=1
        for starpower in brawler.get('starPowers'):
            starpower_count+=1
        for gear in brawler.get('gears'):
            if gear.get('id') in normal_gear_id:
                gear_normal+=1
            if gear.get('id') in epic_gear_id:
                gear_epic+=1
            if gear.get('id') in mythic_gear_id:
                gear_mythic+=1
        if brawler.get('power')==1:
            continue
        else:
            upgrade_power,upgrade_gold=upgrade_per_lvl[brawler.get('power')-2]
            cost_overall_power+=upgrade_power
            cost_overall_gold+=upgrade_gold
    cost_overall_gold=cost_overall_gold+gadget_count*1000+starpower_count*2000+gear_normal*1000+gear_epic*1500+gear_mythic*2000+hypercharge_unlocked*hypercharge_cost
    print(f"required coins: {cost_overall}, required powerpoints: {powerpoints}")
    print(f"Coins spent: {cost_overall_gold}, Powerpoints spent: {cost_overall_power}")
    print(f"percent coins: {round(cost_overall_gold/cost_overall*100, 2)}%, percent powerpoints: {round(cost_overall_power/powerpoints*100, 2)}%")

def progress_two(headers, url1, url2, tag):
    url = url1+tag
    lvl1=[]
    lvl2=[]
    lvl3=[]
    lvl4=[]
    lvl5=[]
    lvl6=[]
    lvl7=[]
    lvl8=[]
    lvl9=[]
    lvl10=[]
    lvl11=[]
    brawler_exist=[]
    brawler_collected=[]
    try:
        r2 = requests.get(url2, headers=headers)
        r2.raise_for_status()
        data2 = r2.json()
        for brawler in data2.get('items'):
            brawler_exist.append(brawler.get('name'))
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()
        for brawler in data.get('brawlers'):
            brawler_collected.append(brawler.get('name'))
        not_unlocked = [element for element in brawler_exist if element not in brawler_collected]

        for brawler in data.get('brawlers'):
            if int(brawler.get('power'))==1:
                lvl1.append(brawler.get('name'))
            elif int(brawler.get('power'))==2:
                lvl2.append(brawler.get('name'))
            elif int(brawler.get('power'))==3:
                lvl3.append(brawler.get('name'))
            elif int(brawler.get('power'))==4:
                lvl4.append(brawler.get('name'))
            elif int(brawler.get('power'))==5:
                lvl5.append(brawler.get('name'))
            elif int(brawler.get('power'))==6:
                lvl6.append(brawler.get('name'))
            elif int(brawler.get('power'))==7:
                lvl7.append(brawler.get('name'))
            elif int(brawler.get('power'))==8:
                lvl8.append(brawler.get('name'))
            elif int(brawler.get('power'))==9:
                lvl9.append(brawler.get('name'))
            elif int(brawler.get('power'))==10:
                lvl10.append(brawler.get('name'))
            elif int(brawler.get('power'))==11:
                lvl11.append(brawler.get('name'))
            else:
                continue

        print(f"lvl 11: {lvl11}, {str(len(lvl11)/len(brawler_exist)*100)}%")
        print(f"lvl 10: {lvl10}, {str(len(lvl10)/len(brawler_exist)*100)}%")
        print(f"lvl 9: {lvl9}, {str(len(lvl9)/len(brawler_exist)*100)}%")
        print(f"lvl 8: {lvl8}, {str(len(lvl8)/len(brawler_exist)*100)}%")
        print(f"lvl 7: {lvl7}, {str(len(lvl7)/len(brawler_exist)*100)}%")
        print(f"lvl 6: {lvl6}, {str(len(lvl6)/len(brawler_exist)*100)}%")
        print(f"lvl 5: {lvl5}, {str(len(lvl5)/len(brawler_exist)*100)}%")
        print(f"lvl 4: {lvl4}, {str(len(lvl4)/len(brawler_exist)*100)}%")
        print(f"lvl 3: {lvl3}, {str(len(lvl3)/len(brawler_exist)*100)}%")
        print(f"lvl 2: {lvl2}, {str(len(lvl2)/len(brawler_exist)*100)}%")
        print(f"lvl 1: {lvl1}, {str(len(lvl1)/len(brawler_exist)*100)}%")
        print(f"not unlocked: {not_unlocked}, {str(len(not_unlocked)/len(brawler_exist)*100)}%")

    except requests.exceptions.RequestException as e:
        print("Error fetching data from the Brawl Stars API:", e)
    except Exception as e:
        print("An error occurred:", e)

def rank(headers, url1, url2, tag, region):
    try:
        os.mkdir("DATA rank")
    except:
        print("")
    try:
        with_n_rank=int(input("with brawler without rank (1): "))
        os.system('cls')
    except:
        with_n_rank=None
        os.system('cls')
    url=url1+tag
    x=0
    brawler_collected=[]
    r=requests.get(url=url, headers=headers)
    data=r.json()
    for brawler in data.get('brawlers'):
        brawler_collected.append(brawler.get('name'))
        name = re.sub(r'[<>:"/\\|?*]', '_', data.get('name'))
    with open(f"DATA rank\\{name}_rank.txt", "w", encoding="utf-8") as f:
        f.write(f"player: {data.get('name')}\n")
        f.write(f"tag: {data.get('tag')}\n\n")
        for brawler in data.get('brawlers'):
            x+=1
            found=False
            print(f"{str(x)}/{str(len(brawler_collected))}")
            brawlerid=brawler.get('id')
            url_two=url2+region+"/brawlers/"+str(brawlerid)
            r2=requests.get(url=url_two, headers=headers)
            data2=r2.json()
            for item in data2.get('items'):
                if f"#{tag}" in item.get('tag'):
                    print(f"brawler: {brawler.get('name')}")
                    print(f"trophies: {item.get('trophies')}")
                    print(f"rank: {item.get('rank')}\n")
                    f.write(f"brawler: {brawler.get('name')}\n")
                    f.write(f"\ttrophies: {item.get('trophies')}\n")
                    f.write(f"\trank: {item.get('rank')}\n\n")
                    found=True
            if found==False:
                print(f"brawler: {brawler.get('name')}")
                print(f"trophies: -")
                print(f"rank: -\n")
                if with_n_rank==1:
                    f.write(f"brawler: {brawler.get('name')}\n")
                    f.write(f"\ttrophies: -\n")
                    f.write(f"\trank: -\n\n")
            time.sleep(2)

if __name__ == "__main__":
    player_url = "https://api.brawlstars.com/v1/players/%23"
    brawler_url = "https://api.brawlstars.com/v1/brawlers/"
    club_url = "https://api.brawlstars.com/v1/clubs/%23"
    gamemode_map_url = "https://api.brawlstars.com/v1/events/rotation"
    rank_url = "https://api.brawlstars.com/v1/rankings/"
    with open("api_key.txt", "r", encoding="utf-8") as f:
        api_key = f.read().strip()
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    while True:
        os.system('cls')
        choice = get_choice()
        print("\n")
        if choice == 1:
            tag = input("Enter your player tag without # (e.g CGQCYJGY): ")
            acc_data(headers=headers, tag=tag, url1=player_url, url2=brawler_url)
            print("\n")
            print("Finished look in the folder DATA Player")
        elif choice == 2:
            tag = input("Enter your club tag without # (e.g. 2CCQ99U88): ")
            club_data(headers=headers, tag=tag, url1=club_url)
            print("\n")
            print("Finished look in the folder DATA Club")
        elif choice == 3:
            brawler_data(headers=headers, url=brawler_url)
            print("\n")
            print("Finished look in the folder DATA Brawler")
        elif choice == 4:
            gamemode_map_data(headers=headers, url=gamemode_map_url)
        elif choice == 5:
            tag = input("Enter your player tag without # (e.g CGQCYJGY): ")
            progress_one(headers=headers, url1=player_url, url2=brawler_url, tag=tag)
        elif choice == 6:
            tag = input("Enter your player tag without # (e.g CGQCYJGY): ")
            print("\n")
            progress_two(headers=headers, url1=player_url, url2=brawler_url, tag=tag)
        elif choice == 7:
            tag = input("Enter your player tag without # (e.g CGQCYJGY): ")
            region = input("enter your country code (e.g. Germany DE, Unisted Stats US): ")
            rank(headers=headers, url1=player_url, url2 = rank_url, tag=tag, region=region)
            print("Finished look in DATA rank")
        while True:
            another = input("\nDo you want to get other data? (y/n): ")
            if another == "y":
                break
            elif another == "n":
                break
            else:
                print("Choose between y and n")
        if another == "n":
            os.system("cls")
            print("Thx for using this program c:")
            break
