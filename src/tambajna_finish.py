contours = {
    ("H","H"):'^',("H","M"):"\\",("H","L"):'\\',
    ("M","H"):'/',("M","M"):"",("M","L"):'\\',
    ("L","H"):'/',("L","M"):"/",("L","L"):''
    }

def split(string):
    splits = []
    state = 0
    current = tone = ""
    for letter in string:
        if letter in ",'":
            state = 1
        if state == 1 and letter in "aeiu":
            splits += [current,tone if tone else "M"]
            state = 0
            current = tone = ""
        if letter not in "HL":
            current += letter
        elif not(tone):
            tone = letter
    splits += [current,tone if tone else "M"]
    return splits

def finish(string):
    segments = split(string)
    segments[1:-1:2] = [contours[mix] for mix in zip(segments[1::2],segments[3::2])]
    del segments[-1]
    return "".join(segments)