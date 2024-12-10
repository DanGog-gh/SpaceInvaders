[app]

# Название приложение
title = SpaceInvaders

# Имя пакета
package.name = space.invaders

# Домен пакета (необходим для упаковки Android/iOS)
package.domain = org.lesson

# Расширения исходных файлов которые должны быть включены в
# установочный пакет (оставьте пустым, чтобы включить все файлы)
source.include_exts = py,
    txt,
    png,
    jpg,
    jpeg,
    gif,
    kv,
    atlas,
    ttf,
    otf,
    mp3,
    ogg,
    wav,
    json,
    mp3,

# Директория в которой находится модуль main.py
source.dir = .

# Иконка приложения
# icon.filename = %(source.dir)s/data/images/icon.png

# Пресплеш приложения
# presplash.filename = %(source.dir)s/data/images/presplash.png
android.presplash_color = #1E0438

# Версия установочного пакета
version = 1.0.0

# Должно ли приложение быть полноэкранным или нет
fullscreen = 1

# Пакеты/модули зависимостей приложения
requirements = python3,
    kivy,
    https://github.com/kivymd/KivyMD/archive/master.zip,
    requests,
    urllib3,
    charset-normalizer,
    chardet,
    idna,
    pillow,
    materialyoucolor,
    exceptiongroup,
    asyncgui,
    asynckivy,
    mutagen

# Если это значение равно True, то будет пропущена попытка обновления
# Android SDK. Это может быть полезно, чтобы избежать избыточных загрузок
# из Интернета или сэкономить время когда требуется обновление, а вы просто
# хотите протестировать / собрать свой пакет
android.skip_update = True

# Если значение True, то автоматически принимается лицензия SDK соглашения.
# Это предназначено только для автоматизации. Если установлено значение False,
# по умолчанию, вам будет показана лицензия SDK при первом запуске
android.accept_sdk_license = True

# Архитектуры устройств для которых будет собран пакет
android.archs = arm64-v8a, armeabi-v7a

# Целевой уровень Android API.
android.api = 34

# Включает функцию автоматического резервного копирования Android
# (Android API >= 23)
android.allow_backup = True

# Разрешения приложения
# android.permissions = android.permission.INTERNET, android.permission.READ_MEDIA_AUDIO, android.permission.READ_EXTERNAL_STORAGE, android.permission.FOREGROUND_SERVICE

# Настройка ориентации экрана
orientation = portrait

# Формат, используемый для упаковки приложения в режиме выпуска
# (aab, apk или aar)
android.release_artifact = apk

# Перечень сервисов, которые работают в фотовом режиме
# services = Mediaplayerservice:service.py:foreground:sticky

[buildozer]
