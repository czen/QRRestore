import numpy as np
import argparse
# use https://docs.opencv.org/3.4.0/df/d3d/tutorial_py_inpainting.html
# нужно сделать маску около черных пикселов
# потом применить cv.inpaint с этой маской


import cv2
import os


def process_high_image(args):
    input = args['input']
    output = args["output"]
    if not os.path.exists(args["input"]):
        raise BaseException('Error! File {} is not exist'.format(input))
    if not os.path.isdir(output):
        raise BaseException('Error! Directory {} is not exist'.format(output))
    image = cv2.imread(input)
    filename = input.split('/')[-1]
    copy_image = image.copy()
    
    cv2.imwrite(output + filename, copy_image)
    cv2.waitKey(0)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="path to the image file")
    ap.add_argument("-o", "--output", required=True, help="path to the output image file")
    # ap.add_argument("-b", "--high", requred=False, help="mode with huge QR code")
    # ap.add_argument("-l", "--low", requred=False, help="mode with low QR code")

    args = vars(ap.parse_args())
    process_high_image(args)


    '''
        INPUT EXAMPLE!
        python QRDetection.py -i data/1.jpg -o output/
        
    '''