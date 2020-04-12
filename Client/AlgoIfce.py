import abc


class PRES(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def KeyGen(self, *args):
        pass

    @abc.abstractmethod
    def Enc(self, *args):
        pass

    @abc.abstractmethod
    def Trapdoor(self, *args):
        pass

    @abc.abstractmethod
    def ReKeyGen(self, *args):
        pass

    @abc.abstractmethod
    def Search(self, *args):
        pass

    @abc.abstractmethod
    def TokenGen(self, *args):
        pass

    @abc.abstractmethod
    def ReEnc(self, *args):
        pass

    @abc.abstractmethod
    def Test(self, *args):
        pass

    @abc.abstractmethod
    def Dec(self, *args):
        pass
