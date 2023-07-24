# About Data

Data ini diperoleh dengan teknik *scrapping* pada website [**Traveloka**](www.traveloka.com/). Data ini berbentuk sqlite yang berisikan 2 tabel bernama `hotel_yogyakarta` dan `hotel_room_yogyakarta`


## hotel_yogyakarta

Berikut detail column pada tabel `hotel_yogyakarta`.
**Dimensi (378, 12)**
- `id`: Unique id hotel
- `type`: Tipe penginapan
- `name`: Nama hotel
- `starRating`: Rating bintang hotel
- `builtYear`: Tahun dibuatnya hotel
- `description`: Deskripsi tentang hotel
- `link`: URL menuju halaman hotel di Traveloka
- `address`: Alamat hotel
- `city`: Kota hotel
- `image`: URL gambar hotel
- `facilities`: Daftar fasilitas pada hotel
- `nearestPointofInterests`:  Area populer / fasilitas umum disekitar hotel

## hotel_room_yogyakarta

Berikut detail column pada tabel `hotel_room_yogyakarta`.
**Dimensi (1199, 16)**
- `id`: Unique id hotel
- `hotelId`: Id hotel
- `roomType`: Tipe kamar hotel
- `description`: deskripsi kamar hotel
- `bedDescription`: deskripsi kasur kamar
- `size`: Ukuran kamar ($m^2$)
- `originalRate`: Harga kamar per malam
- `baseOccupancy`: Kapasitas kamar
- `maxChildAge`: Umur maksimal anak-anak
- `maxChildOccupancy`: Kapasitas kamar untuk anak-anak
- `numExtraBeds`: Jumlah kasur tambahan
- `isBreakfastIncluded`:  Fasilitas sarapan
- `isWifiIncluded`: Fasilitas WiFi
- `isRefundable`: Fasilitas refund
- `hasLivingRoom`: Fasilitas ruang keluarga
- `facilities`: Daftar fasilitas lainnya pada kamar