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