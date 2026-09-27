import requests
import base64

def _getDifficultyString(difficultyInt: int = 0, isDemon: bool = False):
    if isDemon:
        match difficultyInt:
            case -1:
                return "autoDemon"
            case 0:
                return "unratedDemon"
            case 1 | 10:
                return "easyDemon"
            case 2 | 20:
                return "mediumDemon"
            case 3 | 30:
                return "hardDemon"
            case 4 | 40:
                return "insaneDemon"
            case 5 | 50:
                return "extremeDemon"
            case _:
                return "unknownDemon"
    else:
        match difficultyInt:
            case -1:
                return "auto"
            case 0:
                return "unrated"
            case 1 | 10:
                return "easy"
            case 2 | 20:
                return "normal"
            case 3 | 30:
                return "hard"
            case 4 | 40:
                return "harder"
            case 5 | 50:
                return "insane"
            case _:
                return "unknown"

def parseLevelData(dataString: str, includeLevelString: bool = True):
    rawSplitTable = dataString.split(":")
    rawDict = {rawSplitTable[i]: rawSplitTable[i+1] for i in range(0, len(rawSplitTable)-1, 2)}
    fixedTable = {
        "id": rawDict.get("1", "Unknown"),
        "levelName": rawDict.get("2", "Unknown"),
        "description": rawDict.get("3", "Unknown"),
        "descriptionDecoded": base64.b64decode(rawDict.get("3", "Unknown")),
        "levelString": rawDict.get("4", "Unknown") if includeLevelString else "[Excluded]",
        "version": rawDict.get("5", "Unknown"),
        "playerID": rawDict.get("6", "Unknown"),
        "difficultyDenominator": rawDict.get("8", "Unknown"),
        "difficultyNumerator": rawDict.get("9", "Unknown"),
        "difficultyInt": int(int(rawDict.get("9", 0)) / int(rawDict.get("8", 1))) if int(rawDict.get("8", 0)) != 0 else 0,
        "difficultyString": _getDifficultyString(int(int(rawDict.get("9", 0)) / int(rawDict.get("8", 1))) if int(rawDict.get("8", 0)) != 0 else 0, rawDict.get("17", False)),
        "downloads": rawDict.get("10", "Unknown"),
        "setCompletes": rawDict.get("11", "Unknown"),
        "officialSong": rawDict.get("12", "Unknown"),
        "gameVersion": rawDict.get("13", "Unknown"),
        "likes": rawDict.get("14", "Unknown"),
        "length": rawDict.get("15", "Unknown"),
        "dislikes": rawDict.get("16", "Unknown"),
        "demon": rawDict.get("17", "Unknown"),
        "stars": rawDict.get("18", "Unknown"),
        "featureScore": rawDict.get("19", "Unknown"),
        "auto": rawDict.get("25", "Unknown"),
        "recordString": rawDict.get("26", "Unknown"),
        "password": rawDict.get("27", "Unknown"),
        "uploadDate": rawDict.get("28", "Unknown"),
        "updateDate": rawDict.get("29", "Unknown"),
        "copiedID": rawDict.get("30", "Unknown"),
        "twoPlayer": rawDict.get("31", "Unknown"),
        "customSongID": rawDict.get("35", "Unknown"),
        "extraString": rawDict.get("36", "Unknown"),
        "coins": rawDict.get("37", "Unknown"),
        "verifiedCoins": rawDict.get("38", "Unknown"),
        "starsRequested": rawDict.get("39", "Unknown"),
        "lowDetailMode": rawDict.get("40", "Unknown"),
        "dailyNumber": rawDict.get("41", "Unknown"),
        "epic": rawDict.get("42", "Unknown"),
        "demonDifficulty": rawDict.get("43", "Unknown"),
        "isGauntlet": rawDict.get("44", "Unknown"),
        "objects": rawDict.get("45", "Unknown"),
        "editorTime": rawDict.get("46", "Unknown"),
        "editorTime(Copies)": rawDict.get("47", "Unknown"),
        "settingsString": rawDict.get("48", "Unknown"),
        "songIDs": rawDict.get("52", "Unknown"),
        "sfxIDs": rawDict.get("53", "Unknown"),
        "unknownValue": rawDict.get("54", "Unknown"),
        "verificationTime": rawDict.get("57", "Unknown"),
    }
    
    return fixedTable
    
def getLevel(id: int, includeLevelString: bool = True):
    url = "http://www.boomlings.com/database/downloadGJLevel22.php"

    payload = {
        "secret": "Wmfd2893gb7",
        "gameVersion": "22",
        "binaryVersion": "47",
        "levelID": id,
        "inc": "1",
        "extras": "1"
    }

    headers = {
        "User-Agent": "",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": "gd=1;",
        "Host": "www.boomlings.com"
    }

    serverResponse = requests.post(url, data=payload, headers=headers)
    serverText = serverResponse.text
    levelData = parseLevelData(serverText, includeLevelString)

    return levelData