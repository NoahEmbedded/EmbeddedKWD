################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Drivers/paket/stm32f769i_discovery.c \
../Drivers/paket/stm32f769i_discovery_audio.c \
../Drivers/paket/stm32f769i_discovery_sdram.c \
../Drivers/paket/wm8994.c 

OBJS += \
./Drivers/paket/stm32f769i_discovery.o \
./Drivers/paket/stm32f769i_discovery_audio.o \
./Drivers/paket/stm32f769i_discovery_sdram.o \
./Drivers/paket/wm8994.o 

C_DEPS += \
./Drivers/paket/stm32f769i_discovery.d \
./Drivers/paket/stm32f769i_discovery_audio.d \
./Drivers/paket/stm32f769i_discovery_sdram.d \
./Drivers/paket/wm8994.d 


# Each subdirectory must supply rules for building sources it contributes
Drivers/paket/stm32f769i_discovery.o: ../Drivers/paket/stm32f769i_discovery.c
	arm-none-eabi-gcc "$<" -mcpu=cortex-m7 -std=gnu11 -g3 -DUSE_HAL_DRIVER -DSTM32F769xx -DARM_MATH_CM7 -DDEBUG '-D__FPU_PRESENT=1' -c -I../Drivers/CMSIS/Include -I../Drivers/CMSIS/DSP/Include -I"/home/noah/STM32CubeIDE/workspace_1.0.2/kwdFinal/Drivers/paket" -I../Drivers/CMSIS/Device/ST/STM32F7xx/Include -I../Core/Inc -I../Middlewares/ST/AI/Inc -I../X-CUBE-AI -I../Drivers/STM32F7xx_HAL_Driver/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc/Legacy -I../X-CUBE-AI/App -I"/home/noah/STM32CubeIDE/workspace_1.0.2/kwdFinal/Drivers/CMSIS/DSP/Source/TransformFunctions" -I"/home/noah/STM32CubeIDE/workspace_1.0.2/kwdFinal/Drivers/CMSIS/DSP/CommonTables" -O0 -ffunction-sections -fdata-sections -Wall -lm -fstack-usage -MMD -MP -MF"Drivers/paket/stm32f769i_discovery.d" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"
Drivers/paket/stm32f769i_discovery_audio.o: ../Drivers/paket/stm32f769i_discovery_audio.c
	arm-none-eabi-gcc "$<" -mcpu=cortex-m7 -std=gnu11 -g3 -DUSE_HAL_DRIVER -DSTM32F769xx -DARM_MATH_CM7 -DDEBUG '-D__FPU_PRESENT=1' -c -I../Drivers/CMSIS/Include -I../Drivers/CMSIS/DSP/Include -I"/home/noah/STM32CubeIDE/workspace_1.0.2/kwdFinal/Drivers/paket" -I../Drivers/CMSIS/Device/ST/STM32F7xx/Include -I../Core/Inc -I../Middlewares/ST/AI/Inc -I../X-CUBE-AI -I../Drivers/STM32F7xx_HAL_Driver/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc/Legacy -I../X-CUBE-AI/App -I"/home/noah/STM32CubeIDE/workspace_1.0.2/kwdFinal/Drivers/CMSIS/DSP/Source/TransformFunctions" -I"/home/noah/STM32CubeIDE/workspace_1.0.2/kwdFinal/Drivers/CMSIS/DSP/CommonTables" -O0 -ffunction-sections -fdata-sections -Wall -lm -fstack-usage -MMD -MP -MF"Drivers/paket/stm32f769i_discovery_audio.d" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"
Drivers/paket/stm32f769i_discovery_sdram.o: ../Drivers/paket/stm32f769i_discovery_sdram.c
	arm-none-eabi-gcc "$<" -mcpu=cortex-m7 -std=gnu11 -g3 -DUSE_HAL_DRIVER -DSTM32F769xx -DARM_MATH_CM7 -DDEBUG '-D__FPU_PRESENT=1' -c -I../Drivers/CMSIS/Include -I../Drivers/CMSIS/DSP/Include -I"/home/noah/STM32CubeIDE/workspace_1.0.2/kwdFinal/Drivers/paket" -I../Drivers/CMSIS/Device/ST/STM32F7xx/Include -I../Core/Inc -I../Middlewares/ST/AI/Inc -I../X-CUBE-AI -I../Drivers/STM32F7xx_HAL_Driver/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc/Legacy -I../X-CUBE-AI/App -I"/home/noah/STM32CubeIDE/workspace_1.0.2/kwdFinal/Drivers/CMSIS/DSP/Source/TransformFunctions" -I"/home/noah/STM32CubeIDE/workspace_1.0.2/kwdFinal/Drivers/CMSIS/DSP/CommonTables" -O0 -ffunction-sections -fdata-sections -Wall -lm -fstack-usage -MMD -MP -MF"Drivers/paket/stm32f769i_discovery_sdram.d" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"
Drivers/paket/wm8994.o: ../Drivers/paket/wm8994.c
	arm-none-eabi-gcc "$<" -mcpu=cortex-m7 -std=gnu11 -g3 -DUSE_HAL_DRIVER -DSTM32F769xx -DARM_MATH_CM7 -DDEBUG '-D__FPU_PRESENT=1' -c -I../Drivers/CMSIS/Include -I../Drivers/CMSIS/DSP/Include -I"/home/noah/STM32CubeIDE/workspace_1.0.2/kwdFinal/Drivers/paket" -I../Drivers/CMSIS/Device/ST/STM32F7xx/Include -I../Core/Inc -I../Middlewares/ST/AI/Inc -I../X-CUBE-AI -I../Drivers/STM32F7xx_HAL_Driver/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc/Legacy -I../X-CUBE-AI/App -I"/home/noah/STM32CubeIDE/workspace_1.0.2/kwdFinal/Drivers/CMSIS/DSP/Source/TransformFunctions" -I"/home/noah/STM32CubeIDE/workspace_1.0.2/kwdFinal/Drivers/CMSIS/DSP/CommonTables" -O0 -ffunction-sections -fdata-sections -Wall -lm -fstack-usage -MMD -MP -MF"Drivers/paket/wm8994.d" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"

