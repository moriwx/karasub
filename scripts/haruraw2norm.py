import pykakasi
import re

kks = pykakasi.kakasi()
# newnums = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩',
#            '⑪', '⑫', '⑬', '⑭', '⑮', '⑯', '⑰', '⑱', '⑲', '⑳',
#            '㉑', '㉒', '㉓', '㉔', '㉕', '㉖', '㉗', '㉘', '㉙', '㉚']

def is_english(text):
    return bool(re.match(r'^[a-zA-Z]+$', text))

def is_kanji(char):
    return ('\u4E00' <= char <= '\u9FFF' or '\u3400' <= char <= '\u4DBF' or
            '\uF900' <= char <= '\uFAFF' or char == '\u3005')

def is_hiragana(char):
    return '\u3040' <= char <= '\u309F'

def is_katakana(char):
    return '\u30A0' <= char <= '\u30FF'

def is_kana(char):
    if char in ['・', '゠', 'ー']:
        return False
    return is_hiragana(char) or is_katakana(char)

def get_vowel_for_chouon(prev_phonetic):
    vowel_map = {
        # あ段
        'a': 'a', 'ka': 'a', 'ga': 'a', 'sa': 'a', 'za': 'a', 'ta': 'a', 'da': 'a',
        'na': 'a', 'ha': 'a', 'ba': 'a', 'pa': 'a', 'ma': 'a', 'ya': 'a', 'ra': 'a', 'wa': 'a',
        # い段
        'i': 'i', 'ki': 'i', 'gi': 'i', 'shi': 'i', 'ji': 'i', 'chi': 'i', 'di': 'i',
        'ni': 'i', 'hi': 'i', 'bi': 'i', 'pi': 'i', 'mi': 'i', 'ri': 'i',
        # う段
        'u': 'u', 'ku': 'u', 'gu': 'u', 'su': 'u', 'zu': 'u', 'tsu': 'u', 'du': 'u',
        'nu': 'u', 'fu': 'u', 'bu': 'u', 'pu': 'u', 'mu': 'u', 'yu': 'u', 'ru': 'u',
        # え段
        'e': 'e', 'ke': 'e', 'ge': 'e', 'se': 'e', 'ze': 'e', 'te': 'e', 'de': 'e',
        'ne': 'e', 'he': 'e', 'be': 'e', 'pe': 'e', 'me': 'e', 're': 'e',
        # お段
        'o': 'o', 'ko': 'o', 'go': 'o', 'so': 'o', 'zo': 'o', 'to': 'o', 'do': 'o',
        'no': 'o', 'ho': 'o', 'bo': 'o', 'po': 'o', 'mo': 'o', 'yo': 'o', 'ro': 'o'
    }
    return vowel_map.get(prev_phonetic.lower())

def process_haruhi_line_1(line):
    # 使用正则表达式分割字符串，捕获{...}结构
    tokens = re.split(r'(\{.*?\})', line)
    result = []
    
    for token in tokens:
        if not token:
            continue
            
        # 处理振假名结构 {漢字|假名}
        if token.startswith('{') and token.endswith('}'):
            content = token[1:-1]
            parts = content.split('|')
            assert len(parts) == 2, f"注音格式错误：{token}"
            kanji, ruby_text = parts
            assert len(ruby_text)>=1, "振假名为空"
            result.append({
                'orig': kanji,
                'type': 2,
                'ruby': ruby_text[0]
            })
            if len(ruby_text)>=2:
                for i in range(1, len(ruby_text)):
                    result.append({
                        'orig': '',
                        'type': 2,
                        'ruby': ruby_text[i]
                    })
                
        # 处理普通字符
        else:
            for char in token:
                if is_kana(char):
                    result.append({'orig': char, 'type': 3})
                # elif char in newnums:
                #     speakers = '初音未来；小豆泽心羽；白石杏；东云彰人；青柳冬弥；合唱；初音未来、白石杏、东云彰人；初音未来、小豆泽心羽、青柳冬弥；初音未来、小豆泽心羽、东云彰人；小豆泽心羽、白石杏、青柳冬弥'.replace('、',';').split('；')
                #     speaker = speakers[newnums.index(char)]
                #     result.append({'orig': '【'+speaker+'】', 'type': 0})
                else:
                    result.append({'orig': char, 'type': 0})
            
    return result

def process_pron(parsed):
    prev_pron = None
    for item in parsed:
        if item['type'] == 3:
            if is_english(item['orig']):
                pron = item['orig'].lower()
            elif item['orig']=='ー':
                pron = get_vowel_for_chouon(prev_pron)
            elif is_kana(item['orig']):
                pron = kks.convert(item['orig'])[0]['hepburn']
            if pron is not None:
                item['pron'] = pron
                prev_pron = pron
        elif item['type'] == 2: # 振假名结构
            if item['ruby']=='ー':
                pron = get_vowel_for_chouon(prev_pron)
            else:
                pron = kks.convert(item['ruby'])[0]['hepburn']
            item['pron'] = pron
            prev_pron = pron
        else:
            prev_pron = None
    return parsed

def process_haruhi_line(line):
    parsed = process_haruhi_line_1(line)
    parsed = process_pron(parsed)
    return parsed

if __name__=='__main__':
    input_string = "{心|こころ}{奪|うば}われ {阻|はば}むものは{無|な}い"
    parsed = process_haruhi_line(input_string)
    print(parsed)