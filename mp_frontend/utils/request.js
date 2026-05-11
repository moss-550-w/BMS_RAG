/**
 * 封装微信小程序网络请求
 */
const getBaseUrl = () => {
  const app = getApp();
  return (app && app.globalData && app.globalData.baseUrl) || 'http://10.90.178.212:8001/api/v1';
};

const request = (url, method, data = {}, options = {}) => {
  return new Promise((resolve, reject) => {
    const baseUrl = getBaseUrl();
    const fullUrl = `${baseUrl}${url}`;
    const timeout = options.timeout || 15000;
    
    wx.request({
      url: fullUrl,
      method: method,
      data: data,
      timeout,
      header: {
        'Content-Type': 'application/json'
      },
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data);
        } else {
          const detail =
            (res.data && (res.data.detail || res.data.message)) ||
            `请求失败: ${res.statusCode}`;
          wx.showToast({
            title: String(detail).slice(0, 20),
            icon: 'none'
          });
          reject({
            type: 'http',
            message: String(detail),
            statusCode: res.statusCode,
            url: fullUrl,
            raw: res
          });
        }
      },
      fail: (err) => {
        const errMsg = err && err.errMsg ? err.errMsg : '网络连接异常';
        let friendly = errMsg;

        if (errMsg.includes('timeout')) {
          friendly = '请求超时，请检查后端响应';
        } else if (errMsg.includes('fail')) {
          friendly = `请求失败: ${errMsg}`;
        }

        wx.showToast({
          title: friendly.slice(0, 20),
          icon: 'none'
        });
        reject({
          type: 'network',
          message: friendly,
          errMsg,
          url: fullUrl,
          raw: err
        });
      }
    });
  });
};

module.exports = {
  getBaseUrl,
  get: (url, data, options) => request(url, 'GET', data, options),
  post: (url, data, options) => request(url, 'POST', data, options),
  put: (url, data, options) => request(url, 'PUT', data, options),
  delete: (url, data, options) => request(url, 'DELETE', data, options)
};
