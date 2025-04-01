import re

def ass_time_to_cs(time_str):
    """将ass时间格式转换为厘秒数"""
    hours, minutes, rest = time_str.split(':', 2)
    seconds, centiseconds = rest.split('.')
    return (int(hours)*3600 + int(minutes)*60 + int(seconds)) * 100 + int(centiseconds)

def cs_to_lrc_time(cs):
    """厘秒数转lrc时间格式（MM:SS:CS）"""
    minutes = cs // 6000
    cs %= 6000
    seconds = cs // 100
    centiseconds = cs % 100
    return f"[{minutes:02d}:{seconds:02d}:{centiseconds:02d}]"

def ass2lrc(ass_txt, partwk = True, partwk_logocs = 0, tail = False):
    """
        逐行转换.ass为.lrc格式，支持连结注音格式转换，可设置是否保留句末延长时间
    """
    parts = ass_txt.split(',', 9)
    assert len(parts) == 10, "此行属性有缺失！"
    start_cs = ass_time_to_cs(parts[1].strip())
    if partwk: # 暂未实现注音处分词
        speaker = '【'+parts[4]+'】'
        content = re.sub(r'{\\k(-?\d+\.?\d*)}{\\-([^\\{}]+)}([^{])', r'{\\-\2}{\\k\1}\3', parts[9])
        content = re.sub(r'{\\k(-?\d+\.?\d*)\\-([^\\{}]+)}', r'{\\-\2}{\\k\1}', content)
        content = re.sub(r'{\\-([^\\{}]+)\\k(-?\d+\.?\d*)}', r'{\\-\1}{\\k\2}', content)
        content = re.sub(r'{\\-([^\\{}]+)}', r'{\\k0}【\1】', content)
#         content = re.sub(r'{\\-([^\\{}]+)}', r'{\\k-'+str(partwk_logocs)+r'}{\\k'+str(partwk_logocs)+r'}【\1】', content)
    else:
        speaker = ''
        content = re.sub(r'\\-[^{}\\]+', '', re.sub(r'{\\-[^{}\\]+}', '', parts[9]))
    t1 = re.split(r'{\\k(-?\d+\.?\d*)}', content)
    assert '#' not in t1[0], "此行首个k值前含有#号！"
    mojiraw = [t1[i] for i in range(0, len(t1), 2)]
    timekraw = [start_cs]
    timekraw += [int(t1[i]) for i in range(1, len(t1),2)]
    for i in range(1, len(timekraw)):
        timekraw[i] += timekraw[i-1]
    moji_furistruct = []
    for i in mojiraw:
        if '|' not in i:
            moji_furistruct.append((0,))
        else:
            concat = 0
            if '|<' in i:
                tmp_base, tmp_ruby = i.split('|<', 1)
            else:
                tmp_base, tmp_ruby = i.split('|', 1)
                concat = 1
            assert tmp_base!='', "此行空字符串有注音假名！"
            if tmp_base=='#' and moji_furistruct[-1][0] in (1,2):
                moji_furistruct.append((2, '', tmp_ruby))
            else: moji_furistruct.append((1, tmp_base, tmp_ruby, concat))
    lrctxt = speaker + mojiraw[0]
    furi_base, furi_ruby, base_plus = '', '', 0
    for i in range(0, len(timekraw)-1):
        if (moji_furistruct[i+1][0]==0 or moji_furistruct[i+1][0]==1 and moji_furistruct[i+1][3]==0) and furi_base!='':
            lrctxt += '{' + furi_base + '|' + furi_ruby + base_plus*'＋' + '}'
            furi_base, furi_ruby, base_plus = '', '', 0
        elif moji_furistruct[i+1][0]==1 and moji_furistruct[i+1][3]==1 and furi_base!='':
            furi_ruby += (base_plus+1) * '＋'
            base_plus = 0
        if moji_furistruct[i+1][0] == 0:
            lrctxt += cs_to_lrc_time(timekraw[i])
            lrctxt += mojiraw[i+1]
        elif moji_furistruct[i+1][0] == 1:
            furi_base += moji_furistruct[i+1][1]
            furi_ruby += cs_to_lrc_time(timekraw[i])+moji_furistruct[i+1][2]
            base_plus = max(len(moji_furistruct[i+1][1])-1, 0)
        else:
            furi_ruby += cs_to_lrc_time(timekraw[i])+moji_furistruct[i+1][2]
    if furi_base!='':
        lrctxt += '{' + furi_base + '|' + furi_ruby + base_plus*'＋' + '}'
    if tail==True or mojiraw[-1]!='':
        lrctxt += cs_to_lrc_time(timekraw[-1])
    return lrctxt

if __name__=='__main__':
    lrcstr = '''

Dialogue: 0,0:00:13.90,0:00:17.56,Default,knd,0,0,0,karaoke,{\k23}小|<こ{\k17}石|<い{\k22}#|し{\k21}を{\k17}高|<た{\k19}#|か{\k23}く{\k19}高|<た{\k11}#|か{\k22}く{\k4}　{\k22}積|<つ{\k20}み{\k19}上|<あ{\k19}げ{\k19}て{\k27}は{\k42}
Dialogue: 0,0:00:17.30,0:00:20.53,Default,knd,0,0,0,karaoke,{\k22}吹|<ふ{\k21}き{\k21}さ{\k10}ら{\k28}す{\k20}心|<こ{\k21}#|こ{\k11}#|ろ{\k24}は{\k4}　{\k22}夕|<ゆ{\k38}#|う{\k33}暮|<ぐ{\k38}れ{\k10}
Dialogue: 0,0:00:20.32,0:00:23.72,Default,mfy,0,0,0,karaoke,{\k18}い{\k19}つ{\k21}か{\k21}見|<み{\k20}つ{\k19}か{\k22}る{\k23}と{\k16}　{\k18}ま{\k19}だ{\k18}見|<み{\k24}つ{\k22}か{\k18}る{\k25}と{\k17}
Dialogue: 0,0:00:23.68,0:00:27.15,Default,mfy,0,0,0,karaoke,{\k26}白|<し{\k18}#|ろ{\k45}く{\k3}　{\k34}甘|<あ{\k37}#|ま{\k37}く{\k4}　{\k38}淡|<あ{\k40}#|わ{\k26}く{\k39}
Dialogue: 0,0:00:26.69,0:00:30.39,Default,mzk,0,0,0,karaoke,{\k20}影|<か{\k22}#|げ{\k21}踏|<ふ{\k20}み{\k20}遊|<あ{\k20}#|そ{\k20}び{\k19}ば{\k11}か{\k22}り{\k10}　{\k16}し{\k21}て{\k18}き{\k22}ま{\k19}し{\k26}た{\k43}
Dialogue: 0,0:00:30.10,0:00:33.26,Default,mzk,0,0,0,karaoke,{\k22}贖|<あ{\k19}#|が{\k21}#|な{\k19}い{\k20}足|<あ{\k19}#|し{\k20}が{\k11}か{\k23}り{\k5}　{\k22}探|<さ{\k39}#|が{\k41}し{\k29}て{\k6}
Dialogue: 0,0:00:33.13,0:00:36.70,Default,ena,0,0,0,karaoke,{\k17}い{\k19}つ{\k23}か{\k20}見|<み{\k18}つ{\k22}け{\k20}る{\k25}と{\k17}　{\k16}ま{\k20}だ{\k18}見|<み{\k22}つ{\k23}け{\k18}る{\k22}と{\k37}
Dialogue: 0,0:00:36.52,0:00:40.17,Default,ena,0,0,0,karaoke,{\k19}永|<な{\k20}#|が{\k38}く{\k6}　{\k37}脆|<も{\k40}#|ろ{\k36}く{\k2}　{\k41}遠|<と{\k40}#|お{\k65}く{\k21}
Dialogue: 0,0:00:40.16,0:00:47.70,Default,rin,0,0,0,karaoke,{\k37}鏡|<か{\k40}#|が{\k21}#|み{\k20}越|<ご{\k19}し{\k20}貴方|<あ{\k39}#|な{\k40}#|た{\k56}と{\k18}　{\k45}瞳|<ひ{\k42}#|と{\k19}#|み{\k22}の{\k17}奥|<お{\k21}#|く{\k58}の{\k23}私|<わ{\k58}#|た{\k19}#|し{\k87}と{\k33}
Dialogue: 0,0:00:47.75,0:00:54.22,Default,knd,0,0,0,karaoke,{\k18}誰|<だ{\k19}#|れ{\k40}か{\k40}の{\k29}中|<な{\k32}#|か{\k19}の{\k28}貴方|<あ{\k31}#|な{\k20}#|た{\k29}は{\k12}　{\k18}欠|<か{\k23}#|け{\k37}片|<ら{\k41}の{\k31}ま{\k28}ま{\k21}に{\k18}夢|<ゆ{\k20}#|め{\k21}を{\k19}見|<み{\k28}る{\k25}
Dialogue: 0,0:00:54.10,0:00:57.37,Default,all,0,0,0,karaoke,{\k14}だ{\k9}っ{\k17}て{\k2} {\k36}D|<ディー{\k3}/{\k39}N|<エヌ{\k3}/{\k26}A|<エー{\k3} {\k28}じゃ{\k22}騙|<か{\k28}#|た{\k31}れ{\k23}な{\k23}い{\k20}
Dialogue: 0,0:00:57.29,0:01:06.23,Default,all,0,0,0,karaoke,{\k21}こ{\k21}の{\k40}心|<こ{\k41}#|こ{\k29}#|ろ{\k31}は{\k20}私|<わ{\k20}#|た{\k20}#|し{\k20}の{\k20}中|<な{\k26}#|か{\k18}　{\k15}紅|<あ{\k21}#|か{\k54}く{\k225}　{\k20}紅|<あ{\k20}#|か{\k45}く{\k167}
Dialogue: 0,0:01:06.31,0:01:10.27,Default,rin,0,0,0,karaoke,{\k21}眠|<ね{\k19}#|む{\k20}れ{\k24}な{\k18}い{\k19}迷|<ま{\k12}#|い{\k27}子|<ご{\k21}の{\k21}無|<な{\k13}い{\k26}も{\k19}の{\k20}ね{\k19}だ{\k18}り{\k23}じゃ{\k25}な{\k15}い{\k16}
Dialogue: 0,0:01:10.12,0:01:13.49,Default,knd,0,0,0,karaoke,{\k20}こ{\k18}の{\k21}細|<さ{\k11}#|い{\k29}胞|<ぼう{\k19}は{\k17}愛|<あ{\k13}#|い{\k14}憎|<ぞ{\k18}#|う{\k18}刻|<き{\k22}#|ざ{\k18}ま{\k22}れ{\k21}て{\k25}る{\k31}
Dialogue: 0,0:01:13.32,0:01:16.61,Default,rin,0,0,0,karaoke,{\k24}ま{\k17}だ{\k16}見|<み{\k25}つ{\k19}け{\k22}る{\k31}の{\k5}　{\k21\-knd}ま{\k20}だ{\k17}見|<み{\k22}つ{\k22}け{\k17}る{\k24}の{\k27}
Dialogue: 0,0:01:16.50,0:01:19.97,Default,all,0,0,0,karaoke,{\k21}言|<い{\k22}え{\k37}な{\k39}か{\k42}っ{\k37}た{\k43}音|<お{\k39}#|と{\k42}は？{\k25}
Dialogue: 0,0:01:19.71,0:01:23.04,Default,all,0,0,0,karaoke,{\k23}誰|<だ{\k16}#|れ{\k40}か{\k39}の{\k30}中|<な{\k32}#|か{\k20}の{\k32}貴方|<あ{\k29}#|な{\k21}#|た{\k27}は{\k24}
Dialogue: 0,0:01:22.94,0:01:26.35,Default,all,0,0,0,karaoke,{\k18}繋|<つ{\k20}#|な{\k39}が{\k41}れ{\k30}た{\k30}ま{\k21}ま{\k19}夢|<ゆ{\k21}#|め{\k21}を{\k21}見|<み{\k23}る{\k37}
Dialogue: 0,0:01:26.11,0:01:29.38,Default,all,0,0,0,karaoke,{\k14}だ{\k9}っ{\k17}て{\k2} {\k36}D|<ディー{\k3}/{\k39}N|<エヌ{\k3}/{\k26}A|<エー{\k3} {\k28}じゃ{\k22}語|<か{\k28}#|た{\k31}れ{\k23}な{\k23}い{\k20}
Dialogue: 0,0:01:29.32,0:01:36.68,Default,all,0,0,0,karaoke,{\k19}こ{\k20}の{\k39}痛|<い{\k41}#|た{\k31}み{\k30}も{\k20}私|<わ{\k18}#|た{\k21}#|し{\k20}の{\k20}中|<な{\k22}#|か{\k18}　{\k20}紅|<あ{\k19}#|か{\k57}く{\k223}　{\k21}紅|<あ{\k19}#|か{\k57}く{\k1}
Dialogue: 0,0:01:39.12,0:01:45.57,Default,knd,0,0,0,karaoke,{\k20}鏡|<か{\k59}#|が{\k21}#|み{\k28}の{\k33}　{\k19\-rin}形|<か{\k58}#|た{\k22}#|ち{\k30}と{\k29}　{\k21\-mzk}逆|<さ{\k60}#|か{\k20}さ{\k60}ま{\k19\-rin}な{\k1}　{\k44}D|<ディー{\k17}/{\k20}N|<エヌ{\k2}/{\k30}A|<エー{\k32}
Dialogue: 0,0:01:45.52,0:01:52.06,Default,ena,0,0,0,karaoke,{\k20}私|<わ{\k60}#|た{\k20}#|し{\k27}の{\k33}　{\k21\-rin}証|<あ{\k58}#|か{\k21}#|し{\k39}と{\k21}　{\k20\-mfy}暖|<あ{\k60}#|た{\k19}#|た{\k60}か{\k19\-rin}な{\k1}　{\k44}D|<ディー{\k17}/{\k20}N|<エヌ{\k2}/{\k35}A|<エー{\k37}
Dialogue: 0,0:01:51.91,0:01:58.36,Default,rin,0,0,0,karaoke,{\k20}鏡|<か{\k59}#|が{\k21}#|み{\k28}の{\k33}　{\k19\-mfy}形|<か{\k58}#|た{\k22}#|ち{\k30}と{\k29}　{\k21\-rin}逆|<さ{\k60}#|か{\k20}さ{\k60}ま{\k19\-ena}な{\k1}　{\k44}D|<ディー{\k17}/{\k20}N|<エヌ{\k2}/{\k33}A|<エー{\k29}
Dialogue: 0,0:01:58.31,0:02:04.85,Default,rin,0,0,0,karaoke,{\k20}私|<わ{\k60}#|た{\k20}#|し{\k27}の{\k33}　{\k21\-mzk}証|<あ{\k58}#|か{\k21}#|し{\k39}と{\k21}　{\k20\-rin}暖|<あ{\k60}#|た{\k19}#|た{\k60}か{\k19\-knd}な{\k1}　{\k44}D|<ディー{\k17}/{\k20}N|<エヌ{\k2}/{\k43}A|<エー{\k29}

'''
    for i in lrcstr.splitlines():
        if i.startswith('Dialogue:') or i.startswith('Comment:'):
            print(ass2lrc(i))
