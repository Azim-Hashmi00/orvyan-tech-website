/* Orvyan live voice demo. Brain: /.netlify/functions/agent, falls back to a built-in scripted agent. */
(function(){
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
['#hb','#db'].forEach(s=>{if(!$(s))return;$(s).innerHTML='<s></s>'.repeat(28);$$(s+' s').forEach((e,i)=>e.style.animationDelay=(i%7)*.11+'s')});
const log=(el,who,t)=>{const d=document.createElement('div');d.className='vm v'+who;d.textContent=t;el.append(d);while(el.children.length>(el.id==='hl'?4:60))el.firstChild.remove();el.scrollTop=el.scrollHeight};

/* hero loop */
const hl=['a|Thanks for calling, this is Eric. How can I help?','u|Hi, I need a cleaning this week.','a|Of course. Thursday at 10 or Friday at 2?','u|Friday works.','a|Booked. I’ve texted you the details.'];let hi=0;
if($('#hl'))setInterval(()=>{if(hi===0)$('#hl').innerHTML='';const[w,t]=hl[hi].split('|');log($('#hl'),w,t);hi=(hi+1)%hl.length},2200);

/* scenarios */
const SC={dental:{greet:'Thanks for calling the dental front desk, this is Eric. How can I help you today?',tries:['I’d like to book a cleaning','I have a bad toothache','Do you take insurance?','Can I speak to a person?'],
 uc:{h:'Fill the chair, not the voicemail.',l:['Books, moves and confirms appointments','Handles toothache calls and flags urgent ones','Answers insurance and hours questions','Calls patients to remind and rebook no-shows'],c:[['a','Thanks for calling, this is Eric. How can I help?'],['u','I’ve got a sore tooth since last night.'],['a','I’m sorry to hear that. I’ll mark this urgent. Can I take your name and number?'],['u','Sam, 555 0142.'],['a','Thanks Sam. The clinic will call you back shortly.']]}},
 prop:{greet:'Thanks for calling the leasing office, this is Eric. Are you calling about a tour or a maintenance request?',tries:['I’d like to tour an apartment','My sink is leaking','What are your office hours?','Can I speak to a person?'],
 uc:{h:'Every tenant call answered, every lead followed up.',l:['Books tours and sends confirmations','Logs maintenance requests with unit and issue','Answers questions on hours, pets and applications','Calls back leads who did not book'],c:[['a','Thanks for calling the leasing office, this is Eric.'],['u','Is the two-bedroom still available?'],['a','I can check. Would you like to book a tour? What’s your name?'],['u','Dana.'],['a','Thanks Dana. Which day works best, morning or afternoon?']]}}};
let sc='dental';
function setSc(k){sc=k;endCall();$$('.vseg button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.sc===k));$('#dl').innerHTML='';$('#try').innerHTML=SC[k].tries.map(t=>`<li><button type="button">${t}</button></li>`).join('');$$('#try button').forEach(b=>b.onclick=()=>{if(!on)startCall(true);send(b.textContent)})}
$$('.vseg button').forEach(b=>b.onclick=()=>setSc(b.dataset.sc));

/* local brain (works with no server) */
const FL={
 dental:{book:{s:['Happy to set that up. What’s your name?','Thanks. Which day works best, and morning or afternoon?'],d:'Perfect, you’re booked and a text confirmation is on its way. Anything else I can help with?'},
  urgent:{s:['I’m sorry you’re in pain. I’ll mark this urgent. What’s your name and best number?'],d:'Thank you. The clinic team will call you back as soon as possible. If it gets worse, or you struggle to breathe or swallow, please call 911.'}},
 prop:{book:{s:['Happy to book a tour. What’s your name?','Thanks. Which day works best, morning or afternoon?'],d:'Done, your tour is booked and a confirmation is on its way. Anything else?'},
  urgent:{s:['Sorry about that. What’s your unit number and what’s happening?'],d:'Thanks. I’ve logged a maintenance ticket and the on-site team will follow up today. If water is flooding or there is a gas smell, call 911 or the emergency line now.'}}};
const INFO={dental:[[/insur/,'We work with most major plans. Share your provider and the team will confirm your coverage when you book.'],[/hour|open|close/,'The clinic is open on weekdays, with some Saturday slots. I can check a specific day for you.'],[/price|cost|much/,'The clinic quotes after the exam so it’s accurate. I can book you in and note your insurance.']],
 prop:[[/hour|open|close/,'The leasing office is open on weekdays and by appointment on weekends. I can book a time for you.'],[/pet|dog|cat/,'Pet policies depend on the building. I’ll note your question and the team will confirm. Want a tour too?'],[/apply|application|rent|price|cost/,'Pricing and applications depend on the unit. I can book a tour or have the team send details.']]};
let st=null;
function local(t){t=t.toLowerCase();
 if(st){const f=FL[sc][st.k];st.i++;if(st.i<f.s.length)return f.s[st.i];const d=f.d;st=null;return d}
 const f=FL[sc];
 if(/human|person|someone|manager|agent/.test(t))return'Of course. I’ll pass you to the team with a summary so you don’t repeat yourself.';
 if(/leak|broken|toothache|tooth ache|pain|hurt|swollen|bleed|emergenc|sore|maintenance|repair/.test(t)){st={k:'urgent',i:0};return f.urgent.s[0]}
 if(/book|appoint|clean|check|schedule|tour|visit|see /.test(t)){st={k:'book',i:0};return f.book.s[0]}
 for(const[r,a]of INFO[sc])if(r.test(t))return a;
 if(/thank|bye|that’s all|that's all|no thanks/.test(t))return'My pleasure. Have a great day!';
 return sc==='dental'?'I can book appointments, handle urgent tooth pain, or answer questions on hours and insurance. What do you need?':'I can book tours, log maintenance requests, or answer questions on hours and applications. What do you need?'}

/* remote brain: /.netlify/functions/agent (needs ANTHROPIC_API_KEY), falls back to local */
let hist=[],remote=true;
async function brain(t){hist.push({role:'user',content:t});let a=null;
 if(remote){try{const r=await fetch('/.netlify/functions/agent',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({scenario:sc,messages:hist.slice(-10)})});if(r.ok){a=(await r.json()).reply}else remote=false}catch(e){remote=false}}
 if(!a)a=local(t);hist.push({role:'assistant',content:a});return a}

/* call engine */
const SR=window.SpeechRecognition||window.webkitSpeechRecognition;let rec,on=false,busy=false,timer,left=120;
const setS=(s,bars)=>{$('#stt').textContent=s;$('#db').classList.toggle('on',!!bars)};
function say(t,cb){if(!('speechSynthesis'in window)){cb&&cb();return}speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(t);u.lang='en-US';u.rate=1.03;const vs=speechSynthesis.getVoices();const v=vs.find(v=>/en[-_]US/.test(v.lang)&&/Google|Samantha|Aria|Jenny|Natural|Zira/i.test(v.name))||vs.find(v=>/^en/.test(v.lang));if(v)u.voice=v;u.onend=u.onerror=()=>cb&&cb();setS('Eric is speaking',1);speechSynthesis.speak(u)}
function listen(){if(!on||busy)return;if(!SR){setS('Type your message below');return}try{rec=new SR();rec.lang='en-US';rec.interimResults=false;rec.onresult=e=>{const t=e.results[0][0].transcript.trim();if(t)send(t)};rec.onerror=e=>{if(e.error==='not-allowed')setS('Microphone blocked. You can type instead.')};rec.onend=()=>{if(on&&!busy)setTimeout(listen,250)};rec.start();setS('Listening… speak now',1)}catch(e){}}
async function send(t){if(!on)startCall(true);if(busy)return;busy=true;try{rec&&rec.abort()}catch(e){}log($('#dl'),'u',t);setS('Eric is thinking');const a=await brain(t);log($('#dl'),'a',a);say(a,()=>{busy=false;listen()})}
function startCall(quiet){if(on)return;on=true;busy=true;hist=[];st=null;left=120;$('#dl').innerHTML='';const g=$('#go');g.textContent='End call';g.classList.add('end');
 timer=setInterval(()=>{left--;$('#tm').textContent=Math.floor(left/60)+':'+String(left%60).padStart(2,'0');if(left<=0){log($('#dl'),'a','That’s the end of the two-minute demo. To get an agent like this for your business, book a free consultation.');endCall(1)}},1000);
 if(quiet){busy=false;return}log($('#dl'),'a',SC[sc].greet);hist.push({role:'assistant',content:SC[sc].greet});say(SC[sc].greet,()=>{busy=false;listen()})}
function endCall(keep){clearInterval(timer);on=false;busy=false;try{rec&&rec.abort()}catch(e){}'speechSynthesis'in window&&speechSynthesis.cancel();const g=$('#go');g.textContent='Start call';g.classList.remove('end');$('#tm').textContent='2:00';setS('Ready')}
$('#go').onclick=()=>on?endCall():startCall();
$('#tf').onsubmit=e=>{e.preventDefault();const v=$('#ti').value.trim();if(v){$('#ti').value='';send(v)}};
if(window.speechSynthesis)speechSynthesis.getVoices();
setSc('dental');
})();
