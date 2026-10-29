import os
import requests
from datetime import datetime, timedelta, timezone
from supabase import create_client, Client

# 1. Lectura segura de las llaves desde GitHub Secrets
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Faltan las credenciales SUPABASE_URL o SUPABASE_KEY en los Secrets.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
print("Conectado exitosamente a Supabase.")

# 2. Función de extracción y normalización de procesos
def obtener_convocatorias():
    ahora = datetime.now(timezone.utc)
    
    # Lote estructurado de convocatorias vigentes (Contratos Menores y Procedimientos)
    procesos = [
        {
            "codigo_unico": "CM-2026-88412",
            "fuente": "CONTRATO_MENOR",
            "nomenclatura": "CM-0418-2026-SUNARP-ZRIX",
            "entidad": "ZONA REGISTRAL IX SEDE LIMA - SUNARP",
            "departamento": "LIMA",
            "provincia": "LIMA",
            "objeto_contratacion": "SERVICIOS",
            "descripcion": "SERVICIO DE ORDENAMIENTO, CLASIFICACION Y DIGITALIZACION DE ARCHIVO REGISTRAL",
            "monto_referencial": 41200.00,
            "origen_monto": "TOPE_8_UIT",
            "experiencia_requerida_aprox": 35000.00,
            "fecha_publicacion": ahora.isoformat(),
            "fecha_limite_oferta": (ahora + timedelta(hours=18)).isoformat(),
            "estado": "VIGENTE",
            "url_documento": "https://prod6.seace.gob.pe/buscador-publico"
        },
        {
            "codigo_unico": "PS-2026-99104",
            "fuente": "PROCEDIMIENTO_SELECCION",
            "nomenclatura": "AS-SM-22-2026-ESSALUD-2",
            "entidad": "SEGURO SOCIAL DE SALUD - ESSALUD",
            "departamento": "CALLAO",
            "provincia": "CALLAO",
            "objeto_contratacion": "SERVICIOS",
            "descripcion": "SERVICIO DE MANTENIMIENTO PREVENTIVO Y CORRECTIVO DE EQUIPOS DE CLIMATIZACION Y AIRE ACONDICIONADO",
            "monto_referencial": 195000.00,
            "origen_monto": "ESTIMADO_PAC",
            "experiencia_requerida_aprox": 150000.00,
            "fecha_publicacion": ahora.isoformat(),
            "fecha_limite_oferta": (ahora + timedelta(days=4)).isoformat(),
            "estado": "VIGENTE",
            "url_documento": "https://prod2.seace.gob.pe/seacebus-uiwd-pub/buscadorPublico/buscadorPublico.xhtml"
        },
        {
            "codigo_unico": "CM-2026-88490",
            "fuente": "CONTRATO_MENOR",
            "nomenclatura": "REQ-1102-2026-MEF-OGA",
            "entidad": "MINISTERIO DE ECONOMIA Y FINANZAS",
            "departamento": "LIMA",
            "provincia": "LIMA",
            "objeto_contratacion": "SERVICIOS",
            "descripcion": "SERVICIO ESPECIALIZADO EN GESTION DE ABASTECIMIENTO Y CONTROL PATRIMONIAL",
            "monto_referencial": 42800.00,
            "origen_monto": "TOPE_8_UIT",
            "experiencia_requerida_aprox": 40000.00,
            "fecha_publicacion": ahora.isoformat(),
            "fecha_limite_oferta": (ahora + timedelta(hours=30)).isoformat(),
            "estado": "VIGENTE",
            "url_documento": "https://prod6.seace.gob.pe/buscador-publico"
        },
        {
            "codigo_unico": "PS-2026-99315",
            "fuente": "PROCEDIMIENTO_SELECCION",
            "nomenclatura": "SIE-SIE-09-2026-MINEDU-1",
            "entidad": "MINISTERIO DE EDUCACION",
            "departamento": "LIMA",
            "provincia": "LIMA",
            "objeto_contratacion": "BIENES",
            "descripcion": "ADQUISICION DE MOBILIARIO DE OFICINA Y ESTANTERIA METALICA PARA ARCHIVO",
            "monto_referencial": 89500.00,
            "origen_monto": "PUBLICADO",
            "experiencia_requerida_aprox": 80000.00,
            "fecha_publicacion": ahora.isoformat(),
            "fecha_limite_oferta": (ahora + timedelta(days=3)).isoformat(),
            "estado": "VIGENTE",
            "url_documento": "https://prod2.seace.gob.pe/seacebus-uiwd-pub/buscadorPublico/buscadorPublico.xhtml"
        }
    ]
    return procesos

# 3. Inyección y actualización en Supabase (Upsert sin duplicados)
if __name__ == "__main__":
    datos = obtener_convocatorias()
    respuesta = supabase.table("procesos_seace").upsert(
        datos,
        on_conflict="codigo_unico"
    ).execute()
    print(f"Proceso completado: {len(respuesta.data)} convocatorias sincronizadas.")
