/**
 * 封装微信小程序网络请求
 */
const request = (url, method, data = {}) => {
  return new Promise((resolve, reject) => {
    // 动态获取 app 实例，避免生命周期顺序问题
    const app = getApp();
    const baseUrl = (app && app.globalData && app.globalData.baseUrl) || 'http://127.0.0.1:8001/api/v1';
    
    wx.request({
      url: `${baseUrl}${url}`,
      method: method,
      data: data,
      header: {
        'Content-Type': 'application/json'
      },
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data);
        } else {
          wx.showToast({
            title: `请求失败: ${res.statusCode}`,
            icon: 'none'
          });
          reject(res);
        }
      },
      fail: (err) => {
        wx.showToast({
          title: '网络连接异常',
          icon: 'none'
        });
        reject(err);
      }
    });
  });
};

module.exports = {
  get: (url, data) => request(url, 'GET', data),
  post: (url, data) => request(url, 'POST', data),
  put: (url, data) => request(url, 'PUT', data),
  delete: (url, data) => request(url, 'DELETE', data)
};
