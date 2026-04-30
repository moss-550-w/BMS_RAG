const api = require('../../utils/request.js');

Page({
  data: {
    docs: [],
    loading: false,
    searchQuery: '',
    total: 0
  },

  onLoad() {
    this.fetchDocs();
  },

  onPullDownRefresh() {
    this.fetchDocs();
  },

  onSearchInput(e) {
    this.setData({ searchQuery: e.detail.value });
  },

  onSearch() {
    this.fetchDocs();
  },

  fetchDocs() {
    this.setData({ loading: true });
    // 后端接口：/documents?query=xxx
    api.get('/documents', { query: this.data.searchQuery })
      .then(res => {
        this.setData({
          docs: res.documents || [],
          total: (res.documents || []).length,
          loading: false
        });
        wx.stopPullDownRefresh();
      })
      .catch(() => {
        this.setData({ loading: false });
        wx.stopPullDownRefresh();
      });
  },

  viewDoc(e) {
    const doc = e.currentTarget.dataset.doc;
    wx.showActionSheet({
      itemList: ['查看详情', '复制标题', '收藏文献'],
      success: (res) => {
        if (res.tapIndex === 0) {
          wx.showModal({
            title: doc.name,
            content: `格式: ${doc.type}\n大小: ${doc.size}\n更新时间: ${doc.mtime}\n\n该功能正在开发中，后续支持PDF预览。`,
            showCancel: false
          });
        } else if (res.tapIndex === 1) {
          wx.setClipboardData({ data: doc.name });
        } else if (res.tapIndex === 2) {
          const collections = wx.getStorageSync('collections') || [];
          if (!collections.find(c => c.name === doc.name)) {
            collections.push(doc);
            wx.setStorageSync('collections', collections);
            wx.showToast({ title: '已收藏' });
          } else {
            wx.showToast({ title: '已在收藏夹', icon: 'none' });
          }
        }
      }
    });
  }
});
