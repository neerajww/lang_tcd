import os, sys
import skimage.io as skio
import skimage as sk
from skimage.transform import rescale, resize
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import numpy as np

# def imChange(im_name, path='./images'):
#     os.system('rm ./images/current.png')
#     os.system('cp {0:s}/{1:s}.png ./images/current.png'.format(path, im_name))


def showSentence(text):
    W, H = (500, 400)
    img = Image.new('RGB', (W, H), color = (0, 0, 0))
    pointsize = 50
    draw = ImageDraw.Draw(img)

    font_small = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu/UbuntuMono-B.ttf', pointsize)
    text_small = 'Did you hear'
    text_size_small = draw.textsize(text_small, font=font_small) # the size of the text box!

    font_big = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu/UbuntuMono-B.ttf', pointsize + 20)
    text_big = text
    text_size_big = draw.textsize(text_big, font=font_big) # the size of the text box!
    # figure out center x placement:
    x_small = (W / 2) - (text_size_small[0] / 2)
    y_small = (H / 2) - (text_size_small[1] / 2) - ((text_size_big[1] / 2)) - 5
    draw.text((x_small, y_small), text_small, font=font_small, fill=(255, 255, 255))
    x_big = (W / 2) - (text_size_big[0] / 2)
    y_big = (H / 2) - (text_size_big[1] / 2) + ((text_size_small[1] / 2)) + 5
    draw.text((x_big, y_big), text_big, font=font_big, fill=(100, 200, 250))

    img.save('images/p1speak.png')
    imChange('p1speak', resize=False)


def showRandomSentence():
    with open('data/random_sentences.txt') as file:
        lines = file.readlines()
    num = len(lines)
    choice = np.random.randint(0, num)
    showSentence(lines[choice])


def imChange(im_name, path='./images', resize=True):
    # img = sk.color.rgb2gray(skio.imread('{0:s}/{1:s}.png'.format(path, im_name)))
    img = skio.imread('{0:s}/{1:s}.png'.format(path, im_name))
    if len(img.shape) < 3:
        img = sk.color.gray2rgb(img)
    elif img.shape[2] == 4:
        img = sk.color.rgba2rgb(img)
    h = img.shape[0]
    w = img.shape[1]
    # h_corr = 362
    w_corr = 364
    # scale = w_corr / w
    if resize:
        big = np.max([h, w])
        img_new = np.uint8(np.zeros((big, big, 3)))
        w_extra = big - w
        h_extra = big - h
        scale = 350 / big
        img_new[int(h_extra / 2) : int(h_extra / 2) + h, int(w_extra / 2) : int(w_extra / 2) + w, :] = img / np.max(img) * 255
        # skio.imshow(img_new)
        # skio.show()
        img_new = rescale(img_new, scale)#, anti_aliasing=True)
    else:
        img_new = img
    skio.imsave('images/current.png', img_new)


def getImageList(prompt):
    files = []
    prompts = pd.read_excel('data/prompts.xlsx')
    labels = pd.read_excel('data/labels.xlsx')
    b = prompts[prompts['Prompt no.'] == prompt - 0]
    print(b)
    block = b['Block'].values[0]
    prompts = prompts[prompts['Block'] == block]
    ids = sorted(prompts[prompts['Phase'] == 2.1]['Id'].values)
    print(ids)
    for id in ids:
        files.append(labels[labels['Id'] == id]['Image'].values[0])
    return files


def showBlockSpeak(prompt):
    files = getImageList(prompt)
    bg_w, bg_h = (2000, 700)
    background = Image.new('RGB', (bg_w, bg_h), (0, 0, 0))
    pointsize = 80
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu/UbuntuMono-B.ttf', pointsize)
    for i, file in enumerate(files):
        text = str(i + 1)
        text_size = draw.textsize(text, font=font) # the size of the text box!
        x = 190 + 400 * i
        y = 40
        draw.text((x, y), text, font=font, fill=(255, 255, 255))
        
        img = Image.open('images/jap/{0:s}.png'.format(file), 'r')
        basewidth = 365
        img = img.resize((basewidth, basewidth), Image.ANTIALIAS)
        img_w, img_h = img.size
        offset = ((400 - basewidth) // 2 + 400 * i, (bg_h - img_h) // 2)
        background.paste(img, offset)
    background = background.resize((background.size[0] // 2, background.size[1] // 2), Image.ANTIALIAS)
    background.save('images/p3speak.png')
    imChange('p3speak', resize=False)
