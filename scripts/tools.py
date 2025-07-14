from ass2lrc import *
from lrc2ass import lrctime2int

def hex_to_rgb(hex_color):
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

def countdown_str(starttime, bpm, symbol='●', num=4):
    t = 6000 / bpm
    if isinstance(starttime, str):
        starttime = lrctime2int(*re.findall(r'(\d+):(\d+):(\d+)', starttime)[0])
    timelst = []
    for i in range(num+1):
        timelst.append(cs_to_lrc_time(round(max(starttime-i*t,0))))
    return symbol.join(timelst)

if __name__=='__main__':
    color = "#FF5733"
#     colors = '''&H6611EE&
# &H9966FF&
# &HDDBB00&
# &H2277FF&
# &HDD7700&'''.splitlines()
    colors = '&HCC6633&'.split(';')
    for color in colors: print(hex_to_rgb(color))
    bpm = 133
    print(countdown_str('[00:01:64]', bpm))
    print(countdown_str('[00:31:28]', bpm))
    print(countdown_str('[01:39:55]', bpm))
    print(countdown_str('[02:26:05]', bpm))