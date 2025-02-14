import glob

files = glob.glob("./data/indices/*.xml")


patterns = [
    ("&amp;#34;", "»"),
    ("&amp;#39;", "ߴ")
]
for x in files:
    with open(x, "r", encoding="utf-8") as file:
        content = file.read()

    for y in patterns:
        content = content.replace(y[0], y[1])

    with open(x, "w", encoding="utf-8") as file:
        file.write(content)
