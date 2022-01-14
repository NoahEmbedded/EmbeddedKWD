################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Drivers/CMSIS/DSP/CommonTables/arm_common_tables.c \
../Drivers/CMSIS/DSP/CommonTables/arm_const_structs.c 

OBJS += \
./Drivers/CMSIS/DSP/CommonTables/arm_common_tables.o \
./Drivers/CMSIS/DSP/CommonTables/arm_const_structs.o 

C_DEPS += \
./Drivers/CMSIS/DSP/CommonTables/arm_common_tables.d \
./Drivers/CMSIS/DSP/CommonTables/arm_const_structs.d 


# Each subdirectory must supply rules for building sources it contributes
Drivers/CMSIS/DSP/CommonTables/arm_common_tables.o: ../Drivers/CMSIS/DSP/CommonTables/arm_common_tables.c
	arm-none-eabi-gcc "$<" -mcpu=cortex-m7 -std=gnu11 -g3 -DUSE_HAL_DRIVER -DSTM32F769xx -DARM_MATH_CM7 -DDEBUG '-D__FPU_PRESENT=1' -c -I../Drivers/CMSIS/Include -I../Drivers/CMSIS/DSP/Include -I"/home/noah/STM32CubeIDE/workspace_1.0.2/kwdFinal/Drivers/paket" -I../Drivers/CMSIS/Device/ST/STM32F7xx/Include -I../Core/Inc -I../Middlewares/ST/AI/Inc -I../X-CUBE-AI -I../Drivers/STM32F7xx_HAL_Driver/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc/Legacy -I../X-CUBE-AI/App -I"/home/noah/STM32CubeIDE/workspace_1.0.2/kwdFinal/Drivers/CMSIS/DSP/Source/TransformFunctions" -I"/home/noah/STM32CubeIDE/workspace_1.0.2/kwdFinal/Drivers/CMSIS/DSP/CommonTables" -O0 -ffunction-sections -fdata-sections -Wall -lm -fstack-usage -MMD -MP -MF"Drivers/CMSIS/DSP/CommonTables/arm_common_tables.d" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"
Drivers/CMSIS/DSP/CommonTables/arm_const_structs.o: ../Drivers/CMSIS/DSP/CommonTables/arm_const_structs.c
	arm-none-eabi-gcc "$<" -mcpu=cortex-m7 -std=gnu11 -g3 -DUSE_HAL_DRIVER -DSTM32F769xx -DARM_MATH_CM7 -DDEBUG '-D__FPU_PRESENT=1' -c -I../Drivers/CMSIS/Include -I../Drivers/CMSIS/DSP/Include -I"/home/noah/STM32CubeIDE/workspace_1.0.2/kwdFinal/Drivers/paket" -I../Drivers/CMSIS/Device/ST/STM32F7xx/Include -I../Core/Inc -I../Middlewares/ST/AI/Inc -I../X-CUBE-AI -I../Drivers/STM32F7xx_HAL_Driver/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc/Legacy -I../X-CUBE-AI/App -I"/home/noah/STM32CubeIDE/workspace_1.0.2/kwdFinal/Drivers/CMSIS/DSP/Source/TransformFunctions" -I"/home/noah/STM32CubeIDE/workspace_1.0.2/kwdFinal/Drivers/CMSIS/DSP/CommonTables" -O0 -ffunction-sections -fdata-sections -Wall -lm -fstack-usage -MMD -MP -MF"Drivers/CMSIS/DSP/CommonTables/arm_const_structs.d" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"

