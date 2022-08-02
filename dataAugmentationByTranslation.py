
import os
import requests
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/hwangyun/PycharmProjects/ease_real/nonmentor-4378d254e9ba.json"

def list_languages():
    """Lists all available languages."""
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    results = translate_client.get_languages()

    for language in results:
        print(u"{name} ({language})".format(**language))

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

def makingAugmentationbackTranslation(text):
    languages = ["en", "ja", "zh-CN", "es"]
    translatedList = []
    translatedResultList = []

    for l in languages:
        translatedList.append((l, translate_text(source="ko", target=l, text=text)))
    for l, t in translatedList:
        print(l, t)
        translatedResultList.append((translate_text(source=l, target="ko", text=t)))
    return translatedResultList
for m in makingAugmentationbackTranslation("㉮에서는 경쟁을 우리 삶에서 떼어놓을 수 없는 불가피한 것으로 보며 앞으로도 우리 사회에서 경쟁이 계속될 것이기에 공정한 경쟁을 추구하기 위한 방식을 고민할 필요가 있다고 주장하고 있는 반면에 ㉯에서는 흔히 사회에서 나타나는 경쟁 구도를 설명할 때 언급되는 ‘진화론’이 경쟁보다는 공존의 논리에 바탕을 두고 있다고 하며 앞으로 세상이 변화하면서 경쟁의 시대는 가고 서로 화합하며 더불어 사는 공존의 시대가 올 것이라고 말하고 있다."):
    print(m)
