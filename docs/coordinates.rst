
===========
Coordinates
===========

*********************
座標変換についての説明
*********************

^^^^^
3次元位置
^^^^^

位置は小文字の太字を用いて表される、実数3つのベクトルである。

3つの要素はそれぞれ、x軸、y軸、z軸の軸上の位置を表す。

縦ベクトルとして表すことが多い。

:math:`\mathbf{p} = [ x, y, z ]^{T}`

^^^^^
3次元の回転
^^^^^

3次元の回転は、回転行列を用いて表すことができる。

回転行列は3x3の行列で、基準座標系から見た回転された座標系列の
x軸、y軸、z軸を列方向に並べたものである。

:math:`\mathbf{R} = [ \mathbf{x} \mathbf{y} \mathbf{z} ]`

この行列は直交行列となっており、以下の
行列の転置と逆行列が同値となる。

:math:`\mathbf{R}^{-1} = \mathbf{R}^{T}`

3次元の回転の表し方としては、他に、
ロール・ピッチ・ヨー角(RPY)、単位クォータニオン(quaternion)、軸回り回転(AngleAxis)、等がある。

情報量としては3であるが、計算に使いやすい回転行列や、特異点がなく補間が容易なクォータニオンが使われる。
参考書を参照いただきたい。

.....
軸回り回転(AngleAxis)
.....


^^^^^
同時変換行列
^^^^^

3次元での姿勢は、3次元位置と3次元回転を用いて表すことができ、
位置の3自由度と回転の3自由度で6自由度となっている。

3次元での姿勢を表すのに、同次変換行列 T を用いる。
T は 3次元位置ベクトル :math:`\mathbf{p}` と
3次元回転行列 ::math:`\mathbf{R}` を用いて、以下のように4x4行列として表される。

.. math::
   T = \begin{pmatrix}
   \mathbf{R}  & \mathbf{p} \\
   \mathbf{0}  & 1
   \end{pmatrix}

T の逆行列は以下のようになる。

.. math::
   T^{-1} = \begin{pmatrix}
   \mathbf{R}^{-1}  & - \mathbf{R}^{-1}\mathbf{p} \\
   \mathbf{0}  & 1
   \end{pmatrix}

T の掛け算は、a, bを添え字として以下のようになる。

.. math::
   T_a = \begin{pmatrix}
   \mathbf{R}_a  & \mathbf{p}_a \\
   \mathbf{0}  & 1
   \end{pmatrix}

.. math::
   T_b = \begin{pmatrix}
   \mathbf{R}_b  & \mathbf{p}_b \\
   \mathbf{0}  & 1
   \end{pmatrix}

.. math::
   T_a \times T_b = \begin{pmatrix}
   \mathbf{R}_a\mathbf{R}_b  & \mathbf{R}_a\mathbf{p}_b  + \mathbf{p}_a \\
   \mathbf{0}  & 1
   \end{pmatrix}

^^^^^
座標系
^^^^^


^^^^^
剛体リンクの座標系
^^^^^


*********************
座標系とcoordinatesの関係
*********************

coordinatesクラス (cnoid.IRSLCoords.coordinates) は、
同次変換行列の操作を行うためのクラスである。

coordinatesクラスのインスタンスは、
3次元位置ベクトル :math:`\mathbf{p}` と
3次元回転行列 ::math:`\mathbf{R}` を持つ。

^^^^
回転行列と３次元位置の取り出し
^^^^

coordinates のプロパティとして、
以下のように
::math:`mathbf{p}`
と
::math:`mathbf{R}`
を取り出せる。

以下、Tはcoordinateクラスのインスタンスである。

.. code-block:: python

    T.pos ## 3次元位置
    >>>

    T.rot ## 回転行列
    >>>


^^^^
ベクトルを変換するメソッド
^^^^

以下、
::math:`mathbf{v}`
は3次元ベクトル (numpy.array) である。

.. code-block:: python

    T.rotate_vector(v)
    >>>

    T.inverse_rotate_vector(v)
    >>>

    T.transform_vector(v)
    >>>

    T.inverse_transform_vector(v)
    >>>


^^^^
座標系を返すメソッド (座標系を変更しない)
^^^^

.. code-block:: python

    T.inverse_transformation()
    >>>

    T.transformation(A)
    >>>


^^^^
座標系を変更するメソッド
^^^^

.. code-block:: python

    T.newcoords(A)
    >>>

    T.move_to(A)
    >>>

    T.translate(A)
    >>>

    T.locate(A)
    >>>

    T.transform(A)
    >>>


^^^^
例題
^^^^

******
参考書
******

実践ロボット制御 https://www.ohmsha.co.jp/book/9784274224300/

第2章 姿勢の記述 及び 第4章 運動学の一般的表現 の内容が参考になる

