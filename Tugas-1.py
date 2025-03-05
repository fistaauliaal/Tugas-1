class Rumah:
    def __init__(self, warna, panjang, lebar, tinggi):
        self.warna = warna
        self.panjang = panjang
        self.lebar = lebar
        self.tinggi = tinggi

    def nyalakan(self, perangkat):
        print(f"{perangkat} dinyalakan.")

    def matikan(self, perangkat):
        print(f"{perangkat} dimatikan.")

# Contoh penggunaan
rumah1 = Rumah("Putih",200,150,100)
rumah1.nyalakan("AC")
rumah1.nyalakan("Lampu")
rumah1.nyalakan("Air") 
rumah1.matikan("AC") 
rumah1.matikan("Lampu")
rumah1.matikan("Air")