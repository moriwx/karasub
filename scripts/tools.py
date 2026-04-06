from ass2lrc import *
from lrc2ass import lrctime2int

import colorsys
import math
from typing import Tuple, List

prsk_hex_list = ['#33ccbb', '#ffcc11', '#ffee11', '#ffbbcc', '#dd4444', '#3366cc',
 '#4455dd', '#33aaee', '#ffdd44', '#ee6666', '#bbdd22', # L/n
 '#88dd44', '#ffccaa', '#99ccff', '#ffaacc', '#99eedd', # MMJ
 '#ee1166', '#ff6699', '#00bbdd', '#ff7722', '#0077dd', # VBS
 '#ff9900', '#ffbb00', '#ff66bb', '#33dd99', '#bb88ee', # WS
 '#884499', '#bb6688', '#8888cc', '#ccaa88', '#ddaacc'] # 25

prsk_cl0_list = ['#25c7a5', '#e6af0a', '#e0bd52', '#e384a7', '#e35c55', '#3d69d4',
 '#4455dd', '#35aff5', '#e0be00', '#e03e3a', '#92c700', # L/n
 '#64d426', '#ed9561', '#499bed', '#f72eac', '#2dd69f', # MMJ
 '#ee1166', '#f7569d', '#00b3d4', '#ed6f20', '#006cc9', # VBS
 '#ff9900', '#f0b000', '#ed3bbb', '#0ed975', '#a662e8', # WS
 '#9654ab', '#bf698b', '#7777b3', '#ab8e72', '#c497b6'] # 25

prsk_cl1_list = ['#10a17f', '#bd970d', '#b39f00', '#e04e6c', '#c71616', '#1c48bf',
 '#2b3ccc', '#1186c7', '#a3790f', '#d91215', '#738715', # L/n
 '#58b80a', '#eb6c17', '#0c7ed4', '#eb1dac', '#0dba8a', # MMJ
 '#d40f5b', '#d42c72', '#029fba', '#e0692f', '#0064ba', # VBS
 '#ff9900', '#e37500', '#e517a2', '#01b852', '#8e31d9', # WS
 '#5f2775', '#995370', '#575782', '#73604d', '#a67f99'] # 25

def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """将十六进制颜色转换为RGB"""
    hex_color = hex_color.strip()
    if hex_color[0] == '&':
        hex_color = hex_color.lstrip('&H').rstrip('&')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (4, 2, 0))
    else:
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join([c + c for c in hex_color])
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return rgb

def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """将RGB转换为十六进制颜色"""
    return '#{:02x}{:02x}{:02x}'.format(
        max(0, min(255, int(rgb[0]))),
        max(0, min(255, int(rgb[1]))),
        max(0, min(255, int(rgb[2])))
    )

def rgb_to_hsl(rgb: Tuple[int, int, int]) -> Tuple[float, float, float]:
    """将RGB转换为HSL色彩空间"""
    r, g, b = [x/255.0 for x in rgb]
    
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    
    # 计算明度
    l = (max_val + min_val) / 2
    
    # 计算饱和度
    if max_val == min_val:
        s = 0.0
    else:
        if l > 0.5:
            s = (max_val - min_val) / (2.0 - max_val - min_val)
        else:
            s = (max_val - min_val) / (max_val + min_val)
    
    # 计算色相
    if max_val == min_val:
        h = 0.0
    else:
        if max_val == r:
            h = (g - b) / (max_val - min_val)
        elif max_val == g:
            h = 2.0 + (b - r) / (max_val - min_val)
        else:
            h = 4.0 + (r - g) / (max_val - min_val)
        
        h *= 60
        if h < 0:
            h += 360
    
    return (h / 360.0, s, l)

def hsl_to_rgb(hsl: Tuple[float, float, float]) -> Tuple[int, int, int]:
    """将HSL转换为RGB色彩空间"""
    h, s, l = hsl
    
    if s == 0:
        r = g = b = l
    else:
        def hue_to_rgb(p, q, t):
            if t < 0: t += 1
            if t > 1: t -= 1
            if t < 1/6: return p + (q - p) * 6 * t
            if t < 1/2: return q
            if t < 2/3: return p + (q - p) * (2/3 - t) * 6
            return p
        
        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q
        
        r = hue_to_rgb(p, q, h + 1/3)
        g = hue_to_rgb(p, q, h)
        b = hue_to_rgb(p, q, h - 1/3)
    
    return (int(r * 255), int(g * 255), int(b * 255))

def get_color_category(hue: float) -> str:
    """根据色相确定颜色类别"""
    hue_deg = hue * 360
    
    if hue_deg < 15 or hue_deg >= 345:
        return "red"
    elif hue_deg < 45:
        return "orange"
    elif hue_deg < 75:
        return "yellow"
    elif hue_deg < 165:
        return "green"
    elif hue_deg < 195:
        return "cyan"
    elif hue_deg < 255:
        return "blue"
    elif hue_deg < 285:
        return "purple"
    else:
        return "magenta"

def countdown_str(starttime, bpm, symbol='●', num=4):
    t = 6000 / bpm
    if isinstance(starttime, str):
        starttime = lrctime2int(*re.findall(r'(\d+):(\d+):(\d+)', starttime)[0])
    timelst = []
    for i in range(num+1):
        timelst.append(cs_to_lrc_time(round(max(starttime-i*t,0))))
    return symbol.join(timelst)

def renumber_BV1KiySYBEHn(text):
    lines = text.strip().split('\n')
    new_lines = []
    counter = 1
    
    for line in lines:
        line = line.strip()
        if not line:
            new_lines.append(line)
            continue
        if line.startswith('p') and line[1:].split()[0].isdigit():
            content = ' '.join(line.split()[1:])
            new_line = f"p{counter} {content}"
            new_lines.append(new_line)
            counter += 1
        else:
            new_lines.append(line)
    
    return '\n'.join(new_lines)

if __name__=='__main__':
#     color = "#FF5733"
#     colors = '''&H6611EE&
# &H9966FF&
# &HDDBB00&
# &H2277FF&
# &HDD7700&'''.splitlines()
#     colors = '&HCC6633&'.split(';')
#     for color in colors: print(hex_to_rgb(color))
#     bpm = 133
#     print(countdown_str('[00:01:64]', bpm))
#     print(countdown_str('[00:31:28]', bpm))
#     print(countdown_str('[01:39:55]', bpm))
#     print(countdown_str('[02:26:05]', bpm))
    print(renumber_BV1KiySYBEHn("""
- Leo/need
p1 needLe youtu.be/pW-GK65DYLI
p2 ステラ youtu.be/myVWDvuggQs
p3 「1」 youtu.be/I5hu-LNsS-o
p4 フロムトーキョー sm39106936
p6 てらてら youtu.be/mpaWT_YzRVw
p7 フレー youtu.be/agMgpdy0Aiw
p8 相生 sm42727291
p9 purpose sm43046990
p10 インテグラル sm43487328
- MORE MORE JUMP！
p11 Color of Drops youtu.be/vhJ_wXaVeIA
p12 メタモリボン youtu.be/waYz_v31-e8
p13 パラソルサイダー youtu.be/2huRUG-iGxM
p14 DREAM PLACE sm41264878
p15 フロート・プランナー sm41915596
p16 MOTTO!!! BV1bC4y1e7xJ
p17 JUMPIN' OVER! BV16x4y1C7pE
p18 キラー BV1FpaRebEuJ
- Vivid BAD SQUAD
p19 Forward youtu.be/dCrXNKS2jPQ
p20 シネマ youtu.be/QdSd-2NxHVU
p21 虚ろを扇ぐ youtu.be/Q63vzQKchAU
p22 リアライズ sm42646834
p23 烈火 sm43894030
p24 ULTRA C BV16A8ne4Ejz
- ワンダーランズ×ショウタイム
p25 Glory Steady Go! sm39296549
p26 88☆彡 sm40354730
p27 星空のメロディー sm40699172
p28 どんな結末がお望みだい？ youtu.be/nYu4rlSLPl4
p29 Mr. Showtime sm41987708
p30 オペラ！スペースオペラ！ sm43914598
- 25時、ナイトコードで。
p31 悔やむと書いてミライ youtu.be/e4FakrYWxL8
p32 携帯恋話 youtu.be/SvGHs7F-DN8
p33 再生 youtu.be/iiN7TYmNE3s
p34 ロウワー youtu.be/kua4sEc6Smo
p35 トリコロージュ youtu.be/g70THANniZw
p36 ノマド youtu.be/Prs71tG5Rt0
p37 アイデンティティ youtu.be/7C24evjvOBM
p38 君の夜をくれ youtu.be/4CBFqGSYxc4
p39 Iなんです youtu.be/sppaCuXvM6s
p40 演劇 sm42519680
"""))