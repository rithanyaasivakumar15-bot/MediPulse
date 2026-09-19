from datetime import date,timedelta
from math import ceil
from random import Random
from statistics import mean
from pathlib import Path
from io import BytesIO
import pandas as pd
from fastapi import FastAPI,HTTPException,UploadFile,File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine,Column,Integer,String,Float,Date
from sqlalchemy.orm import declarative_base,sessionmaker

BASE=Path(__file__).resolve().parent
engine=create_engine(f"sqlite:///{BASE/'medipulse.db'}",connect_args={'check_same_thread':False})
Session=sessionmaker(bind=engine); Base=declarative_base()
class Item(Base):
 __tablename__='items'; id=Column(Integer,primary_key=True); code=Column(String,unique=True); name=Column(String); category=Column(String); stock=Column(Float); reserve=Column(Float); lead=Column(Float); buffer=Column(Float); expiry=Column(Date); multiple=Column(Integer); supplier=Column(String); unit=Column(String)
class Usage(Base):
 __tablename__='usage'; id=Column(Integer,primary_key=True); item_id=Column(Integer); day=Column(Date); qty=Column(Float)
Base.metadata.create_all(engine)

def seed():
 db=Session()
 if db.query(Item).count(): db.close(); return
 rows=[
 ('MED-001','Insulin','Medicines',500,100,65,7,80,30,10,'MediSource'),('MED-002','Amoxicillin','Medicines',850,150,42,8,120,45,25,'HealthLine'),('MED-003','Paracetamol','Medicines',1800,250,55,5,180,180,50,'HealthLine'),('MED-004','Ceftriaxone','Medicines',320,80,35,10,100,25,10,'MediSource'),('MED-005','Salbutamol','Medicines',240,60,18,6,70,40,10,'CarePlus'),('CON-001','Syringes 5ml','Consumables',4200,500,380,7,500,300,100,'MedEquip'),('CON-002','IV Sets','Consumables',950,200,110,9,180,240,50,'MedEquip'),('CON-003','Gloves','Consumables',7600,1000,620,5,700,365,500,'SafeHands'),('CON-004','Face Masks','Consumables',12000,1500,900,6,1000,300,1000,'SafeHands'),('EMR-001','Epinephrine','Emergency Supplies',90,30,7,12,25,45,10,'EmergencyMed'),('EMR-002','Oxygen Masks','Emergency Supplies',210,50,16,8,50,240,20,'MedEquip'),('EMR-003','IV Fluids','Emergency Supplies',680,120,80,7,100,75,50,'MediSource'),('SUR-001','Surgical Sutures','Surgical Supplies',480,100,35,10,80,50,20,'SurgiCare'),('SUR-002','Sterile Drapes','Surgical Supplies',330,80,22,12,60,120,20,'SurgiCare'),('SUR-003','Scalpel Blades','Surgical Supplies',1600,250,100,6,160,90,100,'SurgiCare'),('SUR-004','Catheter 16Fr','Surgical Supplies',260,60,24,9,55,50,20,'MedEquip'),('MED-006','Heparin','Medicines',190,50,20,7,45,20,10,'MediSource'),('CON-005','Alcohol Swabs','Consumables',5200,800,260,6,400,240,200,'SafeHands'),('EMR-004','Nebulizer Kits','Emergency Supplies',150,40,12,8,40,180,20,'EmergencyMed'),('SUR-005','Surgical Gloves','Surgical Supplies',1300,250,115,7,180,60,50,'SafeHands')]
 rng=Random(42); today=date.today()
 for idx,r in enumerate(rows,1):
  code,name,cat,stock,reserve,daily,lead,buffer,exp,mult,supplier=r; it=Item(id=idx,code=code,name=name,category=cat,stock=stock,reserve=reserve,lead=lead,buffer=buffer,expiry=today+timedelta(days=exp),multiple=mult,supplier=supplier,unit='units'); db.add(it); db.flush()
  for d in range(28):
   factor=1.45 if code in {'MED-001','MED-004','CON-002'} and d>=21 else .70 if code in {'MED-003','CON-004'} and d>=21 else 1
   db.add(Usage(item_id=it.id,day=today-timedelta(days=27-d),qty=round(daily*factor*rng.uniform(.88,1.12),2)))
 db.commit(); db.close()
seed()

R={'LOW':0,'MEDIUM':1,'HIGH':2,'CRITICAL':3}
def intel(it,db):
 rows=db.query(Usage).filter(Usage.item_id==it.id).order_by(Usage.day).all(); vals=[x.qty for x in rows]
 base=mean(vals[:max(1,len(vals)//2)]) if vals else 0; recent=mean(vals[-7:]) if vals else 0; daily=sum(v*w for v,w in zip(vals[-7:],range(1,min(7,len(vals))+1)))/sum(range(1,min(7,len(vals))+1)) if vals else 0
 change=((recent-base)/base*100) if base else 0; usable=max(0,it.stock-it.reserve); dos=usable/daily if daily else 9999; lead_d=daily*it.lead
 stock='CRITICAL' if daily and dos<it.lead else 'HIGH' if daily and dos<it.lead+2 else 'MEDIUM' if daily and dos<it.lead+5 else 'LOW'
 reserve='CRITICAL' if it.stock<=it.reserve else 'HIGH' if it.stock<=it.reserve*1.25 else 'MEDIUM' if it.stock<=it.reserve*1.5 else 'LOW'
 abnormal='CRITICAL' if change>40 else 'HIGH' if change>30 else 'MEDIUM' if change>20 else 'LOW'
 days=(it.expiry-date.today()).days if it.expiry else None; expected=daily*max(0,days) if days is not None else None; leftover=max(0,it.stock-expected) if expected is not None else None
 expiry='CRITICAL' if days is not None and days<=0 else 'CRITICAL' if days is not None and days<=30 and leftover>it.stock*.25 else 'HIGH' if days is not None and days<=60 and leftover>it.stock*.20 else 'MEDIUM' if days is not None and days<=90 and leftover>it.stock*.15 else 'LOW'
 overall=max([stock,reserve,abnormal,expiry],key=lambda x:R[x]); factors=[]
 if stock in ('HIGH','CRITICAL'): factors.append(f'{dos:.1f} days of usable stock vs {it.lead:.0f}-day lead time.')
 if reserve in ('HIGH','CRITICAL'): factors.append(f'Stock is close to the emergency reserve of {it.reserve:g}.')
 if abnormal!='LOW': factors.append(f'Recent usage is {change:+.1f}% vs baseline.')
 if expiry!='LOW': factors.append(f'Estimated leftover at expiry: {leftover:.0f} units.')
 target=lead_d+it.buffer+it.reserve; raw=max(0,target-it.stock); order=ceil(raw/max(1,it.multiple))*max(1,it.multiple) if raw else 0
 if expiry in ('HIGH','CRITICAL') and stock not in ('HIGH','CRITICAL'): rec='DO NOT PROCURE'
 elif stock in ('HIGH','CRITICAL'): rec='PROCURE NOW'
 elif order: rec='PLAN PROCUREMENT'
 else: rec='NO ACTION'
 return dict(daily_forecast=round(daily,2),baseline_daily=round(base,2),recent_daily=round(recent,2),usage_change_pct=round(change,1),days_of_supply=round(dos,2),lead_time_demand=round(lead_d,2),stockout_risk=stock,expiry_risk=expiry,abnormal_usage_risk=abnormal,emergency_reserve_risk=reserve,overall_risk=overall,risk_factors=factors or ['No major supply-chain risk is currently detected.'],days_to_expiry=days,expected_consumption_before_expiry=round(expected,2) if expected is not None else None,potential_leftover=round(leftover,2) if leftover is not None else None,target_stock=round(target,2),recommended_order=order,recommendation=rec,history=[{'date':x.day.isoformat(),'actual':x.qty,'forecast':round(daily,2)} for x in rows])

def public(it): return {'id':it.id,'item_code':it.code,'name':it.name,'category':it.category,'current_stock':it.stock,'emergency_reserve':it.reserve,'unit':it.unit,'lead_time_days':it.lead,'safety_buffer':it.buffer,'expiry_date':it.expiry,'supplier':it.supplier}
app=FastAPI(title='MediPulse Intelligence API')
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://localhost:5173',
        'http://127.0.0.1:5173',
        'https://medipulse-1-kll5.onrender.com'
    ],
    allow_methods=['*'],
    allow_headers=['*']
)
class Login(BaseModel): email:str; password:str
@app.get('/api/health')
def health(): return {'status':'ok'}
@app.post('/api/auth/login')
def login(x:Login):
 if x.email.lower()=='admin@medipulse.com' and x.password=='demo123': return {'token':'demo-token','email':x.email.lower()}
 raise HTTPException(401,'Invalid email or password')
@app.get('/api/dashboard/summary')
def dashboard():
 db=Session(); items=db.query(Item).all(); xs=[intel(i,db) for i in items]
 category_counts={}
 for i in items: category_counts[i.category]=category_counts.get(i.category,0)+1
 suppliers=len({i.supplier for i in items if i.supplier})
 dos=[x['days_of_supply'] for x in xs if x['days_of_supply']<9999]
 attention=[]
 for i,x in zip(items,xs):
  if x['overall_risk'] in ('HIGH','CRITICAL'):
   attention.append({'id':i.id,'name':i.name,'item_code':i.code,'risk':x['overall_risk'],'action':x['recommendation']})
 attention=sorted(attention,key=lambda a:(-R[a['risk']],a['name']))[:5]
 avg_dos=round(mean(dos),1) if dos else 0
 db.close(); return {'total_items':len(items),'stockout_risks':sum(x['stockout_risk'] in ('HIGH','CRITICAL') for x in xs),'expiry_risks':sum(x['expiry_risk'] in ('HIGH','CRITICAL') for x in xs),'abnormal_usage':sum(x['abnormal_usage_risk']!='LOW' for x in xs),'critical_items':sum(x['overall_risk']=='CRITICAL' for x in xs),'risk_distribution':[{'risk':r,'count':sum(x['overall_risk']==r for x in xs)} for r in R],'category_distribution':[{'category':k,'count':v} for k,v in sorted(category_counts.items())],'supplier_count':suppliers,'average_days_of_supply':avg_dos,'attention_items':attention}
@app.get('/api/inventory')
def inventory(search:str='',category:str='All'):
 db=Session(); q=db.query(Item)
 if search: q=q.filter((Item.name.ilike(f'%{search}%'))|(Item.code.ilike(f'%{search}%')))
 if category!='All': q=q.filter(Item.category==category)
 out=[public(i) for i in q.order_by(Item.name).all()]; db.close(); return out
@app.get('/api/inventory/{id}')
def detail(id:int):
 db=Session(); it=db.get(Item,id)
 if not it: db.close(); raise HTTPException(404,'Item not found')
 x=intel(it,db); out={**public(it),'intelligence':{k:v for k,v in x.items() if k!='history'},'history':x['history']}; db.close(); return out
@app.get('/api/risks')
def risks():
 db=Session(); out=[]
 for it in db.query(Item).all():
  x=intel(it,db); out.append({'id':it.id,'item_code':it.code,'name':it.name,'category':it.category,'overall_risk':x['overall_risk'],'stockout_risk':x['stockout_risk'],'expiry_risk':x['expiry_risk'],'abnormal_usage_risk':x['abnormal_usage_risk'],'emergency_reserve_risk':x['emergency_reserve_risk'],'days_of_supply':x['days_of_supply'],'explanation':' '.join(x['risk_factors'])})
 db.close(); return sorted(out,key=lambda x:(-R[x['overall_risk']],x['name']))
@app.get('/api/procurement/recommendations')
def procurement():
 db=Session(); out=[]
 for it in db.query(Item).all():
  x=intel(it,db); out.append({'id':it.id,'item_code':it.code,'name':it.name,'category':it.category,'current_stock':it.stock,'target_stock':x['target_stock'],'recommended_order':x['recommended_order'],'overall_risk':x['overall_risk'],'recommendation':x['recommendation'],'reason':' '.join(x['risk_factors'])})
 db.close(); return sorted(out,key=lambda x:-x['recommended_order'])
@app.post('/api/data/upload')
async def upload(file:UploadFile=File(...)):
 if not file.filename.lower().endswith('.csv'): raise HTTPException(400,'Please upload a CSV file.')
 try: df=pd.read_csv(BytesIO(await file.read()))
 except Exception as e: raise HTTPException(400,f'Could not read CSV: {e}')
 required={'item_code','name','category','current_stock','emergency_reserve','lead_time_days'}; missing=required-set(df.columns)
 if missing: raise HTTPException(400,'Missing columns: '+', '.join(sorted(missing)))
 db=Session(); inserted=0; updated=0
 try:
  for _,r in df.iterrows():
   code=str(r['item_code']).strip()
   if not code or code.lower()=='nan':
    raise HTTPException(400,'item_code cannot be empty.')
   it=db.query(Item).filter(Item.code==code).first()
   if it:
    # Update only the current inventory fields. Usage/history rows are intentionally preserved.
    it.name=str(r['name']).strip()
    it.category=str(r['category']).strip()
    it.stock=float(r['current_stock'])
    it.reserve=float(r['emergency_reserve'])
    it.lead=float(r['lead_time_days'])
    if 'safety_buffer' in df.columns and pd.notna(r.get('safety_buffer')): it.buffer=float(r['safety_buffer'])
    if 'expiry_date' in df.columns and pd.notna(r.get('expiry_date')):
     parsed=pd.to_datetime(r.get('expiry_date'),errors='coerce')
     if pd.notna(parsed): it.expiry=parsed.date()
    if 'reorder_multiple' in df.columns and pd.notna(r.get('reorder_multiple')): it.multiple=max(1,int(float(r['reorder_multiple'])))
    if 'supplier' in df.columns and pd.notna(r.get('supplier')): it.supplier=str(r['supplier']).strip()
    if 'unit' in df.columns and pd.notna(r.get('unit')): it.unit=str(r['unit']).strip()
    updated+=1
   else:
    parsed=pd.to_datetime(r.get('expiry_date'),errors='coerce') if 'expiry_date' in df.columns and pd.notna(r.get('expiry_date')) else None
    expiry=parsed.date() if parsed is not None and pd.notna(parsed) else date.today()+timedelta(days=365)
    db.add(Item(code=code,name=str(r['name']).strip(),category=str(r['category']).strip(),stock=float(r['current_stock']),reserve=float(r['emergency_reserve']),lead=float(r['lead_time_days']),buffer=float(r.get('safety_buffer',0)) if pd.notna(r.get('safety_buffer')) else 0,expiry=expiry,multiple=max(1,int(float(r.get('reorder_multiple',10)))) if pd.notna(r.get('reorder_multiple',10)) else 10,supplier=str(r.get('supplier','CSV Supplier')).strip() if pd.notna(r.get('supplier','CSV Supplier')) else 'CSV Supplier',unit=str(r.get('unit','units')).strip() if pd.notna(r.get('unit','units')) else 'units'))
    inserted+=1
  db.commit()
 except HTTPException:
  db.rollback(); raise
 except Exception as e:
  db.rollback(); raise HTTPException(400,f'Could not process CSV: {e}')
 finally:
  db.close()
 return {'message':'CSV processed successfully','inserted':inserted,'updated':updated,'rows':len(df),'history_preserved':True}

@app.delete('/api/inventory/{id}')
def delete_inventory(id:int):
 db=Session(); it=db.get(Item,id)
 if not it:
  db.close(); raise HTTPException(404,'Item not found')
 # Remove the item's demand records with the inventory item so no orphan history remains.
 db.query(Usage).filter(Usage.item_id==it.id).delete(synchronize_session=False)
 db.delete(it); db.commit(); db.close()
 return {'message':f'{it.code} deleted successfully'}
