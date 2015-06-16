def find_functions(filename):
    fin = open(filename,'r')
    #fout = open('functions.txt','w')
    output=[]
    
    for lines,count in enumerate(fin):
        if lines.startswith('def '):
            output.append([count+1,lines[4:lines.find('(')]],lines[lines.find(')')+1:lines:find(')')])
            #fout.write(lines)
    
    fin.close()
    #fout.close()
    return output
