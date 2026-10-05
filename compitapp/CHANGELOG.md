# Changelog

## 1.0.5

- **Voti con la virgola** (es. 7,5): ora il colore (verde/giallo/rosso) viene calcolato correttamente, prima venivano sempre segnati come insufficienti.
- **Pagina Configurazione**: le "Statistiche database" ora mostrano i dati dello studente selezionato (prima erano sempre a zero).
- Aggiunti gli screenshot nel README.

## 1.0.4

- **Corretto il cambio tra più figli**: con due o più studenti configurati, toccare il nome del figlio faceva uscire dalla PWA e riapriva Home Assistant. Ora il cambio resta dentro CompitAPP e mantiene la pagina in cui ti trovi.
- I comandi Telegram `/resoconto` e `/voti` ora sono separati per studente (un messaggio per ciascun figlio, con il nome giusto).
- Rimosso un nome di studente scritto nel codice nel comando `/voti`.

## 1.0.3

- **Riepilogo serale intelligente**: in modalità `auto` (predefinita) il messaggio "Nessun compito per domani" non viene più inviato quando domani non è giorno di scuola. I giorni di scuola sono riconosciuti dalle lezioni del registro, quindi chi ha lezione il sabato continua a riceverlo; se ci sono compiti, il riepilogo parte sempre.
- **Riepilogo personalizzabile** dalla configurazione: `reminder_modalita` (auto / sempre / solo_con_compiti), `reminder_mostra_orario` (aggiunge l'orario di domani), `reminder_testo_vuoto` e `reminder_testo_chiusura` (frasi tue).
- **Sabato nell'orario**: se lo studente ha lezioni il sabato, compare nella pagina Orario e nel comando `/orario sab`.
- Le nuove opzioni sono facoltative: se non le tocchi, tutto funziona come prima (con il riepilogo `auto`).

## 1.0.2

- **Orario scolastico dinamico**: Argo non espone l'orario nella dashboard, quindi CompitAPP lo ricostruisce dalle lezioni del registro (ultime 3 settimane) e lo aggiorna da solo, anche a inizio anno scolastico.
- Pagina **Orario** e comando Telegram `/orario` leggono i dati dal database invece di un orario scritto nel codice.
- Anno scolastico e nome dello studente calcolati in automatico: niente più "2025/2026" e "Classe 3B" fissi.
- Gestione corretta di righe doppie, giornate corte (es. primi giorni di scuola) e supplenze isolate.
- Nuova tabella `orario` nel database (creata in automatico all'avvio, nessuna azione richiesta).
- Il campo `anno_scolastico` della configurazione non viene più usato.

## 1.0.1

- Versione precedente.
