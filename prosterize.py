from sys import argv 

from PIL import Image, ImageDraw, ImageFont 

img = Image.open(argv[1])
size = int(argv[2])

# create a new image that is the same size as the original
out = Image.new('RGB', img.size, 'white')
font = ImageFont.truetype('Inconsolata-Bold.ttf', size)
draw = ImageDraw.Draw(out)
cont = True
letters = ' '.join(open('speech.txt', 'rb').read().replace('\r\n', ' ').split())
x, y = 0, 0

# repeat text until we are completely out of space on the image
while cont:
    for letter in letters:
        # determine the bounding box of the next letter without drawing it
        width, height = draw.textsize(letter, font=font)
        # determine what the most prominent color is within that bounding box on the original image
        part = img.crop((x, y + height, x + width, y + height + size))
        colors = part.getcolors()
        # draw it with that color on the new image
        draw.text((x, y), letter, colors[0][1] if colors else (0, 0, 0,), font=font)
        # adjust coords, jump to next lines, and eventually quit
    	x += width
        if x > img.size[0]:
            x = 0
            y += size 
        if y > img.size[1]:
            cont = False

out.save('out.jpg')
