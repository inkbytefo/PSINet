from .column import BionicColumn
from brian2 import Synapses, Network

class SimpleHierarchy:
    """
    Bir girdi katmanı ve bir işlem katmanından (BionicColumn) oluşan
    basit, iki katmanlı bir PSINet hiyerarşisi.
    """
    def __init__(self, input_layer, num_excitatory=100, num_inhibitory=25):
        """
        Args:
            input_layer (PoissonGroup): Girdi verisini sağlayan "retina".
            num_excitatory (int): İşlem sütunundaki uyarıcı nöron sayısı.
            num_inhibitory (int): İşlem sütunundaki engelleyici nöron sayısı.
        """
        self.input_layer = input_layer
        
        print("\nİşlem katmanı (L1) oluşturuluyor...")
        self.layer1 = BionicColumn(num_excitatory, num_inhibitory)
        
        print("Girdi katmanı L1'e bağlanıyor...")
        # Girdi katmanını Sütunun Uyarıcı Nöronlarına bağlayalım
        # Bu bağlantı öğrenecek! Ama şimdilik basit bir bağlantı kuralı kullanalım.
        self.input_to_l1_synapse = Synapses(self.input_layer, 
                                            self.layer1.excitatory_neurons.group, 
                                            on_pre='v += 0.2') # Başlangıçta öğrenme yok
        self.input_to_l1_synapse.connect()
        
    def build_network(self, *monitors):
        """
        Tüm bileşenleri bir araya getirerek çalıştırılabilir bir Brian2 Network'ü kurar.
        """
        all_components = [
            self.input_layer,
            self.input_to_l1_synapse
        ]
        all_components.extend(self.layer1.all_objects)
        all_components.extend(monitors)
        
        return Network(all_components)