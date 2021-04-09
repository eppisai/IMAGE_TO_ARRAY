#ifndef $ICON_TEMPLATE_H

#define $ICON_TEMPLATE_H

#include "../../UI/Widgets/Icon2bit.h"

const Icon2bit $ICON_NAME = {$WIDTH, $HEIGHT, ImageDataFormat::Indexed2Bit, {RGB565(255,255,255), RGB565(128,128,128), RGB565(64,64,64), RGB565(0,0,0)}, (const uint8_t[]){$IMAGE_DATA}};

#endif // $ICON_TEMPLATE_H
