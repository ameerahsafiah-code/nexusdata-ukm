import asyncio
from playwright.async_api import async_playwright
import pandas as pd
import ai_handler  # Pastikan fail ai_handler.py ada dalam folder yang sama
import os

async def main():
    async with async_playwright() as p:
        print("\n🚀 NexusData UKM: Memulakan Bot Pengumpul Data...")
        
        # headless=True supaya browser berjalan di belakang tabir
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        semua_data = []
        current_page = 1
        muka_surat_maksimum = 3  # Kita ambil 3 muka surat sebagai permulaan

        try:
            await page.goto("https://books.toscrape.com/", timeout=60000)
            
            while current_page <= muka_surat_maksimum:
                try:
                    print(f"📄 Memproses Muka Surat {current_page}...")
                    
                    # Tunggu elemen tajuk muncul
                    await page.wait_for_selector("h3 a", timeout=10000)
                    
                    elements_judul = await page.query_selector_all("h3 a")
                    elements_harga = await page.query_selector_all(".price_color")

                    for i in range(len(elements_judul)):
                        judul = await elements_judul[i].get_attribute("title")
                        harga_mentah = await elements_harga[i].inner_text()
                        # Bersihkan simbol mata wang
                        harga_bersih = harga_mentah.replace("£", "").replace("Â", "")
                        semua_data.append([judul, float(harga_bersih)])

                    # Cari dan klik butang 'Next'
                    next_button = await page.query_selector(".next a")
                    if next_button and current_page < muka_surat_maksimum:
                        await next_button.click()
                        current_page += 1
                        await asyncio.sleep(1) # Rehat sekejap
                    else:
                        break
                        
                except Exception as e:
                    print(f"⚠️ Gangguan pada muka surat {current_page}: {e}")
                    break # Berhenti dan selamatkan data sedia ada

        except Exception as e:
            print(f"❌ Ralat kritikal: {e}")

        finally:
            # 1. Simpan ke CSV (Supaya Dashboard boleh baca jadual)
            if semua_data:
                df = pd.DataFrame(semua_data, columns=['Tajuk Buku', 'Harga (GBP)'])
                df.to_csv('data_buku_besar.csv', index=False)
                print(f"✅ Berjaya menyimpan {len(semua_data)} data ke 'data_buku_besar.csv'")

                # 2. Proses Analisis AI
                print("🤖 Menghantar sampel data ke AI untuk rumusan...")
                try:
                    # Ambil 5 baris pertama sebagai sampel untuk AI
                    sampel_ai = "\n".join([f"{d[0]}: £{d[1]}" for d in semua_data[:5]])
                    laporan_ai = ai_handler.tanya_ai(sampel_ai)
                    
                    # Simpan laporan AI ke fail teks (Supaya Dashboard boleh baca)
                    with open('laporan_ai.txt', 'w', encoding='utf-8') as f:
                        f.write(laporan_ai)
                    print("✅ Rumusan AI berjaya dijana dan disimpan!")
                except Exception as ai_err:
                    print(f"⚠️ Gagal menjana rumusan AI: {ai_err}")
            
            await browser.close()
            print("🏁 Operasi tamat secara selamat.")

if __name__ == "__main__":
    asyncio.run(main())