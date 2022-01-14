#ifdef __cplusplus
extern "C" {
#endif

#include "main.h"
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                                      Define-Anweisungen                                                                            //
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#define BUFFSIZE 65536//Bei 16kHz Stereoaufnahme entsprechen 000 Sample 2 Sekunden Aufnahme
#define SCRTCHSIZE 16384
#define SLICESIZE 512
#define SPECTROWIDTH 256
#define SPECTROHEIGHT 62
#define OUTPUTSIZE 3
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                                       Funktionsdeklarationen                                                                       //
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_CRC_Init(void);
static void MX_USART1_UART_Init(void);
void hammingInit(float *coefficient_array, int size);
void fenstern(float *koeffizientenArray,uint16_t *input,float *output,int elementAnzahl);
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                                       Datentypendefinitionen                                                                       //
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
enum status {LEER=0,HALB=1,VOLL=2};
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                               	        Globale Variablen	                                                                      //
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
CRC_HandleTypeDef hcrc;
UART_HandleTypeDef huart1;
enum status bufferStatus;
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                               	 	   	    Main			                                                                      //
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
int main(void)
{
	arm_rfft_fast_instance_f32 fftInstanz;
	float hammingKoeffizienten[SLICESIZE];
	int32_t scrBuff[SCRTCHSIZE];
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	//                                                      Initialisierung                                                                               //
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	HAL_Init();//Initialisierung der Hardware Abstraction Layer
	SystemClock_Config();//Initialisierung der Clock
	MX_GPIO_Init();//Initialisierung der GPIO-Ports
	MX_CRC_Init();//Initialisierung der zyklischen Redundanzpruefung
	MX_USART1_UART_Init();//Initialisierung der USART
	MX_X_CUBE_AI_Init();//Initialisierung der Inferenz des neuronalen Netzes
	BSP_PB_Init(BUTTON_USER, BUTTON_MODE_GPIO);//Initialisierung des Eingabeknopfs
	BSP_LED_Init(LED1);//Initialisierung der USER_LED Nummer 1(Rot)
	BSP_LED_Init(LED2);//Initialisierung der USER_LED Nummer 2(Gruen)
	BSP_AUDIO_IN_Init(DEFAULT_AUDIO_IN_FREQ,DEFAULT_AUDIO_IN_BIT_RESOLUTION,DEFAULT_AUDIO_IN_CHANNEL_NBR);//Initialisierung der Mikrofonaufnahme
	BSP_AUDIO_IN_AllocScratch(scrBuff,SCRTCHSIZE);//Initialisierung des Scratchbuffers der DFSDM-Schnittstelle
	BSP_AUDIO_OUT_Init(OUTPUT_DEVICE_HEADPHONE1,60,DEFAULT_AUDIO_IN_FREQ);//Initialisierung der Audioausgabe
	BSP_SDRAM_Init();
	hammingInit(hammingKoeffizienten,SLICESIZE);//Initialisierung der Hammingfensterkoeffizienten
	arm_rfft_fast_init_f32(&fftInstanz,SLICESIZE);//Initialisierung der float32-rfft
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	//                                                       Programmablauf                                                                               //
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

	int gedrueckt = 0;
	bufferStatus = LEER;
    int16_t *dataIn = (int16_t*)(SDRAM_DEVICE_ADDR);
    int16_t *dataOut = (int16_t*)(SDRAM_DEVICE_ADDR+BUFFSIZE);
//	int16_t dataIn[BUFFSIZE];
//	int16_t dataOut[BUFFSIZE];
	while (1)
	{
		//0->Knopf nicht gedrueckt, 1-> Knopf gedrueckt
		gedrueckt = BSP_PB_GetState(BUTTON_USER);
		if(gedrueckt)
		{
			//Aufnahme
			BSP_LED_On(LED1);
			uint8_t text[50]="Starte Aufnahme\n\r";
			HAL_UART_Transmit(&huart1,text,sizeof(text),100);
			//Die Aufnahme ist ein Stereosignal, der Signalaufbau ist(fuer links=l,rechts=r):l1-r1-l2-r2-l3-r3-....
			memset(dataIn,0,sizeof(dataIn));
			BSP_AUDIO_IN_Record(&dataIn[0],BUFFSIZE*sizeof(uint16_t));
			while(bufferStatus!=VOLL)
			{
				//Wenn die erste Haelfte der Daten fertig aufgenommen ist, wird sie in dem Outputbuffer kopiert.
				//Dort kann sie nicht vom zyklischen Schreiben der Aufnahme ueberschrieben werden
				if(bufferStatus==HALB)
				{
					memcpy(&dataOut[0],&dataIn[0],(BUFFSIZE/2)*sizeof(int16_t));
					bufferStatus=LEER;
				}
			}
			BSP_AUDIO_IN_Stop();
			bufferStatus=LEER;

			//Restliche Aufnahmedaten im Outputbbuffer speichern
			memcpy(&dataOut[BUFFSIZE/2],&dataIn[BUFFSIZE/2],(BUFFSIZE/2)*sizeof(int16_t));
			BSP_LED_Off(LED1);
			sprintf(text,"Aufnahme abgeschlossen, starte Verarbeitung\n\r");
			HAL_UART_Transmit(&huart1,text,sizeof(text),100);
			//Verarbeitung
			BSP_LED_On(LED2);
			float spektrogramm [SPECTROHEIGHT*SPECTROWIDTH];
			for(int sliceNummer = 0;sliceNummer<SPECTROHEIGHT;sliceNummer++)
			{
				//Datenrahmen festlegen
				uint16_t datenSlice[SLICESIZE];
				for(int sliceIndex=0;sliceIndex<SLICESIZE;sliceIndex++)
				{
					datenSlice[sliceIndex]=dataOut[(sliceNummer*SLICESIZE)+(sliceIndex*2)];
				}
				//Fenstern
				float gefensterteWerte[SLICESIZE];
				fenstern(hammingKoeffizienten,datenSlice,gefensterteWerte,SLICESIZE);
				//FFT
				float fftWerte[SLICESIZE];
				arm_rfft_fast_f32(&fftInstanz,gefensterteWerte,fftWerte,0);
				//Betrag bilden und skalieren
				float werteSlice[SLICESIZE/2];
				for(int sliceindex = 0;sliceindex<(SLICESIZE);sliceindex+=2)
				{
					float temp = sqrt(fftWerte[sliceindex]*fftWerte[sliceindex]+fftWerte[sliceindex+1]*fftWerte[sliceindex+1]);
					if(temp>65535)
					{
						temp=65535;//Werte groesser 2^16 werden auf den maximalwert von uint16 gesetzt
					}
					werteSlice[sliceindex/2]=(float)((uint16_t)temp>>8);//Skalierung auf Integerwert zwischen 0 und 256
				}
				//Anhaengen
				memcpy(&spektrogramm[sliceNummer*SPECTROWIDTH],werteSlice,sizeof(werteSlice));
			}
			//Auswerten
			AI_ALIGNED(4)
			static ai_i8 aiInput[SPECTROHEIGHT*SPECTROWIDTH];
			memcpy(&aiInput[0],&spektrogramm[0],SPECTROHEIGHT*SPECTROWIDTH*sizeof(float));
			//ai_i8 *aiInput = &spektrogramm[0];
			float aiOutput[OUTPUTSIZE];
			aiRun(aiInput, aiOutput);
			sprintf(text,"Auswertung beendet\n\r");
			HAL_UART_Transmit(&huart1,text,sizeof(text),100);
			sprintf(text,"N:%f,M:%f,S:%f\n\r)",aiOutput[0],aiOutput[1],aiOutput[2]);
			HAL_UART_Transmit(&huart1,text,sizeof(text),100);
			BSP_LED_Off(LED2);
		}
	}
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                                    Funktionsdefinitionen                                                                           //
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void BSP_AUDIO_IN_TransferComplete_CallBack(void)
{
	bufferStatus=VOLL;
}
void BSP_AUDIO_IN_HalfTransfer_CallBack(void)
{
	bufferStatus=HALB;
}
void BSP_AUDIO_IN_Error_CallBack(void)
{
	bufferStatus=LEER;
}


void hammingInit(float *coefficient_array, int size)
{
	for(int i=0;i<size;i++)
	{
		coefficient_array[i]=0.54-0.46*cos((2*M_PI*i)/(size-1));
	}
}

void fenstern(float *koeffizientenArray,uint16_t *input,float *output,int elementAnzahl)
{
	for(int i=0;i<elementAnzahl;i++)
	{
		output[i]=(float)input[i]*koeffizientenArray[i];
	}
}

/**
 * @brief System Clock Configuration
 * @retval None
 */
void SystemClock_Config(void)
{
	RCC_OscInitTypeDef RCC_OscInitStruct = {0};
	RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};
	RCC_PeriphCLKInitTypeDef PeriphClkInitStruct = {0};

	/** Configure the main internal regulator output voltage
	 */
	__HAL_RCC_PWR_CLK_ENABLE();
	__HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE3);
	/** Initializes the CPU, AHB and APB busses clocks
	 */
	RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
	RCC_OscInitStruct.HSIState = RCC_HSI_ON;
	RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
	RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
	RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI;
	RCC_OscInitStruct.PLL.PLLM = 8;
	RCC_OscInitStruct.PLL.PLLN = 192;
	RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV4;
	RCC_OscInitStruct.PLL.PLLQ = 4;
	if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
	{
		Error_Handler();
	}
	/** Initializes the CPU, AHB and APB busses clocks
	 */
	RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
			|RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
	RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
	RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
	RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV4;
	RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV2;

	if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_3) != HAL_OK)
	{
		Error_Handler();
	}
	PeriphClkInitStruct.PeriphClockSelection = RCC_PERIPHCLK_DFSDM1|RCC_PERIPHCLK_USART1
			|RCC_PERIPHCLK_SAI1;
	PeriphClkInitStruct.PLLSAI.PLLSAIN = 192;
	PeriphClkInitStruct.PLLSAI.PLLSAIR = 2;
	PeriphClkInitStruct.PLLSAI.PLLSAIQ = 6;
	PeriphClkInitStruct.PLLSAI.PLLSAIP = RCC_PLLSAIP_DIV2;
	PeriphClkInitStruct.PLLSAIDivQ = 1;
	PeriphClkInitStruct.PLLSAIDivR = RCC_PLLSAIDIVR_2;
	PeriphClkInitStruct.Sai1ClockSelection = RCC_SAI1CLKSOURCE_PLLSAI;
	PeriphClkInitStruct.Usart1ClockSelection = RCC_USART1CLKSOURCE_PCLK2;
	PeriphClkInitStruct.Dfsdm1ClockSelection = RCC_DFSDM1CLKSOURCE_PCLK;
	if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInitStruct) != HAL_OK)
	{
		Error_Handler();
	}
}

/**
 * @brief CRC Initialization Function
 * @param None
 * @retval None
 */
static void MX_CRC_Init(void)
{
	hcrc.Instance = CRC;
	hcrc.Init.DefaultPolynomialUse = DEFAULT_POLYNOMIAL_ENABLE;
	hcrc.Init.DefaultInitValueUse = DEFAULT_INIT_VALUE_ENABLE;
	hcrc.Init.InputDataInversionMode = CRC_INPUTDATA_INVERSION_NONE;
	hcrc.Init.OutputDataInversionMode = CRC_OUTPUTDATA_INVERSION_DISABLE;
	hcrc.InputDataFormat = CRC_INPUTDATA_FORMAT_BYTES;
	if (HAL_CRC_Init(&hcrc) != HAL_OK)
	{
		Error_Handler();
	}
}

/**
 * @brief USART1 Initialization Function
 * @param None
 * @retval None
 */
static void MX_USART1_UART_Init(void)
{
	huart1.Instance = USART1;
	huart1.Init.BaudRate = 9600;
	huart1.Init.WordLength = UART_WORDLENGTH_8B;
	huart1.Init.StopBits = UART_STOPBITS_1;
	huart1.Init.Parity = UART_PARITY_NONE;
	huart1.Init.Mode = UART_MODE_TX_RX;
	huart1.Init.HwFlowCtl = UART_HWCONTROL_NONE;
	huart1.Init.OverSampling = UART_OVERSAMPLING_16;
	huart1.Init.OneBitSampling = UART_ONE_BIT_SAMPLE_DISABLE;
	huart1.AdvancedInit.AdvFeatureInit = UART_ADVFEATURE_NO_INIT;
	if (HAL_UART_Init(&huart1) != HAL_OK)
	{
		Error_Handler();
	}
}

/**
 * @brief GPIO Initialization Function
 * @param None
 * @retval None
 */
static void MX_GPIO_Init(void)
{
	GPIO_InitTypeDef GPIO_InitStruct = {0};

	/* GPIO Ports Clock Enable */
	__HAL_RCC_GPIOE_CLK_ENABLE();
	__HAL_RCC_GPIOG_CLK_ENABLE();
	__HAL_RCC_GPIOB_CLK_ENABLE();
	__HAL_RCC_GPIOD_CLK_ENABLE();
	__HAL_RCC_GPIOC_CLK_ENABLE();
	__HAL_RCC_GPIOA_CLK_ENABLE();
	__HAL_RCC_GPIOJ_CLK_ENABLE();
	__HAL_RCC_GPIOI_CLK_ENABLE();
	__HAL_RCC_GPIOK_CLK_ENABLE();
	__HAL_RCC_GPIOF_CLK_ENABLE();
	__HAL_RCC_GPIOH_CLK_ENABLE();

	/*Configure GPIO pin : QSPI_D2_Pin */
	GPIO_InitStruct.Pin = QSPI_D2_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
	GPIO_InitStruct.Alternate = GPIO_AF9_QUADSPI;
	HAL_GPIO_Init(QSPI_D2_GPIO_Port, &GPIO_InitStruct);

	/*Configure GPIO pins : RMII_TXD1_Pin RMII_TXD0_Pin RMII_TX_EN_Pin */
	GPIO_InitStruct.Pin = RMII_TXD1_Pin|RMII_TXD0_Pin|RMII_TX_EN_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
	GPIO_InitStruct.Alternate = GPIO_AF11_ETH;
	HAL_GPIO_Init(GPIOG, &GPIO_InitStruct);

	/*Configure GPIO pins : FMC_NBL1_Pin FMC_NBL0_Pin FMC_D5_Pin FMC_D6_Pin
                           FMC_D8_Pin FMC_D11_Pin FMC_D4_Pin FMC_D7_Pin 
                           FMC_D9_Pin FMC_D12_Pin FMC_D10_Pin */
	GPIO_InitStruct.Pin = FMC_NBL1_Pin|FMC_NBL0_Pin|FMC_D5_Pin|FMC_D6_Pin
			|FMC_D8_Pin|FMC_D11_Pin|FMC_D4_Pin|FMC_D7_Pin
			|FMC_D9_Pin|FMC_D12_Pin|FMC_D10_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
	GPIO_InitStruct.Alternate = GPIO_AF12_FMC;
	HAL_GPIO_Init(GPIOE, &GPIO_InitStruct);

	/*Configure GPIO pins : ARDUINO_SCL_D15_Pin ARDUINO_SDA_D14_Pin */
	GPIO_InitStruct.Pin = ARDUINO_SCL_D15_Pin|ARDUINO_SDA_D14_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_OD;
	GPIO_InitStruct.Pull = GPIO_PULLUP;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
	GPIO_InitStruct.Alternate = GPIO_AF4_I2C1;
	HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

	/*Configure GPIO pins : ULPI_D7_Pin ULPI_D6_Pin ULPI_D5_Pin ULPI_D3_Pin
                           ULPI_D2_Pin ULPI_D1_Pin ULPI_D4_Pin */
	GPIO_InitStruct.Pin = ULPI_D7_Pin|ULPI_D6_Pin|ULPI_D5_Pin|ULPI_D3_Pin
			|ULPI_D2_Pin|ULPI_D1_Pin|ULPI_D4_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
	GPIO_InitStruct.Alternate = GPIO_AF10_OTG_HS;
	HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

	/*Configure GPIO pins : uSD_D3_Pin uSD_D2_Pin */
	GPIO_InitStruct.Pin = uSD_D3_Pin|uSD_D2_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
	GPIO_InitStruct.Alternate = GPIO_AF10_SDMMC2;
	HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

	/*Configure GPIO pins : uSD_CMD_Pin uSD_CLK_Pin */
	GPIO_InitStruct.Pin = uSD_CMD_Pin|uSD_CLK_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
	GPIO_InitStruct.Alternate = GPIO_AF11_SDMMC2;
	HAL_GPIO_Init(GPIOD, &GPIO_InitStruct);

	/*Configure GPIO pin : WIFI_RX_Pin */
	GPIO_InitStruct.Pin = WIFI_RX_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
	GPIO_InitStruct.Alternate = GPIO_AF8_UART5;
	HAL_GPIO_Init(WIFI_RX_GPIO_Port, &GPIO_InitStruct);

	/*Configure GPIO pin : CEC_Pin */
	GPIO_InitStruct.Pin = CEC_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_OD;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
	GPIO_InitStruct.Alternate = GPIO_AF4_CEC;
	HAL_GPIO_Init(CEC_GPIO_Port, &GPIO_InitStruct);

	/*Configure GPIO pin : AUDIO_SDA_Pin */
	GPIO_InitStruct.Pin = AUDIO_SDA_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_OD;
	GPIO_InitStruct.Pull = GPIO_PULLUP;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
	GPIO_InitStruct.Alternate = GPIO_AF11_I2C4;
	HAL_GPIO_Init(AUDIO_SDA_GPIO_Port, &GPIO_InitStruct);

	/*Configure GPIO pin : QSPI_NCS_Pin */
	GPIO_InitStruct.Pin = QSPI_NCS_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
	GPIO_InitStruct.Alternate = GPIO_AF10_QUADSPI;
	HAL_GPIO_Init(QSPI_NCS_GPIO_Port, &GPIO_InitStruct);

	/*Configure GPIO pins : FMC_SDNCAS_Pin FMC_SDCLK_Pin FMC_A11_Pin FMC_A12_Pin
                           FMC_A10_Pin FMC_BA1_Pin FMC_BA0_Pin */
	GPIO_InitStruct.Pin = FMC_SDNCAS_Pin|FMC_SDCLK_Pin|FMC_A11_Pin|FMC_A12_Pin
			|FMC_A10_Pin|FMC_BA1_Pin|FMC_BA0_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
	GPIO_InitStruct.Alternate = GPIO_AF12_FMC;
	HAL_GPIO_Init(GPIOG, &GPIO_InitStruct);

	/*Configure GPIO pins : LD_USER1_Pin Audio_INT_Pin WIFI_RST_Pin DSI_RESET_Pin
                           ARD_D8_Pin LD_USER2_Pin ARD_D7_Pin ARD_D4_Pin 
                           ARD_D2_Pin */
	GPIO_InitStruct.Pin = LD_USER1_Pin|Audio_INT_Pin|WIFI_RST_Pin|DSI_RESET_Pin
			|ARD_D8_Pin|LD_USER2_Pin|ARD_D7_Pin|ARD_D4_Pin
			|ARD_D2_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	HAL_GPIO_Init(GPIOJ, &GPIO_InitStruct);

	/*Configure GPIO pins : FMC_D2_Pin FMC_D3_Pin FMC_D1_Pin FMC_D15_Pin
                           FMC_D0_Pin FMC_D14_Pin FMC_D13_Pin */
	GPIO_InitStruct.Pin = FMC_D2_Pin|FMC_D3_Pin|FMC_D1_Pin|FMC_D15_Pin
			|FMC_D0_Pin|FMC_D14_Pin|FMC_D13_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
	GPIO_InitStruct.Alternate = GPIO_AF12_FMC;
	HAL_GPIO_Init(GPIOD, &GPIO_InitStruct);

	/*Configure GPIO pins : QSPI_D1_Pin QSPI_D0_Pin */
	GPIO_InitStruct.Pin = QSPI_D1_Pin|QSPI_D0_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
	GPIO_InitStruct.Alternate = GPIO_AF9_QUADSPI;
	HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);

	/*Configure GPIO pin : ARD_D13_SCK_Pin */
	GPIO_InitStruct.Pin = ARD_D13_SCK_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
	GPIO_InitStruct.Alternate = GPIO_AF5_SPI2;
	HAL_GPIO_Init(ARD_D13_SCK_GPIO_Port, &GPIO_InitStruct);

	/*Configure GPIO pins : NC4_Pin NC5_Pin uSD_Detect_Pin LCD_BL_CTRL_Pin */
	GPIO_InitStruct.Pin = NC4_Pin|NC5_Pin|uSD_Detect_Pin|LCD_BL_CTRL_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	HAL_GPIO_Init(GPIOI, &GPIO_InitStruct);

	/*Configure GPIO pins : FMC_NBL2_Pin D27_Pin D26_Pin FMC_NBL3_Pin
                           D29_Pin D31_Pin D28_Pin D25_Pin 
                           D30_Pin D24_Pin */
	GPIO_InitStruct.Pin = FMC_NBL2_Pin|D27_Pin|D26_Pin|FMC_NBL3_Pin
			|D29_Pin|D31_Pin|D28_Pin|D25_Pin
			|D30_Pin|D24_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
	GPIO_InitStruct.Alternate = GPIO_AF12_FMC;
	HAL_GPIO_Init(GPIOI, &GPIO_InitStruct);

	/*Configure GPIO pins : NC3_Pin NC2_Pin NC1_Pin NC8_Pin
                           NC7_Pin */
	GPIO_InitStruct.Pin = NC3_Pin|NC2_Pin|NC1_Pin|NC8_Pin
			|NC7_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	HAL_GPIO_Init(GPIOK, &GPIO_InitStruct);

	/*Configure GPIO pin : SPDIF_RX_Pin */
	GPIO_InitStruct.Pin = SPDIF_RX_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
	GPIO_InitStruct.Alternate = GPIO_AF7_SPDIFRX;
	HAL_GPIO_Init(SPDIF_RX_GPIO_Port, &GPIO_InitStruct);

	/*Configure GPIO pins : uSD_D1_Pin uSD_D0_Pin */
	GPIO_InitStruct.Pin = uSD_D1_Pin|uSD_D0_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
	GPIO_InitStruct.Alternate = GPIO_AF11_SDMMC2;
	HAL_GPIO_Init(GPIOG, &GPIO_InitStruct);

	/*Configure GPIO pins : RMII_RXER_Pin OTG_FS_OverCurrent_Pin */
	GPIO_InitStruct.Pin = RMII_RXER_Pin|OTG_FS_OverCurrent_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	HAL_GPIO_Init(GPIOD, &GPIO_InitStruct);

	/*Configure GPIO pin : SPI2_NSS_Pin */
	GPIO_InitStruct.Pin = SPI2_NSS_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
	GPIO_InitStruct.Alternate = GPIO_AF5_SPI2;
	HAL_GPIO_Init(SPI2_NSS_GPIO_Port, &GPIO_InitStruct);

	/*Configure GPIO pins : FMC_A0_Pin FMC_A1_Pin FMC_A2_Pin FMC_A3_Pin
                           FMC_A4_Pin FMC_A5_Pin FMC_A6_Pin FMC_A9_Pin 
                           FMC_A7_Pin FMC_A8_Pin FMC_SDNRAS_Pin */
	GPIO_InitStruct.Pin = FMC_A0_Pin|FMC_A1_Pin|FMC_A2_Pin|FMC_A3_Pin
			|FMC_A4_Pin|FMC_A5_Pin|FMC_A6_Pin|FMC_A9_Pin
			|FMC_A7_Pin|FMC_A8_Pin|FMC_SDNRAS_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
	GPIO_InitStruct.Alternate = GPIO_AF12_FMC;
	HAL_GPIO_Init(GPIOF, &GPIO_InitStruct);

	/*Configure GPIO pin : WIFI_TX_Pin */
	GPIO_InitStruct.Pin = WIFI_TX_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
	GPIO_InitStruct.Alternate = GPIO_AF8_UART5;
	HAL_GPIO_Init(WIFI_TX_GPIO_Port, &GPIO_InitStruct);

	/*Configure GPIO pins : D23_Pin D21_Pin D22_Pin FMC_SDNME_Pin
                           FMC_SDNE0_Pin FMC_SDCKE0_Pin D20_Pin FMC_D_7_Pin 
                           FMC_D19_Pin FMC_D16_Pin FMC_D18_Pin */
	GPIO_InitStruct.Pin = D23_Pin|D21_Pin|D22_Pin|FMC_SDNME_Pin
			|FMC_SDNE0_Pin|FMC_SDCKE0_Pin|D20_Pin|FMC_D_7_Pin
			|FMC_D19_Pin|FMC_D16_Pin|FMC_D18_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
	GPIO_InitStruct.Alternate = GPIO_AF12_FMC;
	HAL_GPIO_Init(GPIOH, &GPIO_InitStruct);

	/*Configure GPIO pin : ULPI_DIR_Pin */
	GPIO_InitStruct.Pin = ULPI_DIR_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
	GPIO_InitStruct.Alternate = GPIO_AF10_OTG_HS;
	HAL_GPIO_Init(ULPI_DIR_GPIO_Port, &GPIO_InitStruct);

	/*Configure GPIO pin : CEC_CLK_Pin */
	GPIO_InitStruct.Pin = CEC_CLK_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
	GPIO_InitStruct.Alternate = GPIO_AF0_MCO;
	HAL_GPIO_Init(CEC_CLK_GPIO_Port, &GPIO_InitStruct);

	/*Configure GPIO pin : LCD_INT_Pin */
	GPIO_InitStruct.Pin = LCD_INT_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_EVT_RISING;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	HAL_GPIO_Init(LCD_INT_GPIO_Port, &GPIO_InitStruct);

	/*Configure GPIO pin : ARD_D5_PWM_Pin */
	GPIO_InitStruct.Pin = ARD_D5_PWM_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
	GPIO_InitStruct.Alternate = GPIO_AF2_TIM3;
	HAL_GPIO_Init(ARD_D5_PWM_GPIO_Port, &GPIO_InitStruct);

	/*Configure GPIO pins : ARD_D0_RX_Pin ARDUINO_TX_D1_Pin */
	GPIO_InitStruct.Pin = ARD_D0_RX_Pin|ARDUINO_TX_D1_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
	GPIO_InitStruct.Alternate = GPIO_AF8_USART6;
	HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);

	/*Configure GPIO pin : ULPI_NXT_Pin */
	GPIO_InitStruct.Pin = ULPI_NXT_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
	GPIO_InitStruct.Alternate = GPIO_AF10_OTG_HS;
	HAL_GPIO_Init(ULPI_NXT_GPIO_Port, &GPIO_InitStruct);

	/*Configure GPIO pins : EXT_SDA_Pin EXT_SCL_Pin */
	GPIO_InitStruct.Pin = EXT_SDA_Pin|EXT_SCL_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	HAL_GPIO_Init(GPIOG, &GPIO_InitStruct);

	/*Configure GPIO pin : ARD_D6_PWM_Pin */
	GPIO_InitStruct.Pin = ARD_D6_PWM_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
	GPIO_InitStruct.Alternate = GPIO_AF3_TIM11;
	HAL_GPIO_Init(ARD_D6_PWM_GPIO_Port, &GPIO_InitStruct);

	/*Configure GPIO pin : ARD_D3_PWM_Pin */
	GPIO_InitStruct.Pin = ARD_D3_PWM_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
	GPIO_InitStruct.Alternate = GPIO_AF3_TIM10;
	HAL_GPIO_Init(ARD_D3_PWM_GPIO_Port, &GPIO_InitStruct);

	/*Configure GPIO pins : ARDUINO_A1_Pin ARDUINO_A2_Pin ARDUINO_A3_Pin */
	GPIO_InitStruct.Pin = ARDUINO_A1_Pin|ARDUINO_A2_Pin|ARDUINO_A3_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_ANALOG;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	HAL_GPIO_Init(GPIOF, &GPIO_InitStruct);

	/*Configure GPIO pin : ULPI_STP_Pin */
	GPIO_InitStruct.Pin = ULPI_STP_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
	GPIO_InitStruct.Alternate = GPIO_AF10_OTG_HS;
	HAL_GPIO_Init(ULPI_STP_GPIO_Port, &GPIO_InitStruct);

	/*Configure GPIO pins : RMII_MDC_Pin RMII_RXD0_Pin RMII_RXD1_Pin */
	GPIO_InitStruct.Pin = RMII_MDC_Pin|RMII_RXD0_Pin|RMII_RXD1_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
	GPIO_InitStruct.Alternate = GPIO_AF11_ETH;
	HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);

	/*Configure GPIO pin : ARD_A2_Pin */
	GPIO_InitStruct.Pin = ARD_A2_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_ANALOG;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	HAL_GPIO_Init(ARD_A2_GPIO_Port, &GPIO_InitStruct);

	/*Configure GPIO pin : PB2 */
	GPIO_InitStruct.Pin = GPIO_PIN_2;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
	GPIO_InitStruct.Alternate = GPIO_AF9_QUADSPI;
	HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

	/*Configure GPIO pin : AUDIO_SCL_Pin */
	GPIO_InitStruct.Pin = AUDIO_SCL_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_OD;
	GPIO_InitStruct.Pull = GPIO_PULLUP;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
	GPIO_InitStruct.Alternate = GPIO_AF4_I2C4;
	HAL_GPIO_Init(AUDIO_SCL_GPIO_Port, &GPIO_InitStruct);

	/*Configure GPIO pin : QSPI_D3_Pin */
	GPIO_InitStruct.Pin = QSPI_D3_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
	GPIO_InitStruct.Alternate = GPIO_AF9_QUADSPI;
	HAL_GPIO_Init(QSPI_D3_GPIO_Port, &GPIO_InitStruct);

	/*Configure GPIO pins : RMII_REF_CLK_Pin RMII_MDIO_Pin RMII_CRS_DV_Pin */
	GPIO_InitStruct.Pin = RMII_REF_CLK_Pin|RMII_MDIO_Pin|RMII_CRS_DV_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
	GPIO_InitStruct.Alternate = GPIO_AF11_ETH;
	HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

	/*Configure GPIO pin : B_USER_Pin */
	GPIO_InitStruct.Pin = B_USER_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_IT_RISING;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	HAL_GPIO_Init(B_USER_GPIO_Port, &GPIO_InitStruct);

	/*Configure GPIO pins : ARD_A1_Pin ARD_A0_Pin */
	GPIO_InitStruct.Pin = ARD_A1_Pin|ARD_A0_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_ANALOG;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

	/*Configure GPIO pin : SPDIF_TX_Pin */
	GPIO_InitStruct.Pin = SPDIF_TX_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
	GPIO_InitStruct.Alternate = GPIO_AF10_SAI2;
	HAL_GPIO_Init(SPDIF_TX_GPIO_Port, &GPIO_InitStruct);

	/*Configure GPIO pin : EXT_RST_Pin */
	GPIO_InitStruct.Pin = EXT_RST_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	HAL_GPIO_Init(EXT_RST_GPIO_Port, &GPIO_InitStruct);

	/*Configure GPIO pins : ULPI_CLK_Pin ULPI_D0_Pin */
	GPIO_InitStruct.Pin = ULPI_CLK_Pin|ULPI_D0_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
	GPIO_InitStruct.Alternate = GPIO_AF10_OTG_HS;
	HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

	/*Configure GPIO pin : DSIHOST_TE_Pin */
	GPIO_InitStruct.Pin = DSIHOST_TE_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
	GPIO_InitStruct.Alternate = GPIO_AF13_DSI;
	HAL_GPIO_Init(DSIHOST_TE_GPIO_Port, &GPIO_InitStruct);

	/*Configure GPIO pin : ARDUINO_PWM_D6_Pin */
	GPIO_InitStruct.Pin = ARDUINO_PWM_D6_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
	GPIO_InitStruct.Alternate = GPIO_AF9_TIM12;
	HAL_GPIO_Init(ARDUINO_PWM_D6_GPIO_Port, &GPIO_InitStruct);

	/*Configure GPIO pins : ARDUINO_MISO_D12_Pin ARDUINO_MOSI_PWM_D11_Pin */
	GPIO_InitStruct.Pin = ARDUINO_MISO_D12_Pin|ARDUINO_MOSI_PWM_D11_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
	GPIO_InitStruct.Alternate = GPIO_AF5_SPI2;
	HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

}

/**
 * @brief  This function is executed in case of error occurrence.
 * @retval None
 */
void Error_Handler(void)
{
	//wo keine fehler sind muss nicht gehandelt werden!
}

#ifdef  USE_FULL_ASSERT
/**
 * @brief  Reports the name of the source file and the source line number
 *         where the assert_param error has occurred.
 * @param  file: pointer to the source file name
 * @param  line: assert_param error line source number
 * @retval None
 */
void assert_failed(uint8_t *file, uint32_t line)
{ 
	/* USER CODE BEGIN 6 */
	/* User can add his own implementation to report the file name and line number,
     tex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
	/* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
