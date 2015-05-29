from sys import argv 

from PIL import Image, ImageDraw, ImageFont 

img = Image.open(argv[1])
text_path = argv[2]
out_path = argv[3]
font_path = argv[4]
font_size = int(argv[5])

file = open(text_path, 'rb')
text = ' '.join(file.read().replace('\r\n', ' ').split())
file.close()

# create a new image that is the same size as the original
out = Image.new('RGB', img.size, 'white')
font = ImageFont.truetype(font_path, font_size)
draw = ImageDraw.Draw(out)
cont = True
x, y = 0, 0

# repeat text until we are completely out of space on the image
while cont:
    for letter in text:
        # determine the bounding box of the next letter without drawing it
        width, height = draw.textsize(letter, font=font)
        # determine what the most prominent color is within that bounding box on the original image
        part = img.crop((x, y + height, x + width, y + height + font_size))
        colors = part.getcolors()
        # draw it with that color on the new image
        draw.text((x, y), letter, colors[0][1] if colors else (0, 0, 0), font=font)
        # adjust coords, jump to next line, and eventually quit
    	x += width
        if x > img.size[0]:
            x = 0
            y += font_size 
        if y > img.size[1]:
            cont = False

out.save(out_path)
