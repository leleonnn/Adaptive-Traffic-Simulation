# -*- coding: utf-8 -*-
"""FuzzyTheory.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1fZAwWXV9qtFLYYHu4IKQ7eTzi6yAIdGB
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

lebar_lajur = ctrl.Antecedent(np.arange(1.7, 4, 0.1), 'Lebar Lajur')
jumlah_ringan = ctrl.Antecedent(np.arange(0, 60, 1), 'Jumlah Kendaraan Ringan')
jumlah_berat = ctrl.Antecedent(np.arange(0, 20, 1), 'Jumlah Kendaraan Berat')

waktu_hijau = ctrl.Consequent(np.arange(5, 65, 0.1), "Lama Waktu Lampu Hijau")

jumlah_ringan['Sepi'] = fuzz.trapmf(jumlah_ringan.universe, [-5, 0, 15, 30])
jumlah_ringan['Sedang'] = fuzz.trapmf(jumlah_ringan.universe, [15, 30, 30, 45])
jumlah_ringan['Ramai'] = fuzz.trapmf(jumlah_ringan.universe, [30, 45, 60, 65])

jumlah_ringan.view()

jumlah_berat['Sepi'] = fuzz.trapmf(jumlah_berat.universe, [-5, 0, 3, 6])
jumlah_berat['Sedang'] = fuzz.trapmf(jumlah_berat.universe, [3, 6, 9, 12])
jumlah_berat['Ramai'] = fuzz.trapmf(jumlah_berat.universe, [9, 12, 20, 25])

jumlah_berat.view()

lebar_lajur['Sempit'] = fuzz.trapmf(lebar_lajur.universe, [0, 1.7, 2, 2.5])
lebar_lajur['Lebar'] = fuzz.trapmf(lebar_lajur.universe, [2, 2.5, 4, 4.5])

lebar_lajur.view()

waktu_hijau['S'] = fuzz.trapmf(waktu_hijau.universe, [-5, 0, 10, 20])
waktu_hijau['M'] = fuzz.trapmf(waktu_hijau.universe, [10, 20, 20, 30])
waktu_hijau['L'] = fuzz.trapmf(waktu_hijau.universe, [20, 30, 30, 40])
waktu_hijau['VL'] = fuzz.trapmf(waktu_hijau.universe, [30, 40, 65, 70])

waktu_hijau.view()

rule1 = ctrl.Rule(lebar_lajur['Sempit'] & jumlah_ringan['Sepi'] & jumlah_berat['Sepi'], waktu_hijau['S'])
rule2 = ctrl.Rule(lebar_lajur['Sempit'] & jumlah_ringan['Sepi'] & jumlah_berat['Sedang'], waktu_hijau['M'])
rule3 = ctrl.Rule(lebar_lajur['Sempit'] & jumlah_ringan['Sepi'] & jumlah_berat['Ramai'], waktu_hijau['L'])
rule4 = ctrl.Rule(lebar_lajur['Sempit'] & jumlah_ringan['Sedang'] & jumlah_berat['Sepi'], waktu_hijau['M'])
rule5 = ctrl.Rule(lebar_lajur['Sempit'] & jumlah_ringan['Sedang'] & jumlah_berat['Sedang'], waktu_hijau['L'])
rule6 = ctrl.Rule(lebar_lajur['Sempit'] & jumlah_ringan['Sedang'] & jumlah_berat['Ramai'], waktu_hijau['VL'])
rule7 = ctrl.Rule(lebar_lajur['Sempit'] & jumlah_ringan['Ramai'] & jumlah_berat['Sepi'], waktu_hijau['M'])
rule8 = ctrl.Rule(lebar_lajur['Sempit'] & jumlah_ringan['Ramai'] & jumlah_berat['Sedang'], waktu_hijau['VL'])
rule9 = ctrl.Rule(lebar_lajur['Sempit'] & jumlah_ringan['Ramai'] & jumlah_berat['Ramai'], waktu_hijau['VL'])
rule10 = ctrl.Rule(lebar_lajur['Lebar'] & jumlah_ringan['Sepi'] & jumlah_berat['Sepi'], waktu_hijau['S'])
rule11 = ctrl.Rule(lebar_lajur['Lebar'] & jumlah_ringan['Sepi'] & jumlah_berat['Sedang'], waktu_hijau['S'])
rule12 = ctrl.Rule(lebar_lajur['Lebar'] & jumlah_ringan['Sepi'] & jumlah_berat['Ramai'], waktu_hijau['L'])
rule13 = ctrl.Rule(lebar_lajur['Lebar'] & jumlah_ringan['Sedang'] & jumlah_berat['Sepi'], waktu_hijau['S'])
rule14 = ctrl.Rule(lebar_lajur['Lebar'] & jumlah_ringan['Sedang'] & jumlah_berat['Sedang'], waktu_hijau['M'])
rule15 = ctrl.Rule(lebar_lajur['Lebar'] & jumlah_ringan['Sedang'] & jumlah_berat['Ramai'], waktu_hijau['L'])
rule16 = ctrl.Rule(lebar_lajur['Lebar'] & jumlah_ringan['Ramai'] & jumlah_berat['Sepi'], waktu_hijau['M'])
rule17 = ctrl.Rule(lebar_lajur['Lebar'] & jumlah_ringan['Ramai'] & jumlah_berat['Sedang'], waktu_hijau['L'])
rule18 = ctrl.Rule(lebar_lajur['Lebar'] & jumlah_ringan['Ramai'] & jumlah_berat['Ramai'], waktu_hijau['VL'])

traffic_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18])
traffic = ctrl.ControlSystemSimulation(traffic_ctrl)

traffic.input['Lebar Lajur'] = 2
traffic.input['Jumlah Kendaraan Ringan'] = 20
traffic.input['Jumlah Kendaraan Berat'] = 6
traffic.compute()

waktu_hijau.view(sim=traffic)

print(traffic.output['Lama Waktu Lampu Hijau'])

