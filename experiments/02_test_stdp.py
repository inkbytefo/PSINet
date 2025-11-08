import brian2 as b2
import matplotlib
matplotlib.use('Agg')  # GUI olmayan backend kullan
import matplotlib.pyplot as plt
from psinet.core.neuron import BionicNeuron
from psinet.core.synapse import BionicSynapse

print("PSINet - STDP Öğrenme Kuralı Testi Başlatılıyor...")

# Brian2'nin uyarılarını azalt
b2.prefs.codegen.target = 'numpy'

# --- 1. Kurulum ---
# Nöronları oluşturalım. SpikeGeneratorGroup, tam olarak istediğimiz zamanda
# ateşleme yapmamızı sağlayan özel bir nöron tipidir.
input_neuron = b2.SpikeGeneratorGroup(1, [0], [0]*b2.ms) # Şimdilik boş
output_neuron_group = BionicNeuron(num_neurons=1)

# Sinapsı oluşturalım. w_max'ı ve A'ları test için biraz büyük tuttuk.
synapse = BionicSynapse(input_neuron, output_neuron_group, w_max=1.0, A_pre=0.1, A_post=-0.11)
# Başlangıç ağırlığını ortada bir yere ayarlayalım
synapse.synapses.w = 0.5

# --- 2. Deney Tasarımı ---
# Öğrenmeyi test etmek için ateşleme çiftleri oluşturacağız.
num_pairs = 60
potentiation_dt = 10 * b2.ms  # Güçlenme için: giriş, çıkıştan 10ms ÖNCE ateşler
depression_dt = -10 * b2.ms # Zayıflama için: giriş, çıkıştan 10ms SONRA ateşler
pair_interval = 100 * b2.ms # Her çift arasında 100ms boşluk

# ATEŞLEME ZAMANLAMALARINI OLUŞTUR
input_spikes = []
output_spikes = []

# Faz 1: Güçlenme (Potentiation)
print(f"{num_pairs} ateşleme çifti ile GÜÇLENME test ediliyor...")
for i in range(num_pairs):
    spike_time = (i * pair_interval)
    input_spikes.append(spike_time)
    output_spikes.append(spike_time + potentiation_dt)

# Faz 2: Zayıflama (Depression)
print(f"{num_pairs} ateşleme çifti ile ZAYIFLAMA test ediliyor...")
offset = num_pairs * pair_interval + 200*b2.ms # İki faz arasında boşluk bırak
for i in range(num_pairs):
    spike_time = offset + (i * pair_interval)
    # Zamanlamayı tersine çeviriyoruz!
    input_spikes.append(spike_time + depression_dt)
    output_spikes.append(spike_time)

# Nöronlara ateşleme zamanlarını verelim
input_neuron.set_spikes(indices=[0]*len(input_spikes), times=input_spikes)
# Çıkış nöronunu da ateşlemeye zorlamak için bir SpikeGeneratorGroup olarak tanımlamalıydık.
# Hızlı çözüm: Başka bir SpikeGeneratorGroup oluşturalım
output_stimulator = b2.SpikeGeneratorGroup(1, [0]*len(output_spikes), output_spikes)
# Bu stimülatörü asıl çıkış nöronumuza bağlayalım
stim_synapse = b2.Synapses(output_stimulator, output_neuron_group.group, on_pre='v += 2.0')
stim_synapse.connect()

# --- 3. İzleyicileri Ayarlama ---
# Sinaps ağırlığının (w) zamanla nasıl değiştiğini kaydedelim
weight_monitor = b2.StateMonitor(synapse.synapses, 'w', record=0)

# --- 4. Simülasyonu Çalıştırma ---
simulation_time = offset + num_pairs * pair_interval + 100*b2.ms
print(f"Simülasyon {simulation_time} boyunca çalıştırılıyor...")
# Tüm objeleri içeren bir Network kuralım
net = b2.Network(input_neuron, output_neuron_group.group, synapse.synapses, 
                 output_stimulator, stim_synapse, weight_monitor)
net.run(simulation_time)
print("Simülasyon tamamlandı.")

# --- 5. Sonuçları Görselleştirme ---
print("Sonuçlar görselleştiriliyor...")
plt.figure(figsize=(12, 6))
plt.plot(weight_monitor.t / b2.ms, weight_monitor.w[0], label='Sinaptik Ağırlık (w)')
plt.axvline(offset/b2.ms, color='r', linestyle='--', label='Zayıflama Fazı Başlangıcı')
plt.xlabel('Zaman (ms)')
plt.ylabel('Ağırlık (w)')
plt.title('STDP Öğrenme Kuralının Etkisi')
plt.legend()
plt.grid(True)
plt.savefig('stdp_test_results.png', dpi=150, bbox_inches='tight')
print("Grafik 'stdp_test_results.png' dosyasına kaydedildi.")

# Sonuçları konsola da yazdıralım
print(f"\n=== STDP TEST SONUÇLARI ===")
initial_weight = weight_monitor.w[0][0]
final_weight = weight_monitor.w[0][-1]
max_weight = max(weight_monitor.w[0])
min_weight = min(weight_monitor.w[0])

print(f"Başlangıç ağırlığı: {initial_weight:.4f}")
print(f"Maksimum ağırlık (güçlenme fazında): {max_weight:.4f}")
print(f"Minimum ağırlık (zayıflama fazında): {min_weight:.4f}")
print(f"Son ağırlık: {final_weight:.4f}")
print(f"Toplam değişim: {final_weight - initial_weight:.4f}")

# Güçlenme ve zayıflama fazlarının başarısını kontrol et
potentiation_success = max_weight > initial_weight
depression_success = min_weight < max_weight
print(f"\nGüçlenme fazı başarılı: {potentiation_success}")
print(f"Zayıflama fazı başarılı: {depression_success}")

if potentiation_success and depression_success:
    print("🎉 STDP öğrenme kuralı başarıyla çalışıyor!")
else:
    print("⚠️  STDP öğrenme kuralında sorun var.")

print("Test tamamlandı.")