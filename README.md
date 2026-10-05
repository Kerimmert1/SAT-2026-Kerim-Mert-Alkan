# Öğrenci Devamsızlık Takip Sistemi

Sistem analizi ve tasarım dersi için hazırlanmış, sade ve anlaşılır bir öğrenci devamsızlık takip uygulamasıdır. Bu proje, öğretmenin gün içinde öğrencilerin yoklama durumunu hızlı ve düzenli bir şekilde kaydetmesini, öğrenci listesini yönetmesini ve devamsızlık bilgilerini takip etmesini amaçlar. Gereksiz özelliklerden arındırılmış bir yapıya sahip olması sayesinde hem öğrenme sürecine uygun hem de kullanımı kolay bir uygulama olarak tasarlanmıştır.

## Proje Hakkında

Bu sistem, okul veya ders ortamında kullanılabilecek temel bir yoklama yönetim çözümüdür. Öğretmen, kullanıcı girişi ile sisteme erişerek öğrenci ekleyebilir, yeni ders veya gün için yoklama kaydı oluşturabilir ve her öğrencinin durumunu "Var", "Yok" veya "Geç Kaldı" şeklinde işleyebilir. Tüm veriler yerel SQLite veritabanında saklanır; bu sayede ek bir sunucu kurulumu gerektirmez ve proje daha hafif bir yapıya sahip olur. Ayrıca uygulama arayüzü sade tutulmuş, ana işlevler öne çıkarılmıştır.

## Özellikler

- Yönetici girişi ve güvenli oturum yönetimi
- Öğrenci ekleme ve listeleme
- Günlük yoklama kaydı
- Devamsızlık ve geç kalma takibi
- Anasayfa görünümünde toplam öğrenci ve durum istatistikleri
- SQLite tabanlı veri saklama
- Basit ve anlaşılır kullanıcı arayüzü

## Teknolojiler

- Python
- Flask
- SQLite
- Jinja2
- HTML / CSS / JavaScript

## Kurulum

1. Proje klasörüne gidin:
   ```bash
   cd satproje
   ```

2. Sanal ortam oluşturun:
   ```bash
   python -m venv .venv
   ```

3. Sanal ortamı etkinleştirin:
   ```bash
   .venv\Scripts\activate
   ```

4. Bağımlılıkları yükleyin:
   ```bash
   python -m pip install -r requirements.txt
   ```

5. Uygulamayı çalıştırın:
   ```bash
   python app.py
   ```

6. Tarayıcıda şu adresi açın:
   ```text
   http://127.0.0.1:5000/login
   ```

## Giriş Bilgileri

- Kullanıcı adı: admin
- Şifre: admin123

## Veritabanı

Uygulama SQLite kullanmaktadır. Varsayılan veritabanı dosyası:

```text
attendance_system.db
```

Bu veritabanı, öğrenciler ve yoklama kayıtları gibi bilgileri saklar. Proje küçük ölçekli olduğu için SQLite yeterli ve pratik bir seçenektir.

## Amaç ve Hedefler

Bu proje, sistem analizi ve tasarım dersi kapsamında öğrencilerin devamsızlık işlemlerini daha düzenli, hızlı ve verimli bir şekilde takip edebilecek sade bir web uygulaması geliştirmeyi amaçlamaktadır. Amaç, öğretmenin her gün öğrencilerin yoklama durumunu tek bir sistem üzerinden kontrol etmesi, yeni öğrencileri kaydetmesi ve devamsızlık bilgilerini düzenli bir şekilde takip edebilmesidir. Bu bağlamda proje, gereksiz ve karmaşık özelliklerden arındırılarak yalnızca temel işlevlere odaklanmıştır. Böylece sistemin kullanım kolaylığı artmış, iş akışı daha anlaşılır hale gelmiş ve proje sunum sırasında daha etkili bir örnek çalışma olarak kullanılabilmiştir. Öğrencilerin bilgilerini güvenli ve düzenli şekilde saklamak, günlük yoklama kayıtlarını doğru tutmak ve bu veriler üzerinden temel istatistikleri görmek, proje kapsamında öncelikli hedefler arasında yer almaktadır. Ayrıca sistemin küçük ölçekli olması, temel yazılım geliştirme süreçlerini anlamayı kolaylaştırır. Bu nedenle proje, sistem analizi ve tasarım dersi için uygun, sade ve anlaşılır bir örnek çalışma olarak hazırlanmıştır. Proje geliştirilirken kullanıcı ihtiyaçları, işlevsel gereksinimler ve veri yönetimi gibi temel kavramlar dikkatle ele alınmıştır. Sonuç olarak bu uygulama, devamsızlık takibinin daha basit ve erişilebilir bir şekilde yapılabilmesini sağlar; aynı zamanda öğrencilerin ve öğretmenin iş yükünü azaltmayı hedefler.

## Yöntem

Projenin geliştirilmesinde Flask web frameworkü kullanılmıştır. Flask, hafif yapısı, kolay öğrenilebilir olması ve hızlı geliştirme imkanı nedeniyle bu tür bir öğrenci yoklama sistemi için uygun bir tercih olmuştur. Uygulamanın arka planında Python dili kullanılmış; bu sayede iş mantığı sade ve okunabilir bir şekilde yazılmıştır. Veritabanı olarak SQLite seçilmiştir. SQLite, ek sunucu kurulumu gerektirmemesi, küçük projelerde hızlı bir şekilde çalışması ve kurulumu kolay olması nedeniyle bu çalışma için ideal bir çözümdür. Sistemin yapısında yönetici giriş ekranı, öğrenci ekleme formu, yoklama kaydı ekranı ve anasayfa pano bölümleri oluşturulmuştur. Bu bileşenler, sistemin temel işleyişini temsil eder ve kullanıcıların işlevleri kolayca gerçekleştirmesini sağlar. Her öğrenci için ayrı bir kayıt oluşturulmuş ve her gün için yeni yoklama girişleri tutulmuştur. Bu kayıtlar "Var", "Yok" ve "Geç Kaldı" durumlarına göre sınıflandırılmıştır. Geliştirme sürecinde gereksiz modüller kaldırılmış, yalnızca devamsızlık takibi sürecine odaklanılmıştır. Böylece kullanıcı arayüzü sade tutulmuş ve sistem daha anlaşılır hale getirilmiştir. Ayrıca geliştirilen uygulama, öğretmenin günlük iş akışını kolaylaştıracak şekilde tasarlanmıştır. Tüm bu süreçler dikkate alınarak proje, küçük ama işlevsel bir yazılım çözümü olarak oluşturulmuştur. Bu yöntem, sistem analizi ve tasarım dersinde temel tasarım ve geliştirme prensiplerini anlamayı kolaylaştırır ve akademik olarak uygun bir örnek çalışma sunar.

## Proje Yapısı

```text
satproje/
├── app.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
├── attendance_system.db
├── static/
│   ├── css/
│   └── js/
├── templates/
│   ├── auth/
│   ├── attendance/
│   ├── dashboard/
│   ├── leaves/
│   ├── users/
│   ├── base.html
│   ├── profile.html
│   ├── settings.html
│   └── system_analysis.html
└── tests/
```

## Lisans

Bu proje eğitim ve akademik amaçlar için geliştirilmiştir.
