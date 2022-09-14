import os
import json
import io
import flask

import numpy as np
import lightgbm as lgb

prefix = '/opt/ml/'
model_path = os.path.join(prefix, 'model', 'lightgbm_model.txt')

# モデルをラップするクラス
class ScoringService(object):
    model = None

    @classmethod
    def get_model(cls):
        """クラスが保持しているモデルを返します。モデルを読み込んでなければ読み込みます。"""
        if cls.model == None:
            cls.model = lgb.Booster(model_file=model_path)
        return cls.model

    @classmethod
    def predict(cls, input):
        """推論処理

        Args:
            input (array-like object): 推論を行う対象の特徴量データ"""
        clf = cls.get_model()
        return clf.predict(input)

# 推論処理を提供するflaskアプリとして定義
app = flask.Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    """ヘルスチェックリクエスト
    コンテナが正常に動いているかどうかを確認する。ここで200を返すことで正常に動作していることを伝える。
    """
    health = ScoringService.get_model() is not None

    status = 200 if health else 404
    return flask.Response(response='\n', status=status, mimetype='application/json')

@app.route('/invocations', methods=['POST'])
def transformation():
    """推論リクエスト
    CSVデータが送られてくるので、そのデータを推論する。推論結果をCSVデータに変換して返す。
    """
    data = None

    # CSVデータを読み込む
    if flask.request.content_type == 'text/csv':
        with io.StringIO(flask.request.data.decode('utf-8')) as f:
            data = np.loadtxt(f, delimiter=',')
    else:
        return flask.Response(response='This predictor only supports CSV data', status=415, mimetype='text/plain')

    print('Invoked with {} records'.format(data.shape[0]))

    # 推論実行
    predictions = ScoringService.predict(data)

    # jsonに変換し、レスポンスデータを作成
    result = json.dumps({'results':predictions.tolist()})

    # レスポンスを返す
    return flask.Response(response=result, status=200, mimetype='text/json')