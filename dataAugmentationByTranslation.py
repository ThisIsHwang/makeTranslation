
import os
import requests
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/hwangyun/PycharmProjects/ease_real/nonmentor-4378d254e9ba.json"
import pandas as pd
import random
import re

def sub_chars(string):
    """
    Strips illegal characters from a string.  Used to sanitize input essays.
    Removes all non-punctuation, digit, or letter characters.
    Returns sanitized string.
    string - string
    """
    #Define replacement patterns
    open_par_pat = r"(\(|\[|\{\<)"
    close_par_pat = r"(\)|\]|\}\>)"
    sub_pat = r"[^A-Za-z가-힣\.\ ?!,;:\(\)]"
    char_pat = r"\."
    com_pat = r","
    ques_pat = r"\?"
    excl_pat = r"!"
    sem_pat = r";"
    col_pat = r":"
    whitespace_pat = r"\s{1,}"
    separatedCharList = ["\(%s\)" %c for c in "가나다라마바사아자차카타파하"]
    circleCharList = [s for s in '㉮㉯㉰㉱㉲㉳㉴㉵㉶㉷㉸㉹㉺㉻']
    #Replace text.  Ordering is very important!
    nstring = re.sub(open_par_pat, "(", string)
    nstring = re.sub(close_par_pat, ")", nstring)
    nstring = re.sub(sub_pat, "", nstring)
    nstring = re.sub(char_pat,". ", nstring)
    nstring = re.sub(com_pat, ", ", nstring)
    nstring = re.sub(ques_pat, "? ", nstring)
    nstring = re.sub(excl_pat, "! ", nstring)
    nstring = re.sub(sem_pat, "; ", nstring)
    nstring = re.sub(col_pat, ": ", nstring)
    nstring = re.sub(whitespace_pat, " ", nstring)
    for s, c in zip(separatedCharList, circleCharList):
        nstring = re.sub(s, c,nstring)
    return nstring

def list_languages():
    """Lists all available languages."""
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    results = translate_client.get_languages()
    return results

def translate_text(source, target, text):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    import six
    from google.cloud import translate_v2 as translate


    translate_client = translate.Client()
    # if isinstance(text, six.binary_type):
    #     text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, source_language=source, target_language=target)
    return result["translatedText"]

def makingAugmentationbackTranslation(text, num):
    if num > 100:
        num = 100
    languageList = list_languages()
    languages = [lang["language"] for lang in languageList]
    random.shuffle(languages)
    translatedList = []
    translatedResultList = []
    korToJap = translate_text(source="ko", target="ja", text=text)
    japToKor = translate_text(source="ja", target="ko", text=korToJap)

    translatedResultList.append(japToKor)
    index = 0
    while index < len(languages):
        try:
            if num == index:
                break
            l = languages[index]
            if l == "ja":
                index += 1
                continue
            translatedList.append((l, translate_text(source="ko", target=l, text=japToKor)))
            index += 1
        except Exception as e:
            print(e)
            index += 1
            continue

    index = 0
    while index < len(translatedList):
        try:
            l, t = translatedList[index]
            translatedResultList.append((translate_text(source=l, target="ko", text=t)))
            index += 1
        except Exception as e:
            print(e)
            index += 1
            continue
    return translatedResultList

#df = pd.read_csv('/Users/hwangyun/PycharmProjects/ease_real/0701_nonsul_data.csv', header=0)
df = pd.read_csv("total.csv", index_col="id")
df = df.dropna()
df = df[df['problem_id'] == 20220502]
df['essay_cleaned']=df.apply(lambda row : sub_chars(row['essay']), axis = 1)
from sklearn.model_selection import train_test_split


#trainSet.to_csv("ebsi_0701_trainset.csv", index=False)


X_train, X_test, y_train, y_test = train_test_split(df["essay_cleaned"].tolist(), df["독해"].tolist(), test_size=0.2, random_state=42)
trainSet = pd.DataFrame(list(zip(X_train, y_train)), columns=["essay", "score"])
#trainSet.to_csv("ebsi_0701_trainset.csv", index=False)
# count = trainSet["score"].value_counts()

testSet = pd.DataFrame(list(zip(X_test, y_test)), columns=["essay", "score"])


count = trainSet["score"].value_counts()
#count.
scores =[]

for i in range(1, 6):
    scores.append(trainSet[trainSet["score"]==i])

minIdx = count.idxmin()
s = scores[int(minIdx) -1]
for essay, score in zip(s["essay"], s["score"]):
    temp = makingAugmentationbackTranslation(essay, 3)
    for t in temp:
        new_data = {
            'essay': t,
            'score': score
        }
        trainSet.loc[len(trainSet)] = new_data
#for idx, df in enumerate(scores):

    # for d in range(len(df)):
    #     try:
    #         temp = makingAugmentationbackTranslation(df.iloc[d]["essay_cleaned"], 60//(count[idx + 1] + 1))
    #
    #         for t in temp:
    #             new_data = {
    #                 'essay': t,
    #                 'score': df.iloc[d]["총점"]
    #             }
    #             testSet.loc[len(testSet)] = new_data
    #
    #     except Exception as e:
    #         print(e)
    #         continue
#print()

from sklearn.utils import shuffle
#trainSet = shuffle(trainSet)
testSet = shuffle(testSet)

#trainSet.to_csv("ebsi_0701_train_Aug_set_300.csv", index=False)
#testSet = pd.DataFrame(list(zip(X_test, y_test)), columns=["essay", "score"])
trainSet.to_csv("ebsi_0502_trainset_for_dockhae.csv", index=False)
testSet.to_csv("ebsi_0502_testset_for_dockhae.csv", index=False)



