### БАГИ:

1. Если быстро стрелять враги будут взрываться по несколько раз.
2. Премиальное оружие неправильно подбирается.
3. Иногда при выстреле мгновенно умирает враг в последнем ряду.


Space Invaders
--------------

Space Invaders — shoot 'em up, в котором игрок управляет лазерной пушкой, 
передвигая её горизонтально, в нижней части экрана, а также отстреливая 
инопланетян, надвигающихся сверху экрана. Целью игры является уничтожение пяти 
рядов по одиннадцать инопланетян, которые двигаются горизонтально, а также 
вертикально, по направлению к низу экрана. Игрок имеет бесконечное количество 
патронов. Попадая в инопланетянина, игрок уничтожает его, за что получает очки. 
При уничтожении инопланетян увеличивается скорость движения оставшихся, а 
также ускоряется темп звуковых эффектов. При уничтожении всех инопланетян 
появляется новая, ещё более сильная волна, а игрок получает одно дополнительное 
очко жизни. Количество новых волн инопланетян неограниченно, что делает игру 
бесконечной.

<img height="256" src="https://raw.githubusercontent.com/DanGog-gh/SpaceInvaders/main/resources/images/screenshots/screenshot_1.png"/>

Добавить пару скриншотов игры.
Добавить описание краткое игры.

Dependency
----------

- [Kivy](https://github.com/kivy/kivy) >= 2.3.0 ([Installation](https://kivy.org/doc/stable/gettingstarted/installation.html))
- [KivyMD](https://github.com/kivymd/kivymd) >= 2.0.0
- [Python 3.10+](https://www.python.org/)

Добавить список технологий и библиотек на которых работает проект.

Deployment
----------

- скачать и установить VirtualBox;
- установить на VirtualBox Ubuntu 20.04;
- запустить Ubuntu, открыть консоль и установить необходимы зависимости:

```commandline
git clone git@github.com:DanGog-gh/SpaceInvaders.git

sudo apt install git
sudo apt install python3-pip
sudo apt install autoconf
sudo apt install libtool
sudo apt install pkg-config
sudo apt install zlib1g-dev
sudo apt libncurses5-dev
sudo apt libncursesw5-dev
sudo apt libtinfo5
sudo apt cmake
sudo apt libffi-dev
sudo apt libssl-dev
sudo apt install zip
sudo apt unzip
sudo apt openjdk-17-jdk

pip install --user --upgrade buildozer
pip install Cython==0.29.33
pip install setuptools virtualenv
```

Build APK
---------

```commandline
cd path/to/project
buildozer android debug
```


Здравствуйте!
