# File Sorte 

Un script ligero en Python para organizar automáticamente directorios desordenados (como descargas o escritorio) clasificando archivos en subcarpetas según su extensión.

## Características

- Cero dependencias externas (usa únicamente la biblioteca estándar de Python 3).
- **Modo seguro (`--dry-run`)**: visualiza los cambios antes de mover cualquier archivo.
- Manejo de colisiones de nombres (agrega sufijos numéricos automáticos).
- Salida formateada en consola o en JSON limpio.

##  Uso

```bash
# Simular organización sin mover archivos
python file_sorter.py ~/Downloads --dry-run

# Ejecutar organización real
python file_sorter.py ~/Downloads

# Obtener resultado en formato JSON
python file_sorter.py ~/Downloads --json-output
```

##  Autor

**Humberto Martínez López**
