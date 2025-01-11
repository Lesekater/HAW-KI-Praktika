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

#### Datengenerierung mithilfe von MCGS

Die Datengenerierung erfolgte durch die Simulation von Spielen mithilfe des modifizierten Monte Carlo Game Search-Algorithmus. Um diese Simulation zu starten, wurde der folgende Befehl verwendet:

```bash
python3.10 main.py 0 9 10 4 &
```

Dabei wurde für jedes simulierte Spiel die jeweilige Zwischen-Spielsituation in einer .json-Datei gespeichert. Ein Beispiel für eine generierte Datei sieht wie folgt aus:

```json
{
    "move": [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 3, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [4, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 3, 0, 0, 0, 0, 0, 0]
    ],
    "score": -1
}
```

Im nächsten Schritt wurden die Situationen mithilfe des folgenden Skripts gelabelt:
```bash
python convert_training_data.py
```
Hierbei wurde der ursprüngliche Score durch Werte ersetzt, die auf den im ersten Praktikum entwickelten Heuristiken basieren. Für jede Heuristik wurde dabei eine eigene Datei erstellt, in der der score entsprechend angepasst wurde. Der finale Datensatz enthält somit für jede Spielsituation mehrere Scores, die die Heuristiken repräsentieren. Diese Daten dienten als Grundlage für das Training des neuronalen Netzes.

### Training des Neuronalen Netz

Im Rahmen des Projekts wurden zwei verschiedene Modelle entwickelt und trainiert, um die Aggregation von Heuristiken zu optimieren. Das erste Modell diente als Basis, während das zweite Modell durch Hinzufügen eines Convolutional Layers weiterentwickelt wurde, um die Trainingsergebnisse zu verbessern.

#### Modell 01

Das erste Modell ist ein einfaches feedforward Netz mit einer flachen Architektur. Es besteht aus mehreren voll verbundenen Dense-Layern, die schrittweise die Eingabedaten transformieren. Die Architektur sieht wie folgt aus:

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Layer (type)                    ┃ Output Shape           ┃       Param # ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ flatten (Flatten)               │ (None, 64)             │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dense (Dense)                   │ (None, 128)            │         8,320 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dense_1 (Dense)                 │ (None, 64)             │         8,256 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dense_2 (Dense)                 │ (None, 64)             │         4,160 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dense_3 (Dense)                 │ (None, 1)              │            65 │
└─────────────────────────────────┴────────────────────────┴───────────────┘
```

#### Modell 02

Das zweite Modell erweitert die Architektur durch die Einführung eines Convolutional Layers. Dieser ermöglicht die Extraktion von räumlichen Merkmalen aus den Eingabedaten, die anschließend in Dense-Layern verarbeitet werden. Zusätzlich wurden Dropout-Schichten hinzugefügt, um gegen Overfitting gegenzuwirken. Die Architektur ist wie folgt:

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Layer (type)                    ┃ Output Shape           ┃       Param # ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ conv2d (Conv2D)                 │ (None, 8, 8, 32)       │           320 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ max_pooling2d (MaxPooling2D)    │ (None, 4, 4, 32)       │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dropout (Dropout)               │ (None, 4, 4, 32)       │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ flatten (Flatten)               │ (None, 512)            │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dense (Dense)                   │ (None, 128)            │        65,664 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dropout_1 (Dropout)             │ (None, 128)            │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dense_1 (Dense)                 │ (None, 1)              │           129 │
└─────────────────────────────────┴────────────────────────┴───────────────┘
```

## Ergebnisse Training
Die Ergebnisse des Trainings zeigen, dass das zweite Modell (mit Convolutional Layer) keinen signifikanten Vorteil im Vergleich zum ersten Modell gebracht hat. Tatsächlich schnitt das erste Modell in einigen Konfigurationen sogar leicht besser ab.

### Vergleich der Modelle

- **CountOfPiecesAndDames (Modell 01)**:  
  - MAE: 0.0662  
  - MSE: 0.0076  
  - R²: 0.8571  

- **CountOfPiecesAndDames (Modell 02)**:  
  - MAE: 0.0702  
  - MSE: 0.0083  
  - R²: 0.8437  

Die Einführung des Convolutional Layers im zweiten Modell führte in diesem Fall zu einer geringfügigen Verschlechterung der Ergebnisse. Dies könnte darauf hinweisen, dass die räumliche Struktur der Daten in diesem Szenario keine wesentliche Rolle spielt oder dass das zusätzliche Layer-Design nicht optimal auf die Daten abgestimmt ist.

### Einfluss der Heuristiken

Des weiteren ist zu erkennen, dass das Training schlechter wurde, je mehr Heuristiken in den Datensatz aufgenommen wurden. Beispielsweise zeigen die Ergebnisse mit drei Heuristiken (**CountOfPiecesAndDames**, **CountOfPiecesAtEndOfBoard**, **ProgressPiecesOnBoard**) eine deutlich höhere MAE und MSE sowie einen stark abnehmenden R²-Wert:

- **CountOfPiecesAndDames, CountOfPiecesAtEndOfBoard, ProgressPiecesOnBoard (Modell 01)**:  
  - MAE: 0.2863  
  - MSE: 0.1210  
  - R²: 0.0457  

- **CountOfPiecesAndDames, CountOfPiecesAtEndOfBoard, ProgressPiecesOnBoard (Modell 02)**:  
  - MAE: 0.2886  
  - MSE: 0.1218  
  - R²: 0.0385  

Der R²-Wert, der die Güte der Anpassung des Modells misst, fiel mit der Hinzunahme weiterer Heuristiken drastisch ab. Mit allen verfügbaren Heuristiken aus dem ersten Praktikum im Datensatz lag der R²-Wert bei nahezu 0:

- **alle Heuristiken (Modell 01)**:  
  - MAE: 0.3126  
  - MSE: 0.1218  
  - R²: 0.0033  

## Fazit TODO

Die Implementierung des Minimax-Algorithmus mit Alpha-Beta-Pruning hat gezeigt, dass die Effizienz des Algorithmus erheblich verbessert werden kann. Es müssen im Durchschnitt, wie in [B2] zu sehen, deutlich weniger Züge betrachtet werden, und dadurch erhöht sich die Berechnungsgeschwindigkeit erheblich. Außerdem konnte im Vergleich zum ersten Praktikum mit diesem Algorithmus, im Gegensatz zum A*-Algorithmus, auch das volle 8×8 Dame-Feld in wenigen Minuten "gelöst" werden.

## Quellen & Referenzen TODO

[Q1] Algorithmen in Python: 32 Klassiker vom Damenproblem bis zu neuronalen Netzen  
Kopec, David; 1. Aufl.; ISBN: 978-3-8362-7749-5  
[Q2] Implementierungsdetails aus Praktikum 1 (siehe [Dokumentation P1](https://raw.githubusercontent.com/Lesekater/HAW-KI-Praktika/refs/heads/main/p1_dokumentation.md))  
[Q3] Implementierungsdetails aus Praktikum 2 (siehe [Dokumentation P2](https://raw.githubusercontent.com/Lesekater/HAW-KI-Praktika/refs/heads/main/p2_dokumentation.md))  
[R1] Quellcode Dame-Anwendung (https://github.com/Lesekater/HAW-KI-Praktika.git)

## Bilder

[B1] 8x8_field_abp_test.png ![Testergebnisse mit 8×8 Feld](https://raw.githubusercontent.com/Lesekater/HAW-KI-Praktika/refs/heads/main/8x8_field_abp_test.png)  
[B2] 4x5_field_abp_test.png ![Testergebnisse mit 4×5 Feld](https://raw.githubusercontent.com/Lesekater/HAW-KI-Praktika/refs/heads/main/4x5_field_abp_test.png)  
[B3] ablauf_minimax.png ![Ablaufdiagramm Minimax ohne ABP](https://raw.githubusercontent.com/Lesekater/HAW-KI-Praktika/refs/heads/main/ablauf_minimax.png)  
[B4] ablauf_minimax_abp.png ![Ablaufdiagramm Minimax mit ABP](https://raw.githubusercontent.com/Lesekater/HAW-KI-Praktika/refs/heads/main/ablauf_minimax_abp.png)
