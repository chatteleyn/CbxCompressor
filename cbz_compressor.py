import sys
import os
from zipfile import ZipFile
from PIL import Image

TEMP_DIR_PATH= "temp"

def argument_parser():
    args = sys.argv
    parsed_args = {}
    i = 0
    while i < len(args):
        if args[i][:1] == "-":
            if i+1 <= len(args) and args[i+1][:1] != "-":
                parsed_args[args[i]] = args[i+1]
                i += 1
            else:
                parsed_args[args[i]] = None
        i += 1
    
    return parsed_args

def create_temp_dir():
    if not os.path.isdir(TEMP_DIR_PATH):
        os.mkdir(TEMP_DIR_PATH)

def remove_temp_dir():
    if os.path.isdir(TEMP_DIR_PATH):
        for file_name in os.listdir(TEMP_DIR_PATH):
            os.remove(TEMP_DIR_PATH+"\\"+file_name)
        os.rmdir(TEMP_DIR_PATH)

def compress_cbz(file_path,output_path,grey=False,width=None,height=None):
    print("> Compressing '{}' ...".format(os.path.basename(file_path)))

    create_temp_dir()

    with ZipFile(file_path, 'r') as cbz_file:
        cbz_file.extractall(TEMP_DIR_PATH)

    if output_path is None:
        new_cbz_file = ZipFile(file_path,mode="w")
    else:
        if not os.path.isdir(output_path):
            os.mkdir(output_path)
        new_cbz_file = ZipFile(output_path+"\\"+os.path.basename(file_path),mode="w")

    image_list = os.listdir(TEMP_DIR_PATH)

    for image_file in image_list:
        img = Image.open(TEMP_DIR_PATH+"\\"+image_file)
        if width is not None and height is not None:
            img = img.resize((width,height))
        if grey:
            img = img = img.convert('L')
        img.save(TEMP_DIR_PATH+"\\"+image_file, format='JPEG')
        new_cbz_file.write(TEMP_DIR_PATH+"\\"+image_file,arcname=image_file)

    remove_temp_dir()

    print("> Compressed '{}'".format(os.path.basename(file_path)))
                
if __name__ == "__main__":
    args = argument_parser()
    if "-output" in args and args["-output"] is not None:
        output_path = args["-output"]
    else:
        output_path = None
    if "-grey" in args:
        grey = True
    else:
        grey = False
    if "-width" in args and args["-width"] is not None:
        width = int(args["-width"])
    else:
        width = None
    if "-height" in args and args["-height"] is not None:
        height = int(args["-height"])
    else:
        height = None

    compress_cbz(os.path.realpath(sys.argv[-1]),output_path,grey,width,height)