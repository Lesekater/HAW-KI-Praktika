# Aggregation von Heuristiken mithilfe von neuronalen Netzen

11.01.2024 \
Elias Wernicke, Lars Janssen

TODO:
Forschungsfrage ausarbeiten
Theorie smoothen
quellen finden
fuer elias part quellen finden
fatzit schreiben

## Forschungsfrage

Wie gut kann ein neuronales Netz mehrere Heuristiken aggregieren?

## Theorie

### Neuronale Netze 

Neuronale Netze sind Systeme, welche die Struktur und Funktion von biologischen Gehirnen imitieren. [Q8, S.1]

Sie bestehen aus untereinander verbundenen Neuronen. Zu jedem Neuron gehört eine Aktivierungsfunktion mit welche entschieden wird, ob das Neuron auslöst und ein signal an andere Neuronen weiter gibt. Diese Funktion ist gewichtet und über Fine-tuning der einzelnen Gewichte kann das Netz trainiert werden. [Q8, S.1]

Diese Neuronen werden zu Schichten zusammengefasst.
Einem Input layer, in welchem die dort angesetzten Neuronen direkt die Eingabe für das neuronale Netz erhalten. Mehreren Hidden layers, welche die Daten transformieren und weiter verarbeiten.
Und schließlich dem Output layer, welcher die finale Entscheidung des Netzwerkes repräsentiert. [Q8, S.1]

Die am weitest verbreitete Art von neuronalen Netzen ist die des Feed-forward Netzes, in welcher die Signale nur von Input zu Output fließen. [Q8, S.1]

### Aggregation von Heuristiken? 

Das universelle approximations Theorem sagt aus, dass normale feed-forward neurale Netzwerke mit nur einer versteckten Schicht jede kontinuierliche multivariate Funktion approximiert werden. [Q6, S.1]  [Q7, S.1]


Da neuronale Netzwerke nur Funktionen approximieren und bei jedem Aufruf (abhängig von implementation) einen gewissen Zufallsfaktor beinhalten, sind wiederholte Entscheidungen bei selbem input immer leicht unterschiedlich. Dieses Rauschen ist eine durchaus unerwünschte Eigenschaft für Heuristiken. Da beim mehrfachen Anwenden von Neuronalen Netzen als Heuristiken sich der Effekt dieses Rauschen auf das letztendliche Ergebnis des Algorithmus bei tieferer Suche signifikant auswirken kann. [Q7, S.1]

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

Was das Netzwerk welches auf allen Heuristiken trainiert wurde wahrscheinlich unnutzbar gemacht hat, ist dass Heuristiken wie PiecesAtEndOfBoard und CountOfPieces den selben Spielzustand komplett unterschiedlich bewerten, sowohl gut als auch schlecht. Diese Unentschlossenheit der Bewertungen in den Trainingsdaten fuehrt zur Verunreinigung des Modells (Garbage in Garbage out).

Schlussendlich ist also die Frage, ob sich Heuristiken wie hier aufgefuehrt durch eine neuronals Netz aggregieren lassen, mit nein zu beantworten. Allerdings gibt es noch eine Verbesserung, die hier nicht eingesetzt wurde, welche aber potenzial haben koennte.

Diese Verbesserung liegt in der zussamensetztung der Trainingsdaten.
Um zu vermeiden, dass das neuronale Netz auf mehreren Heuristiken gleichzeitig trainiert wird, koennte man zwei oder mehr Heuristiken auswaehlen und das Spiel in genau so viele Phasen unterteilen. Und so nur von einer Heuristik bewertete Spielzustaende in die Trainingsdaten geben, wenn der Spielzustand zu der entsprechenden Phase gehoert. Die Phase koennte man beispielsweise an der Anzahl der Zuege messen. Mit einem solchen Ansatz wuerde man die unentschlossenheit aus den Trainingsdaten eventuell entfernen koennen.

## Quellen & Referenzen TODO

[Q2] Implementierungsdetails aus Praktikum 1 (siehe [Dokumentation P1](https://raw.githubusercontent.com/Lesekater/HAW-KI-Praktika/refs/heads/main/p1_dokumentation.md))  
[Q3] Implementierungsdetails aus Praktikum 2 (siehe [Dokumentation P2](https://raw.githubusercontent.com/Lesekater/HAW-KI-Praktika/refs/heads/main/p2_dokumentation.md))  
[Q4] Machine Learning für Zeitreihen : Einstieg in Regressions-, ARIMA- und Deep Learning-Verfahren mit Python / Jochen Hirschle 	
Hirschle, Jochen; ISBN: 978-3-446-46814-6
[Q5] TensorFlow Pocket Primer Oswald Campesato; ISBN: 978-1-68392-366-4
[Q6](https://arxiv.org/abs/2002.06505) A closer look at the approximation capabilities of neural networks / Kai Fong Ernest Chong
[Q7](https://www.sciencedirect.com/science/article/abs/pii/0893608089900208?via%3Dihub) Multilayer feedforward networks are universal approximators / Kurt Hornik, Maxwell Stinchcombe, Halbert White
[Q7](https://cdn.aaai.org/AAAI/1994/AAAI94-211.pdf)Evolving Nural Networks to Focus Minimax Search / David E. Moritarty, Risto Miikkulainen
[Q8](https://pmc.ncbi.nlm.nih.gov/articles/PMC6428006/)Artificial Neural Network: Understanding the Basic Concepts without Mathematics
[R1] Quellcode Dame-Anwendung (https://github.com/Lesekater/HAW-KI-Praktika.git)

## Bilder

[B1] P3_MAE.png ![MAE Werte von trainierten Modellen](https://raw.githubusercontent.com/Lesekater/HAW-KI-Praktika/refs/heads/main/P3_MAE.png)  
[B2] P3_MSE.png ![MSE Werte von trainierten Modellen](https://raw.githubusercontent.com/Lesekater/HAW-KI-Praktika/refs/heads/main/P3_MSE.png)  
[B3] P3_R^2.png ![R^2 Werte von trainierten Modellen](https://raw.githubusercontent.com/Lesekater/HAW-KI-Praktika/refs/heads/main/P3_R^2.png)
