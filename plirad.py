
class GLLv3:
    i2c = None

    __GLL_ACQ_COMMAND       = 0x00
    __GLL_STATUS            = 0x01
    __GLL_SIG_COUNT_VAL     = 0x02
    __GLL_ACQ_CONFIG_REG    = 0x04
    __GLL_VELOCITY          = 0x09
    __GLL_PEAK_CORR         = 0x0C
    __GLL_NOISE_PEAK        = 0x0D
    __GLL_SIGNAL_STRENGTH   = 0x0E
    __GLL_FULL_DELAY_HIGH   = 0x0F
    __GLL_FULL_DELAY_LOW    = 0x10
    __GLL_OUTER_LOOP_COUNT  = 0x11
    __GLL_REF_COUNT_VAL     = 0x12
    __GLL_LAST_DELAY_HIGH   = 0x14
    __GLL_LAST_DELAY_LOW    = 0x15
    __GLL_UNIT_ID_HIGH      = 0x16
    __GLL_UNIT_ID_LOW       = 0x17
    __GLL_I2C_ID_HIGHT      = 0x18
    __GLL_I2C_ID_LOW        = 0x19
    __GLL_I2C_SEC_ADDR      = 0x1A
    __GLL_THRESHOLD_BYPASS  = 0x1C
    __GLL_I2C_CONFIG        = 0x1E
    __GLL_COMMAND           = 0x40
    __GLL_MEASURE_DELAY     = 0x45
    __GLL_PEAK_BCK          = 0x4C
    __GLL_CORR_DATA         = 0x52
    __GLL_CORR_DATA_SIGN    = 0x53
    __GLL_ACQ_SETTINGS      = 0x5D
    __GLL_POWER_CONTROL     = 0x65

    def __init__(self, address=0x62, rate=10):
        self.i2c = I2C(address)
        self.rate = rate

        #-------------------------------------------------------------------------------------------
        # Set to continuous sampling after initial read.
        #-------------------------------------------------------------------------------------------
        self.i2c.write8(self.__GLL_OUTER_LOOP_COUNT, 0xFF)

        #-------------------------------------------------------------------------------------------
        # Set the sampling frequency as 2000 / Hz:
        # 10Hz = 0xc8
        # 20Hz = 0x64
        # 100Hz = 0x14
        #-------------------------------------------------------------------------------------------
        self.i2c.write8(self.__GLL_MEASURE_DELAY, int(2000 / rate))

        #-------------------------------------------------------------------------------------------
        # Include receiver bias correction 0x04
        #AB: 0x04 | 0x01 should cause (falling edge?) GPIO_GLL_DR_INTERRUPT.  Test GPIO handle this?
        #-------------------------------------------------------------------------------------------
        self.i2c.write8(self.__GLL_ACQ_COMMAND, 0x04 | 0x01)

        #-------------------------------------------------------------------------------------------
        # Acquisition config register:
        # 0x01 Data ready interrupt
        # 0x20 Take sampling rate from MEASURE_DELAY
        #-------------------------------------------------------------------------------------------
        self.i2c.write8(self.__GLL_ACQ_CONFIG_REG, 0x21)


    def read(self):
        #-------------------------------------------------------------------------------------------
        # Distance is in cm hence the 100s to convert to meters.
        # Velocity is in cm between consecutive reads; sampling rate converts these to a velocity.
        # Reading the list from 0x8F seems to get the previous reading, probably cached for the sake
        # of calculating the velocity next time round.
        #-------------------------------------------------------------------------------------------
        distance = self.i2c.readU16(self.__GLL_FULL_DELAY_HIGH)
        if distance == 1:
            raise ValueError("GLL out of range")

        return distance / 100
print(distance/100)
