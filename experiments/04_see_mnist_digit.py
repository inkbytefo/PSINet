import brian2 as b2
import matplotlib
matplotlib.use('Agg')  # GUI olmayan backend kullan
import matplotlib.pyplot as plt
import numpy as np
from psinet.io.encoders import image_to_poisson_rates, create_input_layer
from psinet.network.hierarchy import SimpleHierarchy

# Brian2'nin uyarılarını azalt
b2.prefs.codegen.target = 'numpy'

# MNIST veri setini yüklemek için bir yardımcı fonksiyon
# (Eğer yüklü değilse, pip install mnist)
def load_mnist_data():
    try:
        import mnist
        images = mnist.train_images()
        return images
    except Exception as e:
        print("MNIST veri seti yüklenemedi. Lütfen 'pip install mnist' komutuyla yükleyin.")
        print(f"Hata: {e}")
        return None

def create_sample_digit():
    """
    MNIST yüklenemezse, basit bir örnek rakam oluştur
    """
    # 28x28 boyutunda basit bir "5" rakamı çiz
    digit = np.zeros((28, 28))
    
    # Üst yatay çizgi
    digit[5:8, 8:20] = 255
    # Sol dikey çizgi
    digit[5:15, 8:11] = 255
    # Orta yatay çizgi
    digit[12:15, 8:18] = 255
    # Sağ dikey çizgi
    digit[12:22, 15:18] = 255
    # Alt yatay çizgi
    digit[19:22, 8:18] = 255
    
    return digit

print("PSINet - MNIST Rakamı Görselleştirme Testi Başlatılıyor...")

# --- 1. Veriyi Yükle ve Hazırla ---
mnist_images = load_mnist_data()
if mnist_images is not None:
    # Test için ilk görüntüyü alalım (genellikle bir '5' rakamı)
    image_index = 0
    test_image = mnist_images[image_index]
    print(f"Test için {image_index}. MNIST görüntüsü kullanılıyor (28x28).")
else:
    # MNIST yüklenemezse örnek rakam kullan
    test_image = create_sample_digit()
    print("MNIST yüklenemedi, örnek rakam kullanılıyor.")

# Görüntüyü ateşleme frekanslarına çevir
input_rates = image_to_poisson_rates(test_image, max_rate=150*b2.Hz)
num_inputs = 28 * 28

# Girdi katmanını ("retina") oluştur
input_layer = create_input_layer(input_rates)

# --- 2. Ağı Kur ---
# 784 girdi nöronu, 100 uyarıcı nörondan oluşan bir sütuna bağlanıyor
network_hierarchy = SimpleHierarchy(input_layer, num_excitatory=100, num_inhibitory=25)

# --- 3. İzleyicileri Ayarlama ---
input_monitor = b2.SpikeMonitor(network_hierarchy.input_layer)
l1_exc_monitor = b2.SpikeMonitor(network_hierarchy.layer1.excitatory_neurons.group)

# --- 4. Simülasyonu Çalıştırma ---
simulation_time = 350 * b2.ms
print(f"Simülasyon {simulation_time} boyunca çalıştırılıyor...")

# Çalıştırılabilir ağı oluştur
net = network_hierarchy.build_network(input_monitor, l1_exc_monitor)
net.run(simulation_time)

print("Simülasyon tamamlandı.")

# --- 5. Sonuçları Görselleştirme ---
print("Sonuçlar görselleştiriliyor...")
fig, axes = plt.subplots(3, 1, figsize=(12, 15), gridspec_kw={'height_ratios': [1, 2, 2]})

# Orijinal Görüntü
axes[0].imshow(test_image, cmap='gray_r')
if mnist_images is not None:
    axes[0].set_title(f'Orijinal MNIST Görüntüsü (indis 0)')
else:
    axes[0].set_title('Örnek Rakam (5)')
axes[0].axis('off')

# Girdi Katmanı ("Retina") Ateşlemeleri
axes[1].plot(input_monitor.t / b2.ms, input_monitor.i, '.k', markersize=1)
axes[1].set_title('Girdi Katmanı ("Retina") Aktivitesi')
axes[1].set_xlabel('Zaman (ms)')
axes[1].set_ylabel('Nöron İndisi (Piksel)')
axes[1].set_xlim(0, simulation_time/b2.ms)

# Katman 1 (L1) Uyarıcı Nöron Ateşlemeleri
axes[2].plot(l1_exc_monitor.t / b2.ms, l1_exc_monitor.i, '.r', markersize=2)
axes[2].set_title('Katman 1 (L1) Sütun Aktivitesi')
axes[2].set_xlabel('Zaman (ms)')
axes[2].set_ylabel('Nöron İndisi')
axes[2].set_xlim(0, simulation_time/b2.ms)

plt.tight_layout()
plt.savefig('mnist_vision_results.png', dpi=150, bbox_inches='tight')
print("Grafik 'mnist_vision_results.png' dosyasına kaydedildi.")

# --- 6. Sonuçları Analiz Et ---
print(f"\n=== PSINet GÖRSEL İŞLEME TEST SONUÇLARI ===")

# Retina aktivitesi analizi
retina_spikes = len(input_monitor.t)
active_pixels = len(np.unique(input_monitor.i))
total_pixels = 28 * 28

print(f"Retina toplam ateşleme: {retina_spikes}")
print(f"Aktif piksel sayısı: {active_pixels}/{total_pixels} (%{active_pixels/total_pixels*100:.1f})")

# L1 aktivitesi analizi
l1_spikes = len(l1_exc_monitor.t)
active_l1_neurons = len(np.unique(l1_exc_monitor.i)) if len(l1_exc_monitor.i) > 0 else 0
total_l1_neurons = 100

print(f"L1 katmanı toplam ateşleme: {l1_spikes}")
print(f"Aktif L1 nöron sayısı: {active_l1_neurons}/{total_l1_neurons} (%{active_l1_neurons/total_l1_neurons*100:.1f})")

if retina_spikes > 0 and l1_spikes > 0:
    print("🎯 PSINet başarıyla görsel veriyi işledi!")
    print("📊 Retina aktivitesi L1 katmanına başarıyla iletildi.")
    
    # Aktivite yoğunluğu analizi
    if active_pixels > total_pixels * 0.1:  # %10'dan fazla piksel aktifse
        print("🔥 Yoğun görsel aktivite tespit edildi - rakam net bir şekilde algılandı!")
    else:
        print("💡 Seyrek görsel aktivite - rakam hafif çizgilerle algılandı.")
        
elif retina_spikes > 0:
    print("⚠️  Retina aktif ama L1 tepki vermiyor - bağlantı zayıf olabilir.")
else:
    print("❌ Retina aktivitesi yok - görüntü kodlama sorunu.")

print("Test tamamlandı.")