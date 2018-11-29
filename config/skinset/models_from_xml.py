#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""
models_from_xml.py

XMLファイルを元にFixtureを生成します.
"""

import os
import re
import sys
import xml.etree.ElementTree as ET

import yaml

# 出力先YAMLファイル
yaml_file_path = './fixture/master.yaml'
# XMLファイル格納場所
xml_root_path = '../../data'
# 画像ファイル格納場所
img_root_path = '../static/skinset/ui.ipf'


def find_all_files(directory):
    for root, dirs, files in os.walk(directory, followlinks=True):
        for f in files:
            file_name, ext = os.path.splitext(f)
            if ext in ('.skn', '.xml'):
                yield os.path.join(root, f)


def process_image(image, xml_file):
    # <image>要素は他の要素を内包しない（must）
    if len(image) != 0:
        sys.stderr.write("{}: <image> has child tag (length={})\n".format(
            xml_file,
            len(image)
        ))
        return None

    # <image>要素は"name"、"file"、"imgrect"の3つの属性をもつ（must）
    if ('name' not in image.attrib.keys()
            or 'file' not in image.attrib.keys()
            or 'imgrect' not in image.attrib.keys()):
        sys.stderr.write("{}: <image> is invalid:{}\n".format(
            xml_file,
            image.attrib
        ))
        return None

    # <image>要素は"CMM_Caption"属性をもつかもしれない（may）
    # <image>要素は"Caption"属性をもつかもしれない（may）
    dic = {}
    for attr in image.attrib.keys():
        if 'name' == attr:
            dic.setdefault(attr, image.attrib[attr])
            pass
        elif 'file' == attr:
            # xml内のファイルセパレータはバックスラッシュ（\）で記載される
            tmp_path = image.attrib['file'].replace('\\', os.sep)
            # パスの先頭にファイルセパレータが記載されることがあるが、Model上では除去した形で格納する
            tmp_path = re.sub((r'^' + os.sep), '', tmp_path)
            dic.setdefault(attr, tmp_path)
            pass
        elif 'imgrect' == attr:
            # rect属性は4つのtuple（left, top, width, height）
            imgrect = image.attrib['imgrect'].split()
            if len(imgrect) != 4:
                sys.stderr.write('{}: attribute "imgrect" is invalid format ({})\n'.format(
                    xml_file,
                    image.attrib['imgrect']
                ))
            else:
                dic.setdefault(attr, image.attrib['imgrect'])
        elif 'CMM_Caption' == attr:
            # TODO: CMM_Caption属性対応
            continue
        elif 'Caption' == attr:
            # TODO: Caption属性対応
            pass
        else:
            sys.stderr.write('{}: <image> has unknown attribute (attr={})\n'.format(
                xml_file,
                attr
            ))
            return None

    return dic


def process_imagelist(imagelist, xml_file):
    images = []

    # <imagelist>要素は"category"属性をもっているかもしれない（may）
    category = 'None'
    if 'category' in imagelist.attrib:
        category = imagelist.attrib['category']
    # <imagelist>要素は"Category"属性をもっているかもしれない（may）
    #    if 'Category' in imagelist.attrib:
    #        print(imagelist.attrib['Category'])

    # <imagelist>要素は<image>要素を内包する（may）
    for child in imagelist:
        # <imagelist>要素は<image>要素以外を内包しない（must）
        if child.tag == 'image':
            image = process_image(child, xml_file)
            if image:
                image.setdefault('category', category)
                images.append(image)
        else:
            sys.stderr.write(xml_file + ": not image in imagelist (tag=" + child.tag + ")\n")

    return images


def process_skinlist(skinlist, xml_file):
    imgs = []

    # <skinlist>要素は"category"属性をもつ（may）
    category = 'None'
    if 'category' in skinlist.attrib:
        category = skinlist.attrib['category']

    # <skinlist>要素は<skin>要素をもつ（may）
    for skin in skinlist:
        # <skin>要素は"name"属性をもつ（must）
        skin_name = skin.attrib['name']
        # <skin>要素は"texture"属性をもつ（must）
        # xml内のファイルセパレータはバックスラッシュ（\）で記載される
        texture = skin.attrib['texture'].replace('\\', os.sep)
        # パスの先頭にファイルセパレータが記載されることがあるが、Model上では除去した形で格納する
        texture = re.sub((r'^' + os.sep), '', texture)

        # <skin>要素は<img>要素をもつ（may）
        for img in skin:
            # <img>要素は"name"属性をもつ（must）
            name = img.attrib['name']
            # <img>要素は"imgrect"属性をもつ（must）
            if 'imgrect' in img.attrib:
                imgs.append({
                    'skin_category': category,
                    'texture': texture,
                    'skin_name': skin_name,
                    'name': name,
                    'imgrect': img.attrib['imgrect']
                })
            else:
                # "imgrect"属性をもたないimgはエラーとして扱う
                sys.stderr.write('{}:no imgrect {}/{}/{}\n'.format(xml_file, category, skin_name, name))

    return imgs


def process_skinset(skinset, xml_file):
    dic = {}
    # <skinset>要素は、下記の要素を0個以上内包する（may）
    # 下位以外の要素は内包しない（must）
    # - <skinlist>要素
    # - <imagelist>要素
    # - <fontlist>要素
    # - <effectimagelist>要素
    # - <spriteimagelist>要素
    # - <layerlist>要素
    for child in skinset:
        if child.tag == 'skinlist':
            for img in process_skinlist(child, xml_file):
                dic.setdefault(child.tag, [])
                dic[child.tag].append(img)
            pass
        elif child.tag == 'imagelist':
            for img in process_imagelist(child, xml_file):
                dic.setdefault(child.tag, [])
                dic[child.tag].append(img)
        elif child.tag == 'fontlist':
            # TODO:fontlist対応
            pass
        elif child.tag == 'effectimagelist':
            # TODO:effectimagelist対応
            pass
        elif child.tag == 'spriteimagelist':
            # TODO:spriteimagelist対応
            pass
        elif child.tag == 'layerlist':
            # TODO:layerlist対応
            pass
        else:
            # 不明な子要素
            sys.stderr.write(xml_file + ':include unknown tag =' + child.tag + '\n')
            continue

    return dic


if __name__ == '__main__':
    all_images = []

    image_categories = {}
    skin_categories = {}
    skins = {}
    crop_images = []

    for xml_file in find_all_files(xml_root_path):
        try:
            tree = ET.parse(xml_file)
        except ET.ParseError as err:
            # そもそもXMLとして読み込めないファイル
            sys.stderr.write(xml_file + ':' + err.msg)
            continue

        # ルートタグはskinsetである（must）
        if tree.getroot().tag != 'skinset':
            sys.stderr.write(xml_file + ':the root tag is not "skinset"\n')
            continue

        # skinsetはname属性をもつ（must）
        # （実データとしてはname属性を持たないskinsetも存在するため処理継続させる）
        if 'name' not in tree.getroot().attrib:
            sys.stderr.write(xml_file + ':the "skinset" element is not has "name" attribute\n')

        # ルートタグの直接の子要素を収集、出現数チェック
        skinset = process_skinset(tree.getroot(), xml_file)

        # skinsetの定義のみ、というのもある？
        if len(skinset) == 0:
            sys.stderr.write(xml_file + ':the root element is not have child\n')
            continue

        source_path = re.sub(r'^' + xml_root_path + '/', '', xml_file)
        for k in skinset:
            if k == 'imagelist':
                # <skinset/imagelist/image>を収集
                for image in skinset[k]:
                    # 画像ファイルの存在確認
                    img_file_path = os.path.join(img_root_path, image['file'])
                    if os.path.exists(img_file_path):
                        # ImageCategory
                        category = image['category']
                        if category not in image_categories:
                            image_categories.setdefault(category, len(image_categories) + 1)
                        # CropImage
                        crop_images.append({
                            'name': image['name'],
                            'imgrect': image['imgrect'],
                            'file': image['file'],
                            'source_path': source_path,
                            'image_category': image_categories[category]
                        })
                    else:
                        sys.stderr.write('{}: {} no such file\n'.format(xml_file, img_file_path))
            elif k == 'skinlist':
                # <skinset/skin/img>を収集
                for image in skinset[k]:
                    # 画像ファイルの存在確認
                    img_file_path = os.path.join(img_root_path, image['texture'])
                    if os.path.exists(img_file_path):
                        # SkinCategory
                        category = image['skin_category']
                        if category not in skin_categories:
                            skin_categories.setdefault(category, len(skin_categories) + 1)
                        # Skin
                        skin_name = image['skin_name']
                        if skin_name not in skins:
                            skins.setdefault(skin_name, {
                                'id': len(skins) + 1,
                                'category_id': skin_categories[category],
                            })
                        # CropImage
                        crop_images.append({
                            'name': image['name'],
                            'imgrect': image['imgrect'],
                            'file': image['texture'],
                            'source_path': source_path,
                            'skin': skins[skin_name]['id']
                        })

            else:
                sys.stderr.write('{}:unknown element "{}"\n', xml_file, k)

    # fixture用にデータを修飾する
    tmp_yaml = []
    for category in image_categories:
        tmp_yaml.append({
            'model': 'skinset.imagecategory',
            'pk': image_categories[category],
            'fields': {'category': category}
        })
    for category in skin_categories:
        tmp_yaml.append({
            'model': 'skinset.skincategory',
            'pk': skin_categories[category],
            'fields': {'category': category}
        })
    for skin in skins:
        tmp_yaml.append({
            'model': 'skinset.skin',
            'pk': skins[skin]['id'],
            'fields': {
                'name': skin,
                'category': skins[skin]['category_id']
            }
        })
    for i, image in enumerate(crop_images):
        tmp_yaml.append({
            'model': 'skinset.cropimage',
            'pk': (i + 1),
            'fields': image
        })

    # YAML出力
    with open(yaml_file_path, 'w') as out:
        yaml.dump(tmp_yaml, stream=out, default_flow_style=False)
