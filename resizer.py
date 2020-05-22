import os
import time
import argparse
from glob import glob
from pathlib import Path
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
            return option


def print_properties(text, size):

    # Print the image properties using the given arguments
    print("\nProperties of the {}: ".format(text))
    print("\tSize:", size)
    print("\tAspect ratio:", Fraction(size[0], size[1]), "~", round(size[0] / size[1], 2))

def print_exit():

    # Prints this message if an error occurs
    print("\nIf you have a problem, file an issue in the repository with all the details.")
    print("Link to the repository: https://github.com/jedi2610/Image-Resizer")

def main(args):
    """
    Driver Code
    """
    # Initializing some variables
    startTime = time.time()
    totalCount = 0
    imgExtensions = ['.png', '.jpg', '.jpeg', '.ppm', '.tiff', '.bmp']
    if args.force == True:
            args.aspect = False
    size = tuple(args.size)
    imageFilePaths = list()
    isdir = False
    
    # Check if the given dimensions are valid
    if len(size) != 2:
        print("\nThe given size", size, "is not supported.")
        print_exit()
        exit(1)
    
    # Checking if the given argument is a file or a folder
    if os.path.isfile(args.input):
        if Path(args.input).suffix in imgExtensions:
            imageFilePaths.append(args.input)
        else:
            print("Error. The given file is not an image.")
            print_exit()
            exit(1)

    elif os.path.isdir(args.input):
        # Gets the path of all the image files in a given directory (sub-directories included)
        isdir = True
        for extensions in imgExtensions:
            imageFilePaths += glob('{}\\**/*{}'.format(args.input, extensions), recursive=True)

    else:
        print("\nCannot find the given file/directory", args.input)
        print("Make sure the file/directory exists and the path contains the image extension if it's an image file.")
        print_exit()
        exit(1)

    # Check if the list contains atleast 1 image file path
    if len(imageFilePaths) == 0:
        print("The directory has no image files.")
        print_exit()
        exit(0)
        
    try:
        # Resize all the images in the list
        for filePath in imageFilePaths:

            imageName = os.path.basename(filePath)
            outPath = os.path.dirname(filePath) + "\\Resized_Images\\\\"
            try:
                os.makedirs(outPath, exist_ok=True)
            except OSError:
                print("An error occured while creating the directory.")
                print_exit()
                exit(1)

            imgFile = Image.open(filePath)
            fileFormat = imgFile.format
            imgObject = Resize(imgFile)
            originalSize = imgFile.size
            outFile = None

            #  Printing properties of the original image
            print_properties(f'original image "{imageName}"', originalSize)
            
            # Checking if the '-f' tag is tagged
            if args.force:
                outFile = imgObject.forceResize(size)

            # Checking if the '-a' tag is tagged
            elif args.aspect:
                outFile = imgObject.aspectResize(size)
                if outFile == 'y':
                    outFile = imgObject.forceResize(size)
                elif outFile == 'n':
                    print('------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                    continue

            # Checking if the outFile is healthy
            if outFile == None:
                print("\nAn error occured. Try again with another image.")
                print_exit()
                exit(1)

            # Printing properties of the resized image
            newSize = outFile.size
            print_properties(f'resized image "{imageName}"', newSize)

            # outFile.show()
            # Saving the resized image
            if args.output and not isdir:
                # TODO implement this method if the given path is a folder
                try:
                    outFile.save(args.output, fileFormat)
                    print("\nThe image is resized and saved at: \"" + args.output + "\"")
                    totalCount += 1
                except IOError:
                    print("\nAn error occured while saving the resized image. Check if the given path exists.")
                    print_exit()
                    continue
            else:
                outPath += imageName.split('.')[0]
                outPath += "_resized." + fileFormat
                try:
                    outFile.save(outPath, fileFormat)
                    print("\nThe image is resized and saved at: \"" + outPath + "\"")
                    totalCount += 1
                except IOError:
                    print("\nAn error occured while saving the resized image")
                    print_exit()
                    continue

                print('------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        print("\nTotal files resized:", totalCount)
        print("Time taken:", time.time() - startTime, "seconds")

    except KeyboardInterrupt:
        print("\nProcess terminated.")
        print("\nTotal files resized: ", totalCount)
        print("Time taken: ", time.time() - startTime, "seconds")
        exit(0)


if __name__ == "__main__":

    # Parsing command line args
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, help='Path of the input file/folder.')
    parser.add_argument('size', nargs='+', type=int, help='The desired dimensions in pixels as a tuple: (w, h).')
    parser.add_argument('-a', '--aspect', action='store_true', default=True, dest='aspect', help='Forces to stick with the aspect ratio of the original image.[Default = True]')
    parser.add_argument('-f', '--force', action='store_true', dest='force', help='Force resize the image even if the given dimensions are not on par with the original image dimensions.')
    parser.add_argument('-o', '--output', dest='output', type=str, help='Path of the output file without extension.')
    args = parser.parse_args()

    # TODO add banners
    # TODO clear up the -o tag working for directories
    # TODO print resizing info only if a tag is tagged
    
    main(args)
