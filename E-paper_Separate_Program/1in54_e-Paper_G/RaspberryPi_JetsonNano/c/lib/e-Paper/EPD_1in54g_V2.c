/*****************************************************************************
* | File        :   EPD_1in54g_V2.cpp
* | Author      :   Waveshare team / V2 port
* | Function    :   1inch54 e-paper (G) V2 parameters
* | Info        :
*----------------
* | This version:   V2.0
* | Info        :   Keep the original ESP32 interface and image buffer format.
* -----------------------------------------------------------------------------
******************************************************************************/
#include "EPD_1in54g.h"
#include "Debug.h"
#include "time.h"

/******************************************************************************
function :  Software reset
parameter:
******************************************************************************/
static void EPD_1IN54G_V2_Reset(void)
{
    DEV_Delay_ms(100);
    DEV_Digital_Write(EPD_RST_PIN, 0);
    DEV_Delay_ms(50);
    DEV_Digital_Write(EPD_RST_PIN, 1);
    DEV_Delay_ms(50);
}

static void EPD_1IN54G_V2_Fast_Reset(void)
{
    DEV_Delay_ms(20);
    DEV_Digital_Write(EPD_RST_PIN, 0);
    DEV_Delay_ms(50);
    DEV_Digital_Write(EPD_RST_PIN, 1);
    DEV_Delay_ms(50);
}


/******************************************************************************
function :  send command
parameter:
     Reg : Command register
******************************************************************************/
static void EPD_1IN54G_V2_SendCommand(UBYTE Reg)
{
    DEV_Digital_Write(EPD_DC_PIN, 0);
    DEV_Digital_Write(EPD_CS_PIN, 0);
    DEV_SPI_WriteByte(Reg);
    DEV_Digital_Write(EPD_CS_PIN, 1);
}

/******************************************************************************
function :  send data
parameter:
    Data : Write data
******************************************************************************/
static void EPD_1IN54G_V2_SendData(UBYTE Data)
{
    DEV_Digital_Write(EPD_DC_PIN, 1);
    DEV_Digital_Write(EPD_CS_PIN, 0);
    DEV_SPI_WriteByte(Data);
    DEV_Digital_Write(EPD_CS_PIN, 1);
}

/******************************************************************************
function :  Wait until the busy_pin goes HIGH
parameter:
******************************************************************************/
void EPD_1IN54G_V2_ReadBusyH(void)
{
    Debug("e-Paper busy H\r\n");
    while(!DEV_Digital_Read(EPD_BUSY_PIN)) {      // HIGH: idle
        DEV_Delay_ms(5);
    }
    Debug("e-Paper busy H release\r\n");
}

/******************************************************************************
function :  Turn On Display
parameter:
******************************************************************************/
static void EPD_1IN54G_V2_TurnOnDisplay(void)
{
    EPD_1IN54G_V2_SendCommand(0x12); // DISPLAY_REFRESH
    EPD_1IN54G_V2_SendData(0x00);
    EPD_1IN54G_V2_ReadBusyH();
}

/******************************************************************************
function :  Initialize the e-Paper register
parameter:
******************************************************************************/
void EPD_1IN54G_V2_Init(void)
{
    EPD_1IN54G_V2_Reset();

    EPD_1IN54G_V2_SendCommand(0xE9);
    EPD_1IN54G_V2_SendData(0x01);

    EPD_1IN54G_V2_SendCommand(0x04);
    EPD_1IN54G_V2_ReadBusyH();
}

void EPD_1IN54G_V2_Init_Fast(void)
{
    EPD_1IN54G_V2_Fast_Reset();
    
    EPD_1IN54G_V2_SendCommand(0xE9);
    EPD_1IN54G_V2_SendData(0x01);

    EPD_1IN54G_V2_SendCommand(0xEF);
    EPD_1IN54G_V2_SendData(0x01);

    EPD_1IN54G_V2_SendCommand(0xF6);
    EPD_1IN54G_V2_SendData(0x24);

    EPD_1IN54G_V2_SendCommand(0xEF);
    EPD_1IN54G_V2_SendData(0x00);

    EPD_1IN54G_V2_SendCommand(0xE0);
    EPD_1IN54G_V2_SendData(0x02);

    EPD_1IN54G_V2_SendCommand(0xE6);
    EPD_1IN54G_V2_SendData(92);

    EPD_1IN54G_V2_SendCommand(0xA5);
    EPD_1IN54G_V2_ReadBusyH();

    EPD_1IN54G_V2_SendCommand(0x04);
    EPD_1IN54G_V2_ReadBusyH();
}

/******************************************************************************
function :  Clear screen
parameter:
******************************************************************************/
void EPD_1IN54G_V2_Clear(UBYTE color)
{
    UWORD Width, Height;
    Width = (EPD_1IN54G_WIDTH % 4 == 0)? (EPD_1IN54G_WIDTH / 4 ): (EPD_1IN54G_WIDTH / 4 + 1);
    Height = EPD_1IN54G_HEIGHT;

    EPD_1IN54G_V2_SendCommand(0x10);
    for (UWORD j = 0; j < Height; j++) {
        for (UWORD i = 0; i < Width; i++) {
            EPD_1IN54G_V2_SendData((color << 6) | (color << 4) | (color << 2) | color);
        }
    }

    EPD_1IN54G_V2_TurnOnDisplay();
}

/******************************************************************************
function :  Sends the image buffer in RAM to e-Paper and displays
parameter:
******************************************************************************/
void EPD_1IN54G_V2_Display(const UBYTE *Image)
{
    UWORD Width, Height;
    Width = (EPD_1IN54G_WIDTH % 4 == 0)? (EPD_1IN54G_WIDTH / 4 ): (EPD_1IN54G_WIDTH / 4 + 1);
    Height = EPD_1IN54G_HEIGHT;

    EPD_1IN54G_V2_SendCommand(0x10);
    for (UWORD j = 0; j < Height; j++) {
        for (UWORD i = 0; i < Width; i++) {
            EPD_1IN54G_V2_SendData(Image[i + j * Width]);
        }
    }

    EPD_1IN54G_V2_TurnOnDisplay();
}

/******************************************************************************
function :  Enter sleep mode
parameter:
******************************************************************************/
void EPD_1IN54G_V2_Sleep(void)
{
    EPD_1IN54G_V2_SendCommand(0x02); // POWER_OFF
    EPD_1IN54G_V2_SendData(0x00);
    EPD_1IN54G_V2_ReadBusyH();
    EPD_1IN54G_V2_SendCommand(0x07); // DEEP_SLEEP
    EPD_1IN54G_V2_SendData(0xA5);
}
