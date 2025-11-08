# Brian2 ve görselleştirme kütüphanelerini içe aktaralım
import brian2 as b2
import matplotlib
matplotlib.use('Agg')  # GUI olmayan backend kullan
import matplotlib.pyplot as plt

# Kendi yazdığımız BionicNeuron sınıfını içe aktaralım
from psinet.core.neuron import BionicNeuron

print("PSINet - Tek Nöron Ateşleme Testi Başlatılıyor...")

# Brian2'nin uyarılarını azalt
b2.prefs.codegen.target = 'numpy'

# --- 1. Kurulum ---
# Tek bir nörondan oluşan bir grup yaratalım
neuron_population = BionicNeuron(num_neurons=1)

# Nörona ateşlemesi için yeterli, sabit bir giriş akımı verelim.
# Eşiğimiz 'v > 1.0' olduğu için 1.1 birim akım ateşlemesini sağlayacaktır.
neuron_population.group.I = 1.1 

# --- 2. İzleyicileri (Monitors) Ayarlama ---
# Bu izleyiciler, simülasyon sırasında nöronda ne olup bittiğini kaydeder.

# SpikeMonitor, her bir nöronun ne zaman ateşlediğini kaydeder.
spike_monitor = b2.SpikeMonitor(neuron_population.group)

# StateMonitor, nöronun potansiyel (v) gibi durumlarını zaman içinde kaydeder.
# record=0 demek, 0. indisteki nöronu (yani tek nöronumuzu) kaydet demektir.
voltage_monitor = b2.StateMonitor(neuron_population.group, 'v', record=0)

# Network oluştur ve tüm bileşenleri ekle
net = b2.Network(neuron_population.group, spike_monitor, voltage_monitor)

# --- 3. Simülasyonu Çalıştırma ---
# Simülasyonu 100 milisaniye boyunca çalıştıralım.
simulation_time = 100 * b2.ms
print(f"Simülasyon {simulation_time} boyunca çalıştırılıyor...")
net.run(simulation_time)
print("Simülasyon tamamlandı.")

# --- 4. Sonuçları Görselleştirme ---
print("Sonuçlar görselleştiriliyor...")
plt.figure(figsize=(12, 6))

# Potansiyel grafiği
plt.subplot(2, 1, 1)
plt.plot(voltage_monitor.t / b2.ms, voltage_monitor.v[0], label='Membran Potansiyeli (v)')
plt.axhline(1.0, color='r', linestyle='--', label='Ateşleme Eşiği')
plt.xlabel('Zaman (ms)')
plt.ylabel('Potansiyel (v)')
plt.title('Tek Biyonik Nöronun Aktivitesi')
plt.legend()
plt.grid(True)

# Ateşleme (Spike) grafiği
plt.subplot(2, 1, 2)
plt.plot(spike_monitor.t / b2.ms, spike_monitor.i, 'or', label='Ateşleme (Spike)') # 'or' -> kırmızı daireler
plt.xlabel('Zaman (ms)')
plt.ylabel('Nöron İndisi')
plt.yticks([]) # Y ekseninde sadece bir nöron olduğu için etiketlere gerek yok
plt.title('Ateşleme Zamanları')
plt.grid(True)

plt.tight_layout()
plt.savefig('neuron_test_results.png', dpi=150, bbox_inches='tight')
print("Grafik 'neuron_test_results.png' dosyasına kaydedildi.")

# Sonuçları konsola da yazdıralım
print(f"\n=== TEST SONUÇLARI ===")
print(f"Toplam ateşleme sayısı: {len(spike_monitor.t)}")
if len(spike_monitor.t) > 0:
    print(f"İlk ateşleme zamanı: {spike_monitor.t[0]/b2.ms:.2f} ms")
    print(f"Son ateşleme zamanı: {spike_monitor.t[-1]/b2.ms:.2f} ms")
    if len(spike_monitor.t) > 1:
        intervals = [spike_monitor.t[i+1] - spike_monitor.t[i] for i in range(len(spike_monitor.t)-1)]
        avg_interval = sum(intervals) / len(intervals)
        print(f"Ortalama ateşleme aralığı: {avg_interval/b2.ms:.2f} ms")
        print(f"Ateşleme frekansı: {1000/(avg_interval/b2.ms):.2f} Hz")

print("Test tamamlandı.")