# Erstellung eines Dame-Algorithmus mithilfe von A*

## Forschungsfrage
Welche Heuristik (oder auch Heuristikart) ist am besten fuer das Brettspiel "Dame"?
Gibt es Aspekte/Variabeln vom Spiel, auf die man sich am besten fokusieren sollte, um die Gewinnchance zu erhoehen?
Kann man anhand der Heuristiken und deren Bewertung aussagen ueber ein Spiel treffen?

## Theorie
Wir erwarten hierbei das nartuerlich Heuristiken die direkt oder indirekt die Anzahl der Damen betreffen besonders gut abschneiden, da die Dame offensichtlich der staerkere Spielstein ist.
Auch anzunehmen ist, dass eine Heuristik die Steine welche naeher am Gegnerischen Ende des Spielbrets sind bevorzugt gut abschneidet, da vorgeschrittene Steine nicht nur zu Damen werden, sondern auch Gegnerische Steine schlagen.

## Quellen
- [Die Spielregeln von Dame](https://www.brettspielnetz.de/spielregeln/dame.php)
- [A* Algorithm](https://www.geeksforgeeks.org/a-search-algorithm/)

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
Es wurden verschiedene Heuristiken verwendet, um einen Spielstand zu bewerten.
Die meisten bestehen bewerten die Anzahl der Steine auf dem Spielfeld. Entweder durch das Zaehlen der eigenen Steine (Normale und Damen) oder durch das Zaehlen der gegnerischen Steine. Also wird entweder nach dem Erhalt der eigenen Spielsteine, oder nach dem Verlust des Gegners optimiert.
Andere Heuristiken bewerten den Vortschritt der eigenen Steine auf dem Spielfeld, wobei Felder mit weiter vortgeschritten Steinen, preferieren.

### Implementierung des Dame-Spiels
Ein Spielzustand wird representiert als 2D-Array von Integern repraesentiert. Moegliche zuege werden als vollzogener Zug dargestellt.
Der Alogrithmus bewertet also eine Liste an 2D-Arrays.
In einem Spielzustand repraesentiert sind leere Felder mit 0 gekenzeichnet. Spieler 1 werden ungerade zahlen zugeordnet (1 und 3), wohingegen spieler 2 die geraden (2 und 4) als Steine besitzt.
Die niedrigere Zahl repraesentiert hier jeweils einen normalen Stein und die hoehere eine Dame.


## Beantwortung der Forschungsfrage
Die drei Heuristiken die am erfolgreichsten waren, sind:
- Die Anzahl der gegnerischen Damen und Steine
- Die Anzahl der eigenen Damen und Steine
- Die Anzahl der eigenen Steine

Anzumerken ist hierbei, dass der Fortschritt der Steine als Heuristik nicht gut abgeschnitten hat.
Es ist also anzunehmen, dass die Anzahl der Steine deutlich relevanter ist, als die Position der Steine.
Die Anzahl der Gegnerischen Steine zu reduzieren sorgt am zuverlässigsten fuer einen Sieg. Was irgendwo zu erwarten ist, da die Gegnerischen Steine auf 0 zu reduzieren die Gewinnkondition des Spieles ist. Wenn jedoch die Anzahl der Eigenen Steine als Heuristik verwendet wird, ergeben sich Siege die wenig verluste haben.

Die Annahme, dass Heuristiken die die Anzahl der Damen betreffen besser abschneiden ist bestaetigt. Jedoch stellte sich herraus, dass weiter vortgeschrittene Steine zu preferieren nicht optimal ist. Dies kann unteranderem daran liegen, dass Damen sobald sie auf dem Spielfeld sind in alle Richtungen ziehen koennen. Und wenn diese Eigenschaft voll ausgenutzt wird, die Damen besser verwendet werden. Dies tut eine Heuristik nartuerlich nicht, die alle Spielsteine ans andere Ende bewegen moechte.

Aus der Performance der Heuristiken haben sich simple und auch intuitive Aussagen ueber das Spiel Dame ergeben, aber das Verfahren koennte auf komplexere Spiele angewandt werden, um ein Strategisches Verstaendnis zu entwickeln.
