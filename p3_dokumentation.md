# Aggregation von Heuristiken mithilfe von neuronalen Netzen

11.01.2024 \
Elias Wernicke, Lars Janssen

## Forschungsfrage

Wie gut kann ein neuronales Netz mehrere 

Wie beeinflusst die Verwendung von Alpha-Beta-Pruning die Effizienz des Minimax-Algorithmus beim Spielen von Dame?

## Theorie

### Neuronale Netze [\<quelle>] TODO



### Aggregation von Heuristiken? [\<quelle>] TODO



## Implementierung

### Übernahme aus Praktikum 1 & 2

Das Grundgerüst des Dame-Spiels sowie die Heuristiken wurden aus dem ersten Praktikum übernommen. Zur Generierung des Datensatzes wurde der Code aus dem zweiten Praktikum entsprechend modifiziert. Während der Simulation zufälliger Spiele mithilfe der Monte Carlo Game Search wurden alle Zwischen-Spielsituationen in .json-Dateien zwischengespeichert, um sie später für den Datensatz zu labeln. Diese Dateien wurden anschließend erneut eingelesen und mithilfe der im ersten Praktikum entwickelten Heuristiken gelabelt. Dadurch konnte ein umfassender Datensatz erstellt werden, der als Grundlage für das Training des neuronalen Netzes dient.

### Ablauf der Tests TODO

1. **Initialisierung**: Die Spielfeldgröße wurde auf 8×8 festgelegt, um die Performance des Algorithmus auf einem realistischen Spielfeld zu testen. Aufgrund der hohen Rechenzeit wurden für wiederholte Tests kleinere Spielfelder mit 4×5 Feldern verwendet.
2. **Zugbewertung**: Der Algorithmus bewertet die möglichen Spielzüge rekursiv, basierend auf einer definierten Bewertungsfunktion für Spielstände.
3. **Optimierung**: Beim Alpha-Beta-Pruning werden die Grenzwerte _alpha_ und _beta_ eingeführt, um die Suche einzuschränken.

## Testergebnisse TODO

### 8×8 Spielfeld

Wie auf dem Diagramm [B1] zu sehen, wurden auf einem vollständigen Spielfeld (8×8) folgende Ergebnisse erzielt:
- **Ohne Alpha-Beta-Pruning**: Bis zu 143.000 Knoten wurden analysiert, und die Berechnung dauerte über 20 Minuten.
- **Mit Alpha-Beta-Pruning**: Durchschnittlich wurden pro Zug maximal 8.000 Knoten betrachtet, und die Berechnung dauerte ca. 2 Minuten.

### 4×5 Spielfeld

Zur Durchführung von 1.000 Simulationen wurde ein reduziertes Spielfeld (4×5) verwendet. Wie auf dem Diagramm [B2] zu sehen, zeigte sich dabei:
- **Ohne Alpha-Beta-Pruning**: Bis zu 650 Knoten wurden analysiert.
- **Mit Alpha-Beta-Pruning**: Durchschnittlich wurden pro Zug maximal 250 Knoten betrachtet.

Die Ergebnisse zeigen, dass Alpha-Beta-Pruning die Anzahl der betrachteten Knoten sowie die Rechenzeit drastisch reduziert.

## Fazit TODO

Die Implementierung des Minimax-Algorithmus mit Alpha-Beta-Pruning hat gezeigt, dass die Effizienz des Algorithmus erheblich verbessert werden kann. Es müssen im Durchschnitt, wie in [B2] zu sehen, deutlich weniger Züge betrachtet werden, und dadurch erhöht sich die Berechnungsgeschwindigkeit erheblich. Außerdem konnte im Vergleich zum ersten Praktikum mit diesem Algorithmus, im Gegensatz zum A*-Algorithmus, auch das volle 8×8 Dame-Feld in wenigen Minuten "gelöst" werden.

## Quellen & Referenzen TODO

[Q1] Algorithmen in Python: 32 Klassiker vom Damenproblem bis zu neuronalen Netzen  
Kopec, David; 1. Aufl.; ISBN: 978-3-8362-7749-5  
[Q2] Implementierungsdetails aus Praktikum 1 (siehe [Dokumentation P1](https://raw.githubusercontent.com/Lesekater/HAW-KI-Praktika/refs/heads/main/p1_dokumentation.md))  
[R1] Quellcode Dame-Anwendung (https://github.com/Lesekater/HAW-KI-Praktika.git)

## Bilder

[B1] 8x8_field_abp_test.png ![Testergebnisse mit 8×8 Feld](https://raw.githubusercontent.com/Lesekater/HAW-KI-Praktika/refs/heads/main/8x8_field_abp_test.png)  
[B2] 4x5_field_abp_test.png ![Testergebnisse mit 4×5 Feld](https://raw.githubusercontent.com/Lesekater/HAW-KI-Praktika/refs/heads/main/4x5_field_abp_test.png)  
[B3] ablauf_minimax.png ![Ablaufdiagramm Minimax ohne ABP](https://raw.githubusercontent.com/Lesekater/HAW-KI-Praktika/refs/heads/main/ablauf_minimax.png)  
[B4] ablauf_minimax_abp.png ![Ablaufdiagramm Minimax mit ABP](https://raw.githubusercontent.com/Lesekater/HAW-KI-Praktika/refs/heads/main/ablauf_minimax_abp.png)
