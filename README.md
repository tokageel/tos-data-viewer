# tos-data-viewer
ToSのLua層で使用可能なリソースを閲覧するためのサーバアプリです.

ここで提供するのは閲覧機能のみで、閲覧対象のリソースファイル自体は含んでいません.
展開済みのaddon.ipf、ui.ipf、ui.ipfを別途用意する必要があります.

## 環境
* Python 3.7
* Django 2.1.3
* PyYAML 3.13
* Pillow 5.3.0 

```bash
pip install PyYaml Pillow
```

## インストール

マイグレーション
```bash
cd <path_to_your_installed_dir>
cd config
python3 manage.py startapp skinset
python3 manage.py makemigrations
python3 manage.py migrate
```

Fixture作成
```bash
cp -r <path_to_your_data> data/
cp -r <path_to_ui.ipf> static/skinset/
cd skinset
python3 models_from_xml.py
cd ..
```

Fixture適用
```bash
python3 manage.py loaddata skinset/fixture/master.yaml
```

起動
```bash
python3 manage.py runserver 8000
```
