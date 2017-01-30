# Get nationality

import re
import csv
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

def get_from_to_max(st):
    res = map(int, get_from_to(st))
    if len(res) == 0:
        return None
    else:
        return max(res)
    
def get_birthdate(page):
    candidates = [get_from_to_max(a) for a in page.split("\n") if "Birth date|" in a or "| birth date" in a or "| birth_date" in a or "|birth_date" in a]
    return candidates[0] if len(candidates) > 0 else None

def get_deathdate(page):
    candidates = [get_from_to_max(a) for a in page.split("\n") if "Death date|" in a or "| death date" in a or "| death_date" in a or "|death_date" in a]
    return candidates[0] if len(candidates) > 0 else None

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

def get_he_she_count(page):
    # Find where the early life starts
    candidates = [page.find("===Early life==="),
                  page.find("== Early life =="),
                  page.find("==Early life=="),
                  page.find("==Early years=="),
                  page.find("==Life=="),
                  page.find("==Personal life=="),
                  page.find("Reign"),
                  page.find("==Childhood and early life=="),
                  page.find("==Children==")]
    
    candidates = [c for c in candidates if c > -1]
    early_life = min(candidates) if len(candidates) > 0 else -1
    if early_life == -1:
        page_subset = page[:10000]
    else:
        page_subset = page[:min(early_life, 10000)]

    hec = page_subset.count("He ") + page_subset.count(" he ") + page_subset.count("His") + page_subset.count(" his ")
    shec = page_subset.count("She ") + page_subset.count(" she ") + page_subset.count("Her ") + page_subset.count(" her ")
    
    hec -= page_subset.count("his death")
    shec -= page_subset.count("her death")

    return (hec, shec)

def classify_gender(page):
    hec, shec = get_he_she_count(page)
    if (hec + shec) == 0 or  float(hec)/(hec + shec) > 0.5:
        return "male"
    else:
        return "female"

result_tuples = []
with open("enwiki-20170120-pages-articles.xml") as input_file:
    l = input_file.readline().strip()
    while(l != "<page>"):
        l = input_file.readline().strip()
        #print(l)
    page = (read_page(input_file))
    while( True ):
        page = read_page(input_file)
        if len(page) < 10: break
        if ("spouse" in page.lower()):
            if len(get_spouse(page)) > 0:
                name = page[17:59].split("<")[0].replace(",","#")
                birth_year = get_birthdate(page)
                death_year = get_deathdate(page)
                hec, shec = get_he_she_count(page)
                gender = classify_gender(page)
                #print(name, birth_year, death_year, classify_gender(page))
                if (len(result_tuples) % 500 == 0):
                    print(len(result_tuples))
                spouses = get_spouse(page)
                nmarriages = len(spouses)
                lens = [int(x[1]) - int(x[0]) for x in spouses]
                max_duration = max(lens)
                min_duration = min(lens)
                avg_duration = float(sum(lens)) / nmarriages
                article_size = len(page)
                result_tuples.append((name, birth_year, death_year,
                                      gender, hec, shec, nmarriages,
                                      max_duration, min_duration,
                                      avg_duration, article_size))


with open('data.csv','wb') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['name','birth_year', 'death_year',
                      'gender', 'hec', 'shec', 'nmarriages',
                      'max_duration', 'min_duration',
                      'avg_duration', 'article_size'])
    for row in result_tuples:
        csv_out.writerow(row)
        
f = open("bla.txt", "w")
f.writelines(page)
f2 = open("bla3.txt", "w")
f2.writelines(page[:3359])

    
