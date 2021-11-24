document.onkeydown = function(e) {
    if(e.code == "BrowserHome") {
        console.log("HomeKey");
        chrome.runtime.sendMessage({greeting: "hello"}, function(response) {
            console.log(response);
        });
        // what you want to on key press.
        e.preventDefault();
        console.log(e);
    }
};


chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
    console.log(sender.tab ?
                "from a content script:" + sender.tab.url :
                "from the extension");
    if (request.greeting === "hello")
        sendResponse(sender);
        chrome.windows.remove(sender.tab.windowId);
    }
);