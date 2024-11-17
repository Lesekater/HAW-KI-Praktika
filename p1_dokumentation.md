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
Der Algorithmus \[...] TODO

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
- Die meisten Heuristiken gewinnnen gegen Random: https://docs.google.com/spreadsheets/d/170CFpr8RLiGMvOxHPpSI5cPoWAZjzb6XiXbXhXjNTGs/edit?usp=sharing

## Kritische Reflexion (Erenntnisse und Herausforderunge) schriftlich beantwortet
- Testen des Algorithmus ohne implementation des Spiels schwierig
    - 
