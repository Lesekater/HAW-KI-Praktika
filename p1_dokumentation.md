# Erstellung eines Dame-Algorithmus mithilfe von A*

## Forschungsfrage
Wie verhalten sich verschiedene Heuristiken im Brettspiel “Dame” im
Hinblick auf ihre Effektivität? Und welche Rückschlüsse koennen 
aus der Effektivität der Heuristiken auf das Spiel Dame geschlossen werden?

## Heurisitken

Es wurden verschiedene Heuristiken eingesetzt, um einen Spielstand zu bewerten. 
Viele dieser Heuristiken konzentrieren sich auf die Anzahl der Steine auf dem Spielfeld,
entweder durch das Zählen der eigenen Steine (normale Steine und Damen) oder der gegnerischen. 
Dadurch wird entweder der Erhalt der eigenen Steine oder die Reduktion der gegnerischen optimiert.
Andere Heuristiken bewerten den Fortschritt der eigenen Steine auf dem Spielfeld,
wobei Felder mit weiter fortgeschrittenen Steinen bevorzugt werden.

### Zulaessigkeit
Die Zulaessigkeit der Heurisitken ist schwer zu bewerten aufgrund der Komplexitaet des Spiels, sowie der Tatsache,
dass die Anzahl der Steine nicht mit der Restanzahl der moeglichen Zuege in korrelation steht und
die meisten unserer Heurisitken sich auf die Anzahl der Steine beziehen.

### Anzahl der eigenen Steine
Die Heuristik weist eine höhere Effektivität auf, wenn eine größere Anzahl eigener Steine auf dem Spielfeld vorhanden ist.

### Anzahl der eigenen Damen
Die Heuristik weist eine höhere Effektivität auf, wenn eine größere Anzahl eigener Damen auf dem Spielfeld vorhanden ist.

### Anzahl der eigenen Steine und Damen
Die Heuristik weist eine höhere Effektivität auf, wenn eine größere Anzahl eigener Steine und Damen auf dem Spielfeld vorhanden ist.

### Anzahl der Steine am Ende vom Board
Die Heuristik weist eine höhere Effektivität auf, wenn eine größere Anzahl eigener Steine sich am Ende vom Board befinden.

### Fortschritt der Steine auf dem Board
Die Heuristik weist eine höhere Effektivität auf, je weiter die eigenen Steine auf dem Board fortgeschritten sind.

### Anzahl der generischen Steine
Die Heuristik weist eine höhere Effektivität auf, wenn eine kleinere Anzahl gegnerischer Steine auf dem Spielfeld vorhanden ist.

### Anzahl der generischen Damen
Die Heuristik weist eine höhere Effektivität auf, wenn eine kleinere Anzahl gegnerischer Damen auf dem Spielfeld vorhanden ist.

### Anzahl der generischen Steine und Damen
Die Heuristik weist eine höhere Effektivität auf, wenn eine kleinere Anzahl gegnerischer Steine und Damen auf dem Spielfeld vorhanden ist.

### Zufall
Die Heuristik ist zufällig generiert für tests.

## Theorie
Wir erwarten, dass Heuristiken, die direkt oder indirekt die Anzahl der Damen beeinflussen,
besonders effektiv sind, da die Dame offensichtlich die stärkste Spielfigur darstellt.
Auch anzunehmen ist, dass eine Heuristik, die Bretter bevorzugt,
auf denen Steine näher am gegnerischen Ende des Spielbretts stehen, gut abschneidet,
da vorgeschrittene Steine nicht nur zu Damen werden, sondern auch gegnerische Steine schlagen können.

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

## Implementation
Die Implementation besteht aus 3 wesentlichen Teilen:
- Dem [Algorithmus](algorithm.py)
- Den [Heuristiken](heuristics.py) für den Algorithmus
- Der [Implementierung des Dame-Spiels](piece.py)

Zudem wurde noch ein Wrapper in Form eines
a. Interaktiven Spiel-Modus gebaut
b. "Automatischen" Modus in welchen der Algorithmus gegen sich selbst spielt
    
```
❯ python main.py help
Usage: python3 main.py [board number] [heuristic1] [heuristic2] or just python3 main.py for interactive mode.
```

### Implementierung des Dame-Spiels
Ein Spielzustand wird als 2D-Array von Integern repräsentiert, und mögliche Züge werden als eine Liste von Spielzuständen zurückgegeben.
In einem Spielzustand sind leere Felder mit der Zahl 0 gekennzeichnet. Spieler 1 werden ungerade Zahlen (1 und 3) zugeordnet, während Spieler 2 die geraden Zahlen (2 und 4) besitzt. Die niedrigere Zahl repräsentiert dabei einen normalen Stein, die höhere eine Dame.
Entsprechend den Regeln werden für einen Ausgangszustand alle möglichen Folgezustände berechnet:
1. Zunächst werden sämtliche Züge für alle Steine ermittelt.
2. Falls Züge existieren, bei denen gegnerische Steine geschlagen werden, werden nur diese berücksichtigt.
3. Von diesen Zügen werden diejenigen bevorzugt, die entweder einen oder, falls mehrere Züge diese Bedingung erfüllen, die meisten gegnerischen Steine schlagen.

#### UML Diagramm der Softawre
<img width="5830" alt="Uml_KI_01" src="https://github.com/user-attachments/assets/adb57119-fab2-4834-a863-22ed2e34fd7c">

## Beantwortung der Forschungsfrage
Die drei Heuristiken die am erfolgreichsten waren, sind:
- Die Anzahl der gegnerischen Damen und Steine
- Die Anzahl der eigenen Damen und Steine
- Die Anzahl der eigenen Steine

Anzumerken ist hierbei, dass der Fortschritt der Steine als Heuristik nicht gut abgeschnitten hat.
Es ist also anzunehmen, dass die Anzahl der Steine deutlich relevanter ist, als die Position der Steine.
Die Reduktion der gegnerischen Steine ist der effektivste Weg, um einen Sieg zu erzielen, da das Ziel des Spiels darin besteht, alle gegnerischen Steine zu schlagen. Wird hingegen die Anzahl der eigenen Steine als Heuristik genutzt,
führt dies in der Regel zu Siegen mit weniger Verlusten. \
Eine Erklaerung hierfuer, ist dass das Spiel Dame in Verschiedene Phasen unterteilt werden kann [1]. Und Heurisitken fuer jede der drei Phasen optimal sind. Die Heuristik die den Vortschritt der eigenen Steine verwendet ist nur in den Anfangsphasen hilfreich und wird spaeter eher zur Hindernis.


Die Annahme, dass Heuristiken die die Anzahl der Damen betreffen besser abschneiden ist bestätigt. Es stellte sich jedoch heraus, dass das Bevorzugen weiter fortgeschrittener Steine nicht optimal ist. Ein möglicher Grund dafür ist, dass Damen, sobald sie das Spielfeld erreichen, sich in alle Richtungen bewegen können. Wird diese Fähigkeit vollständig ausgenutzt, erweist sich der Einsatz der Damen als vorteilhafter. Eine Heuristik, die darauf abzielt, alle Steine ans andere Ende des Spielfelds zu bewegen, berücksichtigt diese Dynamik jedoch nicht.

Durch die Analyse der Gewinnwahrscheinlichkeit der Heuristiken haben wir einfache, aber wichtige Erkenntnisse über das Spiel Dame gewonnen. Dieses Verfahren könnte auch auf komplexere Spiele angewendet werden, um besseres strategisches Verständnis zu entwickeln.

## Quellen
- [Die Spielregeln von Dame](https://www.brettspielnetz.de/spielregeln/dame.php)
- [A* Algorithm](https://www.geeksforgeeks.org/a-search-algorithm/)
- [Evolutionary-based heuristic generators for checkers and give-away checkers](https://pages.mini.pw.edu.pl/~mandziukj/PRACE/es_init.pdf)[1]
- [Project Repository](https://github.com/Lesekater/HAW-KI-Praktika)
