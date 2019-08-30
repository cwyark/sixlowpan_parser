

class BaseModel:
    def __init__(self):
        pass
    def render(self):
        pass

class UDPModel(BaseModel):
    VOLTAGE = 3
    TICK_PER_SECONDS = 4096
    POWER_CPU = 1.8 * VOLTAGE
    POWER_LPM = 0.0545 * VOLTAGE
    POWER_TRANSMIT = 17.7 * VOLTAGE
    POWER_LISTEN = 20.0 * VOLTAGE

    def __init__(self, payload):
        if type(payload) is bytes:
            payload = payload.decode('UTF-8')
        self.payload = list(map(int, payload.split(",")))

    @property
    def number_of_neighbour(self):
        return self.payload[0]

    @property
    def EXT(self):
        return self.payload[1] / 8.0

    @property
    def CPUPower(self):
        return (self.payload[2] * self.POWER_CPU) / (self.payload[2] + self.payload[3])

    @property
    def LPMPower(self):
        return (self.payload[3] * self.POWER_LPM) / (self.payload[2] + self.payload[3])

    @property
    def TransmitPower(self):
        return (self.payload[4] * self.POWER_TRANSMIT) / (self.payload[2] + self.payload[3])

    @property
    def ListenRadioPower(self):
        return (self.payload[6] * self.POWER_LISTEN) * (self.payload[2] + self.payload[3])

    @property
    def Temperature(self):
        return self.payload[7]

    @property
    def Humidity(self):
        return (self.payload[8] * 405.0 / 10000.0) - 4.0

    @property
    def BeaconInterval(self):
        return self.payload[9]

    @property
    def RSSI(self):
        return self.payload[10]

    @property
    def LQI(self):
        return self.payload[11]

    @property
    def battery_voltage(self):
        return self.payload[12]

    def render(self):
        pass

class AggregationModel:

    def __init__(self):
        self._NumOfPkts = 0
        self._NumOfLostPkts = 0
        self._NumOfDIO = 0
        self._NumOfDIS = 0
        self._RPLRank = 0
        self._Hops = 0
        self._ReceivedDBMDict = dict()
        self._TransmitDBMDict = dict()
        self._RSSIDict = dict()
        self._BeaconIntervalDict = dict()
        self._LQIDict = dict()
        self._EXTDict = dict()
        self._RouteMetricsDict = dict()
        self._NumOfNeiborsDict = dict()
        self._TemperatureDict = dict()
        self._HumidityDict = dict()
        self._PowerLevelDict = dict()
        self._ConsumedPowerDict = dict()
        self._RemainingPowerDict = dict()
        self.reset()

    @property
    def ReceivedDBM(self):
        """
        Return mean value of ReceivedDBM
        """
        try:
            ret = self._ReceivedDBMDict['sum'] / self._ReceivedDBMDict['number']
        except ZeroDivisionError as e:
            ret = 0
        return ret

    def updateReceivedDBM(self, dbm):
        self._ReceivedDBMDict['number'] += 1
        self._ReceivedDBMDict['sum'] += dbm

    @property
    def TransmitDBM(self):
        """
        return mean valud of TransmitDBM
        """
        try:
            ret = self._TransmitDBMDict['sum'] / self._TransmitDBMDict['number']
        except ZeroDivisionError as e:
            ret = 0
        return ret

    def updateTransmitDBM(self, dbm):
        self._TransmitDBMDict['number'] += 1
        self._TransmitDBMDict['sum'] += dbm

    @property
    def RSSI(self):
        """
        Return mean value of RSSI
        """
        try:
            ret = self._RSSIDict['sum'] / self._RSSIDict['number']
        except ZeroDivisionError as e:
            ret = 0
        return ret

    def updateRSSI(self, rssi):
        self._RSSIDict['number'] += 1
        self._RSSIDict['sum'] += rssi

    @property
    def BeaconInterval(self):
        """
        Return mean value of beacon interval
        """
        try:
            ret = self._BeaconIntervalDict['sum'] / self._BeaconIntervalDict['number']
        except ZeroDivisionError as e:
            ret = 0
        return 0

    def updateBeaconInterval(self, beacon_interval):
        self._BeaconIntervalDict['number'] += 1
        self._BeaconIntervalDict['sum'] += beacon_interval

    @property
    def LQI(self):
        """
        Return mean value of LQI
        """
        try:
            ret = self._LQIDict['sum'] / self._LQIDict['number']
        except ZeroDivisionError as e:
            ret = 0
        return ret

    def updateLQI(self, lqi):
        self._LQIDict['number'] += 1
        self._LQIDict['sum'] = lqi

    @property
    def EXT(self):
        """
        Return mean value of EXT
        """
        try:
            ret = self._EXTDict['sum'] / self._EXTDict['number']
        except ZeroDivisionError as e:
            ret = 0
        return ret

    def updateEXT(self, ext):
        self._EXTDict['number'] += 1
        self._EXTDict['sum'] += ext

    @property
    def NumOfPkts(self):
        """
        number of packets
        """
        return self._NumOfPkts

    def updateNumOfPkts(self, count = 1):
        self._NumOfPkts += count

    @property
    def NumOfLostPkts(self):
        """
        number of lost packet
        """
        return self._NumOfLostPkts

    def updateNumOfLostPkts(self, count = 1):
        self._NumOfLostPkts += count

    @property
    def NumOfDIS(self):
        """
        number of DIS packet
        """
        return self._NumOfDIS

    def updateNumOfDIS(self, count = 1):
        self._NumOfDIS += count

    @property
    def NumOfDIO(self):
        """
        Number of DIO packet
        """
        return self._NumOfDIO

    def updateNumOfDIO(self, count = 1):
        self._NumOfDIO += count

    @property
    def RouteMetrics(self):
        """
        Number of the routing matrices number of htops
        """
        try:
            ret = self._RouteMetricsDict['sum'] / self._RouteMetricsDict['number']
        except ZeroDivisionError as e:
            ret = 0
        return ret

    def updateRouteMetrics(self, hops):
        self._RouteMetricsDict['number'] += 1
        self._RouteMetricsDict['sum'] += hops

    @property
    def RPLRank(self):
        return self._RPLRank

    def updateRPLRank(self, count = 1):
        self._RPLRank += count

    @property
    def Hops(self):
        """
        Number of tops to the sink
        """
        return self._Hops

    def updateHops(self, count = 1):
        self._Hops += count

    @property
    def PPR(self):
        """
        Packet Reception Ratio
        """
        return 0

    @property
    def NumOfNabors(self):
        """
        Mean value of Number of Nighbours
        """
        try:
            ret = self._NumOfNabors['sum'] / self._NumOfNabors['number']
        except ZeroDivisionError as e:
            ret = 0
        return ret

    def updateNumOfNabors(self, number_of_neighbour):
        self._NumOfNeiborsDict['number'] += 1
        self._NumOfNeiborsDict['sum'] += number_of_neighbour

    @property
    def Temperature(self):
        """
        Mean value of the temperature
        """
        try:
            ret = self._TemperatureDict['sum'] / self._TemperatureDict['number']
        except ZeroDivisionError as e:
            ret = 0
        return ret

    def updateTemperature(self, temp):
        self._TemperatureDict['number'] += 1
        self._TemperatureDict['sum'] += temp

    @property
    def Humidity(self):
        """
        Mean value of the Humidity
        """
        try:
            ret = self._HumidityDict['sum'] / self._HumidityDict['number']
        except ZeroDivisionError as e:
            ret = 0
        return ret

    def updateHumidity(self, humi):
        self._HumidityDict['number'] += 1
        self._HumidityDict['sum'] += humi

    @property
    def PowerLevel(self):
        """
        Mean value of energy over time
        """
        try:
            ret = self._PowerLevelDict['sum'] / self._PowerLevelDict['number']
        except ZeroDivisionError as e:
            ret = 0
        return ret

    def updatePowerLevel(self, power_level):
        self._PowerLevelDict['number'] += 1
        self._PowerLevelDict['sum'] += power_level

    @property
    def ConsumedPower(self):
        """
        Mean value of consumed node
        """
        try:
            ret = self._ConsumedPowerDict['sum'] / self._ConsumedPowerDict['number']
        except ZeroDivisionError as e:
            ret = 0
        return ret

    def updateConsumedPower(self, power):
        self._ConsumedPowerDict['number'] += 1
        self._ConsumedPowerDict['sum'] += power

    @property
    def RemainingPower(self):
        """
        Mean value of the remaining node power
        """
        try:
            ret = self._RemainingPowerDict['sum'] / self._RemainingPowerDict['number']
        except ZeroDivisionError as e:
            ret = 0
        return ret

    def updateRemainingPower(self, power):
        self._RemainingPowerDict['number'] += 1
        self._RemainingPowerDict['sum'] += power

    @property
    def NodeId(self):
        """
        node id
        """
        return 0

    def updateUDPModel(self, udp_model):
        self.updateReceivedDBM(udp_model.ListenRadioPower)
        self.updateTransmitDBM(udp_model.TransmitPower)
        self.updateRSSI(udp_model.RSSI)
        self.updateBeaconInterval(udp_model.BeaconInterval)
        self.updateLQI(udp_model.LQI)
        self.updateEXT(udp_model.EXT)
        # Number of packets ?
        # Number of lost packets ?
        self.updateNumOfNabors(udp_model.number_of_neighbour)
        self.updateTemperature(udp_model.Temperature)
        self.updateHumidity(udp_model.Humidity)
        self.updatePowerLevel(udp_model.battery_voltage)
        self.updateConsumedPower(udp_model.CPUPower)
        self.updateRemainingPower(udp_model.LPMPower)

    @property
    def to_dict(self):
        return dict(
                ReceivedDBM = self.ReceivedDBM,
                TransmitDBM = self.TransmitDBM,
                RSSI = self.RSSI,
                BeaconInterval = self.BeaconInterval,
                LQI = self.LQI,
                NumOfDIS = self.NumOfDIS,
                NumOfDIO = self.NumOfDIO,
                Temperature = self.Temperature,
                Humidity = self.Humidity,
                PowerLevel = self.PowerLevel,
                ConsumedPower = self.ConsumedPower,
                RemainingPower = self.RemainingPower,
                NumOfNabors = self.NumOfNabors
                )

    def reset(self):
        self._NumOfPkts = 0
        self._NumOfLostPkts = 0
        self._NumOfDIO = 0
        self._NumOfDIS = 0
        self._RPLRank = 0
        self._Hops = 0
        self._ReceivedDBMDict = dict(number = 0, sum = 0)
        self._TransmitDBMDict = dict(number = 0, sum = 0)
        self._RSSIDict = dict(number = 0, sum = 0)
        self._BeaconIntervalDict = dict(number = 0, sum = 0)
        self._LQIDict = dict(number = 0, sum = 0)
        self._EXTDict = dict(number = 0, sum = 0)
        self._RouteMetricsDict = dict(number = 0, sum = 0)
        self._NumOfNeiborsDict = dict(number = 0, sum = 0)
        self._TemperatureDict = dict(number = 0, sum = 0)
        self._HumidityDict = dict(number = 0, sum = 0)
        self._PowerLevelDict = dict(number = 0, sum = 0)
        self._ConsumedPowerDict = dict(number = 0, sum = 0)
        self._RemainingPowerDict = dict(number = 0, sum = 0)
