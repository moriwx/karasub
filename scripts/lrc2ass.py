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

def lrc2ass(lrc_string, posttime = 20):
    '逐行转换.lrc为.ass格式，可设置句末延长时间'
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
    asstxt = 'Dialogue: 0,'+int2asstime(timeraw[0])+','+int2asstime(timeraw[-1])+',Default,,0,0,0,karaoke,'+mojinew[0]
    for i in range(len(timedelta)):
        asstxt += f"{{\k{timedelta[i]}}}{mojinew[i+1]}"
    return asstxt

def partwk_process(assstr):
    newnums = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨']
    speakers = ['初音未来', '星乃一歌', '天马咲希', '望月穗波', '日野森志步', '初音未来;星乃一歌', '星乃一歌;日野森志步', '初音未来;星乃一歌;日野森志步']
    for i in range(len(speakers)):
        assstr = assstr.replace(newnums[i], r'{\-'+speakers[i]+'}')
    return re.sub(r'{\\-([^\\{}]+)}{\\k(-?\d+\.?\d*)}', r'{\\k\2}{\\-\1}', assstr)

if __name__=='__main__':
    lrcstr = '''{相|[01:38:58]あ[01:39:72]い}[01:40:06]も{変|[01:40:43]か}[01:40:67]わ[01:40:92]ら[01:41:14]ず{険|[01:41:44]け[01:41:64]わ}[01:41:88]し[01:42:20]く{迷|[01:42:38]ま[01:42:81]よ}っ[01:43:13]た[01:43:18]

{嘘|[01:46:03]う[01:46:14]そ}[01:46:38]は[01:46:49]や[01:46:73]だ{嘘|[01:46:98]う[01:47:08]そ}[01:47:31]は[01:47:40]や[01:47:64]だ[01:47:70]
{嘘|[01:49:72]う[01:49:85]そ}[01:50:10]は[01:50:18]や[01:50:44]だ{嘘|[01:50:69]う[01:50:80]そ}[01:51:04]は[01:51:14]や[01:51:37]だ[01:51:43]'''
    for i in lrcstr.splitlines():
        if i != '':
            # print(lrc2ass(i))
            print(partwk_process(lrc2ass(i)))
