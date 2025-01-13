# Aggregation von Heuristiken mithilfe von neuronalen Netzen

11.01.2024 \
Elias Wernicke, Lars Janssen

## Forschungsfrage

Wie gut kann ein neuronales Netz mehrere Heuristiken aggregieren?
Ist es moeglich ein neuronales Netz auf mehreren Heuristiken zu trainieren, um es selbst als Heuristik zu verwenden?

## Theorie

### Neuronale Netze [\<quelle>] TODO

https://pmc.ncbi.nlm.nih.gov/articles/PMC6428006/
Neuronale Netze sind Systeme, welche die struktur und funktion von biologischen gehirnen imitieren.
Sie bestehen aus untereinander verbundenen Neuronen,
TODO HOW TO NEURON

Diese Neuronen werden zu Schichten zusammengefasst.
Einem Input layer, in welchem die dort angesetzten Neuronen direkt die Eingabe fuer das neuronale Netz erhalten.
Mehreren Hidden layers, welche die Daten transformieren und weiter verarbeiten.
Und schliesslich dem Output layer, welcher die finale Entscheidung des Netzwerkes repraesentiert.

Die am weitest verbreitete Art von neuronalen Netzen ist die des Feedforward Netzes, in welcher die Signale nur von Input zu Output fliessen.

### Aggregation von Heuristiken? [\<quelle>] TODO

https://arxiv.org/abs/2002.06505
Das universele approximations Theorem sagt aus, dass normale feedforward neurale Netzwerke mit nur einer verschteckten Schicht jede kontinuirliche multivariate Funktion approximiert werden.

https://www.sciencedirect.com/science/article/abs/pii/0893608089900208?via%3Dihub
Neuronale Netze koennen genutzt werden, um funktionen zu approximieren.

-> function approximators source here (what are NNs in realation to our question?)

(Given how they work and how minimax / a\* works, would it be smart to use them as a heuristic?)
https://www.reddit.com/r/reinforcementlearning/comments/10t08yj/minimax_with_neural_network_evaluation_function/
-> nn are function approximators -> errors propagate (find better sources)

was macht eine gute heuristik aus?
How does randomization affect algo?

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
Zur besseren Darstellung sind die folgenden Werte auch noch einmal in Diagrammform im Anhang [B1], [B2], [B3] einzusehen.

Der MAE-Wert (Mean Absolute Error) [Q5, s. 103] gibt dabei die durchschnittliche absolute Differenz zwischen den tatsächlichen und den vorhergesagten Werten im Testset an. Ein niedriger MAE-Wert weist auf eine bessere Modellvorhersagegenauigkeit hin, da er die durchschnittliche Fehlergröße in der gleichen Einheit wie die Ausgangsdaten misst.

Der MSE-Wert (Mean Squared Error) [Q5, s. 103] misst die durchschnittliche quadratische Differenz zwischen den tatsächlichen und den vorhergesagten Werten im Testset. Dieser Wert betont größere Fehler stärker, da die Fehler quadriert werden. Ein niedriger MSE-Wert bedeutet eine geringere Streuung der Fehler und eine genauere Modellvorhersage.

Der R²-Wert (Bestimmtheitsmaß) [Q4, 3.1] quantifiziert den Anteil der Varianz der Zielvariable, der durch das Modell erklärt wird. Ein R²-Wert von 1 deutet auf eine perfekte Anpassung hin, während ein Wert von 0 darauf hinweist, dass das Modell keine bessere Erklärung für die Variabilität der Zielvariable bietet als das Mittel der beobachteten Werte.

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

## Fazit

Die Ergebnisse legen nahe, dass die Hinzunahme zusätzlicher Heuristiken nicht zwangsläufig zu einer Verbesserung der Modellleistung führt. Stattdessen scheint eine Überkomplexität der Eingabedaten die Fähigkeit des Modells, sinnvolle Zusammenhänge zu lernen, negativ zu beeinflussen. Ebenso hat das zweite Modell keine signifikanten Vorteile gegenüber dem ersten Modell gebracht, sodass die zusätzliche Komplexität des Convolutional Layers in diesem Fall nicht gerechtfertigt ist.

how about vs. minmax aus praktikum 1/2?
how about only picking from heuristics for certain times from game. Diffrent heuristics are better for different phases of the game. only put gamestates + heuristic in trainingdata if the heuristic is good for the phase of the game the gamestate is in ==> results in smooth transition between heuristics?
Heuristiks not normalized to each other
heuristic CountOfPiecesAndDames does not work => only own move never loses own piece

## Quellen & Referenzen TODO

[Q1] TODO  
[Q2] Implementierungsdetails aus Praktikum 1 (siehe [Dokumentation P1](https://raw.githubusercontent.com/Lesekater/HAW-KI-Praktika/refs/heads/main/p1_dokumentation.md))  
[Q3] Implementierungsdetails aus Praktikum 2 (siehe [Dokumentation P2](https://raw.githubusercontent.com/Lesekater/HAW-KI-Praktika/refs/heads/main/p2_dokumentation.md))  
[Q4] Machine Learning für Zeitreihen : Einstieg in Regressions-, ARIMA- und Deep Learning-Verfahren mit Python / Jochen Hirschle 	
Hirschle, Jochen; ISBN: 978-3-446-46814-6
[Q5] TensorFlow Pocket Primer Oswald Campesato; ISBN: 	
978-1-68392-366-4
[R1] Quellcode Dame-Anwendung (https://github.com/Lesekater/HAW-KI-Praktika.git)

## Bilder TODO: haben/ brauchen wir bilder?

[B1] P3_MAE.png ![MAE Werte von trainierten Modellen](https://raw.githubusercontent.com/Lesekater/HAW-KI-Praktika/refs/heads/main/P3_MAE.png)  
[B2] P3_MSE.png ![MSE Werte von trainierten Modellen](https://raw.githubusercontent.com/Lesekater/HAW-KI-Praktika/refs/heads/main/P3_MSE.png)  
[B3] P3_R^2.png ![R^2 Werte von trainierten Modellen](https://raw.githubusercontent.com/Lesekater/HAW-KI-Praktika/refs/heads/main/P3_R^2.png)
