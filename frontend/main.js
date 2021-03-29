const {app, BrowserWindow} = require('electron');

const url = require('url');
const path = require('path');
const axios = require('axios').default;

let mainWindow;

let subpy = require('child_process').spawn('./app');

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true
        }
    });

    mainWindow.setMenu(null);

    mainWindow.loadURL(
        url.format({
            pathname: path.join(__dirname, './dist/index.html'),
            protocol: 'file:',
            slashes: true
        })
    );

    mainWindow.on('closed', function () {
        mainWindow = null;
    });
}

app.on('ready', createWindow);

app.on('window-all-closed', function () {
    axios({
        method: 'GET',
        url: 'http://127.0.0.1:5000/stop/',
    });
    app.quit();
});

app.on('activate', function () {
    if (mainWindow === null) createWindow();
});
