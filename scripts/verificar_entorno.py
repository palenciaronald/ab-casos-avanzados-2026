"""Comprueba que tu proyecto está listo para trabajar y te dice qué falta.

Uso (desde la raíz de tu repositorio, con el entorno activado):

    python scripts/verificar_entorno.py

Cada línea empieza con:
  OK     todo bien
  AVISO  funciona, pero conviene revisarlo (no bloquea)
  FALTA  hay que arreglarlo antes de seguir

Termina con código 1 si hay algún FALTA. No cambia nada en tu proyecto.
"""
import importlib
import os
import subprocess
import sys
from pathlib import Path

# La consola de Windows usa cp1252: sin esto, un carácter raro rompe el script.
for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
PLACEHOLDERS = ("nombre-de-tu-perfil", "pega-aqui", "TU-WORKSPACE", "tu-correo")
REQUIRED_PACKAGES = {
    "pandas": "pandas",
    "numpy": "numpy",
    "sklearn": "scikit-learn",
    "mlflow": "mlflow",
    "streamlit": "streamlit",
    "joblib": "joblib",
    "pytest": "pytest",
    "dotenv": "python-dotenv",
    "databricks.sdk": "databricks-sdk",
}
EXPECTED_DIRS = ["data/raw", "data/processed", "notebooks", "src", "tests", "models", "app", "reports", "presentacion", "scripts"]
EXPECTED_FILES = ["CLAUDE.md", "especificacion-proyecto.md", "requirements.txt", ".gitignore", ".env.example"]

results = []  # (nivel, texto, pista)


def add(level: str, text: str, hint: str = "") -> None:
    results.append((level, text, hint))


def find_env() -> Path | None:
    for candidate in (ROOT / ".env", ROOT.parent / ".env"):
        if candidate.exists():
            return candidate
    return None


def check_python() -> None:
    v = sys.version_info
    if (v.major, v.minor) == (3, 12):
        add("OK", f"Python {v.major}.{v.minor}.{v.micro}")
    else:
        add("AVISO", f"Python {v.major}.{v.minor}: el curso usa 3.12",
            "Crea el entorno con: uv venv --python 3.12  (guía de instalación, sección 4)")
    if sys.prefix == sys.base_prefix:
        add("AVISO", "No parece que el entorno virtual esté activado",
            "Actívalo: .venv\\Scripts\\activate (Windows) o source .venv/bin/activate (Mac/Linux)")


def check_packages() -> None:
    missing = []
    for module, package in REQUIRED_PACKAGES.items():
        try:
            importlib.import_module(module)
        except Exception:
            missing.append(package)
    if missing:
        add("FALTA", "Paquetes sin instalar: " + ", ".join(missing), "Ejecuta: uv pip install -r requirements.txt")
    else:
        add("OK", f"{len(REQUIRED_PACKAGES)} paquetes principales instalados")


def check_env_file() -> dict:
    env_path = find_env()
    if env_path is None:
        add("FALTA", "No existe el archivo .env", "Copia .env.example como .env y complétalo (guía de instalación, sección 7)")
        return {}
    text = env_path.read_text(encoding="utf-8", errors="replace")
    values = {}
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            values[key.strip()] = value.strip()
    if any(p in text for p in PLACEHOLDERS if not any(l.strip().startswith("#") and p in l for l in text.splitlines())):
        add("AVISO", ".env todavía tiene valores de ejemplo", "Reemplaza los textos de ejemplo por tus datos reales")
    else:
        add("OK", ".env presente y sin valores de ejemplo")
    ignored = ROOT / ".gitignore"
    if ignored.exists() and ".env" in ignored.read_text(encoding="utf-8", errors="replace").splitlines():
        add("OK", ".env está en .gitignore (no se subirá a GitHub)")
    else:
        add("FALTA", ".env NO está en .gitignore", "Agrega una línea .env al archivo .gitignore: si lo subes, expones tus credenciales")
    return values


def check_databricks(values: dict) -> None:
    profile = values.get("PROFILE", "")
    has_profile = bool(profile) and profile not in PLACEHOLDERS
    has_token = bool(values.get("DATABRICKS_HOST")) and bool(values.get("DATABRICKS_TOKEN")) and "pega-aqui" not in values.get("DATABRICKS_TOKEN", "")
    if not (has_profile or has_token):
        add("AVISO", "Databricks sin configurar: se usará MLflow local",
            "Funciona igual para el curso. Para conectar, completa PROFILE o DATABRICKS_HOST y DATABRICKS_TOKEN en .env")
        return
    try:
        import warnings
        import mlflow

        warnings.filterwarnings("ignore")
        if has_profile:
            mlflow.set_tracking_uri(f"databricks://{profile}")
        else:
            os.environ["DATABRICKS_HOST"] = values["DATABRICKS_HOST"]
            os.environ["DATABRICKS_TOKEN"] = values["DATABRICKS_TOKEN"]
            mlflow.set_tracking_uri("databricks")
        mlflow.search_experiments(max_results=1)
        add("OK", "Conexión con Databricks funcionando")
    except Exception as error:
        reason = str(error).splitlines()[0][:110]
        add("AVISO", f"No conecta con Databricks ({reason})",
            "Revisa el token o el perfil, o el CLI en el PATH. Mientras tanto se usa MLflow local y todo sigue funcionando")
    folder = values.get("EXPERIMENT_DIR", "")
    if folder and folder not in PLACEHOLDERS and not folder.endswith("tu-carpeta"):
        add("OK", f"Carpeta de experimentos definida: {folder}")
    else:
        add("AVISO", "No definiste EXPERIMENT_DIR (carpeta de Databricks para tus experimentos)",
            "Crea una carpeta en tu workspace y pon su ruta en .env como EXPERIMENT_DIR=...")


def check_structure() -> None:
    missing_dirs = [d for d in EXPECTED_DIRS if not (ROOT / d).is_dir()]
    missing_files = [f for f in EXPECTED_FILES if not (ROOT / f).exists()]
    if missing_dirs or missing_files:
        add("FALTA", "Estructura del repo incompleta: " + ", ".join(missing_dirs + missing_files),
            "Revisa que clonaste la rama base completa (ver LEEME-PRIMERO.md)")
    else:
        add("OK", "Estructura del repo completa (carpetas y archivos de la plantilla)")
    src = ROOT / "src"
    packages = [p.name for p in src.iterdir() if p.is_dir() and (p / "__init__.py").exists()] if src.is_dir() else []
    if packages:
        add("OK", f"Paquete en src/: {', '.join(packages)}")
    else:
        add("FALTA", "No hay ningún paquete dentro de src/", "Debe existir src/<nombre>/__init__.py")


def check_spec() -> None:
    spec = ROOT / "especificacion-proyecto.md"
    if not spec.exists():
        return
    text = spec.read_text(encoding="utf-8", errors="replace")
    blanks = text.count("_______________")
    empty_rows = sum(1 for line in text.splitlines() if line.strip() in ("| | |", "| | | |"))
    if blanks + empty_rows > 3:
        add("AVISO", f"especificacion-proyecto.md tiene {blanks + empty_rows} campos en blanco",
            "Complétala con tu ficha de caso: Claude la lee antes de generar código")
    else:
        add("OK", "especificacion-proyecto.md completada")


def check_git() -> None:
    if not (ROOT / ".git").exists():
        add("FALTA", "La carpeta no es un repositorio de Git", "Clona tu repositorio de GitHub o ejecuta: git init")
        return
    try:
        remotes = subprocess.run(["git", "remote", "-v"], cwd=ROOT, capture_output=True, text=True).stdout
    except FileNotFoundError:
        add("FALTA", "Git no está instalado", "Guía de instalación, sección 3")
        return
    if "origin" in remotes:
        add("OK", "Git conectado a GitHub (origin)")
    else:
        add("AVISO", "El repositorio no tiene remoto (origin)", "Crea el repo en GitHub y conéctalo: git remote add origin <url>")


def check_data() -> None:
    raw = ROOT / "data" / "raw"
    files = [f for f in raw.iterdir() if f.is_file() and f.name != ".gitkeep"] if raw.is_dir() else []
    if files:
        add("OK", f"Datos en data/raw: {', '.join(f.name for f in files[:3])}")
    else:
        add("AVISO", "data/raw está vacía", "Descarga tu dataset y guárdalo en data/raw/ (no se modifica nunca)")


def main() -> int:
    check_python()
    check_packages()
    values = check_env_file()
    check_databricks(values)
    check_structure()
    check_spec()
    check_git()
    check_data()

    print(f"Verificación del proyecto en: {ROOT}\n")
    for level, text, hint in results:
        print(f"{level:<6} {text}")
        if hint and level != "OK":
            print(f"       -> {hint}")
    counts = {k: sum(1 for r in results if r[0] == k) for k in ("OK", "AVISO", "FALTA")}
    print(f"\nResumen: {counts['OK']} OK · {counts['AVISO']} avisos · {counts['FALTA']} por arreglar")
    if counts["FALTA"]:
        print("Arregla los FALTA y vuelve a ejecutar el script.")
        return 1
    print("Listo para trabajar." if not counts["AVISO"] else "Puedes trabajar; revisa los avisos cuando puedas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
