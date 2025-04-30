import re

def extract_before_brace(s):
    s_new = s[:min(s.find('{') if s.find('{')>=0 else len(s), s.find('}') if s.find('}')>=0 else len(s))]
    if re.findall(r'\}(.+)\{', s): return s_new+'{\k0}'+re.findall(r'\}(.+)\{', s)[0] # 处理注音后的未打轴字符
    if re.findall(r'\}(.+)', s) and '{' not in s:
        return s_new+'{\k0}'+re.findall(r'\}(.+)', s)[0]
    return s_new

def lrctime2int(m: str, s: str, cs: str) -> int:
    '.lrc时轴信息转换为厘秒整数'
    return (int(m)*60 + int(s))*100 + int(cs)

def int2asstime(cs: int) -> str:
    '厘秒整数转换为.ass时轴信息'
    hours = cs // 360000
    cs %= 360000
    minutes = cs // 6000
    cs %= 6000
    seconds = cs // 100
    cs %= 100
    return f"{hours}:{minutes:02d}:{seconds:02d}.{cs:02d}"

def lrc2ass(lrc_string, pretime = 20, posttime = 20):
    '逐行转换.lrc为.ass格式，可设置句首句末延长时间'
    t1 = re.split(r'(\[.*?\])', lrc_string)
    mojiraw = [t1[i] for i in range(0, len(t1), 2)]
    timeraw = [lrctime2int(*re.findall(r'(\d+):(\d+):(\d+)', t1[i])[0]) for i in range(1, len(t1),2)]
    timeraw.append(timeraw[-1] + posttime)
    timedelta = [timeraw[i+1]-timeraw[i] for i in range(len(timeraw)-1)]
    mojinew = [''] * len(mojiraw)
    furistatus = [0] * len(mojiraw) # 默认无注音
    for i in range(len(mojiraw)):
        if  '{' in mojiraw[i]:
            furistatus[i+1] = 1
        elif furistatus[i]>=1 and '}' not in mojiraw[i]:
            furistatus[i+1] = 2
    for i in range(len(mojiraw)):
        if furistatus[i] == 0:
            mojinew[i] = extract_before_brace(mojiraw[i])
        elif furistatus[i] == 1:
            mojinew[i] = re.findall(r'\{(.+)\|', mojiraw[i-1])[0] + '|<' + extract_before_brace(mojiraw[i])
        elif furistatus[i] == 2:
            mojinew[i] = '#|' + extract_before_brace(mojiraw[i])
    asstxt = 'Dialogue: 0,'+int2asstime(timeraw[0]-pretime)+','+int2asstime(timeraw[-1])+r',Default,,0,0,0,karaoke,{\k'+str(pretime)+'}'+mojinew[0]
    for i in range(len(timedelta)):
        asstxt += f"{{\k{timedelta[i]}}}{mojinew[i+1]}"
    return asstxt

def partwk_process(assstr):
    newnums = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩']
    speakers = 'KAITO；天马司；凤笑梦；草薙宁宁；神代类；合唱；KAITO、凤笑梦；KAITO、凤笑梦、神代类；天马司、草薙宁宁；KAITO、天马司、草薙宁宁'.replace('、',';').split('；')
    for i in range(len(speakers)):
        assstr = assstr.replace(newnums[i], r'{\-'+speakers[i]+'}')
        # print(f'@Emoji=【{speakers[i]}】,透明画像1x1.png,,NoDecor,MarginRight=-90')
    return re.sub(r'{\\-([^\\{}]+)}{\\k(-?\d+\.?\d*)}', r'{\\k\2}{\\-\1}', assstr)

if __name__=='__main__':
    lrcstr = '''

③{子|[00:02:94]こ}{供|[00:03:07]ど[00:03:20]も}[00:03:38]の[00:03:56]ま[00:03:75]ま{喚|[00:04:05]わ[00:04:33]め}[00:04:53]い[00:04:69]て[00:04:86]も[00:05:14]


'''
    for i in lrcstr.splitlines():
        if i != '':
            # print(lrc2ass(i, 50))
            print(partwk_process(lrc2ass(i, 100, 100)))