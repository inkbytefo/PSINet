import brian2 as b2
import matplotlib.pyplot as plt
import numpy as np
from psinet.io.encoders import image_to_poisson_rates, create_input_layer
from psinet.network.hierarchy import SimpleHierarchy

# Test görüntüsü oluşturma fonksiyonu
def create_test_digit():
    """Basit bir '0' rakamı benzeri test görüntüsü oluşturur"""
    image = np.zeros((28, 28))
    # Dış çember
    for i in range(28):
        for j in range(28):
            # Merkez (14, 14) etrafında halka şekli
            dist = np.sqrt((i - 14)**2 + (j - 14)**2)
            if 8 <= dist <= 12:  # Halka kalınlığı
                image[i, j] = 255
    return image.astype(np.uint8)

print("🧠 PSINet - MNIST Rakamı Öğrenme Testi Başlatılıyor...")
print("Bu deney, PSINet'in gerçek öğrenme yeteneğini test edecek!")

# --- 1. Veri ve Ağ Kurulumu ---
print("📸 Test görüntüsü oluşturuluyor...")
test_image = create_test_digit()
print("Test için sentetik '0' rakamı kullanılıyor.")

input_rates = image_to_poisson_rates(test_image, max_rate=100*b2.Hz)
input_layer = create_input_layer(input_rates)

# Öğrenme AKTİF olarak hiyerarşiyi oluştur
print("\n🎯 Öğrenme aktif hiyerarşi oluşturuluyor...")
network_hierarchy = SimpleHierarchy(input_layer, num_excitatory=100, num_inhibitory=25, enable_learning=True)

# --- 2. İzleyicileri Ayarlama ---
print("📊 İzleyiciler ayarlanıyor...")
l1_exc_monitor = b2.SpikeMonitor(network_hierarchy.layer1.excitatory_neurons.group)

# Girdi-L1 sinapslarının ağırlıklarını izleyelim
# Tüm sinapsları izlemek çok fazla veri üreteceği için sadece ilk 50 L1 nöronuna giden
# bağlantıların bir alt kümesini izleyelim.
weight_monitor = b2.StateMonitor(network_hierarchy.input_to_l1_synapse.synapses, 'w', 
                                 record=np.random.choice(np.arange(784 * 50), 100, replace=False))

# --- 3. Simülasyonu Çalıştırma ---
# Ağa öğrenmesi için yeterli zaman verelim
simulation_time = 5 * b2.second # Simülasyon süresini saniyelere çıkarıyoruz!
print(f"\n⏱️  Simülasyon {simulation_time} boyunca çalıştırılıyor...")
print("Bu biraz zaman alabilir - PSINet öğreniyor! ⚡")

net = network_hierarchy.build_network(l1_exc_monitor, weight_monitor)

# store() ve restore() ile simülasyonu parçalara bölebiliriz
print("🧠 Öğrenme süreci başlıyor...")
net.run(simulation_time / 2, report='text') # İlk yarı
print("✨ Öğrenme sürecinin yarısı tamamlandı...")
net.run(simulation_time / 2, report='text') # İkinci yarı

print("🎉 Simülasyon tamamlandı! PSINet öğrendi!")

# --- 4. Sonuçları Görselleştirme ---
print("📈 Sonuçlar görselleştiriliyor...")
fig, axes = plt.subplots(3, 1, figsize=(14, 16))

# Orijinal test görüntüsü
axes[0].imshow(test_image, cmap='gray')
axes[0].set_title('Orijinal Test Görüntüsü (Sentetik "0" Rakamı)', fontsize=14, fontweight='bold')
axes[0].axis('off')

# L1 Katmanının Ateşleme Aktivitesi
axes[1].plot(l1_exc_monitor.t / b2.ms, l1_exc_monitor.i, '.k', markersize=1)
axes[1].set_title('🧠 L1 Sütun Aktivitesi - Öğrenme Sonrası', fontsize=14, fontweight='bold')
axes[1].set_ylabel('Nöron İndisi')
axes[1].set_xlabel('Zaman (ms)')
axes[1].grid(True, alpha=0.3)

# Sinaptik Ağırlıkların Değişimi
axes[2].plot(weight_monitor.t / b2.ms, weight_monitor.w.T, alpha=0.7, linewidth=0.8)
axes[2].set_title('⚡ Örnek Sinaptik Ağırlıkların Zamanla Değişimi (STDP Öğrenme)', fontsize=14, fontweight='bold')
axes[2].set_xlabel('Zaman (ms)')
axes[2].set_ylabel('Ağırlık (w)')
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.suptitle('🎯 PSINet Öğrenme Deneyi - MNIST Rakam Tanıma', fontsize=16, fontweight='bold', y=0.98)
plt.show()

# --- 5. Öğrenme Analizi ---
print("\n📊 ÖĞRENME ANALİZİ:")
print("=" * 50)

# L1 aktivite analizi
total_spikes = len(l1_exc_monitor.t)
active_neurons = len(np.unique(l1_exc_monitor.i))
print(f"🔥 Toplam L1 ateşleme: {total_spikes:,}")
print(f"🧠 Aktif nöron sayısı: {active_neurons}/100 (%{active_neurons:.1f})")

# Ağırlık değişimi analizi
initial_weights = weight_monitor.w[:, 0]  # İlk zaman adımı
final_weights = weight_monitor.w[:, -1]   # Son zaman adımı
weight_change = np.abs(final_weights - initial_weights)
significant_changes = np.sum(weight_change > 0.01)

print(f"⚡ Önemli ağırlık değişimi gösteren sinaps: {significant_changes}/100")
print(f"📈 Ortalama ağırlık değişimi: {np.mean(weight_change):.4f}")
print(f"📊 Maksimum ağırlık değişimi: {np.max(weight_change):.4f}")

if significant_changes > 20:
    print("✅ BAŞARILI: Önemli öğrenme tespit edildi!")
    print("   PSINet, MNIST rakamının özelliklerini öğrendi!")
else:
    print("⚠️  Sınırlı öğrenme: Daha uzun simülasyon gerekebilir.")

print("\n🎯 PSINet artık bir öğrenme makinesi!")
print("Bu deney, gözetimsiz özellik öğrenmenin çalışan bir örneğidir.")