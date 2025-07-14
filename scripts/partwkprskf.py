import re

newnums = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩',
           '⑪', '⑫', '⑬', '⑭', '⑮', '⑯', '⑰', '⑱', '⑲', '⑳',
           '㉑', '㉒', '㉓', '㉔', '㉕', '㉖', '㉗', '㉘', '㉙', '㉚']

def process_text(text):
    text = re.sub(r'{{ruby\|(.*?)\|(.*?)}}', r'\1', text)
    speakers = []
    for match in re.finditer(r'{{multiccAlt\|([^|]+)\|([^}]+)}}', text, re.DOTALL):
        speaker = match.group(1)
        content = match.group(2)
        if speaker in speakers:
            sind = speakers.index(speaker)
        else:
            sind = len(speakers)
            speakers.append(speaker)
        text = text.replace(match.group(0), newnums[sind]+content)
    for match in re.finditer(r'{{([^|]+)\|([^}]+)}}', text, re.DOTALL):
        speaker = match.group(1)
        content = match.group(2)
        if speaker in speakers:
            sind = speakers.index(speaker)
        else:
            sind = len(speakers)
            speakers.append(speaker)
        text = text.replace(match.group(0), newnums[sind]+content)
    print(speakers)
    return text # , speakers

if __name__=='__main__':
    lrcstr = '''

{{Emu|生きているこの身体}}
{{Luka wxs|脳天爪先まで}}
{{Tsukasa|一切{{ruby|顧|かえる}}みず 使う 使う
{{ruby|草臥|くたび}}れ果てる日まで}}

{{Nene|想像は絶えず高く}}
{{Luka wxs|頂点に理由が待っている}}
{{Rui|本当は全部 
何もかも零したくないだけだ}}

{{multiccAlt|Luka wxs, Emu|もしも目覚めなくとも}}
{{Tsukasa|何回も何回もやり直せるように暮らす}}
{{multiccAlt|Luka wxs, Nene|確かじゃない未来に}}
{{Rui|全身を賭ける それが眩しい}}

{{multiccAlt|Luka wxs, Tsukasa|知らない 見えない 美しさを}}
{{multiccAlt|Tsukasa, Nene|掴めずとも 確かめてたい}}
{{multiccAlt|Luka wxs, Rui|遠く星を目指して向かう}}
{{multiccAlt|Emu, Rui|後悔が{{ruby|纏|まと}}わりついても尚(なお)
歩幅を合わせて共に歩きたい}}

{{Emu|もう直ぐにブラックアウト
舞台の端から溢れてく魔法が}}
{{multiccAlt|Luka wxs, Tsukasa|｢私は関係ない！｣}}
{{Tsukasa|選ばれなかった仕掛けが摘まれていく}}

{{Nene|生きている限り もう流れ流れて}}
{{Rui|あぁ何か今になって
なんてことない言葉ばかり浮かぶ}}

{{multiccAlt|Luka wxs, Emu|ついさっき奪われた}}{{Tsukasa|役割が
亡霊が僕を{{ruby|頭上|ずじょう}}から見てる}}
{{multiccAlt|Luka wxs, Nene|考えが色付かない}}
{{Rui|恐ろしくて泣きそうになる}}

{{multiccAlt|Emu, Rui|消えない 消せない 光が今}}
{{multiccAlt|Luka wxs, Rui|{{ruby|空|から}}の闇を潰している}}
{{multiccAlt|Tsukasa, Nene|遠くまで もっと 見えるように}}
{{multiccAlt|Luka wxs, Tsukasa|{{ruby|焼却|しょうきゃく}}して命を使い切って
冷たくない場所へ辿り着きたい}}

{{Emu|忘れないで この道が変わらないことを}}
{{Nene|絶えず ずっと繋がって糧になる}}
{{Tsukasa|照明が落ちて 鳴り止まない拍手が}}
{{Rui|響くそれで僕は何をしたら良いんだろうか}}

{{Luka wxs|痛みだけが 終わりだけが
答えだとは思えなくて}}
{{Rui|その重荷を半分持ちたい
透明な僕らは何を選んで 
どこへ行くのか}} {{Tsukasa|(Good job!)}}

{{multiccAlt|Luka wxs, Tsukasa|知らない 見えない 美しさを}}
{{multiccAlt|Tsukasa, Nene|掴めずとも 確かめてたい}}
{{multiccAlt|Luka wxs, Rui|遠く星を目指して向かう}}
{{multiccAlt|Emu, Rui|後悔が纏わりついても尚
歩幅を合わせて共に歩きたい}}

{{Rui|どうにか食らいつきたい！}}


'''
    print(process_text(lrcstr))