from io import BytesIO                       #Used for byte stream, required when saving svg to png
import math                                  #Used for calucations while converting rgba to rgb 
from cairosvg import svg2png                 #Used for converting svg to png
from PIL import Image                        #Used for handling image operations
import numpy as np                           #Used in packing bits to bytes
from string import Template                  #Used for string templating for file handling
import argparse                              #Used for taking input from command line
import glob                                  #Used for locating all the images, needed to to processed

#converts rgba value to its corresponding rgb value 
def rgba_to_2bit(image):
    white_image = Image.new('RGBA', image.size, (255, 255, 255))
    image = Image.alpha_composite(white_image, image)
    image = image.convert('L')
    image = image.quantize(4)
    return image
        
#converts image to byte array
def image_to_array(im):
    im = rgba_to_2bit(im)
    array = []
    im = np.array(im)
    im = im.reshape(im.size//4,4)
    setbits = np.array([0, 2, 4, 6])
    for i in im:
        bits = i<<setbits
        array.append(bits.sum())
    return array

#processes image to 2 bit image array.
def process_image(image, filestream, argsParsed):
    svg2png(url = image, write_to = filestream)
    filestream.seek(0)
    im = Image.open(filestream)
    im = im.resize((argsParsed.width, argsParsed.height))
    uint_array = image_to_array(im)
    hexadecimal_array = ', '.join(hex(num) for num in uint_array)
    return hexadecimal_array

#processes Hexa-decimal array in C header file,which other arguments in C header
def array_to_headerfile(image, hexadecimal_array, argsParsed):
    icon_name = image[slice(0,-4)]
    file_name = icon_name.upper()
    content = {
        'ICON_TEMPLATE_H' : file_name + '_H',
        'ICON_NAME' : icon_name,
        'WIDTH' : argsParsed.width,
        'HEIGHT' : argsParsed.height,
        'IMAGE_DATA' : hexadecimal_array 
    }
    with open('icon_template.h', 'r') as template_content:
        h_template = Template(template_content.read())
        file_content = h_template.substitute(content)
        print(file_content)
        header_file = open(file_name + '_2BIT.h', 'w')
        header_file.write(file_content)
        header_file.close()

#handles input files, and starts conversion to array.
def handle_input_argument(argsParsed):
    files = ''
    if argsParsed.input == 'all':
      files = glob.glob('*_icon.svg')
    else:
      files = argsParsed.input
    for image in files:
        #context closes automatically(scoped), it does not require f.close()
        with BytesIO() as f:
            hexadecimal_array = process_image(image, f, argsParsed)
            array_to_headerfile(image, hexadecimal_array, argsParsed)
    
def main():
    argParse = argparse.ArgumentParser(prog = 'IMAGE_TO_ARRAY', description = 'Convert Image Files to C header Files')
    argParse.add_argument("-i", "--input", required = True, help = "Path of Input Image.", type = str)
    argParse.add_argument("-iw", "--width", default = 24, required = False, help = "Width of output image", type = int)
    argParse.add_argument("-ih", "--height", default = 24, required = False, help = "Height of output image", type = int)
    argsParsed = argParse.parse_args()
    
    handle_input_argument(argsParsed)
        
if __name__ == '__main__':
    main()
