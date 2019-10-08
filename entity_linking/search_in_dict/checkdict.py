import json
synonymsDict = dict()
ambiguationDict = dict()
f_w = open('checkdict', "w+", encoding="utf-8")


def loaddict():
    with open("synonymsDict.txt", "r", encoding='utf-8') as file_sdict:
        for sdict_i in file_sdict.readlines():
            string = str(sdict_i)
            key = string[:string.find("||")].strip()
            value = string[string.find("||") + 2:].strip()
            synonymsDict[key] = value

    print("synonymsDict.txt finished")

    with open("ambiguationDict.txt", "r", encoding='utf-8') as file_adict:
        for adict_i in file_adict.readlines():
            string = str(adict_i)
            key = string[:string.find("||")].strip()
            value = string[string.find("||") + 2:].strip().split("\t|\t")
            ambiguationDict[key] = value

    print("ambiguationDict.txt finished")

def findindict(entity1, entity1_label):
    entityinsDict = '-1'
    entityinaDict = list()
    yesornot = 'yes'


    entityinsDict = synonymsDict.get(entity1, "-1")
    if entityinsDict != "-1":
        print("finded in synonymsDict!!")
        entityinaDict = ambiguationDict.get(entityinsDict, "-1")
    else:
        print("NOT!! finded in synonymsDict!!")
        entityinaDict = ambiguationDict.get(entity1, "-1")
        if "-1" in entityinaDict: print("NOT!! finded in synonymsDict and ambiguationDict!!")

    if entityinsDict == "-1" and "-1" in entityinaDict:
        print("the entity not in dict!")
        yesornot = "not"
    else:
        if entityinsDict == entity1 or (entity1 in entityinaDict):
            print("the entity find in dict!")

    f_w.writelines(yesornot + "," + str(entity1_label) +","+ str(entity1) +","+ str(entityinsDict) +","+ " ".join(entityinaDict) + "\n")
    return entityinsDict, entityinaDict, yesornot


loaddict()
with open("../data/Lc_Quad-test.json", "r", encoding='utf-8') as file_data:
        yesornot = ''
        count = 0
        data = json.loads(file_data.read())
        for data_i in data:
            id = str(data_i['id'])

            entity1 = str(data_i['entity1_uri']).lower()
            entity1 = entity1[entity1.rfind('/') + 1:]
            entity1_label = str(data_i['entity1_mention']).replace(",", ' ').lower().replace(" ", "_")

            entity2 = str(data_i['entity2_uri']).lower()
            entity2 = entity2[entity2.rfind('/') + 1:]
            entity2_label = str(data_i['entity2_mention']).replace(",", ' ').lower().replace(" ", "_")

            if entity1 != '' and entity1_label != '':
                entity1insDict, entity1inaDict, yesornot = findindict(entity1, entity1_label)

                if yesornot == 'yes':
                    count = count + 1

            if entity2 != '' and entity2_label != '':
                entity2insDict, entity2inaDict, yesornot = findindict(entity2, entity2_label)

                if yesornot == 'yes':
                    count = count + 1

        print(count)
