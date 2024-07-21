#Rafli Maulana Putra
#41823010058

import mysql.connector
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Buku:
    def __init__(self, judul, penulis, penerbit, tahun_terbit, konten, ikhtisar):
        self.judul = judul
        self.penulis = penulis
        self.penerbit = penerbit
        self.tahun_terbit = tahun_terbit
        self.konten = konten
        self.ikhtisar = ikhtisar

    def read(self, halaman):
        konten_list = self.konten.split(', ')
        if halaman > len(konten_list):
            return "Halaman tidak tersedia"
        return konten_list[:halaman]

    def __str__(self):
        return f"{self.judul} by {self.penulis}"
 

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1mercumeruya",
        database="perpustakaan"
    )


def post_buku(buku):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO buku (judul, penulis, penerbit, tahun_terbit, konten, ikhtisar)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (buku.judul, buku.penulis, buku.penerbit, buku.tahun_terbit, buku.konten, buku.ikhtisar))
        conn.commit()
        logger.info("Buku berhasil disimpan")
    except mysql.connector.Error as err:
        logger.error(f"Error: {err}")
        raise HTTPException(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()


def get_buku(judul):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM buku WHERE judul = %s", (judul,))
        result = cursor.fetchone()
        if result:
            buku = Buku(
                judul=result['judul'],
                penulis=result['penulis'],
                penerbit=result['penerbit'],
                tahun_terbit=result['tahun_terbit'],
                konten=result['konten'],
                ikhtisar=result['ikhtisar']
            )
            logger.info("Buku berhasil diambil")
            return buku
        else:
            logger.warning("Buku tidak ditemukan")
            return None
    except mysql.connector.Error as err:
        logger.error(f"Error: {err}")
        raise HTTPException(f"Error: {err}")
    finally:
        cursor.fetchall()
        cursor.close()
        conn.close()


class HTTPException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


if __name__ == "__main__":
    buku1 = Buku(
         judul="Wuthering Heights",
        penulis="Emily Brontë",
        penerbit="Gramedia Pustaka Utama",
        tahun_terbit=2016,
        konten="Chapter 1 A Visit to  Wuthering Heights, Chapter 2 A Singular Family, Chapter 3 The Ghost at the Window, Chapter 4 Arrival of a Foundling, Chapter 5 The Death of Mr Earnshaw, Chapter 6 New Acquaintances, Chapter 7 Catherine Becomes a Lady, Chapter 8 The Disintegration of the Earnshaws, Chapter 9 The Disappearance of Heathcliff, Chapter 10 Mr Heathcliff Returns, Chapter 11 The Milk-Blooded Coward, Chapter 12 Delirium, Chapter 13 Isabella Learns Her Fate, Chapter 14 The Mediator, Chapter 15 The Final Meeting, Chapter 16 Life and Death, Chapter 17 The Master of Wuthering Heights, Chapter 18 The Explorer, Chapter 19 A Sickly Child, Chapter 20 Father and Son, Chapter 21 Young Love, Chapter 22 An Invitation from Heathcliff, Chapter 23 The Wiles of Linton, Chapter 24 Deeper In, Chapter 25 Mr Linton Considers the Future, Chapter 26 An Ominous Meeting, Chapter 27 Prisoners, Chapter 28 The Last of the Lintons, Chapter 29 Heathcliff Triumphant, Chapter 30 Catherine Alone, Chapter 31 Mr Lockwood Takes His Leave, Chapter 32 Many Changes, Chapter 33 The Haunted Soul, Chapter 34 Unions",
        ikhtisar="Wuthering Heights merupakan novel karangan. Sejak awal dirilis pada tahun 1847, novel ini telah mengundang banyak kontroversi. Ceritanya sendiri berkisar tentang cinta dan balas dendam. Adalah Heathcliff, anak yang ditemukan di jalan oleh Mr. Earnshaw dan dibawanya pulang ke rumahnya di Wuthering Heights. Namun, kehadiran Heathcliff tidak disambut baik oleh keluarga Mr. Earnshaw. Ketika Mr. Earnshaw meninggal, Heathcliff mendapat perlakuan tidak adil oleh anak-anak Earnshaw. Tetapi, tak seperti Hindley, Catherine justru mulai akrab dengan Heathcliff."
    )


    post_buku(buku1)

    buku_dari_db = get_buku("Wuthering Heights")
    if buku_dari_db:
        print(buku_dari_db)
        print(buku_dari_db.read(3))