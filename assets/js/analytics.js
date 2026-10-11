(() => {
 const tag = document.currentScript;
 const id = tag.dataset.measurementId;
 if (!/^G-[A-Z0-9]+$/.test(id) || !['yangchenglawyer.com','www.yangchenglawyer.com'].includes(location.hostname)) return;
 const lang = document.documentElement.lang;
 const words = lang === 'en' ? ['Visitor statistics','With your permission, Google Analytics records page visits to help improve this website.','Allow','Decline','Statistics settings'] : lang === 'zh-Hant' ? ['訪問統計','經您同意後，Google Analytics 將記錄頁面訪問，幫助改進網站。','允許','拒絕','統計設定'] : ['访问统计','经您同意后，Google Analytics 将记录页面访问，帮助改进网站。','允许','拒绝','统计设置'];
 const key = 'lawyer-analytics-consent';
 let started = false;
 const read = () => { try { return localStorage.getItem(key); } catch { return null; } };
 const track = () => {
  if(started || navigator.doNotTrack === '1' || window.doNotTrack === '1') return;
  started = true;
  window['ga-disable-' + id] = false;
  window.dataLayer = window.dataLayer || [];
  window.gtag = function(){ window.dataLayer.push(arguments); };
  gtag('js', new Date());
  gtag('config', id, {allow_google_signals:false,allow_ad_personalization_signals:false,page_location:location.origin+location.pathname});
  const script = document.createElement('script');
  script.async = true; script.src = 'https://www.googletagmanager.com/gtag/js?id='+id;
  document.head.appendChild(script);
 };
 const init = () => {
  const panel = document.createElement('aside'); panel.className='analytics-consent'; panel.setAttribute('aria-label',words[0]);
  const message=document.createElement('p'); message.textContent=words[1]; panel.appendChild(message);
  const settings=document.createElement('button'); settings.type='button'; settings.className='analytics-settings'; settings.textContent=words[4];
  const choose = value => {
   try {localStorage.setItem(key,value);} catch {}
   panel.hidden=true; settings.hidden=false;
   if(value==='yes') track();
   else {
    window['ga-disable-'+id]=true;
    document.cookie.split(';').forEach(item=>{const name=item.trim().split('=')[0];if(name.startsWith('_ga')) for(const domain of ['',location.hostname,'.yangchenglawyer.com']) document.cookie=name+'=; Max-Age=0; path=/'+(domain?'; domain='+domain:'');});
   }
  };
  [words[2],words[3]].forEach((label,i)=>{const button=document.createElement('button');button.type='button';button.textContent=label;button.addEventListener('click',()=>choose(i===0?'yes':'no'));panel.appendChild(button);});
  settings.addEventListener('click',()=>{panel.hidden=false;settings.hidden=true;});
  document.body.append(panel,settings);
  const saved=read();panel.hidden=!!saved;settings.hidden=!saved;if(saved==='yes')track();
 };
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
