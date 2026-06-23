const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  execute: (data) => ipcRenderer.invoke('execute', data),
  undo: (data) => ipcRenderer.invoke('undo', data),
  browseOutput: () => ipcRenderer.invoke('browse-output')
});
