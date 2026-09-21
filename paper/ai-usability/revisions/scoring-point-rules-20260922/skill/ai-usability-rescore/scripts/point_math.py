"""Pure point-score arithmetic. Does not adjudicate evidence or convert old bounds."""
import math

POINT_STATUSES={'scored','not_applicable','blocked','needs_review','unscorable','not_assessed'}
def numeric(value,lo,hi,integer=False):
    if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or not lo<=value<=hi or (integer and int(value)!=value):
        raise ValueError('Invalid finite point value')
    return value

def score_m1(first_query=None,first_rank=None,*,decisive_records_verified=False,budget_exhausted=False):
    if (first_query is None)!=(first_rank is None):raise ValueError('Incomplete first-hit coordinates')
    if not decisive_records_verified:return None
    if first_query is None:return 1 if budget_exhausted else None
    numeric(first_query,1,4,True);numeric(first_rank,1,5,True)
    return (5 if first_rank==1 else 4) if first_query==1 else 3 if first_query==2 else 2

def score_m2(documents,*,source_inventory_resolved=False):
    if not source_inventory_resolved or not documents:return None
    ids=[d['id'] for d in documents]
    if len(ids)!=len(set(ids)):raise ValueError('Duplicate document')
    if any(set(d)&{'lower','upper','candidate_score','display_interval'} for d in documents):raise ValueError('Old interval/candidate inputs are not point adjudications')
    if any(d.get('status')!='scored' for d in documents):return None
    return math.fsum(numeric(d['score'],1,5,True) for d in documents)/len(documents)

def score_m5(possible_counts):
    """All admissible counts must map to one grade; never discard disputed candidates."""
    if not possible_counts:return None
    def band(n):
        numeric(n,0,10**9,True)
        return 1 if n==0 else 2 if n<=2 else 3 if n<=4 else 4 if n==5 else 5
    scores={band(n) for n in possible_counts}
    return next(iter(scores)) if len(scores)==1 else None

def score_m8(search,fetch,*,valid_complete_run=False):
    numeric(search,0,10**9,True);numeric(fetch,0,10**9,True)
    c=search+fetch
    if not valid_complete_run or c==0:return None
    return 5 if c<=2 else 4 if c<=4 else 3 if c<=6 else 2 if c<=8 else 1

def score_m11(metrics,*,confirmed_unavailable=None,m4_not_applicable=False):
    """Requires all active-channel point inputs, even if another channel saturates.

    confirmed_unavailable must already be independently adjudicated and carry
    reason/evidence. This function only validates their presence, not their truth.
    M9/M10 do not enter the formula. No source acquisition occurs here.
    """
    states=confirmed_unavailable or {}
    for key,state in states.items():
        if key not in ('official','third_party','prior') or state.get('status')!='confirmed_unavailable' or not state.get('reason') or not state.get('evidence'):
            raise ValueError('Unreviewed or unsupported channel-unavailable input')
    groups={'official':['M1','M2','M3'],'third_party':['M5','M6'],'prior':['M7']}
    required=[m for c,ids in groups.items() if c not in states for m in ids]+['M8']
    if not (m4_not_applicable and metrics.get('M4',{}).get('status')=='not_applicable'):required+=['M4']
    if any(set(metrics.get(m,{}))&{'lower','upper','candidate_score','display_interval'} for m in required):raise ValueError('Old interval/candidate inputs are not point adjudications')
    missing=[m for m in required if metrics.get(m,{}).get('status')!='scored' or metrics.get(m,{}).get('score') is None]
    if missing:
        statuses={metrics.get(m,{}).get('status','not_assessed') for m in missing}
        status='needs_review' if 'needs_review' in statuses else 'not_assessed' if 'not_assessed' in statuses else 'unscorable'
        return {'status':status,'score':None,'reason':'Required point inputs unavailable; no saturation shortcut or imputation.','missing_inputs':missing}
    values={m:numeric(metrics[m]['score'],1,5,m!='M2')/5 for m in required}
    channel={c:0.0 if c in states else math.prod(values[m] for m in ids) for c,ids in groups.items()}
    k=1-math.prod(1-v for v in channel.values())
    version=1.0 if m4_not_applicable and metrics.get('M4',{}).get('status')=='not_applicable' else .7+.3*values['M4']
    return {'status':'scored','score':100*k*version*(.9+.1*values['M8']), 'reason':'Calculated from adjudicated point inputs; not a probability.', 'derived_from':sorted(required,key=lambda s:int(s[1:]))}
