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

    def aspectResize(self, dimensions):
        aspectRatio = dimensions[0] / dimensions[1]
        if aspectRatio == self.aspectRatio:
            outFile = self.imageObject.resize(dimensions, Image.ANTIALIAS)
            return outFile
        else:
            print("\nThe given dimensions do not match the aspect ratio of the original image.")
            option = input("Do you want to force resize it?(Y/N): ").lower()
            if option == 'y':
                return 'y'


def print_properties(text, size):
    print("\nProperties of the {} image: ".format(text))
    print("\tSize: ", size)
    print("\tAspect ratio: ", Fraction(size[0], size[1]), "~", round(size[0] / size[1], 2))


def main(args):
    """
    Driver Code
    """
    imgPath = 'D:\\Images\\Wallpapers\\Desktop Wallpapers\\macOS\\MBA2020.png'
    imgFile = Image.open(imgPath)
    imgObject = Resize(imgFile)
    outFile = None
    originalSize = imgFile.size

    #  Printing properties of the original image
    print_properties('original', originalSize)
    
    if args.force:
        outFile = imgObject.forceResize((1920, 1080))

    elif args.aspect:
        outFile = imgObject.aspectResize((1920, 1080))
        if outFile == 'y':
            outFile = imgObject.forceResize((1920, 1080))

    if outFile != None:
        outFile.show()
        # Printing properties of the resized image
        newSize = outFile.size
        print_properties('resized', newSize)


if __name__ == "__main__":

    # Parsing command line args
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', metavar='dimensions', type=tuple, dest='size', help='The desired dimensions in pixels as a tuple: (w, h).')
    parser.add_argument('-a', action='store_true', dest='aspect', help='Forces to stick with the aspect ratio of the original image. The image is not resized if the given dimensions are not on par with the original image dimensions.')
    parser.add_argument('-f', action='store_true', dest='force', help='Force resize the image even if the given dimensions are not on par with the original image dimensions.')
    parser.add_argument('-o')
    args = parser.parse_args()
    main(args)