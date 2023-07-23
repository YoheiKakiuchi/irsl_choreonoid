
Coordinates
===========

座標変換についての説明

3D vector
:math:`\mathbf{p} = ( x, y, z )`

rotation matrix      
:math:`\mathbf{R}`

:math:`\mathbf{R}^{-1} = \mathbf{R}^{T}`

.. math::
   T = \begin{pmatrix}
   \mathbf{R}  & \mathbf{p} \\
   \mathbf{0}  & 1
   \end{pmatrix}
   
.. math::
   T^{-1} = \begin{pmatrix}
   \mathbf{R}^{-1}  & - \mathbf{R}^{-1}\mathbf{p} \\
   \mathbf{0}  & 1
   \end{pmatrix}   

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

reference: 
