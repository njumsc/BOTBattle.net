import random
import json

if __name__ == "__main__":
    with open("data_last.json", "w") as readFile:
        readJson = json.loads(readFile.read())
        goldennums = readJson['goldenNums']
        userActs = readJson['userActs']

    print("Do something here")

    with open("rsl_last.json", 'w') as writeFile:
        writeJson = {
            "num1": random.random() * 100,
            "num2": random.random() * 100
        }
        writeFile.write(json.dumps(writeJson, indent=4))