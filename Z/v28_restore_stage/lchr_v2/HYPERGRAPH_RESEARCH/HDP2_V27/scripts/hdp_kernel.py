"""Offline exact incidence/matching/degree-preserving switches; CPU Numba."""
import numpy as np
from numba import njit,prange

@njit(cache=True)
def matching(B):
    """Exact deterministic augmenting-path bipartite matching, never greedy."""
    nl,nr=B.shape;left=np.full(nl,-1,np.int64);right=np.full(nr,-1,np.int64);answer=0
    for root in range(nl):
        if left[root]>=0:continue
        queue=np.empty(nl,np.int64);queue[0]=root;head=0;tail=1;seen=np.zeros(nl,np.bool_);seen[root]=True;prev=np.full(nr,-1,np.int64);found=-1
        while head<tail and found<0:
            u=queue[head];head+=1
            for w in range(nr):
                if not B[u,w] or prev[w]>=0:continue
                prev[w]=u
                if right[w]<0:found=w;break
                nxt=right[w]
                if not seen[nxt]:seen[nxt]=True;queue[tail]=nxt;tail+=1
        if found>=0:
            while found>=0:
                u=prev[found];old=left[u];left[u]=found;right[found]=u;found=old
            answer+=1
    return answer

@njit(cache=True)
def side(anchor,other,u,v,target,ptr,mem,degree):
    rows=[];graph=[]
    for j in range(ptr[anchor],ptr[anchor+1]):
        center=mem[j]
        if target and (center==other or center==anchor and degree[anchor]==1):continue
        row=[];contains_other=False
        for k in range(ptr[center],ptr[center+1]):
            w=mem[k]
            if target and (center==u and w==v or center==v and w==u):continue
            if w!=anchor:graph.append(w)
            if w==other:contains_other=True
            if w!=u and w!=v:row.append(w)
        if not contains_other:rows.append(np.asarray(row,np.int64))
    return rows,np.unique(np.asarray(graph,np.int64))

@njit(cache=True)
def assemble(u,v,ptr,mem,degree):
    star=mem[ptr[u]:ptr[u+1]];j=np.searchsorted(star,v);target=j<len(star) and star[j]==v and u!=v
    ru,gu=side(u,v,u,v,target,ptr,mem,degree);rv,gv=side(v,u,u,v,target,ptr,mem,degree);support=[]
    for row in ru:
        for w in row:support.append(w)
    for row in rv:
        for w in row:support.append(w)
    ids=np.unique(np.asarray(support,np.int64));A=np.zeros((len(ru),len(ids)),np.bool_);C=np.zeros((len(rv),len(ids)),np.bool_)
    for i,row in enumerate(ru):
        for w in row:A[i,np.searchsorted(ids,w)]=True
    for i,row in enumerate(rv):
        for w in row:C[i,np.searchsorted(ids,w)]=True
    common=0
    for w in gu:
        if w==u or w==v:continue
        j=np.searchsorted(gv,w)
        if j<len(gv) and gv[j]==w:common+=1
    return A,C,len(gu),len(gv),common

@njit(cache=True)
def compatibility(A,C):
    B=np.zeros((A.shape[0],C.shape[0]),np.bool_);multiplicity=0;supports=0
    for w in range(A.shape[1]):
        cu=0;cv=0
        for i in range(A.shape[0]):cu+=int(A[i,w])
        for j in range(C.shape[0]):cv+=int(C[j,w])
        multiplicity+=cu*cv;supports+=int(cu>0 and cv>0)
        if cu and cv:
            for i in range(A.shape[0]):
                if A[i,w]:
                    for j in range(C.shape[0]):
                        if C[j,w]:B[i,j]=True
    return B,multiplicity,supports

@njit(cache=True)
def eligible(A):
    for i in range(A.shape[0]):
        for j in range(i):
            one=False;two=False
            for w in range(A.shape[1]):
                if A[i,w] and not A[j,w]:one=True
                if A[j,w] and not A[i,w]:two=True
                if one and two:return True
    return False

@njit(cache=True)
def random_index(state,n):
    state=np.uint64(state*np.uint64(6364136223846793005)+np.uint64(1442695040888963407))
    return state,int((state>>np.uint64(32))%np.uint64(n))

@njit(cache=True)
def rewire(original,state):
    A=original.copy();nnz=int(A.sum());can=eligible(A);accepted=attempted=0
    if can:
        er=np.empty(nnz,np.int64);ew=np.empty(nnz,np.int64);k=0
        for i in range(A.shape[0]):
            for w in range(A.shape[1]):
                if A[i,w]:er[k]=i;ew[k]=w;k+=1
        goal=max(10,5*nnz);cap=max(100,50*nnz)
        while accepted<goal and attempted<cap:
            attempted+=1;state,p=random_index(state,nnz);state,q=random_index(state,nnz);i,j=er[p],er[q];w,z=ew[p],ew[q]
            if i==j or w==z or A[i,z] or A[j,w]:continue
            A[i,w]=False;A[j,z]=False;A[i,z]=True;A[j,w]=True;ew[p]=z;ew[q]=w;accepted+=1
    for i in range(A.shape[0]):assert A[i].sum()==original[i].sum()
    for w in range(A.shape[1]):assert A[:,w].sum()==original[:,w].sum()
    changed=int(np.count_nonzero(A!=original))
    return A,accepted,attempted,changed,can

@njit(cache=True)
def candidate(u,v,seed,ptr,mem,degree):
    A,C,du,dv,lg=assemble(u,v,ptr,mem,degree);B,m,s=compatibility(A,C);lh=matching(B)
    As,au,tu,chu,eu=rewire(A,seed);Cs,av,tv,chv,ev=rewire(C,np.uint64(seed^np.uint64(11400714819323198485)));Bs,ms,ss=compatibility(As,Cs);assert m==ms and s==ss;lsh=matching(Bs);nnzu=int(A.sum());nnzv=int(C.sum());fraction=(chu+chv)/max(2*(nnzu+nnzv),1)
    return np.asarray([A.shape[0],C.shape[0],lh,lg,int(B.sum()),m,s,lsh,du,dv,au,tu,av,tv,fraction,int(eu),int(ev),int(lh!=lsh),2,int(Bs.sum()),A.shape[1],nnzu,nnzv],np.float64)

@njit(cache=True,parallel=True)
def compute(pairs,seeds,ptr,mem,degree):
    result=np.empty((len(pairs),23),np.float64)
    for i in prange(len(pairs)):result[i]=candidate(pairs[i,0],pairs[i,1],seeds[i],ptr,mem,degree)
    return result
