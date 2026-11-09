# Öğrenci Devamsızlık Takip Sistemi

Sistem Analizi ve Tasarım dersi kapsamında geliştirilmiş, sade ve anlaşılır bir **öğrenci devamsızlık takip web uygulamasıdır**. Öğretmenin günlük yoklama işlemlerini hızlı ve düzenli bir şekilde yapabilmesi, öğrenci listesini yönetebilmesi ve devamsızlık verilerini takip edebilmesi amacıyla tasarlanmıştır.

## Özellikler

- Yönetici girişi ve güvenli oturum yönetimi (Flask session + hash'lenmiş şifre)
- Öğrenci ekleme, listeleme ve pasife alma
- Öğrenci listesinde arama ve sınıf filtresi
- Günlük yoklama kaydı: **Var**, **Yok**, **Geç Kaldı** durumları
- Tarih bazlı yoklama görüntüleme, güncelleme ve not ekleme
- Anasayfa istatistikleri: toplam öğrenci, gün içi var/yok/geç kalan sayıları
- Yoklama kayıtlarını CSV olarak dışa aktarma
- SQLite tabanlı veri saklama (ek sunucu gerektirmez)
- Sağlık kontrolü endpoint'i (`/health`) ve otomatik testler

## Teknolojiler

| Katman     | Teknoloji                          |
| ---------- | ---------------------------------- |
| Backend    | Python, Flask                      |
| Veritabanı | SQLite                             |
| Şablon     | Jinja2                             |
| Arayüz     | HTML, CSS, JavaScript              |
| Güvenlik   | Werkzeug (password hashing), Flask session |

## Proje Yapısı

```text
SAT-2026-Kerim-Mert-Alkan/
├── app.py                      # Flask uygulaması ve rotalar
├── database.py                 # SQLite bağlantısı, şema ve seed verisi
├── requirements.txt            # Python bağımlılıkları
├── test_attendance_system.py   # Otomatik testler
├── README.md
├── .gitignore
├── static/
│   ├── css/style.css
│   └── js/main.js
└── templates/
    ├── base.html
    ├── login.html
    ├── dashboard.html
    ├── students.html
    ├── attendance.html
    └── ...
```

## Kurulum

1. Projeyi klonlayın:

   ```bash
   git clone https://github.com/Kerimmert1/SAT-2026-Kerim-Mert-Alkan.git
   cd SAT-2026-Kerim-Mert-Alkan
   ```

2. Sanal ortam oluşturun ve etkinleştirin:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   # source .venv/bin/activate   # macOS / Linux
   ```

3. Bağımlılıkları yükleyin:

   ```bash
   pip install -r requirements.txt
   ```

4. Uygulamayı çalıştırın:

   ```bash
   python app.py
   ```

5. Tarayıcıda açın:

   ```text
   http://127.0.0.1:5000/login
   ```

## Giriş Bilgileri

| Kullanıcı | Şifre     |
| --------- | --------- |
| `admin`   | `admin123` |

> **Not:** Bu bilgiler yalnızca geliştirme/test amaçlıdır. Üretim ortamında `SECRET_KEY` ortam değişkenini ve yönetici şifresini mutlaka değiştirin.

## Kullanım

- **Anasayfa (Dashboard):** Bugünkü yoklama özetini ve son kayıtları gösterir.
- **Öğrenciler:** Yeni öğrenci eklenir; öğrenci numarası benzersizdir. Öğrenci adına/numarasına göre arama ve sınıf filtresi yapılabilir.
- **Yoklama:** Tarih seçilip her öğrenci için durum (**Var** / **Yok** / **Geç Kaldı**) ve opsiyonel not girilir. Aynı öğrenci + tarih için kayıt güncellenir (tekrar yoklama yapılmaz).
- **Dışa Aktarma:** Seçilen tarihe ait yoklama kayıtları CSV dosyası olarak indirilebilir.

## API / Endpoint'ler

| Yöntem | Yol                          | Açıklama                                   |
| ------ | ---------------------------- | ------------------------------------------ |
| GET    | `/`                          | Giriş durumuna göre yönlendirme            |
| GET/POST | `/login`                   | Yönetici girişi                            |
| GET    | `/logout`                    | Oturumu kapatma                            |
| GET    | `/dashboard`                 | Anasayfa istatistikleri                    |
| GET    | `/students`                  | Öğrenci listesi (arama/filtre destekli)    |
| POST   | `/students/add`              | Yeni öğrenci ekleme                        |
| POST   | `/students/<id>/delete`      | Öğrenciyi pasife alma                      |
| GET    | `/attendance`                | Tarih bazlı yoklama kayıtları              |
| POST   | `/attendance/mark`           | Yoklama kaydı oluşturma/güncelleme         |
| GET    | `/attendance/export`         | Yoklama kayıtlarını CSV olarak indirme     |
| GET    | `/health`                    | Sağlık kontrolü (veritabanı dahil)         |

## Testler

```bash
pytest test_attendance_system.py
```

Testler izole bir veritabanı (`:memory:`) kullanır; mevcut verilerinize dokunmaz.

## Veritabanı

Uygulama SQLite kullanır. Varsayılan dosya:

```text
attendance_system.db
```

Tablolar:

- `admins` — yönetici hesapları (şifre hash'lenmiş)
- `students` — öğrenci bilgileri (`is_active` ile pasife alma)
- `attendance` — `(student_id, date)` benzersizliği ile günlük yoklama kayıtları

## Amaç ve Hedefler

Bu proje, sistem analizi ve tasarım dersi kapsamında; öğretmenin her gün öğrencilerin yoklama durumunu tek bir sistem üzerinden kontrol etmesi, yeni öğrencileri kaydetmesi ve devamsızlık bilgilerini düzenli takip edebilmesi hedefiyle hazırlanmıştır. Gereksiz ve karmaşık özelliklerden arındırılarak yalnızca temel işlevlere odaklanılmış; böylece kullanım kolaylığı artırılmış ve proje sunuma uygun sade bir örnek çalışma haline getirilmiştir.

Temel hedefler:

- Öğrenci ve yoklama verilerini güvenli ve düzenli saklamak
- Günlük yoklama kayıtlarını doğru ve hızlı tutmak
- Temel istatistikleri (var/yok/geç kaldı) tek bakışta göstermek
- Sistemi küçük ölçekli tutarak temel yazılım geliştirme süreçlerini anlaşılır kılmak

## Yöntem

Proje **Flask** web framework'ü ile geliştirilmiştir; hafif yapısı ve hızlı geliştirme imkânı sayesinde bu tür bir öğrenci yoklama sistemi için uygun bir tercihtir. İş mantığı **Python** ile yazılmış, veri katmanında ek sunucu kurulumu gerektirmeyen **SQLite** kullanılmıştır.

Sistem şu bileşenlerden oluşur:

- **Giriş ekranı** — hash'lenmiş şifre ile yönetici doğrulaması
- **Dashboard** — günlük özet istatistikler ve son yoklama kayıtları
- **Öğrenci yönetimi** — öğrenci ekleme, listeleme, arama/filtreleme ve pasife alma
- **Yoklama ekranı** — tarih bazlı durum girişi (`Var` / `Yok` / `Geç Kaldı`) ve not
- **Dışa aktarma** — CSV formatında raporlama

Her öğrenci için tek kayıt tutulur; `(öğrenci, tarih)` çifti benzersizdir, böylece aynı gün tekrar giriş yapıldığında kayıt güncellenir. Arayüz sade tutulmuş, ana işlevler öne çıkarılmıştır.

## Lisans

Bu proje eğitim ve akademik amaçlar için geliştirilmiştir.
