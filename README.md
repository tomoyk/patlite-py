# patlite-py

パトライト社のパトランプを制御するためのプログラムです。動作検証は `NHP-3FB1` で行っています。

## 使い方

手順:
```
git clone https://github.com/tomoyk/patlite-py/
cd patlite-py/
python3 main.py
```

サンプルソース:
```
import patlite

def main():
    p = patlite.Patlite.get_instance()
    p.set_dest('192.168.0.169', 10000)

    p.RED = p.BLINK1
    p.YELLOW = p.BLINK2
    p.GREEN = p.ON
    p.BUZZER = p.STOP

    p.commit()
    

if __name__ == '__main__':
    main()
```

- 実装してあるLEDパターン: ON, OFF, BLINK1, BLINK2
- 実装してあるブザーパターン: STOP, SHORT, LONG, TINY, START
- 対応プロトコル: TCPのみ

## 実装/概要

マニュアルをもとにPNSコマンドを実装しています。そのため、ブザーパターン3,4や点滅パターン2にも対応しています。

書き込み（処理命令）のデータ構造は以下です。

|製品区分   |製品区分   |空き   |データサイズ   |データサイズ   |データ部   |
|---        |---        |---    |---            |---            |---        |
|0x58       |0x58       |0x53   |0x00           |0x06           |           |

データ部(6byte):

|パターン   |LED赤  |LED黄  |LED緑  |LED青  |LED白  |LEDブザー  |
|0x00       |消灯   |消灯   |消灯   |消灯   |消灯   |停止       |
|0x01       |点灯   |点灯   |点灯   |点灯   |点灯   |鳴動1      |
|0x02       |点滅1  |点滅1  |点滅1  |点滅1  |点滅1  |鳴動2      |
|0x03       |点滅2  |点滅2  |点滅2  |点滅2  |点滅2  |鳴動3      |
|0x04       |x      |x      |x      |x      |x      |鳴動4      |
|0x09       |維持   |維持   |維持   |維持   |維持   |維持       |

例えば全てのLEDを点灯させ、ブザーを鳴動1にする場合(送信時には空白を除く):

```
0x58 0x58 0x53 0x00 0x06 0x01 0x01 0x01 0x01 0x01 0x01
```