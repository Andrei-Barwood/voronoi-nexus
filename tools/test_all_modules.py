#!/usr/bin/env python3
"""
Snocomm Security Suite - Test Runner (Python)
Ejecuta pytest en todos los módulos Snocomm y muestra estadísticas detalladas

Uso:
    python tools/test_all_modules.py
    python tools/test_all_modules.py --verbose
    python tools/test_all_modules.py --quiet
    python tools/test_all_modules.py --modulo <nombre>
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Colores ANSI
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[0;36m'
    MAGENTA = '\033[0;35m'
    NC = '\033[0m'  # No Color
    BOLD = '\033[1m'


def print_header():
    """Imprime el encabezado del script"""
    print(f"{Colors.BLUE}{'═' * 55}{Colors.NC}")
    print(f"{Colors.BLUE}    🧪 TESTING ALL SNOCOMM MODULES{Colors.NC}")
    print(f"{Colors.BLUE}{'═' * 55}{Colors.NC}")
    print()


def print_separator():
    """Imprime un separador visual"""
    print(f"{Colors.BLUE}{'━' * 55}{Colors.NC}")


def ensure_pytest_available() -> bool:
    """
    Verifica que pytest esté disponible en el intérprete actual.
    """
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "--version"],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        return True

    print(f"{Colors.RED}❌ pytest no está instalado en este entorno de Python{Colors.NC}")
    print(f"   Python activo: {sys.executable}")
    print("   Instale dependencias con uno de estos comandos:")
    print("   - python -m pip install pytest")
    print('   - python -m pip install -e ".[dev]"')
    print()
    return False


def find_modulo_tests(project_root: Path) -> List[Tuple[str, Path]]:
    """
    Encuentra todos los archivos test_core.py en los corporate
    
    Returns:
        Lista de tuplas (nombre_modulo, path_test_core.py)
    """
    corporate_dir = project_root / "corporate"
    if not corporate_dir.exists():
        return []
    
    tests = []
    for modulo_dir in sorted(corporate_dir.iterdir()):
        if not modulo_dir.is_dir():
            continue
        
        test_file = modulo_dir / "tests" / "test_core.py"
        if test_file.exists():
            tests.append((modulo_dir.name, test_file))
    
    return tests


def run_pytest(test_file: Path, modulo_dir: Path, verbose: bool = False, quiet: bool = False) -> Tuple[bool, str]:
    """
    Ejecuta pytest en un archivo de test específico
    
    Args:
        test_file: Path al archivo test_core.py
        modulo_dir: Directorio del modulo
        verbose: Si True, muestra output detallado
        quiet: Si True, muestra solo resumen mínimo
    
    Returns:
        Tupla (success, output)
    """
    # Cambiar al directorio del modulo
    original_cwd = os.getcwd()
    os.chdir(modulo_dir)
    
    try:
        # Construir comando pytest
        cmd = [sys.executable, "-m", "pytest", str(test_file)]
        
        if quiet:
            cmd.extend(["-q", "--tb=no"])
        elif verbose:
            cmd.extend(["-v", "--tb=short"])
        else:
            cmd.extend(["-q", "--tb=short"])
        
        # Ejecutar pytest
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutos máximo por modulo
        )
        
        success = result.returncode == 0
        output = result.stdout + result.stderr
        
        return success, output
    except subprocess.TimeoutExpired:
        return False, "⏱️  Timeout: Test tomó más de 5 minutos"
    except Exception as e:
        return False, f"❌ Error ejecutando pytest: {str(e)}"
    finally:
        os.chdir(original_cwd)


def run_tests(
    project_root: Path,
    verbose: bool = False,
    quiet: bool = False,
    specific_modulo: str = None,
    show_output: bool = False
) -> Dict[str, any]:
    """
    Ejecuta todos los tests y retorna estadísticas
    
    Returns:
        Diccionario con estadísticas de los tests
    """
    tests = find_modulo_tests(project_root)
    
    if not tests:
        print(f"{Colors.YELLOW}⚠️  No se encontraron módulos con tests{Colors.NC}")
        return {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "results": {}
        }
    
    # Filtrar por modulo específico si se especifica
    if specific_modulo:
        tests = [(name, path) for name, path in tests if name.lower() == specific_modulo.lower()]
        if not tests:
            print(f"{Colors.RED}❌ No se encontró el módulo: {specific_modulo}{Colors.NC}")
            return {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "skipped": 0,
                "results": {}
            }
    
    stats = {
        "total": len(tests),
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "results": {}
    }
    
    print_separator()
    print(f"📦 Encontrados {Colors.CYAN}{len(tests)}{Colors.NC} módulos con tests\n")
    
    for modulo_name, test_file in tests:
        modulo_dir = test_file.parent.parent
        
        print_separator()
        print(f"📦 Testing: {Colors.YELLOW}{modulo_name}{Colors.NC}")
        print_separator()
        
        success, output = run_pytest(test_file, modulo_dir, verbose, quiet)
        
        if success:
            print(f"{Colors.GREEN}✅ {modulo_name} PASSED{Colors.NC}")
            stats["passed"] += 1
            stats["results"][modulo_name] = {"status": "PASSED", "output": output}
        else:
            print(f"{Colors.RED}❌ {modulo_name} FAILED{Colors.NC}")
            stats["failed"] += 1
            stats["results"][modulo_name] = {"status": "FAILED", "output": output}
            
            # Mostrar output si falló y show_output está activado
            if show_output and output:
                print(f"\n{Colors.RED}Output:{Colors.NC}")
                print(output[:500] + "..." if len(output) > 500 else output)
        
        print()
    
    return stats


def run_integration_tests(project_root: Path, verbose: bool = False, quiet: bool = False) -> bool:
    """Ejecuta los tests de integración si existen"""
    integration_test = project_root / "tests" / "test_integration.py"
    
    if not integration_test.exists():
        return None
    
    print_separator()
    print(f"🔗 Testing: {Colors.YELLOW}Integration Tests{Colors.NC}")
    print_separator()
    
    original_cwd = os.getcwd()
    os.chdir(project_root)
    
    try:
        cmd = [sys.executable, "-m", "pytest", str(integration_test)]
        if quiet:
            cmd.extend(["-q", "--tb=no"])
        elif verbose:
            cmd.extend(["-v", "--tb=short"])
        else:
            cmd.extend(["-q", "--tb=short"])
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        success = result.returncode == 0
        
        if success:
            print(f"{Colors.GREEN}✅ Integration Tests PASSED{Colors.NC}")
        else:
            print(f"{Colors.RED}❌ Integration Tests FAILED{Colors.NC}")
            if not quiet:
                print(result.stdout + result.stderr)
        
        print()
        return success
    except Exception as e:
        print(f"{Colors.RED}❌ Error ejecutando integration tests: {str(e)}{Colors.NC}")
        return False
    finally:
        os.chdir(original_cwd)


def print_summary(stats: Dict[str, any], integration_success: bool = None):
    """Imprime el resumen final de los tests"""
    print_separator()
    print(f"{Colors.BLUE}              📊 RESUMEN DE TESTS{Colors.NC}")
    print_separator()
    
    print(f"Total módulos testeados: {Colors.YELLOW}{stats['total']}{Colors.NC}")
    print(f"Pasaron correctamente:    {Colors.GREEN}{stats['passed']}{Colors.NC}")
    print(f"Fallaron:                 {Colors.RED}{stats['failed']}{Colors.NC}")
    
    if stats['total'] > 0:
        percentage = (stats['passed'] / stats['total']) * 100
        print(f"Tasa de éxito:            {Colors.CYAN}{percentage:.1f}%{Colors.NC}")
    
    if integration_success is not None:
        status = f"{Colors.GREEN}PASSED{Colors.NC}" if integration_success else f"{Colors.RED}FAILED{Colors.NC}"
        print(f"Integration Tests:        {status}")
    
    print_separator()
    
    # Mostrar corporate que fallaron
    if stats['failed'] > 0:
        print(f"\n{Colors.RED}Módulos que fallaron:{Colors.NC}")
        for name, result in stats['results'].items():
            if result['status'] == 'FAILED':
                print(f"  {Colors.RED}❌ {name}{Colors.NC}")
    
    # Mensaje final
    if stats['failed'] == 0 and stats['total'] > 0:
        print(f"\n{Colors.GREEN}🎉 ¡Todos los tests pasaron exitosamente!{Colors.NC}")
    elif stats['total'] == 0:
        print(f"\n{Colors.YELLOW}⚠️  No se encontraron módulos para testear{Colors.NC}")
    else:
        print(f"\n{Colors.RED}💥 Algunos tests fallaron. Revisa los errores arriba.{Colors.NC}")


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description="Ejecuta tests de todos los módulos Snocomm en el proyecto",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python tools/test_all_modules.py
  python tools/test_all_modules.py --verbose
  python tools/test_all_modules.py --quiet
  python tools/test_all_modules.py --modulo lemniscate_anon
  python tools/test_all_modules.py --show-output
        """
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Muestra output detallado de pytest"
    )
    
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Muestra solo resumen mínimo"
    )
    
    parser.add_argument(
        "--modulo", "-d",
        type=str,
        help="Ejecuta tests solo para un módulo específico (nombre de carpeta)"
    )
    
    parser.add_argument(
        "--show-output", "-s",
        action="store_true",
        help="Muestra output de tests que fallan"
    )
    
    parser.add_argument(
        "--no-integration",
        action="store_true",
        help="No ejecuta tests de integración"
    )
    
    args = parser.parse_args()
    
    # Determinar el directorio raíz del proyecto
    script_path = Path(__file__).resolve()
    project_root = script_path.parent.parent
    
    if not (project_root / "corporate").exists():
        print(f"{Colors.RED}❌ Error: No se encuentra la carpeta 'corporate'{Colors.NC}")
        print("Ejecuta este script desde la raíz del proyecto o desde tools/")
        sys.exit(1)

    # Verificar pytest antes de ejecutar cientos de tests.
    if not ensure_pytest_available():
        sys.exit(1)
    
    # Ejecutar tests
    print_header()
    stats = run_tests(
        project_root,
        verbose=args.verbose,
        quiet=args.quiet,
        specific_modulo=args.modulo,
        show_output=args.show_output
    )
    
    # Ejecutar tests de integración
    integration_success = None
    if not args.no_integration:
        integration_success = run_integration_tests(
            project_root,
            verbose=args.verbose,
            quiet=args.quiet
        )
    
    # Mostrar resumen
    print_summary(stats, integration_success)
    
    # Exit code basado en resultados
    if stats['failed'] == 0 and stats['total'] > 0:
        if integration_success is False:
            sys.exit(1)
        sys.exit(0)
    elif stats['total'] == 0:
        sys.exit(1)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
