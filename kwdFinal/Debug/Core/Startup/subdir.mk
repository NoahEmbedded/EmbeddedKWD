################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
S_SRCS += \
../Core/Startup/startup_stm32f769nihx.s 

OBJS += \
./Core/Startup/startup_stm32f769nihx.o 


# Each subdirectory must supply rules for building sources it contributes
Core/Startup/%.o: ../Core/Startup/%.s
	arm-none-eabi-gcc -mcpu=cortex-m7 -g3 -c -I"/home/noah/STM32CubeIDE/workspace_1.0.2/kwdFinal/Drivers/CMSIS/DSP/Source/TransformFunctions" -I"/home/noah/STM32CubeIDE/workspace_1.0.2/kwdFinal/Drivers/CMSIS/DSP/CommonTables" -x assembler-with-cpp --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@" "$<"

