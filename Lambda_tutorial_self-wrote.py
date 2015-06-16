def find_numbers(text):
    result=[]
    words=text.split()
    for word in words:
        if word.isdigit():
            result.append(int(word))
    return result

find_numbers3 = lambda text: [int(word) for word in text.split() if word.isdigit()]

def seperate(n):
    return lambda text: text.split(n)
