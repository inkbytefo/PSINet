# PSINet - Biologically Inspired Neural Network Framework

🧠 **PSINet** (Plasticity-based Spiking Intelligence Network), biyolojik beyin işleyişinden ilham alan, spike-timing dependent plasticity (STDP) tabanlı bir yapay sinir ağı framework'üdür.

## 🎯 Proje Hedefi

PSINet, geleneksel yapay sinir ağlarının aksine, gerçek nöronların çalışma prensiplerini taklit eder:
- **Spike-based İletişim**: Nöronlar binary spike'lar ile iletişim kurar
- **Temporal Dynamics**: Zamansal dinamikler ve timing kritik öneme sahiptir  
- **STDP Öğrenme**: "Birlikte ateşleyen nöronlar birlikte bağlanır" prensibi
- **Winner-Take-All**: Rekabetçi öğrenme mekanizmaları
- **Hiyerarşik İşleme**: Kortikal sütun benzeri yapılar

## 🏗️ Mimari

```
PSINet/
├── psinet/              # Ana kütüphane
│   ├── core/            # Temel bileşenler
│   │   ├── neuron.py    # BionicNeuron sınıfı
│   │   ├── synapse.py   # BionicSynapse (STDP öğrenme)
│   │   └── learning_rules.py # Öğrenme algoritmaları
│   ├── network/         # Ağ yapıları
│   │   ├── layer.py     # Katman yönetimi
│   │   ├── column.py    # BionicColumn (Winner-Take-All)
│   │   └── hierarchy.py # Hiyerarşik ağ yapıları
│   ├── modules/         # Özel modüller
│   │   ├── attention.py # Dikkat mekanizmaları
│   │   └── hippocampus.py # Hafıza sistemleri
│   └── io/              # Girdi/Çıktı işleme
│       └── encoders.py  # Görüntü → Spike dönüştürücüler
├── experiments/         # Test senaryoları
├── simulation/          # Simülasyon motoru
├── visualization/       # Görselleştirme araçları
└── tests/               # Birim testleri
```

## 🚀 Özellikler

### ✅ Tamamlanan Bileşenler

- **BionicNeuron**: Leaky Integrate-and-Fire modeli ile gerçekçi nöron davranışı
- **BionicSynapse**: STDP tabanlı öğrenme ile adaptif bağlantılar
- **BionicColumn**: Winner-Take-All mekanizması ile rekabetçi öğrenme
- **Görsel Kodlama**: Statik görüntüleri spike dizilerine dönüştürme
- **Hiyerarşik İşleme**: Retina → Korteks benzeri bilgi akışı

### 🎯 Test Edilen Yetenekler

1. **Nöron Dinamikleri**: Gerçekçi ateşleme davranışları
2. **STDP Öğrenme**: Zamansal korelasyon tabanlı öğrenme
3. **Winner-Take-All**: Gürültüden sinyal ayırma (%58.7 başarı)
4. **Görsel İşleme**: MNIST rakamlarını spike dizilerine dönüştürme

## 🧪 Deneyler

### 1. Temel Nöron Testi (`01_test_basic_neuron.py`)
- Tek nöronun ateşleme davranışını test eder
- Farklı girdi akımlarına tepkiyi ölçer

### 2. STDP Öğrenme Testi (`02_test_stdp_learning.py`)
- İki nöron arasında STDP öğrenmeyi doğrular
- Zamansal korelasyonların sinaptik güçleri nasıl etkilediğini gösterir

### 3. Sütun Rekabet Testi (`03_test_column_competition.py`)
- Winner-Take-All mekanizmasını test eder
- Gürültülü vs odaklanmış girdi senaryoları

### 4. MNIST Görme Testi (`04_see_mnist_digit.py`)
- İlk gerçek görsel veri işleme deneyi
- Rakam görüntüsünü spike dizisine dönüştürme
- Retina → L1 korteks bilgi akışı

## 📊 Test Sonuçları

### Winner-Take-All Başarısı
- **Hedef aktivite aralığı**: %58.7 başarı
- **Gürültü filtreleme**: Etkili sinyal/gürültü ayrımı
- **Rekabetçi dinamik**: Başarılı yanal engelleme

### Görsel İşleme Başarısı  
- **Retina aktivitesi**: 34,937 spike (%84.7 piksel aktif)
- **L1 tepkisi**: 6,900 spike (%100 nöron aktif)
- **Sinyal iletimi**: Başarılı retina → korteks aktarımı

## 🛠️ Kurulum

```bash
# Gerekli paketleri yükle
pip install brian2 matplotlib numpy mnist

# Projeyi klonla
git clone https://github.com/inkbytefo/PSINet.git
cd PSINet

# Test deneyleri çalıştır
python experiments/01_test_basic_neuron.py
python experiments/02_test_stdp_learning.py  
python experiments/03_test_column_competition.py
python experiments/04_see_mnist_digit.py
```

## 🔬 Kullanım Örneği

```python
from psinet.core.neuron import BionicNeuron
from psinet.network.column import BionicColumn
from psinet.io.encoders import image_to_poisson_rates, create_input_layer

# Basit nöron oluştur
neuron = BionicNeuron()

# Winner-Take-All sütunu oluştur  
column = BionicColumn(num_excitatory=100, num_inhibitory=25)

# Görüntüyü spike'lara dönüştür
rates = image_to_poisson_rates(image)
input_layer = create_input_layer(rates)
```

## 🎯 Gelecek Planları

- [ ] **Çok Katmanlı Hiyerarşi**: Derin kortikal ağ yapıları
- [ ] **Dikkat Mekanizması**: Odaklanma ve filtreleme
- [ ] **Hafıza Sistemleri**: Hippocampus benzeri yapılar  
- [ ] **Desen Tanıma**: Karmaşık görsel desen öğrenme
- [ ] **Reinforcement Learning**: Ödül tabanlı öğrenme
- [ ] **Çevrimiçi Öğrenme**: Gerçek zamanlı adaptasyon

## 📚 Teorik Temeller

PSINet, aşağıdaki nörobiyoloji prensiplerini uygular:

- **Hebb Kuralı**: "Cells that fire together, wire together"
- **Spike-Timing Dependent Plasticity (STDP)**: Zamansal korelasyon öğrenme
- **Lateral Inhibition**: Rekabetçi dinamikler
- **Cortical Columns**: Modüler işleme birimleri
- **Hierarchical Processing**: Aşamalı bilgi soyutlama

## 🤝 Katkıda Bulunma

PSINet açık kaynak bir projedir. Katkılarınızı bekliyoruz!

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📄 Lisans

Bu proje MIT lisansı altında yayınlanmıştır.

## 🙏 Teşekkürler

- **Brian2**: Spiking neural network simülasyonu
- **NumPy & Matplotlib**: Bilimsel hesaplama ve görselleştirme
- **MNIST**: Test veri seti

---

**PSINet - Beynin sırlarını çözmek için bir adım** 🧠✨