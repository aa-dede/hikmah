# hikmah — System Memory untuk AI Berjiwa

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen)

> "Coba → Waktu → Memory → Evaluasi → Tidak ulang"
>
> Bukan sempurna — punya jiwa.

hikmah adalah **system memory framework** untuk AI coding agent. Bukan untuk membuat AI lebih cepat atau lebih akurat — tapi untuk membuat AI **belajar dari proses**, termasuk dari kesalahan.

## Filosofi

Di GitHub sudah ada puluhan proyek AI memory. Semuanya kejar satu hal: **akurasi retrieval**. Vector search, knowledge graph, MCP server, benchmark LongMemEval 96% — semua tentang "seberapa tepat AI mengingat."

hikmah berbeda. hikmah tidak peduli seberapa cepat AI menemukan jawaban. hikmah peduli **bagaimana AI sampai ke jawaban itu.**

| Mereka | hikmah |
|--------|-------|
| Kejar akurasi | Kejar proses |
| Shortcut ke makna (vector) | Belajar lewat trial-and-error (FTS5) |
| AI dikasih identitas | AI **tumbuh** identitasnya |
| Stateless, perfect recall | Stateful, boleh lupa, belajar lagi |
| Soul = definisi | Soul = **pengalaman** |

## 6 Pembeda

1. **Flow enforcement** — 6 langkah wajib: input → search → hypothesis → search → evaluation → log. Tidak bisa skip.
2. **Identitas AI generatif** — SIAPA_AKU.md berisi placeholder. AI menemukan identitasnya sendiri lewat `init`.
3. **WAL Protocol** — catat memory SEBELUM deliver. Kompaksi bisa datang kapan saja.
4. **Backup otomatis** — setiap perubahan file di-backup ke `.auto_backup/`.
5. **Audit trail** — semua operasi tercatat, traceable.
6. **Zero dependency** — Python stdlib + SQLite. Tidak perlu Docker, API key, atau cloud.

## Cara Mulai

```bash
git clone https://github.com/aa-dede/hikmah.git
cd hikmah
python memory_tool.py init    # isi nama AI, owner, workspace
python memory_tool.py         # mulai
```

Init akan memandu mengisi:
- Nama AI
- Nama pemilik
- Nama workspace
- Peran/deskripsi

Setelah init, semua file identitas akan ter-generate otomatis.

## Perintah Dasar

| Perintah | Fungsi |
|----------|--------|
| `python memory_tool.py init` | Setup awal (interaktif) |
| `python memory_tool.py add "isi" --tags tag1 --type decision` | Simpan memory |
| `python memory_tool.py search "kata kunci"` | Cari memory |
| `python memory_tool.py log "narasi"` | Catat log harian |
| `python memory_tool.py user "input"` | Catat input user |
| `python memory_tool.py list` | Lihat semua memory |
| `python memory_tool.py stats` | Statistik system |
| `python memory_tool.py audit` | Audit flow compliance |

## Flow 6 Langkah (WAJIB)

Setiap input WAJIB lewat 6 langkah ini:

```
① user "input user"        → Catat input. Wajib sebelum apapun.
② search "kata kunci"      → Cari memory relevan.
③ add "tebakan" --type hypothesis → Catat praduga sebelum deliver.
④ search "verifikasi"      → Verifikasi praduga dengan memory.
⑤ add "hasil" --type learning → Catat evaluasi/kesimpulan.
⑥ log "ringkasan"          → Catat narasi log.
```

Sanksi skip:
- 1× skip: catat error + akui
- 2× skip: STOP, refleksi, tulis kenapa
- 3× skip: STOP total, tanya user

## Struktur File

```
hikmah/
├── memory_tool.py           ← Script utama
├── README.md                ← Panduan ini
├── LICENSE                  ← MIT
└── kenangan/                ← Folder system (nama bisa diubah)
    ├── config.json          ← Konfigurasi identitas AI
    ├── MULAI.md             ← Panduan startup
    ├── ALUR.md              ← Flow 6 langkah detail
    ├── SISTEM.md            ← Referensi tool & file
    ├── SIAPA_AKU.md         ← Identitas AI (auto-generate)
    ├── memory.json          ← Semua memory (append-only)
    ├── logs/                ← Catatan harian
    ├── flow_state.json      ← State flow enforcement
    └── .auto_backup/        ← Backup otomatis
```

## Panduan Lengkap

File `PANDUAN_SISTEM_MEMORY.md` (454 baris) berisi dokumentasi lengkap: setup, semua perintah, flow enforcement, auto-backup, portabilitas lintas platform, dan mapping 5 layer.

## Lisensi

MIT — bebas digunakan, dimodifikasi, dan disebarluaskan.
