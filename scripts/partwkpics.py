from PIL import Image
import itertools
import os

input_path = 'E://Pictures//ACGN//PJSK//'
image_extension = '.png'
image_size = (128, 128)
output_path = 'E://Videos//nicokara//250505if//'
char_zh = '初音未来；花里实乃理；桐谷遥；桃井爱莉；日野森雫'.split('；')
char_en = ['miku', 'mnr', 'hrk', 'airi', 'szk']
main_fontsize = 90

if __name__=='__main__':
    for length in range(len(char_en)):
        for combo in itertools.combinations(range(len(char_en)), length+1):
            images = [Image.open(input_path+f"{char_en[i]}{image_extension}").convert("RGBA") 
                     for i in combo]

            canvas = Image.new('RGBA', (image_size[0] * len(combo), image_size[1]), (0, 0, 0, 0))
            
            x_offset = 0
            for img in images:
                canvas.paste(img, (x_offset, 0), mask=img)
                x_offset += img.width
            
            filename = f"{''.join([char_en[i] for i in combo])}.png"
            canvas.save(output_path+filename)
            # print(f"@Emoji=【{';'.join([char_zh[i] for i in combo])}】,{filename},,NoDecor,MarginRight=15,MarginBottom=15")
            print(f"@Emoji=【{';'.join([char_zh[i] for i in combo])}】,{filename},,NoDecor,MarginRight={-canvas.width},MarginBottom={-main_fontsize}")
    print(f"@Emoji=【合唱】,{filename},,NoDecor,MarginRight={-canvas.width},MarginBottom={-main_fontsize}")