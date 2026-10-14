"""Smoke test: verifica que los 4 agentes funcionen sin errores."""
import pandas as pd
from agents.orchestrator import Orchestrator

print("🧪 Iniciando smoke test...")

# Cargar datos de ejemplo
df = pd.read_csv('sample_data.csv')
print(f"✓ Datos cargados: {len(df)} filas × {len(df.columns)} columnas")

# Ejecutar orquestador
orchestrator = Orchestrator()
print("✓ Orquestador inicializado")

results = orchestrator.run_analysis(df, target_col=None)
print("✓ Análisis completado")

# Verificar resultados
errors = []
for branch, result in results.items():
    if result.error:
        errors.append(f"{branch}: {result.error}")
        print(f"✗ {branch}: ERROR - {result.error}")
    else:
        print(f"✓ {branch}: OK")
        print(f"  - Hallazgos: {len(result.findings)}")
        print(f"  - Métricas: {len(result.metrics)}")
        print(f"  - Figuras: {len(result.figures)}")

# Generar informe
report = orchestrator.generate_executive_report(results)
print(f"\n✓ Informe ejecutivo generado")
print(f"  - Hallazgos clave: {len(report['key_findings'])}")
print(f"  - Advertencias: {len(report['warnings'])}")
print(f"  - Recomendaciones: {len(report['recommendations'])}")

if errors:
    print(f"\n❌ FALLÓ: {len(errors)} agentes con errores")
    for error in errors:
        print(f"  - {error}")
    exit(1)
else:
    print("\n✅ SMOKE TEST EXITOSO: Todos los agentes funcionan correctamente")
    exit(0)
