#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import serial, glob
import subprocess, binascii
import time, os, ConfigParser

from PIL import Image,ImageChops,ImageOps,ImageDraw
import pygame.image
import pygame.camera




class Shapextractor(object):

    def __init__(self):

        # will create empty list if unavailable
        # limited to my setup -- can be more generalized
        self.serialports =  glob.glob('/dev/ttyUSB*')        
        self.videodevices = glob.glob('/dev/video*')   



    def establish_serial(self):
        # tune it up better in the future for flexibility
        # and error handling
        self.ser = serial.Serial(self.serialports[0], 9600, timeout=1)
        return self.ser

    def init_camera(self):
        # generalize and improve
        pygame.camera.init()
        self.cam = pygame.camera.Camera(pygame.camera.list_cameras()[0],(self.RESW,self.RESH))
        self.cam.start()



    # Takes Photos and Processes them 
    # ====================================================================================
    def cheese(self, z):

        i = 0 
        while (i < (self.RESW*self.RESH*65/100) or i > (self.RESW*self.RESH*95/100) ):

            im1 = self.cam.get_image()
            time.sleep(0.055)
     
            self.ser.write('I')         # turns laser on
            time.sleep(0.1)
            im2 = self.cam.get_image()
            time.sleep(0.055)

            self.ser.write('O')        # turns laser off  
            time.sleep(0.055)

            pygame.image.save(im1, "b%08d.jpg" % z)
            pygame.image.save(im2, "a%08d.jpg" % z)
            im2 = Image.open("b%08d.jpg" % z).rotate(self.ROT)
            im1 = Image.open("a%08d.jpg" % z).rotate(self.ROT)

            # cropping the top off images
            draw = ImageDraw.Draw(im2)
            draw.rectangle([0,0, self.RESW, self.CROPH], fill=0)
            draw = ImageDraw.Draw(im1)
            draw.rectangle([0,0, self.RESW, self.CROPH], fill=0)
            draw.line( (int(self.RESW/2), 0,int(self.RESW/2),self.CROPH), fill=255 )

            # extracting the difference between images
            diff = ImageChops.difference(im2, im1)
            diff = ImageOps.grayscale(diff)
            diff = ImageOps.posterize(diff, 6)
            v = diff.getcolors()
            i = v[0][0]
            print i

            im1.save("b%08d.jpg" % z, quality = 90)
            im1 = Image.new("RGB", (self.RESW,self.RESH))
            im1.paste(diff)
            im1.save("%08d.jpg" % z, quality = 90)
            im2.save("a%08d.jpg" % z, quality = 90)



    def read_configs(self):

        config = ConfigParser.ConfigParser()
        config.read('Shapextractor.ini')


        self.CROPH = int(config.get('PYTHON', 'CROPH'))  # pixels to remove from top of img (needed for a clean image final output)
        self.QUALITY = int(config.get('PYTHON', 'QUALITY'))  #(0 to 2) 0=512photo  1=2014    2=4028
        self.RESW = int(config.get('PYTHON', 'RESW'))
        self.RESH = int(config.get('PYTHON', 'RESH'))
        self.ROT = int(config.get('PYTHON', 'ROT'))

        self.CAMERA_HFOV = float(config.get('C++', 'CAMERA_HFOV'))
        self.CAMERA_DISTANCE = float(config.get('C++', 'CAMERA_DISTANCE'))
        self.LASER_OFFSET = float(config.get('C++', 'LASER_OFFSET')) 
        self.HORIZ_AVG = int(config.get('C++', 'HORIZ_AVG'))
        self.VERT_AVG = int(config.get('C++', 'VERT_AVG'))
        self.FRAME_SKIP = int(config.get('C++', 'FRAME_SKIP'))
        self.POINT_SKIP = int(config.get('C++', 'POINT_SKIP'))





