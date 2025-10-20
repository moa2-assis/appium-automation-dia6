from pathlib import Path
import csv

# Caminho base para todos os CSVs de teste
CSV_DIR = Path(__file__).resolve().parent.parent / "csv_tests"

def _to_int_or_none(value):
    """Converte string para int se possível; retorna None se vazio."""
    if value is None:
        return None
    s = str(value).strip()
    return int(s) if s != "" else None

def load_csv_cases(filename):
    """
    Lê um CSV de dentro de /csv_tests e retorna lista de dicionários.

    - Ignora linhas vazias e comentários (# ...).
    - Converte 'userId' e 'expect_status' para int (ou None).
    - Requer 'expect_status' em todas as linhas válidas.
    """
    path = CSV_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Arquivo CSV não encontrado: {path}")

    cases = []
    with path.open(newline="", encoding="utf-8-sig") as f:
        rows = [line for line in f if line.strip() and not line.lstrip().startswith("#")]
        reader = csv.DictReader(rows)

        for row in reader:
            row = {k: (v if v is not None else "") for k, v in row.items()}
            row["title"] = row.get("title")
            row["body"] = row.get("body")
            row["userId"] = _to_int_or_none(row.get("userId"))

            if not str(row.get("expect_status", "")).strip():
                raise ValueError("Campo 'expect_status' ausente em uma linha do CSV.")

            row["expect_status"] = int(row["expect_status"])
            cases.append(row)

    if not cases:
        raise ValueError(f"Nenhum caso válido encontrado em {filename}.")

    return cases