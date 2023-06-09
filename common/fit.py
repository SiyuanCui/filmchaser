"""
algorithm
"""
from abc import ABCMeta, abstractmethod
import numpy as np
from collections import defaultdict


class CF_base(metaclass=ABCMeta):
    def __init__(self, k=3):
        self.k = k
        self.n_user = None
        self.n_item = None

    @abstractmethod
    def init_param(self, data):
        pass

    @abstractmethod
    def cal_prediction(self, *args):
        pass

    @abstractmethod
    def cal_recommendation(self, user_id, data):
        pass

    def fit(self, data):
        # Calculate recommended items for all users
        self.init_param(data)
        all_users = []
        for i in range(self.n_user):
            all_users.append(self.cal_recommendation(i, data))
        return all_users


class CF_svd(CF_base):
    """
    Algorithm based on SVD content recommendation
    """

    def __init__(self, k=3, r=3):
        super(CF_svd, self).__init__(k)
        self.r = r
        self.uk = None
        self.vk = None
        return

    def init_param(self, data):
        # Initialization
        self.n_user = data.shape[0]
        self.n_item = data.shape[1]
        self.svd_simplify(data)
        print(self.n_user)
        print(self.n_item)
        return data

    def svd_simplify(self, data):
        u, s, v = np.linalg.svd(data)
        u, s, v = u[:, :self.r], s[:self.r], v[:self.r, :]
        sk = np.diag(np.sqrt(s))
        self.uk = u @ sk
        self.vk = sk @ v
        print(self.uk)
        print(self.vk)
        return

    def cal_prediction(self, user_ind, item_ind, user_row):
        rate_ave = np.mean(user_row)
        return rate_ave + self.uk[user_ind] @ self.vk[:, item_ind]

    def cal_recommendation(self, user_ind, data):
        item_prediction = defaultdict(float)
        user_row = data[user_ind]
        un_purchase_item_inds = np.where(user_row == 0)[0]
        for item_ind in un_purchase_item_inds:
            item_prediction[item_ind] = self.cal_prediction(user_ind, item_ind, user_row)
        res = sorted(item_prediction, key=item_prediction.get, reverse=True)
        return res[:self.k]


if __name__ == '__main__':
    # data = np.array([[4, 3, 0, 5, 0],
    #                  [4, 0, 4, 4, 0],
    #                  [4, 0, 5, 0, 3],
    #                  [2, 3, 0, 1, 0],
    #                  [0, 4, 2, 0, 5]])
    data = np.array(
                    [
                        [3.5, 1.0, 0.0, 0.0, 0.0, 0.0],
                     [2.5, 3.5, 3.0, 3.5, 2.5, 3.0],
                     [3.0, 3.5, 1.5, 5.0, 3.0, 3.5],
                     [2.5, 3.5, 0.0, 3.5, 4.0, 0.0],
                     [3.5, 2.0, 4.5, 0.0, 3.5, 2.0],
                     [3.0, 4.0, 2.0, 3.0, 3.0, 2.0],
                     [4.5, 1.5, 3.0, 5.0, 3.5, 0.0]

                     ])
    cf = CF_svd(k=1, r=3)
    """
    Content-based K-nearest neighbor recommendation algorithm
    """
    #cf = CF_knearest(k=5)
    print(cf.fit(data))

