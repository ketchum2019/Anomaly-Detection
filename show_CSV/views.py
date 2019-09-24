from django.shortcuts import render
from django.urls import reverse

# Create your views here.
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from sklearn.decomposition import IncrementalPCA

from sklearn.datasets import load_iris
from sklearn.cluster import DBSCAN
from sklearn import metrics
import numpy as np
import pandas as pd
import json

from operator import itemgetter
from itertools import groupby


def index(request):
    data = live_data_curve()  # pass live_data to index.html
    data = data.tolist()
    x_ipca, db_label = ipca_dbscan(0.5)
    anomaly_data, normal_data = partitioned_data(x_ipca, db_label)
    return render(request, "index.html", {
        'X_ipca': json.dumps(x_ipca.tolist()),
        'anomaly_data': json.dumps(anomaly_data.tolist()),
        'normal_data': json.dumps(normal_data.tolist()),
        'db_label': json.dumps(db_label.tolist()),
        'live_data': json.dumps(data),
    })


def incremental_ipca():
    iris = load_iris()
    x = iris.data
    # pd.read_csv()
    ipca = IncrementalPCA(n_components=3, batch_size=3)
    x_ipca_out = ipca.fit_transform(x)
    return x_ipca_out


def ipca_dbscan(eps):
    self_eps = eps
    # x_ipca = np.array(IPCA())
    x_ipca = incremental_ipca()
    clustering = DBSCAN(eps=self_eps, min_samples=2).fit(x_ipca)
    clustering_label = np.reshape(np.array(clustering.labels_, dtype=object), [-1, 1])
    # clustering_label = clustering.labels_
    return x_ipca, clustering_label


def partitioned_data(x_ipca, label):
    clusrering_num = np.unique(label)  # 查看聚类类别
    merge = np.hstack((x_ipca, label))

    anomaly_data = merge[merge[:, 3] == -1]
    anomaly_data = np.reshape(anomaly_data[:, :3], [-1, 3])

    normal_data = merge[merge[:, 3] != -1]
    normal_data = np.reshape(normal_data[:, :3], [-1, 3])

    return anomaly_data, normal_data


def test_IPCA_DBSCAN():
    x_ipca, label = ipca_dbscan(0.5)
    anomaly_data, normal_data = partitioned_data(x_ipca, label)
    print(type(anomaly_data), anomaly_data.tolist())
    print(type(x_ipca), x_ipca)
    # print(merge[np.argsort(merge[:, 3])])  # sort
    # print(groupby(merge, key=itemgetter(3)))
    # print(clusrering_num)
    # print(type(default(label)), default(label))


def default(obj):
    if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
                        np.int16, np.int32, np.int64, np.uint8,
                        np.uint16, np.uint32, np.uint64)):
        return int(obj)
    elif isinstance(obj, (np.float_, np.float16, np.float32,
                          np.float64)):
        return float(obj)
    elif isinstance(obj, (np.ndarray,)):  # add this line
        return obj.tolist()  # add this line
    return json.JSONEncoder.default(obj)


@csrf_exempt
def deal_post(request):
    if request.method == 'POST':
        para1 = request.POST.get('para1')
        para2 = request.POST.get('para2')
        # 传给另一个函数处理数据
        # return HttpResponseRedirect(reverse('show_CSV: deal_function'), 'index.html', )
        x_ipca, label = ipca_dbscan(float(para1))
        anomaly_data, normal_data = partitioned_data(x_ipca, label)
        response = JsonResponse({
            "anomaly": json.dumps(anomaly_data.tolist()),
            "normal": json.dumps(normal_data.tolist()),
        })
        return response
    else:
        return render(request, 'index.html')


def live_data_curve():
    # dataframe = pd.read_csv("../data/rec-center-hourly_out.csv")
    dataframe = pd.read_csv("data/rec-center-hourly_out.csv")

    data = dataframe.values
    return data


def optical_interconnection_data():
    dataframe = pd.read_csv("../data/optical_interconnection_network.csv")
    return dataframe


def test_optical_interconnection_data():
    data = optical_interconnection_data()
    print(data.head())


def test_live_data_curve():
    # 测试前修改路径 ../data/sin_30sec.csv
    data = live_data_curve()
    print(data)
