const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  execute: (data) => ipcRenderer.invoke('execute', data),
  undo: (data) => ipcRenderer.invoke('undo', data),
  getTracks: () => ipcRenderer.invoke('getTracks'),
  getConfig: () => ipcRenderer.invoke('getConfig'),
  setConfig: (data) => ipcRenderer.invoke('setConfig', data),
  browseOutput: () => ipcRenderer.invoke('browse-output')
});
