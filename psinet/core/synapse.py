from brian2 import Synapses, ms
from .learning_rules import STDP_EQUATION, STDP_ON_PRE, STDP_ON_POST

class BionicSynapse:
    """
    Nöron grupları arasında öğrenen bağlantıları yönetir.
    """
    def __init__(self, pre_neurons, post_neurons, tau_pre=20*ms, tau_post=20*ms, 
                 w_max=0.01, A_pre=0.01, A_post=-0.0105):
        """
        STDP öğrenme kuralına sahip bir sinaps grubu oluşturur.

        Args:
            pre_neurons (BionicNeuron): Kaynak nöron grubu.
            post_neurons (BionicNeuron): Hedef nöron grubu.
            tau_pre/tau_post (Quantity): STDP izlerinin zaman sabiteleri.
            w_max (float): Maksimum sinaptik ağırlık.
            A_pre/A_post (float): Her ateşlemede izlerdeki artış/azalış miktarı.
                                  A_post'un A_pre'den biraz daha negatif olması
                                  genellikle daha kararlı bir öğrenme sağlar.
        """
        self.synapses = Synapses(
            pre_neurons.group, 
            post_neurons.group,
            model=STDP_EQUATION,
            on_pre=STDP_ON_PRE,
            on_post=STDP_ON_POST
        )
        
        # Tüm olası bağlantıları kur
        self.synapses.connect()
        
        # Öğrenme parametrelerini ayarla
        self.synapses.taupre = tau_pre
        self.synapses.taupost = tau_post
        self.synapses.wmax = w_max
        self.synapses.Apre = A_pre
        self.synapses.Apost = A_post
    
    def __repr__(self):
        return f"BionicSynapse connecting {self.synapses.source.N} to {self.synapses.target.N} neurons."