import re

INPUT_LOG = 'proxy_log.txt'
OUTPUT_ALPHABET = 'alphabet.txt'

def extract_commands():
    seen = set()
    with open(INPUT_LOG, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            cmd = re.match(r'^\w+', line)
            if cmd:
                seen.add(cmd.group(0))
    with open(OUTPUT_ALPHABET, 'w', encoding='utf-8') as out:
        for cmd in sorted(seen):
            out.write(cmd + '\n')
    print(f"[extract_alphabet] saved {len(seen)} commands to {OUTPUT_ALPHABET}")

if __name__ == '__main__':
    extract_commands()
