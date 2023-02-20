
class Ctxt(object):

    @classmethod
    def init(cls):
        from vsc_dataclasses.impl import Ctor as VscCtor
        from zsp_dataclasses.impl import Ctor as ZspCtor
        import zsp_arl_dm.core as arl_dm

        ctxt = arl_dm.Factory.inst().mkContext()

        ZspCtor.init(ctxt)
        VscCtor.init(ctxt)

        pass