/* Cupertino2 - table filters. Progressive enhancement only; the site works without it. */
(function(){
  document.querySelectorAll('.tablewrap').forEach(function(wrap){
    var tbl = wrap.querySelector('table.data');
    if(!tbl || tbl.tBodies[0].rows.length < 8) return;
    var cap = wrap.querySelector('.tablecap');
    var box = document.createElement('input');
    box.type='search';
    box.className='flt';
    box.placeholder='Filter rows…';
    if(cap){ cap.appendChild(box); } else {
      var d=document.createElement('div'); d.className='tablecap'; d.appendChild(box);
      wrap.insertBefore(d, wrap.firstChild);
    }
    box.addEventListener('input', function(){
      var q = box.value.toLowerCase();
      Array.prototype.forEach.call(tbl.tBodies[0].rows, function(tr){
        tr.style.display = tr.textContent.toLowerCase().indexOf(q) === -1 ? 'none' : '';
      });
    });
  });
  var s=document.createElement('style');
  s.textContent='.flt{margin-left:10px;font:inherit;font-size:12.5px;padding:3px 8px;'+
                'border:1px solid #d7dde5;border-radius:6px;min-width:150px}';
  document.head.appendChild(s);
})();
