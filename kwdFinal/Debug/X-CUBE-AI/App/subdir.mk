################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../X-CUBE-AI/App/app_x-cube-ai.c \
../X-CUBE-AI/App/kwdnetz.c \
../X-CUBE-AI/App/kwdnetz_data.c 

OBJS += \
./X-CUBE-AI/App/app_x-cube-ai.o \
./X-CUBE-AI/App/kwdnetz.o \
./X-CUBE-AI/App/kwdnetz_data.o 

C_DEPS += \
./X-CUBE-AI/App/app_x-cube-ai.d \
./X-CUBE-AI/App/kwdnetz.d \
./X-CUBE-AI/App/kwdnetz_data.d 


# Each subdirectory must supply rules for building sources it contributes
X-CUBE-AI/App/app_x-cube-ai.o: ../X-CUBE-AI/App/app_x-cube-ai.c
	arm-none-eabi-gcc "$<" -mcpu=cortex-m7 -std=gnu11 -g3 -DUSE_HAL_DRIVER -DSTM32F769xx -DARM_MATH_CM7 -DDEBUG '-D__FPU_PRESENT=1' -c -I../Drivers/CMSIS/Include -I../Drivers/CMSIS/DSP/Include -I"/home/noah/STM32CubeIDE/workspace_1.0.2/kwdFinal/Drivers/paket" -I../Drivers/CMSIS/Device/ST/STM32F7xx/Include -I../Core/Inc -I../Middlewares/ST/AI/Inc -I../X-CUBE-AI -I../Drivers/STM32F7xx_HAL_Driver/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc/Legacy -I../X-CUBE-AI/App -I"/home/noah/STM32CubeIDE/workspace_1.0.2/kwdFinal/Drivers/CMSIS/DSP/Source/TransformFunctions" -I"/home/noah/STM32CubeIDE/workspace_1.0.2/kwdFinal/Drivers/CMSIS/DSP/CommonTables" -O0 -ffunction-sections -fdata-sections -Wall -lm -fstack-usage -MMD -MP -MF"X-CUBE-AI/App/app_x-cube-ai.d" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"
X-CUBE-AI/App/kwdnetz.o: ../X-CUBE-AI/App/kwdnetz.c
	arm-none-eabi-gcc "$<" -mcpu=cortex-m7 -std=gnu11 -g3 -DUSE_HAL_DRIVER -DSTM32F769xx -DARM_MATH_CM7 -DDEBUG '-D__FPU_PRESENT=1' -c -I../Drivers/CMSIS/Include -I../Drivers/CMSIS/DSP/Include -I"/home/noah/STM32CubeIDE/workspace_1.0.2/kwdFinal/Drivers/paket" -I../Drivers/CMSIS/Device/ST/STM32F7xx/Include -I../Core/Inc -I../Middlewares/ST/AI/Inc -I../X-CUBE-AI -I../Drivers/STM32F7xx_HAL_Driver/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc/Legacy -I../X-CUBE-AI/App -I"/home/noah/STM32CubeIDE/workspace_1.0.2/kwdFinal/Drivers/CMSIS/DSP/Source/TransformFunctions" -I"/home/noah/STM32CubeIDE/workspace_1.0.2/kwdFinal/Drivers/CMSIS/DSP/CommonTables" -O0 -ffunction-sections -fdata-sections -Wall -lm -fstack-usage -MMD -MP -MF"X-CUBE-AI/App/kwdnetz.d" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"
X-CUBE-AI/App/kwdnetz_data.o: ../X-CUBE-AI/App/kwdnetz_data.c
	arm-none-eabi-gcc "$<" -mcpu=cortex-m7 -std=gnu11 -g3 -DUSE_HAL_DRIVER -DSTM32F769xx -DARM_MATH_CM7 -DDEBUG '-D__FPU_PRESENT=1' -c -I../Drivers/CMSIS/Include -I../Drivers/CMSIS/DSP/Include -I"/home/noah/STM32CubeIDE/workspace_1.0.2/kwdFinal/Drivers/paket" -I../Drivers/CMSIS/Device/ST/STM32F7xx/Include -I../Core/Inc -I../Middlewares/ST/AI/Inc -I../X-CUBE-AI -I../Drivers/STM32F7xx_HAL_Driver/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc/Legacy -I../X-CUBE-AI/App -I"/home/noah/STM32CubeIDE/workspace_1.0.2/kwdFinal/Drivers/CMSIS/DSP/Source/TransformFunctions" -I"/home/noah/STM32CubeIDE/workspace_1.0.2/kwdFinal/Drivers/CMSIS/DSP/CommonTables" -O0 -ffunction-sections -fdata-sections -Wall -lm -fstack-usage -MMD -MP -MF"X-CUBE-AI/App/kwdnetz_data.d" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"

