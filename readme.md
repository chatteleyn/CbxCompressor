# CbxCompressor

CbxCompress is a small python project to compress your .cbz comics/mangas

With CbzCompressor you can convert your .cbz into shades of grey and change its resolution

## Installation

```bash
pip install PIL
pip install zipfile
```

## Usage

```bash
py cbx_compressor [-grey] [-size`<s>] [-width <w>] [-height <h>] [-output <dir_path>] [-verbose] path
```

### Arguments
- ```-grey``` : Convert all the images into shades of grey
- ```-size <s>``` : Reduce the size of all the images (<s> as to be a multiplicator between 0 and 1) (exemple : ```-size 0.5```)
- ```-width <w>``` : Change the width (in px) of all the images (exemple : ```-width 720```)
- ```-height <h>``` : Change the height (in px) of all the images (exemple : ```-width 1280```)
- ```-output <dir_path>``` : Change the destination directory for the compressed file (by default the original file is remplaced)
- ```-verbose``` : Enable the verbose mode
- ```path``` : Path of a .cbz file or a directory containing .cbz files

## Contributing
Feel free to contribute to this project !

## License
[MIT](https://choosealicense.com/licenses/mit/)