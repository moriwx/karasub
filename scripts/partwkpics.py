from PIL import Image, ImageDraw, ImageFilter
import itertools
import os
import math

def crop_to_inscribed_circle(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    width, height = img.size
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    radiusw = width // 2
    radiush = height // 2
    center = (width//2, height//2)
    draw.ellipse(
        (center[0]-radiusw, center[1]-radiush, 
         center[0]+radiusw, center[1]+radiush),
        fill=255
    )
    img.putalpha(mask)
    img.save(output_path, "PNG")

def generate_pentagon_layout(char_list = ['hrk', 'airi', 'szk', 'miku', 'mnr'], circle_diameter = 128):
    ''' Arrange 5 avatars in a regular pentagon shape '''
    circle_radius = circle_diameter // 2
    R = circle_radius / math.sin(math.radians(36))  # radius of the circumcircle of the pentagon
    img_width = circle_diameter * (2*math.cos(math.radians(36))+1)
    img_height = circle_diameter * (math.sin(math.radians(36))+math.sin(math.radians(72))+1)

    canvas = Image.new("RGBA", (int(img_width), int(img_height)), (0,0,0,0))
    images = [Image.open(input_path+f"{i}.png").convert("RGBA") for i in char_list]
    center = (img_width//2, int(R+circle_radius))
    angles = [math.radians(-90 + 72*i) for i in range(5)]
    coords = [(int(center[0] + R*math.cos(a)), int(center[1] + R*math.sin(a))) for a in angles]
    for img, (x,y) in zip(images, coords):
        canvas.paste(img, (x-circle_radius, y-circle_radius), img)
    canvas.save("all.png")

def generate_color_image(colors, outputfile, offseta=0, offsetb=0):
    """
    生成一个100*100的图像，按照输入的颜色从上到下平均排列，考虑纵向偏移参数。
    
    参数:
        colors (list): RGB元组列表。
        outputfile (string): 输出图像文件位置。
        offseta (int): 顶部偏移，默认0。
        offsetb (int): 底部偏移，默认0。
    
    返回:
        PIL.Image.Image: 生成的图像对象。
    """
    height = 100
    n = len(colors)
    img = Image.new('RGB', (height, height))
    pixels = img.load()
    total_length = height + offsetb - offseta
    assert n > 0, "颜色列表不能为空"
    h = total_length / n
    for y in range(height):
        if y < offseta:
            color = colors[0]
        elif y >= height + offsetb:
            color = colors[-1]
        else:
            pos = y - offseta
            i = int(pos // h)
            i = min(i, n-1)
            color = colors[i]
        for x in range(height):
            pixels[x, y] = color
    img.save(outputfile)

# input_path = 'E://Pictures//ACGN//PJSK//Q25//'
input_path = 'E://Pictures//ACGN//profiles//'
image_extension = '.png'
image_size = (256, 256) # (400, 400) # (128, 128)
output_path = 'E://Videos//nicokara//251222starmine//'
# char_zh = 'KAITO；星乃一歌；天马咲希；望月穗波；日野森志步'.split('；')
# char_zh = ['リン', '奏', 'まふゆ', '絵名', '瑞希']
# char_en = ['rin', 'knd', 'mfy', 'ena', 'mzk']
char_zh = ['佑芽', '美鈴', '星南']
char_en = ['hume', 'hmsz', 'jsna']
# char_en = ['KAFU', 'SEKAI', 'RIME', 'COKO', 'HARU']
# char_en = ['KAF', 'KAFU', 'ISEKAI', 'SEKAI', 'RIM', 'RIME', 'KOKO', 'COKO', 'HARUS', 'HARU']
char_all_en = ['miku', 'rin', 'len', 'luka', 'mei', 'kai', 'ick', 'saki', 'hnm', 'shiho', 'mnr', 'hrk', 'airi', 'szk',
               'khn', 'an', 'akt', 'toya', 'tks', 'emu', 'nene', 'rui', 'knd', 'mfy', 'ena', 'mzk']
char_all_ja = ['ミク', 'リン', 'レン', 'ルカ', 'MEIKO', 'KAITO', '一歌', '咲希', '穂波', '志歩', 'みのり', '遥', '愛莉', '雫',
               'こはね', '杏', '彰人', '冬弥', '司', 'えむ', '寧々', '類', '奏', 'まふゆ', '絵名', '瑞希']
char_all_zh = ['ミク', 'リン', 'レン', 'ルカ', 'MEIKO', 'KAITO', '星乃一歌', '天马咲希', '望月穗波', '日野森志步', 'みのり', '遥', '愛莉', '雫',
               'こはね', '杏', '彰人', '冬弥', '司', 'えむ', '寧々', '類', 'knd', 'mfy', 'ena', 'mzk']
# color_rgb = {'miku':(51, 204, 187), 'len':(255,238,17), 'mei':(221,68,68),
#     'khn':(255, 102, 153), 'an':(0, 187, 221), 'akt':(255, 119, 34), 'toya':(0, 119, 221),
#     'knd':(187,102,136), 'mfy':(136,136,204), 'ena':(204,170,136), 'mzk':(221,170,204)}
main_fontsize = 90
zoom_scale = 80

speakers = 'KAITO；星乃一歌；天马咲希；望月穗波；日野森志步；合唱；KAITO、星乃一歌；天马咲希、望月穗波、日野森志步；KAITO、星乃一歌、天马咲希、望月穗波、日野森志步'.replace('、',';').split('；')
speakers = ['リン;絵名', 'リン;まふゆ', 'リン;奏;瑞希', 'まふゆ;絵名;瑞希', 'リン;奏;まふゆ;絵名', 'リン;奏;まふゆ;瑞希', 'リン;奏', 'リン;まふゆ;瑞希', '奏;絵名;瑞希',
'リン;奏;絵名;瑞希', 'リン;瑞希', '奏', '絵名', '瑞希', 'まふゆ', 'リン']

if __name__=='__main__':
    # for i in ['KAF', 'ISEKAI', 'RIM', 'KOKO', 'HARUS']:
    #     crop_to_inscribed_circle(output_path+i+'.jpg', output_path+i+'.png')
    for length in range(len(char_en)):
        # if length in (1,2,3): continue
        for combo in itertools.combinations(range(len(char_en)), length+1):
            if 1: # ';'.join([char_zh[i] for i in combo]) in speakers: # 1
                images = [Image.open(input_path+f"{char_en[i]}{image_extension}").convert("RGBA").resize(image_size)
                         for i in combo]

                canvas = Image.new('RGBA', (image_size[0] * len(combo), image_size[1]), (0, 0, 0, 0))
                
                x_offset = 0
                for img in images:
                    canvas.paste(img, (x_offset, 0), mask=img)
                    x_offset += img.width
                
                filename = f"{''.join([char_en[i] for i in combo])}.png"
                canvas.save(output_path+filename) # 角色拼图
                # if length == 0:
                #     generate_color_image([color_rgb[char_en[i]] for i in combo], output_path+'color//'+filename, 0, -10) # 单色图
                # print(f"@Emoji=【{';'.join([char_zh[i] for i in combo])}】,{filename},,NoDecor,MarginRight=15,MarginBottom=15") # 中插
                print(f"@Emoji=【{';'.join([char_zh[i] for i in combo])}】,{filename},,Zoom={zoom_scale}%,NoDecor"+ \
                    f",MarginRight=-999,MarginBottom={-main_fontsize*zoom_scale/100-2}") # canvas.width/canvas.height*98*zoom_scale/100 # 下插
    print(f"@Emoji=【合唱】,{filename},,Zoom={zoom_scale}%,NoDecor,MarginRight=-999,MarginBottom={-main_fontsize*zoom_scale/100-2}")
    # crop_to_inscribed_circle(output_path+'channels4_profile.jpg', output_path+'2.png') # 裁圆