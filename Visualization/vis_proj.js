
var CHAR_SET = ['бп', 'вф', 'эеё', 'сз', 'ня', 'дт',
                'хг', 'шщ', 'ъьы', 'ий', 'оа', 'ую',
                'цч', 'млр', 'жк', '.,!?']

function draw_charset(pos, good) {

  var checker = document.getElementById("checker");
  out = "<table border=1 align='center'> <tr align='center' height='50'>"
  for (var i = 0; i < CHAR_SET.length; ++i) {
    if (pos == i) {
      if (good) {
        clas = "good";
      } else {
        clas = "bad";
      }
      out += "<td width='50' class='" + clas + "'>" + CHAR_SET[i] + "</td>";
    } else {
      out += "<td width='50'>" + CHAR_SET[i] + "</td>";
    }

  }
  out += "</tr></table>";
  checker.innerHTML = out;
}

function to_binary(number) {
  res = ""
  while (number > 0) {
    res += number % 2;
    number = Math.floor(number / 2);
  }
  return res;
}

function draw_hashnumber(number) {

  var checker = document.getElementById("hashnumber");

  out = "<table border=1 align='center'> <tr align='center' height='50'>"
  b_number = to_binary(number);
  for (var i = 0; i < CHAR_SET.length; ++i) {
      if (!b_number[i]) {
        out += "<td width='50'>" + 0 + "</td>";

      } else {
        out += "<td width='50'>" + b_number[i] + "</td>";
      }

  }
  out += "</tr></table> <br>" + number;
  checker.innerHTML = out;
}


function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function _symb_category(ch) {
    for (var i = 0; i < CHAR_SET.length; ++i) {
        if (CHAR_SET[i].indexOf(ch) != -1) {
            return i;
        }
    }
    return CHAR_SET.length;
}

function sig_hash(str_to_hash) {
    var n = 0;
    for (var i = 0; i < str_to_hash.length; ++i) {
        var j = _symb_category(str_to_hash[i]);
        n |= 1 << i;
    }
    return n;
}

function _mistakes(numb) {
    var all_mistakes = [];
    for (var i = 0; i <= CHAR_SET.length; ++i) {
        if (numb & (1 << i)) {
            var mist_numb = numb - (1 << i);
        } else {
            var mist_numb = numb + (1 << i);
        }
        all_mistakes.push(mist_numb);
    }
    return all_mistakes;
}

function sig_hash_with_mistakes(str_to_hash) {
    answer = sig_hash(str_to_hash);
    Array.prototype.push.apply(answer, _mistakes(answer[0]));
    return answer;
}

async function hash() {
    var inp = document.getElementById("text1");
    var hashword = document.getElementById("hashword");
    var out = document.getElementById("hashword");
    hashword.innerHTML = inp.value;
    draw_charset();

    n = 0;
    draw_hashnumber(n);
    for (var i = 0; i < inp.value.length; ++i) {
      hashword.innerHTML = "";
      for (var j = 0; j < inp.value.length; ++j) {
        if (i == j) {
          hashword.innerHTML += "<span class='letter'>" + inp.value[j] + "</span>";
        } else {
          hashword.innerHTML += inp.value[j];
        }
      }
      console.log(123);
      var cat = _symb_category(inp.value[i]);
      n |= 1 << cat;
      for (var j = 0; j <= cat && j < CHAR_SET.length; ++j) {
        var good = (cat == j);
        draw_charset(j, good);
        await sleep(document.getElementById("speed").value);
      }
      await sleep(document.getElementById("speed").value * 2);
      draw_hashnumber(n);
      await sleep(document.getElementById("speed").value * 2);
    }


}
