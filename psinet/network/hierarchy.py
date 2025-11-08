from .column import BionicColumn
# BionicSynapse'ı içe aktaralım
from ..core.synapse import BionicSynapse
from brian2 import Synapses, Network

class SimpleHierarchy:
    """
    Bir girdi katmanı ve bir işlem katmanından (BionicColumn) oluşan
    basit, iki katmanlı ve ÖĞRENEN bir PSINet hiyerarşisi.
    """
    def __init__(self, input_layer, num_excitatory=100, num_inhibitory=25, enable_learning=True,
                 enable_lateral_inhibition=True, lateral_strength=0.2):
        """
        Args:
            input_layer (PoissonGroup): Girdi verisini sağlayan "retina".
            num_excitatory (int): İşlem sütunundaki uyarıcı nöron sayısı.
            num_inhibitory (int): İşlem sütunundaki engelleyici nöron sayısı.
            enable_learning (bool): Girdi-L1 arasındaki bağlantılarda STDP öğrenmesini aktif eder.
            enable_lateral_inhibition (bool): L1 içi yanal engellemeyi aç/kapat.
            lateral_strength (float): Yanal engelleme şiddeti.
        """
        self.input_layer = input_layer
        
        print("\nİşlem katmanı (L1) oluşturuluyor...")
        self.layer1 = BionicColumn(num_excitatory, num_inhibitory,
                                   enable_lateral_inhibition=enable_lateral_inhibition,
                                   lateral_strength=lateral_strength)
        
        print("Girdi katmanı L1'e öğrenen sinapslarla bağlanıyor...")
        if enable_learning:
            # Girdi katmanını Sütunun Uyarıcı Nöronlarına ÖĞRENEN sinapslarla bağlayalım
            self.input_to_l1_synapse = BionicSynapse(
                pre_neurons=self.input_layer, 
                post_neurons=self.layer1.excitatory_neurons,
                # Öğrenme parametrelerini burada hassas bir şekilde ayarlayabiliriz
                w_max=0.3,
                A_pre=0.01,
                A_post=-0.01
            )
        else:
            # Öğrenmesiz (statik) bağlantı seçeneğini koruyalım
            self.input_to_l1_synapse = Synapses(self.input_layer, 
                                                self.layer1.excitatory_neurons.group, 
                                                on_pre='v += 0.2')
            self.input_to_l1_synapse.connect()
        
    def build_network(self, *monitors):
        """
        Tüm bileşenleri bir araya getirerek çalıştırılabilir bir Brian2 Network'ü kurar.
        """
        # BionicSynapse kullandığımızda, .synapses özelliğine erişmemiz gerekiyor
        synapse_object = self.input_to_l1_synapse.synapses if hasattr(self.input_to_l1_synapse, 'synapses') else self.input_to_l1_synapse
            
        all_components = [
            self.input_layer,
            synapse_object
        ]
        all_components.extend(self.layer1.all_objects)
        all_components.extend(monitors)
        
        return Network(all_components)