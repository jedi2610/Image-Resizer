# Image-Resizer

> Resizing your images using shady websites may concern some people. This python based CLI comes to the rescue.
> Resize images, without any concern on hidden payloads, by yourself

## Dependencies

- Pillow - `pip install pillow`

## Supported Image types:
- PNG
- JPG
- BMP
- PPM
- TIFF

## Usage

```
usage: resizer.py [-h] [-a] [-f] [-o OUTPUT] input size [size ...]

positional arguments:
  input                 Path of the input file/folder.
  size                  The desired dimensions in pixels as a tuple: (w, h).

optional arguments:
  -h, --help            show this help message and exit
  -a, --aspect          Forces to stick with the aspect ratio of the original
                        image.[Default = True]
  -f, --force           Force resize the image even if the given dimensions
                        are not on par with the original image dimensions.
  -o OUTPUT, --output OUTPUT
                        Path of the output file without extension.
```

## Examples

- `resizer.py "D:\\Images\\test.png" 1920 1080` - resizes the image and saves the resized image at "D:\\Images\\Resized_Images\\test.png".
- `resizer.py -f "D:\\Images\\test.png" 1920 1080` - resizes the image even if the aspect ratio's don't match up.
- `resizer.py "D:\\Images\\test.png" 1920 1080 -o "D:\\Images\\test1.png"` - resizes the image and saves the resized image at "D:\\Images\\test1.png".
- `resizer.py -f "D\\Images" 1920 1080` - resizes all the images in the directory

> Note: It is recommened to use the '-f' tag while resizing images in a whole directory. '-o' tag is not supported for directories

## TODO
- [ ] Add support for image compression

## License

[MIT](/LICENSE) License