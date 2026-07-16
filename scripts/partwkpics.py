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

input_path = 'E://Pictures//ACGN//PJSK//Qln//' # Qln
# input_path = 'E://Pictures//ACGN//profiles//'
image_extension = '.png'
image_size = (400, 400) # (256,256) # (128, 128)
output_path = 'E://Videos//nicokara//260507hoshi//'
# char_zh = 'KAITO；星乃一歌；天马咲希；望月穗波；日野森志步'.split('；')
char_zh = ['レン', '一歌', '咲希', '穂波', '志歩']
char_en = ['len', 'ick', 'saki', 'hnm', 'shiho']
# char_zh = ['KAITO', 'こはね', '杏', '彰人', '冬弥']
# char_en = ['kai', 'khn', 'an', 'akt', 'toya']

if 'gakumas':
    char_ja_gakumas = ['咲季', '手毬', 'ことね', 'リーリヤ', '清夏',
        '千奈', '広', '佑芽', '美鈴',
        '麻央', '莉波', '星南']
        '麻央', '莉波', '星南', '燕']
    char_en_gakumas = ['hski', 'ttmr', 'fktn', 'kllj', 'ssmk',
        'kcna', 'shro', 'hume', 'hmsz',
        'amao', 'hrnm', 'jsna']
        'amao', 'hrnm', 'jsna', 'atbm']
    color_gakumas = ['#EA4A5B', '#4FA0CE', '#FAD356', '#EFFDFF', '#A2FD47',
        '#F8AC5E', '#48C6DA', '#EF8472', '#A0B6DC',
        '#A453A6', '#F9C4D6', '#F9C584']
        '#A453A6', '#F9C4D6', '#F9C584', '']

# char_zh = char_ja_gakumas
# char_en = char_en_gakumas
# char_en = ['KAFU', 'SEKAI', 'RIME', 'COKO', 'HARU']
# char_en = ['KAF', 'KAFU', 'ISEKAI', 'SEKAI', 'RIM', 'RIME', 'KOKO', 'COKO', 'HARUS', 'HARU']
char_all_en = ['miku', 'rin', 'len', 'luka', 'mei', 'kai', 'ick', 'saki', 'hnm', 'shiho', 'mnr', 'hrk', 'airi', 'szk',
               'khn', 'an', 'akt', 'toya', 'tks', 'emu', 'nene', 'rui', 'knd', 'mfy', 'ena', 'mzk']
char_all_ja = ['ミク', 'リン', 'レン', 'ルカ', 'MEIKO', 'KAITO', '一歌', '咲希', '穂波', '志歩', 'みのり', '遥', '愛莉', '雫',
               'こはね', '杏', '彰人', '冬弥', '司', 'えむ', '寧々', '類', '奏', 'まふゆ', '絵名', '瑞希']

# char_all_zh = ['ミク', 'リン', 'レン', 'ルカ', 'MEIKO', 'KAITO', '星乃一歌', '天马咲希', '望月穗波', '日野森志步', 'みのり', '遥', '愛莉', '雫',
#                'こはね', '杏', '彰人', '冬弥', '司', 'えむ', '寧々', '類', 'knd', 'mfy', 'ena', 'mzk']
# color_rgb = {'miku':(51, 204, 187), 'len':(255,238,17), 'mei':(221,68,68),
#     'khn':(255, 102, 153), 'an':(0, 187, 221), 'akt':(255, 119, 34), 'toya':(0, 119, 221),
#     'knd':(187,102,136), 'mfy':(136,136,204), 'ena':(204,170,136), 'mzk':(221,170,204)}
main_fontsize = 97.5 # 90
zoom_scale = 80
char_zh_to_idx = {name: idx for idx, name in enumerate(char_zh)}

speakers = 'KAITO；星乃一歌；天马咲希；望月穗波；日野森志步；合唱；KAITO、星乃一歌；天马咲希、望月穗波、日野森志步；KAITO、星乃一歌、天马咲希、望月穗波、日野森志步'.replace('、',';').split('；')
speakers = ['レン;一歌;咲希;穂波;志歩', '一歌;穂波', '穂波;志歩', '咲希;穂波', '一歌;咲希;穂波;志歩',
    '穂波', '志歩', '咲希', '一歌', 'レン', '咲希;穂波_志歩', '一歌;穂波_咲希', '穂波;志歩_一歌']

if __name__=='__main__':
    for pattern in speakers:
        if '_' in pattern:  # main_chorus
            main_part, harmony_part = pattern.split('_', 1)
            main_names = main_part.split(';')
            harmony_names = harmony_part.split(';')
            
            main_indices = [char_zh_to_idx[name] for name in main_names if name in char_zh_to_idx]
            harmony_indices = [char_zh_to_idx[name] for name in harmony_names if name in char_zh_to_idx]
            
            if not main_indices or not harmony_indices:
                print(f"跳过无效模式: {pattern}")
                continue
            
            # 加载主旋律图片（原尺寸）
            main_images = []
            for i in main_indices:
                img = Image.open(input_path + f"{char_en[i]}{image_extension}").convert("RGBA")
                img = img.resize(image_size)
                main_images.append(img)
            
            # 加载和声图片并缩放到70%
            scale = 0.7
            harmony_images = []
            for i in harmony_indices:
                img = Image.open(input_path + f"{char_en[i]}{image_extension}").convert("RGBA")
                img = img.resize(image_size)
                new_size = (int(img.width * scale), int(img.height * scale))
                img_resized = img.resize(new_size)
                harmony_images.append(img_resized)
            
            # 计算画布尺寸
            main_total_w = sum(img.width for img in main_images)
            harmony_total_w = sum(img.width for img in harmony_images)
            canvas_w = main_total_w + harmony_total_w
            canvas_h = image_size[1]
            canvas = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
            
            # 放置主旋律（顶部对齐）
            x = 0
            for img in main_images:
                canvas.paste(img, (x, 0), mask=img)
                x += img.width
            
            # 放置和声（底部对齐）
            for img in harmony_images:
                y = canvas_h - img.height
                canvas.paste(img, (x, y), mask=img)
                x += img.width
            
            # 生成文件名
            main_en = ''.join([char_en[i] for i in main_indices])
            harmony_en = ''.join([char_en[i] for i in harmony_indices])
            filename = f"{main_en}_{harmony_en}.png"
            canvas.save(output_path + filename)
            print(f"@Emoji=【{pattern}】,{filename},,Zoom={zoom_scale}%,NoDecor"+ \
                f",MarginRight=-999,MarginBottom={-main_fontsize*zoom_scale/100-2}")
            
        else:  # main
            names = pattern.split(';')
            indices = [char_zh_to_idx[name] for name in names if name in char_zh_to_idx]
            
            if not indices:
                print(f"跳过无效模式: {pattern}")
                continue
            # for combo in itertools.combinations(range(len(char_en)), length+1): # permutations
            #     if ';'.join([char_zh[i] for i in combo]) in speakers:
            images = []
            for i in indices:
                img = Image.open(input_path + f"{char_en[i]}{image_extension}").convert("RGBA")
                img = img.resize(image_size)
                images.append(img)
            
            # 创建画布
            canvas = Image.new('RGBA', (image_size[0] * len(indices), image_size[1]), (0, 0, 0, 0))
            x = 0
            for img in images:
                canvas.paste(img, (x, 0), mask=img)
                x += img.width
            
            filename = f"{''.join([char_en[i] for i in indices])}.png"
            canvas.save(output_path + filename)
            print(f"@Emoji=【{pattern}】,{filename},,Zoom={zoom_scale}%,NoDecor"+ \
                f",MarginRight=-999,MarginBottom={-main_fontsize*zoom_scale/100-2}")

    # crop_to_inscribed_circle(output_path+'1.png', output_path+'2.png') # 裁圆