#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in9_V3
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd2in9 V2 Demo") 
    epd = epd2in9_V3.EPD()

    logging.info("init and Clear")
    epd.init_Fast()
    epd.Clear(0xFF)
    time.sleep(2)
    
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)
    
    logging.info("1.read bmp file")
    Himage = Image.open(os.path.join(picdir, '2in9.bmp'))
    epd.display_Fast(epd.getbuffer(Himage))
    time.sleep(2)
    
    logging.info("2.read bmp file on window,Quick brush demo")
    Himage2 = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    bmp = Image.open(os.path.join(picdir, '100x100.bmp'))
    Himage2.paste(bmp, (50,10))
    epd.display_Fast(epd.getbuffer(Himage2))
    time.sleep(2)
    
    # Drawing on the Horizontal image
    logging.info("3.Drawing on the Horizontal image...")
    epd.init()
    Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)
    draw.text((10, 0), 'hello world', font = font24, fill = 0)
    draw.text((10, 20), '2.9inch e-Paper', font = font24, fill = 0)
    draw.text((150, 0), u'微雪电子', font = font24, fill = 0)    
    draw.line((20, 50, 70, 100), fill = 0)
    draw.line((70, 50, 20, 100), fill = 0)
    draw.rectangle((20, 50, 70, 100), outline = 0)
    draw.line((165, 50, 165, 100), fill = 0)
    draw.line((140, 75, 190, 75), fill = 0)
    draw.arc((140, 50, 190, 100), 0, 360, fill = 0)
    draw.rectangle((80, 50, 130, 100), fill = 0)
    draw.chord((200, 50, 250, 100), 0, 360, fill = 0)
    # Himage = Himage.transpose(method=Image.ROTATE_180)
    epd.display_Base(epd.getbuffer(Himage))
    time.sleep(2)

    # partial update
    logging.info("show time")
    num = 0
    while (True):
        draw.rectangle((10, 105, 105, 127), fill = 255)
        draw.text((10, 105), time.strftime('%H:%M:%S'), font = font24, fill = 0)
        epd.display_Partial(epd.getbuffer(Himage))
        
        num = num + 1
        if(num == 10):
            break
    time.sleep(2)

    '''4Gray display'''
    logging.info("4Gray display--------------------------------")
    epd.Init_4Gray()
    
    Limage = Image.new('L', (epd.height, epd.width), 0xff)  # 255: clear the frame
    draw = ImageDraw.Draw(Limage)
    draw.text((0, 0), u'微雪电子', font = font35, fill = epd.GRAY4)
    draw.text((0, 35), u'微雪电子', font = font35, fill = epd.GRAY3)
    draw.text((0, 70), u'微雪电子', font = font35, fill = epd.GRAY2)
    draw.text((20, 105), 'hello world', font = font18, fill = epd.GRAY4)
    draw.line((160, 10, 210, 60), fill = epd.GRAY4)
    draw.line((160, 60, 210, 10), fill = epd.GRAY4)
    draw.rectangle((160, 10, 210, 60), outline = epd.GRAY4)
    draw.line((160, 95, 210, 95), fill = epd.GRAY4)
    draw.line((185, 70, 185, 120), fill = epd.GRAY4)
    draw.arc((160, 70, 210, 120), 0, 360, fill = epd.GRAY4)
    draw.rectangle((220, 10, 270, 60), fill = epd.GRAY4)
    draw.chord((220, 70, 270, 120), 0, 360, fill = epd.GRAY4)
    # Limage = Limage.transpose(method=Image.ROTATE_180)
    epd.display_4Gray(epd.getbuffer_4Gray(Limage))
    time.sleep(2)
    
    #display 4Gra bmp
    Himage = Image.open(os.path.join(picdir, '2in9_Scale.bmp'))
    epd.display_4Gray(epd.getbuffer_4Gray(Himage))
    time.sleep(2)
            
    logging.info("Clear...")
    epd.init()
    epd.Clear(0xFF)
    
    logging.info("Goto Sleep...")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in9_V3.epdconfig.module_exit(cleanup=True)
    exit()
