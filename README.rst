ClearMap
========

ClearMap is a toolbox for the analysis and registration of volumetric data
from cleared tissues.

ClearMap is targeted towards large lightsheet volumetric imaging data
of iDISCO+ cleared mouse brains samples, their registration to the Allen brain atlas,
volumetric image processing and statistical analysis.

The method is fully described in this `Cell paper <http://www.cell.com/cell/abstract/S0092-8674%2816%2930555-4>`_. 
For further details visit the `iDISCO website <https://idisco.info/>`_ and 
the `ClearMap documentation <https://rawgit.com/ChristophKirst/ClearMap/master/docs/_build/html/index.html>`_.

= = = = = 
This version of ClearMap is adapted for manual intervention: 
1) Manual alignment via landmarks (using FIJI's BigWarp plugin <https://imagej.net/BigWarp>). Note that this means that alignment between the channels also does not work anymore.
2) Manual background removal via e.g. FIJI or Imaris; Note that this means that the background has to have already been removed before starting. As a consequence, the internal background removal does not do anything except pass the data on. 
= = = = = 

Installation
------------

Install ClearMap by cloning it form `github <http://www.github.com/>`_::

    $ git clone https://github.com/MoritzNegwer/ClearMap.git

See `GIT.md <https://github.com/ChristophKirst/ClearMap/blob/master/GIT.md>`_ for basic help with git.

If you want to register data to reference images via elastix or
classify pixels via ilastik configure the /ClearMap/Settings.py file.

You will most likely also need to install several python packages e.g. via 
pip or apt-get.

See the `documentation <https://rawgit.com/ChristophKirst/ClearMap/master/docs/_build/html/index.html>`_ for more details.

Additional files for mouse brain registration can be found on the `iDISCO website <https://idisco.info/>`_.


Quickstart
----------

   * see the template scripts in the `./ClearMap/Scripts <https://github.com/MoritzNegwer/ClearMap/tree/master/ClearMap/Scripts>`_ folder 
   * see the `ClearMap documentation <https://rawgit.com/MoritzNegwer/ClearMap/master/docs/_build/html/index.html>`_ 


Copyright
---------
    (c) 2016 Christoph Kirst
    The Rockefeller University, 
    ckirst@rockefeller.edu

License
-------
    GPLv3, see LICENSE.txt for details.



