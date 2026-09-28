/* Creatium: та же таблица HaiboProducts, все поля, лимит 50; настройка combo_discount по умолчанию 0. */
(function () {
  var root = el.querySelector('#hb-combo');
  if (!root) return;
  var rows = typeof data !== 'undefined' && data && Array.isArray(data.rows) ? data.rows.filter(function(r){return String(r.active)==='1';}) : [];
  var motor = root.querySelector('[data-combo="motor"]');
  var battery = root.querySelector('[data-combo="battery"]');
  var accessory = root.querySelector('[data-combo="accessory"]');
  var total = root.querySelector('[data-combo="total"]');
  var note = root.querySelector('[data-combo="note"]');
  function txt(v){return v==null?'':String(v).trim();}
  function n(v){var x=Number(txt(v).replace(/\s/g,'').replace(',','.'));return isFinite(x)?x:0;}
  function money(v){return new Intl.NumberFormat('ru-RU').format(v)+' ₽';}
  function split(v){return txt(v).split('|').map(function(x){return x.trim();});}
  function addOption(select,row){var o=document.createElement('option');o.value=txt(row.id);o.textContent=txt(row.title)+' — '+money(n(row.price));select.appendChild(o);}
  function none(select,label){var o=document.createElement('option');o.value='';o.textContent=label;select.appendChild(o);}
  function find(id){return rows.find(function(r){return txt(r.id)===id;});}
  function group(r){
    if(txt(r.combo_group))return txt(r.combo_group);
    if(txt(r.product_type)==='motor')return 'motor';
    if(['A-BAT-12-100','A-BAT-24-100'].indexOf(txt(r.id))>=0)return 'battery';
    if(['A-QR-STANDARD','A-BOW-PVC','A-QR-HD-P002-P003'].indexOf(txt(r.id))>=0)return 'mount';
    if(txt(r.id)==='A-FUSE-60A')return 'protection';
    return 'other';
  }
  function selectable(r){return txt(r.show_in_combo)==='1'||(!txt(r.show_in_combo)&&group(r)!=='other');}
  function compatible(r,m){var series=txt(m.series),voltage=txt(m.voltage_v),keys=split(r.compatibility_filter),vs=split(r.compatible_voltage);return (keys.indexOf(series)>=0||keys.indexOf('Universal')>=0||keys.indexOf('HAIBO')>=0) && (!vs[0]||vs.indexOf(voltage)>=0);}
  function fillExtras(){
    var m=find(motor.value);battery.innerHTML='';accessory.innerHTML='';none(battery,'Без аккумулятора — 0 ₽');none(accessory,'Без аксессуара — 0 ₽');
    if(!m){total.textContent='—';note.textContent='Подключите таблицу HaiboProducts.';return;}
    rows.filter(function(r){return group(r)==='battery'&&selectable(r)&&compatible(r,m);}).forEach(function(r){addOption(battery,r);});
    rows.filter(function(r){return (group(r)==='mount'||group(r)==='protection')&&selectable(r)&&compatible(r,m);}).forEach(function(r){addOption(accessory,r);});
    if(battery.options.length>1)battery.selectedIndex=1;
    calculate();
  }
  function calculate(){
    var m=find(motor.value),b=find(battery.value),a=find(accessory.value);
    if(!m)return;
    var sum=n(m.price)+(b?n(b.price):0)+(a?n(a.price):0);
    var discount=typeof params!=='undefined'&&params?Math.min(100,Math.max(0,n(params.combo_discount))):0;
    total.textContent=money(Math.round(sum*(1-discount/100)));
    var missing=txt(m.voltage_v)==='36'&&battery.options.length===1;
    note.textContent=(discount?'Учтена скидка '+discount+'%. ':'')+(missing?'Аккумулятора 36 В в текущем каталоге нет. ':'')+'Сверьте состав и наличие с менеджером перед заказом.';
  }
  rows.filter(function(r){return group(r)==='motor'&&selectable(r);}).sort(function(a,b){return n(a.sort_order)-n(b.sort_order);}).forEach(function(r){addOption(motor,r);});
  motor.addEventListener('change',fillExtras);battery.addEventListener('change',calculate);accessory.addEventListener('change',calculate);
  fillExtras();
})();
