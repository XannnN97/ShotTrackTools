// ShotTrackTools - Preload Script (compatible with contextIsolation)

const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('shottracktools', {
    launchPython: () => ipcRenderer.send('launch-python')
});
