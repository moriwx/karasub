from janome.tokenizer import Tokenizer
import pykakasi
import re

kks = pykakasi.kakasi()
tokenizer = Tokenizer()

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
    for i in char:
        if not is_hiragana(i) and not is_katakana(i) or i in ['・', '゠']: # , 'ー'
            return False
    return True

def get_norm_ruby(item):
    if item['type'] == 2:
        return item['ruby']
    if item['type'] == 3:
        return item['orig']
    return ''

def get_norm_surface(item):
    if item['type'] in (2,3):
        return item['orig']
    return ''

def min_error_split(target_list, s):
    n = len(s)
    m = len(target_list)
    
    # 初始化 DP 表
    # dp[i][k] 表示处理到字符串位置 i 时，已匹配 k 个目标项的最小错误数
    dp = [[float('inf')] * (m + 1) for _ in range(n + 1)]
    # 记录回溯路径
    backtrack = [[None] * (m + 1) for _ in range(n + 1)]
    
    # 初始状态：空字符串匹配 0 个目标项
    dp[0][0] = 0
    
    # 动态规划填表
    for i in range(n + 1):
        for k in range(m + 1):
            if dp[i][k] == float('inf'):
                continue
                
            # 尝试匹配下一个目标项
            if k < m:
                target = target_list[k]
                # 处理空字符串目标项
                if target == "":
                    # 不消耗任何字符
                    if dp[i][k] < dp[i][k + 1]:
                        dp[i][k + 1] = dp[i][k]
                        backtrack[i][k + 1] = (i, k, "")
                else:
                    # 尝试所有可能的子串
                    for j in range(i + 1, n + 1):
                        segment = s[i:j]
                        # 计算错误成本（0~1 匹配~不匹配）
                        if segment == target:
                            cost = 0
                        elif segment=='wa' and target=='ha' or segment=='e' and target=='ha':
                            cost = 0.1
                        # elif target=='tsu': cost = min(max(len(segment), 1)*0.1, 1)
                        else:
                            cost = 1
                        new_cost = dp[i][k] + cost
                        if new_cost < dp[j][k + 1]:
                            dp[j][k + 1] = new_cost
                            backtrack[j][k + 1] = (i, k, segment)
    
    # 回溯找到最佳分割
    if dp[n][m] == float('inf'):
        return None  # 无有效分割
    
    # 从终点回溯
    result = []
    i, k = n, m
    while k > 0:
        prev_i, prev_k, segment = backtrack[i][k]
        result.append(segment)
        i, k = prev_i, prev_k
    
    # 反转结果（因为是从后往前回溯）
    return result[::-1]


def sylla_split(kana_str):
    kana_list = []
    i = 0
    n = len(kana_str)
    while i < n:
        current_char = kana_str[i]
        if current_char in ['ゃ', 'ゅ', 'ょ', 'ぁ', 'ぃ', 'ぅ', 'ぇ', 'ぉ', 'ー',
                            'ャ', 'ュ', 'ョ', 'ァ', 'ィ', 'ゥ', 'ェ', 'ォ']:
            if i > 0:
                kana_list[-1] += current_char
            else:
                kana_list.append(current_char)
            i += 1
        else:
            kana_list.append(current_char)
            i += 1
    return kana_list

def process_haruhi_line(line):
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
            ruby_text = sylla_split(ruby_text)
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
            token = sylla_split(token)
            for char in token:
                if is_kana(char):
                    result.append({'orig': char, 'type': 3})
                else:
                    result.append({'orig': char, 'type': 0})
    
    # 标注单字罗马音
    postpron = None        
    for i in range(len(result)-1, -1, -1):
        ruby_now = get_norm_ruby(result[i])
        if ruby_now in ('っ', 'ッ'):
            try:
                pron = postpron[0]
            except:
                pron = ''
            else:
                if pron=='c': pron = 't'
        else:
            pron = kks.convert(ruby_now)[0]['hepburn']
        result[i]['pron'] = pron
        postpron = pron
    
    # はへ确认
    line_pron_list = [item['pron'] for item in result]
    # line_kana = ''.join([get_norm_ruby(i) for i in result])
    line_surface = ''.join([get_norm_surface(i) for i in result])
    line_roma = kks.convert(''.join([token.phonetic for token in tokenizer.tokenize(line_surface)]))[0]['hepburn']
    line_roma_proc = min_error_split(line_pron_list, line_roma)
    for i in range(len(result)):
        if result[i]['type']==3:
            if result[i]['orig']=='は' and line_roma_proc[i]=='wa':
                result[i]['pron'] = 'wa'
            elif result[i]['orig']=='へ' and line_roma_proc[i]=='e':
                result[i]['pron'] = 'e'

    return result

if __name__=='__main__':
    input_string = "{阻|はば}むものは{無|な}い {身|み}{勝|かっ}{手|て}に"
    parsed = process_haruhi_line(input_string)
    print(parsed)