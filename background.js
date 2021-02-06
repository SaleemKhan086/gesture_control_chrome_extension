chrome.extension.onMessage.addListener(

  function(message,sender,sendResponse){
    
    if(message.txt==="start")
    {
      //chrome.windows.update(chrome.windows.WINDOW_ID_CURRENT,{width:500,height:400});
      var request = new XMLHttpRequest();
      console.log("inside funtion");
      request.open("POST", "http://127.0.0.1:5000/");
      request.onreadystatechange = function() {
		      console.log(this.readyState);
    };

    const data={"t":1,
         "previous_tab":message.previous_tab,
         "next_tab":message.next_tab,
         "scroll_up":message.scroll_up,
         "scroll_down":message.scroll_down,
         "zoom_out":message.zoom_out,
         "zoom_in":message.zoom_in
    };

    request.setRequestHeader('Content-Type', 'application/json');
    request.send(JSON.stringify(data));
    }
    else{
      console.log("stopped.");
      var request = new XMLHttpRequest();
      request.open("POST", "http://127.0.0.1:5000/");
      const data={"t":0}
      request.setRequestHeader('Content-Type', 'application/json');
      request.send(JSON.stringify(data));
    }
  }
);

