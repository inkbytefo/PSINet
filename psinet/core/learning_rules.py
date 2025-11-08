# Bu dosya, farklı sinaptik plastisite kurallarını saklayacaktır.

# Basitleştirilmiş STDP Kuralı (sıfıra bölme hatasını önlemek için)
STDP_EQUATION = '''
    w : 1 # Sinaptik ağırlık
    
    # Ateşleme "izleri" (traces) - exponential decay
    dapre/dt = -apre / (taupre + 1e-10*second) : 1 (clock-driven)
    dapost/dt = -apost / (taupost + 1e-10*second) : 1 (clock-driven)
    
    # STDP parametreleri
    taupre : second
    taupost : second
    wmax : 1
    Apre : 1
    Apost : 1
'''

# Ağırlıkların nasıl güncelleneceğini tanımlayan kurallar
STDP_ON_PRE = '''
    v_post += w   # Gelen ateşleme, hedef nöronun potansiyelini artırır
    apre += Apre # Giriş nöronunun ateşleme izini artır
    w = clip(w + apost, 0, wmax) # Ağırlığı, çıkış izine göre güncelle
'''

STDP_ON_POST = '''
    apost += Apost # Çıkış nöronunun ateşleme izini artır
    w = clip(w + apre, 0, wmax) # Ağırlığı, giriş izine göre güncelle
'''