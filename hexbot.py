# TODO: Need to allow user to use glitch gradient, need to make smooth many gradient
# Import libraries
import time  # Used to find how fast the program was
import json  # Parse JSON from API
import certifi  # SSL Verification
import urllib3  # Interact with API
from PIL import Image  # Used to create the images
import os  # Used to find directory
import numpy  # Used to sort the 2D array


class HexBot:
    # Makes a image size of 100*100 pixels
    w = 0
    h = 0

    img = 0
    d = os.path.abspath(os.path.dirname(__file__))  # directory of script

    # Starts up a manager, uses ssl
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where())

    # Gets RGB value from hex
    @staticmethod
    def get_rgb(_hex):
        _hex = _hex.lstrip('#')
        return tuple(int(_hex[i:i+2], 16) for i in (0, 2, 4))

    # Gets int value of hex string
    @staticmethod
    def hex_to_int(_hex):
        _hex = _hex.lstrip('#')
        return int(_hex, 16)

    @staticmethod
    def numpy_sort(sort_list):
        sort_list = numpy.sort(sort_list, axis=0)
        sort_list = numpy.sort(sort_list, axis=1)
        return sort_list

    # Changes the size of the image to work on
    def change_size(self, i_w, i_h):
        self.w = i_w
        self.h = i_h
        self.img = Image.new('RGB', (self.w, self.h))

    # Requests a series of hex values
    def request_hex(self, quantity):
        request = 'https://api.noopschallenge.com/hexbot?count=' + quantity
        response = self.http.request('GET', request)
        json_data = json.loads(response.data)
        return json_data

    # Enlarges the image using nearest neighbour, saves as png
    def enlarge(self, img, new_width, name):
        w_percent = (new_width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        img = img.resize((new_width, h_size), Image.NEAREST)
        with open('%s/%s.png' % (self.d, name), 'wb') as f:
            img.save(f)

    # Sorts 2D array using bubble sort, but doesn't work
    def bubble_2d(self, sort_list):
        for i in range(self.w):  # x loop
            for j in range(self.h):  # y loop
                for k in range(self.h - 1):  # gets next row
                    # If left bigger than right value, switch
                    if sort_list[i][k] > sort_list[i][k+1]:
                        t = sort_list[i][k]
                        sort_list[i][k] = sort_list[i][k + 1]
                        sort_list[i][k + 1] = t
        return sort_list

    # Hopefully actually successful at a bubble sort
    def bubble_new_2d(self, sort_list):
        for i in range(self.w):  # x loop
            for j in range(self.h):  # y loop
                for k in range(self.h - 1):  # gets next row
                    # If left bigger than right value, switch
                    if sort_list[i][k] > sort_list[i][k+1]:
                        t = sort_list[i][k]
                        sort_list[i][k] = sort_list[i][k + 1]
                        sort_list[i][k + 1] = t
        return sort_list

    def save_image(self, sort_type, values, save_type):
        save_type += '-'
        if sort_type is 'bubble':
            self.enlarge(
                self.img, 1000, 'gradients\\glitch\\%s%s' % (save_type, values))
        elif sort_type is 'numpy':
            self.enlarge(
                self.img, 1000, 'gradients\\two\\%s%s' % (save_type, values))
        elif sort_type is 'numpyOverride':
            self.enlarge(
                self.img, 1000, 'gradients\\numpyGlitch\\%s%s' % (save_type, values))
        elif sort_type is 'debug':
            self.enlarge(
                self.img, 1000, 'gradients\\debug\\%s%s' % (save_type, values))

    # Gets many values from github API, sorts them
    def gradient(self, values, sort_type):
        # Vars
        pixels = self.img.load()  # Loads var img into pixels
        arr_pixels = [[0 for x in range(self.h)] for y in range(self.w)]  # Array size of image
        colours = []  # 2D array to store colours
        count = 0  # Position in colours tracker
        start_time = time.time()  # Starts timer
        # Gets 10,000 pixels and puts it into array
        for i in range((((self.h * self.w - 1)//1000) + 1)):
            request = 'https://api.noopschallenge.com/hexbot?count=1000&seed=%s' % (
                values)
            response = self.http.request('GET', request)
            json_data = json.loads(response.data)

            # Gets every hex value from json data
            for hexValue in (json_data['colors']):
                colours.append(hexValue['value'])

        # Loops through the array pixels, assigns it a value and adds colour to image
        for y in range(self.h):
            for x in range(self.w):
                # Needs to be int so it can be sorted easily
                # Debug : print('x: %s y: %s c: %s' % (x, y, count))
                arr_pixels[x][y] = self.hex_to_int(colours[count])
                
                # Gets the RGB value of the hex
                rgb = self.get_rgb(colours[count])
                pixels[x, y] = rgb  # Sets the value
                count += 1  # Iterates through colours

        # Show how long it took to generate
        print('Generated in %s seconds!' % (time.time() - start_time))

        # Saves unsorted image in correct folder image
        self.save_image(sort_type, values, 'unsorted')

        # Starts timer
        start_time = time.time()

        # Sorts the data with these algorithms / concatenation of functions
        if sort_type is 'numpy' or sort_type is 'numpyOverride':
            arr_pixels = self.numpy_sort(arr_pixels)
        elif sort_type is 'bubble':
            arr_pixels = self.bubble_2d(arr_pixels)
        elif sort_type is 'debug':
            arr_pixels = self.bubble_new_2d(arr_pixels)

        # Used to debug
        file = open(self.d + '\\debug.txt', 'w')
        file.write('')
        file = open(self.d + '\\debug.txt', 'a')

        # Loops through array, getting rgb values and setting image pixels to that
        for y in range(self.h):
            for x in range(self.w):
                # Get int value from array
                val = arr_pixels[x][y]
                # Get hex from val
                _hex = hex(val)
                file.write('x: %s y: %s v: %s h: %s\n' % (x, y, val, _hex))

                # If not padded to 6 bytes add padding to it to be 6 bytes
                if len(_hex[2:]) < 6:
                    pad = 6 - len(_hex[2:])  # Get the amount to pad
                    tmp = _hex[2:]  # Removes 0x
                    for i in range(pad):  # Adds padding to temp
                        tmp = '0' + tmp
                    _hex = '0x' + tmp  # Sets hex value

                rgb = self.get_rgb(_hex[2:])  # Removes 0x. gets rgb val
                pixels[x, y] = rgb  # Sets pixel to value

        # Prints the time it took to generate
        print('Sorted in %s seconds!' % (time.time() - start_time))

        # Debug
        # print(pixels[45, 45])
        # print(pixels[46, 45])
        # print(pixels[47, 45])
        # print(pixels[48, 45])

        # Saves images
        self.save_image(sort_type, values, 'sorted')

        # returns image file names
        images = ['unsorted-' + values, 'sorted-' + values]
        return images

    # def plot_3d(self):
    #    print()

    def __init__(self):
        # Gets location of instillation, checks if dir exists
        gradients_exists = os.path.isdir(self.d + '\\gradients\\')
        two_exists = os.path.isdir(self.d + '\\gradients\\two')
        glitch_exists = os.path.isdir(self.d + '\\gradients\\glitch')
        numpy_glitch_exists = os.path.isdir(self.d + '\\gradients\\numpyGlitch')
        debug_exists = os.path.isdir(self.d + '\\gradients\\debug')

        if not gradients_exists:
            os.mkdir(self.d + '\\gradients\\')

        if not two_exists:
            os.mkdir(self.d + '\\gradients\\two')

        if not glitch_exists:
            os.mkdir(self.d + '\\gradients\\glitch')

        if not numpy_glitch_exists:
            os.mkdir(self.d + '\\gradients\\numpyGlitch')

        if not debug_exists:
            os.mkdir(self.d + '\\gradients\\debug')
