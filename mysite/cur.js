function gI(e){return document.getElementById(e)}
var left = dgI("leftSelector");
var strUser = left.options[left.selectedIndex].value;
var right = dgI("rightSelector");
var strUser = right.options[right.selectedIndex].value;
var amount = dgI("amount").value;
var xhr = new XMLHttpRequest();
xhr.open('GET', 'site. com/'+left+'/'+right+'/'amount);
xhr.onload = function() {
if (xhr.status === 200)
dgI('result').innerText=xhr.responseText;
else
dgI('result').innerText='Request failed. Returned status of ' + xhr.status;
};
xhr.send();
