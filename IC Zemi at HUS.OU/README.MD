# 国際協力学ゼミ（日本語）
## ダウンロード
　ダウンロードは[こちら](https://github.com/frianasoa/Zotero-Styles-JP/releases/latest/download/chicago-author-date-iczemi-ja.csl)に右クリックして、名前をつけて保存してください。サンプルのワードファイルは[こちら](https://github.com/frianasoa/Zotero-Styles-JP/raw/main/IC%20Zemi%20at%20HUS.OU/chicago-author-date-iczemi-ja.docx)からダウンロードできる。<br/>

## インストール
ダウンロードしたファイルをダブルクリックでよいが、できない場合は図1の①→②→③を押して、ファイルを選択して、インストールする。<br/>
<figure>
<img style="border: dotted 1px; padding: 0.5em;" src="https://github.com/frianasoa/Zotero-Styles-JP/blob/main/assets/installing-style.png?raw=true" />
<figure-caption>図1. スタイルをインストールする</figure-caption>
</figure> <br/>

### インストールエラー
　このスタイルは日本語と英語を両方表示できるように、CSLの原則を守らない書き方をしなければならない。インストールする際、エラーはでるが、図２のように「OK」を押せば、インストールは無事にできる。<br/>

<figure>
<img style="border: dotted 1px; padding: 0.5em;" src="https://github.com/frianasoa/Zotero-Styles-JP/blob/main/assets/install-error.png?raw=true" />
<figure-caption>図2. インストールエラー</figure-caption>
</figure> <br/>

## 日本語の文献について
　日本語の文献の情報には「name-kana」の値を設定する必要がある。 <br/>
例えば 図3のように、「山下彰一（1999）」の「その他」のところに「name-kana:やましたしょういち」と入力する。<br/>

<figure>
<img style="border: dotted 1px; padding: 0.5em;" src="https://github.com/frianasoa/Zotero-Styles-JP/blob/main/assets/adding-extra.png?raw=true" />
<figure-caption>図3. 読み方（並べ替のキー）を設定する</figure-caption>
</figure>

## カタカナの名前について
　Zoteroは著者名が日本語だと自動的に「姓 → 名」の順で名前を表示する。しかし、ICゼミのスタイルではカタカナの名前は筆頭者だけ、「姓、名」というふうになって、その後は「名・姓」という表記になる。これは自動的にできないため、手入力で、「、」や「・」を入れる。<br/>

### 著者が３人以上の場合
著者が３人以上の場合は図4のように対応する。筆頭者の「名」の前に「、」を入れる①。２人目からは「単独のフィールド」（著者名を「姓、名」にわけない［表示を切り替えるには③を押す］）を使って「名・姓」②のようにいれる。<br/>

<figure>
<img style="border: dotted 1px; padding: 0.5em;" src="https://github.com/frianasoa/Zotero-Styles-JP/blob/main/assets/katakana-names.png?raw=true" />
<figure-caption>図4. 手入力でカタカナの名前を入れる</figure-caption>
</figure>

### 著者が２人の場合
著者が２人の場合は筆頭者の「名」の前に「、」を入れるだけ、そして、最終的に参考文献を修正する。

### なぜ手入力がいるか？
　現在のZoteroのバージョンは限界があるため（正しくはCSLの限界）、手入力がいる。将来のバージョンでは要らなくなる可能性はあるが、その時にこのスタイルを更新する。そうすると、お使いのZoteroの情報も通常（手入力した点を削除）に戻さないといけないが、更新したらまた通知する。