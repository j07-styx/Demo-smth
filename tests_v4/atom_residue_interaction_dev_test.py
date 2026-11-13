"""Synthetic engineering gate only; no public affinity data or test labels."""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import torch
from dynacpi.atom_residue_interaction_dev import AtomResidueInteraction

def main():
    torch.set_num_threads(2);torch.manual_seed(7131)
    m=AtomResidueInteraction(5,7,11,width=16).eval()
    a=torch.randn(3,4,5);r=torch.randn(3,6,7);fp=torch.randn(3,11)
    am=torch.ones(3,4,dtype=torch.bool);rm=torch.ones(3,6,dtype=torch.bool)
    am[:,-1]=False;rm[:,-1]=False
    b=torch.zeros(3,4,4,6);b[:,0,1,0]=1;b[:,1,0,0]=1
    with torch.no_grad():
        p,w=m(a,b,am,r,rm,fp)
        ap=torch.tensor([2,0,3,1]);rp=torch.tensor([4,1,5,0,3,2])
        q,_=m(a[:,ap],b[:,ap][:,:,ap],am[:,ap],r[:,rp],rm[:,rp],fp)
        assert torch.allclose(p,q,atol=1e-6)
        aa=a.clone();rr=r.clone();bb=b.clone()
        aa[:,-1]=1e6;rr[:,-1]=1e6;bb[:,-1]=1e6;bb[:,:,-1]=1e6
        q,_=m(aa,bb,am,rr,rm,fp);assert torch.allclose(p,q,atol=1e-6)
        q=torch.cat([m(a[i:i+1],b[i:i+1],am[i:i+1],r[i:i+1],rm[i:i+1],fp[i:i+1])[0] for i in range(3)])
        assert torch.allclose(p,q,atol=1e-6)
        q,_=m(a,b*0,am,r,rm,fp);assert not torch.allclose(p,q,atol=1e-7)
        assert torch.all(w[:,-1]==0) and torch.all(w[:,:,-1]==0)
    try:m(a,b,am*False,r,rm,fp);raise AssertionError('Empty atom set accepted')
    except ValueError:pass
    m(a,b,am,r,rm,fp)[0].square().sum().backward()
    for layer in [m.atom,m.residue,m.bond_message[0],m.pair_value[0]]:
        assert layer.weight.grad.abs().sum()>0

    # Full factorial toy labels have zero compound and protein main effects.
    # Neither target offsets nor chemical-only outputs can fit this signal.
    torch.manual_seed(7132)
    c=torch.tensor([-1.,-.5,.5,1.]);p=c.clone()
    ci=torch.arange(4).repeat_interleave(4);pi=torch.arange(4).repeat(4)
    aa=torch.zeros(16,3,5);rr=torch.zeros(16,4,7)
    aa[:,:,0]=c[ci,None];rr[:,:,0]=p[pi,None]
    bb=torch.zeros(16,3,3,6);bb[:,0,1,0]=1;bb[:,1,0,0]=1
    ma=torch.ones(16,3,dtype=torch.bool);mr=torch.ones(16,4,dtype=torch.bool);f=torch.zeros(16,11)
    y=c[ci]*p[pi];assert torch.allclose(y.reshape(4,4).mean(0),torch.zeros(4))
    model=AtomResidueInteraction(5,7,11,width=16)
    opt=torch.optim.AdamW(model.parameters(),lr=.003,weight_decay=0)
    initial=float(((model(aa,bb,ma,rr,mr,f)[0]-y)**2).mean().detach())
    for step in range(400):
        opt.zero_grad();out,_=model(aa,bb,ma,rr,mr,f);loss=((out-y)**2).mean();loss.backward();opt.step()
    model.eval()
    with torch.no_grad():final=float(((model(aa,bb,ma,rr,mr,f)[0]-y)**2).mean())
    assert final<.01*initial and final<.001
    print(json.dumps({'evidence':'SYNTHETIC_ENGINEERING_ONLY','permutation_invariance':True,'padding_invariance':True,'batch_parity':True,'bond_sensitivity':True,'empty_input_rejected':True,'upstream_gradients':True,'toy_interaction_initial_mse':initial,'toy_interaction_final_mse':final,'steps':400,'biological_gain_demonstrated':False},indent=2))
if __name__=='__main__':main()
