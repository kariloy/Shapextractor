#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import sys, os
import Shapelib as spx
import pygame.image
import pygame.camera
import subprocess, binascii


X = spx.Shapextractor()


ser = X.establish_serial()




try:
   with open('/dev/video0'): pass 
except IOError:
   print 'Check your webcam'
   sys.exit()
 
print 'Shapextractor 2.0alpha'
print 'Initializing system ...' 


X.read_configs()

# ==========================================================================

print 'Starting camera...'

X.init_camera()

#pygame.camera.init()
#cam = pygame.camera.Camera(pygame.camera.list_cameras()[0],(X.RESW,X.RESH))
#cam.start()


if X.ROT==90 :
    z = X.RESW
    X.RESW = X.RESH
    X.RESH = z
subprocess.call("v4l2-ctl --set-ctrl white_balance_automatic=0" ,shell=True)
subprocess.call("v4l2-ctl --set-ctrl sharpness=63" ,shell=True)



# STEP'n'CHEESE
# ===========================================================================
print 'Starting scan...'
z=0

#for x in range(0,2048):

#    print 'Full step N-' , x

#    X.cheese(z)
#    if z==1 :
#        cheese(z)
#    z+=1  

#    if X.QUALITY == 0:
#        if x%4 == 0:
#            X.cheese(z)
#            z += 1
#    if X.QUALITY == 1:
#        if x%2 == 0:
#            X.cheese(z)
#            z +=1
#    if X.QUALITY == 2:
#        X.cheese(z)
#        z += 1

#    ser.write('S')

for x in range(0,512):
    print 'Full step N-' , x

    X.cheese(z)
    if z==0 :
        X.cheese(z)
    z=z+1

    ser.write('S')

    if X.QUALITY >>1 :
        X.cheese(z)
        z=z+1
    ser.write('S')

 #stepper(SEQB,PINS)
    if X.QUALITY >>0 :
        X.cheese(z)
        z=z+1
    ser.write('S')

 #stepper(SEQC,PINS)
    if X.QUALITY >>1 :
        cheese(z)
        z=z+1
    ser.write('S')

# CLOSE resources and prepare folder project
# ==================================================
print 'Cleaning up system...'

ser.write('O')
#ser.write('D')
ser.close()
pygame.camera.quit()


pkey = binascii.b2a_hex(os.urandom(4))
subprocess.call("mkdir ./models/%s" % pkey, shell=True)
subprocess.call("mkdir ./models/%s/jpg" % pkey, shell=True)


# Shapextractor 
# =============================================================================================
print 'starting extractor...'
subprocess.call("./Shapextractor %s %s %s %s %s %s %s %s >./models/%s/%s.ply" %(X.CAMERA_HFOV,X.CAMERA_DISTANCE,X.LASER_OFFSET,X.HORIZ_AVG,X.VERT_AVG,X.FRAME_SKIP,X.POINT_SKIP,X.ROT,pkey,pkey) ,shell=True)

print 'Cleaning up temp directory....'

#clean workbench add project in web site
subprocess.call("mv *.jpg ./models/%s/jpg/" % pkey, shell=True)



#with open("index.htm", "a") as myfile:
# myfile.write('<A href="./PLY Viewer.htm?file=./models/%s/%s.ply">View </a>&nbsp;&nbsp;&nbsp; <A href="./models/%s/%s.ply">Download </a> &nbsp;&nbsp; <img src="./models/%s/jpg/a00000000.jpg"></img>  <br><br>\n' % (pkey,pkey,pkey,pkey,pkey))


#subprocess.call("chmod 777 -R ./" , shell=True)

print 'Shapextractor done....'


