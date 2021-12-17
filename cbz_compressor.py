import sys
import os
from zipfile import ZipFile
from PIL import Image

TEMP_DIR_PATH= "temp"
ARGUMENTS = {
    "output" : {
        "aliases" : ["-output","-o"],
        "type" : str,
        "value" : None
    },
    "verbose" : {
        "aliases" : ["-verbose","-v"],
        "type" : bool,
        "value" : False
    },
    "grey" : {
        "aliases" : ["-grey","-g"],
        "type" : bool,
        "value" : False
    },
    "size" : {
        "aliases" : ["-size","-s"],
        "type" : float,
        "value" : None
    },
    "width" : {
        "aliases" : ["-width","-w"],
        "type" : int,
        "value" : None
    },
    "height" : {
        "aliases" : ["-height","-h"],
        "type" : int,
        "value" : None
    },
}

def argument_parser(args_data):
    args = sys.argv
    i = 0
    while i < len(args):
        if args[i][:1] == "-":
            for arg in args_data:
                if args[i] in args_data[arg]["aliases"]:
                    if args_data[arg]["type"] is bool:
                        args_data[arg]["value"] = True
                    elif args_data[arg]["type"] is str:
                        if i+1 < len(args) and args[i+1][:1] != "-":
                            args_data[arg]["value"] = args[i+1]
                            i+=1
                    elif args_data[arg]["type"] is int:
                        if i+1 < len(args) and args[i+1][:1] != "-":
                            args_data[arg]["value"] = int(args[i+1])
                            i+=1
                    elif args_data[arg]["type"] is float:
                        if i+1 < len(args) and args[i+1][:1] != "-":
                            args_data[arg]["value"] = float(args[i+1])
                            i+=1
        i+=1

    return args_data

def create_temp_dir():
    if not os.path.isdir(TEMP_DIR_PATH):
        os.mkdir(TEMP_DIR_PATH)

def remove_temp_dir():
    if os.path.isdir(TEMP_DIR_PATH):
        for file_name in os.listdir(TEMP_DIR_PATH):
            os.remove(TEMP_DIR_PATH+"\\"+file_name)
        os.rmdir(TEMP_DIR_PATH)

def compress_cbz(file_path,output_path=None,grey=False,size=None,width=None,height=None,verbose=False):
    if os.path.isdir(file_path):
        print("[Error] '{}' is a directory".format(os.path.basename(file_path)))
        return False
    elif file_path[-4:] != ".cbz":
        print("[Error] '{}' is not a cbz file".format(os.path.basename(file_path)))
        return False

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

    for i,image_file in enumerate(image_list):
        img = Image.open(TEMP_DIR_PATH+"\\"+image_file)
        if size is not None and size >= 0 and size <= 1:
            img = img.resize((img.width*size,img.height*size))
        elif width is not None and height is not None:
            img = img.resize((width,height))
        if grey:
            img = img = img.convert('L')
        img.save(TEMP_DIR_PATH+"\\"+image_file, format='JPEG')
        new_cbz_file.write(TEMP_DIR_PATH+"\\"+image_file,arcname=image_file)
        
        if verbose:
            print("Image compressed in '{}' : {}/{} [{}%]".format(os.path.basename(file_path),i+1,len(image_list),int((i+1)*100/len(image_list))))

    remove_temp_dir()

    print("> Compressed '{}'".format(os.path.basename(file_path)))
    
    return True

def compress_directory(dir_path,output_path=None,grey=False,size=None,width=None,height=None,verbose=False):
    cbz_list = os.listdir(dir_path)
    for cbz_file in cbz_list:
        compress_cbz(dir_path+"\\"+cbz_file,output_path,grey,size,width,height,verbose)
    
    return True

if __name__ == "__main__":
    args = argument_parser(ARGUMENTS)

    if os.path.isfile(os.path.realpath(sys.argv[-1])):
        compress_cbz(
        file_path=os.path.realpath(sys.argv[-1]),
        output_path=args["output"]["value"],
        grey=args["grey"]["value"],
        size=args["size"]["value"],
        width=args["width"]["value"],
        height=args["height"]["value"],
        verbose=args["verbose"]["value"])
    
    elif os.path.isdir(os.path.realpath(sys.argv[-1])):
        compress_directory(
        dir_path=os.path.realpath(sys.argv[-1]),
        output_path=args["output"]["value"],
        grey=args["grey"]["value"],
        size=args["size"]["value"],
        width=args["width"]["value"],
        height=args["height"]["value"],
        verbose=args["verbose"]["value"])