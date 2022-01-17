# RPA for attendance management
自社HPで管理している出退勤、休憩時間のデータを外部の給料計算、打刻管理のサイトに自動入力するシステム。
seluniumライブラリを用いたスクレイピングを活用しています。いわゆるRPAってやつでしょうか。

### 使用技術
Python

### 処理内容

<table>
  <caption>実際の打刻が記録されている、データを引っ張りたいページ（以降、甲と呼びます）</caption>
  <tr>
    <th>名前</th>
    <th>出勤時間</th>
    <th>退勤時間</th>
    <th>休憩時間</th>
    <th>ヘルプ店舗</th>
    <th>出勤時間</th>
    <th>退勤時間</th>
  </tr>
  <tr>
    <td>スタッフA</td>
    <td>10:08</td>
    <td>23:35</td>
    <td>02:20</td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>スタッフE</td>
    <td>10:53</td>
    <td>17:16</td>
    <td></td>
    <td>店舗Y（別店舗）</td>
    <td>10:53</td>
    <td>17:16</td>
  </tr>
  <tr>
    <td>スタッフC</td>
    <td>10:58</td>
    <td>24:10</td>
    <td>1:56</td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>スタッフG</td>
    <td>17:50</td>
    <td>24:09</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>スタッフF</td>
    <td>17:55</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
</table>
<table>
  <caption>事前に決まったシフトと実際の打刻データを保存するための別サイトのページ（以降、乙と呼びます）</caption>
  <tr>
    <th>名前</th>
    <th>シフト</th>
    <th>〜省略〜</th>
    <th>出退勤</th>
    <th>休憩</th>
    <th>〜省略〜</th>
  </tr>
  <tr>
    <td>スタッフA</td>
    <td>
      <div>
      10:30 ~ 15:00
      </div>
      <div>
      17:00 ~ 00:00
      </div>
    </td>
    <td>・・・</td>
    <td>
    [form]
    ~
    [form]
    </td>
    <td>
    [form]
    ~
    [form]
    </td>
    <td>・・・</td>
  </tr>
  <tr>
    <td>スタッフB</td>
    <td>
    </td>
    <td>・・・</td>
    <td>
    [form]
    ~
    [form]
    </td>
    <td>
    [form]
    ~
    [form]
    </td>
    <td>・・・</td>
  </tr>
  <tr>
    <td>スタッフC</td>
    <td>
      <div>
      11:00 ~ 15:00
      </div>
      <div>
      17:00 ~ 00:00
      </div>
    </td>
    <td>・・・</td>
    <td>
    [form]
    ~
    [form]
    </td>
    <td>
    [form]
    ~
    [form]
    </td>
    <td>・・・</td>
  </tr>
  <tr>
    <td>スタッフD</td>
    <td>
    </td>
    <td>・・・</td>
    <td>
    [form]
    ~
    [form]
    </td>
    <td>
    [form]
    ~
    [form]
    </td>
    <td>・・・</td>
  </tr>
  <tr>
    <td>スタッフE</td>
    <td>
    </td>
    <td>・・・</td>
    <td>
    [form]
    ~
    [form]
    </td>
    <td>
    [form]
    ~
    [form]
    </td>
    <td>・・・</td>
  </tr>
  <tr>
    <td>スタッフF</td>
    <td>
    </td>
    <td>・・・</td>
    <td>
    [form]
    ~
    [form]
    </td>
    <td>
    [form]
    ~
    [form]
    </td>
    <td>・・・</td>
  </tr>
  <tr>
    <td>スタッフG</td>
    <td>
      <div>
      17:00 ~ 00:00
      </div>
    </td>
    <td>・・・</td>
    <td>
    [form]
    ~
    [form]
    </td>
    <td>
    [form]
    ~
    [form]
    </td>
    <td>・・・</td>
  </tr>
</table>
基本的な処理の流れとしては、
<ol>
  <li>甲に自動ログイン</li>
  <li>自動処理をしたい日付を入力し、ページ遷移</li>
  <li>名前、出退勤データなどを、それぞれリストに格納</li>
  <li>乙に自動ログインし、ページ遷移</li>
  <li>乙にある全スタッフの名前をリストに格納</li>
  <li>甲で取得したデータと合致する名前を持つ乙の列を特定する</li>
  <li>乙上で事前に登録されているシフトデータを取得する</li>
  <li>給料計算が30分単位のため、30分単位のデータに変換して、出退勤、休憩開始終了時間のフォームにデータを入力する。７で取得したシフトデータと実際の打刻データに相違がある場合は後でまとめて出力するためにnoticesをリストに格納。</li>
  <li>保存</li>
  <li>８でnoticesリストに格納したnoticeがある場合noticesを出力する。</li>
</ol>

### 工夫した点や、苦労した点
基本的に、データをもとに判別してそれに応じて処理を変えていく流れは、様々なパターンを考慮しなければならなかったからかなり工夫した。
特に以下に関しての判別
<ul>
  <li>乙上シフトに登録されてないのに出勤した人がいる場合</li>
  <li>他店舗にヘルプへ行った人がいる場合（乙上には登録してはいけない）</li>
  <li>甲上には休憩開始時間の記載がされないため、乙上のデータに基づいて休憩開始時間を予測する</li>
  <li>５時間より長く働いたが、休憩をしなかった人は、出勤時間を１時間早めてそこから１時間休憩したことにする処理</li>
  <li>30分単位の給料計算のため、超過分を切り捨てる処理</li>
  <li>等々！！</li>
</ul>
その他２４３０など、2400より大きいデータは、甲において不適切なデータとして弾かれるため、そこを突破するための処理や、
シフトのデータと違う場合のnoticesの出力や、退勤の打刻し忘れた場合にダミーでデータを入れてそれをnoticesに格納することで、
甲に手動で打刻する際のヒューマンエラーの可能性のあるデータを自動で知らせる処理など...

