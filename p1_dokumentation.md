# Erstellung eines Dame-Algorithmus mithilfe von A*

## Forschungsfrage
TODO?

## Theorie
TODO? ("Theorie und genutze Quellen beschrieben_")
- https://www.brettspielnetz.de/spielregeln/dame.php
- https://www.geeksforgeeks.org/a-search-algorithm/

## Versuch implementiert und dokumentiert
Die Implementation besteht aus 3 wesentlichen Teilen:
- Dem [Algorithmus](algorithm.py)
- Den [Heuristiken](heuristics.py) für den Algorithmus
- Der [Implementierung des Dame-Spiels](piece.py)

Zudem wurde noch ein wrapper in Form eines
a. Interaktiven Spiel-Modus gebaut
b. "Automatischen" Modus in welchen der Algorithmus gegen sich selbst spielt
    
```
❯ python main.py help
Usage: python3 main.py [board number] [heuristic1] [heuristic2] or just python3 main.py for interactive mode.
```

### Algorithmus

Der A*-Algorithmus wurde folgendermaßen implementiert:

1. **Initialisierung**: Zwei Listen werden erstellt:
   - **Offene Liste (OL)**: Enthält Knoten, die noch erweitert werden müssen.
   - **Geschlossene Liste (CL)**: Enthält bereits erweiterte Knoten.

2. **Hauptschleife**: Solange die offene Liste nicht leer ist:
   - Der **nächste Knoten** (`NodeToExpand`) wird aus der OL entfernt (niedrigster f-Wert).
   - **Erzeugung neuer Zustände**:
     - Gültige Züge werden mithilfe der Funktion `getMoves()` generiert.
       - Vor erweitern des Knoten, wird geprüft, ob mit diesem das Ziel erreicht ist. (`checkForWinningBoard()`).
     - Für jeden Zustand werden die Werte **g**, **h** (mit einer methode aus [Heuristiken](#heuristiken)) und **f** berechnet
       und **g** und **f** werden in dem Board gespeichert.
   - **Hinzufügen neuer Zustände**:
     - Ein neuer Zustand wird nur dann der OL hinzugefügt, wenn kein Knoten mit dem gleichen **g-Wert** und einem **kleineren f-Wert** bereits in OL oder CL existiert.
   - Die OL wird nach den **f-Werten** sortiert.
   - Der erweiterte Knoten wird zur CL hinzugefügt.

### Heuristiken
TODO

### Implementierung des Dame-Spiels
TODO


## Beantwortung der Forschungsfrage
TODO: Ausformulieren + welche Forschungsfrage - passt dazu?
TODO: Tests machen?
- Verschiedene Heuristiken verhalten sich anders
    - CountOfPiecesAndDamesOfOtherPlayer sorgt gefühlt am zuverlässigsten für einen Sieg
    - CountOfPiecesAndDames ist sehr zurückhaltend, sorgt aber bei Sieg oft für einen Sieg mit wenig "verlusten".
    - ProgressPiecesOnBoard sorgt nicht zwinged für einen Sieg, bringt die Pieces aber zuverlässig nach vorne.
- Die meisten Heuristiken gewinnnen gegen Random

## Kritische Reflexion (Erenntnisse und Herausforderunge) schriftlich beantwortet
- Testen des Algorithmus ohne implementation des Spiels schwierig
    - 