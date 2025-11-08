# Gerekli Brian2 bileşenlerini içe aktaralım
from brian2 import NeuronGroup, ms, pA

# Nöronumuzun davranışını tanımlayan diferansiyel denklem.
# Bu, Leaky Integrate-and-Fire (LIF) modelinin temelidir.
LIF_EQUATION = '''
dv/dt = (I - v) / tau : 1 (unless refractory)
I : 1
tau : second
'''

class BionicNeuron:
    """
    PSINet mimarisinin temel işlem birimi.
    
    Brian2 kütüphanesini kullanarak bir Leaky Integrate-and-Fire (LIF)
    nöron grubunu sarmalar (encapsulates).
    """
    def __init__(self, num_neurons, tau=10*ms, threshold='v > 1.0', reset='v = 0.0', refractory=5*ms):
        """
        Bir grup Biyonik Nöron oluşturur.

        Args:
            num_neurons (int): Bu grupta oluşturulacak nöron sayısı.
            tau (Quantity): Membran potansiyeli sızıntı zaman sabitesi. Unutma hızı.
            threshold (str): Ateşleme koşulu.
            reset (str): Ateşlemeden sonra potansiyelin sıfırlanacağı değer.
            refractory (Quantity): Ateşlemeden sonra nöronun tekrar ateşleyemeyeceği süre.
        """
        # Brian2'nin NeuronGroup'unu kullanarak nöronları yaratıyoruz.
        # Brian2 bu denklemleri alıp arka planda verimli C++ koduna çevirir.
        self.group = NeuronGroup(
            num_neurons,
            model=LIF_EQUATION,
            threshold=threshold,
            reset=reset,
            refractory=refractory,
            method='exact' # Bu basit denklem için en doğru çözücü
        )
        
        # Nöronların parametrelerini ayarlıyoruz
        self.group.tau = tau
        self.num_neurons = num_neurons

    def __repr__(self):
        return f"BionicNeuron(N={self.num_neurons})"