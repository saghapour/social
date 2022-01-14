import re


def clean_text(text: str):
    return re.sub(r"[^0-9\w\s_,.]", ' ', text.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')
                  .replace('  ', ' ').strip())

def remove_bad_characters(text: str) -> str:
    """
    :param text: A text
    :return: Process on text
    """
    persian_alphabet_full = list(""" اآبپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیئ\xE2\x80\x8C""")
    punctuation = """[~!@#$%^&*()-_=+{}\|;:'",<.>/?÷٪×،ـ»«؛؟…↓↑→←™®°∞٫]"""
    clean_text = ''''''
    for char in text:
        if char in punctuation:
            clean_text += u' {} '.format(char)
            continue
        if char in persian_alphabet_full:
            clean_text += char
    clean_text = clean_text.replace(u'  ', u' ').replace(u'  ', u' ').replace(u'  ', u' ')
    return clean_text