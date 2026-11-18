from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]

def check():
    manifest=json.loads((ROOT/'MANIFEST.sha256.json').read_text())
    for rel,expected in manifest.items():
        p=ROOT/rel
        if not p.is_file(): raise SystemExit('Missing file: '+rel)
        actual=hashlib.sha256(p.read_bytes()).hexdigest()
        if actual!=expected: raise SystemExit('Checksum mismatch: '+rel)
    print(f'PASS: {len(manifest)} static files match SHA-256 manifest. Generated results are excluded.')

if __name__=='__main__':check()
