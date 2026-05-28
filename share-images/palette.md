# SVG カラーパレット（slides.md 準拠）

`session01/images/` 以下の SVG 図版で使用する統一カラーパレット。
`session01/slides.md` の `style:` 設定（h1/h2/border の青系アクセント）と整合を取り、
`class: invert`（暗背景）で読みやすい配色にしている。

## 役割と色の対応

| 役割                                  | fill                       | stroke                 | text                       | 使いどころ                                                     |
| ------------------------------------- | -------------------------- | ---------------------- | -------------------------- | -------------------------------------------------------------- |
| **Primary blue**（標準ボックス）      | `#1e3a8a`                  | `#3b82f6`              | `#dbeafe`                  | ブラウザ / participant / 通常の要素（h2 border と同色 stroke） |
| **Cyan**（クラウド・別カテゴリ）      | `#155e75`                  | `#06b6d4`              | `#cffafe`                  | GitHub・サーバー側コンテナ・中間状態（パケット集合 等）        |
| **Emerald**（結果・成功・レスポンス） | `#064e3b`                  | `#10b981`              | `#a7f3d0`                  | 現在の状態・最終成果物・戻り値（git push / 組み立て後 等）     |
| **Amber**（Note・データ保管）         | `#fef3c7` または `#78350f` | `#d97706` 〜 `#f59e0b` | `#451a03` または `#fde68a` | sequence の Note / SQLite 等                                   |
| **Slate**（subdued）                  | `#334155`                  | `#94a3b8`              | `#cbd5e1`                  | 静的配信・lifeline・補助矢印                                   |
| **コンテナ/subgraph**                 | `#1e3a8a` (opacity 0.25)   | `#60a5fa` dashed       | `#93c5fd`                  | グルーピング枠                                                 |

## 線（矢印・lifeline）

| 用途                          | 色        | スタイル                           |
| ----------------------------- | --------- | ---------------------------------- |
| Forward arrow（主アクション） | `#60a5fa` | 実線（h1 と同色）                  |
| Response arrow（応答・戻り）  | `#34d399` | 実線または dashed `8 5`            |
| Secondary / dashed back       | `#94a3b8` | dashed `10 6`                      |
| Lifeline（sequence の縦線）   | `#94a3b8` | dashed `6 4`、`stroke-width="1.5"` |
| 矢印頭サイズ                  | —         | `markerWidth="8" markerHeight="8"` |

## ラベル・テキスト

| 用途                             | 色                                         |
| -------------------------------- | ------------------------------------------ |
| ボックス内テキスト（青系）       | `#dbeafe`                                  |
| ボックス内テキスト（cyan 系）    | `#cffafe`                                  |
| ボックス内テキスト（emerald 系） | `#a7f3d0`                                  |
| ボックス内テキスト（amber 系）   | `#451a03` (light bg) / `#fde68a` (dark bg) |
| 自立ラベル（アクセント）         | `#93c5fd`（h2 と同色）                     |
| 自立ラベル（中立）               | `#cbd5e1`                                  |

## slides.md 側の参照値

| 要素               | 色        | パレット内の対応    |
| ------------------ | --------- | ------------------- |
| `h1`               | `#60a5fa` | Forward arrow       |
| `h2`               | `#93c5fd` | アクセントラベル    |
| `h2` border-bottom | `#3b82f6` | Primary blue stroke |

## 意味づけのルール

- **Blue** = ローカル / 標準 / プライマリ要素
- **Cyan** = クラウド / リモート / 中間（in-transit）
- **Emerald** = 最終結果 / 成功 / 応答（return）
- **Amber** = 注釈 / 永続データ
- **Slate** = 補助 / 受動的要素 / 構造線

## SVG テンプレート（共通定義）

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 W H"
     font-family="'Hiragino Sans', 'Yu Gothic', 'Meiryo', 'Noto Sans CJK JP', sans-serif">
  <defs>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#60a5fa"/>
    </marker>
    <marker id="arrow-emerald" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#34d399"/>
    </marker>
    <marker id="arrow-slate" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#94a3b8"/>
    </marker>
  </defs>
  <!-- Primary blue box -->
  <rect x="..." y="..." width="..." height="..." rx="10"
        fill="#1e3a8a" stroke="#3b82f6" stroke-width="2"/>
  <text fill="#dbeafe" font-size="24" font-weight="bold">...</text>
</svg>
```

## 背景の扱い

- 個別の図（`git-savepoint.svg` など）は **背景透明** にして、スライドの `class: invert` 暗背景を透かす。
- 全体図（`overview.svg`）のように 1 枚で完結する大きな図のみ、`#0f172a` の独自カードを敷く。
