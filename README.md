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

    p.set_status("red", p.ON)
    p.set_status("yellow", p.BLINK1)
    p.set_status("green", p.BLINK2)
    p.set_status("buzzer", p.OFF)
    p.commit()
    
    ''' Reset
    p.reset_status()
    p.commit()
    '''


if __name__ == '__main__':
    main()
```

- 実装してあるLEDパターン: ON, OFF, BLINK1, BLINK2
- 実装してあるブザーパターン: OFF, SHORT, LONG, TINY, BEEP
- 対応プロトコル: TCPのみ

## httpserver

デフォルトで `0.0.0.0` の `8080` でHTTPサーバが起動します。

エンドポイント: `http://yourhost/patlite`

メソッド: GET

パラメータ: 
```
green/red/yellow:
- 1:点灯
- 2:点滅パターン1
- 3:点滅パターン2
- 0:消灯
buzzer:
- 0:停止
- 1:鳴動パターン4
- 2:鳴動パターン1
- 3:鳴動パターン2
- 4:鳴動パターン3
timeout:
- 初期値: 5
- 設定秒数が経過すると停止
```

リクエストの例: `http://yourhost:8080/patlite?red=1&yellow=2&green=3&buzzer=0&timeout=3`

## 実装/概要

マニュアルをもとにPNSコマンドを実装しています。そのため、ブザーパターン3,4や点滅パターン2にも対応しています。

書き込み（処理命令）のデータ構造は以下です。

|製品区分(1byte)|製品区分(1byte)|空き(1byte)   |データサイズ(1byte)   |データサイズ(1byte)   |データ部(6byte)   |
|---            |---            |---           |---                   |---                   |---               |
|0x58           |0x58           |0x53          |0x00                  |0x06                  |                  |

データ部(6byte):

|パターン   |LED赤  |LED黄  |LED緑  |LED青  |LED白  |LEDブザー  |
|---        |---    |---    |---    |---    |---    |---        |
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

## 参考サイト

chibieggさんがPython2系で書かれていたソースを一部、参考にさせていただきました。🙏

- [Pythonでシングルトン(Singleton)を実装してみる - [Dd]enzow(ill)? with DB and Python](http://www.denzow.me/entry/2018/01/28/171416)
- [chibiegg/pytlite: Control Patlite Signal Tower from Python](https://github.com/chibiegg/pytlite)
