from pathlib import Path
import yt_dlp

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_DIR = BASE_DIR / "input"
DOWNLOAD_DIR = BASE_DIR / "downloads"

# GitHub Actions decrypts the cookies here
COOKIE_FILE = Path.home() / "secrets" / "cookies.txt"

DOWNLOAD_DIR.mkdir(exist_ok=True)

ydl_opts = {
    # Audio only — ideal for your notes/transcription pipeline
    "format": "bestaudio/best",

    # Save downloaded files
    "outtmpl": str(DOWNLOAD_DIR / "%(title)s.%(ext)s"),

    "quiet": False,
    "noplaylist": True,

    # This fixed the 403 on your local machine
    "force_ipv4": True,

    # YouTube authentication cookies
    "cookiefile": str(COOKIE_FILE),
}

txt_files = list(INPUT_DIR.glob("*.txt"))

if not txt_files:
    print(f"No input files found in: {INPUT_DIR}")
    exit(0)

print(f"Found {len(txt_files)} input file(s).")

with yt_dlp.YoutubeDL(ydl_opts) as ydl:

    for txt in txt_files:
        print(f"\nProcessing {txt.name}")

        with open(txt, "r", encoding="utf-8") as f:
            urls = [
                line.strip()
                for line in f
                if line.strip() and not line.strip().startswith("#")
            ]

        print(f"Found {len(urls)} URL(s) in {txt.name}")

        for url in urls:
            print(f"\nDownloading: {url}")

            try:
                ydl.download([url])
                print(f"Successfully downloaded: {url}")

            except Exception as e:
                print(f"FAILED: {url}")
                print(f"Reason: {e}")
                print("Continuing with next URL...")

print("\n========================================")
print("All downloads processed.")
print("========================================")