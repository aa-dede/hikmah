# SISTEM — Tool & File Reference

System folder: kenangan/
AI: [AI_NAME] (diatur di config.json)

## PERINTAH
  python memory_tool.py init           ← Setup awal (interaktif)
  python memory_tool.py add "isi"      ← Simpan memory
    --tags tag1,tag2                    ← Tag untuk pencarian
    --type decision|learning|hypothesis  ← Tipe memory
  python memory_tool.py search "q"     ← Cari memory (opsi: --type, --tags, --since, --last, --brief, --random, --sort, dll)
  python memory_tool.py log "narasi"   ← Catat log harian
  python memory_tool.py list           ← Lihat semua memory
  python memory_tool.py user "input"   ← Catat input user
  python memory_tool.py stats          ← Statistik system
  python memory_tool.py generate-identity ← Regenerasi identitas
  python memory_tool.py export         ← Ekspor memory.md
  python memory_tool.py audit          ← Audit flow compliance

## FILE STRUKTUR
  kenangan/config.json          ← Identitas AI
  kenangan/SIAPA_AKU.md         ← Siapa kamu (auto)
  kenangan/MULAI.md             ← Aturan startup (auto)
  kenangan/ALUR.md              ← Flow perintah (auto)
  kenangan/SISTEM.md            ← File ini (auto)
  kenangan/memory.json          ← Semua memory
  kenangan/logs/                ← Catatan harian
  kenangan/flow_state.json      ← State flow enforcement

---
Dibuat: 2026-06-16 11:45:02
AUTO-GENERATED - jangan edit manual.
