def is_dna(string):
    str1 = 'ATCG'
    if len(string) % 3 !=0:
        return False
    for c in string:
        if c not in str1:
            return False
        else:
            return True

def reverse_complement(dna):
    if not is_dna(dna):
        return ('None')
    else:
        comp = ''
        for c in dna:
            if c == 'A':
                comp += 'T'
            elif c == 'T':
                comp += 'A'
            elif c == 'G':
                comp += 'C'
            elif c == 'C':
                comp += 'G'                            
    return comp[::-1]

def print_codons(dna):
    if not is_dna(dna):
        return None
    i = 0
    while(i != len(dna)):
        print (dna[i,i+3])
        i += 3

def get_number(string):
    number = ''
    found = False
    for c in string:
        if c.isdigit():
            number += c
            found = True
        elif found == True:
            break
    return number
    
