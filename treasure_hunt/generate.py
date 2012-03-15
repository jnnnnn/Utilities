import csv

with open("template.html") as t:
    template = "".join(list(t.readlines()))
    
with open("clues.csv") as f:
    reader = csv.reader(f.readlines())
    fields = ""
    for line in reader:
        print(reader.line_num)
        if reader.line_num == 1:            
            fields = line
        else:
            contents = template[:]
            for i, field in enumerate(fields):
                print('replacing {0} with {1}'.format(field, line[i]))
                contents = contents.replace(field, line[i])
            with open(line[1]+".html", 'w') as fw:
                fw.write(contents)
                print("wrote "+line[1]+".html")
                
        
