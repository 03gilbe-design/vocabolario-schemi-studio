# Dettagli

Le spiegazioni lunghe. I percorsi sono relativi alla radice del repo.


[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/03gilbe-design/vocabolario-schemi-studio/blob/main/strumenti/0_demo_colab_per_GPT.ipynb)

**Prova in 1 clic:** il notebook `strumenti/0_demo_colab_per_GPT.ipynb` gira su Colab senza chiavi, credenziali o Drive, sugli esempi inclusi.

Un vocabolario di regole per far generare a un modello (Claude, GPT, Gemini) **schemi di studio nel mio stile**, a partire da una pagina del docente. Ho ricavato le regole confrontando le pagine del prof con gli schemi che ne ho fatto a mano. Lavoro di tirocinio, CdL Informatica, Università di Verona (2026).

## Cosa c'è
```
vocabolario/                         le regole da dare al modello (A, B, C, E) e il modulo per estrarne di nuove (D); PACCHETTO.pdf = tutto in un file
  pronto_per_il_modello/             tutto il vocabolario in un file (PACCHETTO_MODELLO.md) + regole/ una per file
trascrivi_lezioni/                   trascrivere lezioni su GPU Colab (Whisper + chi parla)
collega_schema_a_pagina_prof/        collegare ogni pagina di appunti alla pagina del prof da cui viene
  collega_pagine_colab.ipynb         Colab: ogni tuo schema -> la sua pagina del prof
strumenti/                           codice usato per misurare i risultati
  0_demo_colab_per_GPT.ipynb         Colab: numeri, controllo OK/FUORI, per_GPT.zip
  1_misura_stile_dai_numeri/         estrarre numeri (colore, zone, tinte, stile, testo) da appunti e pagine generate
  2_grafiche_per_spiegare_le_regole/ 174 grafiche gia' fatte delle regole, da mostrare quando ne spieghi una
esempi_confronti/                    2 confronti + 1 grafico (solo pagine generate e miei schemi)
documenti_tirocinio/                 cosa_abbiamo_imparato/, questo file, i video tutorial, i miei appunti di Architettura (pptx + pdf), immagini_readme/
```

## Come si usa il pacchetto (generare uno schema)
Si dà al modello, in quest'ordine (dettagli e conteggio token in `vocabolario/PACCHETTO.md`):
1. **A_VOCABOLARIO.md** — solo le regole (macro 1-5, fino alla riga `---`). Le regole vengono prima dello stile.
2. **B_NON_FARE.md** — solo le 5 voci **[GENERALE]** (1, 2, 6, 10, 11), una riga ciascuna, senza motivi e fonti.
3. **C_STILE.md** — sezione 1 + elenco degli hex della palette + sezione 6, presentati come tono.
4. **E_AGGIUNTA_FIGURA.md** — la frase "scegli UN caso concreto che attraversi tutti i concetti della pagina".
5. Per ultima la pagina del docente, con un prompt minimale e neutro.

Restano fuori: gli esempi in fondo ad A e C, le tabelle numeriche di C, le voci [OVERFITTING] di B, tutto D. Totale circa 2.070 token. In fondo a B ci sono domande "DA DECIDERE" ancora aperte.

## Come si estraggono regole nuove
`vocabolario/D_MODULO_ESTRAI_REGOLE.md`: ingresso = una pagina del docente + lo schema che ne ho fatto io (oppure solo appunti, confermando la regola su una seconda pagina). Un modello estrae **una** regola (prompt E1), un secondo modello la usa su una pagina del docente mai vista, il primo rivede il risultato. Solo miei schemi veri, mai fatti con l'AI.

## Prova veloce: trovare in numeri cosa distingue i tuoi schemi da quelli dell'AI
```
cd strumenti/1_misura_stile_dai_numeri
pip install -r requirements.txt
python -m playwright install chromium
python -X utf8 trova_differenze.py --suoi esempi_numeri/suoi/Architettura_Gilberto.pdf --generate esempi_numeri/generate --prof-parole 385
```
Il risultato è in `risultati_numeri/`: la classifica dei numeri che distinguono i miei schemi da quelli dell'AI, le frasi da dare al modello e i valori per il controllo automatico.

**Con i propri appunti, in 3 passi:**
1. **Una cartella con le pagine fatte dall'AI** (`.html`, `.svg` o `.png`).
2. **Il comando** `python -X utf8 trova_differenze.py --suoi miei_schemi.pdf --generate cartella`.
3. **Le frasi e il controllo:**
   - le frasi di `FRASI_PER_IL_MODELLO.md` vanno nel prompt;
   - ogni pagina nuova si controlla con `python -X utf8 controlla_stile.py pagina.png --sorgente pagina.html --rif risultati_numeri/numeri.json`, che stampa OK o FUORI.

I dettagli sono in `strumenti/1_misura_stile_dai_numeri/README.md`.

## Strumenti
Ognuno ha il suo README con cosa fa, input, output e comando.
- **Trascrizione Colab** — `trascrivi.py "audio.m4a"` -> `audio_chi_parla.txt`.
- **Collegare pagine** — `annotatore/` (solo codice, parole rare in comune + interfaccia per annotare) e `groq/` (modello che guarda la pagina, sceglie fra 10 candidate BM25, confronto con verità nota).
- **Numeri dagli appunti** — `trova_differenze.py` (tutto con un comando, vedi sopra), `controlla_stile.py pagina.png --sorgente pagina.html` (OK/FUORI su 10 numeri), `controlla_attenzione.py pagina.png` (OK/FUORI rispetto alle mie pagine), `quanto_urla.py`, `stile_numeri.py`, `numeri_coppie.py`.

## Risultati principali (esperimenti 39, 40, 41, pagina "cache associativo a gruppi" di Architettura)
- Tre numeri separano le mie pagine da quelle generate: colore forte 3,7-14,3% della pagina (generate: mediana 1,85%), zone di colore forte 1-6 (generate: mediana 6,5), tinta principale 68-99,5% del colore (generate: mediana 67,5%).
- Senza regole le pagine generate sono "arcobaleno": fino a 14 macchie di colore e tinta principale sotto il 60%; con le mie regole la tinta diventa una sola, come nei miei schemi.
- Solo 1 pagina generata su 18 sta dentro tutti e tre i miei range: Claude + pacchetto, prova r1 (7,6% / 3 zone / 84,9%).
- Claude + pacchetto riprende tono (fondo crema, un solo colore forte che segue il caso), il disegno centrale e la barra dell'indirizzo in 3 campi in 3 prove su 3; difetti di impaginazione: senza regole 14 e 24, con pacchetto 0, 5 e 8.
- Cosa non passa ancora: un terzo della pagina resta vuoto, forme perfette invece di contorni a mano (ignorati 3/3), il testo del prof sparisce nelle etichette. Con GPT, la voce NOT TODO toglie le legende (0/5 contro 2/5 senza).

## Cosa c'è e cosa no (scelte per il repo pubblico)
- **Pagine del docente: tolte.** In `esempi_confronti/` resta solo la versione `p03_cache_associativo_prof_sfocato.png` (pagina del prof sfocata, non leggibile); l'originale resta sul disco ed è in `.gitignore`.
- **`strumenti/1_misura_stile_dai_numeri/esempi_numeri/suoi/Architettura_Gilberto.pdf`: tenuto.** Sono miei appunti (7 pagine, Architettura degli elaboratori), servono alla demo di `trova_differenze.py` come esempio di "suoi schemi". Non contengono dati personali oltre al nome; in una pagina ci sono piccoli ritagli di microistruzioni del corso.
- `esempi_numeri/generate/` contiene solo pagine generate dall'AI.
- Nessuna chiave è nel codice: la chiave Groq si passa con la variabile d'ambiente `GROQ_API_KEY`. `.env`, `*auth*.json` e `materiali.json` (percorsi locali) sono esclusi da `.gitignore`.
