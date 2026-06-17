# Panduan Sistem Memory

## Apa Ini?

Sistem memory mandiri (standalone) untuk AI assistant. Menyimpan percakapan, keputusan, pembelajaran, dan tracking alur kerja AI.

Bisa digunakan di **project mana pun, platform AI mana pun** — tanpa plugin, tanpa API, tanpa hardcode.

## Struktur Folder

```
Project Root/
  ├── opencode.json                ← (opsional) Config platform OpenCode
  ├── kenangan/                    ← Folder system (bisa diubah di config)
  │   ├── config.json              ← Identitas + pengaturan
  │   ├── SIAPA_AKU.md             ← Identity file (auto-generated)
  │   ├── MULAI.md                 ← Aturan startup (auto-generated)
  │   ├── ALUR.md                  ← Flow perintah WAJIB (auto-generated)
  │   ├── SISTEM.md                ← Referensi tool & file (auto-generated)
  │   ├── memory.json              ← Semua memory tersimpan
  │   ├── memory.md                ← Export readable (dibuat saat diminta)
  │   ├── flow_state.json          ← Status alur kerja AI
  │   ├── conversation.md          ← Transkrip percakapan (verbatim)
  │   ├── logs/                    ← Catatan narasi harian
  │   │   └── YYYY-MM-DD.md
  │   └── .auto_backup/            ← Backup file konfigurasi
  ├── memory_tool.py               ← Script utama
  ├── .opencode/                   ← (opsional) File instruksi platform lama
  └── PANDUAN_SISTEM_MEMORY.md     ← File ini
```

## Layer 0 — File Instruksi

Lapisan TERLUAR yang langsung dibaca AI saat startup. File ini memberi tahu AI:
- Aturan main (jangan akses luar)
- Alur kerja (6 langkah)
- Cara pakai tool
- Identitas (dari SIAPA_AKU.md setelah init)

### MULAI.md — Startup + Aturan (auto-generated)

```
# MULAI — Startup & Aturan

## ATURAN WAJIB
- Kamu hanya akses file di workspace ini.
- JANGAN edit file .md/.json di luar kenangan/.
- JANGAN cari konteks dari luar workspace.

## URUTAN MULAI
1. Baca ALUR.md — pahami alur WAJIB 6 langkah.
2. Baca SISTEM.md — pahami tool & file.
3. Baca SIAPA_AKU.md — siapa kamu.
4. Cari memory: `python memory_tool.py search [topik] [--since --type --tags --brief dll]`
5. Baca log terbaru: `kenangan/logs/`
6. Sampaikan ke user: siap.

## JIKA BELUM INIT
- Kamu netral (belum init).
- Suruh user: python memory_tool.py init
- JANGAN tebak identitas.
```

### ALUR.md — Flow Perintah WAJIB (auto-generated)

```
# ALUR — Flow Perintah (WAJIB)

**Setiap input user WAJIB lewat 6 langkah ini. JANGAN skip.**

## 6 LANGKAH
1. `python memory_tool.py user "input user"`
   -> Catat input. Wajib sebelum apapun.
 2. `python memory_tool.py search "kata kunci" [--since --type --tags --brief --last dll]`
   -> Cari memory relevan. Pakai filter untuk hasil tepat.
3. `python memory_tool.py add "tebakan" --type hypothesis`
   -> Catat praduga sebelum deliver.
 4. `python memory_tool.py search "verifikasi" [--since --type --tags --last --first dll]`
   -> Verifikasi praduga dengan memory. Pakai filter untuk hasil tepat.
5. `python memory_tool.py add "hasil" --type learning`
   -> Catat evaluasi/kesimpulan.
6. `python memory_tool.py log "ringkasan"`
   -> Catat narasi log.

## CATAT JUGA JIKA
- **keputusan** -> `--type decision`
- **insight** -> `--type learning`
- **error** -> `--type learning` (dan akui ke user)
- **koreksi user** -> `--type correction`
- **preferensi user** -> `--type preference`
- **konfigurasi** -> `--type configuration`

## SANKSI SKIP FLOW
- 1x skip: catat error + akui ke user.
- 2x skip: STOP. Refleksi. Tulis kenapa skip.
- 3x skip: STOP total. Tanya user arahan.

**WAJIB: Catat SEBELUM deliver. Kompaksi bisa datang kapan saja.**
```

### SISTEM.md — Tool & File Reference (auto-generated)

```
# SISTEM — Tool & File Reference

System folder: kenangan/
AI: [nama AI dari config]

## PERINTAH
  python memory_tool.py init              ← Setup awal (interaktif)
  python memory_tool.py add "isi"         ← Simpan memory
    --tags tag1,tag2                       ← Tag untuk pencarian
    --type decision|learning|hypothesis    ← Tipe memory
  python memory_tool.py search "q"        ← Cari memory (10 filter: --since, --type, --tags, --regex, --last, --sort, --brief, --random, dll)
  python memory_tool.py log "narasi"      ← Catat log harian
  python memory_tool.py list              ← Lihat semua memory
  python memory_tool.py user "input"      ← Catat input user
  python memory_tool.py stats             ← Statistik system
  python memory_tool.py generate-identity ← Regenerasi SIAPA_AKU.md
  python memory_tool.py generate-instructions ← Regenerasi MULAI/ALUR/SISTEM
  python memory_tool.py export            ← Ekspor memory.md
  python memory_tool.py audit             ← Audit flow compliance

## FILE STRUKTUR
  kenangan/config.json          ← Identitas AI
  kenangan/SIAPA_AKU.md         ← Siapa kamu (auto)
  kenangan/MULAI.md             ← Aturan startup (auto)
  kenangan/ALUR.md              ← Flow perintah (auto)
  kenangan/SISTEM.md            ← File ini (auto)
  kenangan/memory.json          ← Semua memory
  kenangan/logs/                ← Catatan harian
  kenangan/flow_state.json      ← State flow enforcement
```

### Catatan Lintas Platform

File instruksi bisa diadaptasi ke platform AI mana pun:

| Platform | Letak File | Cara |
|----------|-----------|------|
| OpenCode | `opencode.json` | Referensi ke `kenangan/*.md` |
| Claude Code | Root `CLAUDE.md` | Copy/link MULAI.md → `CLAUDE.md` |
| Cursor | `.cursor/rules/` | Copy `kenangan/*.md` ke folder rules |
| Gemini CLI | Root `GEMINI.md` | Copy/link MULAI.md → `GEMINI.md` |
| Tanpa platform | Manual | AI baca langsung file .md di `kenangan/` |

**Prinsip:** file instruksi harus GENERIC (tanpa nama AI/user). Identitas spesifik hanya dari `kenangan/SIAPA_AKU.md` yang dihasilkan init.

## Inisialisasi (Pertama Kali)

Jalankan satu perintah:

```
memory_tool.py init
```

Tool tanya 5 hal (tekan Enter untuk pakai default):
1. Nama AI? `[nama AI]`
2. Nama owner? `[nama pemilik]`
3. Nama workspace? `[nama folder]`
4. Folder system? `[kenangan]`
5. Root path? `[deteksi otomatis]`

Selesai → folder `kenangan/` + semua file (`config.json`, `SIAPA_AKU.md`, **`MULAI.md`**, **`ALUR.md`**, **`SISTEM.md`**) terbentuk.

⚠️ Setelah init, update `opencode.json` (atau file instruksi platform lain) untuk arahkan ke `kenangan/MULAI.md`, `kenangan/SISTEM.md`, `kenangan/ALUR.md`, `kenangan/SIAPA_AKU.md` — bukan `.opencode/`.

## File Config (`kenangan/config.json`)

```json
{
  "identity": {
    "ai_name": "[nama AI]",
    "owner": "[nama pemilik]",
    "role": "[peran AI]"
  },
  "workspace": {
    "name": "[nama workspace]"
  },
  "system": {
    "folder_name": "kenangan",
    "inisialisasi": "[timestamp saat init]"
  }
}
```

| Field | Fungsi | Default |
|-------|--------|---------|
| `identity.ai_name` | Nama AI (muncul di header) | (diisi saat init) |
| `identity.owner` | Nama pemilik | (diisi saat init) |
| `identity.role` | Peran AI | AI asisten pribadi |
| `workspace.name` | Nama project | (deteksi otomatis) |
| `system.folder_name` | Nama folder system | kenangan |
| `system.inisialisasi` | Timestamp init | (otomatis) |

Semua path dihitung RELATIF: `root + folder_name + files.*`.

## File Identitas (`SIAPA_AKU.md`)

Dibuat OTOMATIS oleh tool dari `config.json`. Berisi:
- Identitas AI (nama, owner, role)
- Falsafah dan aturan main
- Cara menggunakan tool
- Status terkini

Jika `config.json` berubah → regenerasi `SIAPA_AKU.md` via `python memory_tool.py generate-identity`.

`SIAPA_AKU.md` auto-tergenerate saat pertama kali tool dijalankan (jika file belum ada).

### Cara Inject ke Platform AI

Platform yang support instruction file:

| Platform | Letak File | Cara |
|----------|-----------|------|
| OpenCode | `kenangan/instructions/` atau referensi di config | `SIAPA_AKU.md` di folder instructions |
| Claude Code | Root: `CLAUDE.md` | Copy/link `SIAPA_AKU.md` → `CLAUDE.md` |
| Cursor | `.cursor/rules/` | Copy `SIAPA_AKU.md` ke folder rules |
| Gemini CLI | Root: `GEMINI.md` | Copy/link `SIAPA_AKU.md` → `GEMINI.md` |
| Codex CLI | MCP server config | Konfigurasi MCP memory server |
| Tanpa platform | Langsung | Tool output header identitas tiap dipanggil |

### Dua Lapis Proteksi Amnesia

1. **Instruction file**: platform inject `SIAPA_AKU.md` ke AI saat startup. AI langsung sadar identitas.
2. **Tool identity header**: setiap `memory_tool.py` dipanggil, output header identitas + flow state. Jika instruction file gagal, tool tetap trigger kesadaran.

## Perintah `memory_tool.py`

### Inisialisasi
```
memory_tool.py init
```
Generate:
- Folder `kenangan/` + subfolder
- `config.json` — identitas AI
- `SIAPA_AKU.md` — file identitas
- `MULAI.md` + `ALUR.md` + `SISTEM.md` — file instruksi

### Generate Identity
```
memory_tool.py generate-identity
```
Regenerasi `SIAPA_AKU.md` dari `config.json`. Jalan otomatis jika file belum ada.

### Generate Instructions
```
memory_tool.py generate-instructions
```
Regenerasi `MULAI.md`, `ALUR.md`, `SISTEM.md` dari template bawaan.

### Menyimpan Memory
```
memory_tool.py add "isi memory" --tags kata_kunci --type decision
```
Simpan ke `memory.json`. Parameter `--type`:
- `decision` — keputusan penting
- `learning` — pembelajaran/insight
- `hypothesis` — praduga/tebakan
- `verification` — konfirmasi/verifikasi
- `configuration` — pengaturan/kode
- `preference` — preferensi user
- `project` — info project (default)

Parameter `--tags`: kata kunci pisah koma, untuk pencarian.

### Mencari Memory — 10 Kategori Filter
```
memory_tool.py search "query" --limit 5
```
Cari di `memory.json` dengan pipeline filter:

| Kategori | Filter | Contoh |
|----------|--------|--------|
| PERBANDINGAN | `--since`, `--until`, `--id`, `--gt-id`, `--lt-id`, `--type`, `--ne-type` | `--since 2026-06-01 --type learning` |
| LOGIKA | `--tags` (AND), `--any` (OR), `--not` | `--tags RAHAYU,test --any` |
| ELEMEN | `--has-tag`, `--orphan`, `--size N` | `--orphan` (tanpa tag) |
| EVALUASI | `query` + `--regex`, `--deep` | `--regex "Bupen.*filter" --deep` |
| ARRAY | `--tags` (AND), `--any` (OR), `--size` | `--size 2` (tepat 2 tag) |
| POSISI | `--last N`, `--first N`, `--range A-B` | `--range 20-50` |
| TRANSFORM | `--sort id/date/type/ts`, `--asc`, `--group` | `--group type` |
| AGREGASI | `--count`, `--brief` | `--brief` (distribusi) |
| RANDOM | `--random`, `--sample N` | `--sample 3` |
| SPESIAL | Error handling + encoding fix | Otomatis |

### Melihat Daftar
```
memory_tool.py list --limit 10
```
Tampilkan memory terbaru.

### Catatan Input User
```
memory_tool.py user "[user]: input user"
```
Catat input user ke memory + flow state. Wajib sebelum langkah lain.

### Catatan Narasi
```
memory_tool.py log "isi kronologi"
```
Simpan ke `logs/` — untuk catatan harian, bukan memory permanen. Tutup siklus flow.

### Rekam Percakapan
```
memory_tool.py transcript "[user]: input" "[AI]: response"
```
Simpan verbatim ke `conversation.md`.

### Ekspor ke Markdown
```
memory_tool.py export
```
Baca `memory.json`, generate `memory.md` untuk dibaca user/AI.

### Statistik
```
memory_tool.py stats
```
Tampilkan jumlah memory, tipe, dll.

### Audit
```
memory_tool.py audit --days 14
```
Cek kepatuhan: apakah ada skip flow? Berapa kali? Pola apa?

## Proses Flow (6 Langkah)

Setiap input dari user memicu alur:

```
① input
    ↓
② baca_ulang (search memory)
    ↓
③ praduga (add --type hypothesis)
    ↓
④ baca_ulang_lagi (search lagi)
    ↓
⑤ evaluasi (add --type learning/decision)
    ↓
⑥ log (catat narasi)
    ↓
kembali ke ①
```

| Langkah | Arti | Perintah |
|---------|------|----------|
| 1 input | Catat input user | `memory_tool.py user "..."` |
| 2 baca_ulang | Cari memory relevan | `memory_tool.py search "..."` |
| 3 praduga | Buat hipotesis | `add --type hypothesis` |
| 4 baca_ulang_lagi | Verifikasi | `memory_tool.py search "..."` |
| 5 evaluasi | Simpan pembelajaran | `add --type learning` |
| 6 log | Catat narasi | `memory_tool.py log "..."` |

### Flow Enforcement

Jika langkah dilewati, flow checker beri **soft warning** (tidak block action) sebagai pengingat:

| Skip ke- | Konsekuensi |
|----------|-------------|
| 1 | Catat error + akui ke user |
| 2 | STOP + refleksi (tulis kenapa skip) |
| 3 | STOP total + tanya user arahan |

⚠️ Enforcement bersifat **soft warning** — data tetap tersimpan, tapi skip menumpuk. Skip ke-3 = harus tanya user arahan.

### Deteksi Folder

Tool cari folder system (default: `kenangan/`) dari direktori aktif naik ke parent sampai ketemu. Jika tidak ketemu, sarankan `memory_tool.py init`.

## Auto-Backup

Setiap perubahan file konfigurasi (config.json, memory.json, flow_state.json), sistem otomatis backup versi sebelumnya ke `.auto_backup/` dengan timestamp.

Format: `YYYYMMDD_HHmmss_namafile`

## Proteksi Amnesia (Recovery)

Saat AI kehilangan konteks (kompaksi):

1. AI baca `SIAPA_AKU.md` — langsung tahu identitas + aturan main
2. AI baca `MULAI.md` — pahami startup sequence
3. AI baca `ALUR.md` — ingat flow
4. AI jalankan `memory_tool.py list` — lihat memory terbaru
5. AI jalankan `memory_tool.py search "..."` — cari konteks spesifik
6. AI baca `logs/` — baca narasi sesi sebelumnya

## 5 Layer Mapping

| Layer | Nama | Isi | Fungsi |
|-------|------|-----|--------|
| 0 | Instruksi AI | `MULAI.md`, `ALUR.md`, `SISTEM.md`, `opencode.json` | Memberi tahu AI aturan, alur, dan cara pakai tool |
| 1 | Config Identity | `config.json` (ai_name, owner, role) | Identitas spesifik dari init |
| 2 | Path System | Semua path relatif dari root + kenangan/ | Zero hardcode |
| 3 | Storage | `memory.json` (master), `memory.md` (export) | Semua memory tersimpan |
| 4 | Workspace Detect | `detect_root()` | Cari kenangan/ dari CWD ke parent |

Layer 0 adalah yang PALING LUAR — langsung dibaca AI saat startup.
Isinya GENERIC — tanpa nama AI/user. Identitas spesifik di Layer 1.

## Mapping Fungsi Internal

| Fungsi | Tugas | Layer |
|--------|-------|-------|
| `detect_root()` | Cari folder system dari CWD ke parent | 4 |
| `cmd_init()` | Inisialisasi + config interaktif | 1 |
| `cmd_add()` | Simpan ke memory.json + log | 3 |
| `cmd_search()` | Cari di memory.json (10 filter: perbandingan, logika, posisi, dll) | 3 |
| `cmd_list()` | Tampilkan memory terbaru | 3 |
| `cmd_log()` | Catat narasi ke logs/ | 3 |
| `cmd_transcript()` | Simpan percakapan ke conversation.md | 3 |
| `cmd_export()` | Generate memory.md dari memory.json | 3 |
| `cmd_generate_identity()` | Update SIAPA_AKU.md dari config | 1 |
| `cmd_generate_instructions()` | Regenerasi MULAI/ALUR/SISTEM.md | 0 |
| `cmd_user()` | Catat input user + flow state | — |
| `flow_read()` | Baca flow_state.json | — |
| `flow_write()` | Update flow state | — |
| `flow_check()` | Periksa urutan langkah | — |
| `memory_json_append()` | Append entry ke memory.json | 3 |

## Portabilitas

System ini 100% standalone — tidak tergantung platform AI.

### Cara Pindah ke Project Lain
1. Copy `memory_tool.py` ke root project baru
2. Jalankan `python memory_tool.py init` — isi nama AI, owner, dll
3. Init otomatis buat `kenangan/` + `config.json` + `SIAPA_AKU.md` + `MULAI.md` + `ALUR.md` + `SISTEM.md`
4. Update `opencode.json` (atau config platform lain) untuk referensi instruksi dari `kenangan/*.md`
5. Siap digunakan

### Syarat
- Python 3.8+
- Standard library only (tidak ada dependency tambahan)

### Yang Tidak Ikut
- `PANDUAN_SISTEM_MEMORY.md` — file panduan ini
- File project lama di `kenangan/`
- File instruksi spesifik platform (`.opencode/`, `CLAUDE.md`, dll)

## Perbedaan dari Versi OpenCode

| Aspek | OpenCode | Standalone (kenangan) |
|-------|----------|----------------------|
| Instruksi AI | HEARTBEAT/BOOTSTRAP/MEMORY.md | MULAI/ALUR/SISTEM.md |
| Folder system | `.opencode/` | `kenangan/` (bisa diubah) |
| Storage | L3 API + memory.json | `memory.json` saja |
| Search | L3 API (vector) | Langsung baca file (keyword) |
| Config | Tersebar | `config.json` terpusat |
| Workspace | WORKSPACES dict hardcode | Auto-detect dari CWD |
| Identitas | Hardcode di kode | Dari `config.json` → `SIAPA_AKU.md` |
| Plugin | opencode-mem, working-memory | Zero plugin |
| Dependency | API server port 4747 | Standard library Python |

## Catatan

- Semua file append-only — tidak ada edit/hapus
- Format `memory.json`: JSON array
- Format `logs/`: markdown dengan timestamp
- Format `conversation.md`: transkrip kronologis
- Nama folder system bisa diubah di `config.json`
- Default folder: `kenangan/` (jika tidak diisi)

---
Dibuat oleh **BIG & Hady** — diskusi, koreksi, dan secangkir kopi. 2026.
