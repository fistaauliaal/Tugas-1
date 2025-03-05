class RemoteTv:
    def __init__(self):
        self.switchIsOn = False
        self.brightness = 0
        self.volume = 5  # Volume awal, misalnya diatur ke 5
        self.MAX_VOLUME = 10  # Batas maksimum volume
        self.MIN_VOLUME = 0   # Batas minimum volume

    def turnOn(self):
        self.switchIsOn = True

    def turnOff(self):
        self.switchIsOn = False

    def raiseLevel(self):
        if self.brightness < 10:
            self.brightness += 1

    def lowerLevel(self):
        if self.brightness > 0:
            self.brightness -= 1

    def volumeUp(self):
        if self.volume < self.MAX_VOLUME:
            self.volume += 1
        else:
            print("Volume sudah maksimum!")

    def volumeDown(self):
        if self.volume > self.MIN_VOLUME:
            self.volume -= 1
        else:
            print("Volume sudah minimum!")

    # Extra method for debugging
    def show(self):
        print('Switch is on ?', self.switchIsOn)
        print('Brightness is:', self.brightness)
        print('Volume is:', self.volume)


# Main code
remoteSatu = RemoteTv()

# Nyalakan TV, tingkatkan brightness dan volume
remoteSatu.turnOn()
remoteSatu.raiseLevel()
remoteSatu.raiseLevel()
remoteSatu.raiseLevel()
remoteSatu.raiseLevel()
remoteSatu.raiseLevel()
remoteSatu.volumeUp()
remoteSatu.volumeUp()
remoteSatu.show()

# Turunkan brightness dan volume
remoteSatu.lowerLevel()
remoteSatu.lowerLevel()
remoteSatu.volumeDown()
remoteSatu.volumeDown()
remoteSatu.turnOff()
remoteSatu.show()