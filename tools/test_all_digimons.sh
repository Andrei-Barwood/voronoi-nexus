#!/bin/bash

################################################################################
# DIGIMON CYBERSECURITY SUITE - Test Runner
# Ejecuta pytest en todos los Digimons y muestra estadísticas
################################################################################

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Contadores
total_digimons=0
passed_digimons=0
failed_digimons=0

echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}    🧪 TESTING ALL DIGIMONS - DIGIMON SEC SUITE${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""

# Navegar al directorio base del proyecto (donde está tools/)
cd "$(dirname "$0")/.." || exit 1

# Verificar si existe la carpeta digimons
if [ ! -d "digimons" ]; then
    echo -e "${RED}❌ Error: No se encuentra la carpeta 'digimons'${NC}"
    echo "Ejecuta este script desde la raíz del proyecto."
    exit 1
fi

# Iterar sobre cada Digimon
for digimon_dir in digimons/*/; do
    # Extraer nombre del Digimon
    digimon_name=$(basename "$digimon_dir")
    
    # Verificar que tiene tests
    if [ ! -d "$digimon_dir/tests" ]; then
        echo -e "${YELLOW}⚠️  $digimon_name - No tiene carpeta tests, saltando...${NC}"
        continue
    fi
    
    total_digimons=$((total_digimons + 1))
    
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "📦 Testing: ${YELLOW}$digimon_name${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    # Cambiar al directorio del Digimon
    cd "$digimon_dir" || continue
    
    # Ejecutar pytest (silenciar output detallado, solo mostrar resumen)
    if pytest -q --tb=short 2>&1; then
        echo -e "${GREEN}✅ $digimon_name PASSED${NC}"
        passed_digimons=$((passed_digimons + 1))
    else
        echo -e "${RED}❌ $digimon_name FAILED${NC}"
        failed_digimons=$((failed_digimons + 1))
    fi
    
    # Volver al directorio raíz
    cd - > /dev/null || exit 1
    echo ""
done


# Tests de integración
if [ -f "tests/test_integration.py" ]; then
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "🔗 Testing: ${YELLOW}Integration Tests${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    if pytest tests/test_integration.py -q --tb=short 2>&1; then
        echo -e "${GREEN}✅ Integration Tests PASSED${NC}"
    else
        echo -e "${RED}❌ Integration Tests FAILED${NC}"
    fi
    echo ""
fi


# Mostrar resumen final
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}              📊 RESUMEN DE TESTS${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "Total Digimons testeados: ${YELLOW}$total_digimons${NC}"
echo -e "Pasaron correctamente:    ${GREEN}$passed_digimons${NC}"
echo -e "Fallaron:                 ${RED}$failed_digimons${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"

# Exit code basado en resultados
if [ $failed_digimons -eq 0 ] && [ $total_digimons -gt 0 ]; then
    echo -e "${GREEN}🎉 ¡Todos los tests pasaron exitosamente!${NC}"
    exit 0
elif [ $total_digimons -eq 0 ]; then
    echo -e "${YELLOW}⚠️  No se encontraron Digimons para testear${NC}"
    exit 1
else
    echo -e "${RED}💥 Algunos tests fallaron. Revisa los errores arriba.${NC}"
    exit 1
fi
