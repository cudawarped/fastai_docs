#AUTOGENERATED! DO NOT EDIT! File to edit: dev/02_data_pipeline.ipynb (unless otherwise specified).

__all__ = ['Transform', 'Pipeline']

from ..imports import *

from ..test import *

from ..core import *


class Transform():
    "A function that `encodes` if `filt` matches, and optionally `decodes`, with an optional `setup`"
    order,filt = 0,None

    def __init__(self, encodes=None, **kwargs):
        if encodes is not None: self.encodes=encodes
        for k,v in kwargs.items(): setattr(self, k, v)

    @classmethod
    def create(cls, f, filt=None):
        "classmethod: Turn `f` into a `Transform` unless it already is one"
        return f if hasattr(f,'decode') or isinstance(f,Transform) else cls(f)

    def __call__(self, o, filt=None, **kwargs):
        "Call `self.encodes` unless `filt` is passed and it doesn't match `self.filt`"
        if self.filt is not None and self.filt!=filt: return o
        return self.encodes(o, **kwargs)

    def decode(self, o, filt=None, **kwargs):
        "Call `self.decodes` unless `filt` is passed and it doesn't match `self.filt`"
        if self.filt is not None and self.filt!=filt: return o
        return self.decodes(o, **kwargs)

    def __repr__(self): return str(self.encodes) if self.__class__==Transform else str(self.__class__)
    def decodes(self, o, *args, **kwargs): return o

class Pipeline():
    "A pipeline of transforms, composed and applied for encode/decode, and setup one at a time"
    def __init__(self, tfms): self.tfms,self.inactiv = [],[Transform.create(t) for t in listify(tfms)]
    def __call__(self, x, **kwargs): return self.composed(x, **kwargs)
    def decode(self, x, **kwargs): return self.composed(x, rev=True, fname='decode', **kwargs)

    def composed(self, x, rev=False, fname='__call__', **kwargs):
        "Compose `{fname}` of all `self.tfms` (reversed if `rev`) on `x`"
        self.setup()
        tfms = reversed(self.tfms) if rev else self.tfms
        for f in tfms: x = opt_call(f, fname, x, **kwargs)
        return x

    def __repr__(self): return str(self.tfms)
    def delete(self, idx): del(self.tfms[idx])
    def remove(self, tfm): self.tfms.remove(tfm)

    def setup(self, items=None):
        "Call `setup` on all `self.tfms` and make them active in this pipeline"
        tfms = self.inactiv
        self.inactiv = []
        self.add(tfms, items)

    def add(self, tfms, items=None):
        "Call `setup` on all `tfms` and append them to this pipeline"
        for t in sorted(listify(tfms), key=lambda o: getattr(o, 'order', 0)):
            self.tfms.append(t)
            if hasattr(t, 'setup'): t.setup(items)

    def __getattr__(self, k):
        "Find last tfm in `self.tfms` that has attr `k`"
        try: return next(getattr(t,k) for t in reversed(self.tfms) if hasattr(t,k))
        except: raise AttributeError(k)

add_docs(
    Pipeline,
    __call__="Compose `__call__` of all `tfms` on `x`",
    decode="Compose `decode` of all `tfms` on `x`",
    delete="Delete transform `idx` from pipeline",
    remove="Remove `tfm` from pipeline",
)