# StackMachine

## Function Block Diagram

![FBD](https://pbs.twimg.com/media/Ej523BhU0AAcxe1?format=png&name=large)

## Instruction Set

### Control Instructions
| instruction | description                                    |
| ----------- | ---------------------------------------------- |
| PUSH        | データレジスタから値を取り出し，スタックにPUSHする |
| POP         | スタックから値を1つPOPする　　　　　　　　　　　　 |
| COPY        | スタックから値を1つPOPし，2回PUSHする            |
| JUMP        | スタックから値を1つPOPし，PCとMARの値を変更する   |
| PRINT       | スタックから値を1つPOPし，出力する                |
| NOP         | 何もしない                                      |

### Arithmetic & Logic Instructions
| instruction | description                                    |
| ----------- | ---------------------------------------------- |
| NEG         | スタックから値を1つPOPし，符号を反転してPUSHする   |
| ADD         | スタックから値を2つPOPし，加算してPUSHする     　 |
| SUB         | スタックから値を2つPOPし，減算してPUSHする        |
| MUL         | スタックから値を2つPOPし，乗算してPUSHする        |
| DIV         | スタックから値を2つPOPし，除算してPUSHする        |
| MOD         | スタックから値を2つPOPし，余算してPUSHする        |
| NOT         | スタックから値を1つPOPし，論理否定をとってPUSHする |
| OR          | スタックから値を2つPOPし，論理和をとってPUSHする 　|
| AND         | スタックから値を2つPOPし，論理積をとってPUSHする　 |
