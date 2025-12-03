"""
Basic usage example for Thirstmon
"""

import sys
# Aseguramos que python encuentre el paquete src
sys.path.insert(0, '../src')

from thirstmon.core import Thirstmon
from thirstmon.utils import setup_logging

def main():
    # 1. Configurar Logs
    setup_logging(level="INFO")
    
    # 2. Crear instancia del Digimon
    digimon = Thirstmon()
    
    print("\n=== 1. Información del Digimon ===")
    info = digimon.get_info()
    for key, value in info.items():
        print(f"{key}: {value}")
    
    # 3. Datos de tráfico simulado (mezcla de buenos y malos)
    traffic_sample = [
        "google.com",
        "github.com",
        "evil-snake-oil.com",      # ¡Amenaza!
        "stackoverflow.com",
        "192.168.66.6",            # ¡Amenaza!
        "python.org"
    ]
    
    print(f"\n=== 2. Validando Input ({len(traffic_sample)} items) ===")
    is_valid = digimon.validate(traffic_sample)
    print(f"¿Datos válidos?: {is_valid}")
    
    if is_valid:
        print("\n=== 3. Ejecutando Análisis de Amenazas ===")
        result = digimon.analyze(traffic_sample)
        
        # Mostrar resultados de forma bonita
        data = result["data"]
        print(f"Status: {result['message']}")
        print(f"Total escaneado: {data['total_scanned']}")
        
        print("\n[!] AMENAZAS DETECTADAS:")
        for threat in data['threats_detected']:
            print(f"    ❌ {threat}")
            
        print("\n[ok] TRÁFICO LIMPIO:")
        for clean in data['clean_traffic']:
            print(f"    ✅ {clean}")

if __name__ == "__main__":
    main()
