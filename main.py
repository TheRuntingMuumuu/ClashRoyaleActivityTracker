import requests, csv, datetime, time

API_KEY = "PLACE_API_KEY_HERE"

PLAYER_TAGS = {"OWEN":"P20PU***","USER2":"123456789"}  # do not include hash

# sets person who we are using. If chainging this, YOU MUST DELETE THE "activityInfo" FILE OR IT WILL BREAK EVERYTHING!!!
person = "OWEN"

def getData():
    """
    str->Dict or None
    Gets the CR data from the server.
    """

    player_tag = PLAYER_TAGS[person]
    url = f"https://api.clashroyale.com/v1/players/%23{player_tag}"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text) 
        return None

def log(data, filename):
    """
    Data, Filename->None
    Writes inputted data to the given file
    """
    with open(filename, "w") as file:
        file.write(str(data))
        file.close()

def getOldBattleInfo(battleCount, donations):
    """
    (int,int)-> Tuple(int,int)
    returns the old battle count and old donations, takes in the battlecount and donations
    """
    # loops in case the file does not exist
    while True:
        try:
            # writes data to file
            with open("activityInfo", "r+") as file:
                fileContents = file.read()
                oldBattleCount, oldDonations = fileContents.split()
                file.close()
            break
        # if the file does not exist
        except FileNotFoundError:
            writeBattleInfo(battleCount, donations)

    return (int(oldBattleCount), int(oldDonations))

def writeBattleInfo(battleCount, donations):
    """
    int, int-> None
    writes the battlecount and donations to file
    """
    with open("activityInfo", "w") as file:
            # write all necessary information
            file.write(str(battleCount))
            file.write(" ")
            file.write(str(donations))
            file.close()

def writeTimeStamp(note=""):
    """
    str->str
    Writes the current timestamp to a CSV file, also writes an optional str to the end of the row. Returns current timestamp
    """
    with open('activity.csv', 'a', newline="") as file:
        csv.writer(file).writerow([datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp()).strftime('%Y-%m-%d %H:%M:%S'),note])

    return datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp()).strftime('%Y-%m-%d %H:%M:%S')


def isActive():
    """
    None->bol
    Returns true if person is active within the last 10 minutes, False if they have not been active. 
    """
    # gets data
    data = getData()

    # checks if data is valid
    if data == None:
        return None

    # writes data to log file
    log(data, "player_data.txt")

    # gets current battle and donation information
    battleCount = data.get("battleCount")
    donations = data.get("totalDonations")

    # gets old battle count and donation information
    oldBattleCount, oldDonations = getOldBattleInfo(battleCount, donations)

    # writes new battlecount and donation to file
    writeBattleInfo(battleCount, donations)

    # checks if the informatino has change, if so, they have been recently active. 
    if not (oldBattleCount==battleCount and oldDonations == donations):
        return True
    else:
        return False

def main():
    while True:
        if isActive():
            timestamp = writeTimeStamp(person)
            print(f'{person} is active right now at {timestamp}')
        time.sleep(5)


# runs main
if __name__ == "__main__":
    main()