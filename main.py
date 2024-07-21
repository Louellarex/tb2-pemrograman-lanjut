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
         judul="Mariane",
        penulis="Risa Saraswati",
        penerbit="PT. Bukune Kreatif Cipta",
        tahun_terbit=2020,
        konten="Cerita Marianne Charlotte van Dziburg",
        ikhtisar="Novel ini menceritakan tentang kehidupan masa lalu seorang gadis nakal, jahil namun cantik yang hidup di zaman penjajahan Belanda"
    )


    post_buku(buku1)

    buku_dari_db = get_buku("Mariane")
    if buku_dari_db:
        print(buku_dari_db)
        print(buku_dari_db.read(3))