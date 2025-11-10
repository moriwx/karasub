import difflib
import os
import re
import webbrowser

def create_char_level_html_diff(text1, text2, filename="check_result.html"):
    """创建字符级别的HTML差异比较文件"""
    
    # 使用difflib进行字符级别比较
    differ = difflib.Differ()
    diff = list(differ.compare(text1, text2))
    
    # 构建HTML内容
    html_content = []
    html_content.append('''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>文本校对结果</title>
    <style>
        body {
            font-family: 'Consolas', 'Monaco', monospace;
            margin: 20px;
            background-color: #f9f9f9;
            line-height: 1.6;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }
        .legend {
            background-color: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .diff-container {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .text-block {
            background-color: #fff;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            white-space: pre-wrap;
            word-wrap: break-word;
            font-size: 14px;
            line-height: 1.8;
        }
        .char {
            padding: 1px 2px;
            border-radius: 2px;
            margin: 0 1px;
        }
        .deleted {
            background-color: #ffcccc;
            /* text-decoration: line-through; */
            color: #cc0000;
        }
        .added {
            background-color: #ccffcc;
            color: #006600;
        }
        .unchanged {
            /* 默认样式，无特殊标记 */
        }
        .summary {
            margin-top: 20px;
            padding: 15px;
            background-color: #e8f4f8;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>文本校对结果</h1>
        <div class="diff-container">
            <div class="text-block" id="combined-diff">''')
    
    # 构建合并的差异显示
    for item in diff:
        char = item[2:]  # 获取字符
        if item.startswith('- '):
            # 被删除的字符
            html_content.append(f'<span class="char deleted">{char}</span>')
        elif item.startswith('+ '):
            # 新增的字符
            html_content.append(f'<span class="char added">{char}</span>')
        elif item.startswith('  '):
            # 相同的字符
            html_content.append(f'<span class="char unchanged">{char}</span>')
    
    html_content.append('''</div>
        </div>
        <div class="summary">
            <h3>差异统计:</h3>
            <p>文本1长度: ''' + str(len(text1)) + ''' 字符</p>
            <p>文本2长度: ''' + str(len(text2)) + ''' 字符</p>
            <p>总差异数: ''' + str(len([d for d in diff if d.startswith(('- ', '+ '))])) + '''</p>
            <p>生成时间: ''' + __import__('datetime').datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '''</p>
        </div>
        <div class="legend">
            <h3>图例说明:</h3>
            <p><span class="char deleted">红色背景</span> - 在文本1中存在但在文本2中被删除的字符</p>
            <p><span class="char added">绿色背景</span> - 在文本2中新增的字符</p>
            <p>无标记 - 两个文本中相同的字符</p>
        </div>
    </div>
</body>
</html>''')
    
    # 写入文件
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(''.join(html_content))
    
    return filename


if __name__=='__main__':
    a = '''「大丈夫」なんて言えなくて 
わたしはまた口籠って
あなたに掛ける言葉さえ
持てないんです

視えないこころの目盛りが
溢れるまで　堰き止めて
傷付くあなたをこれ以上　見たくないんです
でもかなしいくらいに空回っちゃうから
このちいさな願いに魔法をかけて
足りないわたしだってあなたに応えて
その手を暖める希みをまださがしてる
あなたに巻きつく鎖を渦巻く嵐を
ふいに翳っていくその微笑を
あなたの空が泣いている理由をどうか
はんぶんこ　はんぶんこ　はんぶんこしたいだけ
はんぶんの　はんぶんの　はんぶん でもいいから

ほぞを嚙むような思いは　卒業したはずなのに
ただ祈るだけのわたしの　儘なのです
「優しさ」じゃいつだって　役に立たなくて
か細い声になって　消えていくから
要らないよあなたに　届かないのなら
この手で差し出せる望みに　換えてください
あなたを嗤う闇ごと　抱きしめる強さを
晴らせるような言葉があれば
あなたの背負う荷物を　わたしもどうか
はんぶんを　はんぶんを　はんぶんを持たせて
はんぶんの　はんぶんの　はんぶんになるまで

もうこのままじゃ　居られない　わたし達は過去を
かなぐり捨て　変わろうと　してはもがくけど
冷たい雨も　凍てる雪も
もう大丈夫だねって　言えたら、
言い合えたなら

あなたに巻きつく鎖を渦巻く嵐を
ふいに翳っていくその微笑を
あなたの空が泣いている理由をどうか
はんぶんこ　はんぶんこ　はんぶんこしたいだけ
ねえ、ずっと　そう、ずっと　差し出す傘の
はんぶんに　はんぶんに　はんぶんに居させて'''

    b = '''「大丈夫」なんて言えなくてわたしはまた口篭って
あなたに掛ける言葉さえ持てないんです

視えないこころの目盛りが溢れるまで堰き止めて
傷付くあなたをこれ以上見たくないんです

でもかなしいくらいに空回っちゃうから
このちいさな願いに魔法をかけて
足りないわたしだってあなたに応えて
その手を暖める希みをまださがしてる

あなたに巻きつく鎖を 渦巻く嵐を
ふいに翳っていくその微笑を
あなたの空が泣いている理由をどうか
はんぶんこ はんぶんこ はんぶんこしたいだけ
はんぶんの はんぶんの はんぶんでもいいから

ほぞを噛むような思いは卒業したはずなのに
ただ祈るだけのわたしの儘なのです

「優しさ」じゃいつだって役に立たなくて
か細い声になって消えていくから
要らないよあなたに届かないのなら
この手で差し出せる望みに換えてください

あなたを嗤う闇ごと抱きしめる強さを
晴らせるような言葉があれば
あなたの背負う荷物をわたしもどうか
はんぶんを はんぶんを はんぶんを持たせて
はんぶんの はんぶんの はんぶんになるまで

もうこのままじゃ居られないわたしたちは過去を
かなぐり捨てて変わろうとしてはもがくけど
冷たい雨も凍てる雪ももう大丈夫だねって
言えたら、言い合えたなら

あなたに巻きつく鎖を 渦巻く嵐を
ふいに翳っていくその微笑を
あなたの空が泣いている理由をどうか
はんぶんこ はんぶんこ はんぶんこしたいだけ

ねえ、ずっと そう、ずっと 差し出す傘の
はんぶんに はんぶんに はんぶんに居させて'''

    a = re.sub(r"【\S+】", "", a)
    a = re.sub(r"\[(\d+:\d+:\d+)\]", "", a)
    filename = create_char_level_html_diff(a, b)

    try:
        file_path = os.path.abspath(filename)
        print(f"正在打开: {file_path}")
        webbrowser.open('file://' + file_path)
        print("已在默认浏览器中打开结果文件")
    except Exception as e:
        print(f"自动打开失败，请手动打开文件: {filename}")
        print(f"错误信息: {e}")