const api = require('../../utils/request.js');

Page({
  data: {
    libList: [],
    filteredList: [],
    searchQuery: '',
    sortBy: 'date', // date or cite
    refreshing: false,
    showDetail: false,
    activeItem: null,
    isCollected: false
  },

  onLoad() {
    this.loadList();
  },

  onRefresh() {
    this.setData({ refreshing: true });
    this.loadList().finally(() => {
      this.setData({ refreshing: false });
    });
  },

  loadList() {
    // 模拟从后端获取文献列表
    // 实际应调用 api.get('/papers')
    return new Promise((resolve) => {
      setTimeout(() => {
        const mockData = [
          { id: 1, title: 'A Comprehensive Review of Cloud-Based Lithium-Ion Battery Management Systems', author: 'A. Author et al.', pages: 15, citeCount: 12 },
          { id: 2, title: 'Microcontroller-Driven Battery Management in Hybrid Energy Systems', author: 'B. Zhang', pages: 20, citeCount: 8 },
          { id: 3, title: '基于物理信息神经网络的锂离子电池荷电状态估计研究综述', author: '王顺利', pages: 12, citeCount: 25 },
          { id: 4, title: '基于电化学模型的锂离子电池荷电状态估计方法综述', author: '武龙星', pages: 18, citeCount: 19 }
        ];
        this.setData({
          libList: mockData,
          filteredList: mockData
        });
        resolve();
      }, 500);
    });
  },

  onSearch(e) {
    const query = e.detail.value.toLowerCase();
    const filtered = this.data.libList.filter(item => 
      item.title.toLowerCase().includes(query) || 
      (item.author && item.author.toLowerCase().includes(query))
    );
    this.setData({
      searchQuery: query,
      filteredList: filtered
    });
  },

  toggleSort() {
    const newSort = this.data.sortBy === 'date' ? 'cite' : 'date';
    const list = [...this.data.filteredList];
    if (newSort === 'cite') {
      list.sort((a, b) => b.citeCount - a.citeCount);
    } else {
      list.sort((a, b) => b.id - a.id);
    }
    this.setData({
      sortBy: newSort,
      filteredList: list
    });
  },

  viewDetail(e) {
    const item = e.currentTarget.dataset.item;
    this.setData({
      activeItem: item,
      showDetail: true,
      isCollected: wx.getStorageSync('collections')?.includes(item.id) || false
    });
  },

  closeDetail() {
    this.setData({ showDetail: false });
  },

  stopBubble() {},

  toggleCollect() {
    const collections = wx.getStorageSync('collections') || [];
    const id = this.data.activeItem.id;
    let newCollections;
    
    if (this.data.isCollected) {
      newCollections = collections.filter(cid => cid !== id);
      wx.showToast({ title: '已取消收藏', icon: 'none' });
    } else {
      newCollections = [...collections, id];
      wx.showToast({ title: '已加入收藏', icon: 'success' });
    }
    
    wx.setStorageSync('collections', newCollections);
    this.setData({ isCollected: !this.data.isCollected });
  },

  onShareAppMessage() {
    return {
      title: this.data.activeItem ? `推荐文献：${this.data.activeItem.title}` : 'BMS 智能问答文献库',
      path: '/pages/literature/literature'
    };
  }
});
