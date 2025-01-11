generate data with `python3.10 main.py 0 9 10 4 &`
- generating data with mcgs

read in data with convert-script and label it with heuristics

model01:
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

model02:
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

# Output
## only CountOfPiecesAndDames
Mean Absolute Error (MAE): 0.0702
Mean Squared Error (MSE): 0.0083
R² Score: 0.8437

![alt text](./neural_net_trainig_docu/image-4.png)

![alt text](./neural_net_trainig_docu/image-5.png)

## only CountOfPiecesAndDames (with model 01)
Mean Absolute Error (MAE): 0.0662
Mean Squared Error (MSE): 0.0076
R² Score: 0.8571

![alt text](./neural_net_trainig_docu/image-6.png)

![alt text](./neural_net_trainig_docu/image-7.png)

## with CountOfPiecesAndDames, CountOfPiecesAtEndOfBoard
Mean Absolute Error (MAE): 0.1444
Mean Squared Error (MSE): 0.0295
R² Score: 0.5256

![alt text](./neural_net_trainig_docu/image-2.png)

![alt text](./neural_net_trainig_docu/image-3.png)

## with CountOfPiecesAndDames, CountOfPiecesAtEndOfBoard (with model 01)
Mean Absolute Error (MAE): 0.1374
Mean Squared Error (MSE): 0.0264
R² Score: 0.5777

![alt text](./neural_net_trainig_docu/image-8.png)

![alt text](./neural_net_trainig_docu/image-9.png)

## with CountOfPiecesAndDames, CountOfPiecesAtEndOfBoard, ProgressPiecesOnBoard
Mean Absolute Error (MAE): 0.2886
Mean Squared Error (MSE): 0.1218
R² Score: 0.0385

![alt text](./neural_net_trainig_docu/image.png)

![alt text](./neural_net_trainig_docu/image-1.png)

# Output
## with CountOfPiecesAndDames, CountOfPiecesAtEndOfBoard, ProgressPiecesOnBoard (with model 01)
Mean Absolute Error (MAE): 0.2863
Mean Squared Error (MSE): 0.1210
R² Score: 0.0457

![alt text](./neural_net_trainig_docu/image-10.png)

![alt text](./neural_net_trainig_docu/image-11.png)

## with \<all>
Mean Absolute Error (MAE): 0.3126
Mean Squared Error (MSE): 0.1218
R² Score: 0.0033

![alt text](./neural_net_trainig_docu/image-12.png)

![alt text](./neural_net_trainig_docu/image-13.png)

