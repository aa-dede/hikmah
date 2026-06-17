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
- 1× skip: catat error + akui ke user.
- 2× skip: STOP. Refleksi. Tulis kenapa skip.
- 3× skip: STOP total. Tanya user arahan.

**WAJIB: Catat SEBELUM deliver. Kompaksi bisa datang kapan saja.**

---
Dibuat: 2026-06-16 11:45:02
AUTO-GENERATED - jangan edit manual.
