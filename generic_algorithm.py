import time
from collections import namedtuple
from functools import partial
from random import choices, randint, randrange, random
from typing import List, Callable, Tuple

Barang = List[int]
BanyakBarang = List[Barang]
FungsiOptimal = Callable[[Barang],int]
FungsiBanyakBarang = Callable[[],BanyakBarang]
FungsiSeleksi = Callable[[BanyakBarang,FungsiOptimal],Tuple[Barang,Barang]]
FungsiCrossover = Callable[[Barang,Barang], Tuple[Barang,Barang]]
FungsiMutasi = Callable[[Barang],Barang]
Benda = namedtuple('Benda',['nama','bobot_kepentingan','harga'])

benda = [
    Benda('Tenda',2,850000),
    Benda('Sleeping Bag',3,400000),
    Benda('Jaket',5,300000),
    Benda('Ransel',5,500000),
    Benda('Sepatu',4,700000),
    Benda('Jas Hujan',1,150000),
    Benda('Alat Masak',2,400000),
    Benda('P3K',3,300000),
    Benda('Topi',1,150000),
    Benda('Trousers',2,250000),
    Benda('Botol Minum',2,150000),
    Benda('T-shirt',1,150000),
    Benda('Kemeja',1,300000),
    Benda('Kacamata',1,200000),
    Benda('Kaos tangan',2,200000),
    Benda('Jam tangan',1,500000),
]


def inisiasi_barang(panjang: int) -> Barang:
    return choices([0,1],k = panjang)

def inisiasi_banyakbarang(ukuran: int, panjang_barang: int) -> BanyakBarang:
    return [inisiasi_barang(panjang_barang) for _ in range(ukuran)]

def optimal(barang: Barang, benda: [Benda], harga_maksimal: int) -> int:
    if len(barang) != len(benda):
        raise ValueError("Kudu sama")
    harga = 0
    bobot_kepentingan = 0

    for i, benda in enumerate(benda):
        if barang[i] == 1:
            harga += benda.harga
            bobot_kepentingan += benda.bobot_kepentingan

            if harga > harga_maksimal:
                return 0

    return bobot_kepentingan

def seleksi_pasangan(banyak_barang: BanyakBarang,fungsi_optimal: FungsiOptimal) -> BanyakBarang:
    return choices(
        population = banyak_barang,
        weights=[fungsi_optimal(barang) for barang in banyak_barang],
        k = 2
    )

def crossover(a: Barang, b: Barang) -> Tuple[Barang,Barang]:
    if len(a) != len(b):
        raise ValueError("a dan b harus sama panjang")
    panjang = len(a)
    if panjang < 2:
        return a,b
    p = randint(1, panjang - 1)
    return a[0:p] + b[p:], b[0:p] + a[p:]

def mutasi(barang: Barang, num: int = 1, kemungkinan: float = 0.5) -> Barang:
    for _ in range(num):
        index = randrange(len(barang))
        barang[index] = barang[index] if random() > kemungkinan else abs(barang[index] - 1)
    return barang

def evolusi(
        fungsi_banyak_barang: FungsiBanyakBarang,
        fungsi_optimal: FungsiOptimal,
        batas_optimal: int,
        fungsi_seleksi: FungsiSeleksi = seleksi_pasangan,
        fungsi_crossover: FungsiCrossover = crossover,
        fungsi_mutasi: FungsiMutasi = mutasi,
        batas_generasi: int = 100,
) -> Tuple[BanyakBarang,int,int]:
    banyak_barang = fungsi_banyak_barang()

    for i in range(batas_generasi):
        banyak_barang = sorted(
            banyak_barang,
            key=lambda  barang: fungsi_optimal(barang),
            reverse = True
        )



        if fungsi_optimal(banyak_barang[0]) >= batas_optimal:
            break

        generasi_selanjutnya = banyak_barang[0:2]

        for j in range(int(len(banyak_barang) / 2) -1 ):
            induk = fungsi_seleksi(banyak_barang,fungsi_optimal)
            a,b = fungsi_crossover(induk[0],induk[1])
            a = fungsi_mutasi(a)
            b = fungsi_mutasi(b)
            generasi_selanjutnya += [a,b]

        banyak_barang = generasi_selanjutnya

    banyak_barang = sorted(
        banyak_barang,
        key=lambda barang: fungsi_optimal(barang),
        reverse=True
    )

    return  banyak_barang, i

start = time.time()
banyak_barang, generasi = evolusi(
    fungsi_banyak_barang=partial(
        inisiasi_banyakbarang, ukuran=10, panjang_barang = len(benda)
    ),
    fungsi_optimal=partial(
        optimal, benda = benda, harga_maksimal = 2000000
    ),
    batas_optimal=21,
    batas_generasi=100
)
end = time.time()

def barang_ke_benda(barang: Barang, benda: [Benda]) -> Tuple[Benda, int, int]:
    result = []
    total_harga = 0
    total_bobot = 0
    for i, benda in enumerate(benda):
        if barang[i] == 1:
            result += [benda.nama]
            total_harga += int(benda.harga)
            total_bobot += int(benda.bobot_kepentingan)
    return result ,total_harga , total_bobot

print(generasi)
print(end - start)
print(barang_ke_benda(banyak_barang[0],benda))



