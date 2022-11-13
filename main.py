import nltk
nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow
import random
import json
import pickle
import telebot
import time
import re

with open("intents.json") as file:
	data = json.load(file)

try:
	with open("data.pickle", "rb") as f:
		words, labels, training, output = pickle.load(f)
except:
	words = []
	labels = []
	docs_x = []
	docs_y = []
	
	for intent in data["intents"]:
		for pattern in intent["patterns"]:
			wrds = nltk.word_tokenize(pattern)
			words.extend(wrds)
			docs_x.append(wrds)
			docs_y.append(intent["tag"])

		if intent["tag"] not in labels:
			labels.append(intent["tag"])

	words = [stemmer.stem(w.lower()) for w in words if w != "?"]
	words = sorted(list(set(words)))

	labels = sorted(labels)

	training = []
	output = []

	out_empty = [0 for _ in range(len(labels))]

	for x, doc in enumerate(docs_x):
		bag = []

		wrds = [stemmer.stem(w) for w in doc]

		for w in words:
			if w in wrds:
				bag.append(1)
			else:
				bag.append(0)

		output_row = out_empty[:]
		output_row[labels.index(docs_y[x])] = 1

		training.append(bag)
		output.append(output_row)

		with open("data.pickle", "wb") as f:
			pickle.dump((words, labels, training, output), f)

training = numpy.array(training)
output = numpy.array(output)

tensorflow.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 150)
net = tflearn.fully_connected(net, 150)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
model.save("model.tflearn")

bot_token = '1342465421:AAGzRcFgHpr9qEQng8OICRkuJW3nGkrs9o4'
bot = telebot.TeleBot(bot_token)

item = 'selesai'
jumlah_pesanan = 0
pesan = ''
tag = ''

@bot.message_handler()
def chat(message):
	global tag, pesanan, item, jumlah_pesanan, pesan
	inp = message.text
	print(item)
	for intent in data["intents"]:
		if intent["tag"] == item:
			pesanan = int(inp) * int(intent["harga"])
			pesan = pesan + ' ' + item + ' ' + inp + '@' + intent["harga"] + " = Rp "+ str(pesanan) + "."
			jumlah_pesanan = jumlah_pesanan + pesanan
			bot.reply_to(message, pesanan)
			bot.reply_to(message, "Ketik nama vessel untuk melanjutkan atau ketik Tidak jika sudah selesai")
			inp = 'Selesai'

	if(tag == "Berapa tue?" and inp != "Selesai"):
		if inp == "Tidak":
			pesan = ["Terima kasih sudah melakukan pemesanan di TANTO!" + "\n" + "\nPesanan Anda adalah " + pesan + "\nTotal biaya yang harus dibayar adalah Rp " + str(jumlah_pesanan) + "\n" +
"\nApabila sudah benar silahkan hubungi (021)8067 8000 untuk memeriksa ketersediaan kuota dan proses lebih lanjut"  + "\n" + "\nHarga tidak mengikat mohon konfirmasi kepada marketing sebelum pengiriman"+ "\n" + "\nKetik Selesai jika sudah."]
			bot.reply_to(message, pesan)
		else:
			bot.reply_to(message, tag)
			item = inp
	else:
		item = 'Selesai'

	if inp == "jkt":
		poljkt = ["--- pelabuhan muat Jakarta ---"
		"\n"
		"\nKetik balikpapan untuk melihat jadwal pelabuhan balikpapan"
		"\nKetik banjarmasin untuk melihat jadwal pelabuhan banjarmasin"
		"\nKetik batam untuk melihat jadwal pelabuhan batam"
		"\nKetik bitung untuk melihat jadwal pelabuhan bitung"
		"\nKetik makassar untuk melihat jadwal pelabuhan makassar"
		"\nKetik medan untuk melihat jadwal pelabuhan medan"
		"\nKetik padang untuk melihat jadwal pelabuhan padang"
		"\nKetik perawang untuk melihat jadwal pelabuhan perawang"
		"\nKetik pontianak untuk melihat jadwal pelabuhan pontianak"
		"\nKetik samarinda untuk melihat jadwal pelabuhan samarinda"
		"\nKetik sibolga untuk melihat jadwal pelabuhan sibolga"
		"\nKetik surabaya untuk melihat jadwal pelabuhan surabaya"
		"\n"
		"\nUntuk kembali ke menu pilihan pol ketik pol"]
		bot.reply_to(message, poljkt)
	elif inp == "sby":
		polsby = ["--- pelabuhan muat Surabaya ---"
		"\n"
		"\nKetik ambon untuk melihat jadwal pelabuhan ambon"
		"\nKetik benete untuk melihat jadwal pelabuhan benete"
		"\nKetik bitung2 untuk melihat jadwal pelabuhan bitung"
		"\nKetik gorontalo anggrek untuk melihat jadwal pelabuhan gorontalo anggrek"
		"\nKetik kendari untuk melihat jadwal pelabuhan kendari"
		"\nKetik lembar untuk melihat jadwal pelabuhan lembar"
		"\nKetik luwuk untuk melihat jadwal pelabuhan luwuk"
		"\nKetik makassar2 untuk melihat jadwal pelabuhan makassar"
		"\nKetik samarinda2 untuk melihat jadwal pelabuhan samarinda"
		"\nKetik sorong untuk melihat jadwal pelabuhan sorong"
		"\nKetik ternate untuk melihat jadwal pelabuhan ternate"
		"\n"
		"\nUntuk kembali ke menu pilihan pol ketik pol"]
		bot.reply_to(message, polsby)

	if inp == "banjarmasin":
		pilbjr = ["--- Untuk pelabuhan muat Banjarmasin ---"
		"\n"
		"\n-------------------"
		"\nHari: Rabu"
		"\nVessel: SINAR PRAYA"
		"\nWaktu Tempuh: 2 Hari "
		"\nTarif: Rp3000000/tue"
		"\n-------------------"
		"\nHari: Sabtu"
		"\nVessel: TANTO TERIMA"
		"\nWaktu Tempuh: 2 Hari "
		"\nTarif: Rp3000000/tue"
		"\n-------------------"
		"\n"
		"\nUntuk kembali ke menu pilihan POL ketik pol"]
		bot.reply_to(message, pilbjr)
	elif inp == "banjarmasin2":
		pilbjr2 = ["--- Untuk pelabuhan muat Banjarmasin ---"
		"\n"
		"\n-------------------"
		"\nHari: Rabu"
		"\nVessel: TANTO HORAS"
		"\nWaktu Tempuh: 1 Hari "
		"\nTarif: Rp1200000/tue"
		"\n-------------------"
		"\nHari: Kamis"
		"\nVessel: TANTO HORAS 2"
		"\nWaktu Tempuh: 2 Hari "
		"\nTarif: Rp1200000/tue"
		"\n-------------------"
		"\nHari: Jumat"
		"\nVessel: TANTO HARMONI"
		"\nWaktu Tempuh: 1 Hari "
		"\nTarif: Rp1200000/tue"
		"\n-------------------"
		"\nHari: Minggu"
		"\nVessel: TANTO HARMONI 2"
		"\nWaktu Tempuh: 1 Hari "
		"\nTarif: Rp1200000/tue"
		"\n-------------------"
		"\n"
		"\nUntuk kembali ke menu pilihan POL ketik pol"]
		bot.reply_to(message, pilbjr2)
	elif inp == "batam":
		pilbtm = ["--- Untuk pelabuhan muat Batam ---"
		"\n"
		"\n-------------------"
		"\nHari: Kamis"
		"\nVessel: TANTO LANCAR"
		"\nWaktu Tempuh: 2 Hari "
		"\nTarif: Rp3000000/tue"
		"\n-------------------"
		"\n"
		"\nUntuk kembali ke menu pilihan POL ketik pol"]
		bot.reply_to(message, pilbtm)
	elif inp == "samarinda":
		pilsmrnd = ["--- Untuk pelabuhan muat Batam ---"
		"\n"
		"\n-------------------"
		"\nHari: Minggu"
		"\nVessel: TANTO KURNIA 2"
		"\nWaktu Tempuh: 3 Hari "
		"\nTarif: Rp3000000/tue"
		"\n-------------------"
		"\n"
		"\nUntuk kembali ke menu pilihan POL ketik pol"]
		bot.reply_to(message, pilsmrnd)
	elif inp == "surabaya":
		pilsby = ["--- Untuk pelabuhan muat Surabaya ---"
		"\n"
		"\n-------------------"
		"\nHari: Selasa"
		"\nVessel: TANTO TERANG"
		"\nWaktu Tempuh: 1 Hari "
		"\nTarif: Rp2000000/tue"
		"\n-------------------"
		"\nHari: Kamis"
		"\nVessel: TANTO TANGGUH"
		"\nWaktu Tempuh: 1 Hari "
		"\nTarif: Rp2000000/tue"
		"\n-------------------"
		"\nHari: Minggu"
		"\nVessel: TANTO SEJAHTERA"
		"\nWaktu Tempuh: 1 Hari "
		"\nTarif: Rp2000000/tue"
		"\n-------------------"
		"\n"
		"\nUntuk kembali ke menu pilihan POL ketik pol"]
		bot.reply_to(message, pilsby)
	elif inp == "pontianak":
		pilptn = ["--- Untuk pelabuhan muat Pontianak ---"
		"\n"
		"\n-------------------"
		"\nHari: Rabu"
		"\nVessel: TANTO SEHAT"
		"\nWaktu Tempuh: 2 Hari "
		"\nTarif: Rp2500000/tue"
		"\n-------------------"
		"\nHari: Jumat"
		"\nVessel: TANTO LANGGENG"
		"\nWaktu Tempuh: 2 Hari "
		"\nTarif: Rp2500000/tue"
		"\n-------------------"
		"\nHari: Minggu"
		"\nVessel: TANTO MANDIRI"
		"\nWaktu Tempuh: 2 Hari "
		"\nTarif: Rp2500000/tue"
		"\n-------------------"
		"\n"
		"\nUntuk kembali ke menu pilihan POL ketik pol"]
		bot.reply_to(message, pilptn)
	elif inp == "medan":
		pilmdn = ["--- Untuk pelabuhan muat Medan ---"
		"\n"
		"\n-------------------"
		"\nHari: Kamis"
		"\nVessel: TANTO NUSANTARA"
		"\nWaktu Tempuh: 3 Hari "
		"\nTarif: Rp3000000/tue"
		"\n-------------------"
		"\nHari: Minggu"
		"\nVessel: TANTO BERSAMA"
		"\nWaktu Tempuh: 3 Hari "
		"\nTarif: Rp3000000/tue"
		"\n-------------------"
		"\n"
		"\nUntuk kembali ke menu pilihan POL ketik pol"]
		bot.reply_to(message, pilmdn)
	elif inp == "makassar":
		pilmksr = ["--- Untuk pelabuhan muat Makassar ---"
		"\n"
		"\n-------------------"
		"\nHari: Sabtu"
		"\nVessel: TANTO TENANG"
		"\nWaktu Tempuh: 3 Hari "
		"\nTarif: Rp3000000/tue"
		"\n-------------------"
		"\nHari: Minggu"
		"\nVessel: TANTO BERSATU"
		"\nWaktu Tempuh: 3 Hari "
		"\nTarif: Rp3000000/tue"
		"\n-------------------"
		"\n"
		"\nUntuk kembali ke menu pilihan POL ketik pol"]
		bot.reply_to(message, pilmksr)
	elif inp == "makassar2":
		pilmksr2 = ["--- Untuk pelabuhan muat Makassar ---"
		"\n"
		"\n-------------------"
		"\nHari: Sabtu"
		"\nVessel: TANTO SIAP"
		"\nWaktu Tempuh: 2 Hari "
		"\nTarif: Rp1500000/tue"
		"\n-------------------"
		"\n"
		"\nUntuk kembali ke menu pilihan POL ketik pol"]
		bot.reply_to(message, pilmksr2)
	elif inp == "padang":
		pilpdg = ["--- Untuk pelabuhan muat Padang ---"
		"\n"
		"\n-------------------"
		"\nHari: Minggu"
		"\nVessel: TANTO SUBUR 1"
		"\nWaktu Tempuh: 2 Hari "
		"\nTarif: Rp2500000/tue"
		"\n-------------------"
		"\n"
		"\nUntuk kembali ke menu pilihan POL ketik pol"]
		bot.reply_to(message, pilpdg)
	elif inp == "sibolga":
		pilsblg = ["--- Untuk pelabuhan muat Sibolga ---"
		"\n"
		"\n-------------------"
		"\nHari: Kamis"
		"\nVessel: TANTO BERSATU"
		"\nWaktu Tempuh: 2 Hari "
		"\nTarif: Rp8000000/tue"
		"\n-------------------"
		"\n"
		"\nUntuk kembali ke menu pilihan POL ketik pol"]
		bot.reply_to(message, pilsblg)
	elif inp == "perawang":
		pilprwg = ["--- Untuk pelabuhan muat Perawang ---"
		"\n"
		"\n-------------------"
		"\nHari: Kamis"
		"\nVessel: TANTO MANIS"
		"\nWaktu Tempuh: 3 Hari "
		"\nTarif: Rp5000000/tue"
		"\n-------------------"
		"\n"
		"\nUntuk kembali ke menu pilihan POL ketik pol"]
		bot.reply_to(message, pilprwg)
	elif inp == "balikpapan":
		pilblkppn = ["--- Untuk pelabuhan muat Balikpapan ---"
		"\n"
		"\n-------------------"
		"\nHari: Minggu"
		"\nVessel: TANTO KAWAN"
		"\nWaktu Tempuh: 7 Hari "
		"\nTarif: Rp3000000/tue"
		"\n-------------------"
		"\n"
		"\nUntuk kembali ke menu pilihan POL ketik pol"]
		bot.reply_to(message, pilblkppn)
	elif inp == "balikpapan2":
		pilblkppn2 = ["--- Untuk pelabuhan muat Balikpapan ---"
		"\n"
		"\n-------------------"
		"\nHari: Sabtu"
		"\nVessel: TANTO SUBUR 2"
		"\nWaktu Tempuh: 2 Hari "
		"\nTarif: Rp1500000/tue"
		"\n-------------------"
		"\n"
		"\nUntuk kembali ke menu pilihan POL ketik pol"]
		bot.reply_to(message, pilblkppn2)
	elif inp == "bitung":
		pilbtg = ["--- Untuk pelabuhan muat Bitung ---"
		"\n"
		"\n-------------------"
		"\nHari: Sabtu"
		"\nVessel: TANTO SALAM"
		"\nWaktu Tempuh: 7 Hari "
		"\nTarif: Rp3500000/tue"
		"\n-------------------"
		"\n"
		"\nUntuk kembali ke menu pilihan POL ketik pol"]
		bot.reply_to(message, pilbtg)
	elif inp == "sorong":
		pilsrg = ["--- Untuk pelabuhan muat Sorong ---"
		"\n"
		"\n-------------------"
		"\nHari: Minggu"
		"\nVessel: TANTO RAYA"
		"\nWaktu Tempuh: 5 Hari "
		"\nTarif: Rp4500000/tue"
		"\n-------------------"
		"\n"
		"\nUntuk kembali ke menu pilihan POL ketik pol"]
		bot.reply_to(message, pilsrg)
	elif inp == "bitung2":
		pilbtg2 = ["--- Untuk pelabuhan muat Bitung ---"
		"\n"
		"\n-------------------"
		
		"\nHari: Selasa"
		"\nVessel: TANTO TANGGUH 2"
		"\nWaktu Tempuh: 6 Hari "
		"\nTarif: Rp3500000/tue"
		"\n-------------------"
		"\nHari: Kamis"
		"\nVessel: TANTO SEJAHTERA 2"
		"\nWaktu Tempuh: 6 Hari "
		"\nTarif: Rp3500000/tue"
		"\n-------------------"
		"\nHari: Jumat"
		"\nVessel: TANTO JAYA"
		"\nWaktu Tempuh: 6 Hari "
		"\nTarif: Rp3500000/tue"
		"\n-------------------"
		"\n"
		"\nUntuk kembali ke menu pilihan POL ketik pol"]
		bot.reply_to(message, pilbtg2)
	elif inp == "benete":
		pilbnt = ["--- Untuk pelabuhan muat Benete ---"
		"\n"
		"\n-------------------"
		"\nHari: Sabtu"
		"\nVessel: LUMOSO BAHAGIA"
		"\nWaktu Tempuh: 2 Hari "
		"\nTarif: Rp1000000/tue"
		"\n-------------------"
		"\n"
		"\nUntuk kembali ke menu pilihan POL ketik pol"]
		bot.reply_to(message, pilbnt)
	elif inp == "medan2":
		pilmdn2 = ["--- Untuk pelabuhan muat Medan ---"
		"\n"
		"\n-------------------"
		"\nHari: Jumat"
		"\nVessel: MERATUS MAMIRI"
		"\nWaktu Tempuh: 5 Hari "
		"\nTarif: Rp3000000/tue"
		"\n-------------------"
		"\n"
		"\nUntuk kembali ke menu pilihan POL ketik pol"]
		bot.reply_to(message, pilmdn2)
	elif inp == "lembar":
		pillmbr = ["--- Untuk pelabuhan muat Lembar ---"
		"\n"
		"\n-------------------"
		"\nHari: Sabtu"
		"\nVessel: LUMOSO BAHAGIA"
		"\nWaktu Tempuh: 4 Hari "
		"\nTarif: Rp2800000/tue"
		"\n-------------------"
		"\n"
		"\nUntuk kembali ke menu pilihan POL ketik pol"]
		bot.reply_to(message, pillmbr)
	elif inp == "luwuk":
		pillwk = ["--- Untuk pelabuhan muat Luwuk ---"
		"\n"
		"\n-------------------"
		"\nHari: Rabu"
		"\nVessel: LUMOSO GEMBIRA"
		"\nWaktu Tempuh: 4 Hari "
		"\nTarif: Rp5600000/tue"
		"\n-------------------"
		"\n"
		"\nUntuk kembali ke menu pilihan POL ketik pol"]
		bot.reply_to(message, pillwk)
	elif inp == "gorontalo anggrek":
		pilgtlagk = ["--- Untuk pelabuhan muat Gorontalo Anggrek ---"
		"\n"
		"\n-------------------"
		"\nHari: Rabu"
		"\nVessel: TANTO SALAM 2"
		"\nWaktu Tempuh: 7 Hari "
		"\nTarif: Rp4200000/tue"
		"\n-------------------"
		"\nHari: Minggu"
		"\nVessel: TANTO TERANG 2"
		"\nWaktu Tempuh: 7 Hari "
		"\nTarif: Rp4200000/tue"
		"\n-------------------"
		"\n"
		"\nUntuk kembali ke menu pilihan POL ketik pol"]
		bot.reply_to(message, pilgtlagk)
	elif inp == "ambon":
		pilabn = ["--- Untuk pelabuhan muat Ambon ---"
		"\n"
		"\n-------------------"
		"\nHari: Sabtu"
		"\nVessel: TANTO SIAP 2"
		"\nWaktu Tempuh: 6 Hari "
		"\nTarif: Rp2000000/tue"
		"\n-------------------"
		"\n"
		"\nUntuk kembali ke menu pilihan POL ketik pol"]
		bot.reply_to(message, pilabn)
	elif inp == "kendari":
		pilkndr= ["--- Untuk pelabuhan muat Kendari ---"
		"\n"
		"\n-------------------"
		"\nHari: Jumat"
		"\nVessel: TANTO REJEKI"
		"\nWaktu Tempuh: 6 Hari "
		"\nTarif: Rp3500000/tue"
		"\n-------------------"
		"\n"
		"\nUntuk kembali ke menu pilihan POL ketik pol"]
		bot.reply_to(message, pilkndr)				
	elif inp == "samarinda2":
		pilsmrnd2 = ["--- Untuk pelabuhan muat Samarinda ---"
		"\n"
		"\n-------------------"
		"\nHari: Senin"
		"\nVessel: TANTO LUAS"
		"\nWaktu Tempuh: 2 Hari "
		"\nTarif: Rp2000000/tue"
		"\n-------------------"
		"\nHari: Jumat"
		"\nVessel: MERATUS KARIMATA"
		"\nWaktu Tempuh: 2 Hari"
		"\nTarif: Rp2000000/tue"
		"\n-------------------"
		"\n"
		"\nUntuk kembali ke menu pilihan POL ketik pol"]
		bot.reply_to(message, pilsmrnd2)
	elif inp == "ternate":
		piltrnt= ["--- Untuk pelabuhan muat Ternate ---"
		"\n"
		"\n-------------------"
		"\nHari: Minggu"
		"\nVessel: TANTO HANDAL"
		"\nWaktu Tempuh: 5 Hari "
		"\nTarif: Rp9100000/tue"
		"\n-------------------"
		"\n"
		"\nUntuk kembali ke menu pilihan POL ketik pol"]
		bot.reply_to(message, piltrnt)
	if inp == 'pesan':
		orderpesan = ["Silahkan order : (Ketik nama vessel saja)"
		"\n"
		"\nMisalkan : "
		"\nUser : TANTO SUBUR"
		"\nTANTO : Berapa tue?"]
		bot.reply_to(message, orderpesan)
		tag = "Berapa tue?"
	else:
		if inp == "info":
			info = ["TANTO adalah perusahaan yang telah berdiri sejak 1971'."
			"\nMeskipun bermula dari sebuah perusahaan dengan skala yang sangat kecil. Saat ini, TANTO memiliki armada kapal berjumlah 50 kapal kontainer dengan total kapasitas 26.731 TEUs"
			"\n"
			"\nUntuk kembali ke menu utama ketik menu"]
			bot.reply_to(message, info)
		elif inp == "jadwal":
			pol = ["--- Untuk melihat pilihan pelabuhan muat ---"
			"\n"
			"\nKetik jkt untuk melihat jadwal pelabuhan jakarta."
			"\nKetik sby untuk melihat jadwal pelabuhan surabaya."
			"\n"
			"\nUntuk kembali ke menu utama ketik menu"]
			bot.reply_to(message, pol)
		elif inp == "mulai":
			pembuka = ["Selamat Datang di TANTO!"
			"\n"
			"\nKetik info untuk informasi mengenai TANTO."
			"\nKetik jadwal untuk pilihan jadwal."
			"\nKetik pesan untuk memesan"]
			bot.reply_to(message, pembuka)
		elif inp == "menu":
			pembuka1 = ["Selamat Datang di TANTO!"
			"\n"
			"\nKetik info untuk informasi mengenai TANTO."
			"\nKetik jadwal untuk pilihan jadwal."
			"\nKetik pesan untuk memesan"]
			bot.reply_to(message, pembuka1)
		elif inp == "pol":
			pol1 = ["--- Untuk melihat pilihan pelabuhan muat ---"
			"\n"
			"\nKetik jkt untuk melihat jadwal pelabuhan jakarta."
			"\nKetik sby untuk melihat jadwal pelabuhan surabaya."
			"\n"
			"\nUntuk kembali ke menu utama ketik menu"]
			bot.reply_to(message, pol1)
bot.polling()