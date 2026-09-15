const $=s=>document.querySelector(s);
const ALL_MENUS=["Dashboard","Penjualan","Pembelian","Kas & Bank","Buku Besar","Persediaan","Aset Tetap","Budgeting","Laporan","Master","HRD","AI & Integrasi"];
let MENUS=ALL_MENUS;
let COA=[],WH=[],ITEMS=[],CUST=[],VEND=[],SP=[],BR=[],TAX=[],cur="Dashboard",ME=null;
let curSub="",curDetail=null,curDetailId=null,searchQ="";
const MASTER_SUBS={"Keuangan":["Chart of Accounts","Pajak"],"Pelanggan":["Daftar Pelanggan"],"Vendor":["Daftar Vendor"],"Persediaan":["Daftar Barang","Gudang"],"Sales":["Salesman"],"Organisasi":["Cabang","Karyawan"],"Sistem":["User & Peran","Backup & Restore","Log Aktivitas"]};
const MASTER_SUB_ICONS={"Keuangan":"💰","Pelanggan":"👥","Vendor":"🏭","Persediaan":"📦","Sales":"👨‍💼","Organisasi":"🏢","Sistem":"⚙️"};
const SUB_ICONS={"Chart of Accounts":"📒","Pajak":"🏷️","Daftar Pelanggan":"👥","Daftar Vendor":"🏭","Daftar Barang":"📦","Gudang":"🏪","Salesman":"👨‍💼","Cabang":"🏢","Karyawan":"👤","User & Peran":"🔐","Backup & Restore":"💾","Log Aktivitas":"📋"};
const fmt=n=>"Rp "+Number(Math.round(n||0)).toLocaleString("id-ID");
const esc=s=>String(s??"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;").replace(/'/g,"&#39;");
const today=()=>new Date().toISOString().slice(0,10);
const tok=()=>localStorage.getItem("tok")||"";
const MENU_ICONS={"Dashboard":"📈","Penjualan":"🛒","Pembelian":"📦","Kas & Bank":"💰","Buku Besar":"📒","Persediaan":"🏪","Aset Tetap":"🏢","Budgeting":"💰","Laporan":"📊","Master":"⚙️","HRD":"👥","AI & Integrasi":"🤖"};
async function api(p,o){const r=await fetch(p,{headers:{"Content-Type":"application/json","Authorization":"Bearer "+tok()},...o});
 if(r.status===401){logout();throw new Error("Sesi habis, silakan login lagi");}
 const j=await r.json();if(!r.ok)throw new Error(j.error||"Error");return j;}
async function loadM(){try{[COA,WH,ITEMS,CUST,VEND,SP,BR,TAX]=await Promise.all(["/api/coa","/api/warehouses","/api/items","/api/customers","/api/vendors","/api/salespersons","/api/branches","/api/taxes"].map(u=>api(u).catch(()=>[])));}catch(e){console.error("Gagal muat master:",e);throw new Error("Gagal muat data master: "+e.message+" — cek koneksi / login ulang");}drawNav();}
function taxSel(id,val){const opts=(TAX.length?TAX:[{id:"",rate:11,tax_name:"PPN 11%"},{rate:0,tax_name:"Non-PPN"}]);return `<select id="${id}">${opts.map(t=>`<option value="${t.rate}"${Number(val??11)===Number(t.rate)?" selected":""}>${esc(t.tax_name||("Pajak "+t.rate+"%"))}</option>`).join("")}</select>`;}
window.quickCust=async()=>{const n=prompt("Nama pelanggan baru:");if(!n)return;try{await api("/api/customers",{method:"POST",body:JSON.stringify({customer_name:n})});await loadM();render();alert("Pelanggan ditambah");}catch(e){alert(e.message)}};
window.quickVend=async()=>{const n=prompt("Nama pemasok baru:");if(!n)return;try{await api("/api/vendors",{method:"POST",body:JSON.stringify({vendor_name:n})});await loadM();render();alert("Pemasok ditambah");}catch(e){alert(e.message)}};
function bankSel(v){return `<select id="${v}">${COA.filter(c=>c.account_code.startsWith("110")).map(c=>`<option value="${c.id}">${c.account_code} — ${c.account_name}</option>`).join("")}</select>`;}
function logout(){localStorage.removeItem("tok");ME=null;location.reload();}
window.chPass=async()=>{const o=prompt("Password lama:");if(!o)return;const n=prompt("Password baru (min 6 karakter):");if(!n)return;
 try{await api("/api/change-password",{method:"POST",body:JSON.stringify({old:o,new:n})});alert("Password diganti");}catch(e){alert(e.message)}};
async function boot(){
 // Canvas roundRect polyfill
 if(!CanvasRenderingContext2D.prototype.roundRect){
  CanvasRenderingContext2D.prototype.roundRect=function(x,y,w,h,r){
   r=Math.min(r||0,w/2,h/2);
   this.moveTo(x+r,y);this.arcTo(x+w,y,x+w,y+h,r);this.arcTo(x+w,y+h,x,y+h,r);this.arcTo(x,y+h,x,y,r);this.arcTo(x,y,x+w,y,r);this.closePath();
  };
 }
 if(!tok())return loginScreen();
 // Dark mode toggle
 const savedTheme=localStorage.getItem("erp-theme")||"light";
 document.documentElement.setAttribute("data-theme",savedTheme);

 const themeBtn=document.createElement("button");
 themeBtn.className="theme-toggle";
 themeBtn.innerHTML=savedTheme==="dark"?"☀️":"🌙";
 themeBtn.onclick=()=>{
  const current=document.documentElement.getAttribute("data-theme");
  const next=current==="dark"?"light":"dark";
  document.documentElement.setAttribute("data-theme",next);
  localStorage.setItem("erp-theme",next);
  themeBtn.innerHTML=next==="dark"?"☀️":"🌙";
  showToast(next==="dark"?"Mode Gelap":"Mode Terang","Tema telah diubah","success");
 };
 document.body.appendChild(themeBtn);

 // Keyboard shortcuts
 const shortcuts={
  "d":()=>window.location.hash="#dashboard",
  "p":()=>{cur="Penjualan";render();},
  "b":()=>{cur="Pembelian";render();},
  "k":()=>{cur="Kas & Bank";render();},
  "l":()=>{cur="Laporan";render();},
  "m":()=>{cur="Master";render();},
  "Escape":()=>{curDetail=null;render();},
  "?":()=>toggleShortcuts()
 };

 function toggleShortcuts(){
  const hint=document.querySelector(".shortcut-hint");
  if(hint){hint.classList.toggle("show");}
  else{
   const div=document.createElement("div");
   div.className="shortcut-hint show";
   div.innerHTML=`<h4>⌨️ Keyboard Shortcuts</h4>
   <table>
    <tr><td><span class="kbd">D</span></td><td>Dashboard</td></tr>
    <tr><td><span class="kbd">P</span></td><td>Penjualan</td></tr>
    <tr><td><span class="kbd">B</span></td><td>Pembelian</td></tr>
    <tr><td><span class="kbd">K</span></td><td>Kas & Bank</td></tr>
    <tr><td><span class="kbd">L</span></td><td>Laporan</td></tr>
    <tr><td><span class="kbd">M</span></td><td>Master</td></tr>
    <tr><td><span class="kbd">ESC</span></td><td>Kembali</td></tr>
    <tr><td><span class="kbd">?</span></td><td>Tampilkan/Sembunyikan</td></tr>
   </table>`;
   document.body.appendChild(div);
  }
 }

 document.addEventListener("keydown",(e)=>{
  if(e.target.tagName==="INPUT"||e.target.tagName==="TEXTAREA"||e.target.tagName==="SELECT")return;
  if(shortcuts[e.key]){shortcuts[e.key]();}
 });

 try{ME=await api("/api/me");}
 catch(e){return loginScreen();}
 const R=ME.role;
 MENUS = R==="KASIR" ? ["Dashboard","Penjualan","Pembelian","Kas & Bank","Persediaan"]
  : R==="GUDANG" ? ["Dashboard","Persediaan","Pembelian"]
   : R==="HRD" ? ["Dashboard","Master","HRD"]
  : R==="FINANCE" ? ALL_MENUS.filter(m=>m!=="Master")
  : ALL_MENUS;
 if(!MENUS.includes(cur))cur="Dashboard";
 $("#nav").innerHTML+=`<div class="mut">${esc(ME.full_name)} (${esc(ME.role)})</div><button onclick="logout()">Keluar</button><button onclick="chPass()">Ganti password</button>`;
 loadM().then(render).catch(e=>{$("#app").innerHTML=`<div class="card">❌ ${esc(e.message)}</div>`;});
}
function loginScreen(){
 const main=$("main");main.innerHTML="";
 document.body.style.background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)";
 main.innerHTML=`<div class="login-wrap"><div class="login-card">
 <span class="logo-icon">📊</span>
 <h3>ERP-MSP</h3>
 <p class="tagline">Enterprise Resource Planning - Micro Small Business</p>
 <input id="l_u" placeholder="Username" value="admin">
 <input id="l_p" type="password" placeholder="Password" value="admin123">
 <button class="go" onclick="doLogin()">Masuk</button>
 <div class="hints">
 <p><b>Demo:</b> admin / admin123</p>
 <p>manager / manager123</p>
 <p>kasir / kasir123</p>
 </div>
 <div id="l_err"></div></div></div>`;
}
window.doLogin=async()=>{try{const r=await (await fetch("/api/login",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({username:$("#l_u").value,password:$("#l_p").value})})).json();
 if(!r.ok&&!r.token)throw new Error(r.error||"Gagal");localStorage.setItem("tok",r.token);
 if(r.must_change_password){alert("Demi keamanan: password default masih dipakai. Wajib ganti password sekarang.");location.reload();setTimeout(()=>{if(window.chPass)window.chPass();},800);return;}
 location.reload();}catch(e){$("#l_err").textContent=e.message;}};
function drawNav(){
 const nav=$("#nav");
 let menuHtml=MENUS.map(m=>{
  if(m==="Master"&&cur==="Master"){
   let subHtml=Object.keys(MASTER_SUBS).map(k=>`<button class="sub-btn${curSub===k?' active':''}" onclick="goMaster('${k}')"><span class="nav-icon">${MASTER_SUB_ICONS[k]||"📄"}</span>${k}</button>`).join("");
   return `<button class="${m===cur?'active':''}" onclick="go('${m}')"><span class="nav-icon">${MENU_ICONS[m]||"📄"}</span>${m}</button><div class="sub-nav">${subHtml}</div>`;
  }
  return `<button class="${m===cur?'active':''}" onclick="go('${m}')"><span class="nav-icon">${MENU_ICONS[m]||"📄"}</span>${m}</button>`;
 }).join("");
 const userSection=ME?`<div class="user-info"><div class="user-avatar">${(ME.full_name||"U").charAt(0).toUpperCase()}</div><div class="user-details"><div class="user-name">${esc(ME.full_name)}</div><div class="user-role">${esc(ME.role)}</div></div></div><button onclick="chPass()" title="Ganti Password"><span class="nav-icon">🔑</span>Ganti Password</button><button onclick="logout()" title="Keluar"><span class="nav-icon">🚪</span>Keluar</button>`:"";
 nav.innerHTML=`<div class="nav-section">Menu</div>${menuHtml}${userSection}`;
}
function go(m){cur=m;curSub="";curDetail=null;curDetailId=null;searchQ="";$("#title").textContent=m;drawNav();render();}
window.goMaster=sub=>{curSub=sub;curDetail=null;curDetailId=null;searchQ="";$("#title").textContent="Master — "+sub;drawNav();render();};
window.loadSistem=sub=>{
 if(sub==='currency'){
  const A=$("#app");
  const currData=currencies;
  A.innerHTML=`<div class="card"><h3><span class="card-icon">💱</span>Konfigurasi Mata Uang</h3>
   <table><thead><tr><th>Kode</th><th>Nama</th><th>Simbol</th><th>Kurs (vs IDR)</th></tr></thead>
   <tbody>${currData.map(c=>`<tr><td><b>${c.code}</b></td><td>${c.name}</td><td>${c.symbol}</td><td><input type="number" value="${c.rate}" min="1" style="width:120px" id="rate_${c.code}" onchange="updateCurrRate('${c.code}',this.value)"></td></tr>`).join("")}</tbody></table>
   <p style="margin-top:16px;color:var(--sub)">Kurs ini digunakan untuk konversi mata uang dalam transaksi internasional</p></div>`;
 }
};
window.goDetail=(type,id)=>{curDetail=type;curDetailId=id;render();};
window.goBack=()=>{curDetail=null;curDetailId=null;render();};
function searchBar(placeholder,onsrch){return `<div class="search-bar"><input type="text" id="search_input" placeholder="${placeholder}" value="${esc(searchQ)}" oninput="searchQ=this.value" onkeyup="if(event.key==='Enter'){${onsrch}}"><button class="go info" onclick="${onsrch}">Cari</button></div>`;}
function filterRows(rows,q){if(!q)return rows;const lq=q.toLowerCase();return rows.filter(r=>JSON.stringify(r).toLowerCase().includes(lq));}
function validateForm(fields){
 for(const f of fields){
  const el=$("#"+f.id);
  if(!el){continue;}
  if(f.required&&!el.value.trim()){
   el.style.borderColor="var(--bad)";
   el.focus();
   alert(f.label+" wajib diisi!");
   return false;
  }
  if(f.type==="number"&&(isNaN(+el.value)||+el.value<0)){
   el.style.borderColor="var(--bad)";
   el.focus();
   alert(f.label+" harus angka positif!");
   return false;
  }
  el.style.borderColor="";
 }
 return true;
}
function showLoading(btn,text){
 if(typeof btn==="string")btn=$(btn);
 if(!btn)return;
 btn._oldHtml=btn.innerHTML;
 btn.innerHTML=`<span class="spinner"></span> ${text||"Memproses..."}`;
 btn.disabled=true;
}
function hideLoading(btn){
 if(typeof btn==="string")btn=$(btn);
 if(!btn)return;
 btn.innerHTML=btn._oldHtml||"Simpan";
 btn.disabled=false;
}
// Toast notification
function showToast(title,message,type="info"){
 const toast=document.createElement("div");
 toast.className=`toast ${type}`;
 toast.innerHTML=`<div class="title">${esc(title)}</div><div class="message">${esc(message)}</div>`;
 document.body.appendChild(toast);
 setTimeout(()=>toast.remove(),4000);
}
function coaSel(v){return `<select id="${v}">${COA.map(c=>`<option value="${c.id}">${c.account_code} — ${c.account_name}</option>`).join("")}</select>`;}
function st(x){return `<span class="bdg b-${x}">${x}</span>`;}

const currencies=[
 {code:"IDR",name:"Rupiah Indonesia",symbol:"Rp",rate:1},
 {code:"USD",name:"US Dollar",symbol:"$",rate:15800},
 {code:"EUR",name:"Euro",symbol:"€",rate:17200},
 {code:"SGD",name:"Singapore Dollar",symbol:"S$",rate:11800},
 {code:"MYR",name:"Malaysian Ringgit",symbol:"RM",rate:3500},
 {code:"JPY",name:"Japanese Yen",symbol:"¥",rate:105},
 {code:"AUD",name:"Australian Dollar",symbol:"A$",rate:10400},
 {code:"GBP",name:"British Pound",symbol:"£",rate:20000}
];
function getCurrency(code){return currencies.find(c=>c.code===code)||currencies[0];}
function convertCurrency(amount,fromCode,toCode){
 const from=getCurrency(fromCode);
 const to=getCurrency(toCode);
 if(from.code===to.code)return amount;
 return Math.round(amount*from.rate/to.rate);
}
function formatCurrency(amount,code){
 const c=getCurrency(code);
 if(c.code==="IDR")return"Rp"+amount.toLocaleString("id-ID");
 return c.symbol+" "+amount.toLocaleString("en-US",{minimumFractionDigits:2,maximumFractionDigits:2});
}
function currSelectHTML(id,defaultCode){
 return `<select id="${id}">${currencies.map(c=>`<option value="${c.code}" ${c.code===defaultCode?"selected":""}>${c.code} - ${c.name}</option>`).join("")}</select>`;
}
window.updateCurrRate=async(code,rate)=>{
 rate=+rate;
 if(isNaN(rate)||rate<=0)return alert("Kurs harus positif");
 const c=currencies.find(x=>x.code===code);
 if(c){c.rate=rate;alert(code+" kurs diperbarui: "+rate);}
};
let GRIDS={};
function gridHTML(gid){return `<table class="grid-table"><thead><tr><th>No</th><th>Barang</th><th>Deskripsi</th>${GRIDS[gid].cfg.wh?"<th>Gudang</th>":""}<th>Satuan</th><th>Qty</th><th>Harga</th>${GRIDS[gid].cfg.disc?"<th>D1%</th><th>D2%</th>":""}<th>Total</th><th></th></tr></thead><tbody id="${gid}_body"></tbody></table><button class="go" onclick="gridAdd('${gid}')">+ Tambah baris</button><div class="grid-sub">Subtotal:&nbsp;<b id="${gid}_sub">Rp 0</b></div>`;}
function gridStart(gid,cfg){GRIDS[gid]={rows:[],cfg};const w=document.createElement("div");w.innerHTML=gridHTML(gid);const host=$("#"+gid+"_wrap");host.innerHTML="";host.appendChild(w);gridAdd(gid);}
function gridAdd(gid,pref){
 const G=GRIDS[gid];if(!G||!ITEMS.length)return;
 const r=Object.assign({item_id:ITEMS[0].id,wh:WH.length?WH[0].id:null,qty:1,price:0,d1:0,d2:0,unit:null,lt:0,desc:""},pref||{});
 const it=ITEMS.find(i=>i.id==r.item_id)||ITEMS[0];
 if(!r.price)r.price=G.cfg.type==="sale"?(it.sales_price||0):(it.purchase_price||0);
 if(!r.unit){const u=((it&&it.units)||[{unit_code:it.base_unit,conversion:1}])[0];r.unit=u.unit_code+"|"+u.conversion;}
 G.rows.push(r);gridDraw(gid);
}
function gridDraw(gid){
 const G=GRIDS[gid];const tb=$("#"+gid+"_body");if(!tb)return;
 if(!ITEMS.length){tb.innerHTML=`<tr><td colspan="9">Belum ada barang — tambah di Master → Barang.</td></tr>`;return;}
 tb.innerHTML=G.rows.map((r,i)=>{
  const it=ITEMS.find(x=>x.id==r.item_id)||ITEMS[0];
  const us=((it&&it.units)||[{unit_code:it.base_unit,conversion:1}]);
  return `<tr><td>${i+1}</td><td><select id="${gid}_it_${i}" onchange="gridItem('${gid}',${i})">${ITEMS.map(x=>`<option value="${x.id}"${x.id==r.item_id?" selected":""}>${esc(x.item_code)}</option>`).join("")}</select></td><td><input id="${gid}_ds_${i}" value="${esc(r.desc||"")}" placeholder="ket..." oninput="gridUpd('${gid}',${i})"></td>`
  +(G.cfg.wh?`<td><select id="${gid}_wh_${i}" onchange="gridUpd('${gid}',${i})">${WH.map(w=>`<option value="${w.id}"${w.id==r.wh?" selected":""}>${esc(w.warehouse_name)}</option>`).join("")}</select></td>`:"")
  +`<td><select id="${gid}_un_${i}" onchange="gridUpd('${gid}',${i})">${us.map(u=>`<option value="${esc(u.unit_code)}|${u.conversion}"${String(r.unit||"").split("|")[0]===u.unit_code?" selected":""}>${esc(u.unit_code)}</option>`).join("")}</select></td>`
  +`<td><input class="num" id="${gid}_q_${i}" type="number" min="0" step="any" value="${r.qty}" oninput="gridUpd('${gid}',${i})"></td>`
  +`<td><input class="num" id="${gid}_p_${i}" type="number" min="0" step="any" value="${r.price}" oninput="gridUpd('${gid}',${i})"></td>`
  +(G.cfg.disc?`<td><input class="num" id="${gid}_a_${i}" type="number" min="0" step="any" value="${r.d1}" oninput="gridUpd('${gid}',${i})"></td><td><input class="num" id="${gid}_b_${i}" type="number" min="0" step="any" value="${r.d2}" oninput="gridUpd('${gid}',${i})"></td>`:"")
  +`<td style="text-align:right" id="${gid}_t_${i}"></td><td><button class="row-del" onclick="gridDel('${gid}',${i})" title="Hapus baris">×</button></td></tr>`;
 }).join("");
 G.rows.forEach((r,i)=>gridUpd(gid,i));
}
function gridItem(gid,i){
 const G=GRIDS[gid];const r=G.rows[i];if(!r)return;
 r.item_id=+$("#"+gid+"_it_"+i).value;
 const it=ITEMS.find(x=>x.id==r.item_id);
 r.price=G.cfg.type==="sale"?(it.sales_price||0):(it.purchase_price||0);
 const u=((it&&it.units)||[{unit_code:it.base_unit,conversion:1}])[0];r.unit=u.unit_code+"|"+u.conversion;
 gridDraw(gid);
}
function gridUpd(gid,i){
 const G=GRIDS[gid];if(!G)return;const r=G.rows[i];if(!r)return;
 const g=id=>$("#"+gid+"_"+id+"_"+i);if(!g("it"))return;
 r.item_id=+g("it").value;if(G.cfg.wh&&g("wh"))r.wh=+g("wh").value;r.unit=g("un").value;
 r.qty=+g("q").value||0;r.price=+g("p").value||0;
 r.desc=g("ds")?g("ds").value:"";
 r.d1=G.cfg.disc?+g("a").value||0:0;r.d2=G.cfg.disc?+g("b").value||0:0;
 const gross=r.qty*r.price,d1=gross*r.d1/100,d2=(gross-d1)*r.d2/100;
 r.lt=Math.round((gross-d1-d2)*100)/100;
 const t=$("#"+gid+"_t_"+i);if(t)t.textContent=fmt(r.lt);
 const s=$("#"+gid+"_sub");if(s)s.textContent=fmt(Math.round(G.rows.reduce((a,x)=>a+(x.lt||0),0)*100)/100);
}
function gridDel(gid,i){const G=GRIDS[gid];if(!G)return;G.rows.splice(i,1);if(!G.rows.length)gridAdd(gid);else gridDraw(gid);}
function gridLines(gid){
 const G=GRIDS[gid];if(!G)return [];
 return G.rows.filter(r=>r.qty>0).map(r=>{const parts=String(r.unit||"|1").split("|");
  const o={item_id:r.item_id,qty:r.qty,price:r.price,discount_pct:r.d1,discount_pct2:r.d2,description:r.desc||"",unit_code:parts[0],unit_conv:+parts[1]||1};
  if(G.cfg.wh)o.warehouse_id=r.wh;return o;});
}
function renderCustomerDetail(id){
 const c=CUST.find(x=>x.id===id);if(!c)return A.innerHTML=`<div class="card">Pelanggan tidak ditemukan.</div>`;
 const a=COA.find(x=>x.id===c.receivable_account_id);
 return `<div class="card">
  <div class="row" style="margin-bottom:16px"><button class="go" onclick="goBack()">← Kembali</button> <h3 style="margin:0">Detail Pelanggan</h3></div>
  <div class="grid" style="grid-template-columns:1fr 1fr">
   <div><p><b>Kode:</b> ${esc(c.customer_code)}</p><p><b>Nama:</b> ${esc(c.customer_name)}</p><p><b>Email:</b> ${esc(c.email||"-")}</p></div>
   <div><p><b>Akun Piutang:</b> ${a?esc(a.account_code+" "+a.account_name):"-"}</p><p><b>Limit Piutang:</b> ${fmt(c.credit_limit||0)}</p><p><b>Termin:</b> ${esc((c.terms||"")+" "+(c.term_days||""))}</p></div>
  </div>
  <div class="row" style="margin-top:16px"><button class="go" onclick="editCustomer(${c.id})">✏️ Edit</button></div>
 </div>
 <div class="card"><h3>Edit Pelanggan</h3>
  <div class="grid" style="grid-template-columns:1fr 1fr">
   <div><div class="row">Nama <input id="ec_name" value="${esc(c.customer_name)}"></div>
   <div class="row">Email <input id="ec_email" value="${esc(c.email||"")}" type="email"></div></div>
   <div><div class="row">Limit <input id="ec_limit" value="${c.credit_limit||0}" type="number"></div>
   <div class="row">Termin <input id="ec_terms" value="${esc(c.terms||"NET 30")}" style="width:100px"> Hari <input id="ec_days" value="${c.term_days||30}" style="width:60px" type="number"></div></div>
  </div>
  <div class="row" style="margin-top:12px"><button class="go" onclick="saveEditCust(${c.id})">💾 Simpan</button></div>
 </div>`;
}
window.editCustomer=id=>{curDetail="customer";curDetailId=id;render();};
window.saveEditCust=async id=>{try{await api("/api/customers/"+id,{method:"PUT",body:JSON.stringify({customer_name:$("#ec_name").value,email:$("#ec_email").value})});await api("/api/customers/limit",{method:"POST",body:JSON.stringify({id,credit_limit:+$("#ec_limit").value,terms:$("#ec_terms").value,term_days:+$("#ec_days").value})});await loadM();alert("Tersimpan");render();}catch(e){alert(e.message)}};
async function renderSalesInvoiceDetail(id){
 try{
  const inv=(await api("/api/sales")).find(x=>x.id===id);
  if(!inv)return A.innerHTML=`<div class="card">Invoice tidak ditemukan.</div>`;
  const cust=CUST.find(c=>c.id===inv.customer_id);
  return `<div class="card">
   <div class="detail-header"><button class="go" onclick="goBack()">← Kembali</button> <h3 style="margin:0">Faktur Penjualan ${esc(inv.invoice_number)}</h3> ${st(inv.status)}</div>
   <div class="info-grid">
    <div class="info-item"><label>Nomor</label><span>${esc(inv.invoice_number)}</span></div>
    <div class="info-item"><label>Tanggal</label><span>${inv.transaction_date}</span></div>
    <div class="info-item"><label>Jatuh Tempo</label><span>${inv.due_date||"-"}</span></div>
    <div class="info-item"><label>Customer</label><span>${esc(inv.customer_name)}</span></div>
    <div class="info-item"><label>Salesman</label><span>${esc(inv.salesperson||"-")}</span></div>
    <div class="info-item"><label>Komisi</label><span>${fmt(inv.commission_amount||0)}</span></div>
    <div class="info-item"><label>Mata Uang</label><span>${esc(cust?.currency_code||"IDR")}</span></div>
   </div>
   <div class="card" style="margin-top:16px"><h3>Detail Baris</h3>
    <table><thead><tr><th>Barang</th><th>Deskripsi</th><th>Qty</th><th>Harga</th><th>Diskon</th><th>Total</th></tr></thead>
    <tbody>${(inv.lines||[]).map(l=>`<tr><td>${esc(l.item_name||"")}</td><td>${esc(l.description||"")}</td><td>${l.unit_qty||l.quantity} ${l.unit_code||""}</td><td>${fmt(l.unit_price)}</td><td>${fmt(l.discount_amount||0)}</td><td>${fmt(l.line_total)}</td></tr>`).join("")}</tbody></table></div>
   <div class="grid" style="grid-template-columns:1fr 1fr;margin-top:16px">
    <div class="card"><h3>Ringkasan</h3>
     <p>Subtotal: <b>${fmt(inv.subtotal)}</b></p>
     <p>PPN: <b>${fmt(inv.tax_amount)}</b></p>
     <p><b>Total: ${fmt(inv.total_amount)}</b></p>
     <p>Tukar+: <b>${fmt(inv.tradein_total||0)}</b></p>
    </div>
    <div class="card"><h3>Pembayaran</h3>
     <p>Dibayar: <b>${fmt(inv.paid)}</b></p>
     <p>Retur: <b>${fmt(inv.returned||0)}</b></p>
     <p>Sisa: <b>${fmt(inv.outstanding)}</b></p>
    </div>
   </div>
    <div class="row" style="margin-top:16px">
     <button class="go" onclick="printInv(${inv.id})">🖨️ Cetak</button>
     <button class="go" onclick="exportInvoicePDF(${inv.id})">📄 Export PDF</button>
     ${inv.status!=="VOID"?`<button class="go danger" onclick="voidSale(${inv.id})">Void</button>`:""}
    </div>
  </div>`;
 }catch(e){return `<div class="card">❌ ${e.message}</div>`;}
}
async function renderPurchaseInvoiceDetail(id){
 try{
  const inv=(await api("/api/purchases")).find(x=>x.id===id);
  if(!inv)return A.innerHTML=`<div class="card">Invoice tidak ditemukan.</div>`;
  return `<div class="card">
   <div class="detail-header"><button class="go" onclick="goBack()">← Kembali</button> <h3 style="margin:0">Faktur Pembelian ${esc(inv.invoice_number)}</h3> ${st(inv.status)}</div>
   <div class="info-grid">
    <div class="info-item"><label>Nomor</label><span>${esc(inv.invoice_number)}</span></div>
    <div class="info-item"><label>Tanggal</label><span>${inv.transaction_date}</span></div>
    <div class="info-item"><label>Vendor</label><span>${esc(inv.vendor_name)}</span></div>
   </div>
   <div class="card" style="margin-top:16px"><h3>Detail Baris</h3>
    <table><thead><tr><th>Barang</th><th>Qty</th><th>Harga</th><th>Total</th></tr></thead>
    <tbody>${(inv.lines||[]).map(l=>`<tr><td>${esc(l.item_name||"")}</td><td>${l.quantity} ${l.unit_code||""}</td><td>${fmt(l.unit_price)}</td><td>${fmt(l.line_total)}</td></tr>`).join("")}</tbody></table></div>
   <div class="grid" style="grid-template-columns:1fr 1fr;margin-top:16px">
    <div class="card"><h3>Ringkasan</h3>
     <p>Subtotal: <b>${fmt(inv.subtotal)}</b></p>
     <p>PPN: <b>${fmt(inv.tax_amount)}</b></p>
     <p><b>Total: ${fmt(inv.total_amount)}</b></p>
    </div>
    <div class="card"><h3>Pembayaran</h3>
     <p>Dibayar: <b>${fmt(inv.paid)}</b></p>
     <p>Retur: <b>${fmt(inv.returned||0)}</b></p>
     <p>Sisa: <b>${fmt(inv.outstanding)}</b></p>
    </div>
   </div>
   <div class="row" style="margin-top:16px">
    ${inv.status!=="VOID"?`<button class="go danger" onclick="voidBuy(${inv.id})">Void</button>`:""}
   </div>
  </div>`;
 }catch(e){return `<div class="card">❌ ${e.message}</div>`;}
}
async function renderSalesOrderDetail(id){
 try{
  const so=(await api("/api/sales-orders")).find(x=>x.id===id);
  if(!so)return A.innerHTML=`<div class="card">SO tidak ditemukan.</div>`;
  return `<div class="card">
   <div class="detail-header"><button class="go" onclick="goBack()">← Kembali</button> <h3 style="margin:0">Pesanan Penjualan ${esc(so.order_number)}</h3> ${st(so.status)}</div>
   <div class="info-grid">
    <div class="info-item"><label>Nomor</label><span>${esc(so.order_number)}</span></div>
    <div class="info-item"><label>Tanggal</label><span>${so.transaction_date}</span></div>
    <div class="info-item"><label>Customer</label><span>${esc(so.customer_name)}</span></div>
    <div class="info-item"><label>Total</label><span>${fmt(so.total_amount)}</span></div>
   </div>
   <div class="card" style="margin-top:16px"><h3>Detail Baris</h3>
    <table><thead><tr><th>Barang</th><th>Order</th><th>Terkirim</th><th>Tertagih</th></tr></thead>
    <tbody>${(so.lines||[]).map(l=>`<tr><td>${esc(l.item_name||"")}</td><td>${l.quantity}</td><td>${l.delivered}</td><td>${l.invoiced}</td></tr>`).join("")}</tbody></table></div>
   <div class="row" style="margin-top:16px">
    ${so.status!=="CLOSED"?`<button class="go danger" onclick="closeDoc('/api/sales-orders/close',${so.id})">Close</button>`:""}
   </div>
  </div>`;
 }catch(e){return `<div class="card">❌ ${e.message}</div>`;}
}
async function renderPurchaseOrderDetail(id){
 try{
  const po=(await api("/api/purchase-orders")).find(x=>x.id===id);
  if(!po)return A.innerHTML=`<div class="card">PO tidak ditemukan.</div>`;
  return `<div class="card">
   <div class="detail-header"><button class="go" onclick="goBack()">← Kembali</button> <h3 style="margin:0">Pesanan Pembelian ${esc(po.order_number)}</h3> ${st(po.status)}</div>
   <div class="info-grid">
    <div class="info-item"><label>Nomor</label><span>${esc(po.order_number)}</span></div>
    <div class="info-item"><label>Tanggal</label><span>${po.transaction_date}</span></div>
    <div class="info-item"><label>Vendor</label><span>${esc(po.vendor_name)}</span></div>
    <div class="info-item"><label>Total</label><span>${fmt(po.total_amount)}</span></div>
   </div>
   <div class="card" style="margin-top:16px"><h3>Detail Baris</h3>
    <table><thead><tr><th>Barang</th><th>Order</th><th>Diterima</th><th>Tertagih</th></tr></thead>
    <tbody>${(po.lines||[]).map(l=>`<tr><td>${esc(l.item_name||"")}</td><td>${l.quantity}</td><td>${l.received}</td><td>${l.billed}</td></tr>`).join("")}</tbody></table></div>
   <div class="row" style="margin-top:16px">
    ${po.status!=="CLOSED"?`<button class="go danger" onclick="closeDoc('/api/purchase-orders/close',${po.id})">Close</button>`:""}
   </div>
  </div>`;
 }catch(e){return `<div class="card">❌ ${e.message}</div>`;}
}
async function renderJournalDetail(id){
 try{
  const j=(await api("/api/journals")).find(x=>x.id===id);
  if(!j)return A.innerHTML=`<div class="card">Jurnal tidak ditemukan.</div>`;
  return `<div class="card">
   <div class="detail-header"><button class="go" onclick="goBack()">← Kembali</button> <h3 style="margin:0">Jurnal ${esc(j.journal_number)}</h3> ${st(j.status)}</div>
   <div class="info-grid">
    <div class="info-item"><label>Nomor</label><span>${esc(j.journal_number)}</span></div>
    <div class="info-item"><label>Tanggal</label><span>${j.transaction_date}</span></div>
    <div class="info-item"><label>Deskripsi</label><span>${esc(j.description)}</span></div>
   </div>
   <div class="card" style="margin-top:16px"><h3>Detail Jurnal</h3>
    <table><thead><tr><th>Kode</th><th>Akun</th><th>Debit</th><th>Kredit</th></tr></thead>
    <tbody>${(j.lines||[]).map(l=>`<tr><td>${esc(l.account_code)}</td><td>${esc(l.account_name)}</td><td>${fmt(l.debit)}</td><td>${fmt(l.credit)}</td></tr>`).join("")}</tbody>
    <tfoot><tr><td colspan="2"><b>Total</b></td><td><b>${fmt((j.lines||[]).reduce((a,l)=>a+l.debit,0))}</b></td><td><b>${fmt((j.lines||[]).reduce((a,l)=>a+l.credit,0))}</b></td></tr></tfoot></table></div>
  </div>`;
 }catch(e){return `<div class="card">❌ ${e.message}</div>`;}
}
function renderVendorDetail(id){
 const v=VEND.find(x=>x.id===id);if(!v)return A.innerHTML=`<div class="card">Vendor tidak ditemukan.</div>`;
 const a=COA.find(x=>x.id===v.payable_account_id);
 return `<div class="card">
  <div class="row" style="margin-bottom:16px"><button class="go" onclick="goBack()">← Kembali</button> <h3 style="margin:0">Detail Vendor</h3></div>
  <div class="grid" style="grid-template-columns:1fr 1fr">
   <div><p><b>Kode:</b> ${esc(v.vendor_code)}</p><p><b>Nama:</b> ${esc(v.vendor_name)}</p><p><b>Email:</b> ${esc(v.email||"-")}</p></div>
   <div><p><b>Akun Utang:</b> ${a?esc(a.account_code+" "+a.account_name):"-"}</p><p><b>Limit Utang:</b> ${fmt(v.credit_limit||0)}</p></div>
  </div>
  <div class="row" style="margin-top:16px"><button class="go" onclick="editVendor(${v.id})">✏️ Edit</button></div>
 </div>
 <div class="card"><h3>Edit Vendor</h3>
  <div class="grid" style="grid-template-columns:1fr 1fr">
   <div><div class="row">Nama <input id="ev_name" value="${esc(v.vendor_name)}"></div>
   <div class="row">Email <input id="ev_email" value="${esc(v.email||"")}" type="email"></div></div>
   <div><div class="row">Limit <input id="ev_limit" value="${v.credit_limit||0}" type="number"></div></div>
  </div>
  <div class="row" style="margin-top:12px"><button class="go" onclick="saveEditVend(${v.id})">💾 Simpan</button></div>
 </div>`;
}
window.editVendor=id=>{curDetail="vendor";curDetailId=id;render();};
window.saveEditVend=async id=>{try{await api("/api/vendors/"+id,{method:"PUT",body:JSON.stringify({vendor_name:$("#ev_name").value,email:$("#ev_email").value})});await api("/api/vendors/limit",{method:"POST",body:JSON.stringify({id,credit_limit:+$("#ev_limit").value})});await loadM();alert("Tersimpan");render();}catch(e){alert(e.message)}};
function renderItemDetail(id){
 const it=ITEMS.find(x=>x.id===id);if(!it)return A.innerHTML=`<div class="card">Barang tidak ditemukan.</div>`;
 const stk=window._stkCache||[];
 const itemStk=stk.filter(s=>s.item_code===it.item_code);
 const meth=itemStk.length?itemStk[0].method:"AVERAGE";
 const totalStock=itemStk.reduce((a,s)=>a+s.stock,0);
 const totalValue=itemStk.reduce((a,s)=>a+s.value,0);
 return `<div class="card">
  <div class="row" style="margin-bottom:16px"><button class="go" onclick="goBack()">← Kembali</button> <h3 style="margin:0">Detail Barang</h3></div>
  <div class="grid" style="grid-template-columns:1fr 1fr">
   <div><p><b>Kode:</b> ${esc(it.item_code)}</p><p><b>Nama:</b> ${esc(it.item_name)}</p><p><b>Tipe:</b> ${esc(it.item_type)}</p></div>
   <div><p><b>Stok Total:</b> ${totalStock} ${it.base_unit}</p><p><b>Nilai Stok:</b> ${fmt(totalValue)}</p><p><b>Metode HPP:</b> ${meth}</p></div>
  </div>
  <div class="grid" style="grid-template-columns:1fr 1fr 1fr;margin-top:12px">
   <div class="kpi"><div class="kpi-label">Harga Beli</div><b>${fmt(it.purchase_price||0)}</b></div>
   <div class="kpi kpi-info"><div class="kpi-label">Harga Jual</div><b>${fmt(it.sales_price||0)}</b></div>
   <div class="kpi kpi-success"><div class="kpi-label">Avg Cost</div><b>${fmt(it.avg_cost||0)}</b></div>
  </div>
  ${itemStk.length?`<div class="card" style="margin-top:16px"><h3>Stok per Gudang</h3><table><thead><tr><th>Gudang</th><th>Stok</th><th>Nilai</th><th>Avg Cost</th></tr></thead><tbody>${itemStk.map(s=>`<tr><td>${esc(s.warehouse)}</td><td>${s.stock}</td><td>${fmt(s.value)}</td><td>${fmt(s.avg_cost)}</td></tr>`).join("")}</tbody></table></div>`:""}
  <div class="row" style="margin-top:16px"><button class="go" onclick="editItem(${it.id})">✏️ Edit</button> <button class="go info" onclick="showStockCard(${it.id})">📊 Kartu Stok</button></div>
 </div>
 <div class="card"><h3>Edit Barang</h3>
  <div class="grid" style="grid-template-columns:1fr 1fr">
   <div><div class="row">Nama <input id="ei_name" value="${esc(it.item_name)}"></div>
   <div class="row">Harga Beli <input id="ei_bp" value="${it.purchase_price||0}" type="number"></div></div>
   <div><div class="row">Harga Jual <input id="ei_sp" value="${it.sales_price||0}" type="number"></div>
   <div class="row">Tipe <select id="ei_type"><option${it.item_type==="INVENTORY"?" selected":""}>INVENTORY</option><option${it.item_type==="SERVICE"?" selected":""}>SERVICE</option><option${it.item_type==="NON_INVENTORY"?" selected":""}>NON_INVENTORY</option></select></div></div>
  </div>
  <div class="row" style="margin-top:12px"><button class="go" onclick="saveEditItem(${it.id})">💾 Simpan</button></div>
 </div>`;
}
window.editItem=id=>{curDetail="item";curDetailId=id;render();};
window.saveEditItem=async id=>{try{await api("/api/items/"+id,{method:"PUT",body:JSON.stringify({item_name:$("#ei_name").value,purchase_price:+$("#ei_bp").value,sales_price:+$("#ei_sp").value,item_type:$("#ei_type").value})});await loadM();alert("Tersimpan");render();}catch(e){alert(e.message)}};
window.showStockCard=async id=>{try{const r=await api("/api/stock-card?item_id="+id);curDetail="stockcard";curDetailId=id;window._stockCardData=r;render();}catch(e){alert(e.message)}};
 async function render(){
  const A=$("#app");
  try{
  if(curDetail==="sales-invoice"){A.innerHTML=await renderSalesInvoiceDetail(curDetailId);return;}
  if(curDetail==="purchase-invoice"){A.innerHTML=await renderPurchaseInvoiceDetail(curDetailId);return;}
  if(curDetail==="sales-order"){A.innerHTML=await renderSalesOrderDetail(curDetailId);return;}
  if(curDetail==="purchase-order"){A.innerHTML=await renderPurchaseOrderDetail(curDetailId);return;}
  if(curDetail==="journal"){A.innerHTML=await renderJournalDetail(curDetailId);return;}
  if(cur==="Dashboard"){
   const d=await api("/api/dashboard");const f=await api("/api/forecast");
   A.innerHTML=`<div class="grid">
    <div class="kpi kpi-info"><div class="kpi-icon">📈</div><div class="kpi-label">Omzet</div><b>${fmt(d.omzet)}</b></div>
    <div class="kpi kpi-success"><div class="kpi-icon">💰</div><div class="kpi-label">Kas & Bank</div><b>${fmt(d.kas_bank)}</b></div>
    <div class="kpi kpi-warning"><div class="kpi-icon">📋</div><div class="kpi-label">Piutang Outstanding</div><b>${fmt(d.piutang_outstanding)}</b></div>
    <div class="kpi"><div class="kpi-icon">🛒</div><div class="kpi-label">Pembelian</div><b>${fmt(d.pembelian)}</b></div></div>
   <div class="card"><h3><span class="card-icon">💡</span>Cash-Flow Forecast (Next-Gen)</h3>
   <div style="overflow-x:auto"><table><thead><tr><th>Bulan</th><th>Proyeksi Kas Masuk</th><th>Status</th></tr></thead><tbody>${f.map(x=>`<tr><td>${x.bulan}</td><td><b>${fmt(x.proyeksi_kas_masuk)}</b></td><td><span class="bdg b-PENDING">Proyeksi</span></td></tr>`).join("")}</tbody></table></div>
   <p class="mut" style="margin-top:12px">${d.forecast}</p></div>
   <div class="grid" style="grid-template-columns: repeat(auto-fit, minmax(300px, 1fr))">
   <div class="card"><h3><span class="card-icon">⚠️</span>Stok Menipis</h3>${d.stok_menipis.length?`<div style="max-height:200px;overflow-y:auto">${d.stok_menipis.map(s=>`<div style="padding:8px;margin:4px 0;background:#fff5f5;border-radius:8px;border-left:3px solid #f56565"><b>${s.item_code}</b> - ${s.item_name}</div>`).join("")}</div>`:'<div class="empty-state"><div class="icon">✅</div><h4>Semua Stok Aman</h4><p>Tidak ada stok yang menipis</p></div>'}
   <p class="mut" style="margin-top:12px">📝 SO terbuka: <b>${d.open_so||0}</b> | PO terbuka: <b>${d.open_po||0}</b></p></div>
   <div class="card"><h3><span class="card-icon">📍</span>Absensi Cepat (GPS)</h3>
   <div class="row">Karyawan <select id="ab_emp" style="flex:1"></select></div>
   <div class="row"><button class="go ok" onclick="att('in')">✅ Masuk</button><button class="go danger" onclick="att('out')">🚪 Pulang</button></div>
   <div id="ab_out" class="mut">Lokasi GPS diambil otomatis dari browser.</div></div></div>
   <div class="card"><h3><span class="card-icon">📊</span>Omzet 6 Bulan Terakhir</h3><div id="ch" style="padding:16px 0"></div></div>
   <div class="card"><h3><span class="card-icon">⏰</span>Lewat Jatuh Tempo</h3><div id="due">Memuat…</div></div>
    <div class="card"><h3><span class="card-icon">📝</span>Transaksi Terakhir</h3><div id="recent_tx">Memuat...</div></div>
    <div class="card"><h3><span class="card-icon">📊</span>Omzet 6 Bulan Terakhir</h3><canvas id="chartOmzet" width="400" height="200"></canvas></div>
    <div class="card"><h3><span class="card-icon">💰</span>Piutang & Hutang</h3><canvas id="chartPH" width="400" height="200"></canvas></div>`;
  api("/api/employees").then(e=>{$("#ab_emp").innerHTML=e.filter(x=>x.is_active).map(x=>`<option value="${x.id}">${x.full_name}</option>`).join("");}).catch(()=>{$("#ab_out").textContent="Gagal muat karyawan.";});
   api("/api/dashboard/monthly").then(m=>{const mx=Math.max(1,...m.map(x=>x.omzet));
    const colors=["#667eea","#764ba2","#f093fb","#f5576c","#4facfe","#43e97b"];
    $("#ch").innerHTML=`<div style="display:flex;align-items:flex-end;gap:12px;height:180px;padding:0 10px">${m.map((x,i)=>{const h=Math.round(x.omzet/mx*100);return `<div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:8px"><div style="width:100%;height:${Math.max(h,8)}%;background:linear-gradient(180deg,${colors[i%colors.length]} 0%,${colors[(i+1)%colors.length]} 100%);border-radius:8px 8px 0 0;transition:all 0.3s;min-height:8px"></div><div style="font-size:11px;color:var(--mut)">${x.bulan}</div><div style="font-size:12px;font-weight:600;color:var(--ink)">${fmt(x.omzet)}</div></div>`;}).join("")}</div>`;}).catch(()=>{});
   Promise.all([api("/api/aging?type=AR"),api("/api/aging?type=AP")]).then(([ar,ap])=>{
    const od=ar.filter(x=>x.days_overdue>0), oa=ap.filter(x=>x.days_overdue>0);
    let html="<div style='display:flex;gap:16px;flex-wrap:wrap'>";
    html+=`<div style="flex:1;min-width:250px"><h4 style="color:var(--bad);margin-bottom:8px">Piutang (${od.length} telat)</h4>`;
    if(od.length){html+=`<div style="max-height:150px;overflow-y:auto">${od.map(x=>`<div style="padding:8px;margin:4px 0;background:#fff5f5;border-radius:8px;border-left:3px solid #f56565"><b>${x.invoice_number}</b> - ${x.contact}<br><span style="color:var(--mut)">${fmt(x.outstanding)} | ${x.days_overdue} hari telat</span></div>`).join("")}</div>`;}
    else{html+='<div class="empty-state" style="padding:16px"><div class="icon">✅</div><p>Piutang aman</p></div>';}
    html+="</div>";
    html+=`<div style="flex:1;min-width:250px"><h4 style="color:var(--warn);margin-bottom:8px">Utang (${oa.length} telat)</h4>`;
    if(oa.length){html+=`<div style="max-height:150px;overflow-y:auto">${oa.map(x=>`<div style="padding:8px;margin:4px 0;background:#fffff0;border-radius:8px;border-left:3px solid #ed8936"><b>${x.invoice_number}</b> - ${x.contact}<br><span style="color:var(--mut)">${fmt(x.outstanding)} | ${x.days_overdue} hari telat</span></div>`).join("")}</div>`;}
    else{html+='<div class="empty-state" style="padding:16px"><div class="icon">✅</div><p>Utang aman</p></div>';}
     html+="</div></div>";
     $("#due").innerHTML=html;}).catch(()=>{$("#due").textContent="—";});
     api("/api/sales").then(sales=>{
      const recent=sales.slice(-5).reverse();
      $("#recent_tx").innerHTML=recent.length?`<table><thead><tr><th>No</th><th>Tgl</th><th>Customer</th><th>Total</th><th>Status</th></tr></thead><tbody>${recent.map(x=>`<tr class="clickable-row" onclick="goDetail('sales-invoice',${x.id})"><td><b>${x.invoice_number}</b></td><td>${x.transaction_date}</td><td>${esc(x.customer_name)}</td><td>${fmt(x.total_amount)}</td><td>${st(x.status)}</td></tr>`).join("")}</tbody></table>`:'<div class="empty-state" style="padding:16px"><div class="icon">📝</div><p>Belum ada transaksi</p></div>';
     }).catch(()=>{});

     // Draw omzet chart
     setTimeout(async()=>{
      try{
       const sales=await api("/api/sales");
       const now=new Date();
       const months=[];
       const amounts=[];
       for(let i=5;i>=0;i--){
        const d=new Date(now.getFullYear(),now.getMonth()-i,1);
        const label=d.toLocaleDateString("id-ID",{month:"short"});
        const m=d.getMonth();
        const y=d.getFullYear();
        const total=sales.filter(x=>{
         const xd=new Date(x.transaction_date);
         return xd.getMonth()===m&&xd.getFullYear()===y;
        }).reduce((a,x)=>a+x.total_amount,0);
        months.push(label);
        amounts.push(total);
       }
       const canvas=document.getElementById("chartOmzet");
       if(canvas){
        const ctx=canvas.getContext("2d");
        const max=Math.max(...amounts,1);
        const barW=50;
        const gap=15;
        const startX=50;
        ctx.clearRect(0,0,canvas.width,canvas.height);
        ctx.font="11px Inter";
        // Y axis
        for(let i=0;i<=4;i++){
         const y=180-i*40;
         ctx.fillStyle="#94a3b8";
         ctx.fillText(fmt(max*i/4).replace(",00",""),0,y+4);
         ctx.strokeStyle="#e2e8f0";
         ctx.beginPath();ctx.moveTo(45,y);ctx.lineTo(400,y);ctx.stroke();
        }
        // Bars
        months.forEach((m,i)=>{
         const x=startX+i*(barW+gap);
         const h=(amounts[i]/max)*160;
         const grad=ctx.createLinearGradient(x,180-h,x,180);
         grad.addColorStop(0,"#6366f1");
         grad.addColorStop(1,"#818cf8");
         ctx.fillStyle=grad;
         ctx.beginPath();
         ctx.roundRect(x,180-h,barW,h,4);
         ctx.fill();
         ctx.fillStyle="#1e293b";
         ctx.textAlign="center";
         ctx.fillText(m,x+barW/2,195);
         if(amounts[i]>0){
          ctx.fillText(fmt(amounts[i]).replace(",00",""),x+barW/2,175-h);
         }
        });
       }
      }catch(e){console.log("Chart error:",e);}
     },200);

     // Draw piutang/hutang chart
     setTimeout(async()=>{
      try{
       const sales=await api("/api/sales");
       const purchases=await api("/api/purchases");
       const piutang=sales.reduce((a,x)=>a+x.outstanding,0);
       const hutang=purchases.reduce((a,x)=>a+x.outstanding,0);
       const canvas=document.getElementById("chartPH");
       if(canvas){
        const ctx=canvas.getContext("2d");
        ctx.clearRect(0,0,canvas.width,canvas.height);
        const max=Math.max(piutang,hutang,1);
        // Piutang bar
        ctx.fillStyle="#10b981";
        ctx.beginPath();ctx.roundRect(50,50,((piutang/max)*300),30,4);ctx.fill();
        ctx.fillStyle="#1e293b";ctx.font="bold 12px Inter";
        ctx.fillText("Piutang: "+fmt(piutang),50,100);
        // Hutang bar
        ctx.fillStyle="#ef4444";
        ctx.beginPath();ctx.roundRect(50,130,((hutang/max)*300),30,4);ctx.fill();
        ctx.fillStyle="#1e293b";
        ctx.fillText("Hutang: "+fmt(hutang),50,180);
       }
      }catch(e){console.log("Chart error:",e);}
     },300);
 }
 if(cur==="Penjualan"){
  const sub=window._psub||"invoice";
  const inv=await api("/api/sales");const rets=await api("/api/returns?type=SALES");
  const sq=await api("/api/quotations");const so=await api("/api/sales-orders");const dn=await api("/api/deliveries");
   let h=`<div class="row">${[["quotation","Penawaran"],["order","Pesanan"],["delivery","Surat Jalan"],["invoice","Faktur"],["return","Retur"],["cn","CN (Credit Note)"],["dn","DN (Debit Note)"]].map(t=>`<button class="go"${sub===t[0]?"":' style="opacity:.55"'} onclick="_psub='${t[0]}';render()">${t[1]}</button>`).join("")}</div>`;
   h+=`<div class="row" style="margin:16px 0"><button class="go" onclick="batchPrintInvoices()">🖨️ Batch Print Faktur</button></div>`;
   if(sub==="quotation"){
   h+=`<div class="card"><h3>Penawaran Penjualan (non-posting)</h3>
   <div class="row">Customer <select id="q_cust">${CUST.map(c=>`<option value="${c.id}">${c.customer_name}</option>`).join("")}</select>
   Tgl <input type="date" id="q_date" value="${today()}"> PPN% <input id="q_tax" value="11" style="width:60px"></div>
   <div class="row">Barang <select id="q_item" onchange="unitCh('q')">${ITEMS.map(i=>`<option value="${i.id}">${i.item_code}</option>`).join("")}</select>
   Satuan <select id="q_unit"></select> Qty <input id="q_qty" value="1" style="width:60px"> Harga <input id="q_price" value="100000" style="width:120px">
   Deskripsi <input id="q_desc" value="" style="width:160px">
   <button class="go" onclick="addQ()">+ baris</button></div><div id="qlines"></div>
   <button class="go" onclick="saveQ()">Simpan Penawaran</button></div>
   <div class="card"><h3>Riwayat Penawaran</h3><table><tr><th>No</th><th>Tgl</th><th>Customer</th><th>Total</th><th>Status</th><th></th></tr>
   ${sq.map(x=>`<tr><td>${x.quotation_number}</td><td>${x.transaction_date}</td><td>${x.customer_name}</td><td>${fmt(x.total_amount)}</td><td>${st(x.status)}</td><td>${x.status==="OPEN"?`<button class="go danger" onclick="closeDoc('/api/quotations/close',${x.id})">Close</button>`:""}</td></tr>`).join("")}</table></div>`;
  }
  if(sub==="order"){
   h+=`<div class="card"><h3>Pesanan Penjualan / SO (non-posting, mengikat stok)</h3>
   <div class="row">Customer <select id="o_cust">${CUST.map(c=>`<option value="${c.id}">${c.customer_name}</option>`).join("")}</select>
   Tgl <input type="date" id="o_date" value="${today()}"> PPN% <input id="o_tax" value="11" style="width:60px">
   Dari penawaran <select id="o_sq"><option value="">- manual -</option>${sq.filter(x=>x.status==="OPEN").map(x=>`<option value="${x.id}">${x.quotation_number}</option>`).join("")}</select>
   <button class="go" onclick="copySQ()">Salin</button></div>
   <div id="oo_wrap"></div>
   <button class="go" onclick="saveO()">Simpan SO</button></div>
   <div class="card"><h3>Riwayat SO</h3>${so.map(x=>`<details><summary class="clickable-row" onclick="goDetail('sales-order',${x.id})" style="cursor:pointer"><b>${x.order_number}</b> ${x.transaction_date} ${x.customer_name} ${fmt(x.total_amount)} ${st(x.status)}</summary>
   <table><tr><th>Barang</th><th>Deskripsi</th><th>Order</th><th>Terkirim</th><th>Tertagih</th></tr>${x.lines.map(l=>`<tr><td>${l.item_name}</td><td>${l.description||""}</td><td>${l.quantity}</td><td>${l.delivered}</td><td>${l.invoiced}</td></tr>`).join("")}</table>
   ${x.status!=="CLOSED"?`<button class="go danger" onclick="closeDoc('/api/sales-orders/close',${x.id})">Close</button>`:""}</details>`).join("")}</div>`;
  }
  if(sub==="delivery"){
   const openSO=so.filter(x=>x.status!=="CLOSED");
   h+=`<div class="card"><h3>Surat Jalan / Delivery (stok keluar → Brg Dalam Perjalanan)</h3>
   <div class="row">Customer <select id="d_cust">${CUST.map(c=>`<option value="${c.id}">${c.customer_name}</option>`).join("")}</select>
   Tgl <input type="date" id="d_date" value="${today()}">
   Dari SO <select id="d_so" onchange="doLines()"><option value="">- langsung -</option>${openSO.map(x=>`<option value="${x.id}">${x.order_number} (${x.customer_name})</option>`).join("")}</select></div>
   <div id="dref"></div>
   <div class="row">Barang <select id="d_item" onchange="unitCh('d')">${ITEMS.filter(i=>i.item_type==="INVENTORY").map(i=>`<option value="${i.id}">${i.item_code}</option>`).join("")}</select>
   Gudang <select id="d_wh">${WH.map(w=>`<option value="${w.id}">${w.warehouse_name}</option>`).join("")}</select>
   Satuan <select id="d_unit"></select> Qty <input id="d_qty" value="1" style="width:60px"> Deskripsi <input id="d_desc" value="" style="width:140px">
   <button class="go" onclick="addD()">+ baris langsung</button></div><div id="dlines"></div>
   <button class="go" onclick="saveD()">Simpan Surat Jalan</button></div>
   <div class="card"><h3>Riwayat Surat Jalan</h3>${dn.map(x=>`<details><summary><b>${x.delivery_number}</b> ${x.transaction_date} ${x.customer_name} ${st(x.status)}</summary><table><tr><th>Barang</th><th>Deskripsi</th><th>Qty</th><th>Tertagih</th></tr>${x.lines.map(l=>`<tr><td>${l.item_name}</td><td>${l.description||""}</td><td>${l.quantity}</td><td>${l.invoiced_qty}</td></tr>`).join("")}</table>${x.status==="POSTED"?`<button class="go danger" onclick="voidD(${x.id})">Void</button>`:""}</details>`).join("")}</div>`;
  }
  if(sub==="invoice"){
  h+=`<div class="card"><h3>Buat Faktur Penjualan (auto-jurnal + auto-HPP FIFO/Average)</h3>
  <div class="row">Customer <select id="s_cust">${CUST.map(c=>`<option value="${c.id}">${esc(c.customer_name)}</option>`).join("")}</select>
  <button class="go" onclick="quickCust()">+ Baru</button>
  Gudang <select id="s_wh">${WH.map(w=>`<option value="${w.id}">${esc(w.warehouse_name)}</option>`).join("")}</select>
  Tgl <input type="date" id="s_date" value="${today()}"> PPN ${taxSel("s_tax",11)}</div>
  <div class="row">Salesman <select id="s_sp"><option value="">- tanpa salesman -</option>${SP.map(s=>`<option value="${s.id}">${s.sp_name} (${s.commission_pct}%)</option>`).join("")}</select>
  <span class="mut">komisi otomatis: Dr Beban Komisi / Cr Utang Komisi</span></div>
  <div class="row">Dari DO <select id="s_do" onchange="siDO()"><option value="">-</option>${dn.filter(x=>x.status==="POSTED").map(x=>`<option value="${x.id}">${x.delivery_number}</option>`).join("")}</select>
  Dari SO <select id="s_so" onchange="siSO()"><option value="">-</option>${so.filter(x=>x.status!=="CLOSED").map(x=>`<option value="${x.id}">${x.order_number}</option>`).join("")}</select>
  <span class="mut">Pilih untuk tagih dari surat jalan / pesanan</span></div>
  <div id="sref"></div>
  <div id="sg_wrap"></div><div id="slines" class="mut"></div>
  <button class="go" onclick="saveSale()">Simpan & Posting Jurnal</button>
  <details><summary class="mut">+ Tukar tambah (barang bekas masuk stok, piutang berkurang)</summary>
  <div class="row">Barang diterima <select id="ti_item">${ITEMS.filter(i=>i.item_type==="INVENTORY").map(i=>`<option value="${i.id}">${i.item_code}</option>`).join("")}</select>
  Qty <input id="ti_qty" value="1" style="width:60px"> Nilai kesepakatan <input id="ti_val" value="0" style="width:130px">
  Ket <input id="ti_note" value=""></div></details></div>
  <div class="card"><h3>Riwayat Invoice</h3><table><tr><th>No</th><th>Tgl</th><th>Customer</th><th>Sales</th><th>Total</th><th>Komisi</th><th>Tukar+</th><th>Sisa</th><th>Status</th><th></th></tr>
   ${inv.map(x=>`<tr class="clickable-row" onclick="goDetail('sales-invoice',${x.id})"><td><b>${x.invoice_number}</b></td><td>${x.transaction_date}</td><td>${x.customer_name}</td><td>${x.salesperson||"-"}</td><td>${fmt(x.total_amount)}</td><td>${fmt(x.commission_amount||0)}</td><td>${fmt(x.tradein_total||0)}</td><td>${fmt(x.outstanding)}</td><td>${st(x.status)}</td><td>${x.status!=="VOID"?`<button class="go danger" onclick="voidSale(${x.id})">Void</button>`:""} <button class="go" onclick="printInv(${x.id})">Cetak</button></td></tr>`).join("")}</table></div>`;
  }
  if(sub==="return"){
  h+=`<div class="card"><h3>Retur Penjualan (parsial, stok kembali + jurnal)</h3>
  <div class="row">Invoice <select id="rs_inv">${inv.filter(x=>x.status!=="VOID").map(x=>`<option value="${x.id}">${x.invoice_number} (sisa ${fmt(x.outstanding)})</option>`).join("")}</select>
  Barang <select id="rs_item">${ITEMS.map(i=>`<option value="${i.id}">${i.item_code}</option>`).join("")}</select>
  Gudang <select id="rs_wh">${WH.map(w=>`<option value="${w.id}">${w.warehouse_name}</option>`).join("")}</select>
  Qty <input id="rs_qty" value="1" style="width:60px"> Tgl <input type="date" id="rs_date" value="${today()}">
  <button class="go" onclick="saveRS()">Catat Retur</button></div>
   <table><tr><th>No Retur</th><th>Invoice</th><th>Tgl</th><th>Total</th></tr>${rets.map(r=>`<tr><td>${r.return_number}</td><td>${r.invoice_number}</td><td>${r.transaction_date}</td><td>${fmt(r.total_amount)}</td></tr>`).join("")}</table></div>`;
  }
  if(sub==="cn"){
   h+=`<div class="grid" style="grid-template-columns:1fr 1fr;gap:24px">
   <div class="card"><h3><span class="card-icon">📝</span>Form Credit Note</h3>
    <div class="grid grid-2">
     <div class="field"><label>Tanggal</label><input id="cn_d" type="date"></div>
     <div class="field"><label>Pelanggan</label><select id="cn_cust"><option value="">Pilih...</option>${CUST.map(x=>`<option value="${x.id}">${esc(x.customer_name)}</option>`).join("")}</select></div>
    </div>
    <div class="field"><label>Alasan / Deskripsi</label><input id="cn_desc" placeholder="Deskripsi credit note"></div>
    <div class="card" style="background:#004d400f;border:1px solid #004d4033">
     <div style="display:flex;align-items:center;gap:12px">
      <div class="field" style="flex:2"><label>Item</label><select id="cn_it"><option value="">Non-Inventory</option>${ITEMS.map(x=>`<option value="${x.id}">${esc(x.item_name)} [${esc(x.item_code)}]</option>`).join("")}</select></div>
      <div class="field" style="flex:1"><label>Qty</label><input id="cn_q" type="number" min="1" value="1"></div>
      <div class="field" style="flex:1"><label>Harga</label><input id="cn_pr" type="number" min="0" value="0"></div>
      <button class="go danger" style="margin-top:20px" onclick="addCNLine()">+ Tambah</button>
     </div>
    </div>
    <div class="field"><label>Deskripsi Baris</label><input id="cn_ldesc"></div>
    <div id="cn_preview" class="mut"></div>
    <button class="go" onclick="saveCN()" style="width:100%">Simpan Credit Note</button>
   </div>
   <div class="card"><h3>Daftar Credit Note</h3><div id="cn_list"></div></div></div>`;
  }
  if(sub==="dn"){
   h+=`<div class="grid" style="grid-template-columns:1fr 1fr;gap:24px">
   <div class="card"><h3><span class="card-icon">📝</span>Form Debit Note</h3>
    <div class="grid grid-2">
     <div class="field"><label>Tanggal</label><input id="dn_d" type="date"></div>
     <div class="field"><label>Vendor</label><select id="dn_ven"><option value="">Pilih...</option>${VEND.map(x=>`<option value="${x.id}">${esc(x.vendor_name)}</option>`).join("")}</select></div>
    </div>
    <div class="field"><label>Alasan / Deskripsi</label><input id="dn_desc" placeholder="Deskripsi debit note"></div>
    <div class="card" style="background:#7f1d1d0f;border:1px solid #7f1d1d33">
     <div style="display:flex;align-items:center;gap:12px">
      <div class="field" style="flex:2"><label>Item</label><select id="dn_it"><option value="">Non-Inventory</option>${ITEMS.map(x=>`<option value="${x.id}">${esc(x.item_name)} [${esc(x.item_code)}]</option>`).join("")}</select></div>
      <div class="field" style="flex:1"><label>Qty</label><input id="dn_q" type="number" min="1" value="1"></div>
      <div class="field" style="flex:1"><label>Harga</label><input id="dn_pr" type="number" min="0" value="0"></div>
      <button class="go danger" style="margin-top:20px" onclick="addDNLine()">+ Tambah</button>
     </div>
    </div>
    <div class="field"><label>Deskripsi Baris</label><input id="dn_ldesc"></div>
    <div id="dn_preview" class="mut"></div>
    <button class="go" onclick="saveDN()" style="width:100%">Simpan Debit Note</button>
   </div>
   <div class="card"><h3>Daftar Debit Note</h3><div id="dn_list"></div></div></div>`;
  }
  A.innerHTML=h;
  if(sub==="quotation"){window._ql=[];unitCh('q');}
  if(sub==="order"){gridStart('oo',{type:'sale',wh:false,disc:true});window._sq=sq;}
  if(sub==="delivery"){window._dl=[];unitCh('d');window._so=so.filter(x=>x.status!=="CLOSED");}
   if(sub==="invoice"){gridStart('sg',{type:'sale',wh:false,disc:true});window._sl=[];window._dn=dn;window._so2=so;}
   if(sub==="cn"){cnCLines=[];api("/api/sales").then(inv=>{const el=$("#cn_list");if(el)el.innerHTML=inv.filter(x=>x.status==='OPEN').map(x=>`<div style="padding:8px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;align-items:center"><div><b>${esc(x.invoice_number)}</b> - ${esc(x.customer_name)} - ${fmt(x.outstanding)}</div><button class="go" onclick="createCNFromInvoice(${x.id})">Buat CN</button></div>`).join("")||"<div class='empty-state'>Belum ada faktur</div>";});}
   if(sub==="dn"){dnDLines=[];api("/api/purchases").then(inv=>{const el=$("#dn_list");if(el)el.innerHTML=inv.filter(x=>x.status==='OPEN').map(x=>`<div style="padding:8px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;align-items:center"><div><b>${esc(x.invoice_number)}</b> - ${esc(x.vendor_name)} - ${fmt(x.outstanding)}</div><button class="go" onclick="createDNFromInvoice(${x.id})">Buat DN</button></div>`).join("")||"<div class='empty-state'>Belum ada faktur</div>";});}
 }
 if(cur==="Pembelian"){
  const sub=window._bsub||"invoice";
  const inv=await api("/api/purchases");const rets=await api("/api/returns?type=PURCHASE");
  const pr=await api("/api/requisitions");const po=await api("/api/purchase-orders");const ri=await api("/api/receives");
  let h=`<div class="row">${[["req","Permintaan"],["order","Pesanan (PO)"],["receive","Penerimaan"],["invoice","Faktur"],["return","Retur"]].map(t=>`<button class="go"${sub===t[0]?"":' style="opacity:.55"'} onclick="_bsub='${t[0]}';render()">${t[1]}</button>`).join("")}</div>`;
  if(sub==="req"){
   h+=`<div class="card"><h3>Permintaan Pembelian / PR (non-posting)</h3>
   <div class="row">Vendor (opsional) <select id="r_vend"><option value="">- internal -</option>${VEND.map(c=>`<option value="${c.id}">${c.vendor_name}</option>`).join("")}</select>
   Tgl <input type="date" id="r_date" value="${today()}"> Peminta <input id="r_req" value=""></div>
   <div class="row">Barang <select id="r_item">${ITEMS.map(i=>`<option value="${i.id}">${i.item_code}</option>`).join("")}</select>
   Qty <input id="r_qty" value="10" style="width:60px"> Estimasi harga <input id="r_price" value="50000" style="width:120px"> Deskripsi <input id="r_desc" value="" style="width:140px">
   <button class="go" onclick="addR()">+ baris</button></div><div id="rlines"></div>
   <button class="go" onclick="saveR()">Simpan PR</button></div>
   <div class="card"><h3>Riwayat PR</h3><table><tr><th>No</th><th>Tgl</th><th>Vendor</th><th>Status</th><th></th></tr>
   ${pr.map(x=>`<tr><td>${x.requisition_number}</td><td>${x.transaction_date}</td><td>${x.vendor_name||"-"}</td><td>${st(x.status)}</td><td>${x.status==="OPEN"?`<button class="go danger" onclick="closeDoc('/api/requisitions/close',${x.id})">Close</button>`:""}</td></tr>`).join("")}</table></div>`;
  }
  if(sub==="order"){
   h+=`<div class="card"><h3>Pesanan Pembelian / PO (non-posting)</h3>
   <div class="row">Vendor <select id="o_vend">${VEND.map(c=>`<option value="${c.id}">${c.vendor_name}</option>`).join("")}</select>
   Tgl <input type="date" id="o_date" value="${today()}"> PPN% <input id="o_tax" value="11" style="width:60px">
   Dari PR <select id="o_pr"><option value="">- manual -</option>${pr.filter(x=>x.status==="OPEN").map(x=>`<option value="${x.id}">${x.requisition_number}</option>`).join("")}</select>
   <button class="go" onclick="copyPR()">Salin</button></div>
   <div id="og_wrap"></div>
   <button class="go" onclick="saveO2()">Simpan PO</button></div>
   <div class="card"><h3>Riwayat PO</h3>${po.map(x=>`<details><summary class="clickable-row" onclick="goDetail('purchase-order',${x.id})" style="cursor:pointer"><b>${x.order_number}</b> ${x.transaction_date} ${x.vendor_name} ${fmt(x.total_amount)} ${st(x.status)}</summary>
   <table><tr><th>Barang</th><th>Order</th><th>Diterima</th><th>Tertagih</th></tr>${x.lines.map(l=>`<tr><td>${l.item_name}</td><td>${l.quantity}</td><td>${l.received}</td><td>${l.billed}</td></tr>`).join("")}</table>
   ${x.status!=="CLOSED"?`<button class="go danger" onclick="closeDoc('/api/purchase-orders/close',${x.id})">Close</button>`:""}</details>`).join("")}</div>`;
  }
  if(sub==="receive"){
   const openPO=po.filter(x=>x.status!=="CLOSED");
   h+=`<div class="card"><h3>Penerimaan Barang (stok masuk + utang akrual)</h3>
   <div class="row">Vendor <select id="v_vend">${VEND.map(c=>`<option value="${c.id}">${c.vendor_name}</option>`).join("")}</select>
   Tgl <input type="date" id="v_date" value="${today()}">
   Dari PO <select id="v_po" onchange="riLines()"><option value="">- langsung -</option>${openPO.map(x=>`<option value="${x.id}">${x.order_number} (${x.vendor_name})</option>`).join("")}</select></div>
   <div id="vref"></div>
   <div class="row">Barang <select id="v_item" onchange="unitCh('v')">${ITEMS.filter(i=>i.item_type==="INVENTORY").map(i=>`<option value="${i.id}">${i.item_code}</option>`).join("")}</select>
   Gudang <select id="v_wh">${WH.map(w=>`<option value="${w.id}">${w.warehouse_name}</option>`).join("")}</select>
   Satuan <select id="v_unit"></select> Qty <input id="v_qty" value="10" style="width:60px"> Harga <input id="v_price" value="50000" style="width:120px"> Deskripsi <input id="v_desc" value="" style="width:140px">
   <button class="go" onclick="addV()">+ baris langsung</button></div><div id="vlines"></div>
   <button class="go" onclick="saveV()">Simpan Penerimaan</button></div>
   <div class="card"><h3>Riwayat Penerimaan</h3><table><tr><th>No</th><th>Tgl</th><th>Vendor</th><th>Subtotal</th><th>Status</th><th></th></tr>
   ${ri.map(x=>`<tr><td>${x.receive_number}</td><td>${x.transaction_date}</td><td>${x.vendor_name}</td><td>${fmt(x.subtotal)}</td><td>${st(x.status)}</td><td>${x.status==="POSTED"?`<button class="go danger" onclick="voidR(${x.id})">Void</button>`:""}</td></tr>`).join("")}</table></div>`;
  }
  if(sub==="invoice"){
  h+=`<div class="card"><h3>Buat Faktur Pembelian (Dr Persediaan + PPN / Cr Utang)</h3>
  <div class="row">Vendor <select id="p_vend">${VEND.map(c=>`<option value="${c.id}">${esc(c.vendor_name)}</option>`).join("")}</select>
  <button class="go" onclick="quickVend()">+ Baru</button>
  Gudang <select id="p_wh">${WH.map(w=>`<option value="${w.id}">${esc(w.warehouse_name)}</option>`).join("")}</select>
  Tgl <input type="date" id="p_date" value="${today()}"> PPN ${taxSel("p_tax",11)}</div>
  <div class="row">Dari Receive <select id="p_ri" onchange="piRI()"><option value="">-</option>${ri.filter(x=>x.status==="POSTED").map(x=>`<option value="${x.id}">${x.receive_number}</option>`).join("")}</select>
  Dari PO <select id="p_po" onchange="piPO()"><option value="">-</option>${po.filter(x=>x.status!=="CLOSED").map(x=>`<option value="${x.id}">${x.order_number}</option>`).join("")}</select></div>
  <div id="pref"></div>
  <div id="pg_wrap"></div><div id="plines" class="mut"></div>
  <button class="go" onclick="saveBuy()">Simpan & Tambah Stok</button></div>
  <div class="card"><h3>Riwayat Tagihan Vendor</h3><table><tr><th>No</th><th>Tgl</th><th>Vendor</th><th>Total</th><th>Dibayar</th><th>Retur</th><th>Sisa</th><th>Status</th><th></th></tr>
   ${inv.map(x=>`<tr class="clickable-row" onclick="goDetail('purchase-invoice',${x.id})"><td><b>${x.invoice_number}</b></td><td>${x.transaction_date}</td><td>${x.vendor_name}</td><td>${fmt(x.total_amount)}</td><td>${fmt(x.paid)}</td><td>${fmt(x.returned||0)}</td><td>${fmt(x.outstanding)}</td><td>${st(x.status)}</td><td>${x.status!=="VOID"?`<button class="go danger" onclick="voidBuy(${x.id})">Void</button>`:""}</td></tr>`).join("")}</table></div>`;
  }
  if(sub==="return"){
  h+=`<div class="card"><h3>Retur Pembelian (parsial, stok keluar + jurnal)</h3>
  <div class="row">Tagihan <select id="rp_inv">${inv.filter(x=>x.status!=="VOID").map(x=>`<option value="${x.id}">${x.invoice_number} (sisa ${fmt(x.outstanding)})</option>`).join("")}</select>
  Barang <select id="rp_item">${ITEMS.map(i=>`<option value="${i.id}">${i.item_code}</option>`).join("")}</select>
  Gudang <select id="rp_wh">${WH.map(w=>`<option value="${w.id}">${w.warehouse_name}</option>`).join("")}</select>
  Qty <input id="rp_qty" value="1" style="width:60px"> Tgl <input type="date" id="rp_date" value="${today()}">
  <button class="go" onclick="saveRP()">Catat Retur</button></div>
  <table><tr><th>No Retur</th><th>Tagihan</th><th>Tgl</th><th>Total</th></tr>${rets.map(r=>`<tr><td>${r.return_number}</td><td>${r.invoice_number}</td><td>${r.transaction_date}</td><td>${fmt(r.total_amount)}</td></tr>`).join("")}</table></div>`;
  }
  A.innerHTML=h;
  if(sub==="req"){window._rl=[];}
  if(sub==="order"){gridStart('og',{type:'buy',wh:true,disc:false});window._pr=pr;}
  if(sub==="receive"){window._vl=[];unitCh('v');window._po=openPO;}
  if(sub==="invoice"){gridStart('pg',{type:'buy',wh:true,disc:false});window._pl=[];window._ri=ri;window._po2=po;}
 }
 if(cur==="Kas & Bank"){
  const p=await api("/api/payments");window._ag=await api("/api/aging?type=AR");window._agAP=await api("/api/aging?type=AP");
  A.innerHTML=`<div class="card"><h3>Kas & Bank — Pelunasan per Invoice (parsial didukung)</h3>
  <div class="row"><select id="k_kind" onchange="kindCh()"><option value="AR">Terima dari Customer (Dr Kas / Cr Piutang)</option><option value="AP">Bayar ke Vendor (Dr Utang / Cr Kas)</option></select>
  Akun Kas ${coaSel("k_cash")}</div>
  <div class="row">Kontak <select id="k_c"></select> Invoice <select id="k_inv" onchange="invCh()"></select>
  Nominal <input id="k_alloc" style="width:130px"><button class="go" onclick="addAlloc()">+ Alokasi</button></div>
  <div id="alocs"></div>
   <div class="row">Tgl <input type="date" id="k_date" value="${today()}"> Catatan <input id="k_note" value=""> Kurs <input id="k_rate" type="number" min="1" value="1" step="0.01" style="width:100px">
   <button class="go" onclick="savePay()">Catat Pembayaran</button></div>
  <p class="mut">Tips rekonsiliasi: bandingkan saldo akun 11001/11002 di Trial Balance dengan mutasi di bawah. Selisih = belum rekonsil.</p></div>
  <div class="card"><h3>Transfer Antar Kas / Bank</h3>
  <div class="row">Dari ${coaSel("t_from")} Ke ${coaSel("t_to")} Nominal <input id="t_amt" value="500000">
  Tgl <input type="date" id="t_date" value="${today()}"> Ket <input id="t_note" value="Transfer dana">
  <button class="go" onclick="saveT()">Transfer</button></div></div>
  <div class="card"><h3>Rekonsiliasi Bank (koran vs sistem)</h3>
  <div class="row">Rekening ${bankSel("rc_acc")} <button class="go" onclick="loadRecon()">Tampilkan</button>
  <button class="go" onclick="autoRecon()">Auto-Match</button></div>
  <div class="row">Tgl <input type="date" id="rc_d" value="${today()}"> Ket <input id="rc_desc" value="Mutasi koran">
  Nominal <input id="rc_amt" value="1000000" style="width:130px">
  <select id="rc_dir"><option value="IN">Masuk (IN)</option><option value="OUT">Keluar (OUT)</option></select>
  <button class="go" onclick="saveStmt()">+ Mutasi Koran</button></div>
  <div id="recon"></div></div>
  <div class="card"><h3>Uang Muka (DP) — terima/bayar lalu alokasikan</h3>
  <div class="row"><select id="dp_kind" onchange="dpKind()"><option value="AR">Terima DP Customer (Dr Kas / Cr UMP)</option><option value="AP">Bayar DP Vendor (Dr UMB / Cr Kas)</option></select>
  Kontak <select id="dp_c"></select> Kas ${coaSel("dp_cash")} Nominal <input id="dp_amt" value="1000000" style="width:130px">
  Tgl <input type="date" id="dp_date" value="${today()}"><button class="go" onclick="saveDP()">Catat DP</button></div>
  <div class="row">DP <select id="dpa_dp"></select> ke Invoice <select id="dpa_inv"></select>
  Nominal <input id="dpa_amt" style="width:130px"><button class="go" onclick="allocDP()">Alokasikan</button></div>
  <div id="dp_list" class="mut">Memuat…</div></div>
  <div class="card"><h3>Giro — terima/keluar, cairkan/tolak</h3>
  <div class="row"><select id="g_kind" onchange="giroKind()"><option value="AR">Terima giro Customer</option><option value="AP">Giro ke Vendor</option></select>
  Kontak <select id="g_c"></select> No giro <input id="g_no" value="" style="width:110px"> Bank <input id="g_bank" value="" style="width:110px">
  Tgl <input type="date" id="g_issue" value="${today()}"> Jth tempo <input type="date" id="g_due" value="${today()}"></div>
  <div class="row">Invoice <select id="g_inv"></select> Nominal <input id="g_amt" style="width:130px">
  <button class="go" onclick="addGiroAlloc()">+ Alokasi</button></div><div id="galocs"></div>
  <button class="go" onclick="saveGiro()">Catat Giro</button>
  <div id="giro_list">Memuat…</div></div>
  <div class="card"><table><tr><th>No</th><th>Tgl</th><th>Jenis</th><th>Nominal</th></tr>${p.map(x=>`<tr><td>${x.payment_number}</td><td>${x.transaction_date}</td><td>${x.kind}</td><td>${fmt(x.amount)}</td></tr>`).join("")}</table></div>`;
  window._al=[];kindCh();window._gal=[];dpInit();giroInit();
 }
 if(cur==="Buku Besar"){
  const j=await api("/api/journals");
  A.innerHTML=`<div class="card"><h3>Jurnal Umum (wajib seimbang D=K)</h3>
  <div class="row">Tgl <input type="date" id="j_d" value="${today()}"> Ket <input id="j_desc" value="Jurnal penyesuaian"> Akun ${coaSel("j_a")} D <input id="j_db" value="100000" style="width:100px"> K <input id="j_cr" value="0" style="width:100px">
  <button class="go" onclick="addJ()">+ baris</button></div><div id="jlines"></div><button class="go" onclick="saveJ()">Posting Jurnal</button></div>
   <div class="card"><h3>Histori (${j.length})</h3>${j.slice(0,30).map(x=>`<details><summary class="clickable-row" onclick="goDetail('journal',${x.id})" style="cursor:pointer"><b>${x.journal_number}</b> ${x.transaction_date} — ${x.description} [${x.status}]</summary><table>${x.lines.map(l=>`<tr><td>${l.account_code}</td><td>${l.account_name}</td><td>${fmt(l.debit)}</td><td>${fmt(l.credit)}</td></tr>`).join("")}</table></details>`).join("")}</div>
  <div class="card"><h3>🔒 Tutup Buku / Kunci Periode (admin)</h3>
  <div class="row">Tahun <input id="pe_y" value="${new Date().getFullYear()-1}" style="width:80px"><button class="go danger" onclick="closeYear()">Tutup & Kunci</button></div>
  <div id="locks" class="mut">Memuat…</div></div>`;
  window._jl=[];
  api("/api/period-locks").then(l=>{$("#locks").innerHTML=l.length?("Terkunci: "+l.map(x=>x.year+" (oleh "+x.locked_by+")").join(", ")):"Belum ada periode terkunci.";}).catch(()=>{$("#locks").textContent="";});
 }
  if(cur==="Persediaan"){
   const s=await api("/api/stock");
   const invItems=ITEMS.filter(i=>i.item_type==="INVENTORY");
   const stab=window._ssub||"default";
   let h=`<div class="row">${[["default","📦 Kartu Stok"],["sa","📝 Stok Opname"],["adj","🔧 Adjustment"]].map(t=>`<button class="go"${stab===t[0]?"":' style="opacity:.55"'} onclick="_ssub='${t[0]}';render()">${t[1]}</button>`).join("")}</div>`;
   if(stab==="default"){
   h+=`<div class="card"><h3>Kartu Stok (SUM in − out) + HPP Average</h3>
   <table><tr><th>Barang</th><th>Gudang</th><th>Stok</th><th>Avg Cost</th></tr>${s.map(x=>`<tr><td>${x.item_code} ${x.item_name}</td><td>${x.warehouse}</td><td>${x.stock}</td><td>${fmt(x.avg_cost)}</td></tr>`).join("")}</table>
   <div class="row">Lihat kartu: <select id="sc">${ITEMS.map(i=>`<option value="${i.id}">${i.item_code}</option>`).join("")}</select><button class="go" onclick="card()">Tampilkan</button></div><div id="card"></div></div>
   <div class="card"><h3>💡 Saran Order Cerdas (30 hari terakhir, buffer 10 hari)</h3><div id="reorder">Memuat…</div></div>
   <div class="card"><h3>Stock Opname (penyesuaian + jurnal selisih)</h3>
   <div class="row">Barang <select id="o_item">${invItems.map(i=>`<option value="${i.id}">${i.item_code}</option>`).join("")}</select>
   Gudang <select id="o_wh">${WH.map(w=>`<option value="${w.id}">${w.warehouse_name}</option>`).join("")}</select>
   Stok fisik <input id="o_qty" style="width:80px"> Tgl <input type="date" id="o_date" value="${today()}">
   <button class="go" onclick="opname()">Simpan Opname</button></div></div>
   <div class="card"><h3>Mutasi Antar Gudang</h3>
   <div class="row">Barang <select id="t_item">${invItems.map(i=>`<option value="${i.id}">${i.item_code}</option>`).join("")}</select>
   Dari <select id="t_from">${WH.map(w=>`<option value="${w.id}">${w.warehouse_name}</option>`).join("")}</select>
   Ke <select id="t_to">${WH.map(w=>`<option value="${w.id}">${w.warehouse_name}</option>`).join("")}</select>
   Qty <input id="t_qty" style="width:80px"> Tgl <input type="date" id="t_date" value="${today()}">
   <button class="go" onclick="transfer()">Pindahkan</button></div></div>`;
   }
   if(stab==='sa'){
    h+=`<div class="grid" style="grid-template-columns:1fr 1fr;gap:24px">
    <div class="card"><h3><span class="card-icon">📝</span>Form Stok Opname</h3>
    <div class="grid grid-2">
    <div class="field"><label>Tanggal</label><input id="sa_d" type="date"></div>
    <div class="field"><label>Gudang</label><select id="sa_wh"><option value="">Pilih...</option>${WH.map(x=>`<option value="${x.id}">${esc(x.warehouse_name)}</option>`).join("")}</select></div>
    </div>
    <div class="field"><label>Catatan</label><input id="sa_note" placeholder="Catatan opname"></div>
    <div class="card" style="background:#f0fdf4;border:1px solid #22c55e33">
    <div style="display:flex;align-items:center;gap:12px">
    <div class="field" style="flex:2"><label>Barang</label><select id="sa_it"><option value="">Pilih...</option>${ITEMS.map(x=>`<option value="${x.id}">${esc(x.item_name)} [${esc(x.item_code)}]</option>`).join("")}</select></div>
    <div class="field" style="flex:1"><label>Stok Sistem</label><input id="sa_sys" type="number" readonly></div>
    <div class="field" style="flex:1"><label>Stok Fisik</label><input id="sa_fisik" type="number" min="0"></div>
    <div class="field" style="flex:1"><label>Selisih</label><input id="sa_selisih" type="number" readonly></div>
    <button class="go danger" style="margin-top:20px" onclick="addSALine()">+ Tambah</button>
    </div>
    </div>
    <button class="go" onclick="saveSA()" style="width:100%">Simpan Stok Opname</button>
    </div>
    <div class="card"><h3>Riwayat Stok Opname</h3><div id="sa_list">Memuat...</div></div></div>`;
    saLines=[];
    api("/api/stock-adjustments").then(adj=>{
    if($("#sa_list"))$("#sa_list").innerHTML=adj.filter(x=>x.type==="OPNAME").slice(-10).reverse().map(x=>`<div style="padding:8px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;align-items:center">
    <div><b>${esc(x.adjustment_number||"ADJ-"+x.id)}</b> - ${x.transaction_date} - ${esc(x.note||"-")}</div>
    <button class="go" onclick="viewSA(${x.id})">Lihat</button></div>`).join("")||"<div class='empty-state'>Belum ada opname</div>";
    });
    if($("#sa_it"))$("#sa_it").onchange=async()=>{
    const id=+$("#sa_it").value;
    if(!id)return;
    const items=await api("/api/items");
    const item=items.find(x=>x.id===id);
    if($("#sa_sys"))$("#sa_sys").value=item?.stock_qty||0;
    if($("#sa_selisih"))$("#sa_selisih").value=(+($("#sa_fisik")?$("#sa_fisik").value:0))-($("#sa_sys")?+$("#sa_sys").value:0);
    };
    if($("#sa_fisik"))$("#sa_fisik").oninput=()=>{
    if($("#sa_selisih"))$("#sa_selisih").value=(+($("#sa_fisik").value||0))-($("#sa_sys")?+$("#sa_sys").value:0);
    };
   }
   if(stab==='adj'){
    h+=`<div class="grid" style="grid-template-columns:1fr 1fr;gap:24px">
    <div class="card"><h3><span class="card-icon">📝</span>Adjustment Manual</h3>
    <div class="grid grid-2">
    <div class="field"><label>Tanggal</label><input id="adj_d" type="date"></div>
    <div class="field"><label>Gudang</label><select id="adj_wh"><option value="">Pilih...</option>${WH.map(x=>`<option value="${x.id}">${esc(x.warehouse_name)}</option>`).join("")}</select></div>
    </div>
    <div class="field"><label>Jenis</label><select id="adj_kind"><option value="IN">Stok Masuk (+)</option><option value="OUT">Stok Keluar (-)</option></select></div>
    <div class="field"><label>Catatan</label><input id="adj_note" placeholder="Catatan adjustment"></div>
    <div class="card" style="background:#fef3c7;border:1px solid #f59e0b33">
    <div style="display:flex;align-items:center;gap:12px">
    <div class="field" style="flex:2"><label>Barang</label><select id="adj_it"><option value="">Pilih...</option>${ITEMS.map(x=>`<option value="${x.id}">${esc(x.item_name)} [${esc(x.item_code)}]</option>`).join("")}</select></div>
    <div class="field" style="flex:1"><label>Qty</label><input id="adj_q" type="number" min="1" value="1"></div>
    <button class="go danger" style="margin-top:20px" onclick="addAdjLine()">+ Tambah</button>
    </div>
    </div>
    <button class="go" onclick="saveAdj()" style="width:100%">Simpan Adjustment</button>
    </div>
    <div class="card"><h3>Riwayat Adjustment</h3><div id="adj_list">Memuat...</div></div></div>`;
    adjLines=[];
    api("/api/stock-adjustments").then(adj=>{
    if($("#adj_list"))$("#adj_list").innerHTML=adj.filter(x=>x.type!=="OPNAME").slice(-10).reverse().map(x=>`<div style="padding:8px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;align-items:center">
    <div><b>${esc(x.adjustment_number||"ADJ-"+x.id)}</b> - ${x.transaction_date} - ${esc(x.note||"-")}</div>
    <button class="go" onclick="viewSA(${x.id})">Lihat</button></div>`).join("")||"<div class='empty-state'>Belum ada adjustment</div>";
    });
   }
   A.innerHTML=h;
   if(stab==="default"){
   api("/api/reorder").then(r=>{$("#reorder").innerHTML=`<table><tr><th>Barang</th><th>Stok</th><th>Laku/bln</th><th>Tahan</th><th>Saran Order</th><th>Status</th></tr>${r.map(x=>`<tr><td>${x.item_code}</td><td>${x.stock}</td><td>${x.rata_hari}/hr</td><td>${x.tahan_hari} hr</td><td>${x.saran_order}</td><td>${x.status}</td></tr>`).join("")}</table>`;}).catch(e=>{$("#reorder").textContent=e.message;});
   }
  }
 if(cur==="Aset Tetap"){
  const a=await api("/api/assets");
  A.innerHTML=`<div class="card"><h3>Aset Tetap + Penyusutan otomatis</h3>
  <div class="row">Kode <input id="a_c" value="AST-001"> Nama <input id="a_n" value="Mobil Operasional"> Tgl <input type="date" id="a_d" value="${today()}">
  Harga <input id="a_cost" value="200000000"> Umur(bln) <input id="a_u" value="48" style="width:60px"><button class="go" onclick="saveA()">Tambah</button></div></div>
  <div class="card"><table><tr><th>Kode</th><th>Nama</th><th>Harga</th><th>Akum.</th><th>Aksi</th></tr>
  ${a.map(x=>`<tr><td>${x.asset_code}</td><td>${x.asset_name}</td><td>${fmt(x.cost)}</td><td>${fmt(x.accum_depr)}</td><td><button class="go" onclick="susut(${x.id})">Susutkan bulan ini</button></td></tr>`).join("")}</table></div>`;
 }
 if(cur==="Budgeting"){
 const now=new Date();
 const curYear=now.getFullYear();
 const yearOpts=[curYear-1,curYear,curYear+1].map(y=>`<option value="${y}" ${y===curYear?"selected":""}>${y}</option>`).join("");
 
 A.innerHTML=`<div class="page-header"><h1>💰 Anggaran (Budgeting)</h1></div>
 <div class="row" style="margin-bottom:24px">
  <div class="field"><label>Tahun</label><select id="bud_year" onchange="loadBudget()">${yearOpts}</select></div>
  <div class="field"><label>Bulan</label><select id="bud_month">
   <option value="0">Semua Bulan</option>
   ${["Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus","September","Oktober","November","Desember"].map((m,i)=>`<option value="${i+1}">${m}</option>`).join("")}
  </select></div>
  <button class="go" onclick="loadBudget()">🔍 Tampilkan</button>
  <button class="go" onclick="exportBudget()">📥 Export</button>
 </div>
 <div class="card" id="budgetOutput">
  <div class="empty-state"><div class="icon">💰</div><p>Pilih tahun untuk menampilkan anggaran</p></div>
 </div>`;
 setTimeout(loadBudget,100);
}
if(cur==="Laporan"){
  const now=new Date();
  const curMonth=now.getMonth()+1;
  const curYear=now.getFullYear();
  
  // Generate month options
  const months=["Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus","September","Oktober","November","Desember"];
  const monthOpts=months.map((m,i)=>`<option value="${i+1}" ${i+1===curMonth?"selected":""}>${m}</option>`).join("");
  const yearOpts=[curYear-1,curYear,curYear+1].map(y=>`<option value="${y}" ${y===curYear?"selected":""}>${y}</option>`).join("");
  
  A.innerHTML=`<div class="page-header"><h1>📊 Laporan</h1></div>
 <div class="grid" style="grid-template-columns:1fr 1fr 1fr;gap:16px;margin-bottom:24px">
  <div class="card" style="cursor:pointer" onclick="loadReport('penjualan')"><h3>📈 Laporan Penjualan</h3><p>Faktur penjualan per periode</p></div>
  <div class="card" style="cursor:pointer" onclick="loadReport('pembelian')"><h3>📉 Laporan Pembelian</h3><p>Faktur pembelian per periode</p></div>
  <div class="card" style="cursor:pointer" onclick="loadReport('laba_rugi')"><h3>💹 Laba Rugi</h3><p>Pendapatan vs Beban</p></div>
  <div class="card" style="cursor:pointer" onclick="loadReport('piutang')"><h3>💰 Aging Piutang</h3><p>Umur piutang pelanggan</p></div>
  <div class="card" style="cursor:pointer" onclick="loadReport('hutang')"><h3>💳 Aging Hutang</h3><p>Umur hutang vendor</p></div>
  <div class="card" style="cursor:pointer" onclick="loadReport('buku_besar')"><h3>📒 Buku Besar</h3><p>Mutasi per akun</p></div>
 </div>
 <div class="card" id="reportOutput">
  <h3>Pilih laporan di atas untuk menampilkan hasil</h3>
  <div class="empty-state"><div class="icon">📊</div><p>Klik salah satu kartu laporan</p></div>
 </div>`;
 
 // Store period selectors globally for report functions
 window._reportPeriod={month:curMonth,year:curYear};
 }
 if(cur==="Master"){
  let users=[],logs=[];
  const stk=await api("/api/stock");
  window._stkCache=stk;
  const valOf=c=>stk.filter(s=>s.item_code===c).reduce((a,s)=>a+s.value,0);
  const methOf=c=>{const s=stk.find(s=>s.item_code===c);return s?s.method:"AVERAGE";};
  if(ME.role!=="KASIR"){try{logs=await api("/api/activity");}catch(e){}
   if(ME.role==="ADMIN"){try{users=await api("/api/users");}catch(e){}}}

  if(curDetail==="customer")return A.innerHTML=renderCustomerDetail(curDetailId);
  if(curDetail==="vendor")return A.innerHTML=renderVendorDetail(curDetailId);
  if(curDetail==="item")return A.innerHTML=renderItemDetail(curDetailId);

  if(curSub==="Keuangan"){
   A.innerHTML=`<div class="card"><h3>Chart of Accounts (5-digit)</h3>${searchBar("Cari akun...","render()")}<table>${filterRows(COA,searchQ).map(c=>`<tr><td>${c.account_code}</td><td>${c.account_name}</td><td>${c.account_type}</td></tr>`).join("")}</table>
   <div class="row">Kode <input id="c_c" value="63002"> Nama <input id="c_n" value="Beban Iklan"> <select id="c_t"><option>EXPENSE</option><option>ASSET</option><option>LIABILITY</option><option>EQUITY</option><option>REVENUE</option><option>COGS</option></select>
   <button class="go" onclick="saveCOA()">Tambah Akun</button></div></div>
   <div class="card"><h3>Master Tarif Pajak (PPN)</h3><div id="tax_list">Memuat…</div>
   <div class="row">Kode <input id="tx_c" value="PPN12" style="width:80px"> Nama <input id="tx_n" value="PPN 12%"> Tarif% <input id="tx_r" value="12" style="width:60px">
   <button class="go" onclick="saveTX()">Tambah Pajak</button></div></div>`;
   loadTaxAp();
  }
  else if(curSub==="Pelanggan"){
   A.innerHTML=`<div class="card"><h3>Pelanggan (Customer + Akun Piutang)</h3>${searchBar("Cari pelanggan...","render()")}<table><tr><th>Kode</th><th>Nama</th><th>Email</th><th>Akun Piutang</th><th>Limit</th><th>Termin</th></tr>${filterRows(CUST,searchQ).map(x=>{const a=COA.find(c=>c.id===x.receivable_account_id);return `<tr class="clickable-row" onclick="goDetail('customer',${x.id})"><td>${esc(x.customer_code)}</td><td>${esc(x.customer_name)}</td><td>${esc(x.email||"")}</td><td>${a?esc(a.account_code+" "+a.account_name):""}</td><td>${fmt(x.credit_limit||0)}</td><td>${esc((x.terms||"")+" "+(x.term_days||""))}</td></tr>`;}).join("")}</table>
   <div class="row">Kode <input id="cu_c" value="CUST-002" style="width:90px"> Nama <input id="cu_n" value=""> Email <input id="cu_e" value="" style="width:150px">
   Akun Piutang <select id="cu_a">${COA.filter(c=>c.account_type==="ASSET").map(c=>`<option value="${c.id}"${c.account_code==="12001"?" selected":""}>${c.account_code} ${c.account_name}</option>`).join("")}</select></div>
   <div class="row">Mata Uang ${currSelectHTML("cu_curr","IDR")}</div>
   <div class="row">Limit piutang (0=tak terbatas) <input id="cu_l" value="0" style="width:130px"> Termin <input id="cu_t" value="NET 30" style="width:90px"> Hari <input id="cu_d" value="30" style="width:60px">
   <button class="go" onclick="saveCU()">Tambah</button></div>
   <div class="row">Ubah limit: <select id="cu_id">${CUST.map(x=>`<option value="${x.id}">${x.customer_name}</option>`).join("")}</select>
   Limit <input id="cu_l2" value="0" style="width:130px"> Termin <input id="cu_t2" value="NET 30" style="width:90px"> Hari <input id="cu_d2" value="30" style="width:60px">
   <button class="go" onclick="saveCUL()">Simpan</button></div></div>`;
  }
  else if(curSub==="Vendor"){
   A.innerHTML=`<div class="card"><h3>Pemasok (Vendor + Akun Utang)</h3>${searchBar("Cari vendor...","render()")}<table><tr><th>Kode</th><th>Nama</th><th>Email</th><th>Akun Utang</th><th>Limit</th></tr>${filterRows(VEND,searchQ).map(x=>{const a=COA.find(c=>c.id===x.payable_account_id);return `<tr class="clickable-row" onclick="goDetail('vendor',${x.id})"><td>${x.vendor_code}</td><td>${x.vendor_name}</td><td>${x.email||""}</td><td>${a?a.account_code+" "+a.account_name:""}</td><td>${fmt(x.credit_limit||0)}</td></tr>`;}).join("")}</table>
   <div class="row">Kode <input id="vn_c" value="VEND-002" style="width:90px"> Nama <input id="vn_n" value=""> Email <input id="vn_e" value="" style="width:150px">
   Akun Utang <select id="vn_a">${COA.filter(c=>c.account_type==="LIABILITY").map(c=>`<option value="${c.id}"${c.account_code==="21001"?" selected":""}>${c.account_code} ${c.account_name}</option>`).join("")}</select>
   <div class="row">Mata Uang ${currSelectHTML("vn_curr","IDR")}</div>
   <button class="go" onclick="saveVN()">Tambah</button></div></div>
   <div class="card"><h3>Vendor & Limit Utang (0 = tanpa limit)</h3><table><tr><th>Kode</th><th>Nama</th><th>Limit</th></tr>${VEND.map(v=>`<tr><td>${v.vendor_code}</td><td>${v.vendor_name}</td><td>${fmt(v.credit_limit||0)}</td></tr>`).join("")}</table>
   <div class="row">Vendor <select id="vl_id">${VEND.map(v=>`<option value="${v.id}">${v.vendor_name}</option>`).join("")}</select>
   Limit <input id="vl_amt" value="50000000"><button class="go" onclick="saveVL()">Simpan Limit</button></div></div>`;
  }
  else if(curSub==="Persediaan"){
   A.innerHTML=`<div class="card"><h3>Barang, Satuan & Metode HPP</h3>${searchBar("Cari barang...","render()")}<table><tr><th>Kode</th><th>Nama</th><th>Stok (dasar)</th><th>Satuan</th><th>Metode</th><th>Nilai Stok</th><th></th></tr>${filterRows(ITEMS,searchQ).map(i=>`<tr class="clickable-row" onclick="goDetail('item',${i.id})"><td>${i.item_code}</td><td>${i.item_name}</td><td>${i.stock} ${i.base_unit}</td><td>${(i.units||[]).map(u=>u.unit_code+"×"+u.conversion).join(", ")}</td><td>${methOf(i.item_code)}</td><td>${fmt(valOf(i.item_code))}</td><td>${i.item_type==="INVENTORY"?`<button class="go" onclick="event.stopPropagation();setMethod(${i.id},'${methOf(i.item_code)==="FIFO"?"AVERAGE":"FIFO"}')">jadi ${methOf(i.item_code)==="FIFO"?"AVERAGE":"FIFO"}</button>`:""}</td></tr>`).join("")}</table>
   <div class="row">Barang <select id="u_item">${ITEMS.map(i=>`<option value="${i.id}">${i.item_code}</option>`).join("")}</select>
   Satuan <input id="u_code" value="BOX" style="width:70px"> Isi (konversi) <input id="u_conv" value="10" style="width:80px">
   <button class="go" onclick="saveU()">Tambah Satuan</button></div></div>
   <div class="card"><h3>Gudang & Cabang</h3><table><tr><th>Kode</th><th>Gudang</th><th>Cabang</th></tr>${WH.map(w=>{const b=BR.find(x=>x.id===w.branch_id);return `<tr><td>${w.warehouse_code}</td><td>${w.warehouse_name}</td><td>${b?b.branch_code:""}</td></tr>`;}).join("")}</table>
   <div class="row">Gudang <select id="wb_id">${WH.map(w=>`<option value="${w.id}">${w.warehouse_name}</option>`).join("")}</select>
   Cabang <select id="wb_br">${BR.map(b=>`<option value="${b.id}">${b.branch_code}</option>`).join("")}</select>
   <button class="go" onclick="saveWB()">Set Cabang Gudang</button></div></div>`;
  }
  else if(curSub==="Sales"){
   A.innerHTML=`<div class="card"><h3>Salesman, Komisi & Target</h3>${searchBar("Cari salesman...","render()")}<table><tr><th>Kode</th><th>Nama</th><th>Komisi%</th><th>Target/bln</th></tr>${filterRows(SP,searchQ).map(s=>`<tr><td>${s.sp_code}</td><td>${s.sp_name}</td><td>${s.commission_pct}%</td><td>${fmt(s.monthly_target)}</td></tr>`).join("")}</table>
   <div class="row">Kode <input id="sp_c" value="SP-001" style="width:80px"> Nama <input id="sp_n" value="Budi">
   Komisi% <input id="sp_p" value="3" style="width:60px"> Target <input id="sp_t" value="50000000" style="width:130px">
   <button class="go" onclick="saveSP()">Tambah</button></div></div>`;
  }
  else if(curSub==="Organisasi"){
   A.innerHTML=`<div class="card"><h3>Cabang</h3>${searchBar("Cari cabang...","render()")}<table><tr><th>Kode</th><th>Nama</th><th>Gudang</th></tr>${filterRows(BR,searchQ).map(b=>`<tr><td>${b.branch_code}</td><td>${b.branch_name}</td><td>${b.n_wh}</td></tr>`).join("")}</table>
   <div class="row">Kode <input id="br_c" value="CAB-SBY" style="width:90px"> Nama <input id="br_n" value="Cabang Surabaya">
   <button class="go" onclick="saveBR()">Tambah Cabang</button></div></div>
   <div class="card"><h3>Karyawan</h3><div id="emp_list">Memuat…</div>
   <div class="row">Kode <input id="em_c" value="EMP-002" style="width:90px"> Nama <input id="em_n" value="">
   Jabatan <input id="em_j" value="Staff" style="width:100px"> Gaji <input id="em_g" value="5000000" style="width:120px">
   Kuota cuti <input id="em_q" value="12" style="width:60px"><button class="go" onclick="saveEM()">Tambah</button></div></div>`;
   api("/api/employees").then(e=>{window._emps=e;
    $("#emp_list").innerHTML=`<table><tr><th>Kode</th><th>Nama</th><th>Jabatan</th><th>Gaji</th><th>Sisa cuti</th></tr>${e.map(x=>`<tr><td>${x.emp_code}</td><td>${x.full_name}</td><td>${x.position}</td><td>${fmt(x.base_salary)}</td><td>${x.leave_quota}</td></tr>`).join("")}</table>`;}).catch(e=>{$("#emp_list").textContent=e.message;});
  }
  else if(curSub==="Sistem"){
   A.innerHTML=`${ME.role==="ADMIN"?`<div class="card"><h3>Backup & Restore Database</h3><p class="mut">Unduh file database SQLite (jadwalkan berkala, simpan di tempat aman).</p><div class="row"><a href="/api/backup?token=${tok()}"><button class="go">Unduh Backup</button></a></div>
   <div class="row"><input type="file" id="rs_f" accept=".db"><button class="go" onclick="restore()">Restore dari File</button></div><div id="rs_out" class="mut"></div></div>
   <div class="card"><h3>User & Peran</h3><table><tr><th>Username</th><th>Nama</th><th>Peran</th><th>Aktif</th></tr>${users.map(u=>`<tr><td>${u.username}</td><td>${u.full_name}</td><td>${u.role}</td><td>${u.is_active?"Ya":"Tidak"}</td></tr>`).join("")}</table>
   <div class="row">Username <input id="nu_u" value=""> Password <input id="nu_p" value=""> Nama <input id="nu_n" value="">
   Peran <select id="nu_r"><option>KASIR</option><option>GUDANG</option><option>HRD</option><option>FINANCE</option><option>MANAGER</option><option>ADMIN</option></select>
   <button class="go" onclick="saveNU()">Tambah User</button></div></div>
   <div class="card" style="cursor:pointer" onclick="loadSistem('currency')"><h3>💱 Mata Uang</h3><p>Konfigurasi mata uang & kurs</p></div>`:""}
   ${ME.role!=="KASIR"?`<div class="card"><h3>Log Aktivitas</h3><table><tr><th>Waktu</th><th>User</th><th>Aksi</th></tr>${logs.slice(0,50).map(l=>`<tr><td>${esc(l.created_at||"")}</td><td>${esc(l.username)}</td><td>${esc(l.action)}</td></tr>`).join("")}</table></div>`:""}`;
  }
  else{
   A.innerHTML=`<div class="card"><h3>Master Data</h3><p class="mut">Pilih sub-menu di panel kiri untuk mengelola data master.</p></div>`;
  }
 }
 if(cur==="AI & Integrasi"){
  const w=await api("/api/webhooks");
  A.innerHTML=`<div class="card"><h3>📸 OCR Struk → Draft Jurnal (Next-Gen)</h3>
  <p class="mut">Pilih foto/PDF struk (simulasi baca otomatis di browser), lalu buat draft jurnal tanpa ketik manual.</p>
  <div class="row"><input type="file" id="ocr_f"><button class="go" onclick="ocr()">Baca & Buat Draft</button></div><div id="ocr_out"></div></div>
  <div class="card"><h3>🔗 Webhook / API Builder (WA, E-commerce)</h3>
  <div class="row"><input id="w_e" value="sales.created" style="width:140px"><input id="w_u" value="https://wa.me/62812xxxx?text=invoice" style="width:300px"><button class="go" onclick="saveW()">Tambah</button></div>
  <pre>${JSON.stringify(w,null,1).slice(0,3000)}</pre></div>`;
 }
 if(cur==="HRD"){
  A.innerHTML=`<div class="card"><h3>👥 Karyawan</h3><div id="emp_list">Memuat…</div>
  <div class="row">Kode <input id="em_c" value="EMP-002" style="width:90px"> Nama <input id="em_n" value="">
  Jabatan <input id="em_j" value="Staff" style="width:100px"> Gaji <input id="em_g" value="5000000" style="width:120px">
  Kuota cuti <input id="em_q" value="12" style="width:60px"><button class="go" onclick="saveEM()">Tambah</button></div></div>
  <div class="card"><h3>🌴 Cuti (pengajuan + approval)</h3>
  <div class="row">Karyawan <select id="lv_emp"></select> Dari <input type="date" id="lv_f" value="${today()}">
  Sampai <input type="date" id="lv_t" value="${today()}"> Alasan <input id="lv_r" value="">
  <button class="go" onclick="saveLV()">Ajukan</button></div><div id="lv_list">Memuat…</div></div>
  <div class="card"><h3>📊 Rekap Kehadiran</h3>
  <div class="row">Bulan <input type="month" id="rc_m" value="${today().slice(0,7)}"><button class="go" onclick="loadRecap()">Tampilkan</button></div><div id="rc_out"></div></div>
  <div class="card"><h3>💰 Penggajian + PPh 21</h3>
  <div class="row">Nama <input id="pr_n" value="Andi"> Tgl <input type="date" id="pr_d" value="${today()}">
  Bruto <input id="pr_g" value="10000000"> PPh21 (isi sesuai hitungan pajak) <input id="pr_p" value="500000">
  <button class="go" onclick="savePR()">Posting Gaji (Dr Beban / Cr PPh21+Utang Gaji)</button></div><div id="pr_out"></div></div>
  <div class="card"><h3>Riwayat Gaji</h3><div id="pr_hist">Memuat…</div></div>`;
  api("/api/payroll").then(h=>{$("#pr_hist").innerHTML=`<table><tr><th>Tgl</th><th>Nama</th><th>Bruto</th><th>PPh21</th><th>Bersih</th><th>Oleh</th></tr>${h.map(x=>`<tr><td>${x.transaction_date}</td><td>${x.employee_name}</td><td>${fmt(x.gross)}</td><td>${fmt(x.pph21)}</td><td>${fmt(x.net)}</td><td>${x.created_by}</td></tr>`).join("")}</table>`;}).catch(e=>{$("#pr_hist").textContent=e.message;});
  api("/api/employees").then(e=>{window._emps=e;
   $("#emp_list").innerHTML=`<table><tr><th>Kode</th><th>Nama</th><th>Jabatan</th><th>Gaji</th><th>Sisa cuti</th></tr>${e.map(x=>`<tr><td>${x.emp_code}</td><td>${x.full_name}</td><td>${x.position}</td><td>${fmt(x.base_salary)}</td><td>${x.leave_quota}</td></tr>`).join("")}</table>`;
   $("#lv_emp").innerHTML=e.filter(x=>x.is_active).map(x=>`<option value="${x.id}">${x.full_name}</option>`).join("");}).catch(e=>{$("#emp_list").textContent=e.message;});
  api("/api/leaves").then(l=>{$("#lv_list").innerHTML=`<table><tr><th>Karyawan</th><th>Dari</th><th>Sampai</th><th>Hari</th><th>Alasan</th><th>Status</th><th></th></tr>${l.map(x=>`<tr><td>${x.full_name}</td><td>${x.date_from}</td><td>${x.date_to}</td><td>${x.days}</td><td>${x.reason}</td><td>${st(x.status)}</td><td>${x.status==="PENDING"?`<button class="go ok" onclick="decLV(${x.id},1)">Setujui</button> <button class="go danger" onclick="decLV(${x.id},0)">Tolak</button>`:""}</td></tr>`).join("")}</table>`;}).catch(e=>{$("#lv_list").textContent=e.message;});
 }
 }catch(e){A.innerHTML=`<div class="card">❌ ${e.message}</div>`;}
}
window.unitCh=pref=>{const it=ITEMS.find(i=>i.id==$("#"+pref+"_item").value);const us=(it&&it.units)||[{unit_code:"PCS",conversion:1}];
 $("#"+pref+"_unit").innerHTML=us.map(u=>`<option value="${u.unit_code}|${u.conversion}">${u.unit_code} (isi ${u.conversion})</option>`).join("");};
window.addJ=()=>{_jl.push({account_id:+$("#j_a").value,debit:+$("#j_db").value,credit:+$("#j_cr").value});$("#jlines").innerHTML=_jl.map(x=>`<div>${x.account_id} D${x.debit} K${x.credit}</div>`).join("");};
window.saveSale=async()=>{
 const tiv=+($("#ti_val")?$("#ti_val").value:0)||0;
 const lines=gridLines('sg').concat(_sl);
 if(!lines.length)return alert("Isi minimal 1 baris");
 try{showLoading("#app button.go","Menyimpan...");
 const body={customer_id:+$("#s_cust").value,warehouse_id:+$("#s_wh").value,date:$("#s_date").value,tax_rate:+$("#s_tax").value,lines};
 if($("#s_sp").value)body.salesperson_id=+$("#s_sp").value;
 if(tiv>0)body.trade_in={item_id:+$("#ti_item").value,qty:+$("#ti_qty").value,value:tiv,note:$("#ti_note").value,warehouse_id:+$("#s_wh").value};
 const r=await api("/api/sales",{method:"POST",body:JSON.stringify(body)});
 alert("Tersimpan "+r.invoice+" "+fmt(r.total)+" (piutang "+fmt(r.receivable)+", komisi "+fmt(r.commission)+")");render();}catch(e){alert(e.message)}finally{hideLoading("#app button.go");}};
window.saveSP=async()=>{try{await api("/api/salespersons",{method:"POST",body:JSON.stringify({sp_code:$("#sp_c").value,sp_name:$("#sp_n").value,commission_pct:+$("#sp_p").value,monthly_target:+$("#sp_t").value})});loadM().then(render);}catch(e){alert(e.message)}};
window.loadTargets=async()=>{try{const t=await api("/api/targets?month="+$("#tg_m").value);
 $("#tg_out").innerHTML=`<table><tr><th>Salesman</th><th>Komisi%</th><th>Target</th><th>Realisasi</th><th>Trx</th><th>%</th><th>Komisi Terutang</th></tr>${t.rows.map(r=>`<tr><td>${r.sp_name}</td><td>${r.commission_pct}%</td><td>${fmt(r.target)}</td><td>${fmt(r.realisasi)}</td><td>${r.transaksi}</td><td>${r.pencapaian}%</td><td>${fmt(r.komisi)}</td></tr>`).join("")}</table>`;}catch(e){alert(e.message)}};
window.savePR=async()=>{try{const r=await api("/api/payroll",{method:"POST",body:JSON.stringify({date:$("#pr_d").value,employee_name:$("#pr_n").value,gross:+$("#pr_g").value,pph21:+$("#pr_p").value})});alert("Gaji terposting, bersih "+fmt(r.net));render();}catch(e){alert(e.message)}};
window.saveBuy=async()=>{
 try{const lines=gridLines('pg').concat(_pl);if(!lines.length)return alert("Isi minimal 1 baris");
 showLoading("#app button.go","Menyimpan...");
 const r=await api("/api/purchases",{method:"POST",body:JSON.stringify({vendor_id:+$("#p_vend").value,warehouse_id:+$("#p_wh").value,date:$("#p_date").value,tax_rate:+$("#p_tax").value,lines})});
 alert("Tersimpan "+r.invoice);loadM().then(render);}catch(e){alert(e.message)}finally{hideLoading("#app button.go");}};
window.saveT=async()=>{try{await api("/api/transfers",{method:"POST",body:JSON.stringify({from_account:+$("#t_from").value,to_account:+$("#t_to").value,amount:+$("#t_amt").value,date:$("#t_date").value,note:$("#t_note").value})});alert("Transfer tercatat");render();}catch(e){alert(e.message)}};
window.saveRS=async()=>{try{const r=await api("/api/sales/returns",{method:"POST",body:JSON.stringify({sales_invoice_id:+$("#rs_inv").value,warehouse_id:+$("#rs_wh").value,date:$("#rs_date").value,lines:[{item_id:+$("#rs_item").value,qty:+$("#rs_qty").value}]})});alert("Retur "+r.return+" "+fmt(r.total));loadM().then(render);}catch(e){alert(e.message)}};
window.saveRP=async()=>{try{const r=await api("/api/purchases/returns",{method:"POST",body:JSON.stringify({purchase_invoice_id:+$("#rp_inv").value,warehouse_id:+$("#rp_wh").value,date:$("#rp_date").value,lines:[{item_id:+$("#rp_item").value,qty:+$("#rp_qty").value}]})});alert("Retur "+r.return+" "+fmt(r.total));loadM().then(render);}catch(e){alert(e.message)}};
window.saveVL=async()=>{await api("/api/vendors/limit",{method:"POST",body:JSON.stringify({id:+$("#vl_id").value,credit_limit:+$("#vl_amt").value})});loadM().then(render);};
window.dpKind=async()=>{try{const k=$("#dp_kind").value;const cs=k==="AR"?CUST:VEND;const nm=k==="AR"?"customer_name":"vendor_name";
 $("#dp_c").innerHTML=cs.map(c=>`<option value="${c.id}">${c[nm]}</option>`).join("");
 const dps=await api(k==="AR"?"/api/sales-dp":"/api/purchase-dp");
 const open=dps.filter(d=>d.status!=="CLOSED");
 $("#dpa_dp").innerHTML=open.map(d=>`<option value="${d.id}">${d.dp_number} (sisa ${fmt(d.amount-d.allocated)})</option>`).join("")||"<option value=''>-</option>";
 const invs=(k==="AR"?await api("/api/sales"):await api("/api/purchases")).filter(x=>x.status!=="VOID"&&x.outstanding>0.005);
 $("#dpa_inv").innerHTML=invs.map(x=>`<option value="${x.id}">${x.invoice_number} (sisa ${fmt(x.outstanding)})</option>`).join("")||"<option value=''>-</option>";
 $("#dp_list").innerHTML=`<table><tr><th>No</th><th>Tgl</th><th>Nilai</th><th>Terpakai</th><th>Status</th></tr>${dps.map(d=>`<tr><td>${d.dp_number}</td><td>${d.transaction_date}</td><td>${fmt(d.amount)}</td><td>${fmt(d.allocated)}</td><td>${st(d.status)}</td></tr>`).join("")}</table>`;}catch(e){$("#dp_list").textContent=e.message;}};
window.dpInit=()=>{dpKind();};
window.saveDP=async()=>{try{const k=$("#dp_kind").value;const key=k==="AR"?"customer_id":"vendor_id";
 const body={cash_account_id:+$("#dp_cash").value,amount:+$("#dp_amt").value,date:$("#dp_date").value};body[key]=+$("#dp_c").value;
 const r=await api(k==="AR"?"/api/sales-dp":"/api/purchase-dp",{method:"POST",body:JSON.stringify(body)});alert("DP "+r.dp);render();}catch(e){alert(e.message)}};
window.allocDP=async()=>{try{const k=$("#dp_kind").value;
 await api(k==="AR"?"/api/sales-dp/allocate":"/api/purchase-dp/allocate",{method:"POST",body:JSON.stringify({dp_id:+$("#dpa_dp").value,invoice_id:+$("#dpa_inv").value,amount:+$("#dpa_amt").value,date:today()})});alert("Dialokasikan");render();}catch(e){alert(e.message)}};
window.giroKind=async()=>{try{const k=$("#g_kind").value;const cs=k==="AR"?CUST:VEND;const nm=k==="AR"?"customer_name":"vendor_name";
 $("#g_c").innerHTML=cs.map(c=>`<option value="${c.id}">${c[nm]}</option>`).join("");
 const invs=(k==="AR"?await api("/api/sales"):await api("/api/purchases")).filter(x=>x.status!=="VOID"&&x.outstanding>0.005);
 $("#g_inv").innerHTML=invs.map(x=>`<option value="${x.id}">${x.invoice_number} (sisa ${fmt(x.outstanding)})</option>`).join("")||"<option value=''>-</option>";
 const gs=(await api("/api/giros")).filter(g=>g.kind===k);
 $("#giro_list").innerHTML=`<div class="row">Kas pencairan ${bankSel("g_cash")}</div><table><tr><th>No</th><th>Giro</th><th>Kontak</th><th>Jth tempo</th><th>Nilai</th><th>Status</th><th></th></tr>${gs.map(g=>`<tr><td>${g.giro_number}</td><td>${g.giro_no} ${g.bank_name}</td><td>${g.contact_name}</td><td>${g.due_date}</td><td>${fmt(g.amount)}</td><td>${st(g.status)}</td><td>${g.status==="POSTED"?`<button class="go ok" onclick="giroClear(${g.id})">Cair</button> <button class="go danger" onclick="giroReject(${g.id})">Tolak</button>`:""}</td></tr>`).join("")}</table>`;}catch(e){$("#giro_list").textContent=e.message;}};
window.giroInit=()=>{window._gal=[];giroKind();};
window.addGiroAlloc=()=>{const id=+$("#g_inv").value;if(!id)return alert("Tidak ada invoice");_gal.push({invoice_id:id,amount:+$("#g_amt").value,invoice_type:$("#g_kind").value});
 $("#galocs").innerHTML=_gal.map(a=>`<div>#${a.invoice_id} — ${fmt(a.amount)}</div>`).join("")+`<b>Total: ${fmt(_gal.reduce((a,x)=>a+x.amount,0))}</b>`;};
window.saveGiro=async()=>{try{await api("/api/giros",{method:"POST",body:JSON.stringify({kind:$("#g_kind").value,contact_id:+$("#g_c").value,giro_no:$("#g_no").value,bank_name:$("#g_bank").value,issue_date:$("#g_issue").value,due_date:$("#g_due").value,allocations:_gal})});alert("Giro tercatat");render();}catch(e){alert(e.message)}};
window.giroClear=async id=>{try{await api("/api/giros/clear",{method:"POST",body:JSON.stringify({id,cash_account_id:+$("#g_cash").value,date:today()})});render();}catch(e){alert(e.message)}};
window.giroReject=async id=>{if(!confirm("Tolak giro ini? Piutang/utang kembali."))return;try{await api("/api/giros/reject",{method:"POST",body:JSON.stringify({id,date:today()})});render();}catch(e){alert(e.message)}};
window.closeYear=async()=>{const y=$("#pe_y").value;if(!confirm(`Tutup buku tahun ${y}? Jurnal penutup dibuat & periode dikunci permanen.`))return;try{const r=await api("/api/period-end",{method:"POST",body:JSON.stringify({year:y})});alert("Laba bersih "+fmt(r.net_income)+". Periode dikunci.");render();}catch(e){alert(e.message)}};
window.saveCU=async()=>{
 try{if(!$("#cu_n").value.trim())return alert("Nama pelanggan wajib diisi!");
 showLoading("#app button.go","Menyimpan...");
 await api("/api/customers",{method:"POST",body:JSON.stringify({customer_code:$("#cu_c").value,customer_name:$("#cu_n").value,email:$("#cu_e").value,receivable_account_id:+$("#cu_a").value,currency_code:$("#cu_curr").value})});
 const cu=CUST.find(x=>x.customer_code===$("#cu_c").value);
 if(cu)await api("/api/customers/limit",{method:"POST",body:JSON.stringify({id:cu.id,credit_limit:+$("#cu_l").value,terms:$("#cu_t").value,term_days:+$("#cu_d").value})});
 loadM().then(render);}catch(e){alert(e.message)}finally{hideLoading("#app button.go");}};
window.saveCUL=async()=>{try{await api("/api/customers/limit",{method:"POST",body:JSON.stringify({id:+$("#cu_id").value,credit_limit:+$("#cu_l2").value,terms:$("#cu_t2").value,term_days:+$("#cu_d2").value})});loadM().then(render);}catch(e){alert(e.message)}};
window.saveVN=async()=>{
 try{if(!$("#vn_n").value.trim())return alert("Nama vendor wajib diisi!");
 showLoading("#app button.go","Menyimpan...");
 await api("/api/vendors",{method:"POST",body:JSON.stringify({vendor_code:$("#vn_c").value,vendor_name:$("#vn_n").value,email:$("#vn_e").value,payable_account_id:+$("#vn_a").value,currency_code:$("#vn_curr").value})});
 loadM().then(render);}catch(e){alert(e.message)}finally{hideLoading("#app button.go");}};
window.closeDoc=async(url,id)=>{try{await api(url,{method:"POST",body:JSON.stringify({id})});render();}catch(e){alert(e.message)}};
window.addQ=()=>{const id=+$("#q_item").value;const[uc,cv]=$("#q_unit").value.split("|");_ql.push({item_id:id,qty:+$("#q_qty").value,price:+$("#q_price").value,description:$("#q_desc").value,unit_code:uc,unit_conv:+cv});$("#qlines").innerHTML=_ql.map(x=>`<div>${x.qty} ${x.unit_code} item#${x.item_id} ${x.description||""}</div>`).join("");};
window.saveQ=async()=>{
 try{showLoading("#app button.go","Menyimpan...");
 const r=await api("/api/quotations",{method:"POST",body:JSON.stringify({customer_id:+$("#q_cust").value,date:$("#q_date").value,tax_rate:+$("#q_tax").value,lines:_ql})});
 alert("Penawaran "+r.quotation);render();}catch(e){alert(e.message)}finally{hideLoading("#app button.go");}};
window.copySQ=()=>{const q=_sq.find(x=>x.id==$("#o_sq").value);if(!q)return;await_api_copy(q);};
async function await_api_copy(q){const full=(await api("/api/quotations")).find(x=>x.id===q.id);full.lines.forEach(l=>gridAdd('oo',{item_id:l.item_id,wh:l.warehouse_id,qty:l.unit_qty||l.quantity,price:l.unit_price,d1:l.discount_pct||0,d2:l.discount_pct2||0,unit:(l.unit_code||"PCS")+"|"+(l.unit_conv||1)}));$("#o_sq").value="";}
window.saveO=async()=>{
 try{const b={customer_id:+$("#o_cust").value,date:$("#o_date").value,tax_rate:+$("#o_tax").value,lines:gridLines('oo')};
 if(!b.lines.length)return alert("Isi minimal 1 baris");
 showLoading("#app button.go","Menyimpan...");
 if($("#o_sq").value)b.quotation_id=+$("#o_sq").value;
 const r=await api("/api/sales-orders",{method:"POST",body:JSON.stringify(b)});
 alert("SO "+r.order);render();}catch(e){alert(e.message)}finally{hideLoading("#app button.go");}};
window.doLines=()=>{const s=_so.find(x=>x.id==$("#d_so").value);if(!s){$("#dref").innerHTML="";return;}
 $("#dref").innerHTML=`<table><tr><th>Barang</th><th>Deskripsi</th><th>Sisa</th><th>Gudang</th><th>Qty kirim</th><th></th></tr>${s.lines.map(l=>`<tr><td>${l.item_name}</td><td>${l.description||""}</td><td>${l.quantity-l.delivered}</td><td><select id="dw_${l.id}">${WH.map(w=>`<option value="${w.id}">${w.warehouse_name}</option>`).join("")}</select></td><td><input id="dq_${l.id}" value="${l.quantity-l.delivered}" style="width:70px"></td><td><button class="go" onclick="addDRef(${l.id})">+</button></td></tr>`).join("")}</table>`;};
window.addDRef=solId=>{const s=_so.find(x=>x.id==$("#d_so").value);const l=s.lines.find(x=>x.id===solId);_dl.push({sales_order_line_id:solId,item_id:l.item_id,warehouse_id:+$("#dw_"+solId).value,qty:+$("#dq_"+solId).value,description:l.description||""});$("#dlines").innerHTML=_dl.map(x=>`<div>SO#${x.sales_order_line_id} ${x.qty} item#${x.item_id}</div>`).join("");};
window.addD=()=>{const[uc,cv]=$("#d_unit").value.split("|");_dl.push({item_id:+$("#d_item").value,warehouse_id:+$("#d_wh").value,qty:+$("#d_qty").value,unit_code:uc,unit_conv:+cv,description:$("#d_desc").value});$("#dlines").innerHTML=_dl.map(x=>`<div>${x.qty} item#${x.item_id}</div>`).join("");};
window.saveD=async()=>{
 try{const b={customer_id:+$("#d_cust").value,date:$("#d_date").value,lines:_dl};
 showLoading("#app button.go","Menyimpan...");
 if($("#d_so").value)b.sales_order_id=+$("#d_so").value;
 const r=await api("/api/deliveries",{method:"POST",body:JSON.stringify(b)});
 alert("DO "+r.delivery);render();}catch(e){alert(e.message)}finally{hideLoading("#app button.go");}};
window.voidD=async id=>{if(!confirm("Void surat jalan ini? Stok kembali & jurnal dibalik."))return;try{await api("/api/deliveries/void",{method:"POST",body:JSON.stringify({id,date:today()})});render();}catch(e){alert(e.message)}};
window.siDO=()=>{const d=_dn.find(x=>x.id==$("#s_do").value);if(!d){$("#sref").innerHTML="";return;}
 api("/api/deliveries").then(all=>{const full=all.find(x=>x.id===d.id);
 $("#sref").innerHTML=`<table><tr><th>Barang</th><th>Sisa tagih</th><th>Qty</th><th></th></tr>${full.lines.map(l=>`<tr><td>${l.item_name}</td><td>${l.quantity-l.invoiced_qty}</td><td><input id="sdo_${l.id}" value="${l.quantity-l.invoiced_qty}" style="width:70px"></td><td><button class="go" onclick="addDORef(${l.id})">+</button></td></tr>`).join("")}</table>`;});};
window.addDORef=dlId=>{_sl.push({delivery_line_id:dlId,qty:+$("#sdo_"+dlId).value});$("#slines").innerHTML=_sl.map(x=>`<div>${x.delivery_line_id?"DO#"+x.delivery_line_id+" ":""}${x.qty||""} ${x.item_id?"item#"+x.item_id:""}</div>`).join("");};
window.siSO=()=>{const s=_so2.find(x=>x.id==$("#s_so").value);if(!s){if(!$("#s_do").value)$("#sref").innerHTML="";return;}
 $("#sref").innerHTML=`<table><tr><th>Barang</th><th>Sisa</th><th>Qty</th><th></th></tr>${s.lines.map(l=>`<tr><td>${l.item_name}</td><td>${l.quantity-l.delivered}</td><td><input id="sso_${l.id}" value="${l.quantity-l.delivered}" style="width:70px"></td><td><button class="go" onclick="addSORef(${l.id})">+</button></td></tr>`).join("")}</table>`;};
window.addSORef=solId=>{const s=_so2.find(x=>x.id==$("#s_so").value);const l=s.lines.find(x=>x.id===solId);_sl.push({sales_order_line_id:solId,item_id:l.item_id,qty:+$("#sso_"+solId).value,price:l.unit_price});$("#slines").innerHTML=_sl.map(x=>`<div>${x.sales_order_line_id?"SO#"+x.sales_order_line_id+" ":""}${x.qty||""} ${x.item_id?"item#"+x.item_id:""}</div>`).join("");};
window.addR=()=>{_rl.push({item_id:+$("#r_item").value,qty:+$("#r_qty").value,price:+$("#r_price").value,description:$("#r_desc").value});$("#rlines").innerHTML=_rl.map(x=>`<div>${x.qty} item#${x.item_id}</div>`).join("");};
window.saveR=async()=>{try{const b={date:$("#r_date").value,requester:$("#r_req").value,lines:_rl};if($("#r_vend").value)b.vendor_id=+$("#r_vend").value;await api("/api/requisitions",{method:"POST",body:JSON.stringify(b)});alert("PR tersimpan");render();}catch(e){alert(e.message)}};
window.copyPR=async()=>{const id=$("#o_pr").value;if(!id)return;const full=(await api("/api/requisitions")).find(x=>x.id==+id);full.lines.forEach(l=>gridAdd('og',{item_id:l.item_id,wh:WH[0].id,qty:l.unit_qty||l.quantity,price:l.est_price}));$("#o_pr").value="";};
window.saveO2=async()=>{
 try{const lines=gridLines('og');if(!lines.length)return alert("Isi minimal 1 baris");
 showLoading("#app button.go","Menyimpan...");
 const b={vendor_id:+$("#o_vend").value,date:$("#o_date").value,tax_rate:+$("#o_tax").value,lines};
 if($("#o_pr").value)b.requisition_id=+$("#o_pr").value;
 const r=await api("/api/purchase-orders",{method:"POST",body:JSON.stringify(b)});
 alert("PO "+r.order);render();}catch(e){alert(e.message)}finally{hideLoading("#app button.go");}};
window.riLines=()=>{const p=_po.find(x=>x.id==$("#v_po").value);if(!p){$("#vref").innerHTML="";return;}
 $("#vref").innerHTML=`<table><tr><th>Barang</th><th>Sisa</th><th>Qty terima</th><th></th></tr>${p.lines.map(l=>`<tr><td>${l.item_name}</td><td>${l.quantity-l.received}</td><td><input id="vq_${l.id}" value="${l.quantity-l.received}" style="width:70px"></td><td><button class="go" onclick="addVRef(${l.id})">+</button></td></tr>`).join("")}</table>`;};
window.addVRef=polId=>{const p=_po.find(x=>x.id==$("#v_po").value);const l=p.lines.find(x=>x.id===polId);_vl.push({purchase_order_line_id:polId,item_id:l.item_id,warehouse_id:l.warehouse_id,qty:+$("#vq_"+polId).value,price:Math.round(l.unit_price/(l.unit_conv||1))});$("#vlines").innerHTML=_vl.map(x=>`<div>PO#${x.purchase_order_line_id||""} ${x.qty} item#${x.item_id}</div>`).join("");};
window.addV=()=>{const[uc,cv]=$("#v_unit").value.split("|");_vl.push({item_id:+$("#v_item").value,warehouse_id:+$("#v_wh").value,qty:+$("#v_qty").value,price:+$("#v_price").value,unit_code:uc,unit_conv:+cv,description:$("#v_desc").value});$("#vlines").innerHTML=_vl.map(x=>`<div>${x.qty} item#${x.item_id}</div>`).join("");};
window.saveV=async()=>{
 try{const b={vendor_id:+$("#v_vend").value,date:$("#v_date").value,lines:_vl};
 showLoading("#app button.go","Menyimpan...");
 if($("#v_po").value)b.purchase_order_id=+$("#v_po").value;
 const r=await api("/api/receives",{method:"POST",body:JSON.stringify(b)});
 alert("Receive "+r.receive);render();}catch(e){alert(e.message)}finally{hideLoading("#app button.go");}};
window.voidR=async id=>{if(!confirm("Void penerimaan ini? Stok dikurangi & jurnal dibalik."))return;try{await api("/api/receives/void",{method:"POST",body:JSON.stringify({id,date:today()})});render();}catch(e){alert(e.message)}};
window.piRI=()=>{const r=_ri.find(x=>x.id==$("#p_ri").value);if(!r){if(!$("#p_po").value)$("#pref").innerHTML="";return;}
 api("/api/receives").then(all=>{const full=all.find(x=>x.id===r.id);
 $("#pref").innerHTML=`<table><tr><th>Barang</th><th>Sisa tagih</th><th>Qty (satuan dasar)</th><th>Harga tagih/satuan dasar</th><th></th></tr>${full.lines.map(l=>`<tr><td>${l.item_name}</td><td>${l.quantity-l.billed_qty}</td><td><input id="pri_${l.id}" value="${l.quantity-l.billed_qty}" style="width:70px"></td><td><input id="prp_${l.id}" value="${Math.round(l.unit_price/(l.unit_conv||1))}" style="width:100px"></td><td><button class="go" onclick="addRIRef(${l.id})">+</button></td></tr>`).join("")}</table>`;});};
window.addRIRef=rlId=>{_pl.push({receive_line_id:rlId,qty:+$("#pri_"+rlId).value,price:+$("#prp_"+rlId).value});$("#plines").innerHTML=_pl.map(x=>`<div>${x.receive_line_id?"RI#"+x.receive_line_id+" ":""}${x.qty} ${x.item_id?"item#"+x.item_id:""}</div>`).join("");};
window.piPO=()=>{const p=_po2.find(x=>x.id==$("#p_po").value);if(!p){if(!$("#p_ri").value)$("#pref").innerHTML="";return;}
 $("#pref").innerHTML=`<table><tr><th>Barang</th><th>Sisa</th><th>Qty</th><th></th></tr>${p.lines.map(l=>`<tr><td>${l.item_name}</td><td>${l.quantity-l.received}</td><td><input id="ppo_${l.id}" value="${l.quantity-l.received}" style="width:70px"></td><td><button class="go" onclick="addPORef(${l.id})">+</button></td></tr>`).join("")}</table>`;};
window.addPORef=polId=>{const p=_po2.find(x=>x.id==$("#p_po").value);const l=p.lines.find(x=>x.id===polId);_pl.push({purchase_order_line_id:polId,item_id:l.item_id,warehouse_id:l.warehouse_id,qty:+$("#ppo_"+polId).value,price:Math.round(l.unit_price/(l.unit_conv||1))});$("#plines").innerHTML=_pl.map(x=>`<div>${x.purchase_order_line_id?"PO#"+x.purchase_order_line_id+" ":""}${x.qty} item#${x.item_id}</div>`).join("");};
window.att=(action)=>{const done=(lat,lng)=>{api("/api/attendance",{method:"POST",body:JSON.stringify({employee_id:+$("#ab_emp").value,action,lat,lng})}).then(r=>{$("#ab_out").textContent=(action==="in"?"Masuk ":"Pulang ")+r.time+(r.late?" — TERLAMBAT":"");}).catch(e=>{$("#ab_out").textContent=e.message;});};
 if(navigator.geolocation)navigator.geolocation.getCurrentPosition(p=>done(p.coords.latitude,p.coords.longitude),()=>done(null,null),{timeout:5000});
 else done(null,null);};
window.saveEM=async()=>{try{await api("/api/employees",{method:"POST",body:JSON.stringify({emp_code:$("#em_c").value,full_name:$("#em_n").value,position:$("#em_j").value,base_salary:+$("#em_g").value,leave_quota:+$("#em_q").value})});render();}catch(e){alert(e.message)}};
window.saveLV=async()=>{try{const r=await api("/api/leaves",{method:"POST",body:JSON.stringify({employee_id:+$("#lv_emp").value,date_from:$("#lv_f").value,date_to:$("#lv_t").value,reason:$("#lv_r").value})});alert("Diajukan "+r.days+" hari");render();}catch(e){alert(e.message)}};
window.decLV=async(id,ok)=>{try{await api("/api/leaves/decide",{method:"POST",body:JSON.stringify({id,approve:!!ok})});render();}catch(e){alert(e.message)}};
window.loadRecap=async()=>{try{const t=await api("/api/attendance/summary?month="+$("#rc_m").value);
 $("#rc_out").innerHTML=`<table><tr><th>Karyawan</th><th>Hadir</th><th>Telat</th><th>Cuti</th><th>Alpa</th><th>Hari kerja</th></tr>${t.rows.map(r=>`<tr><td>${r.employee}</td><td>${r.hadir}</td><td>${r.telat}</td><td>${r.cuti}</td><td>${r.alpa}</td><td>${r.workdays}</td></tr>`).join("")}</table>`;}catch(e){alert(e.message)}};
window.saveBR=async()=>{try{await api("/api/branches",{method:"POST",body:JSON.stringify({branch_code:$("#br_c").value,branch_name:$("#br_n").value})});loadM().then(render);}catch(e){alert(e.message)}};
window.loadPPN=async()=>{try{const t=await api("/api/reports/ppn?month="+$("#ppn_m").value);
 $("#ppn_out").innerHTML=`<table><tr><th>PPN Keluaran</th><th>PPN Masukan</th><th>Selisih</th><th>Status</th></tr><tr><td>${fmt(t.keluaran)}</td><td>${fmt(t.masukan)}</td><td>${fmt(t.selisih)}</td><td><b>${t.status}</b></td></tr></table>
 <details><summary class="mut">Rincian (${t.detail.length})</summary><table><tr><th>Tgl</th><th>Jurnal</th><th>Ket</th><th>Akun</th><th>D</th><th>K</th></tr>${t.detail.map(d=>`<tr><td>${d.transaction_date}</td><td>${d.journal_number}</td><td>${d.description}</td><td>${d.account_code}</td><td>${fmt(d.debit)}</td><td>${fmt(d.credit)}</td></tr>`).join("")}</table></details>`;}catch(e){alert(e.message)}};
window.restore=async()=>{const f=$("#rs_f").files[0];if(!f)return alert("Pilih file .db dulu");
 if(!confirm("Restore akan MENGGANTI seluruh data saat ini dengan isi file. Lanjut?"))return;
 $("#rs_out").textContent="Mengunggah…";
 const buf=await f.arrayBuffer();let bin="";const bytes=new Uint8Array(buf);
 for(let i=0;i<bytes.length;i+=8192)bin+=String.fromCharCode.apply(null,bytes.subarray(i,i+8192));
 try{await api("/api/restore",{method:"POST",body:JSON.stringify({data:btoa(bin)})});
  alert("Restore berhasil. Silakan login ulang.");logout();}catch(e){$("#rs_out").textContent=e.message;}};
window.saveWB=async()=>{try{await api("/api/warehouses/branch",{method:"POST",body:JSON.stringify({id:+$("#wb_id").value,branch_id:+$("#wb_br").value})});loadM().then(render);}catch(e){alert(e.message)}};
window.loadBranch=async()=>{try{const t=await api("/api/reports/branch?month="+$("#br_m").value);
 $("#br_out").innerHTML=`<table><tr><th>Cabang</th><th>Omzet</th><th>Pembelian</th><th>Nilai Stok</th></tr>${t.rows.map(r=>`<tr><td>${r.branch}</td><td>${fmt(r.omzet)}</td><td>${fmt(r.pembelian)}</td><td>${fmt(r.stok)}</td></tr>`).join("")}</table>`;}catch(e){alert(e.message)}};
window.loadRecon=async()=>{try{const r=await api("/api/reconcile?account_id="+$("#rc_acc").value);
 const un=r.statements.filter(s=>s.status==="UNMATCHED"),mt=r.statements.filter(s=>s.status==="MATCHED");
 $("#recon").innerHTML=`<h4>Belum cocok — Koran (${un.length})</h4><table><tr><th>Tgl</th><th>Ket</th><th>Arah</th><th>Nominal</th><th></th></tr>${un.map(s=>`<tr><td>${s.transaction_date}</td><td>${s.description}</td><td>${s.direction}</td><td>${fmt(s.amount)}</td><td><button class="go" onclick="manRecon(${s.id})">Match manual</button></td></tr>`).join("")}</table>
 <h4>Sudah cocok (${mt.length})</h4><table><tr><th>Tgl</th><th>Ket</th><th>Nominal</th><th>Jurnal</th><th></th></tr>${mt.map(s=>`<tr><td>${s.transaction_date}</td><td>${s.description}</td><td>${fmt(s.amount)}</td><td>${s.matched_journal||""}</td><td><button class="go" onclick="unRecon(${s.id})">Batal</button></td></tr>`).join("")}</table>
 <h4>Di sistem, belum ada di koran (${r.unmatched_system.length})</h4><table><tr><th>Tgl</th><th>Jurnal</th><th>Ket</th><th>D</th><th>K</th><th>ID baris</th></tr>${r.unmatched_system.map(l=>`<tr><td>${l.transaction_date}</td><td>${l.journal_number}</td><td>${l.description}</td><td>${fmt(l.debit)}</td><td>${fmt(l.credit)}</td><td>${l.line_id}</td></tr>`).join("")}</table>`;}catch(e){alert(e.message)}};
window.autoRecon=async()=>{try{const r=await api("/api/reconcile/auto",{method:"POST",body:JSON.stringify({account_id:+$("#rc_acc").value})});alert(`Cocok ${r.matched} dari ${r.total}`);loadRecon();}catch(e){alert(e.message)}};
window.saveStmt=async()=>{try{await api("/api/statements",{method:"POST",body:JSON.stringify({bank_account_id:+$("#rc_acc").value,date:$("#rc_d").value,description:$("#rc_desc").value,amount:+$("#rc_amt").value,direction:$("#rc_dir").value})});loadRecon();}catch(e){alert(e.message)}};
window.manRecon=async sid=>{const lid=prompt("Masukkan ID baris jurnal (lihat tabel sistem di bawah):");if(!lid)return;
 try{await api("/api/reconcile/manual",{method:"POST",body:JSON.stringify({statement_id:sid,line_id:+lid})});loadRecon();}catch(e){alert(e.message)}};
window.unRecon=async sid=>{try{await api("/api/reconcile/unmatch",{method:"POST",body:JSON.stringify({statement_id:sid})});loadRecon();}catch(e){alert(e.message)}};
window.printInv=async id=>{try{const inv=(await api("/api/sales")).find(x=>x.id===id);if(!inv)return;
 const w=window.open("","_blank");
 w.document.write(`<html><head><title>${inv.invoice_number}</title><style>body{font-family:Arial;margin:40px}table{width:100%;border-collapse:collapse}td,th{border:1px solid #333;padding:6px;text-align:left}</style></head><body>
 <h2>FAKTUR PENJUALAN</h2><p>No: <b>${inv.invoice_number}</b><br>Tgl: ${inv.transaction_date} | Jatuh tempo: ${inv.due_date}<br>Customer: ${inv.customer_name}${inv.salesperson?" | Sales: "+inv.salesperson:""}<br>Status: ${inv.status}</p>
 <table><tr><th>Barang</th><th>Deskripsi</th><th>Qty</th><th>Harga</th><th>Diskon</th><th>Total</th></tr>${inv.lines.map(l=>`<tr><td>${l.item_name||l.item_id}</td><td>${l.description||""}</td><td>${l.unit_qty||l.quantity} ${l.unit_code||""}</td><td>${fmt(l.unit_price)}</td><td>${fmt(l.discount_amount)}</td><td>${fmt(l.line_total)}</td></tr>`).join("")}</table>
 <p>Subtotal: ${fmt(inv.subtotal)}<br>PPN: ${fmt(inv.tax_amount)}<br><b>Total: ${fmt(inv.total_amount)}</b><br>Dibayar: ${fmt(inv.paid)} | Retur: ${fmt(inv.returned||0)} | Tukar+: ${fmt(inv.tradein_total||0)} | <b>Sisa: ${fmt(inv.outstanding)}</b></p>
 <script>onload=()=>{print();}<\/script></body></html>`);w.document.close();}catch(e){alert(e.message)}};
window.exportInvoicePDF=async id=>{
 try{
  const inv=(await api("/api/sales")).find(x=>x.id===id);
  if(!inv)return alert("Invoice tidak ditemukan");
  const html=`<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Faktur ${esc(inv.invoice_number)}</title>
<style>
 body{font-family:Arial,sans-serif;margin:20px;font-size:12px}
 .header{display:flex;justify-content:space-between;border-bottom:3px solid #1a1a2e;padding-bottom:10px;margin-bottom:20px}
 .title{font-size:24px;font-weight:bold;color:#1a1a2e}
 table{width:100%;border-collapse:collapse;margin:10px 0}
 th,td{padding:8px;border:1px solid #ddd;text-align:left}
 th{background:#f5f5f5;font-weight:bold}
 .total{text-align:right;font-size:14px;margin-top:20px}
 .footer{margin-top:40px;border-top:1px solid #ccc;padding-top:10px;font-size:10px;color:#666}
</style></head><body>
<div class="header">
 <div><div class="title">ERP-MSP</div><div>Sistem Akuntansi Modern</div></div>
 <div style="text-align:right"><div style="font-size:18px;font-weight:bold">FAKTUR PENJUALAN</div>
 <div>${esc(inv.invoice_number)}</div><div>${inv.transaction_date}</div><div>Jatuh Tempo: ${inv.due_date||"-"}</div></div>
</div>
<div style="display:flex;justify-content:space-between;margin-bottom:20px">
 <div><b>Kepada:</b><br>${esc(inv.customer_name)}</div>
 <div><b>Salesman:</b> ${esc(inv.salesperson||"-")}</div>
</div>
<table><thead><tr><th>Barang</th><th>Qty</th><th>Harga</th><th>Diskon</th><th>Total</th></tr></thead>
<tbody>${(inv.lines||[]).map(l=>`<tr><td>${esc(l.item_name||l.description||"")}</td><td>${l.unit_qty||l.quantity}</td><td>${fmt(l.unit_price)}</td><td>${fmt(l.discount_amount||0)}</td><td>${fmt(l.line_total)}</td></tr>`).join("")}</tbody></table>
<div class="total">
 <p>Subtotal: ${fmt(inv.subtotal)}</p>
 <p>PPN: ${fmt(inv.tax_amount)}</p>
 <p><b>TOTAL: ${fmt(inv.total_amount)}</b></p>
 <p>Dibayar: ${fmt(inv.paid)}</p>
 <p><b>Sisa Piutang: ${fmt(inv.outstanding)}</b></p>
</div>
<div class="footer">
 <p>Dicetak: ${new Date().toLocaleString("id-ID")} | ERP-MSP</p>
</div></body></html>`;
  const win=window.open('','_blank');
  win.document.write(html);
  win.document.close();
  win.print();
 }catch(e){alert("Gagal cetak: "+e.message);}
};
window.batchPrintInvoices=async()=>{
 try{
  const sales=await api("/api/sales");
  const open=sales.filter(x=>x.status==='OPEN'||x.status==='PARTIAL');
  if(!open.length)return alert("Tidak ada faktur yang bisa dicetak");
  
  const selected=prompt("Faktur yang akan dicetak (pisah koma, atau 'all' untuk semua):\n"+
   open.map((x,i)=>`${i+1}. ${x.invoice_number} - ${x.customer_name} - Rp${x.total_amount}`).join("\n"));
  if(!selected||selected.trim()==="")return;
  
  let invoices;
  if(selected.toLowerCase()==="all"){
   invoices=open;
  }else{
   const indices=selected.split(",").map(x=>parseInt(x.trim())-1);
   invoices=indices.filter(i=>i>=0&&i<open.length).map(i=>open[i]);
  }
  if(!invoices.length)return alert("Tidak ada faktur dipilih");
  
  let html=`<!DOCTYPE html><html><head><meta charset="utf-8"><title>Batch Print - ERP-MSP</title>
  <style>
   @page{size:A4;margin:15mm}
   body{font-family:Arial,sans-serif;margin:0;padding:0;font-size:11px}
   .page{page-break-after:always;padding:15mm;min-height:250mm}
   .page:last-child{page-break-after:avoid}
   .header{display:flex;justify-content:space-between;border-bottom:3px solid #1a1a2e;padding-bottom:10px;margin-bottom:15px}
   .title{font-size:20px;font-weight:bold;color:#1a1a2e}
   table{width:100%;border-collapse:collapse;margin:8px 0}
   th,td{padding:6px;border:1px solid #ddd;text-align:left;font-size:10px}
   th{background:#f5f5f5;font-weight:bold}
   .total{text-align:right;font-size:12px;margin-top:15px}
   .footer{margin-top:30px;border-top:1px solid #ccc;padding-top:8px;font-size:9px;color:#666}
  </style></head><body>`;
  
  for(const inv of invoices){
   html+=`<div class="page">
   <div class="header">
    <div><div class="title">ERP-MSP</div><div>Sistem Akuntansi Modern</div></div>
    <div style="text-align:right"><div style="font-size:16px;font-weight:bold">FAKTUR PENJUALAN</div>
    <div>${esc(inv.invoice_number)}</div><div>${inv.transaction_date}</div></div>
   </div>
   <div style="margin-bottom:15px"><b>Kepada:</b> ${esc(inv.customer_name)}</div>
   <table><thead><tr><th>Barang</th><th>Qty</th><th>Harga</th><th>Total</th></tr></thead>
   <tbody>${(inv.lines||[]).map(l=>`<tr><td>${esc(l.item_name||l.description||"")}</td><td>${l.unit_qty||l.quantity}</td><td>Rp${l.unit_price.toLocaleString("id-ID")}</td><td>Rp${l.line_total.toLocaleString("id-ID")}</td></tr>`).join("")}</tbody></table>
   <div class="total">
    <p>Subtotal: Rp${(inv.subtotal||0).toLocaleString("id-ID")}</p>
    <p>PPN: Rp${(inv.tax_amount||0).toLocaleString("id-ID")}</p>
    <p><b>TOTAL: Rp${inv.total_amount.toLocaleString("id-ID")}</b></p>
   </div>
   <div class="footer">Dicetak batch: ${new Date().toLocaleString("id-ID")} | ERP-MSP</div>
   </div>`;
  }
  
  html+=`</body></html>`;
  const win=window.open('','_blank');
  win.document.write(html);
  win.document.close();
  setTimeout(()=>win.print(),500);
 }catch(e){alert("Gagal batch print: "+e.message);}
};
window.csv=(name,rows)=>{const q2=v=>`"${String(v??"").replace(/"/g,'""')}"`;
 const blob=new Blob([rows.map(r=>r.map(q2).join(",")).join("\n")],{type:"text/csv"});
 const a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download=name;a.click();};
function periodeFilter(monthInputId,yearInputId,records){
 const m=+$(monthInputId).value;
 const y=+$(yearInputId).value;
 if(!m||!y)return records;
 return records.filter(r=>{
  const d=new Date(r.transaction_date);
  return d.getMonth()+1===m&&d.getFullYear()===y;
 });
}
async function loadReport(type){
 const months=["Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus","September","Oktober","November","Desember"];
 const m=window._reportPeriod?.month||new Date().getMonth()+1;
 const y=window._reportPeriod?.year||new Date().getFullYear();
 const out=$("#reportOutput");
 if(!out)return;
 out.innerHTML="<div class='empty-state'>Memuat data...</div>";
 
 try{
  if(type==='penjualan'){
   const sales=await api("/api/sales");
   const filtered=sales.filter(x=>{const d=new Date(x.transaction_date);return d.getMonth()+1===m&&d.getFullYear()===y;});
   const total=filtered.reduce((a,x)=>a+x.total_amount,0);
   const paid=filtered.reduce((a,x)=>a+x.paid,0);
   const outstanding=filtered.reduce((a,x)=>a+x.outstanding,0);
   out.innerHTML=`<h3>📈 Laporan Penjualan - ${months[m-1]} ${y}</h3>
    <div class="kpi-row"><div class="kpi"><label>Total Faktur</label><b>${filtered.length}</b></div>
    <div class="kpi success"><label>Total Omzet</label><b>${fmt(total)}</b></div>
    <div class="kpi info"><label>Sudah Dibayar</label><b>${fmt(paid)}</b></div>
    <div class="kpi warning"><label>Belum Dibayar</label><b>${fmt(outstanding)}</b></div></div>
    <table><thead><tr><th>No</th><th>Tanggal</th><th>Customer</th><th>Total</th><th>Dibayar</th><th>Sisa</th><th>Status</th></tr></thead>
    <tbody>${filtered.map(x=>`<tr class="clickable-row" onclick="goDetail('sales-invoice',${x.id})"><td>${esc(x.invoice_number)}</td><td>${x.transaction_date}</td><td>${esc(x.customer_name)}</td><td>${fmt(x.total_amount)}</td><td>${fmt(x.paid)}</td><td>${fmt(x.outstanding)}</td><td>${st(x.status)}</td></tr>`).join("")}</tbody></table>`;
  }
  else if(type==='pembelian'){
   const purchases=await api("/api/purchases");
   const filtered=purchases.filter(x=>{const d=new Date(x.transaction_date);return d.getMonth()+1===m&&d.getFullYear()===y;});
   const total=filtered.reduce((a,x)=>a+x.total_amount,0);
   const paid=filtered.reduce((a,x)=>a+x.paid,0);
   const outstanding=filtered.reduce((a,x)=>a+x.outstanding,0);
   out.innerHTML=`<h3>📉 Laporan Pembelian - ${months[m-1]} ${y}</h3>
    <div class="kpi-row"><div class="kpi"><label>Total Faktur</label><b>${filtered.length}</b></div>
    <div class="kpi success"><label>Total Belanja</label><b>${fmt(total)}</b></div>
    <div class="kpi info"><label>Sudah Dibayar</label><b>${fmt(paid)}</b></div>
    <div class="kpi warning"><label>Belum Dibayar</label><b>${fmt(outstanding)}</b></div></div>
    <table><thead><tr><th>No</th><th>Tanggal</th><th>Vendor</th><th>Total</th><th>Dibayar</th><th>Sisa</th><th>Status</th></tr></thead>
    <tbody>${filtered.map(x=>`<tr class="clickable-row" onclick="goDetail('purchase-invoice',${x.id})"><td>${esc(x.invoice_number)}</td><td>${x.transaction_date}</td><td>${esc(x.vendor_name)}</td><td>${fmt(x.total_amount)}</td><td>${fmt(x.paid)}</td><td>${fmt(x.outstanding)}</td><td>${st(x.status)}</td></tr>`).join("")}</tbody></table>`;
  }
  else if(type==='laba_rugi'){
   const sales=await api("/api/sales");
   const purchases=await api("/api/purchases");
   const sFiltered=sales.filter(x=>{const d=new Date(x.transaction_date);return d.getMonth()+1===m&&d.getFullYear()===y;});
   const pFiltered=purchases.filter(x=>{const d=new Date(x.transaction_date);return d.getMonth()+1===m&&d.getFullYear()===y;});
   const omzet=sFiltered.reduce((a,x)=>a+x.total_amount,0);
   const cogs=pFiltered.reduce((a,x)=>a+x.total_amount,0);
   const laba=omzet-cogs;
   const margin=omzet>0?((laba/omzet)*100).toFixed(1):0;
   out.innerHTML=`<h3>💹 Laba Rugi - ${months[m-1]} ${y}</h3>
    <div class="kpi-row"><div class="kpi success"><label>Omzet</label><b>${fmt(omzet)}</b></div>
    <div class="kpi warning"><label>HPP/Beban</label><b>${fmt(cogs)}</b></div>
    <div class="kpi" style="background:${laba>=0?'var(--ok)':'var(--bad)'}"><label>Laba Bersih</label><b>${fmt(laba)}</b></div>
    <div class="kpi"><label>Margin</label><b>${margin}%</b></div></div>`;
  }
  else if(type==='piutang'){
   const sales=await api("/api/sales");
   const open=sales.filter(x=>x.outstanding>0);
   const aging=open.map(x=>{
    const due=new Date(x.due_date||x.transaction_date);
    const days=Math.floor((new Date()-due)/(1000*60*60*24));
    let bucket="Belum Jatuh Tempo";
    if(days>90)bucket="Lewat 90 Hari";
    else if(days>60)bucket="61-90 Hari";
    else if(days>30)bucket="31-60 Hari";
    else if(days>0)bucket="1-30 Hari";
    return{...x,aging:bucket};
   });
   const grouped=aging.reduce((a,x)=>{a[x.aging]=(a[x.aging]||0)+x.outstanding;return a;},{});
   out.innerHTML=`<h3>💰 Aging Piutang</h3>
    <div class="kpi-row">${Object.entries(grouped).map(([k,v])=>`<div class="kpi"><label>${k}</label><b>${fmt(v)}</b></div>`).join("")}</div>
    <table><thead><tr><th>No</th><th>Customer</th><th>Jatuh Tempo</th><th>Sisa</th><th>Aging</th></tr></thead>
    <tbody>${aging.sort((a,b)=>b.outstanding-a.outstanding).map(x=>`<tr><td>${esc(x.invoice_number)}</td><td>${esc(x.customer_name)}</td><td>${x.due_date||"-"}</td><td>${fmt(x.outstanding)}</td><td>${x.aging}</td></tr>`).join("")}</tbody></table>`;
  }
  else if(type==='hutang'){
   const purchases=await api("/api/purchases");
   const open=purchases.filter(x=>x.outstanding>0);
   const aging=open.map(x=>{
    const due=new Date(x.due_date||x.transaction_date);
    const days=Math.floor((new Date()-due)/(1000*60*60*24));
    let bucket="Belum Jatuh Tempo";
    if(days>90)bucket="Lewat 90 Hari";
    else if(days>60)bucket="61-90 Hari";
    else if(days>30)bucket="31-60 Hari";
    else if(days>0)bucket="1-30 Hari";
    return{...x,aging:bucket};
   });
   const grouped=aging.reduce((a,x)=>{a[x.aging]=(a[x.aging]||0)+x.outstanding;return a;},{});
   out.innerHTML=`<h3>💳 Aging Hutang</h3>
    <div class="kpi-row">${Object.entries(grouped).map(([k,v])=>`<div class="kpi"><label>${k}</label><b>${fmt(v)}</b></div>`).join("")}</div>
    <table><thead><tr><th>No</th><th>Vendor</th><th>Jatuh Tempo</th><th>Sisa</th><th>Aging</th></tr></thead>
    <tbody>${aging.sort((a,b)=>b.outstanding-a.outstanding).map(x=>`<tr><td>${esc(x.invoice_number)}</td><td>${esc(x.vendor_name)}</td><td>${x.due_date||"-"}</td><td>${fmt(x.outstanding)}</td><td>${x.aging}</td></tr>`).join("")}</tbody></table>`;
  }
  else if(type==='buku_besar'){
   const accounts=await api("/api/accounts");
   const journals=await api("/api/journals");
   const filtered=journals.filter(x=>{const d=new Date(x.transaction_date);return d.getMonth()+1===m&&d.getFullYear()===y;});
   const rows=[];
   for(const acc of accounts){
    const lines=[];
    for(const j of filtered){
     for(const l of (j.lines||[])){
      if(l.account_id===acc.id){
       lines.push({date:j.transaction_date,no:j.journal_number,desc:j.description,debit:l.debit,credit:l.credit});
      }
     }
    }
    if(lines.length>0){
     const totalDebit=lines.reduce((a,l)=>a+l.debit,0);
     const totalCredit=lines.reduce((a,l)=>a+l.credit,0);
     rows.push({code:acc.account_code,name:acc.account_name,lines,totalDebit,totalCredit});
    }
   }
   out.innerHTML=`<h3>📒 Buku Besar - ${months[m-1]} ${y}</h3>
    ${rows.map(r=>`<div style="margin-bottom:24px"><h4>${esc(r.code)} - ${esc(r.name)}</h4>
    <table><thead><tr><th>Tanggal</th><th>No</th><th>Uraian</th><th>Debit</th><th>Kredit</th></tr></thead>
    <tbody>${r.lines.map(l=>`<tr><td>${l.date}</td><td>${esc(l.no)}</td><td>${esc(l.desc)}</td><td>${fmt(l.debit)}</td><td>${fmt(l.credit)}</td></tr>`).join("")}
    <tr style="font-weight:bold;background:var(--card)"><td colspan="3">Total</td><td>${fmt(r.totalDebit)}</td><td>${fmt(r.totalCredit)}</td></tr>
    </tbody></table></div>`).join("")}`;
  }
 }catch(e){out.innerHTML=`<div class="card">❌ Error: ${e.message}</div>`;}
}
async function loadBudget(){
 const y=+$("#bud_year").value;
 const m=+$("#bud_month").value;
 const out=$("#budgetOutput");
 if(!out)return;
 
 try{
  const accounts=[
   {code:"4001",name:"Penjualan Produk",type:"income",budget:50000000},
   {code:"4002",name:"Penjualan Jasa",type:"income",budget:20000000},
   {code:"5001",name:"HPP",type:"expense",budget:30000000},
   {code:"5002",name:"Gaji Karyawan",type:"expense",budget:15000000},
   {code:"5003",name:"Sewa Tempat",type:"expense",budget:5000000},
   {code:"5004",name:"Listrik & Air",type:"expense",budget:3000000},
   {code:"5005",name:"Marketing",type:"expense",budget:7000000},
   {code:"5006",name:"Perlengkapan",type:"expense",budget:2000000}
  ];
  
  const sales=await api("/api/sales");
  const purchases=await api("/api/purchases");
  
  const filtered=sales.filter(x=>{
   const d=new Date(x.transaction_date);
   return d.getFullYear()===y&&(m===0||d.getMonth()+1===m);
  });
  
  const totalSales=filtered.reduce((a,x)=>a+x.total_amount,0);
  const totalPurchases=purchases.filter(x=>{
   const d=new Date(x.transaction_date);
   return d.getFullYear()===y&&(m===0||d.getMonth()+1===m);
  }).reduce((a,x)=>a+x.total_amount,0);
  
  out.innerHTML=`<h3>💰 Anggaran ${y} ${m>0?"- "+["","Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus","September","Oktober","November","Desember"][m]:""}</h3>
   <div class="kpi-row">
    <div class="kpi success"><label>Target Penjualan</label><b>${fmt(accounts.filter(a=>a.type==="income").reduce((a,x)=>a+x.budget,0))}</b></div>
    <div class="kpi" style="background:${totalSales>=accounts.filter(a=>a.type==="income").reduce((a,x)=>a+x.budget,0)?'var(--ok)':'var(--bad)'}"><label>Realisasi Penjualan</label><b>${fmt(totalSales)}</b></div>
    <div class="kpi warning"><label>Target Beban</label><b>${fmt(accounts.filter(a=>a.type==="expense").reduce((a,x)=>a+x.budget,0))}</b></div>
    <div class="kpi" style="background:${totalPurchases<=accounts.filter(a=>a.type==="expense").reduce((a,x)=>a+x.budget,0)?'var(--ok)':'var(--bad)'}"><label>Realisasi Beban</label><b>${fmt(totalPurchases)}</b></div>
   </div>
   <table style="margin-top:24px">
    <thead><tr><th>Akun</th><th>Jenis</th><th>Anggaran</th><th>Realisasi</th><th>Selisih</th><th>% Capai</th><th>Status</th></tr></thead>
    <tbody>
     ${accounts.map(a=>{
      const actual=a.type==="income"?(a.code.startsWith("4")?totalSales:0):(a.code.startsWith("5")?totalPurchases:0);
      const diff=a.budget-actual;
      const pct=a.budget>0?((actual/a.budget)*100).toFixed(1):0;
      const status=Math.abs(diff)<a.budget*0.1?"✅":"⚠️";
      return `<tr>
       <td><b>${a.code}</b> ${a.name}</td>
       <td>${a.type==="income"?"Pendapatan":"Beban"}</td>
       <td>${fmt(a.budget)}</td>
       <td>${fmt(actual)}</td>
       <td style="color:${diff>=0?'var(--ok)':'var(--bad)'}">${fmt(diff)}</td>
       <td>${pct}%</td>
       <td>${status}</td>
      </tr>`;
     }).join("")}
    </tbody>
    <tfoot>
     <tr style="font-weight:bold;background:var(--card)">
      <td colspan="2">TOTAL</td>
      <td>${fmt(accounts.reduce((a,x)=>a+x.budget,0))}</td>
      <td>${fmt(totalSales+totalPurchases)}</td>
      <td style="color:${accounts.reduce((a,x)=>a+x.budget,0)-(totalSales+totalPurchases)>=0?'var(--ok)':'var(--bad)'}">${fmt(accounts.reduce((a,x)=>a+x.budget,0)-(totalSales+totalPurchases))}</td>
      <td>${((totalSales+totalPurchases)/accounts.reduce((a,x)=>a+x.budget,0)*100).toFixed(1)}%</td>
      <td></td>
     </tr>
    </tfoot>
   </table>`;
 }catch(e){out.innerHTML=`<div class="card">❌ Error: ${e.message}</div>`;}
}
function exportBudget(){
 const y=$("#bud_year").value;
 const m=$("#bud_month").value;
 const content=document.getElementById("budgetOutput")?.innerText||"";
 const html=`<!DOCTYPE html><html><head><meta charset="utf-8"><title>Anggaran ${y} - ERP-MSP</title>
 <style>body{font-family:Arial,sans-serif;padding:20px}table{width:100%;border-collapse:collapse}th,td{padding:8px;border:1px solid #ddd;text-align:left}th{background:#f5f5f5}</style>
 </head><body><h1>Anggaran ${y}</h1><pre style="white-space:pre-wrap">${content}</pre></body></html>`;
 const win=window.open('','_blank');
 win.document.write(html);
 win.document.close();
 setTimeout(()=>win.print(),300);
}
window.csvTB=async()=>{const tb=await api("/api/reports/trial-balance");csv("trial-balance.csv",[["Kode","Akun","Tipe","Debit","Kredit"],...tb.map(r=>[r.account_code,r.account_name,r.account_type,r.d,r.k])]);};
window.csvStock=async()=>{const s=await api("/api/stock");csv("stok.csv",[["Kode","Barang","Gudang","Stok","AvgCost","Nilai"],...s.map(x=>[x.item_code,x.item_name,x.warehouse,x.stock,x.avg_cost,x.value])]);};
window.saveU=async()=>{try{await api("/api/units",{method:"POST",body:JSON.stringify({item_id:+$("#u_item").value,unit_code:$("#u_code").value,conversion:+$("#u_conv").value})});loadM().then(render);}catch(e){alert(e.message)}};
window.setMethod=async(id,m)=>{if(!confirm("Ubah metode HPP ke "+m+"? Layer FIFO dibangun ulang dari stok saat ini."))return;try{await api("/api/items/method",{method:"POST",body:JSON.stringify({id,method:m})});loadM().then(render);}catch(e){alert(e.message)}};
window.saveNU=async()=>{try{await api("/api/users",{method:"POST",body:JSON.stringify({username:$("#nu_u").value,password:$("#nu_p").value,full_name:$("#nu_n").value,role:$("#nu_r").value})});render();}catch(e){alert(e.message)}};
window.savePay=async()=>{
 try{const tot=_al.reduce((a,x)=>a+x.amount,0);
 showLoading("#app button.go","Menyimpan...");
 const rate=+$("#k_rate").value||1;
 const curr=(_cs.find(c=>c.id===+$("#k_c").value)?.currency_code||"IDR");
 await api("/api/payments",{method:"POST",body:JSON.stringify({kind:$("#k_kind").value,cash_account_id:+$("#k_cash").value,contact_id:+$("#k_c").value,amount:tot,date:$("#k_date").value,note:$("#k_note").value,allocations:_al,currency:curr,exchange_rate:rate})});
 alert("Pembayaran "+formatCurrency(tot,curr)+" tercatat");render();}catch(e){alert(e.message)}finally{hideLoading("#app button.go");}};
window.kindCh=()=>{const k=$("#k_kind").value;const cs=k==="AR"?CUST:VEND;const nm=k==="AR"?"customer_name":"vendor_name";
 $("#k_c").innerHTML=cs.map(c=>`<option value="${c.id}">${c[nm]}</option>`).join("");
 const ag=k==="AR"?_ag:_agAP;
 $("#k_inv").innerHTML=ag.map(x=>`<option value="${x.id}">${x.invoice_number} — ${x.contact} (sisa ${fmt(x.outstanding)})</option>`).join("")||`<option value="">- lunas semua -</option>`;
 invCh();};
window.invCh=()=>{const ag=$("#k_kind").value==="AR"?_ag:_agAP;const x=ag.find(i=>i.id==$("#k_inv").value);if(x)$("#k_alloc").value=x.outstanding;};
window.addAlloc=()=>{const id=+$("#k_inv").value;if(!id)return alert("Tidak ada invoice outstanding");
 const amt=+$("#k_alloc").value;if(!(amt>0))return alert("Nominal harus > 0");
 if(_al.find(a=>a.invoice_id===id))return alert("Invoice sudah ada di daftar");
 _al.push({invoice_id:id,amount:amt});
 $("#alocs").innerHTML=_al.map((a,i)=>{const ag=$("#k_kind").value==="AR"?_ag:_agAP;const x=ag.find(v=>v.id===a.invoice_id);return `<div>${x?x.invoice_number:"#"+a.invoice_id} — ${fmt(a.amount)} <a href="#" onclick="_al.splice(${i},1);addAllocRefresh();return false">hapus</a></div>`;}).join("")+`<b>Total: ${fmt(_al.reduce((a,x)=>a+x.amount,0))}</b>`;};
window.addAllocRefresh=()=>{const t=_al;_al=[];const keep=$("#k_alloc").value;$("#alocs").innerHTML="";t.forEach(a=>{const ag=$("#k_kind").value==="AR"?_ag:_agAP;if(ag.find(v=>v.id===a.invoice_id))_al.push(a);});$("#k_alloc").value=keep;
 $("#alocs").innerHTML=_al.map((a,i)=>`<div>#${a.invoice_id} — ${fmt(a.amount)} <a href="#" onclick="_al.splice(${i},1);addAllocRefresh();return false">hapus</a></div>`).join("")+(_al.length?`<b>Total: ${fmt(_al.reduce((a,x)=>a+x.amount,0))}</b>`:"");};
window.voidSale=async id=>{if(!confirm("Void invoice ini? Jurnal dibalik & stok dikembalikan."))return;try{const r=await api("/api/sales/void",{method:"POST",body:JSON.stringify({id,date:today()})});alert(r.need_approval?"Diajukan, menunggu MANAGER": "Invoice di-void");render();}catch(e){alert(e.message)}};
window.voidBuy=async id=>{if(!confirm("Void tagihan ini? Jurnal dibalik & stok dikurangi."))return;try{const r=await api("/api/purchases/void",{method:"POST",body:JSON.stringify({id,date:today()})});alert(r.need_approval?"Diajukan, menunggu MANAGER":"Tagihan di-void");render();}catch(e){alert(e.message)}};
let cnCLines=[];
function addCNLine(){
 const item_id=+$("#cn_it").value||null;
 const qty=+$("#cn_q").value;
 const price=+$("#cn_pr").value;
 const desc=esc($("#cn_ldesc").value||"");
 const name=item_id?(ITEMS.find(x=>x.id===item_id)?.item_name||""):"";
 cnCLines.push({item_id,quantity:qty,unit_price:price,line_total:qty*price,description:desc,item_name:name});
 renderCNPreview();
}
function renderCNPreview(){
 const sum=cnCLines.reduce((a,l)=>a+l.line_total,0);
 const el=$("#cn_preview");
 if(el)el.innerHTML=cnCLines.length?`<table><tr><th>Item</th><th>Qty</th><th>Harga</th><th>Total</th><th></th></tr>${cnCLines.map((l,i)=>`<tr><td>${esc(l.item_name||"Non-Inventory")}</td><td>${l.quantity}</td><td>${fmt(l.unit_price)}</td><td>${fmt(l.line_total)}</td><td><button class="row-del" onclick="cnCLines.splice(${i},1);renderCNPreview()">×</button></td></tr>`).join("")}</table><p>Total: <b>${fmt(sum)}</b></p>`:"";
}
window.saveCN=async()=>{
 try{showLoading("#app button.go","Menyimpan...");
 await api("/api/returns",{method:"POST",body:JSON.stringify({type:"CUSTOMER",customer_id:+$("#cn_cust").value,date:$("#cn_d").value,description:$("#cn_desc").value,lines:cnCLines.map(l=>({item_id:l.item_id,quantity:l.quantity,unit_price:l.unit_price,line_total:l.line_total,description:l.description}))})});
 alert("Credit Note tersimpan");cnCLines=[];render();}catch(e){alert(e.message)}finally{hideLoading("#app button.go");}
};
window.createCNFromInvoice=async(invId)=>{
 try{const inv=(await api("/api/sales")).find(x=>x.id===invId);
 if(!inv)return alert("Invoice tidak ditemukan");
 $("#cn_cust").value=inv.customer_id;
 $("#cn_d").value=inv.transaction_date;
 $("#cn_desc").value="CN dari "+inv.invoice_number;
 cnCLines=(inv.lines||[]).map(l=>({item_id:l.item_id,quantity:l.quantity,unit_price:l.unit_price,line_total:l.line_total,description:l.description||"",item_name:l.item_name||""}));
 renderCNPreview();
 alert("Data invoice "+inv.invoice_number+" dimuat. Simpan Credit Note.");}catch(e){alert(e.message);}
};
let dnDLines=[];
function addDNLine(){
 const item_id=+$("#dn_it").value||null;
 const qty=+$("#dn_q").value;
 const price=+$("#dn_pr").value;
 const desc=esc($("#dn_ldesc").value||"");
 const name=item_id?(ITEMS.find(x=>x.id===item_id)?.item_name||""):"";
 dnDLines.push({item_id,quantity:qty,unit_price:price,line_total:qty*price,description:desc,item_name:name});
 renderDNPreview();
}
function renderDNPreview(){
 const sum=dnDLines.reduce((a,l)=>a+l.line_total,0);
 const el=$("#dn_preview");
 if(el)el.innerHTML=dnDLines.length?`<table><tr><th>Item</th><th>Qty</th><th>Harga</th><th>Total</th><th></th></tr>${dnDLines.map((l,i)=>`<tr><td>${esc(l.item_name||"Non-Inventory")}</td><td>${l.quantity}</td><td>${fmt(l.unit_price)}</td><td>${fmt(l.line_total)}</td><td><button class="row-del" onclick="dnDLines.splice(${i},1);renderDNPreview()">×</button></td></tr>`).join("")}</table><p>Total: <b>${fmt(sum)}</b></p>`:"";
}
window.saveDN=async()=>{
 try{showLoading("#app button.go","Menyimpan...");
 await api("/api/returns",{method:"POST",body:JSON.stringify({type:"VENDOR",vendor_id:+$("#dn_ven").value,date:$("#dn_d").value,description:$("#dn_desc").value,lines:dnDLines.map(l=>({item_id:l.item_id,quantity:l.quantity,unit_price:l.unit_price,line_total:l.line_total,description:l.description}))})});
 alert("Debit Note tersimpan");dnDLines=[];render();}catch(e){alert(e.message)}finally{hideLoading("#app button.go");}
};
window.createDNFromInvoice=async(invId)=>{
 try{const inv=(await api("/api/purchases")).find(x=>x.id===invId);
 if(!inv)return alert("Invoice tidak ditemukan");
 $("#dn_ven").value=inv.vendor_id;
 $("#dn_d").value=inv.transaction_date;
 $("#dn_desc").value="DN dari "+inv.invoice_number;
 dnDLines=(inv.lines||[]).map(l=>({item_id:l.item_id,quantity:l.quantity,unit_price:l.unit_price,line_total:l.line_total,description:l.description||"",item_name:l.item_name||""}));
 renderDNPreview();
 alert("Data invoice "+inv.invoice_number+" dimuat. Simpan Debit Note.");}catch(e){alert(e.message);}
};
window.opname=async()=>{try{const r=await api("/api/stock/opname",{method:"POST",body:JSON.stringify({item_id:+$("#o_item").value,warehouse_id:+$("#o_wh").value,actual_qty:+$("#o_qty").value,date:$("#o_date").value})});alert("Selisih "+r.diff+" ("+fmt(r.value)+")");loadM().then(render);}catch(e){alert(e.message)}};
window.transfer=async()=>{try{await api("/api/stock/transfer",{method:"POST",body:JSON.stringify({item_id:+$("#t_item").value,from_warehouse:+$("#t_from").value,to_warehouse:+$("#t_to").value,qty:+$("#t_qty").value,date:$("#t_date").value})});alert("Stok dipindahkan");loadM().then(render);}catch(e){alert(e.message)}};
let saLines=[];
function addSALine(){
 const item_id=+$("#sa_it").value;
 const system_qty=+$("#sa_sys").value;
 const fisik_qty=+$("#sa_fisik").value;
 if(!item_id)return alert("Pilih barang!");
 const diff=fisik_qty-system_qty;
 saLines.push({item_id,system_qty,fisik_qty,difference:diff});
 alert("Ditambahkan: "+(ITEMS.find(x=>x.id===item_id)?.item_name||"")+" selisih "+diff);
 $("#sa_it").value="";$("#sa_sys").value=0;$("#sa_fisik").value=0;$("#sa_selisih").value=0;
}
window.saveSA=async()=>{
 try{showLoading("#app button.go","Menyimpan...");
 await api("/api/stock-adjustments",{method:"POST",body:JSON.stringify({type:"OPNAME",warehouse_id:+$("#sa_wh").value,date:$("#sa_d").value,note:$("#sa_note").value,lines:saLines})});
 alert("Stok Opname tersimpan");saLines=[];render();}catch(e){alert(e.message)}finally{hideLoading("#app button.go");}
};
window.viewSA=async(id)=>{
 try{
  const adj=(await api("/api/stock-adjustments")).find(x=>x.id===id);
  if(!adj)return alert("Data tidak ditemukan");
  const lines=adj.lines||[];
  alert("ADJ #"+adj.id+"\nTanggal: "+adj.transaction_date+"\nCatatan: "+(adj.note||"-")+"\n\n"+lines.map(l=>`${l.item_name||"Item #"+l.item_id}: ${l.system_qty} → ${l.fisik_qty} (${l.difference>0?"+":""}${l.difference})`).join("\n"));
 }catch(e){alert(e.message);}
};
let adjLines=[];
function addAdjLine(){
 const item_id=+$("#adj_it").value;
 const qty=+$("#adj_q").value;
 if(!item_id)return alert("Pilih barang!");
 adjLines.push({item_id,quantity:qty});
 alert("Ditambahkan: "+(ITEMS.find(x=>x.id===item_id)?.item_name||"")+" qty "+qty);
 $("#adj_it").value="";$("#adj_q").value=1;
}
window.saveAdj=async()=>{
 try{showLoading("#app button.go","Menyimpan...");
 const kind=$("#adj_kind").value;
 await api("/api/stock-adjustments",{method:"POST",body:JSON.stringify({type:kind,warehouse_id:+$("#adj_wh").value,date:$("#adj_d").value,note:$("#adj_note").value,lines:adjLines.map(l=>({...l,quantity:kind==="OUT"?-l.quantity:l.quantity}))})});
 alert("Adjustment tersimpan");adjLines=[];render();}catch(e){alert(e.message)}finally{hideLoading("#app button.go");}
};
window.saveJ=async()=>{
 try{showLoading("#app button.go","Posting...");
 await api("/api/journals",{method:"POST",body:JSON.stringify({transaction_date:$("#j_d").value,description:$("#j_desc").value,lines:_jl})});
 alert("Jurnal posted");render();}catch(e){alert(e.message)}finally{hideLoading("#app button.go");}};
window.card=async()=>{const r=await api("/api/stock-card?item_id="+$("#sc").value);$("#card").innerHTML=`<table><tr><th>Tgl</th><th>Ref</th><th>In</th><th>Out</th><th>HPP</th></tr>${r.map(x=>`<tr><td>${x.transaction_date}</td><td>${x.reference_type}</td><td>${x.qty_in}</td><td>${x.qty_out}</td><td>${fmt(x.cogs_unit_price)}</td></tr>`).join("")}</table>`;};
window.saveA=async()=>{await api("/api/assets",{method:"POST",body:JSON.stringify({asset_code:$("#a_c").value,asset_name:$("#a_n").value,purchase_date:$("#a_d").value,cost:Math.round(+$("#a_cost").value),useful_months:+$("#a_u").value})});render();};
window.susut=async id=>{const r=await api("/api/assets/depreciate",{method:"POST",body:JSON.stringify({id,date:today()})});alert("Disusutkan "+fmt(r.amount));render();};
window.disposeA=async id=>{const p=prompt("Harga jual/disposal Rp (0=hapus):","0");if(p===null)return;try{const r=await api("/api/assets/dispose",{method:"POST",body:JSON.stringify({id,sale_price:Math.round(+p||0),date:today()})});alert("Aset di-disposal, jurnal #"+r.journal);render();}catch(e){alert(e.message)}};
window.saveTX=async()=>{try{await api("/api/taxes",{method:"POST",body:JSON.stringify({tax_code:$("#tx_c").value,tax_name:$("#tx_n").value,rate:+$("#tx_r").value})});await loadM();render();}catch(e){alert(e.message)}};
window.loadTaxAp=async()=>{try{const t=TAX.length?TAX:await api("/api/taxes");if($("#tax_list"))$("#tax_list").innerHTML=`<table><tr><th>Kode</th><th>Nama</th><th>Tarif</th></tr>${t.map(x=>`<tr><td>${esc(x.tax_code)}</td><td>${esc(x.tax_name)}</td><td>${esc(x.rate)}%</td></tr>`).join("")}</table>`;}catch(e){if($("#tax_list"))$("#tax_list").textContent=e.message;}
 try{const a=await api("/api/approvals");if($("#ap_list"))$("#ap_list").innerHTML=a.length?a.map(x=>`<div>${esc(x.kind)} ${esc(x.ref_type)}#${x.ref_id} ${fmt(x.amount)} oleh ${esc(x.requested_by)} [${esc(x.status)}] ${x.status==="PENDING"?`<button class="go ok" onclick="decAp(${x.id},1)">Setujui</button> <button class="go danger" onclick="decAp(${x.id},0)">Tolak</button>`:""}</div>`).join(""):"Tidak ada pengajuan.";}catch(e){if($("#ap_list"))$("#ap_list").textContent="—";}};
window.decAp=async(id,ok)=>{try{await api("/api/approvals/decide",{method:"POST",body:JSON.stringify({id,approve:!!ok})});alert(ok?"Disetujui (eksekusi void manual oleh manager)":"Ditolak");render();}catch(e){alert(e.message)}};
window.calcPPh=async()=>{try{const r=await api("/api/payroll/calc",{method:"POST",body:JSON.stringify({gross:Math.round(+$("#pr_g").value||0)})});$("#pr_out").textContent=`Bruto ${fmt(r.gross)} TER ${(r.rate*100).toFixed(2)}% → PPh ${fmt(r.pph21)} Net ${fmt(r.net)}`;}catch(e){alert(e.message)}};
window.saveCOA=async()=>{await api("/api/coa",{method:"POST",body:JSON.stringify({account_code:$("#c_c").value,account_name:$("#c_n").value,account_type:$("#c_t").value})});loadM().then(render);};
window.saveW=async()=>{await api("/api/webhooks",{method:"POST",body:JSON.stringify({event:$("#w_e").value,url:$("#w_u").value})});render();};
window.ocr=async()=>{const f=$("#ocr_f").files[0];$("#ocr_out").textContent=f?("Membaca "+f.name+"… (simulasi) total Rp 275.000 terdeteksi → membuat draft…"):"Pilih file dulu.";if(!f)return;
 const kas=COA.find(c=>c.account_code==="11001").id,beban=COA.find(c=>c.account_code==="62001").id;
 const r=await api("/api/ocr-draft",{method:"POST",body:JSON.stringify({description:"OCR: "+f.name,date:today(),lines:[{account_id:beban,debit:275000,credit:0},{account_id:kas,debit:0,credit:275000}]})});
 $("#ocr_out").textContent="Draft jurnal dibuat #"+r.id+" (status DRAFT). Cek di Buku Besar.";};
window.payroll=async()=>{const g=COA.find(c=>c.account_code==="61001").id,u=COA.find(c=>c.account_code==="23001").id;const v=+$("#hr").value;
 await api("/api/journals",{method:"POST",body:JSON.stringify({transaction_date:today(),description:"Gaji bulan ini (HRIS)",lines:[{account_id:g,debit:v,credit:0},{account_id:u,debit:0,credit:v}]})});
 $("#hr_out").textContent="Jurnal gaji "+fmt(v)+" terposting (Dr Beban Gaji / Cr Utang Gaji).";};
boot();

// Mobile sidebar toggle
if(window.innerWidth<=900){
 const aside=$("aside");
 if(aside&&!aside._mobInit){
  aside._mobInit=true;
  const toggle=document.createElement("button");
  toggle.className="mobile-toggle";
  toggle.innerHTML="☰";
  toggle.onclick=()=>aside.classList.toggle("open");
  document.querySelector("main").prepend(toggle);
 }
}
