def read_scores(filename):
    fd = open(filename,'r')
    dic = {}
    for line in fd:
        line = line.strip()
        if line:
            key,val = line.split(',')
            if val.isdigit():
                dic[key] = int (val)
    fd.close()
    return dic
def get_score(scores, word):
    score = 0
    for letter in word:
        score += scores[letter]
    return score
    
scores = read_scores('scrabble_scores.txt')
get_score(scores, 'quack')


def read_config(filename):
    fd = open (filename,'r')
    output = {}
    section = ""
    details = {}
    for line in fd:
        line = line.strip()
        if line:
            if line.startswith('['):
                if details != {}:
                    output[section] = details
                section = line[1:-1]
                details = {}
            else:
                line = line.split('=')
                details[line[0]] = line[1]
    if details != {}:
        output[section] = details
    fd.close()
    return output

def get_value

             
