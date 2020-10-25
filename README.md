# HarvardMachine

## Function Block Diagram

![FBD](https://pbs.twimg.com/media/ElHJmVSUUAAEb0Z?format=png&name=large)

## Instruction Set

### Control Instructions
| 命令  | 引数  | 説明                                                    |
| ----- | ---- | ------------------------------------------------------- |
| LOAD  | あり  | 引数を累積器にセットする                                  |
| STORE | あり  | 累積器の値を引数のアドレスにセットする                     |
| LT    | あり  | 累積器の値が引数より小さい時0，それ以外の時1をCFにセットする |
| GT    | あり  | 累積器の値が引数より大きい時0，それ以外の時1をCFにセットする |
| BEQ   | あり  | CFが0の時，PCの値を引数に変更する                          |
| BNE   | あり  | CFが0の時，PCの値を引数に変更する                          |
| JUMP  | あり  | CFによらず，PCの値を引数に変更する                         |
| PRINT | あり  | 引数を出力する                                           |
| NOP   | なし  | 何もしない                                               |
| EOP   | なし  | プログラムの終了を示す                                    |

### Arithmetic Instructions
| 命令  | 引数  | 説明                                                    |
| ----- | ---- | ------------------------------------------------------- |
| ADD   | あり  | 累積器の値に引数を加算し，結果を累積器にセットする          |
| SUB   | あり  | 累積器の値に引数を減算し，結果を累積器にセットする          |
| MUL   | あり  | 累積器の値に引数を乗算し，結果を累積器にセットする          |
| DIV   | あり  | 累積器の値に引数を除算し，結果を累積器にセットする          |
| MOD   | あり  | 累積器の値に引数を余算し，結果を累積器にセットする          |
| NOT   | なし  | 累積器の値の論理否定をとり，結果を累積器にセットする        |
| OR    | あり  | 累積器の値と引数の論理和をとり，結果を累積器にセットする     |
| AND   | あり  | 累積器の値と引数の論理積をとり，結果を累積器にセットする     |
