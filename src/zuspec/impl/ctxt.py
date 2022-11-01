
class Ctxt(object):

    @classmethod
    def init(cls):
        from vsc_dataclasses.impl import Ctor as VscCtor
        from arl_dataclasses.impl import Ctor as ArlCtor
        import libarl.core as libarl

        ctxt = libarl.Arl.inst().mkContext()

        ArlCtor.init(ctxt)
        VscCtor.init(ctxt)

        pass