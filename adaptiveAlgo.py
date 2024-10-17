import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import time

# Fungsi untuk membuat sistem fuzzy lampu hijau
def create_fuzzy_system():
    lebar_lajur = ctrl.Antecedent(np.arange(1.7, 4, 0.1), 'Lebar Lajur')
    jumlah_ringan = ctrl.Antecedent(np.arange(0, 60, 1), 'Jumlah Kendaraan Ringan')
    jumlah_berat = ctrl.Antecedent(np.arange(0, 20, 1), 'Jumlah Kendaraan Berat')

    waktu_hijau = ctrl.Consequent(np.arange(5, 65, 0.1), "Lama Waktu Lampu Hijau")

    # Membership functions
    jumlah_ringan['Sepi'] = fuzz.trapmf(jumlah_ringan.universe, [-5, 0, 15, 30])
    jumlah_ringan['Sedang'] = fuzz.trapmf(jumlah_ringan.universe, [15, 30, 30, 45])
    jumlah_ringan['Ramai'] = fuzz.trapmf(jumlah_ringan.universe, [30, 45, 60, 65])

    jumlah_berat['Sepi'] = fuzz.trapmf(jumlah_berat.universe, [-5, 0, 3, 6])
    jumlah_berat['Sedang'] = fuzz.trapmf(jumlah_berat.universe, [3, 6, 9, 12])
    jumlah_berat['Ramai'] = fuzz.trapmf(jumlah_berat.universe, [9, 12, 20, 25])

    lebar_lajur['Sempit'] = fuzz.trapmf(lebar_lajur.universe, [0, 1.7, 2, 2.5])
    lebar_lajur['Lebar'] = fuzz.trapmf(lebar_lajur.universe, [2, 2.5, 4, 4.5])

    waktu_hijau['S'] = fuzz.trapmf(waktu_hijau.universe, [-5, 0, 10, 20])
    waktu_hijau['M'] = fuzz.trapmf(waktu_hijau.universe, [10, 20, 20, 30])
    waktu_hijau['L'] = fuzz.trapmf(waktu_hijau.universe, [20, 30, 30, 40])
    waktu_hijau['VL'] = fuzz.trapmf(waktu_hijau.universe, [30, 40, 65, 70])

    # Definisikan aturan fuzzy
    rules = [
        ctrl.Rule(lebar_lajur['Sempit'] & jumlah_ringan['Sepi'] & jumlah_berat['Sepi'], waktu_hijau['S']),
        ctrl.Rule(lebar_lajur['Sempit'] & jumlah_ringan['Sepi'] & jumlah_berat['Sedang'], waktu_hijau['M']),
        ctrl.Rule(lebar_lajur['Sempit'] & jumlah_ringan['Sepi'] & jumlah_berat['Ramai'], waktu_hijau['L']),
        ctrl.Rule(lebar_lajur['Sempit'] & jumlah_ringan['Sedang'] & jumlah_berat['Sepi'], waktu_hijau['M']),
        ctrl.Rule(lebar_lajur['Sempit'] & jumlah_ringan['Sedang'] & jumlah_berat['Sedang'], waktu_hijau['L']),
        ctrl.Rule(lebar_lajur['Sempit'] & jumlah_ringan['Sedang'] & jumlah_berat['Ramai'], waktu_hijau['VL']),
        ctrl.Rule(lebar_lajur['Sempit'] & jumlah_ringan['Ramai'] & jumlah_berat['Sepi'], waktu_hijau['M']),
        ctrl.Rule(lebar_lajur['Sempit'] & jumlah_ringan['Ramai'] & jumlah_berat['Sedang'], waktu_hijau['VL']),
        ctrl.Rule(lebar_lajur['Sempit'] & jumlah_ringan['Ramai'] & jumlah_berat['Ramai'], waktu_hijau['VL']),
        ctrl.Rule(lebar_lajur['Lebar'] & jumlah_ringan['Sepi'] & jumlah_berat['Sepi'], waktu_hijau['S']),
        ctrl.Rule(lebar_lajur['Lebar'] & jumlah_ringan['Sepi'] & jumlah_berat['Sedang'], waktu_hijau['S']),
        ctrl.Rule(lebar_lajur['Lebar'] & jumlah_ringan['Sepi'] & jumlah_berat['Ramai'], waktu_hijau['L']),
        ctrl.Rule(lebar_lajur['Lebar'] & jumlah_ringan['Sedang'] & jumlah_berat['Sepi'], waktu_hijau['S']),
        ctrl.Rule(lebar_lajur['Lebar'] & jumlah_ringan['Sedang'] & jumlah_berat['Sedang'], waktu_hijau['M']),
        ctrl.Rule(lebar_lajur['Lebar'] & jumlah_ringan['Sedang'] & jumlah_berat['Ramai'], waktu_hijau['L']),
        ctrl.Rule(lebar_lajur['Lebar'] & jumlah_ringan['Ramai'] & jumlah_berat['Sepi'], waktu_hijau['M']),
        ctrl.Rule(lebar_lajur['Lebar'] & jumlah_ringan['Ramai'] & jumlah_berat['Sedang'], waktu_hijau['L']),
        ctrl.Rule(lebar_lajur['Lebar'] & jumlah_ringan['Ramai'] & jumlah_berat['Ramai'], waktu_hijau['VL'])
    ]

    # Membuat sistem kontrol fuzzy
    traffic_ctrl = ctrl.ControlSystem(rules)
    return ctrl.ControlSystemSimulation(traffic_ctrl)

# Inisialisasi bobot
bobot_jumlah = 1
bobot_kelaparan = 1

# Inisialisasi data untuk setiap lajur
lajur_data = {
    "utara": {
        "lebar_lajur": 3.0,
        "jumlah_ringan": 20,
        "jumlah_berat": 5,
        "kelaparan": 0
    },
    "timur": {
        "lebar_lajur": 2.5,
        "jumlah_ringan": 15,
        "jumlah_berat": 3,
        "kelaparan": 0
    },
    "selatan": {
        "lebar_lajur": 3.5,
        "jumlah_ringan": 25,
        "jumlah_berat": 7,
        "kelaparan": 0
    },
    "barat": {
        "lebar_lajur": 2.0,
        "jumlah_ringan": 10,
        "jumlah_berat": 2,
        "kelaparan": 0
    }
}

# Fungsi untuk menghitung skor berdasarkan jumlah kendaraan dan hungry level
def hitung_skor(lajur_data):
    total_jumlah = sum(data['jumlah_ringan'] + data['jumlah_berat'] for data in lajur_data.values())
    skor = {}
    for arah, data in lajur_data.items():
        jumlah_kendaraan = data['jumlah_ringan'] + data['jumlah_berat']
        skor[arah] = (bobot_jumlah * (jumlah_kendaraan / total_jumlah)) + (bobot_kelaparan * (data['kelaparan'] / total_jumlah))
    return skor

# Fungsi untuk memilih lajur berdasarkan skor tertinggi
def pilih_lajur(skor):
    return max(skor, key=skor.get)

# Fungsi untuk memperbarui hungry level
def perbarui_kelaparan(lajur_terpilih, lajur_data):
    for arah in lajur_data.keys():
        if arah == lajur_terpilih:
            lajur_data[arah]['kelaparan'] = 0  # Reset kelaparan jika lajur terpilih
        else:
            lajur_data[arah]['kelaparan'] += 1  # Tambah kelaparan untuk lajur yang tidak terpilih

# Fungsi untuk memeriksa apakah ada kendaraan di semua lajur
def kendaraan_masih_ada(lajur_data):
    return any(data['jumlah_ringan'] > 0 or data['jumlah_berat'] > 0 for data in lajur_data.values())

# Simulasi menggunakan while loop
putaran = 0
while kendaraan_masih_ada(lajur_data):
    putaran += 1
    print(f"\n=== Putaran {putaran} ===")
    # Hitung skor untuk setiap lajur
    skor = hitung_skor(lajur_data)

    # Pilih lajur dengan skor tertinggi
    lajur_terpilih = pilih_lajur(skor)

    # Buat sistem fuzzy untuk lajur terpilih
    traffic_sim = create_fuzzy_system()

    # Masukkan input ke sistem fuzzy
    data_lajur = lajur_data[lajur_terpilih]
    traffic_sim.input['Lebar Lajur'] = data_lajur['lebar_lajur']
    traffic_sim.input['Jumlah Kendaraan Ringan'] = data_lajur['jumlah_ringan']
    traffic_sim.input['Jumlah Kendaraan Berat'] = data_lajur['jumlah_berat']

    # Lakukan komputasi fuzzy
    traffic_sim.compute()

    # Dapatkan hasil durasi lampu hijau
    waktu_hijau = traffic_sim.output['Lama Waktu Lampu Hijau']

    # Tampilkan hasil
    print(f"Lajur yang terpilih: {lajur_terpilih.capitalize()}")
    print(f"Durasi lampu hijau: {waktu_hijau:.2f} detik")

    # Perbarui hungry level
    perbarui_kelaparan(lajur_terpilih, lajur_data)

    # Simulasikan perubahan jumlah kendaraan
    for arah in lajur_data.keys():
        if arah == lajur_terpilih:
            # Kendaraan berkurang setelah lampu hijau
            lajur_data[arah]['jumlah_ringan'] = max(0, lajur_data[arah]['jumlah_ringan'] - 5)
            lajur_data[arah]['jumlah_berat'] = max(0, lajur_data[arah]['jumlah_berat'] - 2)
        else:
            # Kendaraan bertambah di lajur lain
            lajur_data[arah]['jumlah_ringan'] += np.random.randint(1, 5)
            lajur_data[arah]['jumlah_berat'] += np.random.randint(0, 2)

    # Tampilkan hungry level setelah pembaruan
    print(f"Hungry level setelah pembaruan: ")
    for arah, data in lajur_data.items():
        print(f"  '{arah}': {data['kelaparan']}", end=',\n')
    print(" ")

    time.sleep(5)