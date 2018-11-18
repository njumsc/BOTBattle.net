import random


# import string

def randomUser():
    userNames = [
        "jack",
        "mike",
        "lilly",
        "alice",
        "franky",
        "carl",
        "linus",
        "jobs",
        "zark",
        "tao"
    ]
    retval = {
        # "userName": random.sample(string.ascii_letters, 8),
        "userName": random.choice(userNames),
        "userAct": [
            random.random() * 100,
            random.random() * 100
        ]
    }
    return retval


def randomUsers():
    userNames = [
        "jack",
        "mike",
        "lilly",
        "alice",
        "franky",
        "carl",
        "linus",
        "jobs",
        "zark",
        "tao"
    ]
    n = random.randint(1, 10)
    retval = {
        "userNum": n,
        "users": []
    }
    for i in range(n):
        name = random.choice(userNames)
        userNames.remove(name)
        retval['users'].append({
            # "userName": random.sample(string.ascii_letters, 8),
            "userName": name,
            "userAct": [
                random.random() * 100,
                random.random() * 100
            ]
        })
    return retval
