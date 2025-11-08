import numpy as np
from brian2 import PoissonGroup, Hz

def image_to_poisson_rates(image, min_rate=0*Hz, max_rate=100*Hz, invert=True):
    """
    Bir görüntü matrisini, piksel yoğunluğuna göre Poisson ateşleme frekanslarına dönüştürür.

    Args:
        image (np.ndarray): 2D numpy dizisi olarak görüntü (genellikle 0-255 arası).
        min_rate (Quantity): En açık piksel için ateşleme frekansı.
        max_rate (Quantity): En koyu piksel için ateşleme frekansı.
        invert (bool): Eğer True ise, daha yüksek piksel değeri (beyaz) daha düşük
                     ateşleme frekansına neden olur (MNIST için ideal).

    Returns:
        np.ndarray: Her piksel için bir ateşleme frekansı (Hz cinsinden) içeren 1D dizi.
    """
    # Görüntüyü 0-1 aralığına normalize et
    image_flat = image.flatten().astype(float)
    image_flat /= 255.0
    
    if invert:
        image_flat = 1.0 - image_flat
        
    # Ateşleme frekanslarını hesapla
    rates = image_flat * (max_rate - min_rate) + min_rate
    return rates

def create_input_layer(rates):
    """
    Verilen ateşleme frekanslarına sahip bir Poisson nöron grubu oluşturur.
    
    Args:
        rates (np.ndarray): Nöronların ateşleme frekansları (Hz).
        
    Returns:
        PoissonGroup: Brian2'nin PoissonGroup nesnesi.
    """
    num_inputs = len(rates)
    input_layer = PoissonGroup(num_inputs, rates=rates)
    return input_layer