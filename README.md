# Alaybeyoğlu Hukuk Bürosu — Site Dosyaları

Bu çalışma kullanıcının gönderdiği logo üzerinden hazırlanan, telefon / bilgisayar uyumlu **taslak web sitesidir**. Ücretli yazılım lisansı gerektirmez; bir alan adı almanız şart değildir.

## İçerik

- Anasayfa, Hakkımızda, Faaliyet Alanları, Makaleler, İletişim
- Berat Büşra Alaybeyoğlu ve Selahattin Yiğit Alaybeyoğlu profilleri ve eğitim bilgileri
- Kullanıcının verdiği iletişim bilgileri ve Instagram bağlantısı
- Makale arama, kategori filtresi, yazar ve tarih bilgisi, makale ayrıntı sayfası
- Makaleler için **taslak / yayımlandı** anahtarı. İlk örnek yazı taslaktır; ziyaretçiye gösterilmez.

## Yönetim paneli: Makaleler nasıl eklenir?

Bu dosyalarda `.pages.yml` ile tanımlanmış **Pages CMS** yapılandırması bulunur.

1. https://github.com adresinde bir hesap açın (varsa hesabınızı kullanın).
2. Yeni bir depo (repository) oluşturun. Zip içindeki `alaybeyoglu-hukuk-site` klasörünün **içindeki dosyaları** deponun ana dizinine yükleyin. `.pages.yml` adlı gizli dosyanın da yüklendiğinden emin olun.
3. https://dash.cloudflare.com üzerinden **Workers & Pages > Create application > Pages > Connect to Git** adımlarını izleyerek GitHub deponuzu bağlayın.
4. Build command: `pip install -r requirements.txt && python3 build.py`
5. Build output directory: `dist`
6. Oluşan `*.pages.dev` adresinden siteyi görün. Sonra https://app.pagescms.org adresinde GitHub hesabınızla oturum açın, GitHub App'e depoya erişim verin ve projeyi seçin.
7. **Makaleler > Yeni** bölümünde başlık, yayın tarihi, kategori, yazar, özet ve tam metni girin. `Yayımla` kapalıysa ziyaretçiye gösterilmez.
8. Yayımlamaya hazır olduğunuzda `Yayımla`yı açıp kaydedin. Pages CMS GitHub'a kaydeder ve Cloudflare otomatik olarak siteyi yeniler. Her yayınlamada yeniden zip göndermek gerekmez.

Birlikte yayın yapacaksanız ikinci avukata GitHub deposunda uygun erişim izni verilip Pages CMS erişimi sağlanmalıdır; yetkileri ve üyelik/ücret koşullarını ilgili platformda kontrol edin.

**Önemli:** `dist` klasörünü doğrudan internete yüklemek, çalışan siteyi yayımlar ama sonradan kodsuz içerik güncellemeyi *tek başına* sağlamaz. Otomatik güncellemeler için GitHub bağlantısı gerekir.

## Yerel kontrol

```bash
pip install -r requirements.txt
python3 build.py
cd dist
python3 -m http.server 8000
```

`http://localhost:8000` adresinden inceleyebilirsiniz.

## Hukuki yayın kontrolü

**Yayımdan önce** TBB Reklam Yasağı Yönetmeliği'nin güncel metni ve özellikle 7. maddesini kontrol edin. Bu hüküm, internet sitesindeki bilgileri ve iş elde etmeye yönelik genel/soyut paylaşımları sınırlar. Makaleler dahil içeriklerin mevzuata uygunluğu kullanıcı avukatların mesleki değerlendirmesiyle teyit edilmelidir; her makalenin yayımlanması otomatik olarak hukuka uygun olduğu anlamına gelmez.

Ayrıca büro unvanı, baro ve TBB sicil numaraları, profiller ve site ifadelerini yayından önce inceleyin. Hazır taslakta ölçülmemiş SEO, izleme çerezi ve ziyaretçi formu bulunmuyor.

## Teknik yapı

`build.py` yazıları `content/makaleler/*.json` dizininden okuyarak `dist` klasörüne statik HTML üretir. Sadece `published: true` yazılar yayımlanır. Yayımlanmış dosyaların adlarını (URL) mümkünse sonradan değiştirmeyin.

Kaynaklar: https://pagescms.org/docs/quick-start/ ve https://developers.cloudflare.com/pages/configuration/git-integration/ 
