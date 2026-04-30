const api = require('../../utils/request.js');

Page({
  data: {
    historyCount: 0,
    collectCount: 0,
    providers: ['火山引擎 (Ark)', '阿里云 (DashScope)'],
    providerIndex: 0,
    topK: 5,
    rerank: true
  },

  onShow() {
    this.updateStats();
    // 同步全局配置
    const app = getApp();
    const { settings } = app.globalData;
    this.setData({
      providerIndex: settings.provider === 'ark' ? 0 : 1,
      topK: settings.topK,
      rerank: settings.rerank
    });
  },

  updateStats() {
    const history = wx.getStorageSync('chat_history') || [];
    const collections = wx.getStorageSync('collections') || [];
    this.setData({
      historyCount: history.length,
      collectCount: collections.length
    });
  },

  onProviderChange(e) {
    const index = e.detail.value;
    const provider = index == 0 ? 'ark' : 'dashscope';
    this.setData({ providerIndex: index });
    const app = getApp();
    app.globalData.settings.provider = provider;
    wx.showToast({ title: '引擎已切换', icon: 'success' });
  },

  onTopKChange(e) {
    const val = e.detail.value;
    this.setData({ topK: val });
    const app = getApp();
    app.globalData.settings.topK = val;
  },

  onRerankChange(e) {
    const val = e.detail.value;
    this.setData({ rerank: val });
    const app = getApp();
    app.globalData.settings.rerank = val;
  },

  viewHistory() {
    wx.switchTab({ url: '/pages/qa/qa' });
  },

  viewCollections() {
    wx.switchTab({ url: '/pages/literature/literature' });
  },

  showHelp() {
    wx.showModal({
      title: '使用帮助',
      content: '1. 在问答页输入BMS相关问题\n2. 点击引用角标查看原文溯源\n3. 在设置中切换向量引擎和检索参数',
      showCancel: false
    });
  },

  rebuildIndex() {
    wx.showModal({
      title: '重建索引',
      content: '确定要重新扫描文献并建立向量索引吗？这可能需要几分钟。',
      success: (res) => {
        if (res.confirm) {
          wx.showLoading({ title: '索引重建中...' });
          api.post('/reindex')
            .then(() => {
              wx.showToast({ title: '索引重建成功' });
            })
            .finally(() => {
              wx.hideLoading();
            });
        }
      }
    });
  }
});
