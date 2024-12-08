# Implementierung des Minimax-Algorithmus mit Alpha-Beta-Pruning

## Forschungsfrage

Wie beeinflusst die Verwendung von Alpha-Beta-Pruning die Effizienz des Minimax-Algorithmus beim Spielen von Dame?

## Theorie

### Minimax-Algorithmus

Der Minimax-Algorithmus ist ein Entscheidungsalgorithmus, der verwendet wird, um optimale Spielzüge in Spielen mit zwei Spielern zu finden. Ziel ist es, die Gewinnchancen des einen Spielers zu maximieren, während die des Gegners minimiert werden.

### Alpha-Beta-Pruning

Alpha-Beta-Pruning ist eine Optimierung des Minimax-Algorithmus. Es reduziert die Anzahl der zu bewertenden Knoten im Suchbaum, indem es Zweige abschneidet, die nicht zum optimalen Zug beitragen. Dadurch wird die Effizienz deutlich gesteigert, ohne die Genauigkeit der Entscheidungen zu beeinträchtigen.

## Implementierung

### Übernahme aus Praktikum 1

Das Grundgerüst des Dame-Spiels sowie die grundlegenden Bewertungsfunktionen wurden aus Praktikum 1 übernommen. Die Modifikation betrifft die Implementierung des Algorithmus: Anstelle von A* wurde der Minimax-Algorithmus mit und ohne Alpha-Beta-Pruning verwendet.

### Ablauf Tests

1. **Initialisierung**: Die Spielfeldgröße wurde auf 8×8 festgelegt, um die Performance des Algorithmus auf einem realistischen Spielfeld zu testen. Aufgrund der hohen Rechenzeit wurden für wiederholte Tests kleinere Spielfelder mit 4×5 Feldern verwendet.
2. **Zugbewertung**: Der Algorithmus bewertet die möglichen Spielzüge rekursiv, basierend auf einer definierten Bewertungsfunktion für Spielstände.
3. **Optimierung**: Beim Alpha-Beta-Pruning werden Grenzwerte _alpha_ und _beta_ eingeführt, um die Suche einzuschränken.

## Testergebnisse

### 8×8 Spielfeld

Bei einem vollständigen Spielfeld (8×8) wurden folgende Ergebnisse erzielt:
- **Mit Alpha-Beta-Pruning**: Durchschnittlich wurden pro Zug maximal 8.000 Knoten betrachtet, und die Berechnung dauerte ca. 2 Minuten.
- **Ohne Alpha-Beta-Pruning**: Bis zu 143.000 Knoten wurden analysiert, und die Berechnung dauerte über 20 Minuten.

### 4×5 Spielfeld

Zur Durchführung von 1.000 Simulationen wurde ein reduziertes Spielfeld (4×5) verwendet. Dabei zeigte sich:
TODO
- **Mit Alpha-Beta-Pruning**: \( <platzhalterA> \) Sekunden durchschnittliche Rechenzeit.
- **Ohne Alpha-Beta-Pruning**: \( <platzhalterB> \) Sekunden durchschnittliche Rechenzeit.

Die Ergebnisse zeigen, dass Alpha-Beta-Pruning die Anzahl der betrachteten Knoten sowie die Rechenzeit drastisch reduziert.

## Fazit

Die Implementierung des Minimax-Algorithmus mit Alpha-Beta-Pruning hat gezeigt, dass die Effizienz des Algorithmus erheblich verbessert werden kann. Im Vergleich zur ursprünglichen A*-Implementierung aus Praktikum 1 ist der Algorithmus nun besser an die Anforderungen von Spielen mit großen Suchbäumen angepasst.

## Quellen

[Q1] TODO Grundlagen zum Minimax-Algorithmus und Alpha-Beta-Pruning \
[Q2] Implementierungsdetails aus Praktikum 1 (siehe [Dokumentation P1](p1_dokumentation.md))

## Bilder

[B1] ![Testergebnisse mit 8x8 Feld](8x8_field_abp_test.png)
[B2] ![Testergebnisse mit 4x5 Feld](TODO)
[B3] ![Ablaufdiagramm  Minimax ohne ABP](TODO)
[B3] ![Ablaufdiagramm  Minimax mit ABP](TODO)