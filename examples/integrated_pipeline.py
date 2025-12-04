"""
Demostración del Security Pipeline Integrado

Este script muestra cómo Thirstmon y Bandidmon trabajan juntos
para proteger el tráfico web de amenazas y datos sensibles.
"""

import sys
import os

# Agregar shared al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from shared.pipeline import SecurityPipeline


def print_header(text):
    """Helper para imprimir headers bonitos"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)


def print_result(result):
    """Helper para imprimir resultados de forma legible"""
    print(f"\n🔍 STATUS: {result['status']}")
    print(f"📊 Phase Completed: {result['phase_completed']}")
    print("\n--- SUMMARY ---")
    for key, value in result['summary'].items():
        print(f"  • {key}: {value}")


def demo_safe_traffic():
    """Demo 1: Tráfico seguro (pasa ambas fases)"""
    print_header("DEMO 1: Tráfico Seguro con Datos Sensibles")
    
    pipeline = SecurityPipeline()
    
    # URLs seguras
    urls = [
        "google.com",
        "github.com",
        "stackoverflow.com"
    ]
    
    # Contenido con datos sensibles
    content = """
    Email de trabajo: admin@empresa.com
    Tarjeta de crédito: 1234-5678-9012-3456
    
    Este es un email legítimo pero contiene datos que deben protegerse.
    """
    
    result = pipeline.process_traffic(urls, content)
    print_result(result)
    
    if result['status'] == 'SAFE':
        print("\n✅ CONTENIDO SEGURO (redactado):")
        print(result['summary']['safe_content'])


def demo_malicious_traffic():
    """Demo 2: Tráfico malicioso (bloqueado en Fase 1)"""
    print_header("DEMO 2: Tráfico Malicioso Detectado")
    
    pipeline = SecurityPipeline()
    
    # URLs con amenazas
    urls = [
        "google.com",
        "evil-snake-oil.com",      # ⚠️ Amenaza
        "malware-download.net"     # ⚠️ Amenaza
    ]
    
    content = "Este contenido nunca será procesado porque las URLs son maliciosas."
    
    result = pipeline.process_traffic(urls, content)
    print_result(result)
    
    if result['status'] == 'BLOCKED':
        print("\n🚫 URLs BLOQUEADAS:")
        for url in result['summary']['blocked_urls']:
            print(f"  ❌ {url}")


def demo_pipeline_info():
    """Demo 3: Información del pipeline"""
    print_header("DEMO 3: Información del Pipeline")
    
    pipeline = SecurityPipeline()
    info = pipeline.get_pipeline_info()
    
    print(f"\n📦 Pipeline Version: {info['pipeline_version']}")
    print("\n🤖 Digimons Activos:")
    for digimon in info['digimons_active']:
        print(f"  • {digimon['name']} ({digimon['role']}) - Status: {digimon['status']}")
    
    print("\n🔄 Fases del Pipeline:")
    for phase in info['phases']:
        print(f"  {phase}")


def main():
    """Ejecutar todas las demos"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║   🎮 DIGIMON SECURITY SUITE - INTEGRATED PIPELINE        ║
    ║   Thirstmon + Bandidmon trabajando juntos                ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Ejecutar demos
    demo_pipeline_info()
    demo_safe_traffic()
    demo_malicious_traffic()
    
    print("\n" + "="*60)
    print("✅ Demos completadas exitosamente")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
