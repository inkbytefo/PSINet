import brian2 as b2
import matplotlib
matplotlib.use('Agg')  # GUI olmayan backend kullan
import matplotlib.pyplot as plt
from psinet.network.column import BionicColumn

print("PSINet - Biyonik Sütun Rekabet Testi Başlatılıyor...")

# Brian2'nin uyarılarını azalt
b2.prefs.codegen.target = 'numpy'

# --- 1. Kurulum ---
# Test edeceğimiz sütunu oluşturalım
column = BionicColumn(num_excitatory=100, num_inhibitory=25)

# Sütuna girdi sağlamak için bir "Giriş Katmanı" oluşturalım.
# PoissonGroup, rastgele ama belirli bir ortalama frekansta ateşleyen bir nöron grubudur.
# Bu, gerçek beyin aktivitesine daha çok benzer.
num_inputs = 100
input_layer = b2.PoissonGroup(num_inputs, rates=0*b2.Hz) # Başlangıçta sessiz

# Giriş Katmanını Sütunun Uyarıcı Nöronlarına bağlayalım
# Bu, dış dünyadan gelen sinyali temsil eder.
input_synapse = b2.Synapses(input_layer, column.excitatory_neurons.group, on_pre='v += 1.5')
input_synapse.connect(j='i')

# --- 2. Deney Tasarımı ---
# Deneyimiz iki fazdan oluşacak:
# Faz 1: Gürültü. Tüm giriş nöronları düşük frekansta ateşler.
# Faz 2: Odaklanmış Girdi. Giriş nöronlarının küçük bir grubu yüksek frekansta ateşler.

# --- 3. İzleyicileri Ayarlama ---
# Uyarıcı ve Engelleyici nöronların ateşlemelerini izleyelim
exc_spike_monitor = b2.SpikeMonitor(column.excitatory_neurons.group)
inh_spike_monitor = b2.SpikeMonitor(column.inhibitory_neurons.group)

# --- 4. Simülasyonu Çalıştırma ---
# Simülasyonu Brian2'nin Network objesi içinde çalıştıracağız
net = b2.Network(column.all_objects) # Sütunun tüm bileşenlerini al
net.add(input_layer, input_synapse, exc_spike_monitor, inh_spike_monitor)

# Faz 1: Gürültülü Girdi (500 ms)
print("Faz 1: Gürültülü girdi veriliyor...")
input_layer.rates = 10 * b2.Hz  # Daha düşük arka plan gürültüsü
net.run(500 * b2.ms)

# Faz 2: Odaklanmış Girdi (500 ms)
print("Faz 2: Odaklanmış girdi veriliyor...")
input_layer.rates = 5 * b2.Hz # Çok düşük arka plan gürültüsü
# Giriş nöronlarının 20-30 arasındaki küçük bir grubunu "güçlendirelim"
input_layer.rates[20:30] = 80 * b2.Hz  # Güçlü odaklanmış girdi
net.run(500 * b2.ms)

print("Simülasyon tamamlandı.")

# --- 5. Sonuçları Görselleştirme ---
print("Sonuçlar görselleştiriliyor...")
plt.figure(figsize=(15, 8))

# Uyarıcı Nöronların Ateşleme Grafiği
plt.subplot(2, 1, 1)
plt.plot(exc_spike_monitor.t / b2.ms, exc_spike_monitor.i, '.k', markersize=2)
plt.axvline(500, color='r', linestyle='--', label='Odaklanmış Girdi Başlangıcı')
plt.title('Uyarıcı Nöron Aktivitesi')
plt.xlabel('Zaman (ms)')
plt.ylabel('Nöron İndisi')
plt.legend()

# Engelleyici Nöronların Ateşleme Grafiği
plt.subplot(2, 1, 2)
plt.plot(inh_spike_monitor.t / b2.ms, inh_spike_monitor.i, '.b', markersize=2)
plt.axvline(500, color='r', linestyle='--', label='Odaklanmış Girdi Başlangıcı')
plt.title('Engelleyici Nöron Aktivitesi')
plt.xlabel('Zaman (ms)')
plt.ylabel('Nöron İndisi')
plt.legend()

plt.tight_layout()
plt.savefig('column_competition_results.png', dpi=150, bbox_inches='tight')
print("Grafik 'column_competition_results.png' dosyasına kaydedildi.")

# --- 6. Sonuçları Analiz Et ---
print(f"\n=== SÜTUN REKABETİ TEST SONUÇLARI ===")

# Faz 1 ve Faz 2'deki ateşleme sayılarını hesapla
phase1_spikes = sum((exc_spike_monitor.t >= 0*b2.ms) & (exc_spike_monitor.t < 500*b2.ms))
phase2_spikes = sum((exc_spike_monitor.t >= 500*b2.ms) & (exc_spike_monitor.t < 1000*b2.ms))

print(f"Faz 1 (Gürültülü) toplam ateşleme: {phase1_spikes}")
print(f"Faz 2 (Odaklanmış) toplam ateşleme: {phase2_spikes}")

# Faz 2'de hangi nöronların daha aktif olduğunu kontrol et
phase2_mask = (exc_spike_monitor.t >= 500*b2.ms) & (exc_spike_monitor.t < 1000*b2.ms)
phase2_neurons = exc_spike_monitor.i[phase2_mask]

if len(phase2_neurons) > 0:
    # En aktif nöron aralığını bul
    unique_neurons, counts = b2.numpy.unique(phase2_neurons, return_counts=True)
    most_active_neuron = unique_neurons[b2.numpy.argmax(counts)]
    max_activity = b2.numpy.max(counts)
    
    print(f"En aktif nöron: {most_active_neuron} ({max_activity} ateşleme)")
    
    # Hedef aralık (20-30) ile karşılaştır
    target_range_activity = sum((phase2_neurons >= 20) & (phase2_neurons < 30))
    total_phase2_activity = len(phase2_neurons)
    
    if total_phase2_activity > 0:
        target_percentage = (target_range_activity / total_phase2_activity) * 100
        print(f"Hedef aralık (20-30) aktivite oranı: {target_percentage:.1f}%")
        
        if target_percentage > 30:  # Eğer hedef aralık aktivitenin %30'undan fazlasını oluşturuyorsa
            print("🎯 Winner-Take-All mekanizması BAŞARILI! Odaklanmış girdi baskın çıktı.")
        else:
            print("⚠️  Winner-Take-All mekanizması zayıf. Rekabet yeterince güçlü değil.")
    else:
        print("⚠️  Faz 2'de hiç ateşleme yok.")
else:
    print("⚠️  Faz 2'de hiç ateşleme tespit edilmedi.")

print("Test tamamlandı.")