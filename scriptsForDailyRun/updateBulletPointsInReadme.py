
def updateBulletPoints():
    with open("README.md", "r") as f:
        text = f.read()
    startMarker = '<!-- BulletPointStart -->'
    endMarker = '<!-- BulletPointEnd -->'
    start = text.find(startMarker)
    end = text.find(endMarker)
    firstHalf = text[:start + len(startMarker)]
    secondHalf = text[end :]
    with open("./articles/bulletPointSummary.txt", "r") as f:
        bulletPoints = f.read()

    with open("README.md", "w") as f:
        f.write(firstHalf +"\n"+bulletPoints+"\n" +secondHalf)