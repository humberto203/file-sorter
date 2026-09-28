"""
File Sorter CLI
Author: Humberto Martínez López
Description: Organiza automáticamente archivos en un directorio destino 
             agrupándolos por carpetas según su extensión y genera un resumen.
"""

import os
import shutil
import argparse
import json
from pathlib import Path
from typing import Dict, List


CATEGORIES: Dict[str, List[str]] = {
    "Documentos": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv"],
    "Imagenes": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"],
    "Audio_Video": [".mp3", ".wav", ".mp4", ".mkv", ".mov"],
    "Comprimidos": [".zip", ".tar", ".gz", ".rar", ".7z"],
    "Codigo_Scripts": [".py", ".cs", ".kt", ".json", ".sql", ".sh", ".yaml", ".yml"],
}


def get_category(extension: str) -> str:
    ext = extension.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "Otros" if ext else "Sin_Extension"


def organize_directory(target_path: Path, dry_run: bool = False) -> Dict[str, int]:
    if not target_path.exists() or not target_path.is_dir():
        raise ValueError(f"La ruta '{target_path}' no es un directorio válido.")

    summary: Dict[str, int] = {}

    for item in target_path.iterdir():
        # Ignora carpetas y archivos ocultos
        if item.is_dir() or item.name.startswith("."):
            continue

        folder_name = get_category(item.suffix)
        destination_folder = target_path / folder_name
        destination_file = destination_folder / item.name

        if not dry_run:
            destination_folder.mkdir(exist_ok=True)
            # Evita sobreescribir si ya existe un archivo con el mismo nombre
            if destination_file.exists():
                base_name = item.stem
                ext = item.suffix
                counter = 1
                while destination_file.exists():
                    destination_file = destination_folder / f"{base_name}_{counter}{ext}"
                    counter += 1

            shutil.move(str(item), str(destination_file))

        summary[folder_name] = summary.get(folder_name, 0) + 1

    return summary


def main():
    parser = argparse.ArgumentParser(
        description="Organiza tus carpetas caóticas (como Downloads o Desktop) por tipo de archivo."
    )
    parser.add_argument(
        "path",
        type=str,
        help="Ruta absoluta o relativa del directorio a limpiar.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simula la ejecución sin mover ningún archivo físicamente.",
    )
    parser.add_argument(
        "--json-output",
        action="store_true",
        help="Imprime el resumen de resultados en formato JSON.",
    )

    args = parser.parse_args()
    target = Path(args.path).resolve()

    try:
        report = organize_directory(target, dry_run=args.dry_run)

        if args.json_output:
            print(json.dumps(report, indent=2))
            return

        mode = "[SIMULACIÓN]" if args.dry_run else "[COMPLETADO]"
        print(f"\n{mode} Directorio procesado: {target}\n" + "-" * 40)
        if not report:
            print("No se encontraron archivos sueltos para organizar.")
        else:
            for cat, count in sorted(report.items()):
                print(f" • {cat.replace('_', ' ')}: {count} archivo(s)")
        print("-" * 40 + "\n")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()