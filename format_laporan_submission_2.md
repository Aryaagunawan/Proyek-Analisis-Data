# Laporan Proyek Machine Learning - Syifa Azzahro

## Domain Proyek

Musik merupakan elemen yang tidak terpisahkan dari kehidupan manusia, karena berasal dari suara yang menjadi partikel pembentuk alam semesta (Grimonia, 2023). Musik hadir di setiap aspek kehidupan dan menjadi bentuk hiburan yang sangat dibutuhkan oleh sebagian besar orang. Mendengarkan musik dipercaya mampu memberikan ketenangan, terlebih jika sesuai dengan preferensi atau suasana hati pendengarnya.

Seiring perkembangan teknologi dan meningkatnya konsumsi konten digital, berbagai perusahaan mengembangkan platform streaming musik seperti Spotify, Joox, LangitMusik, dan Pandora untuk memenuhi kebutuhan tersebut. Namun, banyaknya pilihan lagu dan genre membuat pengguna seringkali bingung menentukan lagu yang ingin didengarkan. Di sinilah peran sistem rekomendasi menjadi penting, yaitu untuk memprediksi dan menyajikan daftar lagu yang paling relevan bagi pengguna.

Sistem rekomendasi dapat meningkatkan pengalaman pengguna dengan memanfaatkan data seperti preferensi lagu, riwayat pemutaran, hingga konten lagu itu sendiri. Salah satu pendekatan yang digunakan adalah Content-based Filtering, yaitu metode yang merekomendasikan lagu berdasarkan kesamaan konten lagu, baik dari sisi fitur musik (seperti tempo, energy, dan danceability) maupun dari sisi judul lagu. Dalam hal ini, TF-IDF (Term Frequency-Inverse Document Frequency) digunakan untuk menghitung bobot tiap kata dalam judul lagu, dan Cosine Similarity diterapkan untuk mengukur kemiripan antar lagu berdasarkan fitur musik dan judul lagu.

Dengan pendekatan ini, sistem mampu menghasilkan 10 rekomendasi lagu teratas yang relevan dengan preferensi pengguna. Hasil pengujian menunjukkan performa sistem yang sangat baik dengan tingkat akurasi yang tinggi, menunjukkan relevansi rekomendasi berdasarkan analisis kesamaan konten lagu.

  
  Referensi: 
  [Sistem Rekomendasi Musik Menggunakan Machine Learning](https://ojs.adzkia.ac.id/index.php/jtech/article/view/282/168) 

  [SISTEM REKOMENDASI LAGU DENGAN METODE CONTENT-BASED FILTERING BERBASIS WEBSITE](https://repository.telkomuniversity.ac.id/pustaka/files/175506/jurnal_eproc/sistem-rekomendasi-lagu-dengan-metode-content-based-filtering-berbasis-website.pdf)



## Business Understanding

Lagu merupakan media hiburan yang sangat diminati dan sering dipilih berdasarkan suasana hati maupun preferensi pribadi. Namun, karena jumlah lagu yang tersedia sangat banyak dan genre yang beragam, pengguna kerap mengalami kesulitan dalam menentukan lagu mana yang ingin didengarkan. Hal ini menjadi tantangan tersendiri bagi platform streaming musik dalam memberikan pengalaman yang personal dan relevan bagi setiap penggunanya.

Salah satu solusi untuk meningkatkan kepuasan pengguna adalah dengan membangun sistem rekomendasi lagu yang dapat menyesuaikan preferensi masing-masing individu. Dengan memanfaatkan teknologi seperti pembelajaran mesin dan teknik pemrosesan bahasa alami (NLP), sistem dapat menganalisis lirik lagu untuk menemukan kesamaan konten dan merekomendasikan lagu-lagu yang mirip.


### Problem Statements

- Bagaimana meningkatkan pengalaman pengguna dalam menemukan lagu yang relevan dengan preferensi mereka, sehingga meningkatkan kepuasan dan retensi pengguna?



### Goals

- Membangun sistem rekomendasi berbasis konten (content-based filtering) yang dapat memberikan rekomendasi lagu sesuai dengan kesamaan fitur konten musik, sehingga pengguna mendapatkan rekomendasi yang relevan dengan preferensinya.


### Solution statements
Menerapan sistem rekomendasi berbasis Content-Based Filtering menggunakan TF-IDF untuk memproses fitur deskriptif lagu, lalu mengukur kemiripan lagu dengan Cosine Similarity. 


## Data Understanding
Dataset yang digunakan adalah [30000 Spotify Songs](https://www.kaggle.com/datasets/joebeachcapital/30000-spotify-songs). dari Kaggle. Dataset terdiri dari 32833 baris dan 23 kolom. Berdasarkan eksplorasi awal, tipe data setiap kolom sudah sesuai dan terdapat missing value yang akan ditangani pada tahap data preparation.
 

### Variabel-variabel pada Restaurant UCI dataset adalah sebagai berikut:
- track_id: id unik untuk setiap lagu.

- track_name : judul lagu.

- track_artist : artis yang menyanyikan lagu tersebut.

- track_popularity : popularitas lagu dalam skala 1-100.

- track_album_id : id unik dari album tempat lagu dirilis.

- track_album_name : nama album.

- track_album_release_date : tanggal perilisan album.

- playlist_name : nama playlist tempat lagu tersebut berada.

- playlist_id : id unik dari playlist.

- playlist_genre : genre playlist.

- playlist_subgenre : sub-genre dari playlist.

- danceability : seberapa cocok lagu untuk berdansa, berdasarkan kombinasi elemen musikal seperti tempo, kestabilan ritme, kekuatan beat, dan keteraturan keseluruhan. Nilai 0.0 paling tidak cocok dan 1.0 paling cocok.

- energy : mengukur tingkat intensitas dan aktivitas lagu secara perseptual. Nilai 1.0 menunjukkan lagu cepat, keras, dan bising. Nilai ini dipengaruhi oleh dinamika, kekerasan suara, timbre, dan entropi umum.

- key : kunci musik utama dari lagu (mengacu ke pitch class: 0 = C, 1 = C♯/D♭, 2 = D, dst). Nilai -1 berarti tidak terdeteksi.

- loudness : tingkat kekerasan suara secara keseluruhan dalam satuan desibel (dB). Biasanya berada di kisaran -60 hingga 0 dB. Nilai ini merepresentasikan kekuatan fisik dari suara.

- mode : modus musik lagu: 1 = mayor, 0 = minor.

- speechiness : Mengukur seberapa banyak elemen ucapan/spoken word dalam lagu. Nilai > 0.66 mengindikasikan lagu kemungkinan besar terdiri dari kata-kata, sedangkan < 0.33 kemungkinan besar hanya musik.

- acousticness : Mengukur tingkat ke-akustikan sebuah lagu. Nilai 1.0 menunjukkan keyakinan tinggi bahwa lagu bersifat akustik.

- instrumentalness : Probabilitas bahwa sebuah lagu tidak mengandung vokal. Nilai mendekati 1.0 berarti lagu kemungkinan besar adalah instrumental.

- liveness : Mengindikasikan kemungkinan keberadaan audiens dalam rekaman. Nilai > 0.8 mengindikasikan bahwa lagu kemungkinan besar direkam secara live.

- valence : Menggambarkan positiveness atau mood dari lagu. Nilai tinggi menunjukkan lagu ceria/gembira, sedangkan nilai rendah cenderung sedih/depresif.

- tempo : Tempo rata-rata lagu dalam beat per menit (BPM).

- duration_ms : Durasi lagu dalam satuan milidetik.


## Data Preparation
Tahapan data preparation dilakukan untuk memastikan bahwa data siap digunakan oleh model machine learning dan menghasilkan performa yang optimal. Beberapa langkah yang dilakukan pada tahap ini meliputi:

1. **Menangani missing value**
    Terdapat masing-masing 5 data yang hilang pada kolom track_name, track_artist, track_album_name. Karena jumlahnya sangat sedikit dan dianggap tidak signifika, baris-baris tersebut dihapus untuk menjaga kualitas dan konsistensi data.


2. **Menangani data duplikat**
    Duplikasi dihapus berdasarkan track_id yang bersifat unik, untuk menghindari hasil rekomendasi yang redundan. Duplikat pada kolom lain seperti track_name atau track_album_name tidak dihapus karena dapat menyebabkan hilangnya data penting dan mengganggu performa model.

3. **Memilih fitur**
    Fitur utama yang digunakan adalah track_name, karena pendekatan yang digunakan berbasis konten (content-based filtering) dengan memanfaatkan kemiripan antar judul lagu. Fitur-fitur lain yang dipilih: danceability, energy, loudness, speechiness, acousticness, instrumentalness, liveness, valence, tempo, dan track_popularity.
    

4. **Normalisasi fitur numerik**
    Fitur-fitur numerik dinormalisasi menggunakan teknik Min-Max Scaling untuk memastikan semua fitur berada pada skala yang sama dan tidak mendominasi hasil akhir saat dilakukan penggabungan vektor.

5. **Menerapkan TF-IDF pada kolom track_name**
    Kolom track_name diubah menjadi representasi vektor numerik menggunakan algoritma TF-IDF (Term Frequency-Inverse Document Frequency). Teknik ini menghitung bobot kata-kata dalam judul lagu berdasarkan frekuensi kemunculannya, memungkinkan model untuk mengenali kemiripan antar lagu berdasarkan teks judulnya.

6. **Menggabungkan fitur numerik dan TF-IDF**
    Vektor hasil TF-IDF dari track_name digabungkan dengan fitur numerik yang telah dinormalisasi. Gabungan ini membentuk representasi akhir setiap lagu yang akan digunakan pada tahap modeling.

## Modeling

1. **Content-based Filtering**

    Model sistem rekomendasi dibangun menggunakan pendekatan content-based filtering. Dalam pendekatan ini, sistem merekomendasikan lagu-lagu lain yang memiliki karakteristik serupa dengan lagu yang diberikan sebagai input.

    **Teknik yang digunakan**:

    - TF-IDF Vectorization: Untuk mengubah teks track_name menjadi representasi numerik.

    - Cosine Similarity: Untuk mengukur kemiripan antara lagu satu dengan lainnya berdasarkan vektor hasil TF-IDF.

    Sistem akan menghitung skor kesamaan antar lagu, lalu memilih lagu-lagu dengan nilai tertinggi sebagai hasil rekomendasi.

    **Kelebihan**:
    - Tidak memerlukan data pengguna atau interaksi pengguna sebelumnya.
    - Dapat memberikan rekomendasi meskipun lagu belum pernah diputar oleh siapa pun (cold start item).

    **Kekurangan**:
    - Rekomendasi cenderung terbatas pada konten yang mirip secara literal, seperti judul yang mirip, sehingga kurang variatif.

    - Tidak mempertimbangkan preferensi pengguna secara eksplisit karena hanya fokus pada karakteristik item.

    **Hasil top 10 recomendation**
    ![hasil](https://github.com/user-attachments/assets/eeef44c1-2fd3-444e-90f2-534d2ab3b59a)

    
## Evaluation

- **Precision@K** : proporsi item yang relevan di antara K rekomendasi teratas. Hal ini berfokus pada kualitas rekomendasi.

![precision@k](https://github.com/user-attachments/assets/363f0f74-9611-4454-9bd5-7ef6cded4165)


Bayangkan sebuah sistem rekomendasi musik merekomendasikan 10 lagu (K=10) kepada pengguna. Dari 10 lagu ini, pengguna menemukan 5 lagu yang relevan.

maka precision@10 = 5/10 = 0.5. Artinya 50% dari 10 lagu teratas yang direkomendasikan relevan bagi pengguna.

- **Recall@K**: mengukur kemampuan sistem rekomendasi untuk mengidentifikasi semua item yang relevan dalam rekomendasi K teratas. Hal ini berfokus pada kelengkapan sistem.

![recall@k](https://github.com/user-attachments/assets/28b91479-8b02-4e08-aee1-afc4fbe113e3)


Melanjutkan contoh sebelumnya, anggaplah ada total 7 yang relevan untuk pengguna. Dari jumlah tersebut, 5 di antaranya termasuk dalam 10 rekomendasi teratas.

maka recall@10 = 5/7 = 0.714. Artinya, 71,4% dari semua lagu yang relevan masuk dalam 10 rekomendasi teratas.

- **F-Score@K**: rata-rata harmonik dari presisi dan recall pada K. Ini memberikan metrik yang seimbang yang mempertimbangkan presisi dan recall.

![f-score@k](https://github.com/user-attachments/assets/3ca08130-661d-4761-a454-7e9b44c216f3)



F-score@10 = 2(0.5 x 0.714 / 0.5 + 0.714) = 2(0.357/1.214) = 0.588

F-Score@5 sekitar 0.588 ini mencerminkan keseimbangan antara presisi dan recall, memberikan metrik tunggal untuk mengevaluasi kinerja sistem rekomendasi.


<br />

## Kesimpulan

Seluruh proses analisis dan pemodelan yang telah dilakukan berhasil menjawab solution statement yang dirumuskan di awal, yaitu membangun sistem rekomendasi lagu berbasis content-based filtering untuk membantu pengguna menemukan lagu-lagu yang relevan dengan preferensi atau suasana hati mereka.

Tahapan eksplorasi dan pembersihan data memastikan bahwa data yang digunakan dalam sistem memiliki kualitas yang baik dan representatif. Implementasi metode TF-IDF berhasil mengubah judul lagu menjadi representasi numerik, sementara algoritma cosine similarity digunakan untuk mengukur kemiripan antar lagu. Hasil akhir sistem mampu menghasilkan rekomendasi 10 lagu teratas yang relevan dengan lagu input, baik secara semantik maupun emosi yang ditangkap dari judul.

Dengan demikian, sistem ini diharapkan dapat menjadi solusi awal yang efektif untuk membantu pengguna dalam menjelajahi koleksi lagu yang luas dan menemukan lagu-lagu yang sesuai dengan preferensi mereka, serta memberikan dasar bagi pengembangan sistem rekomendasi musik yang lebih kompleks di masa mendatang, seperti dengan menambahkan fitur lirik, genre, atau riwayat pemutaran pengguna.

