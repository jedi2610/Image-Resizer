import os
import argparse
from fractions import Fraction
from PIL import Image

class Resize():
    """
    Class to resize images
    @param imageObject: An 'Image' object of the PIL module.
    """

    def __init__(self, imageObject):
        # Initializing the class with the image and other properties of the image.
        self.imageObject = imageObject
        self.size = imageObject.size
        self.aspectRatio = self.size[0] / self.size[1]

    def forceResize(self, dimensions):
        # Force resize the image even if the aspect ratios do not match
        outFile = self.imageObject.resize(dimensions, Image.BILINEAR)
        return outFile

    def aspectResize(self, dimensions):
        aspectRatio = dimensions[0] / dimensions[1]
        # Tries to stick with the aspect ratio of the original image
        if aspectRatio == self.aspectRatio:
            outFile = self.imageObject.resize(dimensions, Image.ANTIALIAS)
            return outFile
        # If the aspect ratios do not match, get the users consent to force resize the image
        else:
            print_properties('image (if resized)', dimensions)
            print("\nThe given dimensions do not match the aspect ratio of the original image.")
            option = input("Do you want to force resize it?(Y/N): ").lower()
            if option == 'y':
                return 'y'


def print_properties(text, size):
    # Print the image properties
    print("\nProperties of the {}: ".format(text))
    print("\tSize:", size)
    print("\tAspect ratio:", Fraction(size[0], size[1]), "~", round(size[0] / size[1], 2))

def print_exit():
    # Prints a message if an error occurs
    print("\nIf you have a problem, file an issue in the repository with all the details.")
    print("Link to the repository: https://github.com/jedi2610/Image-Resizer")

def main(args):
    """
    Driver Code
    """
    imgPath = args.input
    outPath = args.output
    outPath = args.output
    size = tuple(args.size)

    # Check if the given image path exists
    if not os.path.isfile(imgPath):
        print("\nCannot find the given file", imgPath)
        print("Make sure the file exists and the path contains the image extension.")
        print_exit()
        exit(1)

    # Check if the given dimensions are valid
    if len(size) != 2:
        print("\nThe given size", size, "is not supported.")
        print_exit()
        exit(1)

    imgFile = Image.open(imgPath)
    fileFormat = imgFile.format
    imgObject = Resize(imgFile)
    outFile = None
    originalSize = imgFile.size

    #  Printing properties of the original image
    print_properties('original image', originalSize)
    
    # Checking if the '-f' tag is tagged
    if args.force:
        outFile = imgObject.forceResize(size)

    # Checking if the '-a' tag is tagged
    elif args.aspect:
        outFile = imgObject.aspectResize(size)
        if outFile == 'y':
            outFile = imgObject.forceResize(size)

    # Checking if the outFile is healthy
    if outFile == None:
        print("\nAn error occured. Try again with another image.")
        print_exit()
        exit(1)

    # Printing properties of the resized image
    newSize = outFile.size
    print_properties('resized image', newSize)

    # Saving the resized image
    outFile.show()
    if outPath:
        try:
            outFile.save(outPath, fileFormat)
            print("\nThe image is resized and saved at: \"" + outPath + "\"")
        except IOError:
            print(
                "\nAn error occured while saving the resized image. Check if the given path exists.")
            print_exit()
            exit(1)
    else:
        outPath = '\\'.join(imgPath.split('\\')[0:-1])
        outPath += "\\" + ''.join(imgPath.split('\\')[-1].split('.')[0:-1]) + "_resized." + fileFormat
        try:
            outFile.save(outPath, fileFormat)
            print("\nThe image is resized and saved at: \"" + outPath + "\"")
        except IOError:
            print("\nAn error occured while saving the resized image")
            print_exit()
            exit(1)


if __name__ == "__main__":

    # Parsing command line args
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, help='Path of the input file.')
    parser.add_argument('size', nargs='+', type=int,  help='The desired dimensions in pixels as a tuple: (w, h).')
    parser.add_argument('-a', '--aspect', action='store_true', default=True, dest='aspect', help='Forces to stick with the aspect ratio of the original image.[Default = True]')
    parser.add_argument('-f', '--force', action='store_true', dest='force', help='Force resize the image even if the given dimensions are not on par with the original image dimensions.')
    parser.add_argument('-o', '--output', dest='output', type=str, help='Path of the output file without extension.')
    args = parser.parse_args()

    main(args)
