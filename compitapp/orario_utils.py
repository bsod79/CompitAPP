"""Orario scolastico: ricostruzione dal registro di classe + stili/emoji per materia.

Argo non espone l'orario settimanale nella dashboard, ma ogni lezione del registro
porta data, ora, materia e docente: dalle lezioni delle ultime settimane si
ricostruisce l'orario reale, che si aggiorna da solo a ogni cambio (anche a inizio anno).
"""
from collections import defaultdict
from datetime import date, datetime, timedelta

# Giorni di lezione (0 = lunedì … 5 = sabato; il sabato si mostra solo se ci sono lezioni)
GIORNI = [
    # idx, emoji, nome, sigla, colore titolo, sfondo colonna "oggi" (desktop)
    (0, '☀️', 'Lunedì',    'Lun', '#d97706', '#fffbeb'),
    (1, '🌤️', 'Martedì',   'Mar', '#be185d', '#fdf2f8'),
    (2, '🌈', 'Mercoledì', 'Mer', '#0f766e', '#f0fdfa'),
    (3, '⚡', 'Giovedì',   'Gio', '#5b21b6', '#faf5ff'),
    (4, '🎉', 'Venerdì',   'Ven', '#db2777', '#fdf2f8'),
    (5, '🎈', 'Sabato',    'Sab', '#0369a1', '#f0f9ff'),
]
GIORNI_CHIAVE = {'lunedi': 0, 'martedi': 1, 'mercoledi': 2, 'giovedi': 3, 'venerdi': 4, 'sabato': 5}

# (parola chiave, emoji, sfondo, accento, testo) — l'ordine conta: la prima che combacia vince
_MATERIE = [
    ('motori',      '⚽',  '#dcfce7', '#22c55e', '#15803d'),
    ('italiano',    '📝',  '#fef3c7', '#f59e0b', '#d97706'),
    ('storia',      '📜',  '#fce7f3', '#ec4899', '#be185d'),
    ('tecnologia',  '💻',  '#ccfbf1', '#14b8a6', '#0f766e'),
    ('inglese',     '🇬🇧', '#dbeafe', '#3b82f6', '#1d4ed8'),
    ('religione',   '✝️',  '#f3e8ff', '#a855f7', '#7e22ce'),
    ('matematica',  '🔢',  '#ede9fe', '#6366f1', '#5b21b6'),
    ('arte',        '🎨',  '#ffe4e6', '#f43f5e', '#be123c'),
    ('scienze',     '🔬',  '#d1fae5', '#10b981', '#065f46'),
    ('geografia',   '🌍',  '#fef9c3', '#eab308', '#a16207'),
    ('musica',      '🎵',  '#e0f2fe', '#0ea5e9', '#0369a1'),
    ('laboratorio', '🧪',  '#cffafe', '#06b6d4', '#0e7490'),
    ('francese',    '🗣️', '#fae8ff', '#d946ef', '#a21caf'),
    ('spagnolo',    '🗣️', '#fae8ff', '#d946ef', '#a21caf'),
    ('tedesco',     '🗣️', '#fae8ff', '#d946ef', '#a21caf'),
    ('educazione civica', '🏛️', '#ffedd5', '#f97316', '#c2410c'),
]
_DEFAULT = ('📚', '#f1f5f9', '#94a3b8', '#475569')
_MINUSCOLE = {'e', 'ed', 'di', 'del', 'della', 'dei', 'delle', 'in', 'la', 'il', 'lo', 'a', 'al'}


def normalizza_materia(nome):
    """'ARTE E IMMAGINE' -> 'Arte e Immagine'"""
    parole = (nome or '').strip().lower().split()
    out = []
    for i, p in enumerate(parole):
        out.append(p if (i > 0 and p in _MINUSCOLE) else p.capitalize())
    return ' '.join(out)


def normalizza_docente(nome):
    """'M. RAO' -> 'M. Rao'"""
    return ' '.join(p.capitalize() if len(p) > 2 or not p.endswith('.') else p.upper()
                    for p in (nome or '').strip().split())


def _voce(materia):
    chiave = (materia or '').lower()
    for kw, emoji, bg, accento, testo in _MATERIE:
        if kw in chiave:
            return emoji, bg, accento, testo
    return _DEFAULT


def emoji_materia(materia):
    return _voce(materia)[0]


def stile_materia(materia):
    """Colori per la UI: dict con sfondo, accento, testo."""
    _, bg, accento, testo = _voce(materia)
    return {'bg': bg, 'accento': accento, 'testo': testo}


def etichetta_breve(materia):
    """Nome compatto per le celle della tabella desktop."""
    m = (materia or '').lower()
    if 'motori' in m:
        return 'Sc. Mot.'
    if m.startswith('arte'):
        return 'Arte'
    if m.startswith('educazione civica'):
        return 'Ed. Civica'
    return materia


def anno_scolastico(oggi=None):
    """Anno scolastico corrente: da settembre a agosto ('2026/2027')."""
    oggi = oggi or date.today()
    inizio = oggi.year if oggi.month >= 9 else oggi.year - 1
    return f"{inizio}/{inizio + 1}"


def _parse_data(s):
    try:
        return datetime.strptime(str(s)[:10], '%Y-%m-%d').date()
    except Exception:
        return None


def _ricostruisci(lezioni, dal, al):
    # Lezioni uniche (data, ora, materia): il registro può avere più righe per la stessa ora
    uniche = {}
    for r in lezioni:
        d = _parse_data(r.get('datGiorno'))
        ora = r.get('ora')
        materia = (r.get('materia') or '').strip()
        if not d or not materia or not isinstance(ora, int) or ora < 1:
            continue
        if not (dal <= d <= al) or d.weekday() > 5:
            continue
        uniche.setdefault((d, ora, materia), (r.get('docente') or '').strip())

    # Per ogni data di lezione: l'ultima ora registrata (una giornata corta non "vale" per le ore successive)
    ultima_ora = defaultdict(int)
    for (d, ora, _m) in uniche:
        ultima_ora[d] = max(ultima_ora[d], ora)
    date_per_giorno = defaultdict(set)
    for d in ultima_ora:
        date_per_giorno[d.weekday()].add(d)

    voti = defaultdict(lambda: defaultdict(float))      # (giorno, ora) -> materia -> peso
    visti = defaultdict(lambda: defaultdict(set))       # (giorno, ora) -> materia -> date
    docenti = defaultdict(dict)                         # (giorno, ora) -> materia -> docente più recente
    for (d, ora, materia), docente in sorted(uniche.items()):
        rango = sorted(date_per_giorno[d.weekday()]).index(d) + 1   # più recente = peso maggiore
        chiave = (d.weekday(), ora)
        voti[chiave][materia] += rango
        visti[chiave][materia].add(d)
        if docente:
            docenti[chiave][materia] = docente

    slot = []
    for (giorno, ora), per_materia in voti.items():
        # Il sabato conta come giorno di scuola solo con lezioni in almeno 2 sabati (non per un recupero isolato)
        if giorno == 5 and len(date_per_giorno[5]) < 2:
            continue
        materia = max(per_materia, key=lambda m: (per_materia[m], max(visti[(giorno, ora)][m])))
        # Date in cui quest'ora poteva esserci (giornate abbastanza lunghe): serve almeno metà delle volte
        utili = sum(1 for d in date_per_giorno[giorno] if ultima_ora[d] >= ora)
        if len(visti[(giorno, ora)][materia]) < (utili + 1) // 2:
            continue
        slot.append({
            'giorno': giorno, 'ora': ora,
            'materia': normalizza_materia(materia),
            'docente': normalizza_docente(docenti[(giorno, ora)].get(materia, '')),
        })
    return sorted(slot, key=lambda s: (s['giorno'], s['ora']))


def ricostruisci_orario(registro, oggi=None):
    """Orario settimanale ricostruito dalle lezioni del registro.

    Usa le ultime 3 settimane; se sono vuote (es. dopo le vacanze) allarga a 60 giorni.
    Ritorna una lista di {'giorno': 0-5, 'ora': int, 'materia': str, 'docente': str}.
    """
    oggi = oggi or date.today()
    for giorni in (21, 60):
        slot = _ricostruisci(registro or [], oggi - timedelta(days=giorni), oggi)
        if slot:
            return slot
    return []
