(function(){
  const btn=document.getElementById('menu-button');
  const nav=document.getElementById('site-nav');
  if(btn&&nav){
    btn.addEventListener('click',()=>{
      const opened=nav.classList.toggle('open');
      btn.setAttribute('aria-expanded',String(opened));
      btn.setAttribute('aria-label',opened?'Menüyü kapat':'Menüyü aç');
    });
    nav.addEventListener('click',e=>{if(e.target.closest('a')){nav.classList.remove('open');btn.setAttribute('aria-expanded','false');}});
  }
  const input=document.getElementById('article-search');
  const cards=[...document.querySelectorAll('#article-grid .article-card')];
  const filters=[...document.querySelectorAll('.filter')];
  const empty=document.getElementById('article-no-results');
  let selected='all';
  function apply(){
    const text=(input?.value||'').toLocaleLowerCase('tr-TR').trim();
    let count=0;
    cards.forEach(c=>{
      const shown=(selected==='all'||c.dataset.category===selected)&&(!text||c.dataset.search.toLocaleLowerCase('tr-TR').includes(text));
      c.hidden=!shown;
      if(shown) count++;
    });
    if(empty) empty.hidden=cards.length===0||count!==0;
  }
  input?.addEventListener('input',apply);
  filters.forEach(b=>b.addEventListener('click',()=>{
    selected=b.dataset.filter;
    filters.forEach(f=>f.classList.toggle('active',f===b));
    apply();
  }));
})();
