"""Exact finite-buffer sanity checks and iid stationary AoI sampling.

The infinite-buffer sampler initialises queue length from its exact stationary
geometric law. It then samples time until the first completion of a newly
arrived customer. This random variable has the stationary AoI distribution.
No long-run warm-up or nearly-unstable mixing simulation is used.
"""
from pathlib import Path
import json
import math
import numpy as np
from fractions import Fraction

OUT = Path(__file__).resolve().parent

def rational_solve(mat,rhs):
    n=len(mat)
    augmented=[list(mat[i])+[rhs[i]] for i in range(n)]
    for j in range(n):
        pivot=next(i for i in range(j,n) if augmented[i][j])
        augmented[j],augmented[pivot]=augmented[pivot],augmented[j]
        scale=augmented[j][j]
        augmented[j]=[v/scale for v in augmented[j]]
        for i in range(n):
            if i!=j and augmented[i][j]:
                scale=augmented[i][j]
                augmented[i]=[a-scale*b for a,b in zip(augmented[i],augmented[j])]
    return [row[-1] for row in augmented]

def finite_capacity_mean(capacity, arrival=Fraction(1,2), service=Fraction(1)):
    states=[(m,n) for m in range(capacity+1) for n in range(capacity-m+1)]
    index={state:i for i,state in enumerate(states)}
    mat=[[Fraction(0) for _ in states] for _ in states]
    for i,(m,n) in enumerate(states):
        total=m+n
        if total<capacity:
            mat[i][i]+=arrival
            mat[i][index[(m,n+1)]]-=arrival
        if m:
            r=service*Fraction(m,total)
            mat[i][i]+=r
            mat[i][index[(m-1,n)]]-=r
        if n:
            mat[i][i]+=service*Fraction(n,total)
    t=rational_solve(mat,[Fraction(1) for _ in states])
    rho=arrival/service
    weights=[rho**m for m in range(capacity+1)]
    return sum(weights[m]*t[index[(m,0)]] for m in range(capacity+1))/sum(weights)

def sample_age(rho, count, seed):
    rng=np.random.default_rng(seed)
    old=rng.geometric(1-rho,size=count)-1
    fresh=np.zeros(count,dtype=np.int64)
    times=np.zeros(count)
    alive=np.arange(count)
    events=0
    while len(alive):
        total=old[alive]+fresh[alive]
        rate=np.where(total>0,1+rho,rho)
        times[alive]+=rng.exponential(size=len(alive))/rate
        births=rng.random(len(alive))<rho/rate
        fresh[alive[births]]+=1
        service_slots=alive[~births]
        denom=old[service_slots]+fresh[service_slots]
        dead=rng.random(len(service_slots))<fresh[service_slots]/denom
        old[service_slots[~dead]]-=1
        keep=np.ones(len(alive),dtype=bool)
        service_positions=np.flatnonzero(~births)
        keep[service_positions[dead]]=False
        alive=alive[keep]
        events+=len(keep)
    scaled=math.sqrt(1-rho)*times
    return {
        'rho':rho,'sample_count':count,'seed':seed,'events':events,
        'scaled_mean':float(np.mean(scaled)),
        'scaled_mean_se':float(np.std(scaled,ddof=1)/math.sqrt(count)),
        'scaled_second_moment':float(np.mean(scaled**2)),
        'scaled_survival':{str(s):float(np.mean(scaled>s)) for s in [.25,.5,1.,2.,3.,4.]},
        'mean_age':float(np.mean(times)),
        'mean_C':float(np.mean(times)-1-1/rho),
    }

def main():
    finite={str(k):str(finite_capacity_mean(k)) for k in [1,2,3]}
    l=Fraction(1,2);mu=Fraction(1)
    published_k2=(5*l**4+9*l**3*mu+8*l**2*mu**2+6*l*mu**3+2*mu**4)/(2*l*mu*(l+mu)*(l*l+l*mu+mu*mu))
    assert finite_capacity_mean(2)==published_k2
    results={
        'method':'independent exact stationary first-fresh-completion samples',
        'finite_capacity_exact_means_at_rho_half':finite,
        'capacity2_matches_published_formula':True,
        'limiting_mean':math.pi/(2*math.sqrt(2)),
        'limiting_second_moment':2.,
        'runs':[sample_age(r,200000,88101+j) for j,r in enumerate([.5,.9,.99,.999,.9999])]
    }
    (OUT/'verification.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))

if __name__=='__main__': main()
