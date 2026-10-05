# Changelog

## 1.0.2

- **Orario scolastico dinamico**: Argo non espone l'orario nella dashboard, quindi CompitAPP lo ricostruisce dalle lezioni del registro (ultime 3 settimane) e lo aggiorna da solo, anche a inizio anno scolastico.
- Pagina **Orario** e comando Telegram `/orario` leggono i dati dal database invece di un orario scritto nel codice.
- Anno scolastico e nome dello studente calcolati in automatico: niente più "2025/2026" e "Classe 3B" fissi.
- Gestione corretta di righe doppie, giornate corte (es. primi giorni di scuola) e supplenze isolate.
- Nuova tabella `orario` nel database (creata in automatico all'avvio, nessuna azione richiesta).
- Il campo `anno_scolastico` della configurazione non viene più usato.

## 1.0.1

- Versione precedente.
