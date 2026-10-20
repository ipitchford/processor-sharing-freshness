"""Independent stationary-age sampling with non-exponential Erlang service.

For mean-one Erlang-k work, conditional on stationary population N, each
old residual has uniformly distributed remaining phase count in {1,...,k}.
Every phase has exponential work with rate k. These phase counts give a
finite-dimensional exact Markov simulation, without sampling N residuals.
"""
from pathlib import Path
import json
import math
import numpy as np

OUT=Path(__file__).resolve().parent

def sample_erlang(k,rho,count,seed):
    rng=np.random.default_rng(seed)
    initial=rng.geometric(1-rho,size=count)-1
    old=np.zeros((count,k),dtype=np.int64)
    remain=initial.copy()
    for j in range(k-1):
        old[:,j]=rng.binomial(remain,1/(k-j))
        remain-=old[:,j]
    old[:,k-1]=remain
    fresh=np.zeros_like(old)
    clock=np.zeros(count)
    alive=np.arange(count)
    events=0
    while len(alive):
        totals=(old[alive]+fresh[alive]).sum(axis=1)
        rates=np.where(totals>0,rho+k,rho)
        clock[alive]+=rng.exponential(size=len(alive))/rates
        births=rng.random(len(alive))<rho/rates
        fresh[alive[births],k-1]+=1
        pos=np.flatnonzero(~births)
        ids=alive[pos]
        counts=np.concatenate((old[ids],fresh[ids]),axis=1)
        draws=rng.random(len(ids))*counts.sum(axis=1)
        category=(draws[:,None]>=np.cumsum(counts,axis=1)).sum(axis=1)
        killed=category==k
        for c in range(2*k):
            affected=ids[category==c]
            if c<k:
                old[affected,c]-=1
                if c>0:old[affected,c-1]+=1
            elif c>k:
                fresh[affected,c-k]-=1
                fresh[affected,c-k-1]+=1
        keep=np.ones(len(alive),dtype=bool)
        keep[pos[killed]]=False
        events+=len(alive)
        alive=alive[keep]
    alpha=k/(k+1)
    scale=((k+1)*math.factorial(k)/k**k)**(1/(k+1))
    scaled=(1-rho)**alpha*clock
    theory_mean=scale*math.gamma(1+alpha)*math.gamma(2-alpha)
    theory_second=scale**2*math.gamma(1+2*alpha)*math.gamma(3-2*alpha)
    return {'shape':k,'rho':rho,'sample_count':count,'seed':seed,
        'events':events,'alpha':alpha,'scaled_mean':float(np.mean(scaled)),
        'scaled_mean_se':float(np.std(scaled,ddof=1)/math.sqrt(count)),
        'scaled_second_moment':float(np.mean(scaled**2)),
        'limit_mean':theory_mean,'limit_second_moment':theory_second}

def main():
    results={'service_mean':1,'method':'exact stationary phase-count simulation',
             'runs':[]}
    for k,n in [(2,100000),(3,50000)]:
        for j,r in enumerate([.99,.999,.9999]):
            row=sample_erlang(k,r,n,11200+10*k+j)
            results['runs'].append(row)
            print(json.dumps(row),flush=True)
    (OUT/'erlang_verification.json').write_text(json.dumps(results,indent=2)+'\n')

if __name__=='__main__':main()
