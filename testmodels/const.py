# -*- coding: utf-8 -*-
# TODO
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TMP_DIR_PATH = os.path.join(BASE_DIR_PATH, 'tmp')

RESULT_DIR_PATH = os.path.join(BASE_DIR_PATH, 'result')

SQLITE_DB_NAME = os.path.join(BASE_DIR_PATH, 'db.sqlite3')

CSV_ITEMS_PRE_NAME = os.path.join(TMP_DIR_PATH, 'items')
CSV_ITEMS_TMP_PRE_NAME = os.path.join(TMP_DIR_PATH, 'tmp_items.csv')

CNV_DIR_PATH = os.path.join(BASE_DIR_PATH, 'convert')
CNV_TRANS_DIR_PATH = os.path.join(CNV_DIR_PATH, 'trans_csv')

CSV_BRAND = os.path.join(CNV_TRANS_DIR_PATH, 'brand.csv')
CSV_CAT = os.path.join(CNV_TRANS_DIR_PATH, 'cat.csv')
CSV_CAT1 = os.path.join(CNV_TRANS_DIR_PATH, 'cat1.csv')
CSV_CAT2 = os.path.join(CNV_TRANS_DIR_PATH, 'cat2.csv')
CSV_CAT3 = os.path.join(CNV_TRANS_DIR_PATH, 'cat3.csv')
CSV_COLOR = os.path.join(CNV_TRANS_DIR_PATH, 'color.csv')
CSV_PRODUCT = os.path.join(CNV_TRANS_DIR_PATH, 'prod.csv')

CSV_ITEM_TRANS = os.path.join(TMP_DIR_PATH, 'items_trans.csv')
CSV_ITEM_CAT = os.path.join(RESULT_DIR_PATH, 'item_cat.csv')
CSV_ITEM = os.path.join(RESULT_DIR_PATH, 'item.csv')
CSV_SELECT = os.path.join(RESULT_DIR_PATH, "select.csv")
CSV_SELECT_BASE = os.path.join(TMP_DIR_PATH, "select_base.csv")
CSV_TMP_SELECT = os.path.join(TMP_DIR_PATH, "tmp_select.csv")


STATUS_INIT = 0

STATUS_ON = 1

STATUS_OFF = 2

FIND_INIT = 0

FIND_PROGRESS = 1

FIND_SUCCESS = 2

FIND_ERROR = 3

SCRAPY_START = 0
SCRAPY_PROGRESS = 1
SCRAPY_RESTART = 2
SCRAPY_STOP = 3
# No touch!
SENDER_EMAIL_ADDR = 'root@tk2-245-32333.vs.sakura.ne.jp'
CC_MAIL = ['info@applink.co.jp']

IMAGE_PATH = os.path.join(RESULT_DIR_PATH, "img")

IMAGE_UPLOAD_PATH = "http://image.rakuten.co.jp/megasports/cabinet/"
FTP_HOST = 'upload.rakuten.ne.jp'
FTP_USER = 'megasports'
FTP_PW = 'Takashi1'
