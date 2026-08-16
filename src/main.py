from pathlib import Path
import yt_dlp

INPUT_DIR = Path("input")
DOWNLOAD_DIR = Path("downloads")

DOWNLOAD_DIR.mkdir(exist_ok=True)

ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": str(DOWNLOAD_DIR / "%(title)s.%(ext)s"),
    "quiet": False,
    "noplaylist": True,
    "force_ipv4": True,
}
txt_files = list(INPUT_DIR.glob("*.txt"))

if not txt_files:
    print("No input files found.")
    exit(0)

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    for txt in txt_files:
        print(f"\nProcessing {txt.name}")

        with open(txt, "r") as f:
            urls = [
                line.strip()
                for line in f
                if line.strip() and not line.startswith("#")
            ]

        for url in urls:
            print(f"Downloading: {url}")
            ydl.download([url])

print("\nDone!")