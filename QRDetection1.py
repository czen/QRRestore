import numpy as np
import argparse
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
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # compute the Scharr gradient magnitude representation of the images
    # in both the x and y direction
    gradX = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    gradY = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)
    # subtract the y-gradient from the x-gradient
    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)
    median = cv2.medianBlur(gradient, 5)
    (_, threshold) = cv2.threshold(median, 225, 255, cv2.THRESH_BINARY)
    # cv2.imshow('threshold', threshold)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))  # latest 7 7
    closed = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel)
    # cv2. imshow('closed', closed)
    im22, contors2, _ = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c1 = sorted(contors2, key=cv2.contourArea, reverse=True)[0]
    rect = cv2.minAreaRect(c1)
    x, y, width, height = cv2.boundingRect(c1)
    qr = image[y:y+height, x:x+width]

    qr = process_qr(qr)
    # cv2.imwrite('qr_dec.jpg', qr)
    # print(x, y)
    # dst = cv2.fastNlMeansDenoisingColored(qr, None, 10, 10, 7, 21)
    #cv2.imshow('qr', qr)
    cv2.imwrite(output + filename, qr)
    #cv2.imshow('result', qr)
    #cv2.waitKey(0)
    # box1 = np.int0(cv2.boxPoints(rect))
    # cv2.drawContours(copy_image, [box1], -1, (255, 0, 0), 3)
    # cv2.imwrite(output + filename, qr)
    # cv2.waitKey(0)


def process_qr(qr):
    # gray = cv2.cvtColor(qr, cv2.COLOR_BGR2GRAY)
    # gray = cv2.medianBlur(gray, 5)
    #
    # gradX = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    # gradY = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)
    # # subtract the y-gradient from the x-gradient
    # gradient = cv2.subtract(gradX, gradY)
    # gradient = cv2.convertScaleAbs(gradient)
    # # median = cv2.medianBlur(gradient, 5)
    # (_, threshold) = cv2.threshold(gradient, 225, 255, cv2.THRESH_BINARY)
    # median = cv2.medianBlur(threshold, 5) # threshold
    # bilateral = cv2.bilateralFilter(threshold, 5, 75, 75)
    # # cv2.imshow('qr', gray)
    # cv2.imshow('qr_gradient', median)
    # cv2.imwrite('qr.jpg', bilateral)  # threshold

    sensitivity = 30
    lower_white = np.array([0, 0, 255 - sensitivity])
    upper_white = np.array([255, sensitivity, 255])
    hsv = cv2.cvtColor(qr, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_white, upper_white)
    # thresh = cv2.inRange(hsv, lower_white, upper_white)
    res = cv2.bitwise_and(qr, qr, mask=mask)
    # median = cv2.medianBlur(res, 3)  # threshold
    return(res)


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