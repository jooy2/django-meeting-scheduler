const movePage = function(href) {
    location.href = href;
};

function stringLimit(str, limit) {
    let tmpStr = str;
    let byte_count = 0;
    let len = str.length;
    let dot = "";

    for (let i=0; i<len; i++) {
        byte_count += chr_byte(str.charAt(i));

        if (byte_count === limit - 1) {
            if (chr_byte(str.charAt(i+1)) === 2) {
                tmpStr = str.substring(0, i+1);
                dot = "...";
            } else {
                if (i+2 !== len) dot = "...";
                tmpStr = str.substring(0, i+2);
            }
            break;
        } else if (byte_count === limit){
            if (i+1 !== len) dot = "...";
            tmpStr = str.substring(0, i+1);
            break;
      }
   }
   return tmpStr + dot;
}

function chr_byte(chr) {
   if (escape(chr).length > 4)
       return 2;
   else
       return 1;
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

let csrfToken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

const addCsrfToken = function(xhr) {
    xhr.setRequestHeader("X-CSRFToken", csrfToken);
};

const stringToJson = function(str) {
    return eval("(" + str + ")");
};