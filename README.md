# midiControll
といっても、MIDIのコントローラではなく、MIDIのコントローラでFLLの調整・制御をしましょうという話。

## what you have to prepare:
ハードウエア：
- KORG nanoPAD2
- （SPIドライブ用の回路）
- （将来RasPiで動かすつもり）

開発環境：
- python3
- rtmidi2 パッケージ

テスト環境はWindows10上のVirtualBoxで動いている、ubuntu18.04.3

### ライブラリ等

rtmidi2 をインストールする前に下記のライブラリが必要

```
sudo apt-get install libasound2-dev
sudo apt-get install libjack-jackd2-dev
```
### rtmidi2　のインストール

https://github.com/gesellkammer/rtmidi2.git

clone して
``` sudo python3 setup.py install ```


## 使い方

### Padアサイン：

| Pad | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- |
|upper|(ZERO)|CH-Up|UNIT-UP|Ib On/Off|NA|NA|NA|Extract|
|lower|Fine|CH-Down|UNIT-Down|Ofs on/off|reset|FB on/off|integ on/off|8Hz on/off|  


### X-Y Pad:

- X: [ib]

- Y: [Ofs]

 - 通常は１回上下・左右フルにドラッグ（押しながら移動）するとフルスケール値の1/4変化する

 - ”Fine”を押しながらドラッグするとゆっくりとフルドラッグで127カウント変化

### ib, offset のクリア：

reset押しながら（ZERO）を押す

### フィードバック状態の解除：
　resetを押す。（8Hzは切れない）

### パラメタの出力
　extractを押す。（現在のところプリントアウトのみ）

2019/12  
