App({
  onLaunch() {
    // 展示本地存储能力
    const logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)

    // 获取系统信息
    wx.getSystemInfo({
      success: (res) => {
        this.globalData.systemInfo = res
      }
    })
  },
  globalData: {
    userInfo: null,
    systemInfo: null,
    // 后端 API 地址，建议根据实际环境修改
    // 注意：小程序正式上线需使用 HTTPS 且在后台配置域名
    // baseUrl: 'http://127.0.0.1:8001/api/v1', 
    baseUrl: 'http://10.90.178.212:8001/api/v1',
    settings: {
      topK: 5,
      provider: 'dashscope',
      rerank: true
    }
  }
})
