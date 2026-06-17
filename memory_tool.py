#!/usr/bin/env python3
# memory_tool.py - Standalone System Memory (Prototype 1)
# Identity: [AI_NAME] ([WORKSPACE])
# Folder system: kenangan/ (default, bisa diubah di config.json)

import json, sys, os, argparse, time
from datetime import date, datetime

SYSTEM_DIR = "kenangan"
CONFIG_FILE = "config.json"
IDENTITY_FILE = "SIAPA_AKU.md"
MEMORY_FILE = "memory.json"
LOGS_DIR = "logs"
SIGNATURE = '# LOG v2 -- APPEND ONLY -- jangan edit langsung\n'
CONVERSATION_FILE = 'conversation.md'
EXPORT_FILE = 'memory.md'
AUTO_BACKUP_DIR = '.auto_backup'
INSTRUCTION_MULAI = 'MULAI.md'
INSTRUCTION_ALUR = 'ALUR.md'
INSTRUCTION_SISTEM = 'SISTEM.md'

# ─── Flow Enforcement ────────────────────────────────────────────
FLOW_FILE = 'flow_state.json'
FLOW_TIMEOUT = 300

def flow_read():
    try:
        with open(sys_path(FLOW_FILE), 'r') as f:
            state = json.load(f)
            if 'skip_count' not in state:
                state['skip_count'] = 0
            return state
    except:
        return {'step': 'idle', 'ts': 0, 'last_input': '', 'skip_count': 0}

def flow_write(step, last_input='', reset_skip=False, step_content=None):
    prev = flow_read()
    state = {
        'step': step, 'ts': time.time(),
        'last_input': last_input[:200],
        'skip_count': 0 if reset_skip else prev.get('skip_count', 0)
    }
    if step_content:
        state['step_content'] = step_content[:200]
    elif 'step_content' in prev:
        state['step_content'] = prev['step_content']
    write_json(sys_path(FLOW_FILE), state)

def flow_check(expected_steps, cmd_name, cmd_type=None):
    state = flow_read()
    elapsed = time.time() - state['ts']
    skip_count = state.get('skip_count', 0)
    if elapsed > FLOW_TIMEOUT and state['step'] != 'idle':
        flow_write('idle', reset_skip=True)
        state = {'step': 'idle', 'ts': 0, 'last_input': '', 'skip_count': 0}
        skip_count = 0
    current = state['step']
    step_names = {
        'idle': 'idle', 'input': '1 input',
        'search_before_hypothesis': '2 baca_ulang',
        'hypothesis': '3 praduga',
        'search_before_response': '4 baca_ulang_lagi',
        'evaluation': '5 evaluasi'
    }
    skip_patterns = []
    if current == 'input' and cmd_type in ('hypothesis',):
        skip_patterns.append(('langsung_praduga', 'Langsung praduga tanpa baca ulang! Cari memory dulu (search).'))
    elif current == 'hypothesis' and cmd_type in ('learning', 'verification', 'decision', 'configuration'):
        skip_patterns.append(('langsung_evaluasi', 'Langsung evaluasi tanpa baca ulang! Cari memory dulu (search).'))
    warned = False
    if skip_patterns:
        warned = True
        skip_count += 1
        _, msg = skip_patterns[0]
        print(f'  [!] [{cmd_name}] Flow: {msg}')
        if skip_count >= 2:
            print(f'       Skip ke-{skip_count} dalam sesi ini.')
    if not skip_patterns and current not in expected_steps:
        warned = True
        skip_count += 1
        if current == 'idle' and cmd_name != 'user':
            print(f'  [!] [{cmd_name}] Flow: Belum catat input user! Jalankan user dulu.')
        elif current == 'evaluation' and cmd_name == 'user':
            print(f'  [!] [{cmd_name}] Flow: Catat dulu log narasi sebelum input baru.')
        else:
            print(f'  [!] [{cmd_name}] Flow: Loncat dari {step_names.get(current, current)}.')
        if skip_count >= 2:
            print(f'       Skip ke-{skip_count} dalam sesi ini.')
    if warned:
        final = flow_read()
        final['skip_count'] = final.get('skip_count', 0) + 1
        write_json(sys_path(FLOW_FILE), final)
    return not warned

def flow_show():
    state = flow_read()
    step = state['step']
    next_map = {
        'idle': '1 input (user)', 'input': '2 baca_ulang (search)',
        'search_before_hypothesis': '3 praduga (add --type hypothesis)',
        'hypothesis': '4 baca_ulang_lagi (search)',
        'search_before_response': '5 evaluasi (add --type learning)',
        'evaluation': '6 log (log)'
    }
    print(f'  Langkah selanjutnya: {next_map.get(step, "?")}')
    skip = state.get('skip_count', 0)
    if skip > 0:
        print(f'  Skip count sesi ini: {skip}')

_ROOT = None

def detect_root(start=None):
    if start is None:
        start = os.getcwd()
    path = os.path.abspath(start)
    while True:
        if os.path.isdir(os.path.join(path, SYSTEM_DIR)):
            return path
        if os.path.isfile(os.path.join(path, SYSTEM_DIR, CONFIG_FILE)):
            return path
        parent = os.path.dirname(path)
        if parent == path:
            return None
        path = parent

def ensure_root(create=False):
    global _ROOT
    if _ROOT:
        return _ROOT
    _ROOT = detect_root()
    if _ROOT is None and create:
        _ROOT = os.path.dirname(os.path.abspath(__file__))
        os.makedirs(sys_path(), exist_ok=True)
    return _ROOT

def sys_path(*parts):
    return os.path.join(ensure_root(), SYSTEM_DIR, *parts)

def now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def today():
    return date.today().isoformat()

def read_json(path):
    if not os.path.exists(path):
        return None
    for enc in ('utf-8-sig', 'utf-8', 'utf-16'):
        try:
            with open(path, encoding=enc) as f:
                return json.load(f)
        except (json.JSONDecodeError, UnicodeError):
            continue
    return None

def _auto_backup(path):
    if not os.path.exists(path):
        return
    backup_dir = os.path.join(os.path.dirname(path), AUTO_BACKUP_DIR)
    os.makedirs(backup_dir, exist_ok=True)
    fname = os.path.basename(path)
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    import shutil
    shutil.copy2(path, os.path.join(backup_dir, f'{ts}_{fname}'))

def write_json(path, data):
    _auto_backup(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_config():
    path = sys_path(CONFIG_FILE)
    cfg = read_json(path)
    if cfg is None:
        return {
            "identity": {"ai_name": "Bupen", "owner": "", "role": "System Memory - menyimpan ingatan"},
            "workspace": {"name": "Sekolah"},
            "system": {"folder_name": "kenangan", "inisialisasi": None}
        }
    if 'ai_name' in cfg:
        cfg = {
            "identity": {
                "ai_name": cfg.get("ai_name", "Bupen"),
                "owner": cfg.get("owner", ""),
                "role": cfg.get("role", "System Memory")
            },
            "workspace": {"name": cfg.get("workspace", "Sekolah")},
            "system": {
                "folder_name": cfg.get("system_folder", "kenangan"),
                "inisialisasi": cfg.get("inisialisasi", None)
            }
        }
    return cfg

def save_config(cfg):
    write_json(sys_path(CONFIG_FILE), cfg)

def identity_name():
    return load_config().get("identity", {}).get("ai_name", "Bupen")

def _cfg_id(cfg, key, default=''):
    return cfg.get("identity", {}).get(key, default)

def _cfg_ws(cfg, key, default=''):
    return cfg.get("workspace", {}).get(key, default)

def _cfg_sys(cfg, key, default=''):
    return cfg.get("system", {}).get(key, default)

def generate_identity_file():
    cfg = load_config()
    ai = _cfg_id(cfg, "ai_name", "AI")
    owner = _cfg_id(cfg, "owner", "(belum diatur)")
    ws = _cfg_ws(cfg, "name", "(belum diatur)")
    role = _cfg_id(cfg, "role", "System Memory")
    folder = _cfg_sys(cfg, "folder_name", "kenangan")
    lines = [
        f"Kamu adalah {ai} — system memory untuk workspace {ws}.",
        f"Pemilik: {owner}. Folder system: {folder}.",
        "Gunakan perintah di bawah untuk menyimpan dan mencari ingatan.",
        "Ikuti alur: catat input user dulu, cari memory, baru respon.",
        "",
        f"# SIAPA AKU - {ai}",
        "",
        f"Nama: {ai}",
        f"Pemilik: {owner}",
        f"Workspace: {ws}",
        f"Peran: {role}",
        "",
        "## System Memory",
        f"Folder system: {folder}",
        "",
        "### Perintah",
        "  python memory_tool.py add \"isi memori\" --tags tag1,tag2 --type decision",
        "  python memory_tool.py search \"kata kunci\"",
        "  python memory_tool.py list",
        "  python memory_tool.py log \"narasi kegiatan\"",
        "  python memory_tool.py user \"input user\"",
        "  python memory_tool.py stats",
        "  python memory_tool.py generate-identity",
        "",
        f"---",
        f"Dibuat: {now()}",
        "AUTO-GENERATED - jangan edit manual. Edit config.json lalu regenerate."
    ]
    path = sys_path(IDENTITY_FILE)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    return path

def generate_instruction_set():
    cfg = load_config()
    ai = _cfg_id(cfg, "ai_name", "AI")
    folder = _cfg_sys(cfg, "folder_name", "kenangan")
    ts = now()

    mulai_lines = [
        "# MULAI — Startup & Aturan",
        "",
        "## ATURAN WAJIB",
        "- Kamu hanya akses file di workspace ini.",
        "- JANGAN edit file .md/.json di luar kenangan/.",
        "- JANGAN cari konteks dari luar workspace.",
        "",
        "## URUTAN MULAI",
        "1. Baca ALUR.md — pahami alur WAJIB 6 langkah.",
        "2. Baca SISTEM.md — pahami tool & file.",
        "3. Baca SIAPA_AKU.md — siapa kamu.",
        "4. Cari memory: `python memory_tool.py search [topik]`",
        "5. Baca log terbaru: `kenangan/logs/`",
        "6. Sampaikan ke user: siap.",
        "",
        "## JIKA BELUM INIT",
        "- Kamu netral (belum init).",
        "- Suruh user: python memory_tool.py init",
        "- JANGAN tebak identitas.",
        "",
        f"---",
        f"Dibuat: {ts}",
        "AUTO-GENERATED - jangan edit manual. Edit config.json lalu regenerate."
    ]

    alur_lines = [
        "# ALUR — Flow Perintah (WAJIB)",
        "",
        "**Setiap input user WAJIB lewat 6 langkah ini. JANGAN skip.**",
        "",
        "## 6 LANGKAH",
        "1. `python memory_tool.py user \"input user\"`",
        "   -> Catat input. Wajib sebelum apapun.",
        "2. `python memory_tool.py search \"kata kunci\"`",
        "   -> Cari memory relevan.",
        "3. `python memory_tool.py add \"tebakan\" --type hypothesis`",
        "   -> Catat praduga sebelum deliver.",
        "4. `python memory_tool.py search \"verifikasi\"`",
        "   -> Verifikasi praduga dengan memory.",
        "5. `python memory_tool.py add \"hasil\" --type learning`",
        "   -> Catat evaluasi/kesimpulan.",
        "6. `python memory_tool.py log \"ringkasan\"`",
        "   -> Catat narasi log.",
        "",
        "## CATAT JUGA JIKA",
        "- **keputusan** -> `--type decision`",
        "- **insight** -> `--type learning`",
        "- **error** -> `--type learning` (dan akui ke user)",
        "- **koreksi user** -> `--type correction`",
        "- **preferensi user** -> `--type preference`",
        "- **konfigurasi** -> `--type configuration`",
        "",
        "## SANKSI SKIP FLOW",
        "- 1× skip: catat error + akui ke user.",
        "- 2× skip: STOP. Refleksi. Tulis kenapa skip.",
        "- 3× skip: STOP total. Tanya user arahan.",
        "",
        "**WAJIB: Catat SEBELUM deliver. Kompaksi bisa datang kapan saja.**",
        "",
        f"---",
        f"Dibuat: {ts}",
        "AUTO-GENERATED - jangan edit manual."
    ]

    sistem_lines = [
        "# SISTEM — Tool & File Reference",
        "",
        f"System folder: {folder}/",
        f"AI: {ai}",
        "",
        "## PERINTAH",
        "  python memory_tool.py init           ← Setup awal (interaktif)",
        "  python memory_tool.py add \"isi\"      ← Simpan memory",
        "    --tags tag1,tag2                    ← Tag untuk pencarian",
        "    --type decision|learning|hypothesis  ← Tipe memory",
        "  python memory_tool.py search \"q\"     ← Cari memory",
        "  python memory_tool.py log \"narasi\"   ← Catat log harian",
        "  python memory_tool.py list           ← Lihat semua memory",
        "  python memory_tool.py user \"input\"   ← Catat input user",
        "  python memory_tool.py stats          ← Statistik system",
        "  python memory_tool.py generate-identity ← Regenerasi identitas",
        "  python memory_tool.py export         ← Ekspor memory.md",
        "  python memory_tool.py audit          ← Audit flow compliance",
        "",
        "## FILE STRUKTUR",
        f"  {folder}/config.json          ← Identitas AI",
        f"  {folder}/SIAPA_AKU.md         ← Siapa kamu (auto)",
        f"  {folder}/MULAI.md             ← Aturan startup (auto)",
        f"  {folder}/ALUR.md              ← Flow perintah (auto)",
        f"  {folder}/SISTEM.md            ← File ini (auto)",
        f"  {folder}/memory.json          ← Semua memory",
        f"  {folder}/logs/                ← Catatan harian",
        f"  {folder}/flow_state.json      ← State flow enforcement",
        "",
        f"---",
        f"Dibuat: {ts}",
        "AUTO-GENERATED - jangan edit manual."
    ]

    base = sys_path()
    paths = {}
    with open(os.path.join(base, INSTRUCTION_MULAI), 'w', encoding='utf-8') as f:
        f.write('\n'.join(mulai_lines) + '\n')
    paths['MULAI.md'] = os.path.join(base, INSTRUCTION_MULAI)
    with open(os.path.join(base, INSTRUCTION_ALUR), 'w', encoding='utf-8') as f:
        f.write('\n'.join(alur_lines) + '\n')
    paths['ALUR.md'] = os.path.join(base, INSTRUCTION_ALUR)
    with open(os.path.join(base, INSTRUCTION_SISTEM), 'w', encoding='utf-8') as f:
        f.write('\n'.join(sistem_lines) + '\n')
    paths['SISTEM.md'] = os.path.join(base, INSTRUCTION_SISTEM)
    return paths

def _append_log(narrative, mtype="log"):
    log_dir = os.path.join(sys_path(), LOGS_DIR)
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f'{today()}.md')
    ts = now()
    if not os.path.exists(log_file):
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(SIGNATURE)
    else:
        with open(log_file, 'r', encoding='utf-8') as f:
            first = f.readline()
        if first != SIGNATURE:
            print(f'[!] PERINGATAN: {log_file}')
    with open(log_file, 'a', encoding='utf-8') as f:
        for line in narrative.split('\n'):
            if line.strip():
                f.write(f'- [{ts}] **[ {mtype} ]** {line.strip()}\n')

def load_memories():
    data = read_json(sys_path(MEMORY_FILE))
    if data is None:
        return []
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        return data.get("memory_feed", [])
    return []

def save_memories(entries):
    write_json(sys_path(MEMORY_FILE), {"memory_feed": entries})

def cmd_init(args):
    ensure_root(create=True)
    print("=== Inisialisasi System Memory ===")
    print(f"Folder system: {sys_path()}")
    print()
    defaults = load_config()
    ai = input(f"Nama AI [{_cfg_id(defaults, 'ai_name', 'Bupen')}]: ").strip()
    if not ai:
        ai = _cfg_id(defaults, 'ai_name', 'Bupen')
    owner = input(f"Nama Owner [{_cfg_id(defaults, 'owner', '')}]: ").strip()
    if not owner:
        owner = _cfg_id(defaults, 'owner', '')
    ws = input(f"Nama Workspace [{_cfg_ws(defaults, 'name', 'Sekolah')}]: ").strip()
    if not ws:
        ws = _cfg_ws(defaults, 'name', 'Sekolah')
    role = input(f"Peran [{_cfg_id(defaults, 'role', 'System Memory')}]: ").strip()
    if not role:
        role = _cfg_id(defaults, 'role', 'System Memory')
    folder = input(f"Nama folder system [{_cfg_sys(defaults, 'folder_name', 'kenangan')}]: ").strip()
    if not folder:
        folder = _cfg_sys(defaults, 'folder_name', 'kenangan')
    print(f"  Root path: [auto: {ensure_root()}] (deteksi otomatis)")
    cfg = {
        "identity": {"ai_name": ai, "owner": owner, "role": role},
        "workspace": {"name": ws},
        "system": {"folder_name": folder, "inisialisasi": now()}
    }
    save_config(cfg)
    id_path = generate_identity_file()
    inst_paths = generate_instruction_set()
    print(f"\nInisialisasi selesai!")
    print(f"  AI: {ai}")
    print(f"  Owner: {owner}")
    print(f"  Workspace: {ws}")
    print(f"  Role: {role}")
    print(f"  Folder system: {folder}")
    print(f"  Root: {ensure_root()}")
    print(f"  Identity file: {id_path}")
    print(f"  Instruction files:")
    for name, path in inst_paths.items():
        print(f"    {name} -> {path}")
    flow_write('idle', reset_skip=True)
    print(f"[{ai}] logs: OK")

def cmd_add(args):
    name = identity_name()
    mtype = args.type or 'project'
    expected = ['idle', 'input', 'hypothesis', 'evaluation', 'search_before_hypothesis', 'search_before_response']
    if mtype == 'hypothesis':
        expected = ['input', 'search_before_hypothesis', 'hypothesis']
    elif mtype in ('learning', 'verification', 'decision', 'configuration'):
        expected = ['hypothesis', 'search_before_response', 'evaluation']
    flow_check(expected, 'add', mtype)
    entries = load_memories()
    next_id = max((e.get('id', 0) for e in entries), default=0) + 1
    tags = [t.strip() for t in args.tags.split(',')] if args.tags else []
    entry = {
        'id': next_id, 'ts': now(), 'date': today(),
        'content': args.content.strip(), 'tags': tags,
        'type': mtype
    }
    entries.append(entry)
    save_memories(entries)
    _append_log(f"[memory] [{mtype}] {args.content[:100]}", "memory")
    if mtype == 'hypothesis':
        flow_write('hypothesis', step_content=args.content)
    elif mtype in ('learning', 'verification', 'decision', 'configuration'):
        flow_write('evaluation', step_content=args.content)
    else:
        st = flow_read()
        flow_write(st['step'], st.get('last_input', ''), step_content=args.content)
    print(f'[{name}] memory.json: OK | id={next_id}')

def cmd_log(args):
    name = identity_name()
    flow_check(['idle', 'input', 'hypothesis', 'evaluation', 'search_before_hypothesis', 'search_before_response'], 'log')
    _append_log(args.narrative)
    flow_write('idle', reset_skip=True)
    print(f'[{name}] logs: OK')

def cmd_search(args):
    name = identity_name()
    state = flow_read()
    current = state['step']
    if current in ('idle', 'input'):
        flow_write('search_before_hypothesis')
    elif current in ('hypothesis', 'search_before_hypothesis'):
        flow_write('search_before_response')
    expected = ['idle', 'input', 'search_before_hypothesis', 'hypothesis', 'search_before_response', 'evaluation']
    flow_check(expected, 'search')
    entries = load_memories()
    q = args.query.lower()
    results = []
    for e in entries:
        score = 0
        if q in e.get('content', '').lower():
            score += 3
        for tag in e.get('tags', []):
            if q in tag.lower():
                score += 2
        if q in e.get('type', '').lower():
            score += 1
        if score > 0:
            results.append((score, e))
    results.sort(key=lambda x: (-x[0], -x[1].get('id', 0)))
    for score, e in results[:args.limit]:
        c = e.get('content', '')
        if len(c) > 120:
            c = c[:120] + '...'
        tags = ','.join(e.get('tags', []))
        print(f'  [{e.get("type", "?")}] (score={score}) {c}')
        if tags:
            print(f'    tags: {tags}')
    if not results:
        print('  Tidak ada hasil.')
    else:
        print(f'\nDitemukan: {len(results)} dari {len(entries)} memory')

def cmd_list(args):
    name = identity_name()
    flow_check(['idle', 'input', 'hypothesis', 'evaluation', 'search_before_hypothesis', 'search_before_response'], 'list')
    entries = load_memories()
    entries.sort(key=lambda x: -x.get('id', 0))
    for e in entries[:args.limit]:
        c = e.get('content', '')
        if len(c) > 100:
            c = c[:100] + '...'
        tags = ','.join(e.get('tags', []))
        print(f'  [{e.get("type", "?")}] {c}')
        if tags:
            print(f'    tags: {tags}')
    print(f'\nTotal: {len(entries)} memory')

def cmd_user(args):
    name = identity_name()
    flow_check(['idle', 'evaluation'], 'user')
    entries = load_memories()
    next_id = max((e.get('id', 0) for e in entries), default=0) + 1
    entry = {
        'id': next_id, 'ts': now(), 'date': today(),
        'content': f"[user] {args.content}",
        'tags': ['user-input'], 'type': 'user'
    }
    entries.append(entry)
    save_memories(entries)
    _append_log(f"[user] {args.content[:100]}", "user")
    flow_write('input', last_input=args.content)
    print(f'[{name}] Input user tercatat: id={next_id}')

def cmd_stats(args):
    name = identity_name()
    flow_check(['idle', 'input', 'hypothesis', 'evaluation', 'search_before_hypothesis', 'search_before_response'], 'stats')
    entries = load_memories()
    types = {}
    tag_count = {}
    for e in entries:
        t = e.get('type', 'unknown')
        types[t] = types.get(t, 0) + 1
        for tag in e.get('tags', []):
            tag_count[tag] = tag_count.get(tag, 0) + 1
    cfg = load_config()
    print(f'[{name}] System Memory - Stats:')
    print(f'  AI: {_cfg_id(cfg, "ai_name", "?")}')
    print(f'  Owner: {_cfg_id(cfg, "owner", "?")}')
    print(f'  Workspace: {_cfg_ws(cfg, "name", "?")}')
    print(f'  Root: {ensure_root()}')
    print(f'  System: {sys_path()}')
    print(f'  memory.json: {len(entries)} entries')
    print(f'  Tipe:')
    for t, c in sorted(types.items(), key=lambda x: -x[1]):
        print(f'    {t}: {c}')
    if tag_count:
        print(f'  Tag teratas:')
        for tag, c in sorted(tag_count.items(), key=lambda x: -x[1])[:5]:
            print(f'    {tag}: {c}')

def cmd_transcript(args):
    name = identity_name()
    entries = load_memories()
    next_id = max((e.get('id', 0) for e in entries), default=0) + 1
    entry = {
        'id': next_id, 'ts': now(), 'date': today(),
        'content': f"[transcript] {args.content}",
        'tags': ['transcript'], 'type': 'conversation'
    }
    entries.append(entry)
    save_memories(entries)
    path = sys_path(CONVERSATION_FILE)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'a', encoding='utf-8') as f:
        f.write(f'## {now()}\n{args.content}\n\n')
    _append_log(f"[transcript] {args.content[:100]}", "transcript")
    print(f'[{name}] conversation.md: OK | memory.json: OK | id={next_id}')

def cmd_export(args):
    name = identity_name()
    entries = load_memories()
    lines = ["# Memory Export", f"Dibuat: {now()}", f"Total: {len(entries)} entri", ""]
    types_order = {}
    for e in entries:
        t = e.get('type', 'unknown')
        types_order.setdefault(t, []).append(e)
    for t, items in sorted(types_order.items()):
        lines.append(f"## {t}")
        for e in items:
            ts = e.get('ts', '?')
            c = e.get('content', '')
            tags = ', '.join(e.get('tags', []))
            lines.append(f"- [{ts}] {c}")
            if tags:
                lines.append(f"  _tags: {tags}_")
        lines.append("")
    path = sys_path(EXPORT_FILE)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    _append_log(f"[export] memory.md generated - {len(entries)} entries", "export")
    print(f'[{name}] memory.md: OK | {len(entries)} entries')

def cmd_audit(args):
    name = identity_name()
    state = flow_read()
    skip_count = state.get('skip_count', 0)
    step = state.get('step', 'idle')
    entries = load_memories()
    types_count = {}
    for e in entries:
        t = e.get('type', 'unknown')
        types_count[t] = types_count.get(t, 0) + 1
    print(f'[{name}] Audit - Flow Compliance:')
    print(f'  Step saat ini: {step}')
    print(f'  Skip count sesi: {skip_count}')
    print(f'  Total memory: {len(entries)} entries')
    print(f'  Tipe: {types_count}')
    if skip_count == 0:
        print(f'  Status: Tidak ada skip flow')
    elif skip_count == 1:
        print(f'  Status: 1 skip — catat dan akui')
    elif skip_count == 2:
        print(f'  Status: 2 skip — refleksi diperlukan')
    else:
        print(f'  Status: 3+ skip — STOP dan tanya user')

def cmd_generate_identity(args):
    name = identity_name()
    path = generate_identity_file()
    print(f'[{name}] SIAPA_AKU.md regenerated: {path}')

def cmd_generate_instructions(args):
    name = identity_name()
    paths = generate_instruction_set()
    print(f'[{name}] Instruction files regenerated:')
    for fname, fpath in paths.items():
        print(f'  {fname} -> {fpath}')

def cmd_greet():
    root = detect_root()
    if root is None:
        print()
        print("  Halo! Aku system memory.")
        print("  Sepertinya pertama kali di sini.")
        print()
        ans = input("  Mau kita kenalan dulu? (y/n): ").strip().lower()
        if ans in ('y', 'yes', 'iya', ''):
            print()
            cmd_init(None)
        else:
            print()
            p.print_help()
    else:
        ensure_root()
        cfg = load_config()
        name = _cfg_id(cfg, "ai_name", "System")
        print(f"\n  {name} - System Memory")
        print(f"  Pemilik: {_cfg_id(cfg, 'owner', '?')}")
        print(f"  Workspace: {_cfg_ws(cfg, 'name', '?')}")
        entries = load_memories()
        print(f"  Memory: {len(entries)} entri")
        print()
        p.print_help()

if __name__ == '__main__':
    p = argparse.ArgumentParser(description='System Memory - Standalone')
    sub = p.add_subparsers(dest='cmd')
    sub.add_parser('init', help='Inisialisasi system memory (interaktif)')
    sub.add_parser('generate-identity', help='Regenerasi SIAPA_AKU.md dari config.json')
    sub.add_parser('generate-instructions', help='Regenerasi MULAI.md, ALUR.md, SISTEM.md')
    sub.add_parser('export', help='Ekspor memory ke memory.md')
    sub.add_parser('audit', help='Audit kepatuhan flow')
    pt = sub.add_parser('transcript', help='Rekam percakapan ke conversation.md')
    pt.add_argument('content')
    pa = sub.add_parser('add', help='Simpan memory baru')
    pa.add_argument('content')
    pa.add_argument('--tags', default='')
    pa.add_argument('--type', default='project')
    pl = sub.add_parser('log', help='Catat log narasi')
    pl.add_argument('narrative')
    ps = sub.add_parser('search', help='Cari memory')
    ps.add_argument('query')
    ps.add_argument('--limit', type=int, default=5)
    pls = sub.add_parser('list', help='List memory')
    pls.add_argument('--limit', type=int, default=10)
    pu = sub.add_parser('user', help='Catat input user')
    pu.add_argument('content')
    pst = sub.add_parser('stats', help='Statistik system')
    args = p.parse_args()
    if args.cmd is None:
        cmd_greet()
        sys.exit(0)
    if args.cmd == 'init':
        ensure_root(create=True)
    else:
        if ensure_root() is None:
            print("  Belum ada system memory. Jalankan 'python memory_tool.py init' dulu.")
            sys.exit(1)
        if not os.path.exists(sys_path(IDENTITY_FILE)):
            generate_identity_file()
    cmds = {
        'add': cmd_add, 'log': cmd_log, 'search': cmd_search,
        'list': cmd_list, 'user': cmd_user, 'stats': cmd_stats,
        'init': cmd_init, 'generate-identity': cmd_generate_identity,
        'generate-instructions': cmd_generate_instructions,
        'transcript': cmd_transcript, 'export': cmd_export, 'audit': cmd_audit
    }
    cmds[args.cmd](args)
    if args.cmd not in ('init', 'generate-identity', 'generate-instructions', 'transcript', 'export', 'audit'):
        flow_show()
