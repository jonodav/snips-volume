def ctFromColor(setColor):
        if setColor == "natural":
            return "512"
        if setColor == "warm":
            return "0"
        if setColor == "cool":
            return "1023"
        else:
            return "fail"
    
def rgbctFromColor(setColor):
    if setColor == "natural":
        return "0,0,0,255,255"
    if setColor == "warm":
        return "0,0,0,255,0"
    if setColor == "cool":
        return "0,0,0,0,255"
    if setColor == "blue":
        return "0,0,255,0,0"
    if setColor == "green":
        return "0,255,0,0,0"
    if setColor == "red":
        return "255,0,0,0,0"
    if setColor == "cyan":
        return "0,255,255,0,0"
    if setColor == "yellow":
        return "255,255,0,0,0"
    if setColor == "pink":
        return "255,0,255,0,0"
    else:
        return "fail"

def rgbFromColor(setColor):
    if setColor == "natural":
        return "255,255,255"
    if setColor == "warm":
        return "255,255,200"
    if setColor == "cool":
        return "230,230,255"
    if setColor == "blue":
        return "0,0,255"
    if setColor == "green":
        return "0,255,0"
    if setColor == "red":
        return "255,0,0"
    if setColor == "cyan":
        return "0,255,255"
    if setColor == "yellow":
        return "255,255,0"
    if setColor == "pink":
        return "255,0,255"
    else:
            return "fail"