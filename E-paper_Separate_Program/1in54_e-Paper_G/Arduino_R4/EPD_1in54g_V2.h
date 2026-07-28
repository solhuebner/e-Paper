/*****************************************************************************
* | File        :   EPD_1in54g_V2.h
* | Author      :   Waveshare team / V2 port
* | Function    :   1inch54 e-paper (G) V2
* | Info        :
*----------------
* | This version:   V2.0
* | Info        :   Keep the original ESP32 interface and image buffer format.
* -----------------------------------------------------------------------------
******************************************************************************/
#ifndef __EPD_1IN54G_V2_H_
#define __EPD_1IN54G_V2_H_

#include "DEV_Config.h"

// Display resolution
#define EPD_1IN54G_V2_WIDTH       200
#define EPD_1IN54G_V2_HEIGHT      200

// Color
#define EPD_1IN54G_V2_BLACK       0x0
#define EPD_1IN54G_V2_WHITE       0x1
#define EPD_1IN54G_V2_YELLOW      0x2
#define EPD_1IN54G_V2_RED         0x3

void EPD_1IN54G_V2_Init(void);
void EPD_1IN54G_V2_Init_Fast(void);
void EPD_1IN54G_V2_Clear(UBYTE color);
void EPD_1IN54G_V2_Display(const UBYTE *Image);
void EPD_1IN54G_V2_Sleep(void);

#endif
