"""Batch PDF to markdown via MinerU. Drop PDFs in pdfs_input/, run this script."""
import logging
import subprocess
import sys
from pathlib import Path

# ---- Paths (resolved relative to this script) ----
PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_DIR = PROJECT_ROOT / "pdfs_input"
OUTPUT_DIR = PROJECT_ROOT / "markdown_output"
LOG_DIR = PROJECT_ROOT / "logs"

# ---- MinerU settings (edit here if you want to change behavior) ----
BACKEND = "pipeline"   # "pipeline" = CPU-friendly; "vlm-transformers" = GPU
METHOD = "auto"        # "auto" | "txt" | "ocr"
LANGUAGE = "en"        # OCR language hint

# ---- Setup ----
OUTPUT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)
INPUT_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "parse_run.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)


def already_done(pdf_path: Path) -> bool:
    expected = OUTPUT_DIR / pdf_path.stem / "auto" / f"{pdf_path.stem}.md"
    return expected.exists()

def parse_one(pdf_path: Path) -> bool:
    cmd = [
        "mineru",
        "-p", str(pdf_path),
        "-o", str(OUTPUT_DIR),
        "-b", BACKEND,
        "-m", METHOD,
        "-l", LANGUAGE,
    ]
    log.info(f"CMD: {' '.join(cmd)}")
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    if result.returncode != 0:
        # Log the tail of stderr — usually where the real error is
        log.error(f"mineru exited {result.returncode}")
        log.error(f"stderr (tail): {result.stderr[-2000:]}")
        return False
    return True


def main():
    if not INPUT_DIR.exists():
        log.error(f"Input directory missing: {INPUT_DIR}")
        sys.exit(1)

    pdfs = sorted(INPUT_DIR.glob("*.pdf"), key=lambda p: p.stat().st_size)
    if not pdfs:
        log.warning(f"No PDFs found in {INPUT_DIR}")
        return

    log.info(f"Found {len(pdfs)} PDFs in {INPUT_DIR}")
    log.info(f"Output → {OUTPUT_DIR}")

    done = skipped = failed = 0
    for i, pdf in enumerate(pdfs, 1):
        log.info(f"[{i}/{len(pdfs)}] {pdf.name} ({pdf.stat().st_size / 1024:.0f} KB)")

        if already_done(pdf):
            log.info(f"  SKIP (already parsed)")
            skipped += 1
            continue

        try:
            if parse_one(pdf):
                log.info(f"  DONE")
                done += 1
            else:
                log.error(f"  FAILED")
                failed += 1
        except KeyboardInterrupt:
            log.warning("Interrupted by user")
            break
        except Exception as e:
            log.exception(f"  EXCEPTION: {e}")
            failed += 1

    log.info(f"Summary: done={done} skipped={skipped} failed={failed} total={len(pdfs)}")


if __name__ == "__main__":
    main()