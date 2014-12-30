Installing Halfwaytree Dependencies
===========

###pygraphviz
(1) Run the following command:
```
sudo apt-get install -y graphviz libgraphviz-dev pkg-config python-pip
sudo pip install pygraphviz
```
(2) Test installation
```
import pygraphviz
```

###z3
(1) go to [http://z3.codeplex.com/SourceControl/list/changesets?branch=pure](http://z3.codeplex.com/SourceControl/list/changesets?branch=pure)

  * make sure to download unstable, the master branch doesn't work

(2) cd into the z3 folder and run the following command:
```
 python scripts/mk_make.py
 cd build
 make
 sudo make install
```

(3) Test installation

```
import z3
```

