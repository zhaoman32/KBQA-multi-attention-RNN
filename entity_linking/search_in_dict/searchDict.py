import json
import difflib
from similarity.normalized_levenshtein import NormalizedLevenshtein


synonymsDict = dict()
ambiguationDict = dict()
f_w = open('entityindictnolike.csv', "w+", encoding="utf-8")
# f_not = open('not.txt', "w+", encoding="utf-8")


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


    entityinsDict = synonymsDict.get(entity1_label, "-1")
    if entityinsDict != "-1":
        print("finded in synonymsDict!!")
        entityinaDict = ambiguationDict.get(entityinsDict, "-1")
    else:
        print("NOT!! finded in synonymsDict!!")
        entityinaDict = ambiguationDict.get(entity1_label, "-1")
        if "-1" in entityinaDict: print("NOT!! finded in synonymsDict and ambiguationDict!!")

    if entityinsDict == "-1" and "-1" in entityinaDict:
        print("the entity not in dict!")
        yesornot = "not"
    else:
        if entityinsDict == entity1 or (entity1 in entityinaDict):
            print("the entity find in dict!")

    f_w.writelines(yesornot + "," + str(entity1_label) +","+ str(entity1) +","+ str(entityinsDict) +","+ " ".join(entityinaDict) + "\n")
    return entityinsDict, entityinaDict, yesornot


def searchwithjson():
    with open("../../data/Lc_Quad-test.json", "r", encoding='utf-8') as file_data:
        yesornot = ''
        count = 0
        data = json.loads(file_data.read())
        for data_i in data:
            id = str(data_i['id'])

            entity1 = str(data_i['entity1_uri']).lower()
            entity1 = entity1[entity1.rfind('/') + 1:]
            entity1_label = str(data_i['entity1_mention']).lower().replace(" ", "_")

            entity2 = str(data_i['entity2_uri']).lower()
            entity2 = entity2[entity2.rfind('/') + 1:]
            entity2_label = str(data_i['entity2_mention']).lower().replace(" ", "_")

            if entity1 != '' and entity1_label != '':
                entity1insDict, entity1inaDict, yesornot = findindict(entity1, entity1_label)

                if yesornot == 'yes':
                    count = count + 1

            if entity2 != '' and entity2_label != '':
                entity2insDict, entity2inaDict, yesornot = findindict(entity2, entity2_label)

                if yesornot == 'yes':
                    count = count + 1

        print(count)



def searchwithlink():
    with open("linkmention", "r", encoding='utf-8') as file_data:
        yesornot = ''
        count = 0

        for data_i in file_data.readlines():
            entity_label = str(data_i).strip('\n').strip().lower().replace(" ", "_")
            if entity_label != '':

                entityinsDict = '-1'
                entityinaDict = list()
                yesornot = 'yes'

                entityinsDict = synonymsDict.get(entity_label, "-1")
                if entityinsDict != "-1":
                    print("finded in synonymsDict!!")
                    entityinaDict = ambiguationDict.get(entityinsDict, "-1")
                else:
                    print("NOT!! finded in synonymsDict!!")
                    entityinaDict = ambiguationDict.get(entity_label, "-1")
                    if "-1" in entityinaDict: print("NOT!! finded in synonymsDict and ambiguationDict!!")

                if entityinsDict == "-1" and "-1" in entityinaDict:
                    print("the entity not in dict!")
                    if synonymsDict.get(entity_label.strip('of_').strip('_of'), "-1") != '-1': count = count + 1
                    else: yesornot = "not"
                else:
                    count = count + 1
                    print("the entity find in dict!")

                # if yesornot == "not":
                #     f_not.writelines(str(entity_label)+"\n")

                    # for (k,v) in synonymsDict.items():
                    #     a,b,c = searchlike(entity_label,str(k))
                    #     if a >= 0.85 or b >= 0.9 or c >=0.9:
                    #         yesornot = 'yes'
                    #         entityinsDict = v
                    #         count = count + 1
                    #         break

                f_w.writelines(yesornot + "," + str(entity_label) + "," + str(
                    entityinsDict) + "," + " ".join(entityinaDict) + "\n")

        print(count)

def Jaccrad(model, reference):  # terms_reference为源句子，terms_model为候选句子
       grams_reference = reference.split('_')
       grams_model = model.split('_')
       temp = 0
       for i in grams_reference:
           if i in grams_model:
               temp = temp + 1
       fenmu = len(grams_model) + len(grams_reference) - temp  # 并集
       jaccard_coefficient = float(temp / fenmu)  # 交集
       return jaccard_coefficient

def searchlike(query_str,s1):


    # 字面量相似度
    #print(difflib.SequenceMatcher(None, query_str, s1).quick_ratio())
    # 编辑距离
    normalized_levenshtein = NormalizedLevenshtein()
    #print(normalized_levenshtein.similarity(query_str, s1))
    #杰卡德相似度
    jaccard_coefficient = Jaccrad(query_str, s1)
    #print(jaccard_coefficient)

    return difflib.SequenceMatcher(None, query_str, s1).quick_ratio(), normalized_levenshtein.similarity(query_str, s1),jaccard_coefficient

def searchwithnot():
    with open("not.txt", "r", encoding='utf-8') as file_data:
        yesornot = 'not'
        count = 0


        for data_i in file_data.readlines():
            s = str(data_i).strip('\n').strip().lower().replace(" ", "_")


            with open("synonymsDict.txt", "r", encoding='utf-8') as file_sdict:
                for sdict_i in file_sdict.readlines():
                    string = str(sdict_i)
                    key = string[:string.find("||")].strip()
                    value = string[string.find("||") + 2:].strip()

                    a, b, c = searchlike(str(s), str(key))
                    if  b >= 0.8 or c >= 0.9:
                        yesornot = 'yes'
                        entityinsDict = value
                        count = count + 1
                        f_w.writelines(yesornot + "," + str(s) + "," + str(entityinsDict) + "\n")
                        print("yes," + str(s) + "," + str(entityinsDict) )
                        break

            print("synonymsDict.txt finished")



        print(count)

loaddict()
#searchwithjson()
searchwithlink()
#searchlike("rosemont__illinois",'rosemont,_illinois')
#searchwithnot()



