#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd1in54g_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd1in54g_V2 Demo")

    epd = epd1in54g_V2.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()
    font12 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12)
    font16 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 16)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)

    # read bmp file 
    logging.info("2.read bmp file")
    epd.init_Fast()
    Himage = Image.open(os.path.join(picdir, '1in54g.bmp'))
    epd.display(epd.getbuffer(Himage))
    time.sleep(3)

    # Drawing on the image
    epd.init()
    logging.info("1.Drawing on the image...")
    Himage = Image.new('RGB', (epd.height, epd.width), epd.WHITE)
    draw = ImageDraw.Draw(Himage)
    draw.point((10, 80), fill = epd.RED)
    draw.point((10, 90), fill = epd.YELLOW)
    draw.point((10, 100), fill = epd.BLACK)
    draw.line([(20, 70),(70, 120)], fill = epd.RED, width = 1)
    draw.line([(70, 70),(20, 120)], fill = epd.RED, width = 1)
    draw.rectangle([(20, 70),(70, 120)], outline = epd.YELLOW)
    draw.rectangle([(80, 70),(130, 120)], fill = epd.YELLOW)
    draw.ellipse((25, 75, 65, 115), outline = epd.BLACK)
    draw.ellipse((85, 75, 125, 115), fill = epd.BLACK)
    draw.line([(85, 95),(125, 95)], fill = epd.RED, width = 1)
    draw.line([(105, 75),(105, 115)], fill = epd.YELLOW, width = 1)
    draw.text((10, 0), 'Red,yellow,', font = font16, fill = epd.RED)
    draw.text((10, 20), 'white and black', font = font16, fill = epd.RED)
    draw.text((10, 40), 'Four color e-Paper', font = font12, fill = epd.YELLOW)
    draw.text((10, 150), u'微雪电子', font = font24, fill = epd.RED)
    draw.text((10, 135), '123456', font = font12, fill = epd.RED)
    epd.display(epd.getbuffer(Himage))
    time.sleep(3)

    logging.info("Clear...")
    epd.init()
    epd.Clear()

    logging.info("Goto Sleep...")
    epd.sleep()

    logging.info("close 5V, Module enters 0 power consumption ...")
    epd.EPD_END()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd1in54g_V2.epdconfig.module_exit(cleanup=True)
    exit()
