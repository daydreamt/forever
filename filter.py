# Some ideas: get brithdate
# Get number of marriages
# with min, max, mean
# Then make dataset

import re
def read_page(input_stream):
    page = ""
    l = input_stream.readline().strip()
    while(l != "<page>"):
        l = input_file.readline().strip()
        #print(l)
    while(l.strip() != "</page>"):
        page += l
        l = input_file.readline()
    page += l
    return page

def get_from_to(st):
    return re.findall(r'\d+', st)

def get_spouse(page):
    spouse_lines = []
    all_lines = [s for s in page.split("\n")]
    for idx, line in enumerate(all_lines):
        if "| spouse " in line or "|spouse" in line:
            if "Plainlist" in line:
                for line in range((idx+1), len(all_lines)):
                    if "*" in all_lines[line]:
                        spouse_lines.append(all_lines[line])
                    else:
                        break
            else:
                if ("=" in line) and (line.split("=")[1].strip() != ""):
                    spouse_lines.append(line)
                    if "|" not in all_lines[idx + 1]:
                        spouse_lines.append(all_lines[idx + 1])

    spouse_lines = [s.replace("\xe2\x80\x93", "-") for s in spouse_lines]
    res_spouses = []
    
    for line in spouse_lines:
        fgt = (get_from_to(line))
        if len(fgt) == 2:
            fr = str(fgt[0])
            to = str(fgt[1])
            if len(fr) == 4 and len(to) == 2:
                to = fr[0:2] + to
            if len(fr) == len(to):
                res_spouses.append((fr, to))

    #print(len(spouse_lines))
    return res_spouses

with open("enwiki-20170120-pages-articles.xml") as input_file:
    spouse_dict = dict()
    l = input_file.readline().strip()
    while(l != "<page>"):
        l = input_file.readline().strip()
        #print(l)
    page = (read_page(input_file))
    while( len(blas) < 10000 ):
        page = read_page(input_file)
        if ("spouse" in page.lower()):
            if len(get_spouse(page)) > 0:
                blas.append(page)
                name = page[17:59].split("<")[0] 
                print(name)
                spouses = get_spouse(page)
                spouse_dict[name] = spouses
    f = open("bla.txt", "w")
    f.writelines(page)

    
