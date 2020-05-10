import argparse
from fractions import Fraction
from PIL import Image

class Resize():
    """
    @param imageObject: An 'Image' object of the PIL module.
    """
    def __init__(self, imageObject):
        self.imageObject = imageObject
        self.size = imageObject.size
        self.aspectRatio = self.size[0] / self.size[1]

    def forceResize(self, dimensions):
        outFile = self.imageObject.resize(dimensions, Image.ANTIALIAS)
        return outFile


def main(args):
    imgPath = 'D:\\Images\\Wallpapers\\Desktop Wallpapers\\macOS\\MBA2020.png'
    imgObject = Image.open(imgPath)
    originalSize = imgObject.size

    #  Printing properties of the original image
    print("\nOriginal image properties: ")
    print("\tSize: ", originalSize)
    print("\tAspect ratio: ", Fraction(originalSize[0], originalSize[1]), "~", round(originalSize[0] / originalSize[1], 2))
    
    if args.force:
        outFile = Resize(imgObject).forceResize((1920, 1080))
        newSize = outFile.size
        outFile.show()

    # Printing properties of the resized image
    print("\nResized image properties: ")
    print("\tSize: ", newSize)
    print("\tAspect ratio: ", Fraction(newSize[0], newSize[1]), "~", round(newSize[0]/newSize[1], 2))

if __name__ == "__main__":
    
    # Parsing command line args
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', metavar='dimensions', type=tuple, dest='size', help='The desired dimensions in pixels as a tuple: (w, h).')
    parser.add_argument('-a', action='store_true', dest='aspect', help='Forces to stick with the aspect ratio of the original image. The image is not resized if the given dimensions are not on par with the original image dimensions.')
    parser.add_argument('-f', action='store_true', dest='force', help='Force resize the image even if the given dimensions are not on par with the original image dimensions.')
    parser.add_argument('-o')
    args = parser.parse_args()
    main(args)
